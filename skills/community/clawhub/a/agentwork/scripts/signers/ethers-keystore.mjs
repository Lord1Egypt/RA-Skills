import { readFileSync, writeFileSync, mkdirSync, existsSync, chmodSync, statSync } from 'node:fs';
import { dirname } from 'node:path';
import { execFileSync } from 'node:child_process';
import { randomBytes } from 'node:crypto';
import { importNodePackage } from '../runtime-node-packages.mjs';

const ethers = await importNodePackage('ethers');

export const provider = 'ethers-keystore';
export const signerType = 'local-keystore';
export const requiresKeystore = true;

function resolvePassphraseDir(keystorePath) {
  return dirname(keystorePath);
}

function storePassphrase(passphrase, credDir) {
  if (process.platform === 'darwin') {
    try {
      execFileSync('security', [
        'add-generic-password',
        '-a', 'agentwork-hot-wallet',
        '-s', 'agentwork-hot-wallet',
        '-w', passphrase,
        '-U',
      ], { stdio: 'pipe' });
      return 'keychain';
    } catch {
      // fall through
    }
  }

  if (process.platform === 'linux') {
    try {
      execFileSync('secret-tool', [
        'store',
        '--label', 'agentwork-hot-wallet',
        'service', 'agentwork-hot-wallet',
        'account', 'hot-wallet',
      ], { stdio: 'pipe', input: passphrase });
      return 'secret-tool';
    } catch {
      // fall through
    }
  }

  const passFile = `${credDir}/.passphrase`;
  writeFileSync(passFile, passphrase, { mode: 0o600 });
  return 'file';
}

function readPassphrase(credDir) {
  if (process.platform === 'darwin') {
    try {
      return execFileSync('security', [
        'find-generic-password',
        '-a', 'agentwork-hot-wallet',
        '-s', 'agentwork-hot-wallet',
        '-w',
      ], { stdio: ['pipe', 'pipe', 'pipe'], encoding: 'utf8' }).trim();
    } catch {
      // fall through
    }
  }

  if (process.platform === 'linux') {
    try {
      return execFileSync('secret-tool', [
        'lookup',
        'service', 'agentwork-hot-wallet',
        'account', 'hot-wallet',
      ], { stdio: ['pipe', 'pipe', 'pipe'], encoding: 'utf8' }).trim();
    } catch {
      // fall through
    }
  }

  const passFile = `${credDir}/.passphrase`;
  if (!existsSync(passFile)) {
    throw new Error('No passphrase in keychain or file');
  }
  return readFileSync(passFile, 'utf8').trim();
}

function readKeystoreAddress(keystorePath) {
  if (!existsSync(keystorePath)) {
    throw new Error(`No keystore at ${keystorePath}`);
  }
  const keystore = JSON.parse(readFileSync(keystorePath, 'utf8'));
  if (!keystore.address) {
    throw new Error('No address field in keystore');
  }
  return ethers.getAddress(`0x${keystore.address}`);
}

function loadWalletObject(keystorePath) {
  if (!existsSync(keystorePath)) {
    throw new Error(`No keystore at ${keystorePath}`);
  }
  const keystore = readFileSync(keystorePath, 'utf8');
  const credDir = resolvePassphraseDir(keystorePath);
  const passphrase = readPassphrase(credDir);
  return ethers.Wallet.fromEncryptedJsonSync(keystore, passphrase);
}

export async function createWallet(opts) {
  const keystorePath = opts.keystore;
  if (!keystorePath) throw new Error('keystore is required');
  if (existsSync(keystorePath)) {
    return {
      address: readKeystoreAddress(keystorePath),
      meta: null,
      passphraseStorage: 'existing',
    };
  }

  const credDir = resolvePassphraseDir(keystorePath);
  mkdirSync(credDir, { recursive: true });
  try { chmodSync(credDir, 0o700); } catch { /* best effort */ }

  const wallet = ethers.Wallet.createRandom();
  const passphrase = randomBytes(32).toString('hex');
  const keystore = await wallet.encrypt(passphrase);
  writeFileSync(keystorePath, keystore, { mode: 0o600 });

  return {
    address: wallet.address,
    meta: null,
    passphraseStorage: storePassphrase(passphrase, credDir),
  };
}

export async function loadWallet(opts) {
  const wallet = loadWalletObject(opts.keystore);
  return {
    address: wallet.address,
    wallet,
  };
}

export async function signMessage(opts) {
  const { wallet } = await loadWallet(opts);
  return {
    signature: await wallet.signMessage(opts.message),
  };
}

export async function signTypedData(opts) {
  const { wallet } = await loadWallet(opts);
  return {
    signature: await wallet.signTypedData(opts.domain, opts.types, opts.message),
  };
}

export async function getAddress(opts) {
  return {
    address: readKeystoreAddress(opts.keystore),
  };
}

export async function auditKeystore(opts) {
  const keystorePath = opts.keystore;
  const credDir = resolvePassphraseDir(keystorePath);
  const address = readKeystoreAddress(keystorePath);

  let passphraseStorage = 'none';
  if (process.platform === 'darwin') {
    try {
      execFileSync('security', [
        'find-generic-password',
        '-a', 'agentwork-hot-wallet',
        '-s', 'agentwork-hot-wallet',
      ], { stdio: 'pipe' });
      passphraseStorage = 'keychain';
    } catch {
      passphraseStorage = existsSync(`${credDir}/.passphrase`) ? 'file' : 'none';
    }
  } else if (process.platform === 'linux') {
    try {
      execFileSync('secret-tool', [
        'lookup',
        'service', 'agentwork-hot-wallet',
        'account', 'hot-wallet',
      ], { stdio: ['pipe', 'pipe', 'pipe'] });
      passphraseStorage = 'secret-tool';
    } catch {
      passphraseStorage = existsSync(`${credDir}/.passphrase`) ? 'file' : 'none';
    }
  } else {
    passphraseStorage = existsSync(`${credDir}/.passphrase`) ? 'file' : 'none';
  }

  let keystorePermissions = 'unknown';
  let dirPermissions = 'unknown';
  try {
    keystorePermissions = `0${(statSync(keystorePath).mode & 0o777).toString(8)}`;
  } catch {
    // best effort
  }
  try {
    dirPermissions = `0${(statSync(credDir).mode & 0o777).toString(8)}`;
  } catch {
    // best effort
  }

  return {
    address,
    passphrase_storage: passphraseStorage,
    keystore_permissions: keystorePermissions,
    dir_permissions: dirPermissions,
  };
}
