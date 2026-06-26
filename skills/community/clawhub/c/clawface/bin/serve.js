#!/usr/bin/env node
"use strict";

const http = require("http");
const fs = require("fs");
const path = require("path");
const crypto = require("crypto");
const { execFile } = require("child_process");
const os = require("os");
const { URL } = require("url");

// -- CLI arg parsing ----------------------------------------------------------

function parseArgs(argv) {
  const args = {};
  for (let i = 2; i < argv.length; i++) {
    const arg = argv[i];
    if (arg.startsWith("--") && i + 1 < argv.length) {
      args[arg.slice(2)] = argv[++i];
    }
  }
  return args;
}

const args = parseArgs(process.argv);

const distDir = path.resolve(args.dist || path.join(__dirname, "..", "dist"));
const toolsDir = args["tools-dir"] ? path.resolve(args["tools-dir"]) : "";
const port = parseInt(args.port || "18794", 10);
const gatewayUrl = args["gateway-url"] || "";
const gatewayToken = args["gateway-token"] || "";

// Device credentials: accept --device-id/--private-key/--public-key directly,
// or load from --identity-file (path to device.json).
let deviceId = args["device-id"] || "";
let privateKeyPem = "";
let publicKeyBase64Url = "";

if (!deviceId && args["identity-file"]) {
  try {
    const identity = JSON.parse(fs.readFileSync(args["identity-file"], "utf8"));
    deviceId = identity.deviceId || "";
    privateKeyPem = identity.privateKeyPem || "";
    if (identity.publicKeyPem) {
      const key = crypto.createPublicKey(identity.publicKeyPem);
      const der = key.export({ type: "spki", format: "der" });
      publicKeyBase64Url = der.subarray(-32).toString("base64url");
    }
  } catch (e) {
    console.error(`Failed to read identity file: ${e.message}`);
    process.exit(1);
  }
}

if (!fs.existsSync(distDir)) {
  console.error(`dist directory not found: ${distDir}`);
  process.exit(1);
}

// -- MIME types ---------------------------------------------------------------

const MIME = {
  ".html": "text/html; charset=utf-8",
  ".js": "application/javascript",
  ".mjs": "application/javascript",
  ".css": "text/css",
  ".json": "application/json",
  ".wasm": "application/wasm",
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".gif": "image/gif",
  ".svg": "image/svg+xml",
  ".ico": "image/x-icon",
  ".glb": "model/gltf-binary",
  ".gltf": "model/gltf+json",
  ".ktx": "image/ktx",
  ".ktx2": "image/ktx2",
  ".bin": "application/octet-stream",
  ".ttf": "font/ttf",
  ".woff": "font/woff",
  ".woff2": "font/woff2",
  ".map": "application/json",
};

function mimeType(filePath) {
  return MIME[path.extname(filePath).toLowerCase()] || "application/octet-stream";
}

// -- Config injection (no secrets) --------------------------------------------

const configScript = `<script>
window.CLAWFACE_CONFIG = {
  wsUrl: ${JSON.stringify(`ws://localhost:${port}/ws`)}
};
</script>
</head>`;

let indexHtml = null;

function getIndexHtml() {
  if (indexHtml !== null) return indexHtml;
  const raw = fs.readFileSync(path.join(distDir, "index.html"), "utf8");
  indexHtml = raw.replace("</head>", configScript);
  return indexHtml;
}

// -- COOP/COEP headers -------------------------------------------------------

const securityHeaders = {
  "Cross-Origin-Opener-Policy": "same-origin",
  "Cross-Origin-Embedder-Policy": "credentialless",
};

// -- Minimal WebSocket framing (RFC 6455) ------------------------------------

function decodeFrame(buf) {
  if (buf.length < 2) return null;
  const opcode = buf[0] & 0x0f;
  const fin = (buf[0] & 0x80) !== 0;
  const masked = (buf[1] & 0x80) !== 0;
  let payloadLen = buf[1] & 0x7f;
  let offset = 2;

  if (payloadLen === 126) {
    if (buf.length < 4) return null;
    payloadLen = buf.readUInt16BE(2);
    offset = 4;
  } else if (payloadLen === 127) {
    if (buf.length < 10) return null;
    payloadLen = Number(buf.readBigUInt64BE(2));
    offset = 10;
  }

  let maskKey = null;
  if (masked) {
    if (buf.length < offset + 4) return null;
    maskKey = buf.subarray(offset, offset + 4);
    offset += 4;
  }

  if (buf.length < offset + payloadLen) return null;

  let payload = buf.subarray(offset, offset + payloadLen);
  if (masked) {
    payload = Buffer.from(payload);
    for (let i = 0; i < payload.length; i++) {
      payload[i] ^= maskKey[i & 3];
    }
  }

  return { opcode, fin, payload, totalLen: offset + payloadLen };
}

function encodeFrame(opcode, payload, mask) {
  const len = payload.length;
  let header;
  if (len < 126) {
    header = Buffer.alloc(2);
    header[0] = 0x80 | opcode;
    header[1] = (mask ? 0x80 : 0) | len;
  } else if (len < 65536) {
    header = Buffer.alloc(4);
    header[0] = 0x80 | opcode;
    header[1] = (mask ? 0x80 : 0) | 126;
    header.writeUInt16BE(len, 2);
  } else {
    header = Buffer.alloc(10);
    header[0] = 0x80 | opcode;
    header[1] = (mask ? 0x80 : 0) | 127;
    header.writeBigUInt64BE(BigInt(len), 2);
  }

  if (mask) {
    const maskKey = crypto.randomBytes(4);
    const masked = Buffer.from(payload);
    for (let i = 0; i < masked.length; i++) {
      masked[i] ^= maskKey[i & 3];
    }
    return Buffer.concat([header, maskKey, masked]);
  }

  return Buffer.concat([header, payload]);
}

function sendText(socket, text, mask) {
  socket.write(encodeFrame(0x01, Buffer.from(text), mask));
}

function sendClose(socket, mask) {
  socket.write(encodeFrame(0x08, Buffer.alloc(0), mask));
}

function sendPong(socket, payload, mask) {
  socket.write(encodeFrame(0x0a, payload, mask));
}

// -- Gateway auth (v3 protocol) -----------------------------------------------

function buildV3Payload(params) {
  return [
    "v3", params.deviceId, params.clientId, params.clientMode, params.role,
    params.scopes.join(","), String(params.signedAtMs), params.token,
    params.nonce, params.platform || "", params.deviceFamily || "",
  ].join("|");
}

function signPayload(pem, payload) {
  const key = crypto.createPrivateKey(pem);
  const sig = crypto.sign(null, Buffer.from(payload), key);
  return sig.toString("base64url");
}

function buildConnectFrame(nonce) {
  const signedAtMs = Date.now();
  const scopes = [
    "operator.admin", "operator.read", "operator.write",
    "operator.approvals", "operator.pairing",
  ];

  const payload = buildV3Payload({
    deviceId, clientId: "cli", clientMode: "cli", role: "operator",
    scopes, signedAtMs, token: gatewayToken, nonce, platform: "node",
  });
  const signature = signPayload(privateKeyPem, payload);

  return JSON.stringify({
    type: "req",
    id: `${Date.now().toString(16)}-proxy`,
    method: "connect",
    params: {
      minProtocol: 3, maxProtocol: 3,
      client: {
        id: "cli", displayName: "Clawface Web", version: "1.0",
        platform: "node", mode: "cli",
        instanceId: `clawface-${Date.now()}`,
      },
      locale: "en-US", userAgent: "clawface-web",
      role: "operator", scopes, caps: [],
      device: {
        id: deviceId, publicKey: publicKeyBase64Url,
        signature, signedAt: signedAtMs, nonce,
      },
      auth: { token: gatewayToken },
    },
  });
}

// -- WebSocket proxy ----------------------------------------------------------

function connectToGateway(browserSocket) {
  const gwUrl = new URL(gatewayUrl.replace(/^ws/, "http"));
  const wsKey = crypto.randomBytes(16).toString("base64");

  const req = http.request({
    hostname: gwUrl.hostname,
    port: gwUrl.port || (gwUrl.protocol === "https:" ? 443 : 80),
    path: gwUrl.pathname + gwUrl.search,
    method: "GET",
    headers: {
      "Upgrade": "websocket",
      "Connection": "Upgrade",
      "Sec-WebSocket-Key": wsKey,
      "Sec-WebSocket-Version": "13",
    },
  });

  req.on("upgrade", (res, gwSocket) => {
    let authenticated = false;
    let gwBuf = Buffer.alloc(0);
    let brBuf = Buffer.alloc(0);

    // Gateway → browser (with auth interception)
    gwSocket.on("data", (chunk) => {
      gwBuf = Buffer.concat([gwBuf, chunk]);
      while (true) {
        const frame = decodeFrame(gwBuf);
        if (!frame) break;
        gwBuf = gwBuf.subarray(frame.totalLen);

        if (frame.opcode === 0x08) {
          sendClose(browserSocket, false);
          browserSocket.end();
          gwSocket.end();
          return;
        }
        if (frame.opcode === 0x09) {
          sendPong(gwSocket, frame.payload, true);
          continue;
        }
        if (frame.opcode !== 0x01) continue;

        const text = frame.payload.toString("utf8");
        let msg;
        try { msg = JSON.parse(text); } catch { continue; }

        // Intercept connect.challenge — sign and respond server-side
        if (!authenticated && msg.type === "event" && msg.event === "connect.challenge") {
          const nonce = msg.payload?.nonce;
          if (nonce) {
            sendText(gwSocket, buildConnectFrame(nonce), true);
          }
          continue;
        }

        // Forward hello-ok to browser (marks connection as ready)
        if (!authenticated && msg.type === "res" && msg.ok === true) {
          const pt = msg.payload?.type;
          if (pt === "hello-ok" || pt === "hello") {
            authenticated = true;
          }
        }

        // Forward everything else to browser
        sendText(browserSocket, text, false);
      }
    });

    gwSocket.on("close", () => {
      sendClose(browserSocket, false);
      browserSocket.end();
    });

    gwSocket.on("error", (err) => {
      console.error(`[ws-proxy] gateway error: ${err.message}`);
      sendClose(browserSocket, false);
      browserSocket.end();
    });

    // Browser → gateway
    browserSocket.on("data", (chunk) => {
      brBuf = Buffer.concat([brBuf, chunk]);
      while (true) {
        const frame = decodeFrame(brBuf);
        if (!frame) break;
        brBuf = brBuf.subarray(frame.totalLen);

        if (frame.opcode === 0x08) {
          sendClose(gwSocket, true);
          gwSocket.end();
          browserSocket.end();
          return;
        }
        if (frame.opcode === 0x09) {
          sendPong(browserSocket, frame.payload, false);
          continue;
        }
        if (frame.opcode !== 0x01) continue;

        // Forward browser frames to gateway (must be masked per RFC 6455)
        sendText(gwSocket, frame.payload.toString("utf8"), true);
      }
    });

    browserSocket.on("close", () => {
      sendClose(gwSocket, true);
      gwSocket.end();
    });

    browserSocket.on("error", (err) => {
      console.error(`[ws-proxy] browser error: ${err.message}`);
      sendClose(gwSocket, true);
      gwSocket.end();
    });
  });

  req.on("error", (err) => {
    console.error(`[ws-proxy] gateway connect failed: ${err.message}`);
    sendClose(browserSocket, false);
    browserSocket.end();
  });

  req.end();
}

function handleUpgrade(req, socket) {
  const wsKey = req.headers["sec-websocket-key"];
  if (!wsKey) {
    socket.end("HTTP/1.1 400 Bad Request\r\n\r\n");
    return;
  }

  const acceptKey = crypto
    .createHash("sha1")
    .update(wsKey + "258EAFA5-E914-47DA-95CA-5AB5DC11650A")
    .digest("base64");

  socket.write(
    "HTTP/1.1 101 Switching Protocols\r\n" +
    "Upgrade: websocket\r\n" +
    "Connection: Upgrade\r\n" +
    `Sec-WebSocket-Accept: ${acceptKey}\r\n` +
    "\r\n"
  );

  connectToGateway(socket);
}

// -- TTS endpoint -------------------------------------------------------------

function handleTts(req, res) {
  let body = "";
  req.on("data", (chunk) => (body += chunk));
  req.on("end", () => {
    let text;
    try {
      text = JSON.parse(body).text || "";
    } catch {
      res.writeHead(400);
      res.end("Bad request");
      return;
    }
    if (!text.trim()) {
      res.writeHead(400);
      res.end("Missing text");
      return;
    }

    // Resolve TTS paths from --tools-dir
    if (!toolsDir) {
      res.writeHead(503);
      res.end("TTS not configured (no --tools-dir)");
      return;
    }
    const runtimeDir = path.join(toolsDir, "runtime");

    const bin = path.join(runtimeDir, "bin", "sherpa-onnx-offline-tts");
    if (!fs.existsSync(bin)) {
      res.writeHead(503);
      res.end("TTS binary not found");
      return;
    }

    // Auto-detect first model subdir under --tools-dir/models
    const modelsRoot = path.join(toolsDir, "models");
    let modelDir = "";
    try {
      const subdirs = fs.readdirSync(modelsRoot).filter((f) =>
        fs.statSync(path.join(modelsRoot, f)).isDirectory()
      );
      if (subdirs.length >= 1) modelDir = path.join(modelsRoot, subdirs[0]);
    } catch {}
    if (!modelDir) {
      res.writeHead(503);
      res.end("TTS model not found");
      return;
    }

    // Resolve model files
    let modelFile;
    try {
      const candidates = fs.readdirSync(modelDir).filter((f) => f.endsWith(".onnx"));
      if (candidates.length === 1) modelFile = path.join(modelDir, candidates[0]);
      else { res.writeHead(503); res.end("Model not found"); return; }
    } catch { res.writeHead(503); res.end("Model dir error"); return; }

    const tokensFile = path.join(modelDir, "tokens.txt");
    const dataDir = path.join(modelDir, "espeak-ng-data");
    const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), "tts-"));
    const outputPath = path.join(tmpDir, "speech.wav");

    const libDir = path.join(runtimeDir, "lib");
    const env = { LD_LIBRARY_PATH: libDir, DYLD_LIBRARY_PATH: libDir, PATH: runtimeDir + "/bin" };

    execFile(
      bin,
      [
        `--vits-model=${modelFile}`,
        `--vits-tokens=${tokensFile}`,
        `--vits-data-dir=${dataDir}`,
        `--output-filename=${outputPath}`,
        text,
      ],
      { env, timeout: 30000 },
      (err) => {
        if (err) {
          res.writeHead(500);
          res.end(`TTS failed: ${err.message}`);
          try { fs.rmSync(tmpDir, { recursive: true }); } catch {}
          return;
        }
        try {
          const audio = fs.readFileSync(outputPath);
          res.writeHead(200, {
            ...securityHeaders,
            "Content-Type": "audio/wav",
            "Content-Length": audio.length,
          });
          res.end(audio);
        } finally {
          try { fs.rmSync(tmpDir, { recursive: true }); } catch {}
        }
      }
    );
  });
}

// -- HTTP server --------------------------------------------------------------

const server = http.createServer((req, res) => {
  // Strip query string and decode
  let urlPath = decodeURIComponent(req.url.split("?")[0]);

  // TTS endpoint
  if (urlPath === "/tts" && req.method === "POST") {
    return handleTts(req, res);
  }

  // Prevent path traversal
  if (urlPath.includes("..")) {
    res.writeHead(400);
    res.end("Bad request");
    return;
  }

  // Default to index.html
  if (urlPath === "/" || urlPath === "") {
    urlPath = "/index.html";
  }

  // Serve injected index.html
  if (urlPath === "/index.html") {
    const body = getIndexHtml();
    res.writeHead(200, {
      ...securityHeaders,
      "Content-Type": "text/html; charset=utf-8",
      "Content-Length": Buffer.byteLength(body),
      "Cache-Control": "no-cache",
    });
    res.end(body);
    return;
  }

  // Serve static files
  const filePath = path.join(distDir, urlPath);

  // Ensure resolved path is within distDir
  if (!path.resolve(filePath).startsWith(path.resolve(distDir))) {
    res.writeHead(403);
    res.end("Forbidden");
    return;
  }

  fs.stat(filePath, (err, stats) => {
    if (err || !stats.isFile()) {
      res.writeHead(404);
      res.end("Not found");
      return;
    }

    res.writeHead(200, {
      ...securityHeaders,
      "Content-Type": mimeType(filePath),
      "Content-Length": stats.size,
      "Cache-Control": "public, max-age=3600",
    });

    fs.createReadStream(filePath).pipe(res);
  });
});

// Handle WebSocket upgrade on /ws
server.on("upgrade", (req, socket, head) => {
  if (req.url.split("?")[0] === "/ws") {
    handleUpgrade(req, socket);
  } else {
    socket.end("HTTP/1.1 404 Not Found\r\n\r\n");
  }
});

server.listen(port, () => {
  console.log(`http://localhost:${port}`);
});
