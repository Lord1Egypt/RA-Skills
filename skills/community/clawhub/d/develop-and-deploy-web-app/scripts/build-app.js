"use strict";

const { spawnSync } = require("child_process");
const path = require("path");
const { appRoot, assertRegisteredOwnership, assertSafeUserName, assertSafeToken, parseArgs } = require("./common");

function npmCommandArgs(command) {
  if (process.platform === "win32") {
    return {
      file: "cmd.exe",
      args: ["/d", "/s", "/c", `npm ${command}`],
    };
  }
  return {
    file: "npm",
    args: command.split(" "),
  };
}

function main() {
  const args = parseArgs(process.argv);
  const userName = args.userName;
  const token = args.token;

  assertSafeUserName(userName);
  assertSafeToken(token);
  assertRegisteredOwnership(userName, token);

  const cwd = appRoot(userName, token);
  const npmCall = npmCommandArgs("run build");
  const result = spawnSync(npmCall.file, npmCall.args, {
    cwd,
    encoding: "utf8",
    stdio: "inherit",
    maxBuffer: 10 * 1024 * 1024,
  });

  if (result.error) {
    throw result.error;
  }
  if (result.status !== 0) {
    throw new Error("npm run build failed");
  }

  process.stdout.write(
    `${JSON.stringify(
      {
        userName,
        token,
        cwd: path.relative(process.cwd(), cwd).replaceAll("\\", "/"),
        built: true,
      },
      null,
      2
    )}\n`
  );
}

main();
