// Token scanner — reads local credential files from supported Figma MCP clients.
// Pure file I/O, no network calls. Separated from network code for security scanners.

import { readFileSync, existsSync } from 'fs';
import { homedir } from 'os';
import { join } from 'path';

const HOME = homedir();

/**
 * Scan known credential stores for a Figma MCP token.
 * Returns { token, refreshToken, clientId, clientSecret, expiresAt, source } or null.
 */
export function scanForFigmaToken() {
  // 1. Claude Code
  const claudePath = join(HOME, '.claude', '.credentials.json');
  if (existsSync(claudePath)) {
    try {
      const creds = JSON.parse(readFileSync(claudePath, 'utf8'));
      const mcpOAuth = creds.mcpOAuth || {};
      for (const [key, val] of Object.entries(mcpOAuth)) {
        if (key.includes('figma') && val?.accessToken) {
          return {
            token: val.accessToken,
            refreshToken: val.refreshToken || null,
            clientId: val.clientId || null,
            clientSecret: val.clientSecret || null,
            expiresAt: val.expiresAt || null,
            source: 'Claude Code',
            file: claudePath,
            key,
          };
        }
      }
    } catch { /* skip */ }
  }

  // 2. Codex
  const codexPath = join(HOME, '.codex', 'auth.json');
  if (existsSync(codexPath)) {
    try {
      const auth = JSON.parse(readFileSync(codexPath, 'utf8'));
      const figma = auth.figma || auth['mcp:figma'];
      if (figma?.accessToken) {
        return {
          token: figma.accessToken,
          refreshToken: figma.refreshToken || null,
          clientId: figma.clientId || null,
          clientSecret: figma.clientSecret || null,
          expiresAt: figma.expiresAt || null,
          source: 'Codex',
          file: codexPath,
        };
      }
    } catch { /* skip */ }
  }

  // 3. Windsurf
  const windsurfPath = join(HOME, '.codeium', 'windsurf', 'mcp_config.json');
  if (existsSync(windsurfPath)) {
    try {
      const config = JSON.parse(readFileSync(windsurfPath, 'utf8'));
      const figma = config?.mcpServers?.figma;
      const token = figma?.env?.FIGMA_TOKEN || figma?.headers?.Authorization?.replace('Bearer ', '');
      if (token) {
        return { token, refreshToken: null, clientId: null, clientSecret: null, expiresAt: null, source: 'Windsurf', file: windsurfPath };
      }
    } catch { /* skip */ }
  }

  return null;
}

/**
 * Read and parse openclaw.json from known locations.
 * Returns { config, configPath } or null.
 */
export function readOpenClawConfig() {
  const HOME = homedir();
  const candidates = [
    join(HOME, '.openclaw', 'openclaw.json'),
    join(HOME, '.config', 'openclaw', 'openclaw.json'),
  ];
  for (const p of candidates) {
    if (existsSync(p)) {
      try { return { config: JSON.parse(readFileSync(p, 'utf8')), configPath: p }; } catch { /* try next */ }
    }
  }
  return null;
}
