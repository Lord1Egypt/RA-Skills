"use strict";

const { spawnSync } = require("child_process");
const {
  assertRegisteredOwnership,
  assertSafeUserName,
  assertSafeToken,
  extractLastJsonObject,
  parseArgs,
  repoRoot,
} = require("./common");

function run(scriptName, args, allowFailure = false) {
  const result = spawnSync(process.execPath, [scriptName, ...args], {
    cwd: repoRoot(),
    encoding: "utf8",
  });
  if (!allowFailure && result.status !== 0) {
    throw new Error(result.stderr || result.stdout || `Script failed: ${scriptName}`);
  }
  return result.stdout
    ? extractLastJsonObject(result.stdout)
    : { ok: result.status === 0 };
}

function main() {
  const args = parseArgs(process.argv);
  const userName = args.userName;
  const token = args.token;

  assertSafeUserName(userName);
  assertSafeToken(token);
  assertRegisteredOwnership(userName, token);

  const stopped = run(
    "scripts/stop-app.js",
    ["--userName", userName, "--token", token],
    true
  );
  if (stopped && stopped.reachableAfter) {
    throw new Error(
      `Refusing to restart while the previous instance is still reachable on port ${stopped.port}`
    );
  }
  const deployArgs = ["--userName", userName, "--token", token];
  if (args.skipBuild) {
    deployArgs.push("--skipBuild");
  }
  const deployed = run("scripts/deploy-app.js", deployArgs);

  process.stdout.write(`${JSON.stringify({ stopped, deployed }, null, 2)}\n`);
}

main();
