#!/usr/bin/env node
import crypto from "node:crypto";
import { execFileSync } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const skillRoot = path.resolve(scriptDir, "..");
const bundlePath = path.join(skillRoot, "vendor", "clink-integ-cli", "clink-integ-cli.js");
const manifestPath = path.join(skillRoot, "vendor", "clink-integ-cli", "manifest.json");
const sumsPath = path.join(skillRoot, "vendor", "clink-integ-cli", "SHA256SUMS");
const versionPath = path.join(skillRoot, "vendor", "clink-integ-cli", "VERSION");

const failures = [];
let checks = 0;

check(fs.existsSync(bundlePath), `missing CLI bundle: ${bundlePath}`);
check(fs.existsSync(manifestPath), `missing CLI bundle manifest: ${manifestPath}`);
check(fs.existsSync(sumsPath), `missing CLI bundle checksum file: ${sumsPath}`);
check(fs.existsSync(versionPath), `missing CLI bundle version file: ${versionPath}`);

let expectedVersion = null;
if (fs.existsSync(versionPath)) {
  expectedVersion = fs.readFileSync(versionPath, "utf8").trim();
  check(expectedVersion.length > 0, "CLI bundle VERSION must not be empty");
}

if (fs.existsSync(manifestPath)) {
  const manifest = JSON.parse(fs.readFileSync(manifestPath, "utf8"));
  check(manifest.name === "clink-integ-cli", "CLI bundle manifest name should be clink-integ-cli");
  if (expectedVersion) {
    check(manifest.version === expectedVersion, "CLI bundle manifest version must match VERSION");
  }
  check(manifest.bundle === "clink-integ-cli.js", "CLI bundle manifest should name the clink-integ-cli.js bundle");
}

if (fs.existsSync(bundlePath) && fs.existsSync(sumsPath)) {
  const bundle = fs.readFileSync(bundlePath);
  const expected = fs.readFileSync(sumsPath, "utf8").trim().split(/\s+/)[0];
  const actual = crypto.createHash("sha256").update(bundle).digest("hex");
  const text = bundle.toString("utf8");
  check(actual === expected, "CLI bundle SHA256 does not match SHA256SUMS");
  check(!text.includes("readPackageJson"), "CLI bundle should not read package.json for its version");
  check(!text.includes("github:"), "CLI bundle must not instruct GitHub package installs");
  check(!text.includes("npm install --prefix ./.clink-tools playwright"), "CLI bundle must not instruct remote Playwright installs");
  check(!text.includes("npm install -g playwright"), "CLI bundle must not instruct global Playwright installs");
}

const capabilityChecks = [
  {
    args: ["--version"],
    contains: [expectedVersion || "__missing_version__"],
  },
  {
    args: ["--help"],
    contains: [
      "api",
      "auth",
      "billing",
      "catalog",
      "checkout",
      "dashboard",
      "doctor",
      "env",
      "init",
      "login",
      "order",
      "payment",
      "price",
      "product",
      "refund",
      "smoke-test",
      "subscription",
      "webhook",
    ],
  },
  {
    args: ["env", "list", "--help"],
    contains: ["List built-in and custom environments"],
  },
  {
    args: ["env", "add", "--help"],
    contains: ["--api-base-url", "--dashboard-base-url", "--dashboard-login-url", "--dashboard-client-id"],
  },
  {
    args: ["env", "show", "--help"],
    contains: ["<name>", "Show the resolved configuration for an environment"],
  },
  {
    args: ["auth", "secret", "set", "--help"],
    contains: ["--api-key", "env:CLINK_SECRET_KEY", "--env"],
  },
  {
    args: ["auth", "status", "--help"],
    contains: ["Show resolved auth status without revealing secrets"],
  },
  {
    args: ["api", "request", "--help"],
    contains: ["<method>", "<path>", "--data", "--data-file"],
  },
  {
    args: ["catalog", "validate", "--help"],
    contains: ["--file", "--project-root", "--public-dir"],
  },
  {
    args: ["catalog", "plan", "--help"],
    contains: ["--file", "--project-root", "--public-dir"],
  },
  {
    args: ["catalog", "import", "--help"],
    contains: ["--file", "--project-root", "--public-dir", "imageId"],
  },
  {
    args: ["checkout", "--help"],
    contains: ["session"],
  },
  {
    args: ["subscription", "--help"],
    contains: ["create", "cancel", "get"],
  },
  {
    args: ["order", "--help"],
    contains: ["get", "list"],
  },
  {
    args: ["refund", "--help"],
    contains: ["create", "get"],
  },
  {
    args: ["webhook", "endpoint", "ensure", "--help"],
    contains: ["--url", "--events", "--save-secret", "--show-secret", "--sync-env-file"],
  },
  {
    args: ["webhook", "verify", "--help"],
    contains: ["--secret", "--body-file", "--signature"],
  },
  {
    args: ["doctor", "--help"],
    contains: ["--skip-network", "--webhook-url"],
  },
  {
    args: ["smoke-test", "--help"],
    contains: ["checkout", "webhook"],
  },
];

for (const { args, contains } of capabilityChecks) {
  if (!fs.existsSync(bundlePath)) break;
  const output = execFileSync(process.execPath, [bundlePath, ...args], { encoding: "utf8" });
  check(output.trim().length > 0, `CLI bundle produced no output for: ${args.join(" ")}`);
  for (const token of contains) {
    check(output.includes(token), `CLI bundle output for "${args.join(" ")}" is missing capability token: ${token}`);
  }
}

if (fs.existsSync(bundlePath)) {
  const tempDir = fs.mkdtempSync(path.join(os.tmpdir(), "clink-integ-cli-verify-"));
  try {
    const catalogPath = writeCatalogWithImageFile(tempDir);
    const output = execFileSync(process.execPath, [
      bundlePath,
      "catalog",
      "validate",
      "--file",
      catalogPath,
      "--json",
    ], {
      encoding: "utf8",
      env: {
        ...process.env,
        CLINK_CONFIG_PATH: path.join(tempDir, "config.json"),
        CLINK_SECRET_KEY: "",
        CLINK_API_KEY: "",
      },
    });
    check(output.includes("\"ok\": true"), "CLI bundle should validate a catalog fixture successfully");
    check(output.includes("\"imageFile\""), "CLI bundle catalog validation should preserve imageFile capability");
    check(output.includes("\"imageSource\""), "CLI bundle catalog validation should inspect local imageFile assets");
  } finally {
    fs.rmSync(tempDir, { recursive: true, force: true });
  }
}

if (failures.length > 0) {
  console.error(`FAIL: ${failures.length} CLI bundle checks failed`);
  for (const failure of failures) console.error(`- ${failure}`);
  process.exit(1);
}

console.log(`PASS: ${checks} CLI bundle checks passed`);

function check(condition, message) {
  checks += 1;
  if (!condition) failures.push(message);
}

function writeCatalogWithImageFile(tempDir) {
  const oneByOnePng = Buffer.from(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+/p9sAAAAASUVORK5CYII=",
    "base64"
  );
  fs.mkdirSync(path.join(tempDir, "assets"), { recursive: true });
  fs.writeFileSync(path.join(tempDir, "assets", "starter.png"), oneByOnePng);
  const catalogPath = path.join(tempDir, "catalog.json");
  fs.writeFileSync(
    catalogPath,
    `${JSON.stringify({
      version: 1,
      products: [
        {
          sourceId: "starter-plan",
          name: "Starter",
          description: "Starter subscription plan",
          imageFile: "assets/starter.png",
          taxCategory: "software_service",
          prices: [
            {
              sourceId: "starter-monthly",
              type: "recurring",
              amount: 9.99,
              currency: "USD",
              interval: "month",
              default: true,
            },
          ],
        },
      ],
    }, null, 2)}\n`,
    "utf8"
  );
  return catalogPath;
}
