#!/usr/bin/env node
import { existsSync, readFileSync, writeFileSync } from 'fs'
import { resolve } from 'path'
import { homedir } from 'os'
const D = resolve(homedir(), '.openclaw/plugins/cc-soul/data')
const F = resolve(D, 'features.json')
const load = (p, f) => { try { return existsSync(p) ? JSON.parse(readFileSync(p,'utf-8')) : f } catch { return f } }
const [,,cmd,...args] = process.argv
if (cmd === 'status') {
  const f = load(F, {})
  console.log('\n🧠 cc-soul features:\n')
  for (const [k,v] of Object.entries(f)) { if (!k.startsWith('_')) console.log(`  ${v?'✅':'❌'} ${k}`) }
} else if (cmd === 'enable' && args[0]) {
  const f = load(F, {}); f[args[0]] = true; writeFileSync(F, JSON.stringify(f,null,2))
  console.log(`✅ ${args[0]} enabled.`)
} else if (cmd === 'disable' && args[0]) {
  const f = load(F, {}); f[args[0]] = false; writeFileSync(F, JSON.stringify(f,null,2))
  console.log(`❌ ${args[0]} disabled.`)
} else {
  console.log(`🧠 cc-soul v2.5.0 — Your AI, but it actually knows you\n\n  cc-soul status              Show all features\n  cc-soul enable <feature>    Enable a feature\n  cc-soul disable <feature>   Disable a feature\n\nDocs: https://github.com/wenroudeyu-collab/cc-soul-docs`)
}
