"use strict";

const assert = require("assert");
const fs = require("fs");
const os = require("os");
const path = require("path");
const { findPython, probePython } = require("../lib/python");

function writeFakePython(dir, name, version) {
  const file = path.join(dir, name);
  fs.writeFileSync(
    file,
    `#!/bin/sh\nif [ "$1" = "-c" ]; then\n  printf '${version}\\n'\n  exit 0\nfi\nexit 1\n`,
    { mode: 0o700 },
  );
}

function withPath(dir) {
  return { ...process.env, PATH: dir, X402_VOICE_PYTHON: "" };
}

const tmp = fs.mkdtempSync(path.join(os.tmpdir(), "clawvoice-python-"));
try {
  writeFakePython(tmp, "python3.9", "3.9");
  writeFakePython(tmp, "python3", "3.14");

  const candidates = ["python3.12", "python3.11", "python3.10", "python3.9", "python3"];
  const env = withPath(tmp);
  const probe = probePython({ env, candidates });

  assert.strictEqual(probe.selected, "python3.9");
  assert.strictEqual(findPython({ env, candidates, log: () => {} }), "python3.9");
  assert.deepStrictEqual(
    probe.candidates.map((candidate) => candidate.bin),
    ["python3.12", "python3.11", "python3.10", "python3.9"],
  );
} finally {
  fs.rmSync(tmp, { recursive: true, force: true });
}
