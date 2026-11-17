import { readFileSync, writeFileSync, mkdirSync, existsSync } from 'fs'
import { homedir } from 'os'
import { join } from 'path'
import type { Config } from '../types.js'

const CONFIG_DIR = join(homedir(), '.blogizi')
const CONFIG_PATH = join(CONFIG_DIR, 'config.json')

export function getConfig(): Config | null {
  if (!existsSync(CONFIG_PATH)) return null
  try {
    return JSON.parse(readFileSync(CONFIG_PATH, 'utf-8'))
  } catch {
    return null
  }
}

export function saveConfig(config: Config): void {
  mkdirSync(CONFIG_DIR, { recursive: true })
  writeFileSync(CONFIG_PATH, JSON.stringify(config, null, 2))
}

export function requireConfig(): Config {
  const config = getConfig()
  if (!config) {
    console.error('Not authenticated. Run: blogizi auth <api-key>')
    process.exit(1)
  }
  return config
}
