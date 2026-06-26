import { describe, it, expect, vi } from 'vitest';
import { mkdtempSync, writeFileSync, rmSync } from 'fs';
import { join } from 'path';
import { tmpdir } from 'os';

// Mock the clob-client to avoid real network calls
vi.mock('@polymarket/clob-client', () => {
  class MockClobClient {
    constructor(host, chainId, signer, creds, sigType, addr) {
      this.host = host;
      this.chainId = chainId;
      this.signer = signer;
      this.creds = creds;
      this.sigType = sigType;
      this.addr = addr;
    }
  }

  return {
    ClobClient: MockClobClient,
    SignatureType: { EOA: 0 },
  };
});

import { createL1Client, createL2Client, loadClobCreds } from '../lib/clob.js';

const mockCfg = {
  yaml: {
    polymarket: { clob_url: 'https://clob.polymarket.com', chain_id: 137 },
  },
};
const mockWallet = { address: '0xDeAdBeEf' };

describe('createL1Client', () => {
  it('creates ClobClient with wallet only (no creds)', async () => {
    const client = await createL1Client(mockCfg, mockWallet);
    expect(client.host).toBe('https://clob.polymarket.com');
    expect(client.chainId).toBe(137);
    expect(client.creds).toBeUndefined();
  });
});

describe('loadClobCreds', () => {
  it('loads credentials from .polymarket_clob file', () => {
    const dir = mkdtempSync(join(tmpdir(), 'pm-creds-'));
    try {
      const creds = { key: 'k', secret: 's', passphrase: 'p' };
      writeFileSync(join(dir, '.polymarket_clob'), JSON.stringify(creds));
      const loaded = loadClobCreds(join(dir, '.polymarket_clob'));
      expect(loaded.key).toBe('k');
      expect(loaded.secret).toBe('s');
    } finally {
      rmSync(dir, { recursive: true });
    }
  });

  it('throws with clear error when creds file is missing', () => {
    expect(() => loadClobCreds('/nonexistent/.polymarket_clob')).toThrow('not found');
  });

  it('throws with corruption error when creds file contains invalid JSON', () => {
    const dir = mkdtempSync(join(tmpdir(), 'pm-creds-'));
    try {
      writeFileSync(join(dir, '.polymarket_clob'), '{ bad json }');
      expect(() => loadClobCreds(join(dir, '.polymarket_clob'))).toThrow('corrupted');
    } finally {
      rmSync(dir, { recursive: true });
    }
  });
});

describe('createL2Client', () => {
  it('creates ClobClient with full L2 auth', async () => {
    const dir = mkdtempSync(join(tmpdir(), 'pm-creds-'));
    try {
      writeFileSync(join(dir, '.polymarket_clob'),
        JSON.stringify({ key: 'k', secret: 's', passphrase: 'p' }));
      const client = await createL2Client(mockCfg, mockWallet, join(dir, '.polymarket_clob'));
      expect(client.creds).toEqual({ key: 'k', secret: 's', passphrase: 'p' });
      expect(client.addr).toBe('0xDeAdBeEf');
    } finally {
      rmSync(dir, { recursive: true });
    }
  });
});
