/**
 * Security utilities for ClawPurse
 * Memory safety and input validation
 */

import { NEUTARO_CONFIG } from './config.js';

/**
 * Securely wipe a buffer from memory
 */
export function wipeBuffer(buffer: Buffer): void {
  if (buffer && buffer.length > 0) {
    buffer.fill(0);
  }
}

/**
 * Securely wipe a string from memory (best effort)
 * Note: Strings in JavaScript are immutable, so this creates a new empty string
 */
export function wipeString(str: string): string {
  // Best effort - can't actually wipe immutable strings in JS
  // Return empty string to help GC
  return '';
}

/**
 * Validate password strength
 */
export function validatePassword(password: string): { valid: boolean; reason?: string } {
  if (!password || password.length === 0) {
    return { valid: false, reason: 'Password cannot be empty' };
  }
  
  if (password.length < 12) {
    return { valid: false, reason: 'Password must be at least 12 characters long' };
  }
  
  // Check for common weak passwords
  const weakPasswords = ['password123456', '123456789012', 'qwertyuiopas'];
  if (weakPasswords.some(weak => password.toLowerCase().includes(weak))) {
    return { valid: false, reason: 'Password is too common - please choose a stronger password' };
  }
  
  return { valid: true };
}

/**
 * Validate Neutaro address
 */
export function validateAddress(address: string): { valid: boolean; reason?: string } {
  if (!address || typeof address !== 'string') {
    return { valid: false, reason: 'Address must be a non-empty string' };
  }
  
  if (!address.startsWith(NEUTARO_CONFIG.bech32Prefix)) {
    return { 
      valid: false, 
      reason: `Address must start with '${NEUTARO_CONFIG.bech32Prefix}', got '${address.slice(0, 8)}...'` 
    };
  }
  
  // Bech32 addresses are typically 42-45 characters
  if (address.length < 39 || address.length > 90) {
    return { valid: false, reason: `Invalid address length: ${address.length}` };
  }
  
  // Check for valid bech32 characters (lowercase alphanumeric excluding 'b', 'i', 'o', '1')
  const bech32Regex = /^[a-z0-9]+$/;
  const addressBody = address.slice(NEUTARO_CONFIG.bech32Prefix.length + 1);
  if (!bech32Regex.test(addressBody)) {
    return { valid: false, reason: 'Address contains invalid characters' };
  }
  
  return { valid: true };
}

/**
 * Validate validator address
 */
export function validateValidatorAddress(address: string): { valid: boolean; reason?: string } {
  if (!address || typeof address !== 'string') {
    return { valid: false, reason: 'Validator address must be a non-empty string' };
  }
  
  const validatorPrefix = `${NEUTARO_CONFIG.bech32Prefix}valoper`;
  if (!address.startsWith(validatorPrefix)) {
    return { 
      valid: false, 
      reason: `Validator address must start with '${validatorPrefix}'` 
    };
  }
  
  if (address.length < 47 || address.length > 95) {
    return { valid: false, reason: `Invalid validator address length: ${address.length}` };
  }
  
  return { valid: true };
}

/**
 * Validate amount string
 */
export function validateAmount(amount: string): { valid: boolean; reason?: string } {
  if (!amount || typeof amount !== 'string') {
    return { valid: false, reason: 'Amount must be a non-empty string' };
  }
  
  // Check for numeric value
  const num = parseFloat(amount);
  if (isNaN(num)) {
    return { valid: false, reason: 'Amount must be a valid number' };
  }
  
  // Check for negative or zero
  if (num <= 0) {
    return { valid: false, reason: 'Amount must be greater than zero' };
  }
  
  // Check decimal places (max 6 for NTMPI)
  if (amount.includes('.')) {
    const decimalPart = amount.split('.')[1];
    if (decimalPart && decimalPart.length > NEUTARO_CONFIG.decimals) {
      return { 
        valid: false, 
        reason: `Amount has too many decimal places (max ${NEUTARO_CONFIG.decimals})` 
      };
    }
  }
  
  return { valid: true };
}

/**
 * Validate memo string
 */
export function validateMemo(memo: string): { valid: boolean; reason?: string } {
  if (typeof memo !== 'string') {
    return { valid: false, reason: 'Memo must be a string' };
  }
  
  // Max memo length (256 bytes)
  const maxLength = 256;
  if (Buffer.byteLength(memo, 'utf8') > maxLength) {
    return { 
      valid: false, 
      reason: `Memo exceeds maximum length of ${maxLength} bytes` 
    };
  }
  
  // Check for control characters (except newline and tab)
  if (/[\x00-\x08\x0B-\x0C\x0E-\x1F\x7F]/.test(memo)) {
    return { valid: false, reason: 'Memo contains invalid control characters' };
  }
  
  return { valid: true };
}

/**
 * Sanitize user input to prevent injection attacks
 */
export function sanitizeInput(input: string): string {
  if (typeof input !== 'string') {
    return '';
  }
  
  // Remove null bytes and other control characters
  return input.replace(/[\x00-\x1F\x7F]/g, '');
}

/**
 * Create a safe error message that doesn't leak sensitive information
 */
export function createSafeError(message: string, sensitiveData: string[]): Error {
  let safeMessage = message;
  
  // Remove any sensitive data from error message
  sensitiveData.forEach(data => {
    if (data && typeof data === 'string') {
      safeMessage = safeMessage.replace(new RegExp(data, 'gi'), '[REDACTED]');
    }
  });
  
  return new Error(safeMessage);
}

/**
 * Validate mnemonic phrase
 */
export function validateMnemonic(mnemonic: string): { valid: boolean; reason?: string } {
  if (!mnemonic || typeof mnemonic !== 'string') {
    return { valid: false, reason: 'Mnemonic must be a non-empty string' };
  }
  
  const words = mnemonic.trim().split(/\s+/);
  
  // BIP39 mnemonics are 12, 15, 18, 21, or 24 words
  const validLengths = [12, 15, 18, 21, 24];
  if (!validLengths.includes(words.length)) {
    return { 
      valid: false, 
      reason: `Mnemonic must be 12, 15, 18, 21, or 24 words (got ${words.length})` 
    };
  }
  
  // Check each word is valid (basic check - lowercase alphanumeric)
  for (const word of words) {
    if (!/^[a-z]+$/.test(word)) {
      return { valid: false, reason: `Invalid word in mnemonic: '${word}'` };
    }
  }
  
  return { valid: true };
}
