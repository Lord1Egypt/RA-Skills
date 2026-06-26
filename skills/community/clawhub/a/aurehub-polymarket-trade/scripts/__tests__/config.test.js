import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import { mkdtempSync, writeFileSync, rmSync } from 'fs';
import { join } from 'path';
import { tmpdir } from 'os';
import { loadConfig, resolveRpcUrl } from '../lib/config.js';

let dir;
beforeEach(() => { dir = mkdtempSync(join(tmpdir(), 'pm-cfg-')); });
afterEach(() => { rmSync(dir, { recursive: true }); });

describe('loadConfig', () => {
  it('loads .env and polymarket.yaml', () => {
    writeFileSync(join(dir, '.env'), 'WALLET_MODE=wdk\nPOLYGON_RPC_URL=https://example.com\n');
    writeFileSync(join(dir, 'polymarket.yaml'), 'rpc_env: POLYGON_RPC_URL\n');
    const cfg = loadConfig(dir);
    expect(cfg.env.WALLET_MODE).toBe('wdk');
    expect(cfg.yaml.rpc_env).toBe('POLYGON_RPC_URL');
    expect(cfg.configDir).toBe(dir);
  });

  it('returns empty env/yaml when files are missing', () => {
    const cfg = loadConfig(dir);
    expect(cfg.env).toEqual({});
    expect(cfg.yaml).toEqual({});
  });

  it('strips quotes from .env values', () => {
    writeFileSync(join(dir, '.env'), 'KEY="hello world"\n');
    const cfg = loadConfig(dir);
    expect(cfg.env.KEY).toBe('hello world');
  });
});

describe('resolveRpcUrl', () => {
  it('resolves URL from env via rpc_env pointer', () => {
    const cfg = {
      env: { POLYGON_RPC_URL: 'https://polygon-rpc.com' },
      yaml: { rpc_env: 'POLYGON_RPC_URL' },
    };
    expect(resolveRpcUrl(cfg)).toBe('https://polygon-rpc.com');
  });

  it('throws when rpc_env is missing from yaml', () => {
    const cfg = { env: {}, yaml: {} };
    expect(() => resolveRpcUrl(cfg)).toThrow('rpc_env');
  });

  it('throws when env var is not set', () => {
    const cfg = { env: {}, yaml: { rpc_env: 'POLYGON_RPC_URL' } };
    expect(() => resolveRpcUrl(cfg)).toThrow('POLYGON_RPC_URL');
  });
});
