#!/usr/bin/env node
import crypto from "node:crypto";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";

// 优先使用环境变量 SKILL_ROOT 指定的 skill 根目录，否则回退到脚本所在目录的上一级
const SCRIPT_DIR = path.dirname(new URL(import.meta.url).pathname);
const SKILL_ROOT = process.env.SKILL_ROOT || path.resolve(SCRIPT_DIR, "..");
const STORE_DIR = SKILL_ROOT;
const STORE_FILE = path.join(STORE_DIR, "profiles.json");

function parseArgs(argv) {
  const out = { _: [] };
  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (!arg.startsWith("--")) {
      out._.push(arg);
      continue;
    }
    const key = arg.slice(2);
    const next = argv[i + 1];
    if (!next || next.startsWith("--")) {
      out[key] = true;
    } else {
      out[key] = next;
      i += 1;
    }
  }
  return out;
}

function loadProfiles() {
  if (!fs.existsSync(STORE_FILE)) return {};
  return JSON.parse(fs.readFileSync(STORE_FILE, "utf8"));
}

function saveProfiles(profiles) {
  fs.mkdirSync(STORE_DIR, { recursive: true, mode: 0o700 });
  fs.writeFileSync(STORE_FILE, JSON.stringify(profiles, null, 2), { mode: 0o600 });
  fs.chmodSync(STORE_FILE, 0o600);
}

function signParams(params, appSecret) {
  const raw = Object.keys(params)
    .filter((key) => key !== "sign" && params[key] !== undefined && params[key] !== null && params[key] !== "")
    .sort()
    .map((key) => `${key}${typeof params[key] === "object" ? JSON.stringify(params[key]) : params[key]}`)
    .join("");

  return crypto.createHash("md5").update(appSecret + raw, "utf8").digest("hex");
}

function endpoint(env, apiPath) {
  const base = env === "dev" ? "https://dev-api.jushuitan.com" : "https://openapi.jushuitan.com";
  return `${base}${apiPath}`;
}

async function callApi(profile, apiPath, biz) {
  const timestamp = Math.floor(Date.now() / 1000).toString();
  const params = {
    access_token: profile.access_token,
    app_key: profile.app_key,
    timestamp,
    version: "2",
    charset: "utf-8",
    biz: JSON.stringify(biz ?? {}),
  };
  params.sign = signParams(params, profile.app_secret);

  const body = new URLSearchParams(params);
  const response = await fetch(endpoint(profile.env, apiPath), {
    method: "POST",
    headers: { "content-type": "application/x-www-form-urlencoded;charset=UTF-8" },
    body,
  });
  const text = await response.text();
  try {
    return JSON.parse(text);
  } catch {
    return { http_status: response.status, raw: text };
  }
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const command = args._[0];

  if (command === "public-ip") {
    const response = await fetch("https://api.ipify.org?format=json");
    const data = await response.json();
    console.log(JSON.stringify({ ok: true, ip: data.ip }, null, 2));
    return;
  }

  if (command === "save-profile") {
    const name = args.profile || "default";
    for (const key of ["app-key", "app-secret", "access-token"]) {
      if (!args[key]) throw new Error(`Missing --${key}`);
    }
    const profiles = loadProfiles();
    profiles[name] = {
      app_key: args["app-key"],
      app_secret: args["app-secret"],
      access_token: args["access-token"],
      refresh_token: args["refresh-token"] || profiles[name]?.refresh_token || "",
      env: args.env || profiles[name]?.env || "prod",
      updated_at: new Date().toISOString(),
    };
    saveProfiles(profiles);
    console.log(JSON.stringify({ ok: true, profile: name, store: STORE_FILE }, null, 2));
    return;
  }

  if (command === "list-profiles") {
    const profiles = loadProfiles();
    console.log(JSON.stringify(Object.keys(profiles), null, 2));
    return;
  }

  if (command === "call") {
    const name = args.profile || "default";
    const profiles = loadProfiles();
    const profile = profiles[name];
    if (!profile) throw new Error(`Profile not found: ${name}`);
    if (!args.path) throw new Error("Missing --path");
    const biz = args.biz ? JSON.parse(args.biz) : {};
    const result = await callApi(profile, args.path, biz);
    console.log(JSON.stringify(result, null, 2));
    return;
  }

  console.log(`Usage:
  node scripts/jst_erp.mjs save-profile --profile default --app-key ... --app-secret ... --access-token ... [--refresh-token ...] [--env prod]
  node scripts/jst_erp.mjs list-profiles
  node scripts/jst_erp.mjs public-ip
  node scripts/jst_erp.mjs call --profile default --path /open/shops/query --biz '{"page_index":1,"page_size":10}'
`);
}

main().catch((error) => {
  console.error(JSON.stringify({ ok: false, error: error.message }, null, 2));
  process.exit(1);
});
