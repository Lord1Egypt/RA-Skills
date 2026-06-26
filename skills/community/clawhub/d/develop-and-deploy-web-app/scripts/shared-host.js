"use strict";

const http = require("http");
const {
  SHARED_HOST_HEALTH_PATH,
  SHARED_PUBLIC_PORT,
  appReachable,
  assertSafeToken,
  readWorkspaceRegistry,
} = require("./common");

function flattenApps(registry) {
  const users = Array.isArray(registry && registry.users) ? registry.users : [];
  const apps = [];

  for (const user of users) {
    const userName = user && user.userName;
    for (const app of Array.isArray(user && user.apps) ? user.apps : []) {
      if (!app || !userName) {
        continue;
      }
      apps.push({
        userName,
        token: app.token,
        internalPort: Number.isInteger(app.internalPort) ? app.internalPort : null,
        status: app.status || "unknown",
      });
    }
  }

  return apps;
}

async function resolveTarget(token) {
  assertSafeToken(token);
  const registry = readWorkspaceRegistry();
  const entry = flattenApps(registry).find((app) => app.token === token);
  if (!entry || !Number.isInteger(entry.internalPort)) {
    return null;
  }

  const health = await appReachable(entry.internalPort, entry.userName, token);
  if (!health.ok || !health.matched) {
    return null;
  }

  return {
    userName: entry.userName,
    token,
    internalPort: entry.internalPort,
  };
}

function proxyRequest(targetPort, req, res) {
  const upstream = http.request(
    {
      hostname: "127.0.0.1",
      port: targetPort,
      method: req.method,
      path: req.url,
      headers: {
        ...req.headers,
        host: `127.0.0.1:${targetPort}`,
      },
    },
    (upstreamRes) => {
      res.writeHead(upstreamRes.statusCode || 502, upstreamRes.headers);
      upstreamRes.pipe(res);
    }
  );

  upstream.on("error", (error) => {
    res.statusCode = 502;
    res.setHeader("Content-Type", "application/json; charset=utf-8");
    res.end(
      JSON.stringify({
        ok: false,
        error: "upstream-error",
        message: error.message,
      })
    );
  });

  req.pipe(upstream);
}

const server = http.createServer(async (req, res) => {
  if (req.url === SHARED_HOST_HEALTH_PATH) {
    res.setHeader("Content-Type", "application/json; charset=utf-8");
    res.end(JSON.stringify({ ok: true, port: SHARED_PUBLIC_PORT }));
    return;
  }

  const match = /^\/([A-Z0-9]{8})(\/.*|$)/.exec(req.url || "");
  if (!match) {
    res.statusCode = 404;
    res.setHeader("Content-Type", "application/json; charset=utf-8");
    res.end(JSON.stringify({ ok: false, error: "unknown-token-path" }));
    return;
  }

  const token = match[1];
  let target = null;
  try {
    target = await resolveTarget(token);
  } catch (error) {
    res.statusCode = 500;
    res.setHeader("Content-Type", "application/json; charset=utf-8");
    res.end(JSON.stringify({ ok: false, error: "target-resolution-failed", message: error.message }));
    return;
  }

  if (!target) {
    res.statusCode = 503;
    res.setHeader("Content-Type", "application/json; charset=utf-8");
    res.end(JSON.stringify({ ok: false, error: "app-not-ready", token }));
    return;
  }

  proxyRequest(target.internalPort, req, res);
});

server.listen(SHARED_PUBLIC_PORT, "0.0.0.0");
