import { readFile } from "node:fs/promises";
import { readFileSync } from "node:fs";
import { PUBLISH_CONFIG_PATH } from "./pure.mjs";

function parse(raw) {
  const cfg = JSON.parse(raw);
  if (!cfg || typeof cfg !== "object" || Array.isArray(cfg)) throw new Error("invalid config");
  return cfg;
}

export async function readConfig(path = PUBLISH_CONFIG_PATH) {
  return parse(await readFile(path, "utf8"));
}

export function readConfigSync(path = PUBLISH_CONFIG_PATH) {
  return parse(readFileSync(path, "utf8"));
}

// Test seam: inject a fake fs module.
export function readConfigSyncImpl(fsMod, path = PUBLISH_CONFIG_PATH) {
  return parse(fsMod.readFileSync(path, "utf8"));
}
