#!/usr/bin/env node
/**
 * FTP PHP Proxy API client for OpenClaw Skill
 * 
 * 从环境变量 FTP_PHP_CONFIG (JSON) 中解析配置，
 * 通过 HTTP 请求调用 PHP 代理服务器操作 FTP。
 */

import https from "https";
import http from "http";
import { readFileSync } from "fs";
import { basename } from "path";

// ============================================================
// 解析环境变量
// ============================================================
export function loadConfig() {
  const raw = process.env.FTP_PHP_CONFIG;
  if (!raw) {
    throw new Error(
      "环境变量 FTP_PHP_CONFIG 未设置。\n" +
      '格式: {"ftp_php_domain":"https://...","ftp_client_host":"...","ftp_client_username":"...","ftp_client_password":"..."}\n' +
      "请在 OpenClaw 技能管理面板中设置该环境变量。"
    );
  }

  let cfg;
  try {
    cfg = JSON.parse(raw);
  } catch (e) {
    throw new Error(`FTP_PHP_CONFIG JSON 解析失败: ${e.message}\n原始值: ${raw}`);
  }

  // 必需字段
  const domain = cfg.ftp_php_domain;
  if (!domain) throw new Error("FTP_PHP_CONFIG 缺少 ftp_php_domain 字段");

  const host = cfg.ftp_client_host;
  if (!host) throw new Error("FTP_PHP_CONFIG 缺少 ftp_client_host 字段");

  const username = cfg.ftp_client_username;
  if (!username) throw new Error("FTP_PHP_CONFIG 缺少 ftp_client_username 字段");

  const password = cfg.ftp_client_password;
  if (!password) throw new Error("FTP_PHP_CONFIG 缺少 ftp_client_password 字段");

  return {
    apiUrl: domain,
    apiKey: cfg.ftp_php_apikey || "",
    host: host,
    port: cfg.ftp_client_port || "21",
    username: username,
    password: password,
    mode: cfg.ftp_client_connect_mode || "passive",
    protocol: cfg.ftp_client_protocol || "ftp",
    tlsMode: cfg.ftp_client_encrypt_mode || "",
  };
}

// ============================================================
// 构建发送给 PHP 代理的 FTP 连接参数
// ============================================================
function buildConnParams(config) {
  return {
    host: config.host,
    port: parseInt(config.port, 10),
    username: config.username,
    password: config.password,
    mode: config.mode,
    protocol: config.protocol,
    tls_mode: config.tlsMode,
  };
}

// ============================================================
// HTTP POST JSON 请求
// ============================================================
function httpPostJson(apiUrl, apiKey, body) {
  return new Promise((resolve, reject) => {
    const url = new URL(apiUrl);
    const isHttps = url.protocol === "https:";
    const transport = isHttps ? https : http;

    const jsonData = JSON.stringify(body);

    const headers = {
      "Content-Type": "application/json",
      "Content-Length": Buffer.byteLength(jsonData),
    };
    if (apiKey) {
      headers["X-API-Key"] = apiKey;
    }

    const options = {
      hostname: url.hostname,
      port: url.port || (isHttps ? 443 : 80),
      path: url.pathname + url.search,
      method: "POST",
      headers: headers,
      rejectUnauthorized: false, // 允许自签证书
    };

    const req = transport.request(options, (res) => {
      const chunks = [];
      res.on("data", (chunk) => chunks.push(chunk));
      res.on("end", () => {
        const raw = Buffer.concat(chunks).toString("utf-8");
        try {
          const json = JSON.parse(raw);
          resolve(json);
        } catch {
          reject(new Error(`PHP 代理返回非 JSON 响应 (HTTP ${res.statusCode}):\n${raw.substring(0, 500)}`));
        }
      });
    });

    req.on("error", (e) => reject(new Error(`请求 PHP 代理失败: ${e.message}`)));
    req.setTimeout(120000, () => {
      req.destroy();
      reject(new Error("请求 PHP 代理超时 (120s)"));
    });
    req.write(jsonData);
    req.end();
  });
}

// ============================================================
// HTTP POST Multipart（用于文件上传）
// ============================================================
function httpPostMultipart(apiUrl, apiKey, fields, filePath, fileFieldName) {
  return new Promise((resolve, reject) => {
    const url = new URL(apiUrl);
    const isHttps = url.protocol === "https:";
    const transport = isHttps ? https : http;

    const boundary = "----FTPSkillBoundary" + Date.now().toString(36) + Math.random().toString(36).slice(2);
    const CRLF = "\r\n";

    // 构建 multipart body
    const parts = [];

    // 文本字段
    for (const [key, value] of Object.entries(fields)) {
      parts.push(
        `--${boundary}${CRLF}` +
        `Content-Disposition: form-data; name="${key}"${CRLF}${CRLF}` +
        `${value}`
      );
    }

    // 文件字段
    const fileContent = readFileSync(filePath);
    const fileName = basename(filePath);
    const fileHeader =
      `--${boundary}${CRLF}` +
      `Content-Disposition: form-data; name="${fileFieldName}"; filename="${fileName}"${CRLF}` +
      `Content-Type: application/octet-stream${CRLF}${CRLF}`;
    const fileFooter = CRLF + `--${boundary}--${CRLF}`;

    // 合并为 Buffer
    const headerBufs = parts.map((p) => Buffer.from(p + CRLF, "utf-8"));
    const allParts = [
      ...headerBufs,
      Buffer.from(fileHeader, "utf-8"),
      fileContent,
      Buffer.from(fileFooter, "utf-8"),
    ];
    const bodyBuffer = Buffer.concat(allParts);

    const headers = {
      "Content-Type": `multipart/form-data; boundary=${boundary}`,
      "Content-Length": bodyBuffer.length,
    };
    if (apiKey) {
      headers["X-API-Key"] = apiKey;
    }

    const options = {
      hostname: url.hostname,
      port: url.port || (isHttps ? 443 : 80),
      path: url.pathname + url.search,
      method: "POST",
      headers: headers,
      rejectUnauthorized: false,
    };

    const req = transport.request(options, (res) => {
      const chunks = [];
      res.on("data", (chunk) => chunks.push(chunk));
      res.on("end", () => {
        const raw = Buffer.concat(chunks).toString("utf-8");
        try {
          resolve(JSON.parse(raw));
        } catch {
          reject(new Error(`PHP 代理返回非 JSON 响应 (HTTP ${res.statusCode}):\n${raw.substring(0, 500)}`));
        }
      });
    });

    req.on("error", (e) => reject(new Error(`上传请求失败: ${e.message}`)));
    req.setTimeout(300000, () => {
      req.destroy();
      reject(new Error("上传请求超时 (300s)"));
    });
    req.write(bodyBuffer);
    req.end();
  });
}

// ============================================================
// 下载文件（获取 base64 响应后写入本地）
// ============================================================
function httpDownloadRaw(apiUrl, apiKey, body) {
  return new Promise((resolve, reject) => {
    const url = new URL(apiUrl);
    const isHttps = url.protocol === "https:";
    const transport = isHttps ? https : http;

    const jsonData = JSON.stringify(body);

    const headers = {
      "Content-Type": "application/json",
      "Content-Length": Buffer.byteLength(jsonData),
    };
    if (apiKey) {
      headers["X-API-Key"] = apiKey;
    }

    const options = {
      hostname: url.hostname,
      port: url.port || (isHttps ? 443 : 80),
      path: url.pathname + url.search,
      method: "POST",
      headers: headers,
      rejectUnauthorized: false,
    };

    const req = transport.request(options, (res) => {
      const chunks = [];
      res.on("data", (chunk) => chunks.push(chunk));
      res.on("end", () => {
        const rawBuf = Buffer.concat(chunks);
        const contentType = res.headers["content-type"] || "";

        // 如果是 JSON 响应（base64 模式），解析后提取
        if (contentType.includes("application/json")) {
          try {
            const json = JSON.parse(rawBuf.toString("utf-8"));
            resolve({ type: "json", data: json });
          } catch {
            reject(new Error("下载响应 JSON 解析失败"));
          }
        } else {
          // raw 二进制模式
          resolve({ type: "raw", buffer: rawBuf, headers: res.headers });
        }
      });
    });

    req.on("error", (e) => reject(new Error(`下载请求失败: ${e.message}`)));
    req.setTimeout(300000, () => {
      req.destroy();
      reject(new Error("下载请求超时 (300s)"));
    });
    req.write(jsonData);
    req.end();
  });
}

// ============================================================
// 对外暴露的 API 方法
// ============================================================

/**
 * 通用 API 调用（JSON body）
 */
export async function apiCall(action, extraParams = {}) {
  const config = loadConfig();
  const body = {
    ...buildConnParams(config),
    action,
    ...extraParams,
  };
  return httpPostJson(config.apiUrl, config.apiKey, body);
}

/**
 * 上传本地文件（multipart）
 */
export async function apiUploadFile(localPath, remotePath) {
  const config = loadConfig();
  const connParams = buildConnParams(config);
  const fields = {};
  for (const [k, v] of Object.entries(connParams)) {
    fields[k] = String(v);
  }
  fields["action"] = "upload";
  fields["remote_path"] = remotePath;

  return httpPostMultipart(config.apiUrl, config.apiKey, fields, localPath, "file");
}

/**
 * 上传文本内容到远程文件
 */
export async function apiUploadContent(content, remotePath) {
  return apiCall("upload", { remote_path: remotePath, content: content });
}

/**
 * 下载文件，返回 { buffer, filename }
 */
export async function apiDownloadFile(remotePath) {
  const config = loadConfig();
  const body = {
    ...buildConnParams(config),
    action: "download",
    path: remotePath,
    raw: "0", // 使用 base64 JSON 模式，确保兼容
  };
  const result = await httpPostJson(config.apiUrl, config.apiKey, body);

  if (result.code !== 200) {
    throw new Error(`下载失败: ${result.message}`);
  }

  const b64 = result.data?.content_base64;
  if (!b64) {
    throw new Error("下载响应中缺少 content_base64 字段");
  }

  return {
    buffer: Buffer.from(b64, "base64"),
    filename: result.data.filename || basename(remotePath),
    size: result.data.size || 0,
  };
}

// ============================================================
// 命令行参数解析
// ============================================================
export function parseArgs(argv) {
  const args = argv.slice(2);
  const result = { _: [] };

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if (arg === "--detailed" || arg === "-l") {
      result.detailed = true;
    } else if (arg === "--dir" || arg === "-d") {
      result.dir = true;
    } else if (arg === "--verbose" || arg === "-v") {
      result.verbose = true;
    } else if ((arg === "--out" || arg === "-o") && i + 1 < args.length) {
      result.out = args[++i];
    } else if ((arg === "--to" || arg === "-t") && i + 1 < args.length) {
      result.to = args[++i];
    } else if (arg === "--encoding" && i + 1 < args.length) {
      result.encoding = args[++i];
    } else if (arg === "--stdin") {
      result.stdin = true;
    } else if (arg.startsWith("-")) {
      console.error(`未知选项: ${arg}`);
    } else {
      result._.push(arg);
    }
  }

  return result;
}

/**
 * 格式化文件大小
 */
export function formatSize(bytes) {
  if (bytes === null || bytes === undefined || bytes < 0) return "N/A";
  if (bytes === 0) return "0 B";
  const units = ["B", "KB", "MB", "GB", "TB"];
  const i = Math.floor(Math.log(bytes) / Math.log(1024));
  return (bytes / Math.pow(1024, i)).toFixed(i > 0 ? 1 : 0) + " " + units[i];
}

/**
 * 检查 API 响应，失败则抛出异常
 */
export function checkResponse(result, actionName) {
  if (result.code !== 200) {
    throw new Error(`${actionName} 失败: ${result.message}`);
  }
  return result.data;
}