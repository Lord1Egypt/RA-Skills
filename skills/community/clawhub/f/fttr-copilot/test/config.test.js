import assert from "node:assert/strict";
import test from "node:test";

import { loadConfig } from "../src/config.js";

test("loadConfig reads required values and defaults", () => {
  const config = loadConfig({
    FTTRAI_RPC_URL: "https://fms-main.fttrai.com/api/custom/",
    FTTRAI_AUTH_TOKEN: "token",
  });

  assert.equal(config.baseUrl, "https://fms-main.fttrai.com/api/custom");
  assert.equal(config.token, "token");
  assert.equal(config.timeoutMs, 30000);
  assert.equal(config.maxRetries, 2);
});

test("loadConfig defaults FTTRAI_RPC_URL to fttrai endpoint", () => {
  const config = loadConfig({
    FTTRAI_AUTH_TOKEN: "token",
  });

  assert.equal(config.baseUrl, "https://fms-main.fttrai.com/api");
  assert.equal(config.token, "token");
});

test("loadConfig reports missing required env vars", () => {
  assert.throws(
    () => loadConfig({}),
    (error) => {
      assert.equal(error.code, "missing_config");
      assert.match(error.message, /FTTRAI_AUTH_TOKEN/);
      return true;
    },
  );
});

test("loadConfig rejects unsupported URL protocol", () => {
  assert.throws(
    () => loadConfig({
      FTTRAI_RPC_URL: "ftp://fttrai.example.com",
      FTTRAI_AUTH_TOKEN: "token",
    }),
    (error) => {
      assert.equal(error.code, "invalid_config");
      return true;
    },
  );
});
