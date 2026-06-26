/**
 * Unit Tests for Wallet and Cryptography Operations
 */

import { describe, it, expect, beforeEach, afterEach } from '@jest/globals';
import * as fs from 'fs/promises';
import * as path from 'path';
import * as os from 'os';
import { 
  generateWallet, 
  walletFromMnemonic, 
  saveKeystore, 
  loadKeystore, 
  keystoreExists 
} from '../../src/keystore.js';
import {
  parseAmount,
  formatAmount,
} from '../../src/wallet.js';
import {
  validatePassword,
  validateAddress,
  validateAmount,
  validateMnemonic,
  validateMemo,
  validateValidatorAddress,
} from '../../src/security.js';

const TEST_PASSWORD = 'test-password-very-secure-123456';
const TEST_PASSWORD_WEAK = 'weak';
const TEST_MNEMONIC = 'abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon art';

describe('Wallet Generation', () => {
  it('should generate a valid 24-word mnemonic', async () => {
    const { mnemonic } = await generateWallet();
    expect(mnemonic).toBeDefined();
    expect(mnemonic.split(' ')).toHaveLength(24);
  });

  it('should generate different mnemonics on each call', async () => {
    const wallet1 = await generateWallet();
    const wallet2 = await generateWallet();
    expect(wallet1.mnemonic).not.toBe(wallet2.mnemonic);
  });

  it('should generate valid neutaro addresses', async () => {
    const { address } = await generateWallet();
    expect(address).toMatch(/^neutaro1[a-z0-9]+$/);
  });

  it('should derive same address from same mnemonic', async () => {
    const { address: address1 } = await walletFromMnemonic(TEST_MNEMONIC);
    const { address: address2 } = await walletFromMnemonic(TEST_MNEMONIC);
    expect(address1).toBe(address2);
  });
});

describe('Mnemonic Validation', () => {
  it('should validate correct mnemonic', () => {
    const result = validateMnemonic(TEST_MNEMONIC);
    expect(result.valid).toBe(true);
  });

  it('should reject invalid word count', () => {
    const result = validateMnemonic('abandon abandon abandon');
    expect(result.valid).toBe(false);
    expect(result.reason).toContain('12, 15, 18, 21, or 24 words');
  });

  it('should reject empty mnemonic', () => {
    const result = validateMnemonic('');
    expect(result.valid).toBe(false);
  });
});

describe('Keystore Encryption', () => {
  let testDir: string;
  let keystorePath: string;

  beforeEach(async () => {
    testDir = path.join(os.tmpdir(), `clawpurse-test-${Date.now()}`);
    await fs.mkdir(testDir, { recursive: true });
    keystorePath = path.join(testDir, 'keystore.enc');
  });

  afterEach(async () => {
    try {
      await fs.rm(testDir, { recursive: true, force: true });
    } catch (error) {
      // Ignore cleanup errors
    }
  });

  it('should encrypt and save keystore with correct password', async () => {
    const { mnemonic, address } = await generateWallet();
    await saveKeystore(mnemonic, address, TEST_PASSWORD, keystorePath);
    const exists = await keystoreExists(keystorePath);
    expect(exists).toBe(true);
  });

  it('should set keystore file permissions to 0600', async () => {
    const { mnemonic, address } = await generateWallet();
    await saveKeystore(mnemonic, address, TEST_PASSWORD, keystorePath);
    
    const stats = await fs.stat(keystorePath);
    const mode = stats.mode & parseInt('777', 8);
    expect(mode).toBe(parseInt('600', 8));
  });

  it('should decrypt keystore with correct password', async () => {
    const { mnemonic, address } = await generateWallet();
    await saveKeystore(mnemonic, address, TEST_PASSWORD, keystorePath);
    
    const decrypted = await loadKeystore(TEST_PASSWORD, keystorePath);
    expect(decrypted.mnemonic).toBe(mnemonic);
    expect(decrypted.address).toBe(address);
  });

  it('should fail to decrypt with incorrect password', async () => {
    const { mnemonic, address } = await generateWallet();
    await saveKeystore(mnemonic, address, TEST_PASSWORD, keystorePath);
    
    await expect(loadKeystore('wrong-password', keystorePath)).rejects.toThrow();
  });

  it('should reject weak passwords', async () => {
    const { mnemonic, address } = await generateWallet();
    
    await expect(
      saveKeystore(mnemonic, address, TEST_PASSWORD_WEAK, keystorePath)
    ).rejects.toThrow(/password/i);
  });
});

describe('Password Validation', () => {
  it('should validate strong passwords', () => {
    const result = validatePassword('very-secure-password-123456');
    expect(result.valid).toBe(true);
  });

  it('should reject short passwords', () => {
    const result = validatePassword('short');
    expect(result.valid).toBe(false);
    expect(result.reason).toContain('12 characters');
  });

  it('should reject empty passwords', () => {
    const result = validatePassword('');
    expect(result.valid).toBe(false);
  });

  it('should reject common passwords', () => {
    const result = validatePassword('password123456');
    expect(result.valid).toBe(false);
    expect(result.reason).toContain('common');
  });
});

describe('Address Validation', () => {
  it('should validate correct neutaro address', () => {
    const result = validateAddress('neutaro1abcdefghijklmnopqrstuvwxyz234567890');
    expect(result.valid).toBe(true);
  });

  it('should reject address with wrong prefix', () => {
    const result = validateAddress('cosmos1abcdefghijklmnopqrstuvwxyz234567890');
    expect(result.valid).toBe(false);
    expect(result.reason).toContain('neutaro');
  });

  it('should reject address with wrong length', () => {
    const result = validateAddress('neutaro1short');
    expect(result.valid).toBe(false);
    expect(result.reason).toContain('length');
  });

  it('should reject empty address', () => {
    const result = validateAddress('');
    expect(result.valid).toBe(false);
  });
});

describe('Validator Address Validation', () => {
  it('should validate correct validator address', () => {
    const result = validateValidatorAddress('neutarovaloper1abcdefghijklmnopqrstuvwxyz234567890abc');
    expect(result.valid).toBe(true);
  });

  it('should reject validator address with wrong prefix', () => {
    const result = validateValidatorAddress('neutaro1abcdefghijklmnopqrstuvwxyz234567890');
    expect(result.valid).toBe(false);
    expect(result.reason).toContain('valoper');
  });
});

describe('Amount Validation', () => {
  it('should accept valid positive amounts', () => {
    expect(validateAmount('100').valid).toBe(true);
    expect(validateAmount('0.5').valid).toBe(true);
    expect(validateAmount('1000.123456').valid).toBe(true);
  });

  it('should reject negative amounts', () => {
    const result = validateAmount('-100');
    expect(result.valid).toBe(false);
  });

  it('should reject zero amounts', () => {
    const result = validateAmount('0');
    expect(result.valid).toBe(false);
  });

  it('should reject non-numeric values', () => {
    const result = validateAmount('abc');
    expect(result.valid).toBe(false);
  });

  it('should reject amounts exceeding max precision', () => {
    const result = validateAmount('1.1234567'); // 7 decimal places
    expect(result.valid).toBe(false);
    expect(result.reason).toContain('decimal places');
  });

  it('should accept amounts with trailing zeros', () => {
    const result = validateAmount('100.000000');
    expect(result.valid).toBe(true);
  });

  it('should reject empty amounts', () => {
    const result = validateAmount('');
    expect(result.valid).toBe(false);
  });
});

describe('Amount Parsing and Formatting', () => {
  it('should parse integer amounts to base units', () => {
    expect(parseAmount('1')).toBe(1_000_000n);
    expect(parseAmount('100')).toBe(100_000_000n);
  });

  it('should parse decimal amounts to base units', () => {
    expect(parseAmount('0.5')).toBe(500_000n);
    expect(parseAmount('1.5')).toBe(1_500_000n);
  });

  it('should format base units to display units', () => {
    expect(formatAmount(1_000_000n)).toContain('1.000000');
    expect(formatAmount(500_000n)).toContain('0.500000');
  });

  it('should handle zero amount', () => {
    expect(formatAmount(0n)).toContain('0.000000');
  });

  it('should format large amounts correctly', () => {
    expect(formatAmount(1_234_567_890n)).toContain('1234.567890');
  });
});

describe('Memo Validation', () => {
  it('should accept valid memo', () => {
    const result = validateMemo('Payment for services');
    expect(result.valid).toBe(true);
  });

  it('should accept empty memo', () => {
    const result = validateMemo('');
    expect(result.valid).toBe(true);
  });

  it('should accept memo with special characters', () => {
    const result = validateMemo('Invoice #123 - $100.50');
    expect(result.valid).toBe(true);
  });

  it('should reject memo exceeding max length', () => {
    const longMemo = 'x'.repeat(300);
    const result = validateMemo(longMemo);
    expect(result.valid).toBe(false);
    expect(result.reason).toContain('maximum length');
  });

  it('should reject memo with control characters', () => {
    const result = validateMemo('test\x00memo');
    expect(result.valid).toBe(false);
  });
});
