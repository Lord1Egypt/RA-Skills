import { readFileSync } from "fs";

export const SKILL_VERSION = JSON.parse(
  readFileSync(new URL("../../package.json", import.meta.url), "utf8"),
).version;
