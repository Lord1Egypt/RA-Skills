import { createServer } from "http";
import "./persistence.ts";
const SOUL_API_PORT = parseInt(process.env.SOUL_PORT || "18800", 10);
function configureLLM(config) {
  import("./cli.ts").then(({ setFallbackApiConfig }) => {
    setFallbackApiConfig({
      backend: "openai-compatible",
      cli_command: "",
      cli_args: [],
      api_base: config.api_base,
      api_key: config.api_key,
      api_model: config.model,
      max_concurrent: 8
    });
  }).catch((e) => {
    console.error(`[cc-soul] module load failed (cli): ${e.message}`);
  });
  console.log(`[cc-soul] LLM configured: ${config.model} @ ${config.api_base}`);
}
let heartbeatTimer = null;
let _initDelayTimer = null;
async function initSoulEngine() {
  try {
    (await import("./persistence.ts")).ensureDataDir();
  } catch {
  }
  try {
    (await import("./memory.ts")).ensureSQLiteReady();
  } catch {
  }
  try {
    (await import("./features.ts")).loadFeatures();
  } catch {
  }
  try {
    (await import("./user-profiles.ts")).loadProfiles();
  } catch {
  }
  let llmConfigured = false;
  try {
    (await import("./cli.ts")).loadAIConfig();
    const { hasLLM } = await import("./cli.ts");
    if (hasLLM()) {
      llmConfigured = true;
    }
  } catch {
  }
  if (!llmConfigured) {
    try {
      const { resolve } = await import("path");
      const { DATA_DIR } = await import("./persistence.ts");
      const { readFileSync, existsSync } = await import("fs");
      const soulJsonPath = resolve(DATA_DIR, "..", "soul.json");
      if (existsSync(soulJsonPath)) {
        const soulJson = JSON.parse(readFileSync(soulJsonPath, "utf-8"));
        if (soulJson.llm?.base_url && soulJson.llm?.api_key) {
          configureLLM({ api_base: soulJson.llm.base_url, api_key: soulJson.llm.api_key, model: soulJson.llm.model || "gpt-4o-mini" });
          llmConfigured = true;
          console.log(`[cc-soul] LLM configured from soul.json: ${soulJson.llm.model || "gpt-4o-mini"}`);
        }
      }
    } catch {
    }
  }
  if (llmConfigured) {
    import("./cli.ts").then(async ({ validateLLM }) => {
      const result = await validateLLM();
      if (result.ok) console.log(`[cc-soul] \u2705 LLM \u8FDE\u63A5\u6B63\u5E38`);
      else console.log(`[cc-soul] \u26A0\uFE0F LLM \u8FDE\u63A5\u5931\u8D25: ${result.error}\uFF08\u6838\u5FC3\u529F\u80FD\u4E0D\u53D7\u5F71\u54CD\uFF09`);
    }).catch(() => {
    });
  } else {
    console.log(`[cc-soul] \u672A\u914D\u7F6E LLM\uFF0C\u7EAF NAM \u6A21\u5F0F\u8FD0\u884C`);
  }
  if (!heartbeatTimer) {
    heartbeatTimer = setInterval(async () => {
      try {
        (await import("./handler-heartbeat.ts")).runHeartbeat();
      } catch {
      }
    }, 30 * 60 * 1e3);
    _initDelayTimer = setTimeout(async () => {
      try {
        (await import("./handler-heartbeat.ts")).runHeartbeat();
      } catch {
      }
    }, 5 * 60 * 1e3);
    console.log(`[cc-soul] heartbeat scheduled`);
  }
}
function stopSoulEngine() {
  if (heartbeatTimer) {
    clearInterval(heartbeatTimer);
    heartbeatTimer = null;
  }
  if (_initDelayTimer) {
    clearTimeout(_initDelayTimer);
    _initDelayTimer = null;
  }
}
function readBody(req) {
  return new Promise((resolve) => {
    const chunks = [];
    req.on("data", (chunk) => chunks.push(chunk));
    req.on("end", () => resolve(Buffer.concat(chunks).toString()));
  });
}
let serverStarted = false;
function startSoulApi() {
  if (serverStarted) return;
  serverStarted = true;
  const server = createServer(async (req, res) => {
    res.setHeader("Access-Control-Allow-Origin", "*");
    res.setHeader("Access-Control-Allow-Methods", "POST, GET, OPTIONS");
    res.setHeader("Access-Control-Allow-Headers", "Content-Type, Authorization");
    if (req.method === "OPTIONS") {
      res.writeHead(204);
      res.end();
      return;
    }
    const url = req.url || "";
    res.setHeader("Content-Type", "application/json");
    try {
      const body = req.method === "POST" ? JSON.parse(await readBody(req)) : {};
      if (url === "/memories" && req.method === "POST") {
        try {
          const { addMemory } = await import("./memory.ts");
          const { extractFacts, addFacts } = await import("./fact-store.ts");
          const content = body.content || body.message || body.text || "";
          const userId = body.user_id || body.userId || "default";
          const scope = body.scope || "fact";
          if (!content) {
            res.writeHead(400);
            res.end(JSON.stringify({ error: "content required" }));
            return;
          }
          addMemory(content, scope, userId, "private");
          const facts = extractFacts(content, "user_said", userId);
          if (facts.length > 0) addFacts(facts);
          res.writeHead(200);
          res.end(JSON.stringify({ stored: true, facts_extracted: facts.length }));
        } catch (e) {
          res.writeHead(500);
          res.end(JSON.stringify({ error: e.message }));
        }
        return;
      }
      if (url === "/search" && req.method === "POST") {
        try {
          const { recall, ensureMemoriesLoaded } = await import("./memory.ts");
          ensureMemoriesLoaded();
          let query = body.query || body.message || "";
          const userId = body.user_id || body.userId || "default";
          const topN = body.top_n || body.limit || 5;
          const { hasLLM, spawnCLI } = await import("./cli.ts");
          const llmAvailable = hasLLM();
          if (llmAvailable) {
            const _abstractWords = /方式|习惯|品味|爱好|特点|性格|规划|想法|压力|活动|偏好|style|habit|taste|hobby|trait|plan|routine|preference/i;
            if (_abstractWords.test(query)) {
              try {
                const keywords = await Promise.race([
                  new Promise((resolve) => {
                    spawnCLI(
                      `\u7528\u6237\u95EE"${query.slice(0, 100)}"\uFF0C\u8BF7\u5217\u51FA5\u4E2A\u6700\u53EF\u80FD\u76F8\u5173\u7684\u5177\u4F53\u5173\u952E\u8BCD\uFF0C\u6BCF\u884C\u4E00\u4E2A\uFF0C\u53EA\u8F93\u51FA\u5173\u952E\u8BCD\u4E0D\u8981\u89E3\u91CA`,
                      (output) => resolve(output || ""),
                      8e3,
                      "query-rewrite"
                    );
                  }),
                  new Promise((resolve) => setTimeout(() => resolve(""), 1e4))
                ]);
                if (keywords) {
                  const kws = keywords.split("\n").map((l) => l.trim().replace(/^[\d.、\-*]+/, "").trim()).filter((l) => l.length >= 2 && l.length <= 20);
                  if (kws.length > 0) {
                    query = query + " " + kws.join(" ");
                    console.log(`[cc-soul][search] query rewrite: +${kws.length} keywords \u2192 "${query.slice(0, 80)}"`);
                  }
                }
              } catch {
              }
            }
          }
          const recallN = llmAvailable ? Math.max(topN * 4, 20) : topN;
          let results = recall(query, recallN, userId);
          if (llmAvailable && results.length > topN) {
            try {
              const candidates = results.map((m, i) => `[${i}] <<<${(m.content || "").replace(/\n/g, " ").slice(0, 200)}>>>`).join("\n");
              const rerankPrompt = `Given the question: "${query.slice(0, 200)}"

Here are ${results.length} memory candidates:
${candidates}

Select the ${topN} most relevant memories for answering the question. Reply with ONLY the numbers separated by commas (e.g. "3,7,1"). Nothing else.`;
              const reranked = await Promise.race([
                new Promise((resolve) => {
                  spawnCLI(rerankPrompt, (output) => {
                    try {
                      const indices = (output || "").match(/\d+/g)?.map(Number).filter((i) => i >= 0 && i < results.length) || [];
                      const unique = [...new Set(indices)];
                      if (unique.length > 0) {
                        const picked = unique.slice(0, topN).map((i) => results[i]).filter(Boolean);
                        resolve(picked.length > 0 ? picked : results.slice(0, topN));
                      } else {
                        resolve(results.slice(0, topN));
                      }
                    } catch {
                      resolve(results.slice(0, topN));
                    }
                  }, 1e4, "rerank");
                }),
                new Promise((resolve) => setTimeout(() => resolve(results.slice(0, topN)), 12e3))
              ]);
              try {
                const { learnAssociation: _crLearn } = await import("./aam.ts");
                const _namTopContents = new Set(results.slice(0, topN).map((r) => r.content));
                const queryKw = (query.match(/[\u4e00-\u9fff]{2,}|[a-zA-Z]{3,}/gi) || []).slice(0, 5);
                for (const mem of reranked) {
                  if (!_namTopContents.has(mem.content)) {
                    const memKw = ((mem.content || "").match(/[\u4e00-\u9fff]{2,}|[a-zA-Z]{3,}/gi) || []).slice(0, 5);
                    if (queryKw.length > 0 && memKw.length > 0) {
                      _crLearn(queryKw.join(" ") + " " + memKw.join(" "), 0.8);
                    }
                  }
                }
              } catch {
              }
              results = reranked;
              console.log(`[cc-soul][search] LLM rerank: ${recallN} \u2192 ${results.length} results`);
            } catch {
              results = results.slice(0, topN);
            }
          } else {
            results = results.slice(0, topN);
          }
          const { getFactSummary, queryFacts } = await import("./fact-store.ts");
          const facts = queryFacts({ subject: userId });
          res.writeHead(200);
          res.end(JSON.stringify({
            memories: results.map((m) => ({ content: m.content, scope: m.scope, ts: m.ts, confidence: m.confidence })),
            facts: facts.map((f) => ({ predicate: f.predicate, object: f.object, confidence: f.confidence })),
            fact_summary: getFactSummary(userId),
            _meta: { reranked: llmAvailable && recallN > topN, query_rewritten: query !== (body.query || body.message || "") }
          }));
        } catch (e) {
          res.writeHead(500);
          res.end(JSON.stringify({ error: e.message }));
        }
        return;
      }
      if (url === "/health" && req.method === "GET") {
        let sqliteStatus = "unknown";
        let memoryCount = 0;
        let factCount = 0;
        try {
          const db = globalThis.__ccSoulSqlite?.db;
          if (db) {
            sqliteStatus = "connected";
            memoryCount = db.prepare("SELECT COUNT(*) as c FROM memories").get()?.c ?? 0;
            factCount = db.prepare("SELECT COUNT(*) as c FROM structured_facts").get()?.c ?? 0;
          } else {
            sqliteStatus = "disconnected";
          }
        } catch {
          sqliteStatus = "error";
        }
        let llm = { configured: false, connected: false, model: "", error: "" };
        try {
          llm = require("./cli.ts").getLLMStatus();
        } catch {
        }
        res.writeHead(200);
        res.end(JSON.stringify({
          status: "ok",
          version: "2.9.2",
          port: SOUL_API_PORT,
          uptime: Math.floor(process.uptime()),
          sqlite: sqliteStatus,
          memoryCount,
          factCount,
          llm
        }));
        return;
      }
      res.writeHead(404);
      res.end(JSON.stringify({
        error: "not found",
        endpoints: [
          "POST /memories  \u2014 add memory",
          "POST /search    \u2014 search memories",
          "GET  /health    \u2014 health check"
        ]
      }));
    } catch (e) {
      res.writeHead(500);
      res.end(JSON.stringify({ error: e.message }));
    }
  });
  server.listen(SOUL_API_PORT, "0.0.0.0", () => {
    console.log(`
  cc-soul Memory API \u2014 http://0.0.0.0:${SOUL_API_PORT}`);
    console.log(`  POST /memories  \u2014 add memory`);
    console.log(`  POST /search    \u2014 search memories`);
    console.log(`  GET  /health    \u2014 health check
`);
  });
  server.on("error", (e) => {
    if (e.code === "EADDRINUSE") console.log(`[cc-soul] port ${SOUL_API_PORT} in use`);
    else console.error(`[cc-soul] error: ${e.message}`);
  });
  let shuttingDown = false;
  const shutdown = async (signal) => {
    if (shuttingDown) return;
    shuttingDown = true;
    console.log(`[cc-soul] ${signal} received, shutting down...`);
    const forceExit = setTimeout(() => {
      console.error(`[cc-soul] forced exit after 5s timeout`);
      process.exit(1);
    }, 5e3);
    try {
      server.close();
    } catch {
    }
    try {
      stopSoulEngine();
    } catch {
    }
    try {
      require("./persistence.ts").flushAll();
    } catch {
    }
    try {
      require("./memory.ts").saveMemories();
    } catch {
    }
    try {
      const db = globalThis.__ccSoulSqlite?.db;
      if (db) {
        db.exec("PRAGMA wal_checkpoint(TRUNCATE)");
        db.close();
      }
    } catch {
    }
    try {
      require("./memory-utils.ts").emitCacheEvent("consolidation");
    } catch {
    }
    clearTimeout(forceExit);
    console.log(`[cc-soul] graceful shutdown complete`);
    process.exit(0);
  };
  process.on("SIGTERM", () => shutdown("SIGTERM"));
  process.on("SIGINT", () => shutdown("SIGINT"));
}
const isMain = typeof process !== "undefined" && process.argv[1]?.endsWith("soul-api.ts");
if (isMain) {
  console.log("[cc-soul] Standalone mode");
  initSoulEngine().then(() => startSoulApi());
}
export {
  configureLLM,
  initSoulEngine,
  startSoulApi,
  stopSoulEngine
};
