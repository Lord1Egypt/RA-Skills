#!/usr/bin/env node
// Publish one local video on https://studio.youtube.com (runs inside ego-browser).
// Arguments come from /tmp/youtube-video-publish.json written by publish.sh.
// Exit 0: video URL/ID plus a processing status. Exit 1: flow error. Exit 2: login required.

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
