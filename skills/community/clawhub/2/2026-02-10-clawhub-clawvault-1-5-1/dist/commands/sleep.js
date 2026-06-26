import {
  ClawVault
} from "../chunk-MXNXWOPL.js";
import {
  clearDirtyFlag
} from "../chunk-MZZJLQNQ.js";
import {
  qmdUpdate
} from "../chunk-VJIFT5T5.js";

// src/commands/sleep.ts
import * as fs from "fs";
import * as path from "path";
import * as readline from "readline";
import { execFileSync } from "child_process";
function isInteractive() {
  return Boolean(process.stdin.isTTY && process.stdout.isTTY);
}
async function defaultPrompt(question) {
  const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
  return new Promise((resolve2) => {
    rl.question(question, (answer) => {
      rl.close();
      resolve2(answer.trim());
    });
  });
}
function parseList(raw) {
  if (!raw) return [];
  return raw.split(",").map((item) => item.trim()).filter(Boolean);
}
function ensureNonEmpty(label, items) {
  if (items.length === 0) {
    throw new Error(`${label} is required.`);
  }
}
async function promptForList(label, prompt, interactive) {
  if (!interactive) return [];
  const answer = await prompt(`${label} (comma-separated, empty to skip): `);
  return parseList(answer);
}
function findGitRoot(startPath) {
  let current = path.resolve(startPath);
  while (true) {
    if (fs.existsSync(path.join(current, ".git"))) {
      return current;
    }
    const parent = path.dirname(current);
    if (parent === current) return null;
    current = parent;
  }
}
function getGitStatus(repoRoot) {
  const output = execFileSync("git", ["-C", repoRoot, "status", "--porcelain"], {
    encoding: "utf-8"
  });
  const lines = output.split("\n").filter(Boolean);
  return { clean: lines.length === 0, dirtyCount: lines.length };
}
function isAffirmative(input) {
  const normalized = input.trim().toLowerCase();
  return normalized === "y" || normalized === "yes";
}
async function maybeCommitDirtyRepo(options) {
  if (!options.enabled) {
    return { committed: false, skippedReason: "disabled" };
  }
  const repoRoot = findGitRoot(options.cwd);
  if (!repoRoot) {
    return { committed: false, skippedReason: "no-repo" };
  }
  let status;
  try {
    status = getGitStatus(repoRoot);
  } catch (err) {
    if (err?.code === "ENOENT") {
      return { committed: false, skippedReason: "git-missing" };
    }
    return { repoRoot, committed: false, skippedReason: "status-error" };
  }
  if (status.clean) {
    return { repoRoot, dirtyCount: status.dirtyCount, committed: false, skippedReason: "clean" };
  }
  if (!options.interactive) {
    return { repoRoot, dirtyCount: status.dirtyCount, committed: false, skippedReason: "non-interactive" };
  }
  const confirm = await options.prompt(
    `Git repo dirty (${status.dirtyCount} change(s)). Commit before sleep? (y/N): `
  );
  if (!isAffirmative(confirm)) {
    return { repoRoot, dirtyCount: status.dirtyCount, committed: false, skippedReason: "declined" };
  }
  const message = await options.prompt("Commit message: ");
  if (!message) {
    return { repoRoot, dirtyCount: status.dirtyCount, committed: false, skippedReason: "no-message" };
  }
  try {
    execFileSync("git", ["-C", repoRoot, "add", "-A"], { stdio: "inherit" });
    execFileSync("git", ["-C", repoRoot, "commit", "-m", message], { stdio: "inherit" });
  } catch (err) {
    throw new Error(`Git commit failed: ${err?.message || "unknown error"}`);
  }
  return {
    repoRoot,
    dirtyCount: status.dirtyCount,
    committed: true,
    message
  };
}
async function sleep(options) {
  const prompt = options.prompt ?? defaultPrompt;
  const interactive = isInteractive();
  const workingOn = parseList(options.workingOn);
  ensureNonEmpty("Working-on summary", workingOn);
  const nextProvided = options.next !== void 0;
  const blockedProvided = options.blocked !== void 0;
  let nextSteps = parseList(options.next);
  let blocked = parseList(options.blocked);
  if (!nextProvided) {
    nextSteps = await promptForList("Next steps", prompt, interactive);
  }
  if (!blockedProvided) {
    blocked = await promptForList("Blocked items", prompt, interactive);
  }
  const decisions = parseList(options.decisions);
  const questions = parseList(options.questions);
  const vault = new ClawVault(path.resolve(options.vaultPath));
  await vault.load();
  const handoffInput = {
    workingOn,
    blocked,
    nextSteps,
    decisions: decisions.length > 0 ? decisions : void 0,
    openQuestions: questions.length > 0 ? questions : void 0,
    feeling: options.feeling,
    sessionKey: options.sessionKey
  };
  const document = await vault.createHandoff(handoffInput);
  const handoff = {
    ...handoffInput,
    created: document.modified.toISOString()
  };
  await clearDirtyFlag(vault.getPath());
  if (options.index) {
    qmdUpdate(vault.getQmdCollection());
  }
  const git = await maybeCommitDirtyRepo({
    enabled: options.git !== false,
    prompt,
    cwd: options.cwd ?? process.cwd(),
    interactive
  });
  return { handoff, document, git };
}
export {
  sleep
};
