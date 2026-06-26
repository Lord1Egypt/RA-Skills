import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import { writeFileSync, mkdirSync, rmSync } from 'fs';
import { join } from 'path';
import { tmpdir } from 'os';
import { loadConfig } from '../lib/config.js';

describe('loadConfig', () => {
  let tmpDir;

  beforeEach(() => {
    tmpDir = join(tmpdir(), `hl-config-test-${Date.now()}`);
    mkdirSync(tmpDir, { recursive: true });
  });

  afterEach(() => {
    rmSync(tmpDir, { recursive: true, force: true });
  });

  it('reads WALLET_MODE from .env', () => {
    writeFileSync(join(tmpDir, '.env'), 'WALLET_MODE=wdk\nWDK_PASSWORD_FILE=~/.aurehub/.wdk_password\n');
    const cfg = loadConfig(tmpDir);
    expect(cfg.env.WALLET_MODE).toBe('wdk');
    expect(cfg.env.WDK_PASSWORD_FILE).toBe('~/.aurehub/.wdk_password');
  });

  it('reads risk thresholds from hyperliquid.yaml', () => {
    writeFileSync(join(tmpDir, 'hyperliquid.yaml'), 'risk:\n  confirm_trade_usd: 50\n  large_trade_usd: 500\n  leverage_warn: 10\n');
    const cfg = loadConfig(tmpDir);
    expect(cfg.yaml.risk.confirm_trade_usd).toBe(50);
    expect(cfg.yaml.risk.large_trade_usd).toBe(500);
  });

  it('reads slippage_pct from hyperliquid.yaml as a number', () => {
    writeFileSync(join(tmpDir, 'hyperliquid.yaml'), 'risk:\n  slippage_pct: 2\n');
    const cfg = loadConfig(tmpDir);
    expect(cfg.yaml.risk.slippage_pct).toBe(2);
    expect(typeof cfg.yaml.risk.slippage_pct).toBe('number');
  });

  it('returns empty objects when files are missing', () => {
    const cfg = loadConfig(tmpDir);
    expect(cfg.env).toEqual({});
    expect(cfg.yaml).toEqual({});
  });

  it('strips quotes from .env values', () => {
    writeFileSync(join(tmpDir, '.env'), 'WALLET_MODE="wdk"\n');
    const cfg = loadConfig(tmpDir);
    expect(cfg.env.WALLET_MODE).toBe('wdk');
  });

  it('ignores comment lines in .env', () => {
    writeFileSync(join(tmpDir, '.env'), '# this is a comment\nWALLET_MODE=wdk\n');
    const cfg = loadConfig(tmpDir);
    expect(cfg.env.WALLET_MODE).toBe('wdk');
    expect(Object.keys(cfg.env)).toHaveLength(1);
  });
});
