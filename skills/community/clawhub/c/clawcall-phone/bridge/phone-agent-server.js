#!/usr/bin/env node
"use strict";

const http = require("http");
const { execFile, spawn } = require("child_process");
const { buildPhoneContext, getBasicProfile, getCronSummary, getTaskSummary } = require("./phone-context");
const { buildPhonePrompt } = require("./phone-prompt");

const HOST = process.env.CLAWCALL_AGENT_HOST || "127.0.0.1";
const PORT = parseInt(process.env.CLAWCALL_AGENT_PORT || "4747", 10);
const MODEL = process.env.CLAWCALL_PHONE_MODEL || "";
const MODEL_MODE = (process.env.CLAWCALL_PHONE_MODEL_MODE || "gateway").toLowerCase(); // gateway | local
const MODEL_TIMEOUT_MS = parseInt(process.env.CLAWCALL_PHONE_TIMEOUT_MS || "25000", 10);
const MAX_BODY_BYTES = 64 * 1024;

function sendJson(res, code, body) {
  const raw = JSON.stringify(body);
  res.writeHead(code, {
    "Content-Type": "application/json; charset=utf-8",
    "Content-Length": Buffer.byteLength(raw),
  });
  res.end(raw);
}

function collectJson(req) {
  return new Promise((resolve, reject) => {
    let size = 0;
    const chunks = [];
    req.on("data", (chunk) => {
      size += chunk.length;
      if (size > MAX_BODY_BYTES) {
        reject(new Error("payload too large"));
        req.destroy();
        return;
      }
      chunks.push(chunk);
    });
    req.on("end", () => {
      try {
        const text = Buffer.concat(chunks).toString("utf8") || "{}";
        resolve(JSON.parse(text));
      } catch (err) {
        reject(err);
      }
    });
    req.on("error", reject);
  });
}

function extractModelReply(stdout) {
  const text = (stdout || "").trim();
  if (!text) return "";

  const lines = text.split(/\r?\n/).filter(Boolean).reverse();
  for (const line of lines) {
    try {
      const parsed = JSON.parse(line);
      const candidates = [
        parsed.text,
        parsed.output_text,
        parsed.result,
        parsed.response,
        parsed.message,
        parsed.content,
        parsed.output?.text,
        parsed.output?.[0]?.content?.[0]?.text,
      ];
      const hit = candidates.find((v) => typeof v === "string" && v.trim());
      if (hit) return hit.trim();
    } catch {}
  }

  return text;
}

function runModel(prompt) {
  return new Promise((resolve, reject) => {
    const args = ["infer", "model", "run", MODEL_MODE === "local" ? "--local" : "--gateway", "--json", "--prompt", prompt];
    if (MODEL) args.splice(4, 0, "--model", MODEL);

    if (process.platform === "win32") {
      const child = spawn("openclaw", args, {
        shell: true,
        windowsHide: true,
        stdio: ["ignore", "pipe", "pipe"],
      });

      let stdout = "";
      let stderr = "";
      let settled = false;

      const timer = setTimeout(() => {
        try { child.kill(); } catch {}
        if (!settled) {
          settled = true;
          reject(new Error("model run timed out"));
        }
      }, MODEL_TIMEOUT_MS);

      child.stdout.on("data", (chunk) => { stdout += chunk.toString("utf8"); });
      child.stderr.on("data", (chunk) => { stderr += chunk.toString("utf8"); });

      child.on("error", (error) => {
        clearTimeout(timer);
        if (!settled) {
          settled = true;
          reject(error);
        }
      });

      child.on("close", () => {
        clearTimeout(timer);
        if (settled) return;
        settled = true;
        const reply = extractModelReply(stdout);
        if (reply) return resolve(reply);
        reject(new Error((stderr || "empty model response").trim()));
      });
      return;
    }

    execFile("openclaw", args, {
      timeout: MODEL_TIMEOUT_MS,
      encoding: "utf8",
      windowsHide: true,
      maxBuffer: 1024 * 1024,
    }, (error, stdout, stderr) => {
      const reply = extractModelReply(stdout);
      if (reply) return resolve(reply);
      if (error) {
        const reason = (stderr || error.message || "model run failed").trim();
        return reject(new Error(reason));
      }
      reject(new Error((stderr || "empty model response").trim()));
    });
  });
}

async function handleCallMessage(body) {
  const message = String(body?.message || "").trim();
  if (!message) {
    return { response: "I didn’t catch that. Could you say it again?", end_call: false };
  }

  const lower = message.toLowerCase();
  const profile = getBasicProfile();

  if (/what(?:'s| is) your name|who are you|your name/.test(lower)) {
    return { response: `I’m ${profile.identity} 🎩.`, end_call: false };
  }

  if (/how are you|how're you/.test(lower)) {
    return { response: `I’m doing well, ${profile.user}. I’m here and ready to help.`, end_call: false };
  }

  if (/hello|hi|hey/.test(lower) && lower.length < 40) {
    return { response: `Hey ${profile.user}, I’m ${profile.identity}. What do you need?`, end_call: false };
  }

  if (/cron|reminder|schedule|scheduled|job/.test(lower) && !/meeting|calendar/.test(lower)) {
    const cronSummary = await getCronSummary();
    return { response: `Here are your active cron jobs. ${cronSummary.replace(/\n/g, ' ')}`, end_call: false };
  }

  if (/task|tasks|background|running|pending/.test(lower)) {
    const taskSummary = await getTaskSummary();
    return { response: `Here are your current tasks. ${taskSummary.replace(/\n/g, ' ')}`, end_call: false };
  }

  const context = await buildPhoneContext(message);
  const prompt = buildPhonePrompt({
    identity: context.identity,
    user: context.user,
    contextText: context.contextText,
    message,
  });

  try {
    const reply = await runModel(prompt);
    return {
      response: reply || "I’m here. Could you say that one more time?",
      end_call: false,
    };
  } catch (err) {
    console.error(`[ClawCallBridge] model error: ${err.message}`);
    return {
      response: "I had a little trouble with that. Could you try again?",
      end_call: false,
    };
  }
}

const server = http.createServer(async (req, res) => {
  if (req.method === "GET" && req.url === "/health") {
    return sendJson(res, 200, { ok: true, host: HOST, port: PORT, mode: MODEL_MODE, model: MODEL || null });
  }

  if (req.method === "POST" && req.url === "/clawcall/message") {
    try {
      const body = await collectJson(req);
      const startedAt = Date.now();
      const result = await handleCallMessage(body);
      console.log(`[ClawCallBridge] handled call in ${Date.now() - startedAt}ms`);
      return sendJson(res, 200, result);
    } catch (err) {
      console.error(`[ClawCallBridge] request error: ${err.message}`);
      return sendJson(res, 500, {
        response: "I’m having a little trouble right now. Please try again.",
        end_call: false,
      });
    }
  }

  sendJson(res, 404, { ok: false, error: "not found" });
});

server.listen(PORT, HOST, () => {
  console.log(`[ClawCallBridge] listening on http://${HOST}:${PORT}`);
  console.log(`[ClawCallBridge] model mode=${MODEL_MODE}${MODEL ? ` model=${MODEL}` : ""}`);
});
