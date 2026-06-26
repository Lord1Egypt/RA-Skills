/**
 * Test Setup and Utilities
 * Common configuration and helpers for all tests
 */

import { jest } from '@jest/globals';

// Extend Jest timeout for integration tests
jest.setTimeout(30000);

// Test constants
export const TEST_PASSWORD = 'test-password-123456';
export const TEST_PASSWORD_WEAK = 'weak';

// Test mnemonic - NEVER USE ON MAINNET
export const TEST_MNEMONIC =
  'abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon art';

// Test addresses
export const TEST_ADDRESS_1 = 'neutaro1test1qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqtest1';
export const TEST_ADDRESS_2 = 'neutaro1test2qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqtest2';
export const TEST_INVALID_ADDRESS = 'invalid1address';

// Test validators
export const TEST_VALIDATOR_1 = 'neutarovaloper1test1qqqqqqqqqqqqqqqqqqqqqqqqqqqtestval1';
export const TEST_VALIDATOR_2 = 'neutarovaloper1test2qqqqqqqqqqqqqqqqqqqqqqqqqqqtestval2';

// Mock RPC responses
export const MOCK_CHAIN_STATUS = {
  node_info: {
    network: 'neutaro-testnet',
    version: '0.1.0',
  },
  sync_info: {
    latest_block_height: '1000000',
    catching_up: false,
  },
};

export const MOCK_BALANCE_RESPONSE = {
  balance: {
    denom: 'untmpi',
    amount: '1000000000', // 1000 NTMPI
  },
};

export const MOCK_VALIDATORS_RESPONSE = [
  {
    operator_address: TEST_VALIDATOR_1,
    consensus_pubkey: {
      '@type': '/cosmos.crypto.ed25519.PubKey',
      key: 'test-key-1',
    },
    jailed: false,
    status: 'BOND_STATUS_BONDED',
    tokens: '1000000000000',
    delegator_shares: '1000000000000.000000000000000000',
    description: {
      moniker: 'Test Validator 1',
      identity: '',
      website: 'https://test1.example.com',
      security_contact: '',
      details: 'Test validator 1',
    },
    commission: {
      commission_rates: {
        rate: '0.100000000000000000',
        max_rate: '0.200000000000000000',
        max_change_rate: '0.010000000000000000',
      },
    },
  },
  {
    operator_address: TEST_VALIDATOR_2,
    consensus_pubkey: {
      '@type': '/cosmos.crypto.ed25519.PubKey',
      key: 'test-key-2',
    },
    jailed: false,
    status: 'BOND_STATUS_BONDED',
    tokens: '500000000000',
    delegator_shares: '500000000000.000000000000000000',
    description: {
      moniker: 'Test Validator 2',
      identity: '',
      website: 'https://test2.example.com',
      security_contact: '',
      details: 'Test validator 2',
    },
    commission: {
      commission_rates: {
        rate: '0.050000000000000000',
        max_rate: '0.200000000000000000',
        max_change_rate: '0.010000000000000000',
      },
    },
  },
];

export const MOCK_TX_RESPONSE = {
  txhash: 'ABC123DEF456GHI789JKL012MNO345PQR678STU901VWX234YZ',
  height: '1000001',
  code: 0,
  raw_log: '[{"msg_index":0,"log":"","events":[]}]',
};

// Cleanup helper for test files
export function cleanupTestFiles(files: string[]): void {
  const fs = require('fs');
  files.forEach((file) => {
    try {
      if (fs.existsSync(file)) {
        fs.unlinkSync(file);
      }
    } catch (error) {
      // Ignore cleanup errors
    }
  });
}

// Create temporary test directory
export function createTestDir(): string {
  const fs = require('fs');
  const path = require('path');
  const os = require('os');
  const testDir = path.join(os.tmpdir(), `clawpurse-test-${Date.now()}`);
  fs.mkdirSync(testDir, { recursive: true });
  return testDir;
}

// Mock console methods to reduce noise in tests
export function mockConsole(): void {
  global.console = {
    ...console,
    log: jest.fn(),
    debug: jest.fn(),
    info: jest.fn(),
    warn: jest.fn(),
    error: jest.fn(),
  };
}

// Restore console
export function restoreConsole(): void {
  global.console = require('console');
}

// Wait for async operation
export async function wait(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

// Generate random test address (for testing only)
export function generateRandomTestAddress(): string {
  const chars = 'abcdefghijklmnopqrstuvwxyz0123456789';
  let address = 'neutaro1';
  for (let i = 0; i < 38; i++) {
    address += chars[Math.floor(Math.random() * chars.length)];
  }
  return address;
}

// Assert error is thrown
export async function assertThrows(
  fn: () => Promise<any>,
  expectedMessage?: string
): Promise<void> {
  let threw = false;
  try {
    await fn();
  } catch (err) {
    const error = err as Error;
    threw = true;
    if (expectedMessage && !error.message.includes(expectedMessage)) {
      throw new Error(
        `Expected error message to include "${expectedMessage}", got "${error.message}"`
      );
    }
  }
  if (!threw) {
    throw new Error('Expected function to throw an error');
  }
}

// Mock fetch for network requests
export function mockFetch(responses: Record<string, any>): void {
  global.fetch = jest.fn((input: string | URL | Request) => {
    const url = typeof input === 'string' ? input : input.toString();
    const response = responses[url] || { error: 'Not mocked' };
    return Promise.resolve({
      ok: true,
      json: () => Promise.resolve(response),
      text: () => Promise.resolve(JSON.stringify(response)),
    } as Response);
  }) as any;
}

// Verify file permissions
export function verifyFilePermissions(filePath: string, expected: number): void {
  const fs = require('fs');
  const stats = fs.statSync(filePath);
  const mode = stats.mode & parseInt('777', 8);
  if (mode !== expected) {
    throw new Error(
      `Expected file permissions ${expected.toString(8)}, got ${mode.toString(8)}`
    );
  }
}

// Generate test receipt
export function generateTestReceipt(overrides: any = {}): any {
  return {
    timestamp: new Date().toISOString(),
    from: TEST_ADDRESS_1,
    to: TEST_ADDRESS_2,
    amount: '100',
    txHash: 'ABC123',
    status: 'confirmed',
    ...overrides,
  };
}

// Setup and teardown helpers
beforeAll(() => {
  // Global setup
});

afterAll(() => {
  // Global cleanup
});

beforeEach(() => {
  // Reset mocks before each test
  jest.clearAllMocks();
});

afterEach(() => {
  // Cleanup after each test
});

export default {
  TEST_PASSWORD,
  TEST_PASSWORD_WEAK,
  TEST_MNEMONIC,
  TEST_ADDRESS_1,
  TEST_ADDRESS_2,
  TEST_INVALID_ADDRESS,
  TEST_VALIDATOR_1,
  TEST_VALIDATOR_2,
  MOCK_CHAIN_STATUS,
  MOCK_BALANCE_RESPONSE,
  MOCK_VALIDATORS_RESPONSE,
  MOCK_TX_RESPONSE,
  cleanupTestFiles,
  createTestDir,
  mockConsole,
  restoreConsole,
  wait,
  generateRandomTestAddress,
  assertThrows,
  mockFetch,
  verifyFilePermissions,
  generateTestReceipt,
};
