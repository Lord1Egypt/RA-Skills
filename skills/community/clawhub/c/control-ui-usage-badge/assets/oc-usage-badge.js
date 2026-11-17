/* oc-usage-badge.js
 * Control UI per-message token usage badge.
 *
 * Appends a compact metric line under every assistant message that already
 * renders text. Client-side only: it scans the JSON frames the Control UI
 * already receives over its WebSocket (chat.history / chat.startup / run
 * events), so the gateway transcript is never modified.
 *
 * Tune the displayed fields via CONFIG below, then re-run scripts/apply.sh.
 */
(function () {
  "use strict";

  // ---- what to display -----------------------------------------------------
  var CONFIG = {
    input: true,        // ↑ input tokens (non-cached prompt)
    output: true,       // ↓ output tokens
    total: true,        // Σ provider totalTokens
    cacheRead: true,    // cache N read
    cachePct: true,     // (P%) cache-read share of the prompt
    cacheWrite: true,   // cache N write (only shown when > 0)
    cost: true,         // $x (provider-reported, or estimated from PRICES below)
    duration: true,     // ⏱ approximate turn wall-clock
    throughput: true,   // ⚡Nt/s output tokens per second
    model: true,        // model id
    provider: false,    // provider id
    toolCalls: false,   // 🛠N tool calls in this message
    warn: true,         // ⚠️ on truncated (stopReason=length) replies
  };

  // Optional local price table for cost ESTIMATION when the provider does not
  // report cost. Prices are USD per 1,000,000 tokens.
  var PRICES = {
    "deepseek-v4.1-flash": { in: 0.14, out: 0.28, cacheRead: 0.014 },
    // add more: "model-id": { in: 0, out: 0, cacheRead: 0, cacheWrite: 0 },
  };
  // --------------------------------------------------------------------------

  function fmt(n) {
    if (typeof n !== "number" || !isFinite(n)) return "0";
    if (n >= 1e6) return (n / 1e6).toFixed(2) + "M";
    if (n >= 1e3) return (n / 1e3).toFixed(1) + "k";
    return String(n);
  }

  function fmtDur(ms) {
    if (!(ms > 0)) return "";
    if (ms < 1000) return Math.round(ms) + "ms";
    if (ms < 60000) return (ms / 1000).toFixed(1) + "s";
    var m = Math.floor(ms / 60000);
    var s = Math.round((ms % 60000) / 1000);
    return m + "m" + (s ? s + "s" : "");
  }

  function countToolCalls(m) {
    var c = m && m.content;
    if (!Array.isArray(c)) return 0;
    var n = 0;
    for (var i = 0; i < c.length; i++) {
      var p = c[i];
      if (p && (p.type === "toolCall" || p.type === "tool_use")) n++;
    }
    return n;
  }

  function estimateCost(model, u) {
    var p = model && PRICES ? PRICES[model] : null;
    if (!p) return null;
    var c = 0;
    c += ((u.input || 0) / 1e6) * (p.in || 0);
    c += ((u.output || 0) / 1e6) * (p.out || 0);
    c += ((u.cacheRead || 0) / 1e6) * (p.cacheRead || 0);
    c += ((u.cacheWrite || 0) / 1e6) * (p.cacheWrite || 0);
    return c > 0 ? c : null;
  }

  function usageLine(m, ctx) {
    var u = m.usage || {};
    var out = [];
    if (CONFIG.warn && m.stopReason === "length") out.push("\u26a0\ufe0f truncated");
    if (CONFIG.input && typeof u.input === "number") out.push("\u2191" + fmt(u.input));
    if (CONFIG.output && typeof u.output === "number") out.push("\u2193" + fmt(u.output));
    if (CONFIG.total && typeof u.totalTokens === "number") out.push("\u03a3" + fmt(u.totalTokens));

    var cr = typeof u.cacheRead === "number" ? u.cacheRead : 0;
    var cw = typeof u.cacheWrite === "number" ? u.cacheWrite : 0;
    if (cr > 0 || cw > 0) {
      var txt = "";
      if (CONFIG.cacheRead && cr > 0) {
        txt = fmt(cr) + " read";
        var denom = (typeof u.input === "number" ? u.input : 0) + cr;
        if (CONFIG.cachePct && denom > 0) {
          txt += " (" + (Math.round((cr / denom) * 1000) / 10) + "%)";
        }
      }
      if (CONFIG.cacheWrite && cw > 0) txt += (txt ? " / " : "") + fmt(cw) + " write";
      if (txt) out.push("cache " + txt);
    }

    if (CONFIG.duration && ctx && ctx.deltaMs > 0) out.push("\u23f1" + fmtDur(ctx.deltaMs));
    if (CONFIG.throughput && ctx && ctx.deltaMs >= 500 && typeof u.output === "number" && u.output > 0) {
      var tps = u.output / (ctx.deltaMs / 1000);
      out.push("\u26a1" + (tps >= 100 ? Math.round(tps) : tps.toFixed(1)) + "t/s");
    }
    if (CONFIG.provider && m.provider) out.push(String(m.provider));
    if (CONFIG.model && m.model) out.push(String(m.model));
    if (CONFIG.toolCalls) {
      var tc = countToolCalls(m);
      if (tc > 0) out.push("\ud83d\udee0" + tc);
    }
    if (CONFIG.cost) {
      var reported = u.cost && typeof u.cost.total === "number" ? u.cost.total : 0;
      if (reported > 0) {
        out.push("$" + reported.toFixed(4));
      } else {
        var est = estimateCost(m.model, u);
        if (est !== null) out.push("~$" + est.toFixed(4));
      }
    }
    return out.join(" \u00b7 ");
  }

  function isZeroUsage(u) {
    if (!u) return true;
    return ![
      u.input,
      u.output,
      u.totalTokens,
      u.cacheRead,
      u.cacheWrite,
    ].some(function (v) {
      return typeof v === "number" && v > 0;
    });
  }

  // Append the usage line to an assistant message that already renders text.
  function annotateMessage(m, ctx) {
    if (!m || m.role !== "assistant" || !m.usage) return false;
    if (isZeroUsage(m.usage)) return false;
    if (m.__ocUsageDone) return false;
    var c = m.content;
    if (!Array.isArray(c)) return false;
    var hasText = false;
    for (var j = 0; j < c.length; j++) {
      var part = c[j];
      if (part && part.type === "text" && typeof part.text === "string" && part.text.trim()) {
        hasText = true;
        break;
      }
    }
    if (!hasText) return false;
    var line = usageLine(m, ctx);
    if (!line) return false;
    c.push({ type: "text", text: "\n\n*" + line + "*" });
    try {
      Object.defineProperty(m, "__ocUsageDone", { value: true, enumerable: false });
    } catch (e) {
      m.__ocUsageDone = true;
    }
    return true;
  }

  // Annotate an array of messages. Duration = time from the last user message
  // to this assistant message (approximate turn wall-clock, tool time included).
  var MAX_DELTA_MS = 6 * 60 * 60 * 1000;
  function annotateArray(arr) {
    var changed = false;
    var lastUserTs = null;
    for (var i = 0; i < arr.length; i++) {
      var el = arr[i];
      if (el && typeof el === "object") {
        var role = el.role;
        var ts = typeof el.timestamp === "number" ? el.timestamp : null;
        var ctx = undefined;
        if (role === "assistant" && ts !== null && lastUserTs !== null) {
          var d = ts - lastUserTs;
          if (d > 0 && d < MAX_DELTA_MS) ctx = { deltaMs: d };
        }
        if (annotateMessage(el, ctx)) changed = true;
        if (walk(el, 1)) changed = true;
        if (role === "user" && ts !== null) lastUserTs = ts;
      }
    }
    return changed;
  }

  // Walk any JSON value looking for assistant messages with usage.
  function walk(node, depth) {
    if (depth > 10 || !node || typeof node !== "object") return false;
    if (Array.isArray(node)) return annotateArray(node);
    var changed = false;
    for (var k in node) {
      if (!Object.prototype.hasOwnProperty.call(node, k)) continue;
      var v = node[k];
      if (v && typeof v === "object") {
        if (!Array.isArray(v) && annotateMessage(v)) changed = true;
        if (walk(v, depth + 1)) changed = true;
      }
    }
    return changed;
  }

  function processFrame(data) {
    if (typeof data !== "string" || data.length < 2) return null;
    var o;
    try {
      o = JSON.parse(data);
    } catch (e) {
      return null;
    }
    if (!o || typeof o !== "object") return null;
    if (!walk(o, 0)) return null;
    try {
      console.info("[oc-usage-badge] annotated a frame");
    } catch (e) {}
    return JSON.stringify(o);
  }

  if (typeof module !== "undefined" && module.exports) {
    module.exports = {
      CONFIG: CONFIG,
      PRICES: PRICES,
      estimateCost: estimateCost,
      fmt: fmt,
      fmtDur: fmtDur,
      usageLine: usageLine,
      annotateMessage: annotateMessage,
      annotateArray: annotateArray,
      walk: walk,
      processFrame: processFrame,
    };
  }
  if (typeof window === "undefined") return;

  var Native = window.WebSocket;
  if (!Native || window.__ocUsageBadgeInstalled) return;
  window.__ocUsageBadgeInstalled = true;

  function install(ws) {
    var origAdd = ws.addEventListener.bind(ws);
    ws.addEventListener = function (type, listener, opts) {
      if (type !== "message" || typeof listener !== "function") {
        return origAdd(type, listener, opts);
      }
      var wrapped = function (ev) {
        try {
          var data = ev && ev.data;
          var out = processFrame(data);
          if (out !== null) {
            return listener.call(this, { data: out, type: "message" });
          }
        } catch (e) {}
        return listener.call(this, ev);
      };
      return origAdd(type, wrapped, opts);
    };
  }

  function Patched(url, protocols) {
    var ws = arguments.length > 1 ? new Native(url, protocols) : new Native(url);
    install(ws);
    return ws;
  }
  Patched.prototype = Native.prototype;
  try {
    Object.setPrototypeOf(Patched, Native);
  } catch (e) {}
  ["CONNECTING", "OPEN", "CLOSING", "CLOSED"].forEach(function (k) {
    try {
      Object.defineProperty(Patched, k, { value: Native[k] });
    } catch (e) {}
  });
  window.WebSocket = Patched;
  window.__ocUsageBadgeVersion = "1.2";
  window.__ocUsageBadgeConfig = CONFIG;
  try {
    console.info("[oc-usage-badge] installed v1.2");
  } catch (e) {}
})();
