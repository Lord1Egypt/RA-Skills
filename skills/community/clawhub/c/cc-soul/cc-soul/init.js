let _initialized = false;
function getInitialized() {
  return _initialized;
}
function setInitialized(v) {
  _initialized = v;
}
function initializeSoul() {
  if (_initialized) return;
  _initialized = true;
  try {
    require("./persistence.ts").ensureDataDir();
  } catch {
  }
  try {
    require("./cli.ts").loadAIConfig();
  } catch {
  }
  try {
    require("./body.ts").loadBodyState();
  } catch {
  }
  try {
    require("./memory.ts").ensureSQLiteReady();
  } catch (e) {
    console.error("[cc-soul] SQLite init failed:", e.message);
  }
  try {
    require("./features.ts").loadFeatures();
  } catch {
  }
  try {
    require("./handler-state.ts").loadStats();
  } catch {
  }
  try {
    require("./user-profiles.ts").loadProfiles();
  } catch {
  }
  try {
    require("./distill.ts").loadDistillState();
  } catch {
  }
  try {
    require("./absence-detection.ts").loadAbsenceState();
  } catch {
  }
  console.log(`[cc-soul] initializeSoul done (from init.ts)`);
}
export {
  getInitialized,
  initializeSoul,
  setInitialized
};
