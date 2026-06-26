const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const os = require("node:os");
const path = require("node:path");
const { execFileSync } = require("node:child_process");

const repoDir = path.resolve(__dirname, "..");
const fixtureDir = path.join(__dirname, "fixtures");
const env = {
  ...process.env,
  CLAWSHIER_TEST_MODE: "1",
  CLAWSHIER_TEST_DB_PATH: path.join(os.tmpdir(), `clawshier-test-${process.pid}-${Date.now()}.json`),
  OPENAI_API_KEY: "test-key",
  GOOGLE_SHEETS_ID: "test-sheet",
  GOOGLE_SERVICE_ACCOUNT_KEY: path.join(fixtureDir, "dummy-service-account.json"),
};

function runNode(scriptPath, args = [], input = undefined) {
  return execFileSync(process.execPath, [scriptPath, ...args], {
    cwd: repoDir,
    env,
    input,
    encoding: "utf8",
  });
}

test("mock pipeline runs end-to-end and detects duplicates", () => {
  const stored = runNode(path.join(repoDir, "scripts/run_pipeline.js"), [
    "--image",
    path.join(fixtureDir, "sample-receipt.png"),
    "--date",
    "2026-03-25",
  ]);

  const storedJson = JSON.parse(stored);
  assert.equal(storedJson.success, true);
  assert.equal(storedJson.row, 2);

  const db = JSON.parse(fs.readFileSync(env.CLAWSHIER_TEST_DB_PATH, "utf8"));
  assert.ok(db.sheets["03-26"]);
  assert.ok(db.sheets["Invoice Archive Breakdown"]);
  assert.ok(db.sheets.Summary);
  assert.deepEqual(db.sheets.Summary.rows[0], ["Month", "USD"]);
  assert.deepEqual(db.sheets.Summary.rows[1], ["March 2026", 8.5]);

  assert.throws(
    () => runNode(path.join(repoDir, "scripts/run_pipeline.js"), [
      "--image",
      path.join(fixtureDir, "sample-receipt.png"),
      "--date",
      "2026-03-25",
    ]),
    /Duplicate receipt detected/
  );
});

test("mock OCR rejects not-a-receipt fixtures", () => {
  assert.throws(
    () => runNode(path.join(repoDir, "skills/receipt_ocr/handler.js"), [
      "--image",
      path.join(fixtureDir, "not-a-receipt.png"),
    ]),
    /Image does not appear to be a receipt or invoice/
  );
});
