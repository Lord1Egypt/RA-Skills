// Encrypted local keystore for ClawPurse
import { DirectSecp256k1HdWallet } from '@cosmjs/proto-signing';
import { Secp256k1, Sha256, Random } from '@cosmjs/crypto';
import * as crypto from 'crypto';
import * as fs from 'fs/promises';
import * as path from 'path';
import * as os from 'os';
import { KEYSTORE_CONFIG, NEUTARO_CONFIG } from './config.js';

export interface KeystoreData {
  version: 1;
  address: string;
  encryptedMnemonic: string;
  salt: string;
  iv: string;
  createdAt: string;
}

export interface DecryptedWallet {
  mnemonic: string;
  address: string;
  wallet: DirectSecp256k1HdWallet;
}

function getDefaultKeystorePath(): string {
  return path.join(os.homedir(), KEYSTORE_CONFIG.defaultPath);
}

function deriveKey(password: string, salt: Buffer): Buffer {
  // Use scrypt for key derivation
  return crypto.scryptSync(password, salt, 32, {
    N: KEYSTORE_CONFIG.scryptN,
    r: KEYSTORE_CONFIG.scryptR,
    p: KEYSTORE_CONFIG.scryptP,
  });
}

function encrypt(plaintext: string, password: string): { ciphertext: string; salt: string; iv: string } {
  const salt = crypto.randomBytes(32);
  const iv = crypto.randomBytes(16);
  const key = deriveKey(password, salt);
  
  const cipher = crypto.createCipheriv('aes-256-gcm', key, iv);
  let encrypted = cipher.update(plaintext, 'utf8', 'hex');
  encrypted += cipher.final('hex');
  const authTag = cipher.getAuthTag();
  
  return {
    ciphertext: encrypted + ':' + authTag.toString('hex'),
    salt: salt.toString('hex'),
    iv: iv.toString('hex'),
  };
}

function decrypt(ciphertext: string, salt: string, iv: string, password: string): string {
  const [encryptedData, authTagHex] = ciphertext.split(':');
  const key = deriveKey(password, Buffer.from(salt, 'hex'));
  
  const decipher = crypto.createDecipheriv('aes-256-gcm', key, Buffer.from(iv, 'hex'));
  decipher.setAuthTag(Buffer.from(authTagHex, 'hex'));
  
  let decrypted = decipher.update(encryptedData, 'hex', 'utf8');
  decrypted += decipher.final('utf8');
  
  return decrypted;
}

export async function generateWallet(): Promise<{ mnemonic: string; address: string; wallet: DirectSecp256k1HdWallet }> {
  const wallet = await DirectSecp256k1HdWallet.generate(24, {
    prefix: NEUTARO_CONFIG.bech32Prefix,
  });
  
  const [account] = await wallet.getAccounts();
  const mnemonic = wallet.mnemonic;
  
  return {
    mnemonic,
    address: account.address,
    wallet,
  };
}

export async function walletFromMnemonic(mnemonic: string): Promise<{ address: string; wallet: DirectSecp256k1HdWallet }> {
  const wallet = await DirectSecp256k1HdWallet.fromMnemonic(mnemonic, {
    prefix: NEUTARO_CONFIG.bech32Prefix,
  });
  
  const [account] = await wallet.getAccounts();
  
  return {
    address: account.address,
    wallet,
  };
}

export async function saveKeystore(
  mnemonic: string,
  address: string,
  password: string,
  keystorePath?: string
): Promise<string> {
  // Import security utilities
  const { validatePassword, validateMnemonic } = await import('./security.js');
  
  // Validate password strength
  const passwordValidation = validatePassword(password);
  if (!passwordValidation.valid) {
    throw new Error(`Weak password: ${passwordValidation.reason}`);
  }
  
  // Validate mnemonic
  const mnemonicValidation = validateMnemonic(mnemonic);
  if (!mnemonicValidation.valid) {
    throw new Error(`Invalid mnemonic: ${mnemonicValidation.reason}`);
  }
  
  const filePath = keystorePath || getDefaultKeystorePath();
  
  // Ensure directory exists
  await fs.mkdir(path.dirname(filePath), { recursive: true });
  
  const { ciphertext, salt, iv } = encrypt(mnemonic, password);
  
  const keystoreData: KeystoreData = {
    version: 1,
    address,
    encryptedMnemonic: ciphertext,
    salt,
    iv,
    createdAt: new Date().toISOString(),
  };
  
  await fs.writeFile(filePath, JSON.stringify(keystoreData, null, 2), { mode: 0o600 });
  
  return filePath;
}

export async function loadKeystore(password: string, keystorePath?: string): Promise<DecryptedWallet> {
  const filePath = keystorePath || getDefaultKeystorePath();
  
  const data = await fs.readFile(filePath, 'utf8');
  const keystore: KeystoreData = JSON.parse(data);
  
  if (keystore.version !== 1) {
    throw new Error(`Unsupported keystore version: ${keystore.version}`);
  }
  
  const mnemonic = decrypt(
    keystore.encryptedMnemonic,
    keystore.salt,
    keystore.iv,
    password
  );
  
  const { wallet } = await walletFromMnemonic(mnemonic);
  
  return {
    mnemonic,
    address: keystore.address,
    wallet,
  };
}

export async function keystoreExists(keystorePath?: string): Promise<boolean> {
  const filePath = keystorePath || getDefaultKeystorePath();
  try {
    await fs.access(filePath);
    return true;
  } catch {
    return false;
  }
}

export async function getKeystoreAddress(keystorePath?: string): Promise<string | null> {
  const filePath = keystorePath || getDefaultKeystorePath();
  try {
    const data = await fs.readFile(filePath, 'utf8');
    const keystore: KeystoreData = JSON.parse(data);
    return keystore.address;
  } catch {
    return null;
  }
}

export { getDefaultKeystorePath };
