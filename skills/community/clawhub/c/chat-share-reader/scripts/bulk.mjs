#!/usr/bin/env node
// 登录态批量导出：在已登录的浏览器页面里发请求，把账号下的全部会话拉成 markdown。
//
// 和 read.mjs 的分工：那个抓别人给的公开分享链接，一次一条；这个抓你自己账号里的
// 全部历史，一次几百上千条。两者的接口不是同一个：分享走免认证的 /share/<id>，
// 这里走登录后才放行的列表与详情接口。
//
// 走浏览器通道取登录态，复用浏览器里已有的 session，不需要导出 cookie，
// 也不需要解密 Chrome 的 cookie 库。两条后端都行：
// - opencli：直接借用你日常浏览器的登录态，开箱即用
// - CDP：脚本拉起一个专用 profile 的 Chrome，第一次要在弹出的窗口里手动登录一次，
//   cookie 落在 ~/.chat-share-reader/chrome-profile，之后不用再登
//
// 用法：
//   node scripts/bulk.mjs sites
//   node scripts/bulk.mjs list --site deepseek
//   node scripts/bulk.mjs export --site deepseek --out ../../25-chatArchive/archive --limit 20
//   node scripts/bulk.mjs export --site deepseek --out DIR --since 2026-09-01
import { mkdir, readFile, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { setTimeout as sleep } from 'node:timers/promises';
import { available, createSession } from './lib/backend/index.mjs';
import { buildDoc, safeName } from './lib/md.mjs';
import { t } from './lib/i18n.mjs';

const SESSION = 'csr-bulk';
// 页面里的 fetch 和 XHR 都可能被站点自己的脚本改写：Qwen 的阿里埋点包了 fetch，WAF 又
// 挂了 XHR；豆包同类。同源空白 iframe 里的 fetch 是没被碰过的原生实现，优先用它，
// 拿不到再退回顶层 XHR，最后才用被改写过的 fetch。
const PRELUDE = `
window.__auth = function () {
  var cands = [];
  for (var i = 0; i < localStorage.length; i++) {
    var k = localStorage.key(i);
    if (!/token|jwt|auth|session/i.test(k)) continue;
    cands.push([k, localStorage.getItem(k) || ""]);
  }
  for (var j = 0; j < cands.length; j++) {
    var v = cands[j][1];
    if (/^ey[A-Za-z0-9_-]+\\.[A-Za-z0-9_-]+\\.[A-Za-z0-9_-]+$/.test(v)) return v;
    try {
      var o = JSON.parse(v);
      if (o && typeof o.value === "string" && o.value) return o.value;
      if (o && typeof o.access_token === "string") return o.access_token;
    } catch (e) {}
  }
  for (var m = 0; m < cands.length; m++) {
    var w = cands[m][1];
    if (w && w.length > 20 && w.length < 4000 && w.charAt(0) !== "{") return w;
  }
  return "";
};
window.__unauthed = function (r) {
  if (!r) return false;
  if (r.status === 401 || r.status === 403) return true;
  var j = r.json;
  if (j && (j.code === 40003 || j.code === 40001 || j.code === 401)) return true;
  if (j && j.detail && /unauthor|forbidden|credential/i.test(String(j.detail))) return true;
  var t = String(r.text || "");
  if (t.indexOf("Unauthorized") >= 0 && t.length < 400) return true;
  return false;
};
window.__raw = async function (url, opts) {
  var abs = new URL(url, location.href).href;
  var parse = function (t) { try { return JSON.parse(t); } catch (e) { return null; } };
  try {
    var f = document.createElement("iframe");
    f.style.display = "none";
    document.body.appendChild(f);
    var ctl = new AbortController();
    var timer = setTimeout(function () { ctl.abort(); }, (opts && opts.timeout) || 25000);
    var r = await f.contentWindow.fetch(abs, {
      credentials: "include",
      headers: (opts && opts.headers) || {},
      signal: ctl.signal
    });
    var t = await r.text();
    clearTimeout(timer);
    f.remove();
    return { status: r.status, text: t, json: parse(t), via: "iframe" };
  } catch (e) {}
  return await new Promise(function (res) {
    try {
      var x = new XMLHttpRequest();
      x.open((opts && opts.method) || "GET", url, true);
      x.withCredentials = true;
      x.timeout = (opts && opts.timeout) || 25000;
      var h = (opts && opts.headers) || {};
      for (var q in h) x.setRequestHeader(q, h[q]);
      x.onload = function () { res({ status: x.status, text: x.responseText, json: parse(x.responseText), via: "xhr" }); };
      x.onerror = function () { res({ status: 0, error: "network", text: "", via: "xhr" }); };
      x.ontimeout = function () { res({ status: 0, error: "timeout", text: "", via: "xhr" }); };
      x.send((opts && opts.body) || null);
    } catch (e) { res({ status: 0, error: String(e), text: "", via: "xhr" }); }
  });
};
window.__req = async function (url, opts) {
  var first = await window.__raw(url, opts);
  if (!window.__unauthed(first)) return first;
  var tok = window.__auth();
  if (!tok) return first;
  var h2 = Object.assign({}, (opts && opts.headers) || {});
  h2.Authorization = "Bearer " + tok;
  var second = await window.__raw(url, { method: opts && opts.method, body: opts && opts.body, timeout: opts && opts.timeout, headers: h2 });
  second.retried = true;
  return second;
};
window.__apis = function () {
  return performance.getEntriesByType("resource")
    .map(function (e) { return e.name; })
    .filter(function (n) { return n.indexOf("/api/") >= 0 || n.indexOf("/rest/") >= 0 || n.indexOf("/samantha/") >= 0; });
};
`;


// 每个站点的抓取脚本都在页面上下文执行，靠 window.__arg 传参、window.__list /
// window.__batch / window.__err 回传。脚本里可以随便用引号和花括号，因为注入前
// 会整段 base64，不经过 shell。
const SITES = {
  deepseek: {
    label: 'DeepSeek',
    entry: 'https://chat.deepseek.com/',
    loginProbe: 'window.__probe = document.cookie.includes("ds_session_id") ? "in" : "out"',
    listScript: `(async () => { const req = window.__req;
      const out = [];
      let ts = null;
      for (let page = 0; page < 500; page++) {
        const url = ts
          ? "/api/v0/chat_session/fetch_page?count=100&lte_time=" + ts
          : "/api/v0/chat_session/fetch_page?count=100";
        const r = await req(url);
        const j = r.json || {};
        if (j.code !== 0) { window.__err = JSON.stringify(j) + " status=" + r.status; return; }
        const biz = (j.data && j.data.biz_data) || {};
        const arr = biz.chat_sessions || [];
        for (const s of arr) out.push({ id: s.id, title: s.title || "", updatedAt: s.updated_at || 0 });
        if (!biz.has_more || !arr.length) break;
        ts = arr[arr.length - 1].updated_at;
        await new Promise((r) => setTimeout(r, 300));
      }
      window.__list = JSON.stringify(out);
    })()`,
    detailScript: `(async () => { const req = window.__req;
      const ids = window.__arg || [];
      const out = [];
      for (const it of ids) {
        try {
          const r = await req("/api/v0/chat/history_messages?chat_session_id=" + it.id);
          const j = r.json || {};
          const biz = (j.data && j.data.biz_data) || {};
          const msgs = (biz.chat_messages || []).map((m) => {
            const NL = String.fromCharCode(10);
            return {
              role: m.role === "USER" ? "user" : "assistant",
              time: m.inserted_at ? new Date(m.inserted_at * 1000).toISOString() : "",
              body: (m.fragments || []).map((f) => {
                if (f.type === "REQUEST" || f.type === "RESPONSE") return String(f.content || "");
                if (f.type === "THINK") return "> 思考过程" + NL + "> " + String(f.content || "").trim().split(NL).join(NL + "> ");
                if (f.type === "SEARCH") return "> 联网检索：" + String(f.content || "");
                return "";
              }).filter(Boolean).join(NL + NL).trim()
            };
          }).filter((m) => m.body);
          out.push({ id: it.id, title: it.title || "", updatedAt: it.updatedAt || 0, messages: msgs });
        } catch (e) {
          out.push({ id: it.id, error: String(e) });
        }
        await new Promise((r) => setTimeout(r, 250));
      }
      window.__batch = JSON.stringify(out);
    })()`,
  },

  qwen: {
    label: 'Qwen',
    entry: 'https://chat.qwen.ai/',
    listScript: `(async () => { const req = window.__req;
      const out = [];
      let page = 1;
      for (let i = 0; i < 500; i++) {
        const r = await req("/api/v1/chats/?page=" + page);
        const j = r.json || {};
        if (!r.status || r.status >= 400) { window.__err = (r.error || ("status " + r.status)) + " " + (r.text || "").slice(0, 200); return; }
        const arr = (j.data && j.data.chats) || j.chats || (Array.isArray(j.data) ? j.data : []);
        if (!arr.length) break;
        for (const s of arr) out.push({ id: s.id, title: s.title || "", updatedAt: s.updated_at || s.timestamp || 0 });
        if (arr.length < 20) break;
        page += 1;
        await new Promise((r) => setTimeout(r, 300));
      }
      window.__list = JSON.stringify(out);
    })()`,
    detailScript: `(async () => { const req = window.__req;
      const ids = window.__arg || [];
      const out = [];
      for (const it of ids) {
        try {
          const r = await req("/api/v1/chats/" + it.id);
          const j = r.json || {};
          const msgs = (j.messages || (j.data && j.data.messages) || []).map((m) => ({
            role: m.role === "user" ? "user" : "assistant",
            time: m.created_at || m.timestamp || "",
            body: (m.content || "").trim()
          })).filter((m) => m.body);
          out.push({ id: it.id, title: it.title || "", updatedAt: it.updatedAt || 0, messages: msgs });
        } catch (e) {
          out.push({ id: it.id, error: String(e) });
        }
        await new Promise((r) => setTimeout(r, 250));
      }
      window.__batch = JSON.stringify(out);
    })()`,
  },

  kimi: {
    label: 'Kimi',
    entry: 'https://www.kimi.com/',
    listScript: `(async () => { const req = window.__req;
      const out = [];
      let cursor = "";
      for (let i = 0; i < 500; i++) {
        const url = "/api/chat/list?page_size=50" + (cursor ? "&cursor=" + encodeURIComponent(cursor) : "");
        const r = await req(url);
        const j = r.json || {};
        if (!r.status || r.status >= 400) { window.__err = (r.error || ("status " + r.status)) + " " + (r.text || "").slice(0, 200); return; }
        const arr = (j.data && (j.data.chats || j.data.list)) || j.chats || [];
        if (!arr.length) break;
        for (const s of arr) out.push({ id: s.id, title: s.name || s.title || "", updatedAt: s.update_time || s.updated_at || 0 });
        cursor = (j.data && j.data.next_cursor) || "";
        if (!cursor) break;
        await new Promise((r) => setTimeout(r, 300));
      }
      window.__list = JSON.stringify(out);
    })()`,
    detailScript: `(async () => { const req = window.__req;
      const ids = window.__arg || [];
      const out = [];
      for (const it of ids) {
        try {
          const r = await req("/api/chat/" + it.id + "/detail");
          const j = r.json || {};
          const src = (j.data && (j.data.messages || j.data.chat && j.data.chat.messages)) || [];
          const msgs = src.map((m) => ({
            role: (m.role === "user" || m.sender === "user") ? "user" : "assistant",
            time: m.create_time || m.created_at || "",
            body: (typeof m.content === "string" ? m.content : (m.content && m.content.text) || "").trim()
          })).filter((m) => m.body);
          out.push({ id: it.id, title: it.title || "", updatedAt: it.updatedAt || 0, messages: msgs });
        } catch (e) {
          out.push({ id: it.id, error: String(e) });
        }
        await new Promise((r) => setTimeout(r, 250));
      }
      window.__batch = JSON.stringify(out);
    })()`,
  },

  chatgpt: {
    label: 'ChatGPT',
    entry: 'https://chatgpt.com/',
    // 2026-11 起 backend-api 要 Bearer token，光有 cookie 会返回 total:0 而不报错，
    // 是最容易误判成「账号没有历史」的坑。token 从 /api/auth/session 拿。
    // 另外 tpp 空间与普通空间是两套列表，两个都要拉。
    listScript: `(async () => { const req = window.__req;
      const ses = await req("/api/auth/session");
      const tok = (ses.json && ses.json.accessToken) || "";
      if (!tok) { window.__err = "拿不到 accessToken，登录态可能已失效"; return; }
      const H = { Authorization: "Bearer " + tok };
      const out = [];
      const seen = new Set();
      const queries = ["exclude_conversation_origin=tpp", "conversation_origin=tpp"];
      for (const q of queries) {
        let offset = 0;
        for (let i = 0; i < 300; i++) {
          const url = "/backend-api/conversations?expand=false&hide_snorlax=false&is_archived=false&is_starred=false&order=updated&limit=100&" + q + "&offset=" + offset;
          const r = await req(url, { headers: H });
          if (r.status === 401 || r.status === 403) { window.__err = "列表 " + r.status; return; }
          const j = r.json || {};
          const arr = j.items || [];
          for (const x of arr) {
            if (seen.has(x.id)) continue;
            seen.add(x.id);
            out.push({ id: x.id, title: x.title || "", updatedAt: x.update_time || x.create_time || 0 });
          }
          if (arr.length < 100) break;
          offset += arr.length;
          await new Promise((r) => setTimeout(r, 300));
        }
      }
      window.__list = JSON.stringify(out);
    })()`,
    detailScript: `(async () => { const req = window.__req;
      const ses = await req("/api/auth/session");
      const tok = (ses.json && ses.json.accessToken) || "";
      const H = { Authorization: "Bearer " + tok };
      const ids = window.__arg || [];
      const out = [];
      for (const it of ids) {
        try {
          const r = await req("/backend-api/conversation/" + it.id, { headers: H });
          const j = r.json || {};
          const mapping = j.mapping || {};
          let cur = j.current_node;
          const chain = [];
          const guard = new Set();
          while (cur && mapping[cur] && !guard.has(cur)) {
            guard.add(cur);
            chain.push(mapping[cur]);
            cur = mapping[cur].parent;
          }
          chain.reverse();
          const msgs = [];
          for (const node of chain) {
            const msg = node && node.message;
            if (!msg) continue;
            const role = msg.author && msg.author.role;
            if (role !== "user" && role !== "assistant") continue;
            if (msg.metadata && msg.metadata.is_visually_hidden_from_conversation) continue;
            const parts = (msg.content && msg.content.parts) || [];
            const body = parts.filter((p) => typeof p === "string").join(String.fromCharCode(10, 10)).trim();
            if (!body) continue;
            msgs.push({ role, time: msg.create_time || "", body });
          }
          out.push({ id: it.id, title: j.title || it.title || "", updatedAt: it.updatedAt || 0, messages: msgs });
        } catch (e) {
          out.push({ id: it.id, error: String(e) });
        }
        await new Promise((r) => setTimeout(r, 250));
      }
      window.__batch = JSON.stringify(out);
    })()`,
  },

  gemini: {
    label: 'Gemini',
    entry: 'https://gemini.google.com/app',
    // 走 DOM：正文由 Angular 渲染，接口是 batchexecute RPC（要内部 token，逆向成本高）。
    // 侧边栏分组不显示时间，列表也拿不到 create_time，所以日期留空，md 里标注。
    // 坑：后台标签会被浏览器节流，Angular 不渲染，必须前台窗口打开并且等十几秒。
    domMode: true,
    foreground: true,
    reuseTab: true,
    domDelay: 2500,
    detailUrl: (id) => `https://gemini.google.com/app/${id}`,
    listScript: `(async () => {
      const wait = (ms) => new Promise((r) => setTimeout(r, ms));
      const cnt = () => document.querySelectorAll('a[href*="/app/"]').length;
      // Angular 首屏慢，侧边栏还没出链接就开始滚，会在 0 条时判定「稳定」并提前收工。
      for (let i = 0; i < 25; i++) {
        if (cnt() > 0) break;
        await wait(1000);
      }
      const rounds = window.__max > 0 ? 2 : 120;
      let stable = 0;
      for (let i = 0; i < rounds; i++) {
        const b = cnt();
        const sc = document.querySelector("infinite-scroller") || document.querySelector("conversations-list");
        if (sc) sc.scrollTop = sc.scrollHeight;
        else window.scrollTo(0, document.body.scrollHeight);
        await wait(1500);
        if (cnt() === b) { stable += 1; if (stable >= 5) break; } else stable = 0;
      }
      const NL = String.fromCharCode(10);
      const seen = new Map();
      document.querySelectorAll('a[href*="/app/"]').forEach((a) => {
        const m = (a.getAttribute("href") || "").match(/\\/app\\/([0-9a-f]+)/);
        if (!m) return;
        const title = (a.innerText || "").trim().split(NL)[0];
        if (!seen.has(m[1])) seen.set(m[1], { id: m[1], title: title, updatedAt: "" });
      });
      window.__list = JSON.stringify(Array.from(seen.values()));
    })()`,
    extractScript: `(async () => {
      const NL = String.fromCharCode(10);
      const wait = (ms) => new Promise((r) => setTimeout(r, ms));
      const ready = () => {
        const mr = document.querySelector("model-response");
        const uq = document.querySelector("user-query");
        return !!(uq && mr && String(mr.innerText || "").trim().length > 40);
      };
      for (let i = 0; i < 25; i++) {
        if (ready()) break;
        await wait(1000);
      }
      // 虚拟滚动：只渲染视口附近。单轮会话不值得滚（省 20 秒），多轮才往上翻。
      const box = document.querySelector("chat-window") || document.querySelector("infinite-scroller");
      let last = -1;
      const rounds = document.querySelectorAll("user-query, model-response").length > 3 ? 30 : 0;
      for (let i = 0; i < rounds; i++) {
        const n = document.querySelectorAll("user-query, model-response").length;
        if (n === last) break;
        last = n;
        if (box) box.scrollTop = 0;
        window.scrollTo(0, 0);
        await wait(700);
      }
      const nodes = Array.prototype.slice.call(document.querySelectorAll("user-query, model-response"));
      const msgs = [];
      for (const n of nodes) {
        const isUser = n.tagName.toLowerCase() === "user-query";
        let txt = n.innerText || "";
        txt = txt.replace(/^(你說了|You said)\\s*/, "").replace(/^(Gemini 說了|Gemini said)\\s*/, "").trim();
        if (txt) msgs.push({ role: isUser ? "user" : "assistant", time: "", body: txt });
      }
      const title = (document.title || "").replace(/\\s*-\\s*Google Gemini\\s*$/, "").trim();
      return JSON.stringify({ title: title, messages: msgs, nodes: nodes.length });
    })()`,
  },

  perplexity: {
    label: 'Perplexity',
    entry: 'https://www.perplexity.ai/',
    // 列表没有独立接口（/rest/thread/list_ask_threads 会被当成 thread id 解析，返回
    // Invalid UUID），只能从侧边栏 /session/ 链接收集。详情走 /rest/thread/<id>。
    // 正文在 entry.text 这个 JSON 数组里，取 step_type === FINAL 的 content.answer，
    // 而这个 answer 本身又是一层 JSON 字符串，要二次 parse。
    listScript: `(async () => {
      const wait = (ms) => new Promise((r) => setTimeout(r, ms));
      const cnt = () => document.querySelectorAll('a[href^="/session/"]').length;
      const rounds = window.__max > 0 ? 2 : 60;
      let stable = 0;
      for (let i = 0; i < rounds; i++) {
        const b = cnt();
        window.scrollTo(0, document.body.scrollHeight);
        await wait(900);
        if (cnt() === b) { stable += 1; if (stable >= 2) break; } else stable = 0;
      }
      const NL = String.fromCharCode(10);
      const seen = new Map();
      document.querySelectorAll('a[href^="/session/"]').forEach((a) => {
        const m = (a.getAttribute("href") || "").match(/\\/session\\/([0-9a-f-]{36})/);
        if (!m) return;
        const title = (a.innerText || "").trim().split(NL)[0];
        if (!seen.has(m[1])) seen.set(m[1], { id: m[1], title: title, updatedAt: "" });
      });
      window.__list = JSON.stringify(Array.from(seen.values()));
    })()`,
    detailScript: `(async () => { const req = window.__req;
      const ids = window.__arg || [];
      const out = [];
      for (const it of ids) {
        try {
          const r = await req("/rest/thread/" + it.id + "?with_parent_info=true&version=2.18&source=default&limit=20&offset=0");
          const j = r.json || {};
          const entries = j.entries || [];
          const msgs = [];
          for (const e of entries) {
            const q = (e.query_str || "").trim();
            const when = e.updated_datetime || "";
            if (q) msgs.push({ role: "user", time: when, body: q });
            let steps = [];
            try {
              const p = JSON.parse(e.text);
              steps = Array.isArray(p) ? p : [p];
            } catch (err) {}
            for (const s of steps) {
              if (!s || s.step_type !== "FINAL" || !s.content) continue;
              let ans = s.content.answer || "";
              try {
                const inner = JSON.parse(ans);
                if (inner && typeof inner.answer === "string") ans = inner.answer;
              } catch (err) {}
              ans = String(ans).trim();
              if (ans) msgs.push({ role: "assistant", time: when, body: ans });
            }
          }
          const first = entries[0] || {};
          out.push({
            id: it.id,
            title: (first.query_str || it.title || "").slice(0, 60),
            updatedAt: first.updated_datetime || 0,
            messages: msgs
          });
        } catch (e) {
          out.push({ id: it.id, error: String(e) });
        }
        await new Promise((r) => setTimeout(r, 300));
      }
      window.__batch = JSON.stringify(out);
    })()`,
  },

  grok: {
    label: 'Grok',
    entry: 'https://grok.com/',
    // 全站 Cloudflare 硬挑战：同源 iframe 里的 fetch 会被拦成挑战页，只有顶层 XHR 能过。
    // __req 先试 iframe 再退 XHR，所以这里能自动落到能用的通道。
    // 列表分页用 nextPageToken；详情在 /responses，sender 为 human/assistant。
    listScript: `(async () => { const req = window.__req;
      const out = [];
      const seen = new Set();
      let token = "";
      for (let i = 0; i < 200; i++) {
        const url = "/rest/app-chat/conversations?pageSize=100" + (token ? "&pageToken=" + encodeURIComponent(token) : "");
        const r = await req(url);
        if (!r.status || r.status >= 400) { window.__err = "列表 " + r.status + " " + String(r.text || "").slice(0, 160); return; }
        const j = r.json || {};
        const arr = j.conversations || [];
        for (const c of arr) {
          if (seen.has(c.conversationId)) continue;
          seen.add(c.conversationId);
          out.push({ id: c.conversationId, title: c.title || "", updatedAt: c.modifyTime || c.createTime || "" });
        }
        token = j.nextPageToken || "";
        if (!token || !arr.length) break;
        await new Promise((r2) => setTimeout(r2, 300));
      }
      window.__list = JSON.stringify(out);
    })()`,
    detailScript: `(async () => { const req = window.__req;
      const ids = window.__arg || [];
      const out = [];
      for (const it of ids) {
        try {
          const r = await req("/rest/app-chat/conversations/" + it.id + "/responses?pageSize=200");
          const j = r.json || {};
          const msgs = (j.responses || []).map((m) => ({
            role: (m.sender === "human" || m.sender === "user") ? "user" : "assistant",
            time: m.createTime || "",
            body: String(m.message || "").trim()
          })).filter((m) => m.body);
          out.push({ id: it.id, title: it.title || "", updatedAt: it.updatedAt || 0, messages: msgs });
        } catch (e) {
          out.push({ id: it.id, error: String(e) });
        }
        await new Promise((r2) => setTimeout(r2, 300));
      }
      window.__batch = JSON.stringify(out);
    })()`,
  },

  claude: {
    label: 'Claude',
    entry: 'https://claude.ai/',
    listScript: `(async () => { const req = window.__req;
      const orgsResp = await req("/api/organizations");
      const orgs = orgsResp.json || [];
      const org = Array.isArray(orgs) && orgs[0] && (orgs[0].uuid || orgs[0].id);
      if (!org) { window.__err = "拿不到组织 id，可能未登录"; return; }
      window.__org = org;
      const out = [];
      let offset = 0;
      for (let i = 0; i < 500; i++) {
        const r = await req("/api/organizations/" + org + "/chat_conversations?limit=100&offset=" + offset + "&starred=false");
        if (!r.status || r.status >= 400) { window.__err = "列表接口 " + r.status + " " + (r.text || "").slice(0, 200); return; }
        const arr = r.json;
        if (!Array.isArray(arr) || !arr.length) break;
        for (const s of arr) out.push({ id: s.uuid, title: s.name || "", updatedAt: s.updated_at || "" });
        if (arr.length < 100) break;
        offset += arr.length;
        await new Promise((r) => setTimeout(r, 300));
      }
      window.__list = JSON.stringify(out);
    })()`,
    detailScript: `(async () => { const req = window.__req;
      const ids = window.__arg || [];
      const org = window.__org;
      const out = [];
      for (const it of ids) {
        try {
          const r = await req("/api/organizations/" + org + "/chat_conversations/" + it.id + "?tree=True&rendering_mode=messages&render_all_tools=true");
          const j = r.json || {};
          const msgs = (j.chat_messages || []).map((m) => ({
            role: m.sender === "human" ? "user" : "assistant",
            time: m.created_at || "",
            body: (m.text || "").trim()
          })).filter((m) => m.body);
          out.push({ id: it.id, title: j.name || it.title || "", updatedAt: it.updatedAt || 0, messages: msgs });
        } catch (e) {
          out.push({ id: it.id, error: String(e) });
        }
        await new Promise((r) => setTimeout(r, 250));
      }
      window.__batch = JSON.stringify(out);
    })()`,
  },
};

function cleanJson(raw) {
  const s = String(raw || '').trim();
  if (!s || s === 'undefined' || s === 'null') return null;
  const starts = [s.indexOf('['), s.indexOf('{')].filter((i) => i >= 0);
  if (!starts.length) return null;
  const a = Math.min(...starts);
  const lastArr = s.lastIndexOf(']');
  const lastObj = s.lastIndexOf('}');
  const b = Math.max(lastArr, lastObj);
  if (b < a) return null;
  try {
    return JSON.parse(s.slice(a, b + 1));
  } catch {
    return null;
  }
}

async function waitVar(sess, name, { tries = 180, delay = 1000 } = {}) {
  for (let i = 0; i < tries; i++) {
    const v = cleanJson(await sess.eval(`window.${name} || ""`));
    if (v) return v;
    await sleep(delay);
  }
  return null;
}

function isoTime(t) {
  if (!t) return '';
  const n = typeof t === 'number' ? (t > 1e12 ? t : t * 1000) : Date.parse(t);
  if (!Number.isFinite(n)) return '';
  const d = new Date(n);
  const p = (x) => String(x).padStart(2, '0');
  return `${d.getFullYear()}-${p(d.getMonth() + 1)}-${p(d.getDate())}`;
}

function slug(title) {
  return safeName(String(title || 'untitled')).slice(0, 40).replace(/^\.+/, '') || 'untitled';
}

async function openSite(sess, site) {
  await sess.open(site.entry, { window: site.foreground ? 'foreground' : 'background' });
  await sleep(3000);
  await sess.eval(PRELUDE);
  const here = await sess.eval('location.href');
  return String(here || '').trim();
}

async function fetchList(sess, site, maxWanted) {
  await sess.eval('window.__err = ""; window.__list = ""; window.__max = ' + Number(maxWanted || 0));
  await sess.eval(site.listScript);
  const err = cleanJson(await sess.eval('window.__err || ""'));
  if (err) throw new Error(t('列表接口报错：', 'list API error: ') + ` ${typeof err === 'string' ? err : JSON.stringify(err).slice(0, 300)}`);
  const list = await waitVar(sess, '__list');
  if (!list) throw new Error(t('列表超时未返回，可能是登录态失效或接口改版', 'List request timed out. Session may have expired, or the endpoint changed.'));
  return list;
}

async function fetchBatch(sess, site, items) {
  await sess.eval(`window.__batch = ""; window.__arg = ${JSON.stringify(items)}`);
  await sess.eval(site.detailScript);
  const batch = await waitVar(sess, '__batch', { tries: 120, delay: 1000 });
  if (!batch) return [];
  return batch;
}


// DOM 模式：接口逆向不动的站（Gemini 走 batchexecute RPC，Grok 全站 CF），改成逐条打开
// 会话页读渲染后的 DOM。慢，但选择器一旦对上就稳定，且不依赖私有接口。
async function domExport(sess, site, todo, outDir, opts) {
  const domToMd = await readFile(new URL('./lib/dom-to-md.js', import.meta.url), 'utf8');
  const records = [];
  const failed = [];

  for (let i = 0; i < todo.length; i++) {
    const it = todo[i];
    try {
      const target = site.detailUrl(it.id);
      if (site.reuseTab) {
        // 整页重载要几十秒（Gemini 冷启动尤其慢）。侧边栏已经有这条会话时点它走 SPA 路由，
        // 只换数据不重载；点不到再退回 location 跳转。
        const id = String(it.id);
        await sess.eval(
          '(function(){var id=' + JSON.stringify(id) + ';' +
          'var a=Array.prototype.slice.call(document.querySelectorAll(\'a[href*="/app/"]\'))' +
          '.filter(function(x){return (x.getAttribute("href")||"").indexOf(id)>=0})[0];' +
          'if(a){a.click();return "spa"}location.href=' + JSON.stringify(target) + ';return "nav"})()'
        );
        await sleep(opts.domDelay || 2500);
      } else {
        await sess.open(target, { window: site.foreground ? 'foreground' : 'background' });
        await sleep(opts.domDelay || 3000);
      }
      let data = cleanJson(await sess.eval(domToMd + String.fromCharCode(10) + site.extractScript));
      if (!data || !data.messages) {
        await sleep(2500);
        data = cleanJson(await sess.eval(domToMd + String.fromCharCode(10) + site.extractScript));
      }
      const messages = (data && data.messages || []).filter((m) => m && m.body && String(m.body).trim());
      if (!messages.length) {
        failed.push({ id: it.id, error: (data && data.error) || '无消息' });
        console.log(`[${i + 1}/${todo.length}] ${t('空', 'empty')} ${it.id}`);
        continue;
      }
      const day = isoTime(it.updatedAt) || isoTime(messages[0].time) || '0000-00-00';
      const dir = path.join(outDir, opts.site, day.slice(0, 7));
      await mkdir(dir, { recursive: true });
      const title = (data.title || it.title || '').trim() || '(无标题)';
      const file = path.join(dir, `${day}_${opts.site}_${String(it.id).slice(0, 12)}_${slug(title)}.md`);
      const md = buildDoc({
        title,
        url: site.detailUrl(it.id),
        channel: `bulk/${opts.site}/dom`,
        messages: messages.map((m) => ({ role: m.role, time: m.time || '', body: String(m.body).trim() })),
      });
      await writeFile(file, md, 'utf8');
      records.push({
        date: day,
        source: opts.site,
        id: it.id,
        title,
        messages: messages.length,
        chars: messages.reduce((n, m) => n + String(m.body).length, 0),
        file,
      });
      console.log(`[${i + 1}/${todo.length}] ${messages.length} ${t('条', 'msgs')} ${title.slice(0, 24)}`);
    } catch (e) {
      failed.push({ id: it.id, error: String(e.message || e) });
      console.log(`[${i + 1}/${todo.length}] ${t('失败', 'failed')} ${it.id}`);
    }
    await sleep(opts.delay || 500);
  }

  const indexFile = path.join(outDir, `bulk-${opts.site}.jsonl`);
  await writeFile(indexFile, records.map((r) => JSON.stringify(r)).join(String.fromCharCode(10)) + String.fromCharCode(10), 'utf8');
  if (failed.length) {
    await writeFile(path.join(outDir, `bulk-${opts.site}-failed.json`), JSON.stringify(failed, null, 1), 'utf8');
  }
  console.log(t(`\n完成：成功 ${records.length}，失败 ${failed.length}`, `\nDone: ${records.length} ok, ${failed.length} failed`));
  console.log(t(`索引 ${indexFile}`, `Index: ${indexFile}`));
}

async function cmdExport(opts) {
  const site = SITES[opts.site];
  if (!site) throw new Error(t(`未知站点：${opts.site}`, `Unknown site: ${opts.site}`));
  if (!available()) throw new Error(t('没有可用的浏览器后端：装 Chrome/Edge，或装 opencli 并确保扩展已连接', 'No usable browser backend. Install Chrome/Edge, or install opencli and connect the extension.'));

  const sess = await createSession({ name: SESSION });
  const outDir = path.resolve(opts.out);

  const where = await openSite(sess, site);
  if (/sign_in|login|signin/i.test(where)) {
    throw new Error(t(`还没登录 ${site.label}，当前停在 ${where}。先在浏览器里登录一次再跑。`, `Not signed in to ${site.label}; stopped at ${where}. Sign in once in the browser and rerun.`));
  }

  const cacheFile = path.join(outDir, `bulk-${opts.site}-list.json`);
  let list = null;
  if (opts.reuseList) {
    try {
      const cached = JSON.parse(await readFile(cacheFile, 'utf8'));
      if (Array.isArray(cached) && cached.length) {
        list = cached;
        console.log(t(`复用列表缓存 ${list.length} 个`, `Reusing cached list: ${list.length}`));
      }
    } catch {}
  }
  if (!list) {
    list = await fetchList(sess, site, opts.limit);
    if (!opts.limit && list.length > 3) {
      await writeFile(cacheFile, JSON.stringify(list, null, 1), 'utf8');
    }
  }
  console.log(t(`${site.label} 账号下共 ${list.length} 个会话`, `${list.length} sessions on the ${site.label} account`));

  let todo = list;
  if (opts.since) todo = todo.filter((x) => isoTime(x.updatedAt) >= opts.since);
  if (opts.limit) todo = todo.slice(0, opts.limit);
  todo.sort((a, b) => String(isoTime(b.updatedAt)).localeCompare(String(isoTime(a.updatedAt))));
  console.log(t(`本次导出 ${todo.length} 个${opts.since ? `（${opts.since} 之后）` : ''}`, `Exporting ${todo.length}${opts.since ? ` (after ${opts.since})` : ''}`));

  if (site.domMode) return domExport(sess, site, todo, outDir, opts);

  const records = [];
  const failed = [];
  const size = Math.max(1, opts.batch || 15);
  for (let i = 0; i < todo.length; i += size) {
    const chunk = todo.slice(i, i + size);
    const got = await fetchBatch(sess, site, chunk);
    for (const conv of got) {
      if (conv.error || !conv.messages || !conv.messages.length) {
        failed.push({ id: conv.id, error: conv.error || '无消息' });
        continue;
      }
      const day = isoTime(conv.updatedAt) || '0000-00-00';
      const dir = path.join(outDir, opts.site, day.slice(0, 7));
      await mkdir(dir, { recursive: true });
      const file = path.join(dir, `${day}_${opts.site}_${String(conv.id).slice(0, 12)}_${slug(conv.title)}.md`);
      const md = buildDoc({
        title: conv.title || '(无标题)',
        url: site.entry,
        channel: `bulk/${opts.site}`,
        messages: conv.messages.map((m) => ({ role: m.role, time: m.time, body: m.body })),
      });
      await writeFile(file, md, 'utf8');
      records.push({
        date: day,
        source: opts.site,
        id: conv.id,
        title: conv.title || '',
        messages: conv.messages.length,
        chars: conv.messages.reduce((n, m) => n + m.body.length, 0),
        file,
      });
    }
    const done = Math.min(i + size, todo.length);
    console.log(`[${done}/${todo.length}] ${t('本批', 'batch')} ${got.length}`);
    await sleep(opts.delay || 400);
  }

  const indexFile = path.join(outDir, `bulk-${opts.site}.jsonl`);
  await writeFile(indexFile, records.map((r) => JSON.stringify(r)).join('\n') + '\n', 'utf8');
  if (failed.length) {
    await writeFile(path.join(outDir, `bulk-${opts.site}-failed.json`), JSON.stringify(failed, null, 1), 'utf8');
  }
  console.log(t(`\n完成：成功 ${records.length}，失败 ${failed.length}`, `\nDone: ${records.length} ok, ${failed.length} failed`));
  console.log(t(`正文 ${records.reduce((n, r) => n + r.chars, 0).toLocaleString()} 字符`, `${records.reduce((n, r) => n + r.chars, 0).toLocaleString()} characters`));
  console.log(t(`索引 ${indexFile}`, `Index: ${indexFile}`));
}


// 登录后第一条该跑的命令：把页面自己发过的接口列出来，逐个打一次，打印状态和响应开头。
// 接口路径、字段名都能从这里读到，不用猜。
async function cmdProbe(opts) {
  const site = SITES[opts.site];
  if (!site) throw new Error(t(`未知站点：${opts.site}`, `Unknown site: ${opts.site}`));
  const sess = await createSession({ name: SESSION });
  await openSite(sess, site);
  const apis = cleanJson(await sess.eval('JSON.stringify(window.__apis())')) || [];
  const uniq = [...new Set(apis)].filter((u) => !/configs|models|tts|users\/status|refresh/.test(u));
  console.log(t(`${site.label} 页面发起过的业务接口 ${uniq.length} 个`, `${uniq.length} business endpoints seen on ${site.label}`));
  for (const u of uniq.slice(0, opts.limit || 8)) {
    await sess.eval(`window.__p = ""`);
    await sess.eval(`window.__req(${JSON.stringify(u)}, { timeout: 12000 }).then(function (r) { window.__p = JSON.stringify({ status: r.status, via: r.via, head: String(r.text || "").slice(0, 400) }); })`);
    const out = await waitVar(sess, '__p', { tries: 15, delay: 1000 });
    console.log(`\n${u}`);
    console.log(out ? `  ${out.status} via ${out.via}  ${String(out.head).replace(/\s+/g, ' ').slice(0, 300)}` : t('  无响应', '  no response'));
  }
}

async function cmdList(opts) {
  const site = SITES[opts.site];
  if (!site) throw new Error(t(`未知站点：${opts.site}`, `Unknown site: ${opts.site}`));
  const sess = await createSession({ name: SESSION });
  const where = await openSite(sess, site);
  if (/sign_in|login|signin/i.test(where)) {
    console.log(t(`未登录，当前停在 ${where}`, `Not signed in; stopped at ${where}`));
    return;
  }
  const cacheFile = path.resolve(opts.out, `bulk-${opts.site}-list.json`);
  let list = null;
  if (opts.reuseList) {
    try {
      const cached = JSON.parse(await readFile(cacheFile, 'utf8'));
      if (Array.isArray(cached) && cached.length) {
        list = cached;
        console.log(t(`复用列表缓存 ${list.length} 个`, `Reusing cached list: ${list.length}`));
      }
    } catch {}
  }
  if (!list) {
    list = await fetchList(sess, site, opts.limit);
    if (!opts.limit && list.length > 3) {
      try {
        await mkdir(path.resolve(opts.out), { recursive: true });
        await writeFile(cacheFile, JSON.stringify(list, null, 1), 'utf8');
      } catch {}
    }
  }
  console.log(t(`${site.label} 共 ${list.length} 个会话，缓存 ${cacheFile}`, `${list.length} sessions on ${site.label}; cache at ${cacheFile}`));
  for (const x of list.slice(0, opts.limit || 20)) {
    console.log(`${isoTime(x.updatedAt) || '----'}  ${String(x.id).slice(0, 14)}  ${x.title || t('(无标题)', '(untitled)')}`);
  }
}

async function main() {
  const [cmd, ...rest] = process.argv.slice(2);
  const opts = { site: 'deepseek', out: './bulk-out', limit: 0, since: '', batch: 15, delay: 400, reuseList: false };
  for (let i = 0; i < rest.length; i++) {
    const a = rest[i];
    if (a === '--site') opts.site = rest[++i];
    else if (a === '--out') opts.out = rest[++i];
    else if (a === '--limit') opts.limit = Number(rest[++i]);
    else if (a === '--since') opts.since = rest[++i];
    else if (a === '--batch') opts.batch = Number(rest[++i]);
    else if (a === '--delay') opts.delay = Number(rest[++i]);
    else if (a === '--reuse-list') opts.reuseList = true;
  }

  if (cmd === 'sites') {
    for (const [k, v] of Object.entries(SITES)) console.log(`${k.padEnd(10)} ${v.label}  ${v.entry}`);
    return;
  }
  if (cmd === 'probe') return cmdProbe(opts);
  if (cmd === 'list') return cmdList(opts);
  if (cmd === 'export') return cmdExport(opts);
  console.log(t('用法：', 'Usage: ') + `
  node scripts/bulk.mjs sites
  node scripts/bulk.mjs probe  --site deepseek      # ${t('登录后先校准接口', 'calibrate endpoints after signing in')}
  node scripts/bulk.mjs list   --site deepseek [--limit 20]
  node scripts/bulk.mjs export --site deepseek --out DIR [--since 2026-09-01] [--limit N] [--batch 15]`);
}

main().catch((e) => {
  console.error(String(e.message || e));
  process.exitCode = 1;
});
