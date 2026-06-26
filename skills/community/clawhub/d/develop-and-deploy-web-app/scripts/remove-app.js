"use strict";

const fs = require("fs");
const { spawnSync } = require("child_process");
const {
  appMetaPath,
  appRoot,
  assertRegisteredOwnership,
  assertSafeUserName,
  assertSafeToken,
  parseArgs,
  readJsonIfExists,
  removePlatformRegistryEntry,
  removeWorkspaceRegistryEntry,
  userRoot,
} = require("./common");

function runStop(userName, token) {
  return spawnSync(
    process.execPath,
    ["scripts/stop-app.js", "--userName", userName, "--token", token],
    {
      cwd: process.cwd(),
      encoding: "utf8",
    }
  );
}

function main() {
  const args = parseArgs(process.argv);
  const userName = args.userName;
  const token = args.token;

  assertSafeUserName(userName);
  assertSafeToken(token);
  assertRegisteredOwnership(userName, token);

  const meta = readJsonIfExists(appMetaPath(userName, token), null);
  const appDir = appRoot(userName, token);
  const existed = fs.existsSync(appDir);

  runStop(userName, token);
  const workspaceRegistryRemoved = removeWorkspaceRegistryEntry(userName, token);
  const platformRegistryRemoved = removePlatformRegistryEntry(userName, token);
  fs.rmSync(appDir, { recursive: true, force: true });

  if (fs.existsSync(userRoot(userName))) {
    const remaining = fs.readdirSync(userRoot(userName), { withFileTypes: true });
    if (remaining.length === 0) {
      fs.rmSync(userRoot(userName), { recursive: true, force: true });
    }
  }

  process.stdout.write(
    `${JSON.stringify(
      {
        userName,
        token,
        name: meta ? meta.title : null,
        existed,
        removed: existed || workspaceRegistryRemoved || platformRegistryRemoved.removed,
        workspaceRegistryRemoved,
        platformRegistryRemoved: platformRegistryRemoved.removed,
      },
      null,
      2
    )}\n`
  );
}

main();
