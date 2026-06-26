"use strict";

const fs = require("fs");
const path = require("path");
const { spawn } = require("child_process");
const {
  SHARED_PUBLIC_PORT,
  appReachable,
  appMetaPath,
  appRoot,
  assertRegisteredOwnership,
  assertSafeUserName,
  assertSafeToken,
  ensureDir,
  findFreePort,
  hostUrl,
  isPortFree,
  localUrl,
  logFilePath,
  parseArgs,
  processAlive,
  readPidRecord,
  readJsonIfExists,
  readSharedHostPidRecord,
  removePidRecord,
  removeSharedHostPidRecord,
  request,
  resolveInternalPort,
  runtimeDir,
  sharedHostHealthUrl,
  sharedHostLogFilePath,
  sharedHostRuntimeDir,
  syncPlatformRegistryEntry,
  syncWorkspaceRegistryEntry,
  writeJson,
  writePidRecord,
  writeSharedHostPidRecord,
} = require("./common");

function wait(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function tokenizeCommand(command) {
  const tokens = [];
  const source = String(command || "").trim();
  let current = "";
  let quote = null;

  for (let i = 0; i < source.length; i += 1) {
    const char = source[i];
    if (quote) {
      if (char === quote) {
        quote = null;
      } else {
        current += char;
      }
      continue;
    }
    if (char === '"' || char === "'") {
      quote = char;
      continue;
    }
    if (/\s/.test(char)) {
      if (current) {
        tokens.push(current);
        current = "";
      }
      continue;
    }
    current += char;
  }

  if (current) {
    tokens.push(current);
  }
  return tokens;
}

function resolveStartCommand(serverDir, packageJsonPath) {
  const packageJson = JSON.parse(fs.readFileSync(packageJsonPath, "utf8"));
  const startScript =
    packageJson &&
    packageJson.scripts &&
    typeof packageJson.scripts.start === "string"
      ? packageJson.scripts.start.trim()
      : "";

  const tokens = tokenizeCommand(startScript);
  if (tokens[0] === "node" && tokens.length >= 2) {
    return {
      file: process.execPath,
      args: tokens.slice(1),
      cwd: serverDir,
    };
  }

  if (process.platform === "win32") {
    return {
      file: "cmd.exe",
      args: ["/d", "/s", "/c", "npm run start"],
      cwd: serverDir,
    };
  }

  return {
    file: "npm",
    args: ["run", "start"],
    cwd: serverDir,
  };
}

async function waitForReady(port, userName, token, attempts = 20) {
  for (let i = 0; i < attempts; i += 1) {
    // eslint-disable-next-line no-await-in-loop
    const response = await appReachable(port, userName, token);
    if (response.ok && response.matched) {
      return true;
    }
    // eslint-disable-next-line no-await-in-loop
    await wait(500);
  }
  return false;
}

async function waitForSharedHost(attempts = 20) {
  for (let i = 0; i < attempts; i += 1) {
    // eslint-disable-next-line no-await-in-loop
    const response = await request(sharedHostHealthUrl());
    if (response.ok && response.statusCode === 200) {
      return true;
    }
    // eslint-disable-next-line no-await-in-loop
    await wait(250);
  }
  return false;
}

async function ensureSharedHost() {
  const pidRecord = readSharedHostPidRecord();
  const hostFree = await isPortFree(SHARED_PUBLIC_PORT);

  if (pidRecord && Number.isInteger(pidRecord.pid) && processAlive(pidRecord.pid)) {
    const ready = await waitForSharedHost();
    if (ready) {
      return { reused: true, pid: pidRecord.pid };
    }
    throw new Error(
      `Shared host pid ${pidRecord.pid} is alive but did not become healthy on port ${SHARED_PUBLIC_PORT}`
    );
  }

  if (pidRecord && (!Number.isInteger(pidRecord.pid) || !processAlive(pidRecord.pid))) {
    removeSharedHostPidRecord();
  }

  if (!hostFree) {
    const ready = await waitForSharedHost();
    if (ready) {
      return { reused: true, pid: pidRecord && Number.isInteger(pidRecord.pid) ? pidRecord.pid : null };
    }
    throw new Error(`Expected shared port ${SHARED_PUBLIC_PORT} to be reserved for the LiteApp host, but it is occupied`);
  }

  ensureDir(sharedHostRuntimeDir());
  const logFd = fs.openSync(sharedHostLogFilePath(), "a");
  const child = spawn(process.execPath, [path.join(__dirname, "shared-host.js")], {
    cwd: path.resolve(__dirname, ".."),
    detached: true,
    stdio: ["ignore", logFd, logFd],
    env: {
      ...process.env,
    },
  });

  child.unref();
  fs.closeSync(logFd);
  writeSharedHostPidRecord({
    pid: child.pid,
    port: SHARED_PUBLIC_PORT,
    startedAt: new Date().toISOString(),
  });

  const ready = await waitForSharedHost();
  if (!ready) {
    removeSharedHostPidRecord();
    throw new Error(`Shared LiteApp host failed to become ready on port ${SHARED_PUBLIC_PORT}`);
  }

  return { reused: false, pid: child.pid };
}

async function main() {
  const args = parseArgs(process.argv);
  const userName = args.userName;
  const token = args.token;

  assertSafeUserName(userName);
  assertSafeToken(token);
  assertRegisteredOwnership(userName, token);

  const metaFile = appMetaPath(userName, token);
  const meta = readJsonIfExists(metaFile, null);
  if (!meta) {
    throw new Error(`Missing APP-META.json: ${metaFile}`);
  }

  const appDir = appRoot(userName, token);
  const serverDir = path.join(appDir, "server");
  const packageJson = path.join(serverDir, "package.json");
  if (!fs.existsSync(packageJson)) {
    throw new Error(`Expected server package.json at ${packageJson}`);
  }

  await ensureSharedHost();
  ensureDir(runtimeDir(userName, token));

  const pidRecord = readPidRecord(userName, token);
  const knownPid = pidRecord && Number.isInteger(pidRecord.pid) ? pidRecord.pid : null;
  const preferredPort = resolveInternalPort(meta, pidRecord);

  if (knownPid && processAlive(knownPid) && preferredPort) {
    const health = await appReachable(preferredPort, userName, token);
    if (health.ok && health.matched) {
      const next = {
        ...meta,
        port: SHARED_PUBLIC_PORT,
        internalPort: preferredPort,
        url: hostUrl(SHARED_PUBLIC_PORT, token),
        status: "running",
        updatedAt: new Date().toISOString(),
      };
      writeJson(metaFile, next);
      syncWorkspaceRegistryEntry(next);
      syncPlatformRegistryEntry(next);
      process.stdout.write(
        `${JSON.stringify(
          {
            pid: knownPid,
            port: SHARED_PUBLIC_PORT,
            internalPort: preferredPort,
            url: next.url,
            readinessUrl: localUrl(SHARED_PUBLIC_PORT, token),
            ready: true,
            reused: true,
            logPath: logFilePath(userName, token),
          },
          null,
          2
        )}\n`
      );
      return;
    }
    throw new Error(
      `Refusing to start a second instance: tracked pid ${knownPid} is still alive but app health is not clean on internal port ${preferredPort}`
    );
  }

  if (knownPid && !processAlive(knownPid)) {
    removePidRecord(userName, token);
  }

  let internalPort = preferredPort;
  if (internalPort) {
    const reachable = await appReachable(internalPort, userName, token);
    if (reachable.ok && reachable.matched) {
      throw new Error(
        `Refusing to start a second instance: app is already reachable on internal port ${internalPort} but no live tracked pid can be safely reused`
      );
    }
    const portFree = await isPortFree(internalPort);
    if (!portFree) {
      throw new Error(`Expected to reuse internal port ${internalPort}, but it is occupied`);
    }
  } else {
    internalPort = await findFreePort();
  }

  const basePath = `/${token}`;
  const publicUrl = hostUrl(SHARED_PUBLIC_PORT, token);
  const readinessUrl = localUrl(SHARED_PUBLIC_PORT, token);

  const logPath = logFilePath(userName, token);
  const logFd = fs.openSync(logPath, "a");
  const command = resolveStartCommand(serverDir, packageJson);
  const child = spawn(command.file, command.args, {
    cwd: command.cwd,
    detached: true,
    stdio: ["ignore", logFd, logFd],
    env: {
      ...process.env,
      PORT: String(internalPort),
      USER_NAME: userName,
      SESSION_ID: userName,
      APP_TOKEN: token,
      BASE_PATH: basePath,
    },
  });

  child.unref();
  fs.closeSync(logFd);

  writePidRecord(userName, token, {
    pid: child.pid,
    port: SHARED_PUBLIC_PORT,
    internalPort,
    startedAt: new Date().toISOString(),
  });

  const ready = await waitForReady(internalPort, userName, token);
  const next = {
    ...meta,
    port: SHARED_PUBLIC_PORT,
    internalPort,
    url: publicUrl,
    status: ready ? "running" : "starting",
    updatedAt: new Date().toISOString(),
  };
  writeJson(metaFile, next);
  syncWorkspaceRegistryEntry(next);
  syncPlatformRegistryEntry(next);

  process.stdout.write(
    `${JSON.stringify(
      {
        pid: child.pid,
        port: SHARED_PUBLIC_PORT,
        internalPort,
        url: publicUrl,
        readinessUrl,
        ready,
        reused: false,
        logPath,
      },
      null,
      2
    )}\n`
  );
}

main();
