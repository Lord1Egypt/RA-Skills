import http from "node:http";
import { randomUUID } from "node:crypto";
import { WebSocketServer } from "ws";

const PORT = Number(process.env.BOOKMARK_BRIDGE_PORT || 8787);
const HOST = process.env.BOOKMARK_BRIDGE_HOST || "127.0.0.1";
const EXECUTOR_GRACE_MS = Number(process.env.BOOKMARK_BRIDGE_EXECUTOR_GRACE_MS || 90000);

let executorSocket = null;
let lastExecutorSeenAt = 0;
let lastExecutorHello = null;
const pendingRequests = new Map();

const server = http.createServer(async (req, res) => {
  try {
    if (req.method === "GET" && req.url === "/health") {
      return sendJson(res, 200, buildHealthPayload());
    }

    if (req.method === "POST" && req.url === "/context") {
      return sendJson(res, 200, await forwardToExecutor({
        type: "bridge.context",
        ...(await readJsonBody(req))
      }));
    }

    if (req.method === "POST" && req.url === "/validate") {
      return sendJson(res, 200, await forwardToExecutor({
        type: "bridge.validate",
        ...(await readJsonBody(req))
      }));
    }

    if (req.method === "POST" && req.url === "/apply") {
      return sendJson(res, 200, await forwardToExecutor({
        type: "bridge.apply",
        ...(await readJsonBody(req))
      }));
    }

    if (req.method === "POST" && req.url === "/undo") {
      return sendJson(res, 200, await forwardToExecutor({
        type: "bridge.undo",
        ...(await readJsonBody(req))
      }));
    }

    if (req.method === "POST" && req.url === "/cleanup-test-artifacts") {
      return sendJson(res, 200, await forwardToExecutor({
        type: "bridge.cleanup_test_artifacts",
        ...(await readJsonBody(req))
      }));
    }

    return sendJson(res, 404, {
      error: {
        code: "NOT_FOUND",
        message: "Route not found."
      }
    });
  } catch (error) {
    const message = error?.message || String(error);
    const code = message === "Executor unavailable" ? 503 : 500;
    return sendJson(res, code, {
      error: {
        code: code === 503 ? "EXTENSION_UNAVAILABLE" : "INTERNAL_BRIDGE_ERROR",
        message
      }
    });
  }
});

const wss = new WebSocketServer({
  noServer: true
});

server.on("upgrade", (req, socket, head) => {
  if (req.url !== "/ws") {
    socket.destroy();
    return;
  }

  wss.handleUpgrade(req, socket, head, (ws) => {
    wss.emit("connection", ws, req);
  });
});

wss.on("connection", (ws) => {
  ws.on("message", (raw) => {
    let payload;
    try {
      payload = JSON.parse(String(raw));
    } catch (error) {
      return;
    }

    if (payload?.type === "hello" && payload?.role === "chrome-executor") {
      executorSocket = ws;
      lastExecutorSeenAt = Date.now();
      lastExecutorHello = {
        extensionVersion: payload.extensionVersion || null,
        capabilities: payload.capabilities || null
      };
      ws.send(JSON.stringify({
        type: "hello_ack",
        accepted: true,
        serverTime: Date.now()
      }));
      return;
    }

    if (payload?.type === "heartbeat" && payload?.role === "chrome-executor") {
      executorSocket = ws;
      lastExecutorSeenAt = Date.now();
      return;
    }

    if (payload?.type === "response" && payload?.requestId) {
      lastExecutorSeenAt = Date.now();
      const pending = pendingRequests.get(payload.requestId);
      if (!pending) {
        return;
      }
      pendingRequests.delete(payload.requestId);
      pending.resolve(payload.response);
    }
  });

  ws.on("close", () => {
    if (executorSocket === ws) {
      executorSocket = null;
    }
  });
});

server.listen(PORT, HOST, () => {
  console.log(`[bookmark-bridge] listening on http://${HOST}:${PORT}`);
  console.log(`[bookmark-bridge] websocket endpoint ws://${HOST}:${PORT}/ws`);
});

function buildHealthPayload() {
  const socketOpen = Boolean(executorSocket?.readyState === 1);
  const recentlySeen = lastExecutorSeenAt > 0 && (Date.now() - lastExecutorSeenAt) <= EXECUTOR_GRACE_MS;
  return {
    ok: true,
    bridge: {
      host: HOST,
      port: PORT
    },
    executorConnected: socketOpen,
    executor: {
      socketOpen,
      lastSeenAt: lastExecutorSeenAt || null,
      withinGracePeriod: recentlySeen,
      graceMs: EXECUTOR_GRACE_MS,
      extensionVersion: lastExecutorHello?.extensionVersion || null
    }
  };
}

function sendJson(res, statusCode, payload) {
  res.writeHead(statusCode, {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET,POST,OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type"
  });
  res.end(JSON.stringify(payload));
}

function readJsonBody(req) {
  return new Promise((resolve, reject) => {
    let body = "";
    req.on("data", (chunk) => {
      body += String(chunk);
    });
    req.on("end", () => {
      if (!body) {
        resolve({});
        return;
      }
      try {
        resolve(JSON.parse(body));
      } catch (error) {
        reject(new Error("Invalid JSON body"));
      }
    });
    req.on("error", reject);
  });
}

function forwardToExecutor(message) {
  return new Promise((resolve, reject) => {
    if (!executorSocket || executorSocket.readyState !== 1) {
      reject(new Error("Executor unavailable"));
      return;
    }

    const requestId = randomUUID();
    const timer = setTimeout(() => {
      pendingRequests.delete(requestId);
      reject(new Error("Executor request timed out"));
    }, 15000);

    pendingRequests.set(requestId, {
      resolve: (response) => {
        clearTimeout(timer);
        resolve(response);
      },
      reject: (error) => {
        clearTimeout(timer);
        reject(error);
      }
    });

    executorSocket.send(JSON.stringify({
      type: "request",
      requestId,
      message
    }));
  });
}
