"use strict";

const fs = require("fs");
const path = require("path");
const net = require("net");
const http = require("http");

const SHARED_PUBLIC_PORT = 33333;
const MIN_PORT = 33334;
const MAX_PORT = 39999;
const TOKEN_LENGTH = 8;
const SHARED_HOST_HEALTH_PATH = "/__shared_host/health";

function assertSafeUserName(userName) {
  if (!userName || !/^[A-Za-z0-9_-]+$/.test(userName)) {
    throw new Error("userName must match /^[A-Za-z0-9_-]+$/");
  }
}

function assertSafeToken(token) {
  if (!token || !/^[A-Z0-9]{8}$/.test(token)) {
    throw new Error("token must match /^[A-Z0-9]{8}$/");
  }
}

function generateToken() {
  const alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
  let token = "";
  for (let i = 0; i < TOKEN_LENGTH; i += 1) {
    token += alphabet[Math.floor(Math.random() * alphabet.length)];
  }
  return token;
}

function repoRoot() {
  return path.resolve(__dirname, "..");
}

function webAppsRoot() {
  return path.join(repoRoot(), "workspaces", "web-apps");
}

function userRoot(userName) {
  assertSafeUserName(userName);
  return path.join(webAppsRoot(), userName);
}

function appRoot(userName, token) {
  assertSafeUserName(userName);
  assertSafeToken(token);
  return path.join(userRoot(userName), token);
}

function findAppByToken(token) {
  assertSafeToken(token);
  const registry = readWorkspaceRegistry();
  for (const user of registry.users) {
    for (const app of user.apps) {
      if (app && app.token === token) {
        return app;
      }
    }
  }
  return null;
}

function registryRoot() {
  return path.join(webAppsRoot(), "users");
}

function registryPath() {
  return path.join(webAppsRoot(), "registry.json");
}

function envPath(name) {
  const value = process.env[name];
  return typeof value === "string" && value.trim() ? value.trim() : null;
}

function openclawRootFromEnv() {
  const configuredRoot =
    envPath("OPENCLAW_ROOT") ||
    envPath("OPENCLAW_HOME") ||
    envPath("OPENCLAW_DIR");

  if (!configuredRoot) {
    return null;
  }

  return path.resolve(configuredRoot);
}

function defaultOpenclawRoot() {
  const homeDir = envPath("HOME") || envPath("USERPROFILE");
  if (!homeDir) {
    return null;
  }
  return path.join(path.resolve(homeDir), ".openclaw");
}

function findOpenclawRoot(startDir = repoRoot()) {
  const configuredRoot = openclawRootFromEnv();
  if (configuredRoot) {
    return configuredRoot;
  }

  let currentDir = path.resolve(startDir);
  while (true) {
    const candidate = path.join(currentDir, ".openclaw");
    if (fs.existsSync(candidate) && fs.statSync(candidate).isDirectory()) {
      return candidate;
    }

    const parentDir = path.dirname(currentDir);
    if (parentDir === currentDir) {
      break;
    }
    currentDir = parentDir;
  }

  return defaultOpenclawRoot();
}

function platformDataDir() {
  const openclawRoot = findOpenclawRoot();
  if (!openclawRoot) {
    throw new Error(
      "Cannot resolve .openclaw root. Set OPENCLAW_ROOT or create a .openclaw directory in an ancestor path."
    );
  }
  return path.join(path.dirname(openclawRoot), "platform_data");
}

function platformRegistryPath() {
  return path.join(platformDataDir(), "web-app-registry.json");
}

function sharedHostRuntimeDir() {
  return path.join(webAppsRoot(), ".shared-runtime");
}

function sharedHostPidFilePath() {
  return path.join(sharedHostRuntimeDir(), "shared-host.pid");
}

function sharedHostLogFilePath() {
  return path.join(sharedHostRuntimeDir(), "shared-host.log");
}

function userIndexPath(userName) {
  assertSafeUserName(userName);
  return path.join(registryRoot(), `${userName}.json`);
}

function appMetaPath(userName, token) {
  return path.join(appRoot(userName, token), "APP-META.json");
}

function appNotesPath(userName, token) {
  return path.join(appRoot(userName, token), "APP-NOTES.md");
}

function runtimeDir(userName, token) {
  return path.join(appRoot(userName, token), ".runtime");
}

function pidFilePath(userName, token) {
  return path.join(runtimeDir(userName, token), "server.pid");
}

function logFilePath(userName, token) {
  return path.join(runtimeDir(userName, token), "server.log");
}

function ensureDir(dir) {
  fs.mkdirSync(dir, { recursive: true });
}

function readJsonIfExists(filePath, fallback) {
  if (!fs.existsSync(filePath)) {
    return fallback;
  }
  return JSON.parse(fs.readFileSync(filePath, "utf8"));
}

function writeJson(filePath, data) {
  ensureDir(path.dirname(filePath));
  fs.writeFileSync(filePath, `${JSON.stringify(data, null, 2)}\n`, "utf8");
}

function readSharedHostPidRecord() {
  const pidFile = sharedHostPidFilePath();
  if (!fs.existsSync(pidFile)) {
    return null;
  }
  const raw = fs.readFileSync(pidFile, "utf8").trim();
  if (!raw) {
    return null;
  }
  const parsed = raw.startsWith("{") ? JSON.parse(raw) : { pid: Number(raw) };
  return parsed && Number.isInteger(parsed.pid) ? parsed : null;
}

function writeSharedHostPidRecord(record) {
  ensureDir(sharedHostRuntimeDir());
  fs.writeFileSync(
    sharedHostPidFilePath(),
    `${JSON.stringify(record, null, 2)}\n`,
    "utf8"
  );
}

function removeSharedHostPidRecord() {
  fs.rmSync(sharedHostPidFilePath(), { force: true });
}

function toPascalCase(value) {
  const parts = String(value || "")
    .replace(/([a-z0-9])([A-Z])/g, "$1 $2")
    .split(/[^A-Za-z0-9]+/)
    .filter(Boolean);

  if (parts.length === 0) {
    return "";
  }

  return parts
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1).toLowerCase())
    .join("");
}

function deriveAppDescriptors(meta = {}) {
  const explicitKind = toPascalCase(meta.appKind);
  const explicitLabel = toPascalCase(meta.appLabel);
  const inferredKind =
    toPascalCase(meta.title) ||
    toPascalCase(meta.goal) ||
    "WebApp";

  return {
    appKind: explicitKind || inferredKind,
    appLabel: explicitLabel || "WebApp",
  };
}

function resolveInternalPort(meta, pidRecord = null) {
  const pidInternalPort =
    pidRecord && Number.isInteger(pidRecord.internalPort)
      ? pidRecord.internalPort
      : pidRecord &&
          Number.isInteger(pidRecord.port) &&
          pidRecord.port !== SHARED_PUBLIC_PORT
        ? pidRecord.port
        : null;

  const metaInternalPort =
    meta && Number.isInteger(meta.internalPort)
      ? meta.internalPort
      : meta &&
          Number.isInteger(meta.port) &&
          meta.port !== SHARED_PUBLIC_PORT
        ? meta.port
        : null;

  return pidInternalPort || metaInternalPort || null;
}

function normalizeWorkspaceRegistry(registry) {
  const source = registry && typeof registry === "object" ? registry : {};
  const users = Array.isArray(source.users) ? source.users : [];
  return {
    users: users.map((entry) => ({
      userName: entry.userName,
      apps: Array.isArray(entry.apps)
        ? entry.apps.map((app) => ({
          userName: app.userName,
          token: app.token,
          path: app.path,
          port: app.port,
          internalPort: app.internalPort,
          url: app.url,
          title: app.title,
          goal: app.goal,
          status: app.status,
          autoStart: app.autoStart !== false,
          updatedAt: app.updatedAt,
          ...deriveAppDescriptors(app),
        }))
        : [],
    })),
  };
}

function readWorkspaceRegistry() {
  return normalizeWorkspaceRegistry(readJsonIfExists(registryPath(), { users: [] }));
}

function writeWorkspaceRegistry(registry) {
  writeJson(registryPath(), normalizeWorkspaceRegistry(registry));
}

function readUserIndex(userName) {
  const registry = readWorkspaceRegistry();
  const user = Array.isArray(registry.users)
    ? registry.users.find((entry) => entry.userName === userName)
    : null;
  return user
    ? { userName, apps: Array.isArray(user.apps) ? user.apps : [] }
    : { userName, apps: [] };
}

function workspaceAppRecord(meta) {
  return {
    userName: meta.userName,
    token: meta.token,
    path: meta.path,
    port: meta.port,
    internalPort: meta.internalPort,
    url: meta.url,
    title: meta.title,
    goal: meta.goal,
    status: meta.status,
    autoStart: meta.autoStart !== false,
    updatedAt: meta.updatedAt,
    ...deriveAppDescriptors(meta),
  };
}

function syncWorkspaceRegistryEntry(meta) {
  const registry = readWorkspaceRegistry();
  const users = Array.isArray(registry.users) ? [...registry.users] : [];
  const userIdx = users.findIndex((entry) => entry.userName === meta.userName);
  const userRecord =
    userIdx === -1
      ? { userName: meta.userName, apps: [] }
      : {
        ...users[userIdx],
        apps: Array.isArray(users[userIdx].apps) ? [...users[userIdx].apps] : [],
      };

  const record = workspaceAppRecord(meta);
  const appIdx = userRecord.apps.findIndex((item) => item && item.token === meta.token);
  if (appIdx === -1) {
    userRecord.apps.push(record);
  } else {
    userRecord.apps[appIdx] = record;
  }
  userRecord.apps.sort((a, b) => a.token.localeCompare(b.token));

  if (userIdx === -1) {
    users.push(userRecord);
  } else {
    users[userIdx] = userRecord;
  }
  users.sort((a, b) => a.userName.localeCompare(b.userName));

  writeWorkspaceRegistry({ users });
  writeJson(userIndexPath(meta.userName), {
    userName: meta.userName,
    apps: userRecord.apps,
  });
  return record;
}

function removeWorkspaceRegistryEntry(userName, token) {
  const registry = readWorkspaceRegistry();
  const users = Array.isArray(registry.users) ? registry.users : [];
  const nextUsers = [];
  let removed = false;

  for (const user of users) {
    if (!user || user.userName !== userName) {
      nextUsers.push(user);
      continue;
    }

    const apps = Array.isArray(user.apps) ? user.apps : [];
    const nextApps = apps.filter((app) => !(app && app.token === token));
    removed = removed || nextApps.length !== apps.length;

    if (nextApps.length > 0) {
      nextUsers.push({
        ...user,
        apps: nextApps,
      });
    }
  }

  writeWorkspaceRegistry({ users: nextUsers });
  const remainingUser = nextUsers.find((user) => user.userName === userName);
  if (remainingUser) {
    writeJson(userIndexPath(userName), {
      userName,
      apps: remainingUser.apps,
    });
  } else {
    fs.rmSync(userIndexPath(userName), { force: true });
  }

  return removed;
}

function platformRegistryRecord(meta) {
  const descriptors = deriveAppDescriptors(meta);
  return {
    name: meta.title,
    token: meta.token,
    file_path: meta.path,
    port: meta.port,
    created_at: meta.createdAt,
    modified_at: meta.updatedAt,
    user_name: meta.userName,
    app_kind: descriptors.appKind,
    app_label: descriptors.appLabel,
  };
}

function syncPlatformRegistryEntry(meta) {
  const current = readJsonIfExists(platformRegistryPath(), { apps: [] });
  const apps = Array.isArray(current.apps) ? [...current.apps] : [];
  const record = platformRegistryRecord(meta);
  const index = apps.findIndex((item) => item && item.token === meta.token);

  if (index === -1) {
    apps.push(record);
  } else {
    apps[index] = record;
  }

  apps.sort((a, b) => {
    const userCompare = String(a.user_name).localeCompare(String(b.user_name));
    if (userCompare !== 0) {
      return userCompare;
    }
    return String(a.file_path).localeCompare(String(b.file_path));
  });

  writeJson(platformRegistryPath(), { apps });
  return record;
}

function removePlatformRegistryEntry(userName, token) {
  const current = readJsonIfExists(platformRegistryPath(), { apps: [] });
  const apps = Array.isArray(current.apps) ? current.apps : [];
  const nextApps = apps.filter((item) => !(item && item.token === token && item.user_name === userName));
  writeJson(platformRegistryPath(), { apps: nextApps });
  return {
    removed: nextApps.length !== apps.length,
    count: nextApps.length,
  };
}

function readPidRecord(userName, token) {
  const pidFile = pidFilePath(userName, token);
  if (!fs.existsSync(pidFile)) {
    return null;
  }
  const raw = fs.readFileSync(pidFile, "utf8").trim();
  if (!raw) {
    return null;
  }
  const parsed = raw.startsWith("{") ? JSON.parse(raw) : { pid: Number(raw) };
  const parsedUserName = parsed && parsed.userName;
  if (
    parsed &&
    parsedUserName &&
    parsedUserName !== userName
  ) {
    return null;
  }
  if (
    parsed &&
    parsed.token &&
    parsed.token !== token
  ) {
    return null;
  }
  return {
    ...parsed,
    userName: parsedUserName || null,
  };
}

function writePidRecord(userName, token, record) {
  ensureDir(runtimeDir(userName, token));
  fs.writeFileSync(
    pidFilePath(userName, token),
    `${JSON.stringify(
      {
        ...record,
        userName,
        token,
      },
      null,
      2
    )}\n`,
    "utf8"
  );
}

function removePidRecord(userName, token) {
  fs.rmSync(pidFilePath(userName, token), { force: true });
}

function processAlive(pid) {
  if (!Number.isInteger(pid)) {
    return false;
  }
  try {
    process.kill(pid, 0);
    return true;
  } catch (error) {
    return false;
  }
}

function canListen(port, host) {
  return new Promise((resolve) => {
    const server = net.createServer();
    server.unref();
    server.on("error", () => resolve(false));
    server.listen({ port, host, exclusive: true }, () => {
      server.close(() => resolve(true));
    });
  });
}

async function isPortFree(port) {
  const loopbackFree = await canListen(port, "127.0.0.1");
  if (!loopbackFree) {
    return false;
  }
  return canListen(port, "0.0.0.0");
}

async function findFreePort(start = MIN_PORT, end = MAX_PORT) {
  for (let port = start; port <= end; port += 1) {
    // eslint-disable-next-line no-await-in-loop
    if (await isPortFree(port)) {
      return port;
    }
  }
  throw new Error(`No free port found in range ${start}-${end}`);
}

function isoNow() {
  return new Date().toISOString();
}

function hostUrl(port, token) {
  return `http://host:${port}/${token}/`;
}

function localUrl(port, token) {
  return `http://127.0.0.1:${port}/${token}/`;
}

function sharedHostHealthUrl() {
  return `http://127.0.0.1:${SHARED_PUBLIC_PORT}${SHARED_HOST_HEALTH_PATH}`;
}

function request(url) {
  return new Promise((resolve) => {
    const req = http.get(url, (res) => {
      const chunks = [];
      res.on("data", (chunk) => chunks.push(chunk));
      res.on("end", () => {
        resolve({
          ok: true,
          statusCode: res.statusCode || 0,
          body: Buffer.concat(chunks).toString("utf8"),
        });
      });
    });
    req.on("error", () => resolve({ ok: false, statusCode: 0, body: "" }));
    req.setTimeout(3000, () => {
      req.destroy();
      resolve({ ok: false, statusCode: 0, body: "" });
    });
  });
}

async function appReachable(port, userName, token) {
  if (!Number.isInteger(port)) {
    return { ok: false, statusCode: 0, body: "", matched: false };
  }
  const response = await request(`${localUrl(port, token)}api/health`);
  if (!response.ok || response.statusCode !== 200) {
    return { ...response, matched: false };
  }
  try {
    const data = JSON.parse(response.body || "{}");
    const expectedBasePath = `/${token}`;
    const matched =
      data &&
      data.ok === true &&
      data.token === token &&
      (
        data.basePath === undefined ||
        data.basePath === expectedBasePath
      );
    return { ...response, matched };
  } catch (error) {
    return { ...response, matched: false };
  }
}

function parseArgs(argv) {
  const args = {};
  for (let i = 2; i < argv.length; i += 1) {
    const current = argv[i];
    if (!current.startsWith("--")) {
      continue;
    }
    const key = current.slice(2);
    const next = argv[i + 1];
    if (!next || next.startsWith("--")) {
      args[key] = true;
    } else {
      args[key] = next;
      i += 1;
    }
  }
  return args;
}

function findRegisteredApp(userName, token) {
  assertSafeUserName(userName);
  assertSafeToken(token);
  const registry = readWorkspaceRegistry();
  const user = Array.isArray(registry.users)
    ? registry.users.find((entry) => entry.userName === userName)
    : null;
  const app = user && Array.isArray(user.apps)
    ? user.apps.find((item) => item && item.token === token)
    : null;
  return app || null;
}

function assertRegisteredOwnership(userName, token) {
  const app = findRegisteredApp(userName, token);
  if (!app) {
    throw new Error(`App ${token} is not registered under user ${userName}`);
  }
  return app;
}

function extractLastJsonObject(text) {
  const source = String(text || "").trimEnd();
  if (!source) {
    return null;
  }

  let depth = 0;
  let inString = false;
  let escaping = false;
  let end = -1;

  for (let i = source.length - 1; i >= 0; i -= 1) {
    const char = source[i];

    if (inString) {
      if (escaping) {
        escaping = false;
      } else if (char === "\\") {
        escaping = true;
      } else if (char === '"') {
        inString = false;
      }
      continue;
    }

    if (char === '"') {
      inString = true;
      escaping = false;
      continue;
    }

    if (char === "}") {
      if (end === -1) {
        end = i;
      }
      depth += 1;
      continue;
    }

    if (char === "{") {
      depth -= 1;
      if (depth === 0 && end !== -1) {
        return JSON.parse(source.slice(i, end + 1));
      }
    }
  }

  return null;
}

module.exports = {
  SHARED_PUBLIC_PORT,
  SHARED_HOST_HEALTH_PATH,
  MIN_PORT,
  MAX_PORT,
  appMetaPath,
  appNotesPath,
  appRoot,
  assertSafeUserName,
  assertRegisteredOwnership,
  assertSafeToken,
  deriveAppDescriptors,
  ensureDir,
  extractLastJsonObject,
  findRegisteredApp,
  findAppByToken,
  findFreePort,
  findOpenclawRoot,
  generateToken,
  hostUrl,
  isoNow,
  isPortFree,
  localUrl,
  logFilePath,
  parseArgs,
  platformDataDir,
  platformRegistryPath,
  processAlive,
  pidFilePath,
  readPidRecord,
  readSharedHostPidRecord,
  readUserIndex,
  readJsonIfExists,
  readWorkspaceRegistry,
  removePlatformRegistryEntry,
  removePidRecord,
  removeSharedHostPidRecord,
  removeWorkspaceRegistryEntry,
  resolveInternalPort,
  request,
  registryPath,
  registryRoot,
  repoRoot,
  runtimeDir,
  sharedHostHealthUrl,
  sharedHostLogFilePath,
  sharedHostPidFilePath,
  sharedHostRuntimeDir,
  syncWorkspaceRegistryEntry,
  userIndexPath,
  userRoot,
  syncPlatformRegistryEntry,
  appReachable,
  webAppsRoot,
  writeSharedHostPidRecord,
  writeWorkspaceRegistry,
  writePidRecord,
  writeJson,
};
