#!/usr/bin/env node
import { existsSync, mkdirSync, cpSync, writeFileSync, readFileSync } from 'fs'
import { resolve, dirname } from 'path'
import { homedir } from 'os'

const PLUGIN_DIR = resolve(homedir(), '.openclaw/plugins/cc-soul')
const SOURCE = resolve(dirname(new URL(import.meta.url).pathname), '..')

console.log('🧠 cc-soul installing as OpenClaw plugin...')

// 1. Copy plugin files
mkdirSync(resolve(PLUGIN_DIR, 'cc-soul'), { recursive: true })
mkdirSync(resolve(PLUGIN_DIR, 'data'), { recursive: true })
cpSync(resolve(SOURCE, 'cc-soul'), resolve(PLUGIN_DIR, 'cc-soul'), { recursive: true, force: true })
if (existsSync(resolve(SOURCE, 'hub'))) {
  mkdirSync(resolve(PLUGIN_DIR, 'hub'), { recursive: true })
  cpSync(resolve(SOURCE, 'hub'), resolve(PLUGIN_DIR, 'hub'), { recursive: true, force: true })
}

// 2. Copy soul definition files (identity, style, heartbeat)
for (const f of ['soul.json', 'IDENTITY.md', 'STYLE.md', 'HEARTBEAT.md', 'CHANGELOG.md', 'README.md']) {
  const src = resolve(SOURCE, f)
  if (existsSync(src)) {
    cpSync(src, resolve(PLUGIN_DIR, f), { force: true })
  }
}
console.log('   ✅ soul files copied')

// 3. Create package.json (plugin mode)
if (!existsSync(resolve(PLUGIN_DIR, 'package.json'))) {
  writeFileSync(resolve(PLUGIN_DIR, 'package.json'), JSON.stringify({
    name: "cc-soul", version: "3.2.0", type: "module",
    main: "cc-soul/plugin-entry.js",
    openclaw: { extensions: ["./cc-soul/plugin-entry.js"] }
  }, null, 2))
}

// 4. Create openclaw.plugin.json (plugin manifest)
writeFileSync(resolve(PLUGIN_DIR, 'openclaw.plugin.json'), JSON.stringify({
  id: "cc-soul",
  name: "cc-soul",
  description: "Soul layer for OpenClaw — memory, personality, context engine",
  version: "3.2.0",
  configSchema: {}
}, null, 2))

// 5. Create default features
if (!existsSync(resolve(PLUGIN_DIR, 'data/features.json'))) {
  writeFileSync(resolve(PLUGIN_DIR, 'data/features.json'), JSON.stringify({
    memory_active:true, memory_consolidation:true, memory_contradiction_scan:true,
    memory_tags:true, memory_associative_recall:true, memory_predictive:true,
    memory_session_summary:true, memory_core:true, memory_working:true,
    episodic_memory:true, lorebook:true, skill_library:true,
    persona_splitting:true, emotional_contagion:true, emotional_arc:true,
    fingerprint:true, metacognition:true, relationship_dynamics:true,
    intent_anticipation:true, attention_decay:true,
    dream_mode:false, autonomous_goals:true, plan_tracking:true,
    cost_tracker:true,
    smart_forget:true, context_compress:true, cron_agent:true,
    persona_drift:true, persona_drift_detection:true, wal_protocol:true,
    a2a:true, theory_of_mind:true, dag_archive:true,
    rhythm_adaptation:true, trust_annotation:true, self_correction:true,
    predictive_memory:true, scenario_shortcut:true, context_reminder:true,
    auto_memory_reference:true, auto_time_travel:true, auto_natural_citation:true,
    auto_contradiction_hint:true, auto_mood_care:true, auto_daily_review:false,
    auto_topic_save:true, auto_memory_chain:true, auto_repeat_detect:true,
    behavior_prediction:true, absence_detection:true
  }, null, 2))
}

// 6. Update openclaw.json — add plugin load path + allow
try {
  const cfgPath = resolve(homedir(), '.openclaw/openclaw.json')
  if (existsSync(cfgPath)) {
    const cfg = JSON.parse(readFileSync(cfgPath, 'utf-8'))
    if (!cfg.plugins) cfg.plugins = {}
    if (!cfg.plugins.load) cfg.plugins.load = {}
    if (!cfg.plugins.load.paths) cfg.plugins.load.paths = []
    const pluginsDir = resolve(homedir(), '.openclaw/plugins')
    if (!cfg.plugins.load.paths.includes(pluginsDir)) {
      cfg.plugins.load.paths.push(pluginsDir)
    }
    if (!cfg.plugins.allow) cfg.plugins.allow = []
    if (!cfg.plugins.allow.includes('cc-soul')) {
      cfg.plugins.allow.push('cc-soul')
    }
    if (!cfg.plugins.entries) cfg.plugins.entries = {}
    cfg.plugins.entries['cc-soul'] = { enabled: true }
    writeFileSync(cfgPath, JSON.stringify(cfg, null, 2))
    console.log('   ✅ openclaw.json updated')
  }
} catch (e) {
  console.log('   ⚠️  Could not update openclaw.json:', e.message)
}

// 7. Migrate from old hooks location if exists
const OLD_HOOKS = resolve(homedir(), '.openclaw/hooks/cc-soul')
if (existsSync(resolve(OLD_HOOKS, 'data')) && !existsSync(resolve(PLUGIN_DIR, 'data/memories.json'))) {
  try {
    cpSync(resolve(OLD_HOOKS, 'data'), resolve(PLUGIN_DIR, 'data'), { recursive: true })
    console.log('   ✅ Migrated data from hooks/ to plugins/')
  } catch { /* ignore */ }
}

// 8. Auto-start soul-api (background daemon)
import { spawn } from 'child_process'
const API_ENTRY = resolve(PLUGIN_DIR, 'cc-soul', 'soul-api.js')
if (existsSync(API_ENTRY)) {
  try {
    const child = spawn('node', [API_ENTRY], {
      stdio: 'ignore', detached: true,
      env: { ...process.env, SOUL_PORT: process.env.SOUL_PORT || '18800' }
    })
    child.unref()
    console.log(`   ✅ cc-soul API started (port ${process.env.SOUL_PORT || '18800'}, pid ${child.pid})`)
  } catch (e) {
    console.log(`   ⚠️  Could not auto-start API: ${e.message}`)
    console.log('   Run manually: node ' + API_ENTRY)
  }
}

console.log('')
console.log('🎉 cc-soul installed!')
console.log('   Plugin: ~/.openclaw/plugins/cc-soul/')
console.log('   API:    http://localhost:' + (process.env.SOUL_PORT || '18800'))
console.log('')
console.log('   OpenClaw users: just chat normally, cc-soul works in the background.')
console.log('   Other AIs: POST http://localhost:18800/process to get started.')
console.log('')
console.log('   Say "help" or "帮助" to see all commands.')
console.log('')
