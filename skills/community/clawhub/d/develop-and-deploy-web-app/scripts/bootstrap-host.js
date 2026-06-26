"use strict";

const path = require("path");
const { repoRoot } = require("./common");

function main() {
  const command =
    process.platform === "win32"
      ? `node "${path.join(repoRoot(), "scripts", "restore-apps.js")}" --skipBuild`
      : `node "${path.join(repoRoot(), "scripts", "restore-apps.js")}" --skipBuild`;

  process.stdout.write(
    `${JSON.stringify(
      {
        purpose: "Host-level startup command",
        command,
        note: "Run this from the machine startup mechanism or process supervisor. The skill does not register startup hooks automatically.",
      },
      null,
      2
    )}\n`
  );
}

main();
