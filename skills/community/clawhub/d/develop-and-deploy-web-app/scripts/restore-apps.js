"use strict";

const { spawnSync } = require("child_process");
const {
  extractLastJsonObject,
  parseArgs,
  readWorkspaceRegistry,
  repoRoot,
} = require("./common");

function runNodeScript(scriptName, args) {
  const result = spawnSync(process.execPath, [scriptName, ...args], {
    cwd: repoRoot(),
    encoding: "utf8",
  });
  if (result.status !== 0) {
    return {
      ok: false,
      scriptName,
      error: result.stderr || result.stdout || "Unknown error",
    };
  }
  return {
    ok: true,
    scriptName,
    data: extractLastJsonObject(result.stdout),
  };
}

function flattenApps(registry, onlyUserName) {
  const users = Array.isArray(registry.users) ? registry.users : [];
  const apps = [];
  for (const user of users) {
    if (onlyUserName && user.userName !== onlyUserName) {
      continue;
    }
    for (const app of Array.isArray(user.apps) ? user.apps : []) {
      apps.push({
        userName: user.userName,
        token: app.token,
        autoStart: app.autoStart !== false,
      });
    }
  }
  return apps;
}

function main() {
  const args = parseArgs(process.argv);
  const onlyUserName = args.userName || null;
  const skipBuild = args.skipBuild ? true : false;
  const registry = readWorkspaceRegistry();
  const apps = flattenApps(registry, onlyUserName).filter((app) => app.autoStart);

  const results = [];
  for (const app of apps) {
    const deployArgs = ["--userName", app.userName, "--token", app.token];
    if (skipBuild) {
      deployArgs.push("--skipBuild");
    }
    results.push(
      runNodeScript("scripts/deploy-app.js", deployArgs)
    );
  }

  process.stdout.write(
    `${JSON.stringify(
      {
        restored: results.filter((item) => item.ok).length,
        attempted: apps.length,
        results,
      },
      null,
      2
    )}\n`
  );
}

main();
