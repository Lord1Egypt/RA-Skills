import path from "node:path";
import process from "node:process";
import { fileURLToPath } from "node:url";
import { spawnSync } from "node:child_process";

import { bootstrapSuite } from "./bootstrap.mjs";

const DEFAULT_WORKFLOW = "cover";
const skillDir = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const setupScript = path.join(skillDir, "scripts", "vendor", "weryai-image", "setup.mjs");

const argv = process.argv.slice(2);
const workflowIndex = argv.indexOf("--workflow");
if (workflowIndex === -1) argv.push("--workflow", DEFAULT_WORKFLOW);
const projectIndex = argv.indexOf("--project");
if (projectIndex === -1) argv.push("--project", process.cwd());
const dryRun = argv.includes("--dry-run");
const bootstrap = bootstrapSuite({ dir: skillDir, dryRun });
if (!bootstrap.ok) process.exit(1);
const skillNamespace = process.env.IMAGE_SKILL_NAMESPACE?.trim() || path.basename(skillDir);
const result = spawnSync(process.execPath, [setupScript, ...argv], {
  stdio: "inherit",
  env: {
    ...process.env,
    IMAGE_SKILL_NAMESPACE: skillNamespace,
    IMAGE_SKILL_LABEL: process.env.IMAGE_SKILL_LABEL?.trim() || skillNamespace,
  },
});
process.exit(result.status ?? 1);
