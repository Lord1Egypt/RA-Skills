"use strict";

const { spawnSync } = require("child_process");
const {
  assertSafeUserName,
  assertSafeToken,
  extractLastJsonObject,
  parseArgs,
  repoRoot,
} = require("./common");

function runNodeScript(scriptName, args) {
  const result = spawnSync(process.execPath, [scriptName, ...args], {
    cwd: repoRoot(),
    encoding: "utf8",
  });
  if (result.status !== 0) {
    throw new Error(
      `Script failed: ${scriptName}\n${result.stderr || result.stdout || "Unknown error"}`
    );
  }
  return extractLastJsonObject(result.stdout);
}

function main() {
  const args = parseArgs(process.argv);
  const userName = args.userName;
  const token = args.token;

  assertSafeUserName(userName);
  assertSafeToken(token);

  if (!args.skipBuild) {
    runNodeScript("scripts/install-app.js", [
      "--userName",
      userName,
      "--token",
      token,
    ]);
    runNodeScript("scripts/build-app.js", [
      "--userName",
      userName,
      "--token",
      token,
    ]);
  }

  const started = runNodeScript("scripts/start-app.js", [
    "--userName",
    userName,
    "--token",
    token,
  ]);

  const synced = runNodeScript("scripts/sync-docs.js", [
    "--userName",
    userName,
    "--token",
    token,
    "--status",
    started.ready ? "running" : "starting",
    "--port",
    String(started.port),
    "--internalPort",
    String(started.internalPort),
    "--url",
    started.url,
  ]);

  const registry = runNodeScript("scripts/update-registry.js", [
    "--userName",
    userName,
    "--token",
    token,
  ]);

  process.stdout.write(
    `${JSON.stringify(
      {
        started,
        synced,
        registry,
        built: !args.skipBuild,
      },
      null,
      2
    )}\n`
  );
}

main();
