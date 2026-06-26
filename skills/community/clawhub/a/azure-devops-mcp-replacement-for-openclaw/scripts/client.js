// SECURITY MANIFEST:
//   Environment variables accessed: AZURE_DEVOPS_ORG, AZURE_DEVOPS_PAT (only)
//   External endpoints called: https://dev.azure.com/, https://vsrm.dev.azure.com/ (only)
//   Local files read: none
//   Local files written: none

"use strict";

const https = require("https");
const { URL } = require("url");

const ORG = process.env.AZURE_DEVOPS_ORG;
const PAT = process.env.AZURE_DEVOPS_PAT;

if (!ORG || !PAT) {
  console.error(
    "❌ Missing required env vars: AZURE_DEVOPS_ORG and AZURE_DEVOPS_PAT must both be set."
  );
  process.exit(1);
}

// Validate org/project/repo names to prevent path injection
function validateSegment(value, name) {
  if (!value || typeof value !== "string") {
    console.error(`❌ Invalid ${name}: must be a non-empty string`);
    process.exit(1);
  }
  // Allow only alphanumeric, dash, underscore, dot, space (ADO names)
  if (!/^[\w\s.\-]+$/.test(value)) {
    console.error(`❌ Invalid characters in ${name}: "${value}"`);
    process.exit(1);
  }
  return encodeURIComponent(value);
}

// Build auth header from PAT
function authHeader() {
  const token = Buffer.from(`:${PAT}`).toString("base64");
  return { Authorization: `Basic ${token}`, "Content-Type": "application/json" };
}

// Generic HTTPS request
function request(urlStr, method = "GET", body = null) {
  return new Promise((resolve, reject) => {
    const parsed = new URL(urlStr);
    const options = {
      hostname: parsed.hostname,
      path: parsed.pathname + parsed.search,
      method,
      headers: {
        ...authHeader(),
        Accept: "application/json",
        "User-Agent": "openclaw-azure-devops-skill/1.0.0",
      },
    };

    if (body) {
      const payload = JSON.stringify(body);
      options.headers["Content-Length"] = Buffer.byteLength(payload);
    }

    const req = https.request(options, (res) => {
      let data = "";
      res.on("data", (chunk) => (data += chunk));
      res.on("end", () => {
        if (res.statusCode >= 400) {
          reject(new Error(`HTTP ${res.statusCode}: ${data}`));
          return;
        }
        try {
          resolve(JSON.parse(data));
        } catch {
          resolve(data);
        }
      });
    });

    req.on("error", reject);
    if (body) req.write(JSON.stringify(body));
    req.end();
  });
}

// ADO REST API base URL builders
function orgUrl(path, apiVersion = "7.1") {
  const base = `https://dev.azure.com/${encodeURIComponent(ORG)}`;
  return `${base}/${path}${path.includes("?") ? "&" : "?"}api-version=${apiVersion}`;
}

function projectUrl(project, path, apiVersion = "7.1") {
  const p = validateSegment(project, "project");
  return orgUrl(`${p}/${path}`, apiVersion);
}

// Pretty-print JSON output
function output(data) {
  console.log(JSON.stringify(data, null, 2));
}

module.exports = { request, orgUrl, projectUrl, validateSegment, output, ORG };
