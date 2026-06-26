import { existsSync, readFileSync, writeFileSync } from "fs";
import { resolve } from "path";
import { homedir } from "os";
import { createHash } from "crypto";
const SOUL_API = process.env.SOUL_API || "http://localhost:18800";
let _lastProcessed = "";
let _lastProcessedTs = 0;
let _lastMsg = "";
let _lastSenderId = "";
const _sentFeedbackHashes = /* @__PURE__ */ new Set();
const FEEDBACK_DEDUP_MAX = 200;
function _feedbackHash(userMsg, aiReply) {
  return createHash("md5").update(userMsg.slice(0, 100) + "||" + aiReply.slice(0, 200)).digest("hex");
}
function _markFeedbackSent(userMsg, aiReply) {
  const h = _feedbackHash(userMsg, aiReply);
  if (_sentFeedbackHashes.has(h)) return false;
  if (_sentFeedbackHashes.size >= FEEDBACK_DEDUP_MAX) {
    const keep = [..._sentFeedbackHashes].slice(-100);
    _sentFeedbackHashes.clear();
    keep.forEach((k) => _sentFeedbackHashes.add(k));
  }
  _sentFeedbackHashes.add(h);
  return true;
}
let _api;
function getPluginApi() {
  return _api;
}
function updatePluginStats(_s) {
}
function setSoulDynamicLock(_ms) {
}
let _contextEngineRegistered = false;
var plugin_entry_default = {
  id: "cc-soul",
  name: "cc-soul",
  description: "Soul engine for AI \u2014 memory, personality, cognition, emotion",
  kind: "context-engine",
  configSchema: {},
  register(api) {
    _api = api;
    const log = api.logger || console;
    const t0 = Date.now();
    import("./context-engine.ts").then(async (mod) => {
      try {
        const { initSoulEngine } = await import("./soul-api.ts");
        await initSoulEngine();
      } catch (e) {
        console.error(`[cc-soul] soul engine init failed: ${e.message}`);
      }
      if (typeof api.registerContextEngine === "function") {
        try {
          const engine = {
            async assemble(params) {
              try {
                const { buildSoulPrompt } = require("./prompt-builder.ts");
                const { stats } = require("./handler-state.ts");
                const { recall, ensureMemoriesLoaded } = require("./memory.ts");
                ensureMemoriesLoaded();
                const soulPrompt = buildSoulPrompt(stats.totalMessages, stats.corrections, stats.firstSeen, []);
                let memoryAugment = "";
                const msgs = params?.messages || [];
                const lastMsg = msgs.length > 0 ? msgs[msgs.length - 1] : null;
                const userMsg = typeof lastMsg?.content === "string" ? lastMsg.content : Array.isArray(lastMsg?.content) ? lastMsg.content.find((p) => p.type === "text")?.text || "" : "";
                const cleanMsg = userMsg.includes(":") ? userMsg.split(/\n/).pop()?.replace(/^\S+:\s*/, "") || userMsg : userMsg;
                if (cleanMsg && cleanMsg.length > 1) {
                  const recalled = recall(cleanMsg, 5);
                  if (recalled.length > 0) {
                    memoryAugment = "\n\n[\u76F8\u5173\u8BB0\u5FC6] " + recalled.map((m) => m.content?.slice(0, 80)).join("\uFF1B");
                  }
                }
                return { systemPrompt: soulPrompt + memoryAugment };
              } catch (e) {
                console.error(`[cc-soul][context-engine] assemble error: ${e.message}`);
                return { systemPrompt: "" };
              }
            }
          };
          api.registerContextEngine("cc-soul", () => engine);
          console.log(`[cc-soul] \u2705 Context Engine registered\uFF08\u6570\u636E\u6765\u81EA soul.db\uFF09`);
        } catch (e) {
          console.log(`[cc-soul] \u26A0 Context Engine registration failed: ${e.message}`);
        }
      } else {
        console.log(`[cc-soul] \u72EC\u7ACB API \u6A21\u5F0F\uFF08\u65E0 Context Engine\uFF09`);
      }
      try {
        const { startSoulApi } = await import("./soul-api.ts");
        startSoulApi();
        console.log(`[cc-soul] Soul API started (${SOUL_API}) for external access`);
      } catch (e) {
        console.log(`[cc-soul] Soul API start failed: ${e.message} (external access unavailable)`);
      }
    }).catch((e) => {
      console.error(`[cc-soul] context-engine load failed: ${e.message}, falling back to pure API mode`);
      _startSoulApiFallback();
    });
    try {
      api.registerHook(["message:preprocessed"], async (event) => {
        const ctx = event.context || {};
        const rawMsg = (ctx.body || "").replace(/^\[Feishu[^\]]*\]\s*/i, "").replace(/^\[message_id:\s*\S+\]\s*/i, "").replace(/^[a-zA-Z0-9_\u4e00-\u9fff]{1,20}:\s*/, "").replace(/^\n+/, "").trim();
        const senderId = ctx.senderId || "";
        if (!rawMsg) return;
        const msgKey = rawMsg.slice(0, 50) + ":" + senderId;
        const now2 = Date.now();
        if (_lastProcessed === msgKey && now2 - _lastProcessedTs < 3e3) return;
        _lastProcessed = msgKey;
        _lastProcessedTs = now2;
        try {
          const { setLastSenderId } = await import("./context-engine.ts");
          setLastSenderId(senderId);
        } catch {
        }
        try {
          const resp = await fetch(`${SOUL_API}/process`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: rawMsg, user_id: senderId })
          });
          const data = await resp.json();
          if (data.command && data.command_reply) {
            try {
              const { setLastAugments } = await import("./context-engine.ts");
              setLastAugments([`[cc-soul \u547D\u4EE4\u7ED3\u679C\uFF0C\u8BF7\u76F4\u63A5\u8F6C\u8FF0\u7ED9\u7528\u6237\uFF0C\u4E0D\u8981\u4FEE\u6539\u5185\u5BB9]
${data.command_reply}`]);
              console.log(`[cc-soul] command \u2192 augment injected (${data.command_reply.length} chars)`);
            } catch {
            }
          }
          _lastMsg = rawMsg;
          _lastSenderId = senderId;
        } catch (e) {
          console.log(`[cc-soul] process: ${e.message}`);
        }
      }, { name: "cc-soul:preprocessed" });
      api.registerHook(["message:sent"], async (event) => {
        if (_contextEngineRegistered) return;
        const content = event.context?.content || event.content || event.text || "";
        const lastMsg = _lastMsg;
        const lastSenderId = _lastSenderId;
        if (!lastMsg || !content || content.length < 5) return;
        if (!_markFeedbackSent(lastMsg, content)) return;
        try {
          await fetch(`${SOUL_API}/feedback`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ user_message: lastMsg, ai_reply: content, user_id: lastSenderId })
          });
          console.log(`[cc-soul] feedback sent (hook fallback)`);
        } catch {
        }
      }, { name: "cc-soul:sent" });
      if (typeof api.on === "function") {
        api.on("inbound_claim", async (event, _ctx) => {
          const content = (event?.content || event?.body || "").trim();
          if (!content) return;
          try {
            const senderId = event?.senderId || event?.context?.senderId || "";
            const cmdResp = await fetch(`${SOUL_API}/command`, {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({ message: content, user_id: senderId })
            });
            const cmdData = await cmdResp.json();
            if (cmdData.handled && cmdData.reply && cmdData.reply !== "(done)") {
              return { handled: true, reply: cmdData.reply };
            }
            if (cmdData.handled) return { handled: true };
          } catch {
          }
        });
      }
    } catch (e) {
      console.error(`[cc-soul] hook registration failed: ${e.message}`);
    }
    const bootLockPath = resolve(homedir(), ".openclaw/plugins/cc-soul/data/.boot-lock");
    const now = Date.now();
    let shouldNotify = true;
    try {
      if (existsSync(bootLockPath)) {
        const lockTs = parseInt(readFileSync(bootLockPath, "utf-8").trim(), 10);
        if (now - lockTs < 5 * 60 * 1e3) shouldNotify = false;
      }
    } catch {
    }
    if (shouldNotify) {
      try {
        writeFileSync(bootLockPath, String(now), "utf-8");
      } catch {
      }
      setTimeout(async () => {
        const mode = _contextEngineRegistered ? "Context Engine" : "Hook + SOUL.md";
        console.log(`[cc-soul] boot complete \u2014 mode: ${mode}, API: ${SOUL_API}`);
      }, 3e3);
    }
    log.info(`[cc-soul] register() done in ${Date.now() - t0}ms`);
  }
};
function _startSoulApiFallback() {
  fetch(`${SOUL_API}/health`).then((r) => r.json()).then((d) => {
    if (d.status === "ok") console.log(`[cc-soul] Soul API already running (fallback)`);
  }).catch(() => {
    console.log(`[cc-soul] Soul API not running, auto-starting (fallback)...`);
    import("./soul-api.ts").then(async ({ initSoulEngine, startSoulApi }) => {
      await initSoulEngine();
      startSoulApi();
    }).catch((e) => {
      console.error(`[cc-soul] Failed to auto-start Soul API: ${e.message}`);
    });
  });
}
export {
  plugin_entry_default as default,
  getPluginApi,
  setSoulDynamicLock,
  updatePluginStats
};
