import assert from "node:assert/strict";
import { execFile } from "node:child_process";
import { mkdtemp, readFile, readdir, rm, writeFile } from "node:fs/promises";
import { createServer } from "node:http";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { fileURLToPath } from "node:url";
import { promisify } from "node:util";
import test from "node:test";

const execute = promisify(execFile);
const runner = fileURLToPath(new URL("./run.mjs", import.meta.url));
const browserId = "mock-current-sample-browser";
const accountAlias = "测试店铺";
const history = [{ title: "历史无关商品_UNRELATED_HISTORY", price: 9999, sourceUrl: "https://www.goofish.com/item?id=history" }];
const current = [{ title: "当前指纹浏览器定制", price: 188, sourceUrl: "https://www.goofish.com/item?id=current", sellerName: "测试卖家", condition: "定制服务", brand: "自主开发", collectedAt: "2026-10-04T10:00:00Z" }];

// 完整模拟 Bridge 生命周期，测试始终只连接随机本机端口，不操作真实浏览器。
async function withMockBridge(collected, check) {
  const calls = [];
  const directory = await mkdtemp(join(tmpdir(), "xianyu-current-sample-"));
  const output = join(directory, "output");
  const input = join(directory, "input.json");
  const server = createServer(async (request, response) => {
    try {
      assert.equal(request.headers.authorization, "Bearer isolated-test-token");
      response.setHeader("Content-Type", "application/json");
      if (request.method === "GET" && request.url === "/v1/browsers") {
        calls.push("list");
        response.end(JSON.stringify({ browsers: [{ browserId, online: true }] }));
        return;
      }
      assert.equal(request.method, "POST");
      assert.equal(request.url, `/v1/browsers/${browserId}/commands`);
      let raw = "";
      for await (const chunk of request) raw += chunk;
      const body = JSON.parse(raw);
      if (body.action === "navigate") {
        calls.push("navigate");
        assert.equal(body.args.url, "https://www.goofish.com/search?q=" + encodeURIComponent("指纹浏览器"));
        assert.equal(body.args.newTab, true);
        response.end(JSON.stringify({ result: { tabId: 42 } }));
      } else if (body.action === "close_session") {
        calls.push("close");
        assert.ok(body.args.session.startsWith("xianyu-competitor-"));
        response.end(JSON.stringify({ result: { ok: true } }));
      } else {
        assert.equal(body.action, "extension_message");
        const message = body.args.message;
        assert.equal(message.type, "DHH_EXTERNAL_COMMAND");
        assert.equal(message.browserId, browserId);
        assert.equal(message.accountAlias, accountAlias);
        calls.push(message.action);
        if (message.action === "health") {
          response.end(JSON.stringify({ result: { ok: true, result: { store: { browserId, alias: accountAlias } } } }));
        } else {
          assert.equal(message.action, "collect");
          assert.equal(message.tabId, 42);
          assert.equal(message.payload.limit, 7);
          response.end(JSON.stringify({ result: { ok: true, result: collected } }));
        }
      }
    } catch (error) {
      response.statusCode = 500;
      response.end(JSON.stringify({ error: error.message }));
    }
  });
  try {
    await new Promise((resolve) => server.listen(0, "127.0.0.1", resolve));
    await writeFile(input, JSON.stringify({ browserId, accountAlias, keyword: "指纹浏览器", limit: 7 }));
    let execution;
    try {
      execution = { ...(await execute(process.execPath, [runner, "--input", input, "--output", output], {
        env: { ...process.env, EASY_WEBBRIDGE_URL: `http://127.0.0.1:${server.address().port}`, EASY_WEBBRIDGE_TOKEN: "isolated-test-token" },
        timeout: 12000,
      })), code: 0 };
    } catch (error) {
      execution = error;
    }
    assert.equal(execution.stderr, "");
    await check({ result: JSON.parse(execution.stdout), code: execution.code, output });
    assert.deepEqual(calls, ["list", "navigate", "health", "collect", "close"]);
  } finally {
    await new Promise((resolve) => server.close(resolve));
    await rm(directory, { recursive: true, force: true });
  }
}

test("报告只包含当前搜索样本，历史无关商品不进入 JSON、CSV 或 Markdown", async () => {
  await withMockBridge({ products: history, collectedProducts: current }, async ({ result, code, output }) => {
    assert.equal(code, 0);
    assert.equal(result.ok, true);
    assert.equal(result.status, "completed");
    assert.equal(result.sampleSize, 1);
    const report = JSON.parse(await readFile(join(output, "competitors.json"), "utf8"));
    assert.equal(report.products[0].title, current[0].title);
    assert.equal(report.priceSummary.median, 188);
    for (const name of ["competitors.json", "competitors.csv", "competitors.md"]) {
      const text = await readFile(join(output, name), "utf8");
      assert.ok(text.includes(current[0].title));
      assert.ok(!text.includes(history[0].title));
    }
  });
});

test("当前采样为空时返回 partial，不使用非空历史商品库补齐", async () => {
  await withMockBridge({ products: history, collectedProducts: [] }, async ({ result, code, output }) => {
    assert.equal(code, 0);
    assert.equal(result.status, "partial");
    assert.equal(result.sampleSize, 0);
    const report = JSON.parse(await readFile(join(output, "competitors.json"), "utf8"));
    assert.deepEqual(report.products, []);
    assert.equal(report.priceSummary.max, 0);
  });
});

for (const [name, collected] of [["缺少当前采样", { products: history }], ["当前采样类型错误", { products: history, collectedProducts: {} }]]) {
  test(`${name}明确失败并关闭本次会话，不写成功报告`, async () => {
    await withMockBridge(collected, async ({ result, code, output }) => {
      assert.equal(code, 1);
      assert.equal(result.ok, false);
      assert.match(result.error, /本次采样 collectedProducts 数组/);
      await assert.rejects(readdir(output), { code: "ENOENT" });
    });
  });
}
