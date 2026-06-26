// Copyright 2026 CRMy Contributors
// SPDX-License-Identifier: Apache-2.0

import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';

export interface CrmyClientConfig {
  serverUrl: string;
  apiKey: string;
}

/** Read config from ~/.crmy/config.json, with env var and plugin-config overrides. */
export function resolveConfig(pluginConfig?: { serverUrl?: string; apiKey?: string }): CrmyClientConfig {
  let fileConfig: { serverUrl?: string; apiKey?: string } = {};
  try {
    const raw = fs.readFileSync(path.join(os.homedir(), '.crmy', 'config.json'), 'utf-8');
    fileConfig = JSON.parse(raw) as typeof fileConfig;
  } catch {
    // File not found — will fail below if no overrides provided
  }

  const serverUrl =
    pluginConfig?.serverUrl ??
    process.env.CRMY_SERVER_URL ??
    fileConfig.serverUrl ??
    'http://localhost:3000';

  const apiKey =
    pluginConfig?.apiKey ??
    process.env.CRMY_API_KEY ??
    fileConfig.apiKey ??
    '';

  return { serverUrl: serverUrl.replace(/\/$/, ''), apiKey };
}

export class CrmyClient {
  private base: string;
  private headers: Record<string, string>;

  constructor(cfg: CrmyClientConfig) {
    this.base = `${cfg.serverUrl}/api/v1`;
    this.headers = {
      'Authorization': `Bearer ${cfg.apiKey}`,
      'Content-Type': 'application/json',
    };
  }

  async get(endpoint: string, params?: Record<string, string | number | undefined>): Promise<unknown> {
    const url = new URL(`${this.base}${endpoint}`);
    if (params) {
      for (const [k, v] of Object.entries(params)) {
        if (v !== undefined && v !== null && v !== '') {
          url.searchParams.set(k, String(v));
        }
      }
    }
    const res = await fetch(url.toString(), { headers: this.headers });
    return this.parse(res);
  }

  async post(endpoint: string, body: unknown): Promise<unknown> {
    const res = await fetch(`${this.base}${endpoint}`, {
      method: 'POST',
      headers: this.headers,
      body: JSON.stringify(body),
    });
    return this.parse(res);
  }

  async patch(endpoint: string, body: unknown): Promise<unknown> {
    const res = await fetch(`${this.base}${endpoint}`, {
      method: 'PATCH',
      headers: this.headers,
      body: JSON.stringify(body),
    });
    return this.parse(res);
  }

  private async parse(res: Response): Promise<unknown> {
    const text = await res.text();
    if (!res.ok) {
      let msg = text;
      try {
        const j = JSON.parse(text) as { error?: string; message?: string };
        msg = j.error ?? j.message ?? text;
      } catch { /* keep raw */ }
      throw new Error(`CRMy API error ${res.status}: ${msg}`);
    }
    try {
      return JSON.parse(text);
    } catch {
      return text;
    }
  }
}
