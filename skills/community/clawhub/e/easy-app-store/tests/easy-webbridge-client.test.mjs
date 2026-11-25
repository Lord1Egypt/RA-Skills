import assert from "node:assert/strict";
import { spawn } from "node:child_process";
import { createServer } from "node:http";
import { after, before, test } from "node:test";
import { fileURLToPath } from "node:url";

const script = fileURLToPath(new URL("../scripts/easy-webbridge-client.mjs", import.meta.url));
const token = "unit-test-token";
let server;
let baseUrl;
let browsers = [];
const requests = [];

before(async () => {
  server = createServer(async (req, res) => {
    const chunks = [];
    for await (const chunk of req) chunks.push(chunk);
    const body = Buffer.concat(chunks).toString("utf8");
    requests.push({ method: req.method, url: req.url, authorization: req.headers.authorization, body: body ? JSON.parse(body) : null });
    res.setHeader("content-type", "application/json");
    if (req.method === "GET" && req.url === "/health") {
      res.end(JSON.stringify({ ok: true, service: "easy-webbridge" }));
    } else if (req.method === "GET" && req.url === "/v1/browsers") {
      res.end(JSON.stringify({ browsers }));
    } else if (req.method === "POST" && req.url.includes("/commands")) {
      res.end(JSON.stringify({ ok: true, accepted: true }));
    } else {
      res.statusCode = 404;
      res.end(JSON.stringify({ error: "not found" }));
    }
  });
  await new Promise((resolve) => server.listen(0, "127.0.0.1", resolve));
  baseUrl = `http://127.0.0.1:${server.address().port}`;
});

after(async () => {
  await new Promise((resolve) => server.close(resolve));
});

function run(args) {
  return new Promise((resolve, reject) => {
    const child = spawn(process.execPath, [script, ...args], {
      env: { ...process.env, EASY_WEBBRIDGE_URL: baseUrl, EASY_WEBBRIDGE_TOKEN: token },
      stdio: ["ignore", "pipe", "pipe"],
    });
    let stdout = "";
    let stderr = "";
    child.stdout.setEncoding("utf8").on("data", (chunk) => { stdout += chunk; });
    child.stderr.setEncoding("utf8").on("data", (chunk) => { stderr += chunk; });
    child.on("error", reject);
    child.on("close", (status) => resolve({ status, stdout, stderr }));
  });
}

test("preflight lists online browsers without echoing its token", async () => {
  browsers = [
    { browserId: "offline", displayName: "Offline", online: false },
    { browserId: "browser-1", displayName: "Test ASC", online: true, platform: "macOS" },
  ];
  const result = await run(["preflight"]);
  assert.equal(result.status, 0, result.stderr);
  const output = JSON.parse(result.stdout);
  assert.deepEqual(output.browsers, [{ browserId: "browser-1", name: "Test ASC", platform: "macOS", version: null }]);
  assert.ok(!result.stdout.includes(token));
  assert.ok(requests.some((request) => request.authorization === `Bearer ${token}`));
});

test("preflight reports when no connected browser is online", async () => {
  browsers = [{ browserId: "offline", online: false }];
  const result = await run(["preflight"]);
  assert.equal(result.status, 1);
  assert.equal(JSON.parse(result.stdout).code, "browser-offline");
});

test("snapshot sends a validated numeric tab ID to the selected browser", async () => {
  const beforeCount = requests.length;
  const result = await run(["snapshot", "browser-1", "42"]);
  assert.equal(result.status, 0, result.stderr);
  const request = requests.slice(beforeCount).find((item) => item.method === "POST");
  assert.equal(request.url, "/v1/browsers/browser-1/commands");
  assert.deepEqual(request.body, { action: "snapshot", args: { tabId: 42 } });
});

test("invalid tab IDs fail before sending a browser command", async () => {
  const beforeCount = requests.length;
  const result = await run(["snapshot", "browser-1", "not-a-number"]);
  assert.equal(result.status, 1);
  assert.equal(JSON.parse(result.stdout).code, "invalid-arguments");
  assert.equal(requests.slice(beforeCount).filter((item) => item.method === "POST").length, 0);
});

test("generic command accepts object arguments and rejects JSON arrays", async () => {
  const beforeCount = requests.length;
  const invalid = await run(["command", "browser-1", "snapshot", "[]"]);
  assert.equal(invalid.status, 1);
  assert.equal(JSON.parse(invalid.stdout).code, "invalid-arguments");
  assert.equal(requests.slice(beforeCount).filter((item) => item.method === "POST").length, 0);

  const valid = await run(["command", "browser-1", "snapshot", '{"tabId":7}']);
  assert.equal(valid.status, 0, valid.stderr);
  const request = requests.slice(beforeCount).find((item) => item.method === "POST");
  assert.deepEqual(request.body, { action: "snapshot", args: { tabId: 7 } });
});

test("upload requires absolute paths and forwards them unchanged", async () => {
  const beforeCount = requests.length;
  const relative = await run(["upload", "browser-1", "input[type=file]", "build.ipa"]);
  assert.equal(relative.status, 1);
  assert.equal(JSON.parse(relative.stdout).code, "invalid-arguments");
  assert.equal(requests.slice(beforeCount).filter((item) => item.method === "POST").length, 0);

  const absolute = await run(["upload", "browser-1", "input[type=file]", "/tmp/build.ipa"]);
  assert.equal(absolute.status, 0, absolute.stderr);
  const request = requests.slice(beforeCount).find((item) => item.method === "POST");
  assert.deepEqual(request.body, { action: "upload", args: { selector: "input[type=file]", files: ["/tmp/build.ipa"] } });
});
