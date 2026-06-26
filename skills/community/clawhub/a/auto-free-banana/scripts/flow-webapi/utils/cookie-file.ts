import fs from 'node:fs';
import path from 'node:path';
import { mkdir, readFile, writeFile } from 'node:fs/promises';

import { resolveFlowWebCookiePath } from './paths.js';

export type CookieMap = Record<string, string>;

export type FlowCookieFileData = {
  version: number;
  updatedAt: string;
  accessToken: string;
  cookies: CookieMap;
  source?: string;
};

export async function read_cookie_file(p: string = resolveFlowWebCookiePath()): Promise<FlowCookieFileData | null> {
  try {
    if (!fs.existsSync(p) || !fs.statSync(p).isFile()) return null;
    const raw = await readFile(p, 'utf8');
    const data = JSON.parse(raw) as unknown;

    if (data && typeof data === 'object' && 'accessToken' in (data as any)) {
      const d = data as FlowCookieFileData;
      if (typeof d.accessToken === 'string' && d.accessToken.startsWith('ya29.')) {
        return d;
      }
    }

    return null;
  } catch {
    return null;
  }
}

export async function write_cookie_file(
  accessToken: string,
  cookies: CookieMap,
  p: string = resolveFlowWebCookiePath(),
  source?: string,
): Promise<void> {
  const dir = path.dirname(p);
  await mkdir(dir, { recursive: true });

  const payload: FlowCookieFileData = {
    version: 1,
    updatedAt: new Date().toISOString(),
    accessToken,
    cookies,
    source,
  };
  await writeFile(p, JSON.stringify(payload, null, 2), 'utf8');
}

export const readCookieFile = read_cookie_file;
export const writeCookieFile = write_cookie_file;
