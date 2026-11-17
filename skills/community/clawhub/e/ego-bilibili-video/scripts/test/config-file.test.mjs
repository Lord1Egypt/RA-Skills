import assert from "node:assert/strict";
import { test } from "node:test";
import { readConfigSyncImpl } from "../lib/config-file.mjs";

function fakeFs(content) {
  return { readFileSync: () => content };
}

test("readConfigSyncImpl parses a config object", () => {
  const cfg = readConfigSyncImpl(fakeFs(JSON.stringify({ video: "/v.mp4", title: "t" })), "/tmp/x.json");
  assert.equal(cfg.video, "/v.mp4");
});

test("readConfigSyncImpl rejects non-object and bad json", () => {
  assert.throws(() => readConfigSyncImpl(fakeFs("[]")));
  assert.throws(() => readConfigSyncImpl(fakeFs("not json")));
});
