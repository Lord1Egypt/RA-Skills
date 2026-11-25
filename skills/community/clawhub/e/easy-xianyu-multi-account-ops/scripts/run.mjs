#!/usr/bin/env node
import { mkdir, readFile, rename, writeFile } from "node:fs/promises";
import { homedir } from "node:os";
import { dirname, join, resolve } from "node:path";

const bridgeUrl = process.env.EASY_WEBBRIDGE_URL || "http://127.0.0.1:17777";
const dianqunhelpExtensionId = process.env.DIANQUNHELP_EXTENSION_ID || "oapgddmgefblpkmalflpkolkmbfhegaj";
const readActions = new Set(["collect", "sync-orders", "order-detail"]);
const writeActions = new Set(["publish", "deliver"]);
function clean(value) { return String(value ?? "").replace(/\s+/g, " ").trim(); }
function arg(name) { const index = process.argv.indexOf(name); return index < 0 ? "" : process.argv[index + 1] || ""; }
function print(value) { process.stdout.write(`${JSON.stringify(value, null, 2)}\n`); }
async function token() { if (process.env.EASY_WEBBRIDGE_TOKEN) return process.env.EASY_WEBBRIDGE_TOKEN; return (await readFile(join(homedir(), ".easy-webbridge", "bridge-token"), "utf8")).trim(); }
async function request(path, init = {}) { const response = await fetch(`${bridgeUrl}${path}`, { ...init, headers: { Authorization: `Bearer ${await token()}`, "Content-Type": "application/json", ...(init.headers || {}) } }); const body = await response.json().catch(() => ({})); if (!response.ok) throw new Error(body.error || `Easy WebBridge HTTP ${response.status}`); return body; }
async function command(browserId, action, args = {}, timeoutMs = 30000) { return request(`/v1/browsers/${encodeURIComponent(browserId)}/commands`, { method: "POST", body: JSON.stringify({ action, args, timeoutMs }) }); }
async function extensionCommand(account, action, options = {}, timeoutMs = 30000) { const response = await command(account.browserId, "extension_message", { extensionId: dianqunhelpExtensionId, message: { type: "DHH_EXTERNAL_COMMAND", browserId: account.browserId, accountAlias: account.alias, action, ...options } }, timeoutMs); if (!response.result?.ok) throw new Error(response.result?.error || "店群助手执行失败"); return response.result.result; }
async function readJsonIfExists(path, fallback) { try { return JSON.parse(await readFile(path, "utf8")); } catch (error) { if (error.code === "ENOENT") return fallback; throw error; } }
async function writeJsonAtomic(path, value) { await mkdir(dirname(path), { recursive: true }); const temporary = `${path}.${process.pid}.${Date.now()}.tmp`; await writeFile(temporary, `${JSON.stringify(value, null, 2)}\n`, { mode: 0o600 }); await rename(temporary, path); }

function validate(input) {
  const accounts = Array.isArray(input.accounts) ? input.accounts.map((account) => ({ id: clean(account.id), browserId: clean(account.browserId), alias: clean(account.alias) })) : [];
  const jobs = Array.isArray(input.jobs) ? input.jobs.map((job, index) => ({ id: clean(job.id) || `job-${index + 1}`, accountId: clean(job.accountId), action: clean(job.action), payload: job.payload || {}, authorized: Boolean(job.authorized), idempotencyKey: clean(job.idempotencyKey) })) : [];
  if (!accounts.length) throw new Error("accounts 不能为空");
  for (const field of ["id", "browserId", "alias"]) { const values = accounts.map((account) => account[field]); if (values.some((value) => !value) || new Set(values).size !== values.length) throw new Error(`账号 ${field} 必须填写且唯一`); }
  const ids = new Set(accounts.map((account) => account.id));
  for (const job of jobs) { if (!ids.has(job.accountId)) throw new Error(`任务账号不存在：${job.accountId}`); if (!readActions.has(job.action) && !writeActions.has(job.action)) throw new Error(`未知任务：${job.action}`); if (writeActions.has(job.action) && (!job.authorized || !job.idempotencyKey)) throw new Error(`写任务 ${job.id} 必须有 authorized=true 和 idempotencyKey`); }
  return { accounts, jobs, concurrency: Math.max(1, Math.min(Number(input.concurrency) || 2, 4)) };
}

function actionConfig(job) {
  if (job.action === "collect") return { url: `https://www.goofish.com/search?q=${encodeURIComponent(clean(job.payload.keyword))}`, action: "collect", payload: { limit: Math.max(1, Math.min(Number(job.payload.limit) || 10, 30)) }, timeout: 30000 };
  if (job.action === "sync-orders") return { url: "https://seller.goofish.com/?site=COMMONPRO#/seller-trade/order-manage", action: "syncOrders", payload: { pageSize: Number(job.payload.pageSize) || 30 }, timeout: 60000 };
  if (job.action === "order-detail") return { url: `https://www.goofish.com/order-detail?orderId=${encodeURIComponent(clean(job.payload.orderId))}&role=seller`, action: "orderDetail", payload: { orderId: clean(job.payload.orderId) }, timeout: 30000 };
  if (job.action === "publish") return { url: "https://www.goofish.com/", action: "publish", payload: job.payload.product || job.payload, timeout: 100000 };
  if (job.action === "deliver") return { url: "https://www.goofish.com/", action: "deliver", payload: { orderId: clean(job.payload.orderId), text: String(job.payload.text || "").trim() }, timeout: 70000 };
  throw new Error(`不支持的任务：${job.action}`);
}

async function runJob(account, job, journal, persistJournal) {
  const config = actionConfig(job); const session = `dianqun-${account.id}-${job.id}-${Date.now()}`; let keepSession = false;
  if (writeActions.has(job.action) && journal[job.idempotencyKey]) return { id: job.id, accountId: account.id, browserId: account.browserId, alias: account.alias, action: job.action, status: "needs_user_action", error: "幂等键已经执行或结果不确定", idempotencyKey: job.idempotencyKey };
  const navigation = await command(account.browserId, "navigate", { url: config.url, newTab: true, active: false, session, groupTitle: `店群助手-${account.alias}` });
  try {
    await new Promise((resolveWait) => setTimeout(resolveWait, job.action === "collect" ? 1800 : 1200));
    const health = await extensionCommand(account, "health", {}, 12000);
    if (health.store?.browserId !== account.browserId || health.store?.alias !== account.alias) throw new Error("店群助手绑定的店铺与本次任务不一致");
    if (writeActions.has(job.action)) {
      journal[job.idempotencyKey] = { status: "running", jobId: job.id, browserId: account.browserId, startedAt: new Date().toISOString() };
      await persistJournal();
    }
    if (job.action === "deliver") {
      const expectedKey = `delivery:${health.store.id}:${clean(job.payload.orderId)}`;
      if (job.idempotencyKey !== expectedKey) throw new Error(`发货幂等键必须是 ${expectedKey}`);
    }
    const result = await extensionCommand(account, config.action, { tabId: navigation.result.tabId, payload: config.payload, authorized: writeActions.has(job.action) && job.authorized, idempotencyKey: job.idempotencyKey }, Math.min(120000, config.timeout + 10000));
    const uncertain = result?.status === "uncertain";
    const status = uncertain ? "uncertain" : "completed";
    if (writeActions.has(job.action)) {
      journal[job.idempotencyKey] = { ...journal[job.idempotencyKey], status, result, finishedAt: new Date().toISOString() };
      await persistJournal();
    }
    return { id: job.id, accountId: account.id, browserId: account.browserId, alias: account.alias, action: job.action, status, idempotencyKey: job.idempotencyKey || "", result, finishedAt: new Date().toISOString() };
  } catch (error) {
    const needsUser = /登录|验证|安全校验|实名|账号不一致/i.test(error.message); const uncertain = writeActions.has(job.action) && /超时|timeout|网络|连接|未响应/i.test(error.message);
    keepSession = needsUser;
    const status = needsUser ? "needs_user_action" : uncertain ? "uncertain" : "failed";
    if (writeActions.has(job.action)) {
      journal[job.idempotencyKey] = { ...(journal[job.idempotencyKey] || {}), status, error: error.message, finishedAt: new Date().toISOString() };
      await persistJournal();
    }
    return { id: job.id, accountId: account.id, browserId: account.browserId, alias: account.alias, action: job.action, status, idempotencyKey: job.idempotencyKey || "", error: error.message, nextAction: uncertain ? "人工回读，禁止自动重试" : needsUser ? "在保留页面中处理" : "修正输入后重新执行", finishedAt: new Date().toISOString() };
  } finally { if (!keepSession) await command(account.browserId, "close_session", { session }).catch(() => {}); }
}

async function schedule(validated, journal, persistJournal) {
  const online = (await request("/v1/browsers")).browsers || [];
  const onlineIds = new Set(online.filter((browser) => browser.online).map((browser) => browser.browserId));
  const accountById = new Map(validated.accounts.map((account) => [account.id, account]));
  const groups = new Map();
  validated.jobs.forEach((job, index) => {
    const account = accountById.get(job.accountId);
    if (!groups.has(account.browserId)) groups.set(account.browserId, []);
    groups.get(account.browserId).push({ index, job, account });
  });
  const browserGroups = [...groups.values()]; let cursor = 0; const results = [];
  const worker = async () => {
    while (cursor < browserGroups.length) {
      const group = browserGroups[cursor++];
      for (const { index, job, account } of group) {
        if (!onlineIds.has(account.browserId)) {
          results[index] = { id: job.id, accountId: account.id, browserId: account.browserId, alias: account.alias, action: job.action, status: "needs_user_action", error: "browserId 不在线" };
          continue;
        }
        results[index] = await runJob(account, job, journal, persistJournal);
      }
    }
  };
  await Promise.all(Array.from({ length: Math.min(validated.concurrency, Math.max(1, browserGroups.length)) }, worker));
  return results;
}

function accountStatus(results) {
  if (!results.length) return "completed";
  const statuses = new Set(results.map((entry) => entry.status));
  if (statuses.size === 1 && statuses.has("completed")) return "completed";
  if (statuses.size === 1 && statuses.has("failed")) return "failed";
  if (statuses.has("needs_user_action") && !statuses.has("completed")) return "needs_user_action";
  return "partial";
}

function selfTest() {
  const valid = validate({ accounts: [{ id: "a", browserId: "b1", alias: "主店" }, { id: "c", browserId: "b2", alias: "副店" }], jobs: [{ accountId: "a", action: "collect", payload: { keyword: "键盘" } }, { accountId: "c", action: "deliver", authorized: true, idempotencyKey: "d:1", payload: { orderId: "1", text: "卡密" } }] });
  if (valid.concurrency !== 2 || valid.jobs.length !== 2) throw new Error("输入校验自测失败");
  let rejected = false; try { validate({ accounts: [{ id: "a", browserId: "b", alias: "A" }, { id: "c", browserId: "b", alias: "C" }], jobs: [] }); } catch { rejected = true; }
  if (!rejected) throw new Error("重复 browserId 自测失败");
  if (accountStatus([{ status: "completed" }, { status: "failed" }]) !== "partial") throw new Error("账号汇总状态自测失败");
  return { ok: true, tests: 3 };
}

async function main() {
  if (process.argv.includes("--self-test")) return print(selfTest());
  const inputPath = arg("--input"); if (!inputPath) throw new Error("用法：node scripts/run.mjs --input jobs.json --output report.json");
  const outputPath = resolve(arg("--output") || join(dirname(resolve(inputPath)), "multi-account-report.json"));
  const journalPath = `${outputPath}.intents.json`; const journal = await readJsonIfExists(journalPath, {});
  const validated = validate(JSON.parse(await readFile(resolve(inputPath), "utf8"))); const startedAt = new Date().toISOString();
  await mkdir(dirname(outputPath), { recursive: true });
  let journalWriteTail = Promise.resolve();
  const persistJournal = () => {
    journalWriteTail = journalWriteTail.then(() => writeJsonAtomic(journalPath, journal));
    return journalWriteTail;
  };
  const results = await schedule(validated, journal, persistJournal);
  const accounts = validated.accounts.map((account) => {
    const accountResults = results.filter((entry) => entry.accountId === account.id);
    const errors = accountResults.filter((entry) => entry.error).map((entry) => ({ jobId: entry.id, message: entry.error }));
    return { ...account, status: accountStatus(accountResults), results: accountResults, errors, nextAction: errors.length ? "处理该店铺失败或待确认任务后再运行" : "该店铺任务已完成" };
  });
  const report = { schemaVersion: 1, mode: "browser-session", accounts, summary: { total: results.length, completed: results.filter((entry) => entry.status === "completed").length, needsUserAction: results.filter((entry) => entry.status === "needs_user_action").length, uncertain: results.filter((entry) => entry.status === "uncertain").length, failed: results.filter((entry) => entry.status === "failed").length }, startedAt, finishedAt: new Date().toISOString(), results };
  await Promise.all([writeJsonAtomic(outputPath, report), persistJournal()]); print(report);
}

main().catch((error) => { print({ ok: false, error: error.message }); process.exitCode = 1; });
