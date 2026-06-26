/**
 * Crusheart AutoBrain Turbo — Plugin Entry
 *
 * Bridges 30+ Python engines into the OpenClaw lifecycle.
 * Universal edition — works on any OpenClaw environment.
 * Features exclusive slot locking (atomic mkdir): only ONE crusheart plugin
 * may be active per workspace.
 */
import { definePluginEntry } from "openclaw/plugin-sdk/plugin-entry";
import { execFile, execSync } from "child_process";
import { join, dirname } from "path";
import {
  writeFileSync, existsSync, mkdirSync, readFileSync,
  unlinkSync, readdirSync, rmdirSync
} from "fs";
import { fileURLToPath } from "url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const WORKSPACE = process.env.OPENCLAW_WORKSPACE ||
  join(process.env.HOME || process.env.USERPROFILE || "/tmp", ".openclaw/workspace");
const PYTHON = process.env.CRUSHEART_PYTHON || "python3";
const BUNDLE = join(__dirname, "bundle", "crusheart-core.tar.gz");
const SKILL_DIR = join(__dirname, "skill");
const PLUGIN_ID = "crusheart-autobrain-turbo";
const PLUGIN_VERSION = "6.3.1";
const LOCK_DIR = join(WORKSPACE, ".crusheart-slot.lock");
const DEPLOY_STATE_PATH = join(WORKSPACE, ".crusheart-deploy-state.json");

// ============================================================
//  Exclusive Slot + Overlap Detection
//  - Atomic mkdir slot lock (prevents multiple crusheart instances)
//  - Scans openclaw plugins list for overlapping functionality
//  - Blocks install if conflicting plugin is detected
// ============================================================
const OVERLAP_KEYWORDS = [
  "memory", "anti-hallucination", "anti.fake", "self.evolution",
  "self-evolution", "workflow.orchestrator", "orch", "judge",
  "failover", "circuit.breaker", "autobrain", "brain"
];

function checkConflictingPlugins() {
  try {
    const listOut = execSync("openclaw plugins list 2>/dev/null", { timeout: 10000 });
    const lines = listOut.toString().split("\n").filter(l => l.trim());
    const conflicts = [];
    for (const line of lines) {
      const pluginName = line.toLowerCase().trim();
      // Skip ourselves
      if (pluginName.includes("crusheart-autobrain-turbo")) continue;
      // Check for functionality overlap
      for (const keyword of OVERLAP_KEYWORDS) {
        const re = new RegExp(keyword.replace(/\./g, "[ ._-]"));
        if (re.test(pluginName)) {
          conflicts.push(line.trim());
          break;
        }
      }
    }
    return conflicts;
  } catch {
    // openclaw CLI not available yet (first install) — skip
    return [];
  }
}

function acquireSlot() {
  const info = JSON.stringify({
    plugin: PLUGIN_ID,
    version: PLUGIN_VERSION,
    acquiredAt: Date.now(),
    pid: process.pid
  }, null, 2);

  // 1. Check for conflicting plugins with overlapping functionality
  const conflicts = checkConflictingPlugins();
  if (conflicts.length > 0) {
    return {
      ok: false,
      reason: `检测到功能重叠的插件: ${conflicts.join(", ")}\n` +
        `灵枢 AutoBrain Turbo 已包含记忆、防幻觉、自进化、工作流编排、错误隔离等完整能力。\n` +
        `请先卸载冲突插件后再安装本插件。`
    };
  }

  // 2. Acquire atomic slot lock
  try {
    mkdirSync(LOCK_DIR);
    writeFileSync(join(LOCK_DIR, "info.json"), info, "utf-8");
    return { ok: true };
  } catch (e) {
    if (e.code === 'EEXIST') {
      try {
        const existing = JSON.parse(readFileSync(join(LOCK_DIR, "info.json"), "utf-8"));
        if (existing.plugin === PLUGIN_ID) return { ok: true, slot: existing };
        return {
          ok: false,
          reason: `插件槽已被 "${existing.plugin}" (v${existing.version}) 占用。` +
            `一个 workspace 只能激活一个功能重叠的插件。` +
            `如需更换请先卸载旧插件，或手动删除 ${LOCK_DIR}。`
        };
      } catch {
        return { ok: false, reason: "插件槽锁损坏，请手动删除 .crusheart-slot.lock/。" };
      }
    }
    return { ok: false, reason: `获取插件槽失败: ${e.message}` };
  }
}

function releaseSlot() {
  const infoPath = join(LOCK_DIR, "info.json");
  if (!existsSync(infoPath)) return;
  try {
    const existing = JSON.parse(readFileSync(infoPath, "utf-8"));
    if (existing.plugin === PLUGIN_ID) {
      unlinkSync(infoPath);
      rmdirSync(LOCK_DIR);
    }
  } catch { /* best effort */ }
}

// ============================================================
//  Workspace Helpers
// ============================================================
const ENGINE_GROUPS = [
  "init", "memory", "quality", "operations",
  "workflow", "hooks", "tools", "compat"
];

function resolveScript(script) {
  const direct = join(WORKSPACE, script);
  if (existsSync(direct)) return direct;
  for (const g of ENGINE_GROUPS) {
    const p = join(WORKSPACE, "core/engines", g, script);
    if (existsSync(p)) return p;
  }
  const scriptsP = join(WORKSPACE, "scripts", script);
  if (existsSync(scriptsP)) return scriptsP;
  const bundleP = join(__dirname, "bundle", script);
  if (existsSync(bundleP)) return bundleP;
  return join(WORKSPACE, "scripts", script);
}

function runPyWithResult(script, args = []) {
  // Same as runPy but always resolves from bundle if not yet deployed
  const candidates = [
    join(WORKSPACE, script),
    join(WORKSPACE, "scripts", script),
    join(__dirname, "bundle", script),
  ];
  for (const g of ENGINE_GROUPS) {
    candidates.push(join(WORKSPACE, "core/engines", g, script));
  }
  let p = null;
  for (const c of candidates) {
    if (existsSync(c)) { p = c; break; }
  }
  if (!p) {
    console.warn(`[${PLUGIN_ID}] Script not found: ${script}`);
    return Promise.resolve({ stdout: "", stderr: "" });
  }
  return new Promise(resolve => {
    execFile(PYTHON, [p, ...args], {
      cwd: WORKSPACE, timeout: 60000, maxBuffer: 1024 * 1024
    }, (err, stdout, stderr) => {
      if (err) console.warn(`[${PLUGIN_ID}] runPy error for ${script}: ${err.message.slice(0, 200)}`);
      resolve({
        stdout: stdout?.trim() || "",
        stderr: err?.message?.slice(0, 200) || stderr?.trim() || ""
      });
    });
  });
}

function runPy(script, args = []) {
  return new Promise(resolve => {
    const p = resolveScript(script);
    if (!existsSync(p)) {
      console.warn(`[${PLUGIN_ID}] Script not found: ${p}`);
      return resolve({ stdout: "", stderr: "" });
    }
    execFile(PYTHON, [p, ...args], {
      cwd: WORKSPACE, timeout: 30000, maxBuffer: 1024 * 1024
    }, (err, stdout, stderr) => {
      if (err) console.warn(`[${PLUGIN_ID}] runPy error for ${script}: ${err.message.slice(0, 200)}`);
      resolve({
        stdout: stdout?.trim() || "",
        stderr: err?.message?.slice(0, 200) || stderr?.trim() || ""
      });
    });
  });
}

// ============================================================
//  Native JS capsule save (no Python spawn, includes context)
// ============================================================
function saveCapsule(context) {
  const capsule = {
    last_saved: new Date().toISOString(),
    status: "ok",
    message_preview: context?.message?.text?.slice(0, 200) || ""
  };
  const capsuleFile = join(WORKSPACE, ".context_capsule.json");
  try {
    writeFileSync(capsuleFile, JSON.stringify(capsule, null, 2), "utf-8");
  } catch (e) {
    console.warn(`[${PLUGIN_ID}] Failed to save capsule: ${e.message}`);
  }
}

// ============================================================
//  Dynamic Channel Detection
// ============================================================
function detectChannels() {
  const channels = [];
  try {
    const configDir = process.env.OPENCLAW_CONFIG_DIR ||
      join(process.env.HOME || process.env.USERPROFILE || "/tmp", ".openclaw");
    for (const cf of ["openclaw.json", "channel-config.json", "channels.json"]) {
      const fp = join(configDir, cf);
      if (!existsSync(fp)) continue;
      try {
        const raw = JSON.parse(readFileSync(fp, "utf-8"));
        const walk = (obj, depth = 0) => {
          if (depth > 8 || !obj || typeof obj !== 'object') return;
          for (const [k, v] of Object.entries(obj)) {
            if ((k === 'channel' || k === 'id') && typeof v === 'string' && v && !channels.includes(v)) {
              channels.push(v);
            } else if (typeof v === 'object') walk(v, depth + 1);
          }
        };
        walk(raw);
      } catch { /* skip */ }
    }
  } catch { /* best effort */ }
  if (channels.length === 0) channels.push("default");
  return channels;
}

// ============================================================
//  Deploy Engines, Scripts & Skill
// ============================================================
async function deploy() {
  // 1. Decompress engine bundle to workspace core/
  if (existsSync(BUNDLE)) {
    try {
      execSync(`tar xzf "${BUNDLE}" -C "${WORKSPACE}" 2>/dev/null`, { timeout: 30000 });
    } catch { /* partial deploy OK */ }
  }

  // 2. Copy skill metadata
  if (existsSync(SKILL_DIR)) {
    const t = join(WORKSPACE, "skills", "Crusheart-AutoBrain-Turbo");
    if (!existsSync(t)) mkdirSync(t, { recursive: true });
    for (const f of ["SKILL.md", "_meta.json"]) {
      const s = join(SKILL_DIR, f);
      if (existsSync(s)) writeFileSync(join(t, f), readFileSync(s, "utf-8"), "utf-8");
    }
  }

  // 3. Deploy bundle scripts & guide to workspace
  const BUNDLE_SCRIPTS = [
    "auto_save_capsule.py",
    "daily_maintenance.py",
    "version_check.py",
    "scan_memory.py",
    "scan_skills.py",
    "read_config.py",
    "init_correction_data.py",
    "register_crons.sh",
    "install_wizard.py",
    "INSTALL_GUIDE.md"
  ];
  const bundleDir = join(__dirname, "bundle");
  for (const s of BUNDLE_SCRIPTS) {
    const src = join(bundleDir, s);
    if (existsSync(src)) {
      try {
        writeFileSync(join(WORKSPACE, "scripts", s), readFileSync(src, "utf-8"), "utf-8");
      } catch (e) {
        console.error(`[${PLUGIN_ID}] Failed to deploy ${s}: ${e.message}`);
      }
    }
  }

  // 4. Inject crusheart presence marker (NOT overwrite SOUL.md)
  const soulPath = join(WORKSPACE, "SOUL.md");
  const markerPath = join(WORKSPACE, ".crusheart-injected.md");
  if (existsSync(soulPath)) {
    const marker = [
      "<!-- Crusheart AutoBrain injection marker -->",
      `- Injected: ${new Date().toISOString()}`,
      "- See scripts/ for bundled maintenance tools"
    ].join("\n") + "\n";
    writeFileSync(markerPath, marker, "utf-8");
  } else {
    const soulSrc = join(bundleDir, "SOUL.md");
    if (existsSync(soulSrc)) {
      writeFileSync(soulPath, readFileSync(soulSrc, "utf-8"), "utf-8");
    }
  }

  // 5. First-install: run install wizard (compatibility check + init)
  let deployState = {};
  try {
    if (existsSync(DEPLOY_STATE_PATH)) {
      deployState = JSON.parse(readFileSync(DEPLOY_STATE_PATH, "utf-8"));
    }
  } catch { /* fresh state */ }

  if (!deployState.firstRunDone) {
    // Phase 1: Compatibility check
    console.log(`\n[${PLUGIN_ID}] ════════════════════════════════════════════`);
    console.log(`[${PLUGIN_ID}]  🦞 灵枢 AutoBrain Turbo v${PLUGIN_VERSION} — 安装向导`);
    console.log(`[${PLUGIN_ID}] ════════════════════════════════════════════`);
    console.log(`[${PLUGIN_ID}] 📋 Phase 1: 兼容性检查...`);
    
    const compatRs = await runPyWithResult("install_wizard.py", ["--check"]);
    let compat = { blocked: false, warnings: [] };
    try { compat = JSON.parse(compatRs.stdout || "{}"); } catch {}
    
    if (compat.blocked) {
      console.error(`[${PLUGIN_ID}] ❌ 兼容性检查未通过，无法安装：`);
      for (const w of (compat.warnings || [])) {
        console.error(`[${PLUGIN_ID}]    - ${w}`);
      }
      console.log(`[${PLUGIN_ID}] 📖 请查阅 bundle/INSTALL_GUIDE.md 了解兼容性要求`);
      throw new Error("Compatibility check failed. See warnings above.");
    }
    
    console.log(`[${PLUGIN_ID}] ✅ 环境检查通过`);
    
    // Phase 2: Full initialization
    console.log(`[${PLUGIN_ID}] 📋 Phase 2: 正在初始化...`);
    const initRs = await runPyWithResult("install_wizard.py", ["--init"]);
    let init = { status: "error", steps: {}, summary: {} };
    try { init = JSON.parse(initRs.stdout || "{}"); } catch {}
    
    if (init.status === "ok" || init.status === "partial") {
      console.log(`[${PLUGIN_ID}] ✅ 初始化${init.status === "ok" ? "完成" : "部分完成"}`);
      const summary = init.summary || {};
      for (const [step, status] of Object.entries(summary)) {
        console.log(`[${PLUGIN_ID}]    ${step}: ${status}`);
      }
    } else {
      console.warn(`[${PLUGIN_ID}] ⚠️ 初始化状态: ${init.status}`);
    }
    
    deployState.firstRunDone = true;
    deployState.initStatus = init.status;
    try {
      writeFileSync(DEPLOY_STATE_PATH, JSON.stringify(deployState, null, 2), "utf-8");
    } catch { /* best effort */ }
  } else {
    // Subsequent installs: quick engine scan only
    console.log(`[${PLUGIN_ID}] 📋 快速部署（非首次）: 扫描引擎...`);
    await runPy("install_wizard.py", ["--status"]);
  }

  // 6. For non-first install: ensure cron tasks are registered
  if (deployState.firstRunDone) {
    await runPy("task_scheduler.py", ["--register-crons"]);
  }

  // 7. Always scan & register engines
  await runPy("auto_engines.py", ["scan"]);
}

// ============================================================
//  Plugin Registration
// ============================================================
export default definePluginEntry({
  id: PLUGIN_ID,
  name: "灵枢 AutoBrain",
  description: "Plugin+skill hybrid pack: memory, anti-hallucination, self-evolution, workflow orchestration, daily maintenance, auto-scan, version check. Exclusive slot + compat layer.",

  async onLoad() {
    const slot = acquireSlot();
    if (!slot.ok) {
      console.error(`[${PLUGIN_ID}] ${slot.reason}`);
      throw new Error(slot.reason);
    }
    await deploy();
  },

  async onUnload() {
    releaseSlot();
  },

  hooks: {
    "agent:bootstrap": [{
      id: "crusheart-init",
      priority: 100,
      async handler() {
        const initRs = await runPy("init_engines.py", ["--bootstrap"]);
        const modeRs = await runPy("dual_mode_classifier.py", ["--init"]);
        return {
          engines: { status: "ok", detail: initRs.stdout?.slice(0, 200) },
          mode: modeRs.stdout?.slice(0, 100) || "auto"
        };
      }
    }],

    "message:received": [
      {
        id: "crusheart-mode",
        priority: 50,
        async handler(ctx) {
          if (!ctx?.message?.text) return { mode: "auto" };
          const r = await runPy("dual_mode_classifier.py", [ctx.message.text]);
          try {
            return { mode: JSON.parse(r.stdout || "{}").mode || "auto" };
          } catch {
            return { mode: r.stdout || "auto" };
          }
        }
      },
      {
        id: "crusheart-capsule",
        priority: 10,
        async handler(ctx) {
          saveCapsule(ctx);
          return { status: "ok" };
        }
      }
    ],

    "message:preprocessed": [{
      id: "crusheart-anti-fake",
      priority: 100,
      async handler(ctx) {
        if (!ctx?.message?.text) return { blocked: false };
        const r = await runPy("anti_fake_validator.py", [ctx.message.text]);
        return { blocked: (r.stdout || "").includes("[BLOCKED]") };
      }
    }],

    "message:sent": [
      {
        id: "crusheart-post",
        priority: 50,
        async handler(ctx) {
          saveCapsule(ctx);
          return {};
        }
      },
      {
        id: "crusheart-evolve",
        priority: 10,
        async handler() {
          await runPy("self_evolution_v3.py", ["--evaluate-turn"]);
          return {};
        }
      }
    ]
  }
});
