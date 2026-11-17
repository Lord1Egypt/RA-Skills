#!/usr/bin/env node
"use strict";

const fs = require("node:fs");
const http = require("node:http");
const https = require("node:https");
const path = require("node:path");
const { spawn } = require("node:child_process");

const { resolveReportAgent } = require("./detect-agent");

const SKILL_NAME = "byted-livesaas-master";
const DEFAULT_ENDPOINT = "https://live.byteoc.com/apiservice/skill/track";
const TIMEOUT_MS = 800;

function readVersion() {
  try {
    return fs.readFileSync(path.join(__dirname, "..", "VERSION"), "utf8").trim();
  } catch {
    return "";
  }
}

function readArg(name) {
  const prefix = `--${name}=`;
  const inline = process.argv.find((arg) => arg.startsWith(prefix));
  if (inline) return inline.slice(prefix.length);
  const index = process.argv.indexOf(`--${name}`);
  if (index >= 0) return process.argv[index + 1] || "";
  return "";
}

function postJsonWithNode(urlString, payload) {
  return new Promise((resolve) => {
    let url;
    try {
      url = new URL(urlString);
    } catch {
      resolve({ ok: false, fallback: false });
      return;
    }

    const body = JSON.stringify(payload);
    const client = url.protocol === "http:" ? http : https;
    const req = client.request(
      url,
      {
        method: "POST",
        timeout: TIMEOUT_MS,
        headers: {
          "content-type": "application/json",
          "content-length": Buffer.byteLength(body),
        },
      },
      (res) => {
        res.resume();
        res.on("end", () => resolve({ ok: res.statusCode >= 200 && res.statusCode < 500, fallback: false }));
      }
    );
    req.on("timeout", () => {
      req.destroy();
      resolve({ ok: false, fallback: true });
    });
    req.on("error", () => resolve({ ok: false, fallback: true }));
    req.end(body);
  });
}

function postJsonWithCurl(urlString, payload) {
  return new Promise((resolve) => {
    const body = JSON.stringify(payload);
    const child = spawn(
      "curl",
      [
        "-L",
        "-sS",
        "-o",
        "/dev/null",
        "-w",
        "%{http_code}",
        "-X",
        "POST",
        urlString,
        "-H",
        "content-type: application/json",
        "--data-binary",
        "@-",
        "--max-time",
        String(Math.max(1, Math.ceil(TIMEOUT_MS / 1000))),
      ],
      { stdio: ["pipe", "pipe", "ignore"] }
    );
    let output = "";
    let settled = false;
    const finish = (ok) => {
      if (settled) return;
      settled = true;
      resolve(ok);
    };
    const timer = setTimeout(() => {
      child.kill();
      finish(false);
    }, TIMEOUT_MS + 500);

    child.stdout.on("data", (chunk) => {
      output += chunk.toString("utf8");
    });
    child.on("error", () => {
      clearTimeout(timer);
      finish(false);
    });
    child.on("close", () => {
      clearTimeout(timer);
      const statusCode = Number(output.trim().slice(-3));
      finish(statusCode >= 200 && statusCode < 500);
    });
    child.stdin.end(body);
  });
}

async function postJson(urlString, payload) {
  const result = await postJsonWithNode(urlString, payload);
  if (result.ok || !result.fallback) return result.ok;
  return postJsonWithCurl(urlString, payload);
}

async function main() {
  if (process.env.BYTEDLIVE_TELEMETRY_DISABLED === "1" || process.env.BYTEDLIVE_TELEMETRY_DISABLED === "true") {
    return;
  }

  await postJson(process.env.BYTEDLIVE_TELEMETRY_ENDPOINT || DEFAULT_ENDPOINT, {
    skillName: SKILL_NAME,
    agent: resolveReportAgent({
      cliArg: readArg("agent"),
      skillRootDir: path.join(__dirname, ".."),
    }),
    source: "skill-start",
    action: "skill_use",
    eventId: readArg("event-id") || undefined,
    skillVersion: readVersion(),
  });
}

main().catch(() => {});
