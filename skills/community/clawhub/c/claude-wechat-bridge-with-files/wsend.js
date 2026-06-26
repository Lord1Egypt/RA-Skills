#!/usr/bin/env node
// wsend.js — 独立的微信「主动发送」器，绕开 MCP 的"必须先入站"限制。
// 复用 ~/.wechat-claude 里的账号凭证 + (可选)持久化的 contextToken，
// 直接 POST 到 ilink/bot/sendmessage。
//
// 用法:
//   node wsend.js "要发的文字"                  # 发给凭证里的默认 userId
//   node wsend.js --to <userId> "文字"
//   node wsend.js --no-context "文字"           # 强制不带 contextToken(测试 bot 能否主动发起)
//   echo "长文字" | node wsend.js -             # 从 stdin 读
//
// 退出码: 0 成功 / 1 用法或凭证错 / 2 发送失败
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import crypto from "node:crypto";

const HOME = os.homedir();
const ACCT_DIR = path.join(HOME, ".wechat-claude", "accounts");
const CTX_FILE = path.join(HOME, ".wechat-claude", "last-context.json");

function die(msg, code = 1) { console.error(msg); process.exit(code); }

// ── 读账号凭证 ──────────────────────────────────────────────
function loadAccount() {
  if (!fs.existsSync(ACCT_DIR)) die(`凭证目录不存在: ${ACCT_DIR}`);
  const files = fs.readdirSync(ACCT_DIR).filter(f => f.endsWith(".json"));
  for (const f of files) {
    try {
      const a = JSON.parse(fs.readFileSync(path.join(ACCT_DIR, f), "utf-8"));
      if (a.token && a.baseUrl) return a; // {token, baseUrl, userId, accountId}
    } catch {}
  }
  die("没找到可用的账号凭证(需含 token + baseUrl)");
}

// ── 读持久化的 contextToken(若有) ──────────────────────────
function loadContext(userId) {
  try {
    const c = JSON.parse(fs.readFileSync(CTX_FILE, "utf-8"));
    if (!userId || c.userId === userId) return c.contextToken || "";
    // 文件里存了多个用户时按 userId 取
    if (c.byUser && c.byUser[userId]) return c.byUser[userId];
  } catch {}
  return "";
}

function randomWechatUin() {
  const u = crypto.randomBytes(4).readUInt32BE(0);
  return Buffer.from(String(u), "utf-8").toString("base64");
}
function clientId() {
  return "wechat-claude-" + crypto.randomBytes(8).toString("hex");
}

async function sendOne({ baseUrl, token, to, text, contextToken }) {
  const body = JSON.stringify({
    msg: {
      from_user_id: "",
      to_user_id: to,
      client_id: clientId(),
      message_type: 2,          // BOT
      message_state: 2,         // FINISH
      item_list: [{ type: 1, text_item: { text } }], // TEXT
      ...(contextToken ? { context_token: contextToken } : {}),
    },
    base_info: { channel_version: "wsend-1.0" },
  });
  const url = (baseUrl.endsWith("/") ? baseUrl : baseUrl + "/") + "ilink/bot/sendmessage";
  const res = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      AuthorizationType: "ilink_bot_token",
      Authorization: `Bearer ${token.trim()}`,
      "X-WECHAT-UIN": randomWechatUin(),
    },
    body,
  });
  const raw = await res.text();
  return { ok: res.ok, status: res.status, raw };
}

function splitMessage(text, max = 4000) {
  if (text.length <= max) return [text];
  const out = []; let rem = text;
  while (rem.length) {
    if (rem.length <= max) { out.push(rem); break; }
    let at = rem.lastIndexOf("\n", max);
    if (at <= 0 || at < max * 0.5) at = max;
    out.push(rem.slice(0, at)); rem = rem.slice(at).trimStart();
  }
  return out;
}

// ── main ────────────────────────────────────────────────────
(async () => {
  const argv = process.argv.slice(2);
  let to = "", noContext = false, parts = [];
  for (let i = 0; i < argv.length; i++) {
    if (argv[i] === "--to") { to = argv[++i]; }
    else if (argv[i] === "--no-context") { noContext = true; }
    else parts.push(argv[i]);
  }
  let text = parts.join(" ");
  if (text === "-" || text === "") {
    text = fs.readFileSync(0, "utf-8"); // stdin
  }
  if (!text.trim()) die("没有要发送的文字");

  const acct = loadAccount();
  to = to || acct.userId;
  if (!to) die("没有目标 userId(凭证无 userId，请用 --to 指定)");

  const contextToken = noContext ? "" : loadContext(to);

  const chunks = splitMessage(text);
  let lastResp = null;
  for (const ch of chunks) {
    lastResp = await sendOne({ baseUrl: acct.baseUrl, token: acct.token, to, text: ch, contextToken });
    console.error(`[wsend] status=${lastResp.status} ctx=${contextToken ? "yes" : "no"} → ${lastResp.raw.slice(0, 200)}`);
    if (!lastResp.ok) process.exit(2);
  }
  // 成功:输出 ret 判断
  try {
    const j = JSON.parse(lastResp.raw);
    if (j.ret !== undefined && j.ret !== 0) {
      console.error(`[wsend] API ret=${j.ret} (非0，可能未真正送达): ${lastResp.raw}`);
      process.exit(2);
    }
  } catch {}
  console.error(`[wsend] ✅ 发送完成 → ${to} (${chunks.length} 段)`);
})();
