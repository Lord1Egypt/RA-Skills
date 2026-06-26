import { spawnSync } from "node:child_process";
import { existsSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

  const command = process.argv[2] || "bridge:preflight";
const allowedCommands = new Set([
  "setup",
  "bridge:preflight",
  "bridge:ensure-live"
]);

if (!allowedCommands.has(command)) {
  console.error(`[bookmark-organize] unsupported command: ${command}`);
  process.exit(2);
}

const scriptDir = dirname(fileURLToPath(import.meta.url));
const repoRoot = resolve(scriptDir, "..");

if (!existsSync(resolve(repoRoot, "node_modules"))) {
  console.log("[bookmark-organize] installing local bridge dependencies...");
  const install = spawnSync("npm", ["install", "--omit=dev"], {
    cwd: repoRoot,
    stdio: "inherit"
  });
  if (install.status !== 0) {
    process.exit(install.status ?? 1);
  }
}

const result = spawnSync("npm", ["run", command], {
  cwd: repoRoot,
  stdio: "inherit"
});

process.exit(result.status ?? 1);
