import { spawnSync } from "node:child_process";
import { existsSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const bridgeDir = dirname(fileURLToPath(import.meta.url));
const repoRoot = resolve(bridgeDir, "..");
const extensionDir = join(repoRoot, "apps", "chrome-executor-extension");

function main() {
  console.log("[bookmark-setup] ClawHub skill root:", repoRoot);
  console.log("[bookmark-setup] ClawHub/OpenClaw already installed this skill; no OpenClaw config will be modified.");

  if (!existsSync(join(repoRoot, "node_modules"))) {
    run("npm", ["install", "--omit=dev"], repoRoot);
  } else {
    console.log("[bookmark-setup] dependencies already installed.");
  }

  openChromeExtensions();
  console.log("\n[bookmark-setup] One manual browser step is required:");
  console.log("1. Enable Developer Mode on chrome://extensions");
  console.log("2. Click Load unpacked");
  console.log("3. Select this bundled Chrome executor extension folder:");
  console.log(extensionDir);
  console.log("\n[bookmark-setup] After loading the extension, reply to OpenClaw with: 好了");
  console.log("[bookmark-setup] For terminal verification, run: npm run bridge:preflight && npm run bridge:smoke");
}

function run(command, args, cwd = repoRoot) {
  const result = spawnSync(command, args, {
    cwd,
    stdio: "inherit"
  });
  if (result.status !== 0) {
    process.exit(result.status ?? 1);
  }
}

function openChromeExtensions() {
  const script = `
    tell application "Google Chrome"
      activate
      open location "chrome://extensions/"
    end tell
  `;

  const result = spawnSync("osascript", ["-e", script], {
    stdio: "ignore"
  });

  if (result.status === 0) {
    console.log("[bookmark-setup] opened chrome://extensions/ in Google Chrome.");
    return;
  }

  console.log("[bookmark-setup] could not open Chrome automatically. Open chrome://extensions/ manually.");
}

main();
