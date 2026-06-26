import { readFileSync, existsSync } from "node:fs";
import { resolve } from "node:path";

/** 从项目根 `.env` 加载 KEY=value（不覆盖已有环境变量） */
export function loadDotEnv(cwd = process.cwd(), envPath) {
  const p = envPath ?? resolve(cwd, ".env");
  if (!existsSync(p)) return;
  const raw = readFileSync(p, "utf8");
  for (const line of raw.split("\n")) {
    const t = line.trim();
    if (!t || t.startsWith("#")) continue;
    const eq = t.indexOf("=");
    if (eq <= 0) continue;
    const key = t.slice(0, eq).trim();
    let val = t.slice(eq + 1).trim();
    if (
      (val.startsWith('"') && val.endsWith('"')) ||
      (val.startsWith("'") && val.endsWith("'"))
    ) {
      val = val.slice(1, -1);
    }
    if (process.env[key] === undefined) process.env[key] = val;
  }
}
