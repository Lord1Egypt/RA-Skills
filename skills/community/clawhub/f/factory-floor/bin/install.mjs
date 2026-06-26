#!/usr/bin/env node
import { cpSync, mkdirSync } from 'fs'
import { execSync } from 'child_process'
import { resolve, dirname, join } from 'path'
import { fileURLToPath } from 'url'
import { homedir } from 'os'

const __dirname = dirname(fileURLToPath(import.meta.url))
const pkgRoot = resolve(__dirname, '..')
const target = join(homedir(), '.claude', 'skills', 'factory-floor')

console.log('Installing Factory Floor skill...\n')

// Copy skill files
mkdirSync(join(target, 'references'), { recursive: true })
mkdirSync(join(target, 'stages'), { recursive: true })
mkdirSync(join(target, 'scripts'), { recursive: true })

const files = [
  'SKILL.md',
  'references/intake.md',
  'references/misdiagnoses.md',
  'references/coaching-patterns.md',
  'references/pillar-goldratt.md',
  'references/pillar-maurya.md',
  'references/pillar-sharp.md',
  'references/pillar-ritson.md',
  'references/estimation.md',
  'references/jtbd.md',
  'references/weekly-review.md',
  'references/pillar-strategy.md',
  'references/weekly-diagrams.md',
  'stages/pre-revenue.md',
  'stages/restart.md',
  'stages/growth.md',
  'stages/scaling.md',
  'scripts/render-diagram.mjs',
  'scripts/package.json',
]

for (const file of files) {
  try {
    cpSync(join(pkgRoot, file), join(target, file))
  } catch (err) {
    console.error(`  Failed to copy ${file}: ${err.message}`)
    process.exit(1)
  }
}

// Install diagram renderer dependencies
console.log('Installing diagram renderer...')
try {
  execSync('npm install --silent', { cwd: join(target, 'scripts'), stdio: 'inherit' })
} catch (err) {
  console.error(`  Failed to install diagram renderer: ${err.message}`)
  process.exit(1)
}

console.log(`\n  Installed to ${target}\n`)
console.log('The skill triggers automatically when you ask Claude Code about')
console.log('prioritisation, bottlenecks, weekly reviews, or what to work on next.')
