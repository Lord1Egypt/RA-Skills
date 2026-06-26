const fs = require("fs");
const path = require("path");

function isTraceEnabled(env = process.env) {
  return String(env.CLAWSHIER_TRACE || "").trim() === "1";
}

function traceFilePath(env = process.env) {
  return env.CLAWSHIER_TRACE_FILE || path.resolve(__dirname, "../.clawshier-last-trace.json");
}

function readTrace(env = process.env) {
  const file = traceFilePath(env);
  if (!fs.existsSync(file)) return null;
  return JSON.parse(fs.readFileSync(file, "utf8"));
}

function writeTrace(trace, env = process.env) {
  const file = traceFilePath(env);
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, JSON.stringify(trace, null, 2));
}

function startTraceStep(name, extra = {}) {
  return {
    name,
    startedAt: new Date().toISOString(),
    startMs: Date.now(),
    ...extra,
  };
}

function finishTraceStep(step, extra = {}) {
  return {
    ...step,
    endedAt: new Date().toISOString(),
    durationMs: Date.now() - step.startMs,
    ...extra,
  };
}

module.exports = {
  isTraceEnabled,
  traceFilePath,
  readTrace,
  writeTrace,
  startTraceStep,
  finishTraceStep,
};
