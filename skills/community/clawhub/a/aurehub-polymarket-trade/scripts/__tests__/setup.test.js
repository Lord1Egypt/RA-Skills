import { describe, it, expect } from 'vitest';
import { mkdtempSync, writeFileSync, rmSync, mkdirSync } from 'fs';
import { join } from 'path';
import { tmpdir } from 'os';
import { checkEnvFile, checkVaultFile, checkClobCreds, checkNodeModules, checkPasswordFile, checkConfigFile } from '../setup.js';

let dir;
function setup() { dir = mkdtempSync(join(tmpdir(), 'pm-setup-')); }
function teardown() { rmSync(dir, { recursive: true }); }

describe('checkEnvFile', () => {
  it('passes when .env exists', () => {
    setup();
    try {
      writeFileSync(join(dir, '.env'), 'POLYGON_RPC_URL=https://polygon-rpc.com\n');
      expect(() => checkEnvFile(dir)).not.toThrow();
    } finally { teardown(); }
  });

  it('throws when .env is missing', () => {
    setup();
    try {
      expect(() => checkEnvFile(dir)).toThrow('.env');
    } finally { teardown(); }
  });

  it('does not require WALLET_MODE=wdk', () => {
    setup();
    try {
      writeFileSync(join(dir, '.env'), 'POLYGON_RPC_URL=https://polygon-rpc.com\n');
      expect(() => checkEnvFile(dir)).not.toThrow();
    } finally { teardown(); }
  });
});

describe('checkVaultFile', () => {
  it('passes when .wdk_vault exists', () => {
    setup();
    try {
      writeFileSync(join(dir, '.wdk_vault'), '{}');
      expect(() => checkVaultFile(dir)).not.toThrow();
    } finally { teardown(); }
  });

  it('throws when .wdk_vault is missing', () => {
    setup();
    try {
      expect(() => checkVaultFile(dir)).toThrow('.wdk_vault');
    } finally { teardown(); }
  });
});

describe('checkClobCreds', () => {
  it('returns true when .polymarket_clob exists', () => {
    setup();
    try {
      writeFileSync(join(dir, '.polymarket_clob'), '{"key":"k"}');
      expect(checkClobCreds(dir)).toBe(true);
    } finally { teardown(); }
  });

  it('returns false (no throw) when missing — caller decides to derive', () => {
    setup();
    try {
      expect(checkClobCreds(dir)).toBe(false);
    } finally { teardown(); }
  });
});

describe('checkPasswordFile', () => {
  it('passes when .wdk_password exists', () => {
    setup();
    try {
      writeFileSync(join(dir, '.wdk_password'), 'secret');
      expect(() => checkPasswordFile(dir)).not.toThrow();
    } finally { teardown(); }
  });

  it('throws when .wdk_password is missing', () => {
    setup();
    try {
      expect(() => checkPasswordFile(dir)).toThrow('.wdk_password');
    } finally { teardown(); }
  });
});

describe('checkConfigFile', () => {
  it('passes when polymarket.yaml exists', () => {
    setup();
    try {
      writeFileSync(join(dir, 'polymarket.yaml'), 'rpc: http://localhost');
      expect(() => checkConfigFile(dir)).not.toThrow();
    } finally { teardown(); }
  });

  it('throws when polymarket.yaml is missing', () => {
    setup();
    try {
      expect(() => checkConfigFile(dir)).toThrow('polymarket.yaml');
    } finally { teardown(); }
  });
});

describe('checkNodeModules', () => {
  it('passes when node_modules exists', () => {
    setup();
    try {
      mkdirSync(join(dir, 'node_modules'));
      expect(() => checkNodeModules(dir)).not.toThrow();
    } finally { teardown(); }
  });

  it('throws with install hint when node_modules is missing', () => {
    setup();
    try {
      expect(() => checkNodeModules(dir)).toThrow('npm install');
    } finally { teardown(); }
  });
});
