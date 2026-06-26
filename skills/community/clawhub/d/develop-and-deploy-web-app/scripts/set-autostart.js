"use strict";

const {
  appMetaPath,
  assertRegisteredOwnership,
  assertSafeUserName,
  assertSafeToken,
  isoNow,
  parseArgs,
  readJsonIfExists,
  syncWorkspaceRegistryEntry,
  writeJson,
} = require("./common");

function main() {
  const args = parseArgs(process.argv);
  const userName = args.userName;
  const token = args.token;

  assertSafeUserName(userName);
  assertSafeToken(token);
  assertRegisteredOwnership(userName, token);

  const metaPath = appMetaPath(userName, token);
  const meta = readJsonIfExists(metaPath, null);
  if (!meta) {
    throw new Error("Missing APP-META.json");
  }

  const autoStart = args.enabled === "false" ? false : true;
  const next = {
    ...meta,
    autoStart,
    updatedAt: isoNow(),
  };
  writeJson(metaPath, next);
  syncWorkspaceRegistryEntry(next);
  process.stdout.write(`${JSON.stringify(next, null, 2)}\n`);
}

main();
