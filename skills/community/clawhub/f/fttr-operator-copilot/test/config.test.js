import assert from "node:assert/strict";
import test from "node:test";

import { DEFAULT_FTTRAI_RPC_URL, loadConfig } from "../src/config.js";

test("loadConfig reads operator token and defaults", () => {
  const config = loadConfig({
    FTTRAI_OPERATOR_AUTH_TOKEN: "operator-token",
  });

  assert.equal(config.baseUrl, DEFAULT_FTTRAI_RPC_URL);
  assert.equal(config.token, "operator-token");
  assert.equal(config.timeoutMs, 30000);
  assert.equal(config.maxRetries, 2);
});

test("loadConfig requires operator token", () => {
  assert.throws(
    () => loadConfig({}),
    /FTTRAI_OPERATOR_AUTH_TOKEN/,
  );
});
