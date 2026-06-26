import { join, dirname } from 'path';
import { fileURLToPath, pathToFileURL } from 'url';
import { existsSync } from 'fs';

const __here = dirname(fileURLToPath(import.meta.url));

export const SKILL_ROOT  = join(__here, '..');
export const SCRIPTS     = __here;
export const SCRIPTS_URL = pathToFileURL(__here + '/').href;

/** OpenClaw workspace 根目录 */
function findWorkspace() {
  const candidates = [
    join(process.env.USERPROFILE || '', '.openclaw', 'workspace'),
    join(process.env.HOME || '',         '.openclaw', 'workspace'),
  ];
  for (const p of candidates) if (existsSync(p)) return p;
  return candidates[0]; // 兜底
}

export const WORKSPACE   = process.env.OPENCLAW_WORKSPACE || findWorkspace();
export const SOUL_FILE   = join(WORKSPACE, 'SOUL.md');
export const MEMORY_FILE = join(WORKSPACE, 'MEMORY.md');

/**
 * character.json 存放在 workspace/claw-rpg/ 下，而非 skill 目錄。
 * 這樣重裝 skill 不會清零存檔。
 */
export const DATA_DIR       = join(WORKSPACE, 'claw-rpg');
export const CHARACTER_FILE = join(DATA_DIR, 'character.json');
