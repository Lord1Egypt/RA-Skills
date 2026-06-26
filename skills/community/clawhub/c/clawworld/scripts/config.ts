/**
 * Config management for the ClawWorld skill.
 * Reads and writes ~/.openclaw/clawworld/config.json.
 * This file is created by bind.sh during the bind flow and
 * read by the OpenClaw plugin for status/activity reporting.
 */

import * as fs from 'fs';
import * as path from 'path';

export interface ClawWorldConfig {
  deviceToken: string;
  endpoint: string;
  lobsterId: string;
  instanceId: string;
}

const CONFIG_DIR = path.join(
  process.env.HOME || '~',
  '.openclaw',
  'clawworld'
);
const CONFIG_FILE = path.join(CONFIG_DIR, 'config.json');

export function readConfig(): ClawWorldConfig | null {
  try {
    const raw = fs.readFileSync(CONFIG_FILE, 'utf-8').replace(/^\uFEFF/, '');
    return JSON.parse(raw) as ClawWorldConfig;
  } catch {
    return null; // Not bound yet
  }
}

export function writeConfig(config: ClawWorldConfig): void {
  fs.mkdirSync(CONFIG_DIR, { recursive: true });
  fs.writeFileSync(CONFIG_FILE, JSON.stringify(config, null, 2), 'utf-8');
}

export function deleteConfig(): void {
  try {
    fs.rmSync(CONFIG_FILE);
  } catch {
    // Already gone — no-op
  }
}
