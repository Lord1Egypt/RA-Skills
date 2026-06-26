"use strict";

const fs = require("fs");
const { spawnSync } = require("child_process");
const {
  SHARED_PUBLIC_PORT,
  appReachable,
  appMetaPath,
  assertRegisteredOwnership,
  assertSafeUserName,
  assertSafeToken,
  hostUrl,
  isoNow,
  localUrl,
  parseArgs,
  processAlive,
  readPidRecord,
  readJsonIfExists,
  removePidRecord,
  resolveInternalPort,
  request,
  syncWorkspaceRegistryEntry,
  writeJson,
} = require("./common");

function stopPid(pid) {
  if (!Number.isInteger(pid)) {
    return false;
  }

  try {
    process.kill(pid, "SIGTERM");
    return true;
  } catch (error) {
    if (process.platform === "win32") {
      const result = spawnSync("taskkill", ["/PID", String(pid), "/T", "/F"], {
        stdio: "ignore",
      });
      return result.status === 0;
    }
    return false;
  }
}

function wait(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function waitForShutdown(port, userName, token, attempts = 20) {
  for (let i = 0; i < attempts; i += 1) {
    // eslint-disable-next-line no-await-in-loop
    const reachable = await appReachable(port, userName, token);
    if (!reachable.matched) {
      return { ok: false, statusCode: reachable.statusCode || 0, matched: false };
    }
    // eslint-disable-next-line no-await-in-loop
    await wait(250);
  }
  return appReachable(port, userName, token);
}

async function requestGracefulShutdown(port, token) {
  if (!Number.isInteger(port)) {
    return false;
  }
  const response = await request(`${localUrl(port, token)}shutdown`);
  return response.ok && response.statusCode === 200;
}

async function main() {
  const args = parseArgs(process.argv);
  const userName = args.userName;
  const token = args.token;

  assertSafeUserName(userName);
  assertSafeToken(token);
  assertRegisteredOwnership(userName, token);

  const pidRecord = readPidRecord(userName, token);
  const meta = readJsonIfExists(appMetaPath(userName, token), null);
  const pid =
    pidRecord &&
    Number.isInteger(pidRecord.pid)
      ? pidRecord.pid
      : null;
  const internalPort = resolveInternalPort(meta, pidRecord);
  const publicPort =
    pidRecord && Number.isInteger(pidRecord.port)
      ? pidRecord.port
      : meta && Number.isInteger(meta.port)
        ? meta.port
        : internalPort
          ? SHARED_PUBLIC_PORT
          : null;

  if (!pidRecord && !meta) {
    process.stdout.write(`${JSON.stringify({ stopped: false, reason: "missing-pid-file" }, null, 2)}\n`);
    return;
  }

  const aliveBefore = processAlive(pid);
  const gracefulStopIssued =
    internalPort && (aliveBefore || !pid)
      ? await requestGracefulShutdown(internalPort, token)
      : false;
  const stoppedBySignal = aliveBefore ? stopPid(pid) : false;
  removePidRecord(userName, token);

  const reachableAfter =
    internalPort && (aliveBefore || stopped)
      ? await waitForShutdown(internalPort, userName, token)
      : internalPort
        ? await appReachable(internalPort, userName, token)
        : { ok: false, statusCode: 0 };
  const stopped = Boolean(gracefulStopIssued || stoppedBySignal || !reachableAfter.matched);
  if (meta) {
    const next = {
      ...meta,
      port: publicPort || meta.port || null,
      internalPort: internalPort || meta.internalPort || null,
      url: publicPort ? hostUrl(publicPort, token) : meta.url,
      status: reachableAfter.ok ? "unknown" : "stopped",
      updatedAt: isoNow(),
    };
    writeJson(appMetaPath(userName, token), next);
    syncWorkspaceRegistryEntry(next);
  }

  process.stdout.write(
    `${JSON.stringify(
      {
        stopped,
        pid,
        aliveBefore,
        port: publicPort,
        internalPort,
        reachableAfter: reachableAfter.ok,
        matchedAfter: reachableAfter.matched,
      },
      null,
      2
    )}\n`
  );
}

main();
