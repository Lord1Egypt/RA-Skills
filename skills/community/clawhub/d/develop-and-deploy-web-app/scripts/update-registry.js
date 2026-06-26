"use strict";

const {
  assertRegisteredOwnership,
  appMetaPath,
  assertSafeUserName,
  assertSafeToken,
  ensureDir,
  parseArgs,
  readJsonIfExists,
  registryRoot,
  syncPlatformRegistryEntry,
  syncWorkspaceRegistryEntry,
  webAppsRoot,
  registryPath,
} = require("./common");

function main() {
  const args = parseArgs(process.argv);
  const userName = args.userName;
  const token = args.token;

  assertSafeUserName(userName);
  assertSafeToken(token);
  assertRegisteredOwnership(userName, token);

  const meta = readJsonIfExists(appMetaPath(userName, token), null);
  if (!meta) {
    throw new Error("Cannot update registry without APP-META.json");
  }

  ensureDir(webAppsRoot());
  ensureDir(registryRoot());

  syncWorkspaceRegistryEntry(meta);
  syncPlatformRegistryEntry(meta);

  process.stdout.write(
    `${JSON.stringify({ userName, token, registry: registryPath() }, null, 2)}\n`
  );
}

main();
