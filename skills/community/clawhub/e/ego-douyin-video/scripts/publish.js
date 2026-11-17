#!/usr/bin/env node
// Publish one local video on https://creator.douyin.com (runs inside ego-browser).
// Arguments come from /tmp/douyin-video-publish.json written by publish.sh.
// Exit 0: redirected to content/manage or the page says 发布成功.
// Exit 1: flow error. Exit 2: login required (handOff done, space left open).

import { existsSync, statSync } from "node:fs";
import { readConfigSync } from "./lib/config-file.mjs";
import { PUBLISH_CONFIG_PATH } from "./lib/pure.mjs";
import { executePublish } from "./lib/publish-flow.mjs";

let cfg = null;
try {
  cfg = readConfigSync(PUBLISH_CONFIG_PATH);
} catch {
  cfg = null;
}

const code = await executePublish(cfg, {
  taskSpace: globalThis.taskSpace,
  existsSync,
  statSync,
});
process.exit(code);
