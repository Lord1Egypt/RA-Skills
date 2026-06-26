const { describe, it, beforeEach, afterEach } = require("node:test");
const assert = require("node:assert/strict");
const fs = require("fs");
const os = require("os");
const path = require("path");

let tmpMemoryDir;
const savedEnv = {};
const envKeys = ["EVOLVER_ATP_AUTOBUY", "MEMORY_DIR"];

function makeTmpMemoryDir() {
  return fs.mkdtempSync(path.join(os.tmpdir(), "cli-autobuy-prompt-"));
}

function freshModule() {
  for (const k of Object.keys(require.cache)) {
    if (k.includes("/src/atp/") || k.includes("/src/gep/paths")) {
      delete require.cache[k];
    }
  }
  // Return both the prompt and autoBuyer so tests reach ack-file plumbing
  // (filename constant + path resolver) through autoBuyer's public surface
  // instead of duplicated re-exports on cliAutobuyPrompt.__internals
  // (Bugbot PR #141 R6 follow-up).
  const prompt = require("../src/atp/cliAutobuyPrompt");
  const autoBuyer = require("../src/atp/autoBuyer");
  return Object.assign(prompt, { autoBuyer });
}

function makeTTY(preset) {
  return {
    isTTY: true,
    _answer: preset,
  };
}

function makeNonTTY() {
  return { isTTY: false };
}

function collectingStream() {
  const chunks = [];
  return {
    write(x) {
      chunks.push(String(x));
      return true;
    },
    read() {
      return chunks.join("");
    },
  };
}

beforeEach(() => {
  for (const k of envKeys) {
    savedEnv[k] = process.env[k];
    delete process.env[k];
  }
  tmpMemoryDir = makeTmpMemoryDir();
  process.env.MEMORY_DIR = tmpMemoryDir;
});

afterEach(() => {
  for (const k of envKeys) {
    if (savedEnv[k] === undefined) delete process.env[k];
    else process.env[k] = savedEnv[k];
  }
  try {
    fs.rmSync(tmpMemoryDir, { recursive: true, force: true });
  } catch (_) {}
});

describe("cliAutobuyPrompt", () => {
  it("skips completely when stdin is not a TTY", async () => {
    const mod = freshModule();
    const output = collectingStream();
    const fakeAsk = async () => {
      throw new Error("ask should not be called in non-TTY mode");
    };

    const res = await mod.runPrompt({
      input: makeNonTTY(),
      output,
      env: { ...process.env },
      ask: fakeAsk,
    });

    assert.equal(res.prompted, false);
    assert.equal(res.reason, "non_tty");
    assert.equal(res.decision, null);
    assert.equal(output.read(), "");
    assert.equal(fs.existsSync(mod.autoBuyer.getAckPath()), false);
  });

  it("skips when EVOLVER_ATP_AUTOBUY is already set (any value)", async () => {
    const mod = freshModule();
    const output = collectingStream();
    const env = { EVOLVER_ATP_AUTOBUY: "off" };

    const res = await mod.runPrompt({
      input: makeTTY("y"),
      output,
      env,
      ask: async () => {
        throw new Error("ask should not be called when env is set");
      },
    });

    assert.equal(res.prompted, false);
    assert.equal(res.reason, "env_set");
    assert.equal(output.read(), "");
  });

  it("skips when an ack file already exists", async () => {
    const mod = freshModule();
    fs.mkdirSync(tmpMemoryDir, { recursive: true });
    fs.writeFileSync(
      path.join(tmpMemoryDir, mod.autoBuyer.ACK_FILENAME),
      JSON.stringify({ enabled: false, acknowledged_at: "2026-04-20", version: 1 }),
    );
    const output = collectingStream();

    const res = await mod.runPrompt({
      input: makeTTY("y"),
      output,
      env: { ...process.env, EVOLVER_ATP_AUTOBUY: undefined },
      ask: async () => {
        throw new Error("ask should not be called when ack exists");
      },
    });

    assert.equal(res.prompted, false);
    assert.equal(res.reason, "ack_present");
  });

  it("on answer='y' writes ack enabled=true (does NOT mutate env)", async () => {
    const mod = freshModule();
    const output = collectingStream();
    const env = { ...process.env };
    delete env.EVOLVER_ATP_AUTOBUY;

    const res = await mod.runPrompt({
      input: makeTTY("y"),
      output,
      env,
      ask: async () => "y",
    });

    assert.equal(res.prompted, true);
    assert.equal(res.decision, "yes");
    // env is left untouched: autoBuyer.getConsent() reads the ack file
    // directly and only falls back to env when no ack exists.
    assert.equal(env.EVOLVER_ATP_AUTOBUY, undefined);
    const ack = JSON.parse(fs.readFileSync(mod.autoBuyer.getAckPath(), "utf8"));
    assert.equal(ack.enabled, true);
    assert.equal(ack.version, 1);
    assert.match(output.read(), /\[ATP-AutoBuyer\]/);
  });

  it("on answer='n' writes ack enabled=false (does NOT mutate env)", async () => {
    const mod = freshModule();
    const output = collectingStream();
    const env = { ...process.env };
    delete env.EVOLVER_ATP_AUTOBUY;

    const res = await mod.runPrompt({
      input: makeTTY("n"),
      output,
      env,
      ask: async () => "n",
    });

    assert.equal(res.prompted, true);
    assert.equal(res.decision, "no");
    assert.equal(env.EVOLVER_ATP_AUTOBUY, undefined);
    const ack = JSON.parse(fs.readFileSync(mod.autoBuyer.getAckPath(), "utf8"));
    assert.equal(ack.enabled, false);
  });

  it("on answer='later' (or anything else) writes NO ack and keeps env untouched", async () => {
    const mod = freshModule();
    const output = collectingStream();
    const env = { ...process.env };
    delete env.EVOLVER_ATP_AUTOBUY;

    const res = await mod.runPrompt({
      input: makeTTY("later"),
      output,
      env,
      ask: async () => "later",
    });

    assert.equal(res.prompted, true);
    assert.equal(res.decision, "later");
    assert.equal(env.EVOLVER_ATP_AUTOBUY, undefined);
    assert.equal(fs.existsSync(mod.autoBuyer.getAckPath()), false);

    const res2 = await mod.runPrompt({
      input: makeTTY(""),
      output,
      env,
      ask: async () => "",
    });
    assert.equal(res2.decision, "later");
    assert.equal(fs.existsSync(mod.autoBuyer.getAckPath()), false);
  });

  it("on ack write failure: surfaces WARN and returns reason='ack_write_failed'", async () => {
    // Bugbot PR #141 Medium: unchecked ack write would silently lose the
    // user's explicit opt-in. Simulate FS failure by pointing MEMORY_DIR at
    // a file (so mkdirSync inside setConsent → ENOTDIR or similar).
    const collidingPath = path.join(tmpMemoryDir, "is-a-file-not-a-dir");
    fs.writeFileSync(collidingPath, "x");
    process.env.MEMORY_DIR = collidingPath;

    const mod = freshModule();
    const output = collectingStream();
    const env = { ...process.env };
    delete env.EVOLVER_ATP_AUTOBUY;

    const res = await mod.runPrompt({
      input: makeTTY("y"),
      output,
      env,
      ask: async () => "y",
    });

    assert.equal(res.prompted, true);
    assert.equal(res.decision, "yes", "decision still reflects what the user typed");
    assert.equal(res.reason, "ack_write_failed", "reason flags the persistence failure");
    assert.match(output.read(), /failed to persist consent/i);
    assert.match(output.read(), /evolver atp enable/);
  });

  it("corrupted ack file does NOT permanently suppress prompt (Bugbot R3)", async () => {
    // Bugbot PR #141 Low: classify previously accepted any parsed object as
    // "ack_present" (suppressing prompt forever) while autoBuyer.getConsent
    // rejected non-boolean `enabled` (returning no_consent). User stuck:
    // no prompt + autoBuyer off. Both readers now share the strict check;
    // corrupted ack → both treat as absent → prompt re-fires.
    const mod = freshModule();
    fs.mkdirSync(tmpMemoryDir, { recursive: true });
    fs.writeFileSync(
      path.join(tmpMemoryDir, mod.autoBuyer.ACK_FILENAME),
      JSON.stringify({ enabled: "yes", acknowledged_at: "x", version: 1 }),
    );

    // classify must NOT return ack_present — corrupted file is treated as
    // absent so the user gets another chance.
    assert.equal(mod.classify({}, makeTTY("y")), "eligible");
  });

  it("classify() returns the precedence order (env_set > non_tty > ack > eligible)", async () => {
    const mod = freshModule();

    assert.equal(
      mod.classify({ EVOLVER_ATP_AUTOBUY: "on" }, makeNonTTY()),
      "env_set",
      "env takes priority over TTY",
    );
    assert.equal(
      mod.classify({}, makeNonTTY()),
      "non_tty",
      "non-TTY comes before ack/eligible when env is unset",
    );
    assert.equal(
      mod.classify({}, makeTTY("y")),
      "eligible",
      "fresh install on a TTY is eligible",
    );

    fs.mkdirSync(tmpMemoryDir, { recursive: true });
    fs.writeFileSync(
      path.join(tmpMemoryDir, mod.autoBuyer.ACK_FILENAME),
      JSON.stringify({ enabled: false, acknowledged_at: "2026-04-20", version: 1 }),
    );
    assert.equal(
      mod.classify({}, makeTTY("y")),
      "ack_present",
      "ack file demotes eligible to ack_present",
    );
  });
});
