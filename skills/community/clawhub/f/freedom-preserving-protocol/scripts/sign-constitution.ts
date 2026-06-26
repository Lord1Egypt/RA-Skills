import { readFileSync, writeFileSync, existsSync, chmodSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import * as ed from '@noble/ed25519';
import { sha512 } from '@noble/hashes/sha512';
import { sha256 } from '@noble/hashes/sha256';
import { bytesToHex, hexToBytes } from '@noble/hashes/utils';

ed.etc.sha512Sync = (...m) => sha512(ed.etc.concatBytes(...m));

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = resolve(__dirname, '..');

const constitutionPath = resolve(root, 'constitution.json');
const sigPath = resolve(root, 'signature.ed25519.txt');
const pubkeyPath = resolve(root, 'pubkey.ed25519.txt');
const localKeyPath = resolve(root, '.signing-key.ed25519.local');

const args = new Set(process.argv.slice(2));
const allowGenerate = args.has('--generate-key');

// CI detection: any of these env vars being set means we refuse to mint a new
// key, because CI logs and artifact stores routinely capture stdout and on-disk
// files in ways that have historically leaked secrets.
const CI_ENV_VARS = [
  'CI',
  'GITHUB_ACTIONS',
  'GITLAB_CI',
  'BUILDKITE',
  'CIRCLECI',
  'TRAVIS',
  'JENKINS_URL',
  'TEAMCITY_VERSION',
  'TF_BUILD',
  'BITBUCKET_BUILD_NUMBER',
  'CODEBUILD_BUILD_ID',
] as const;
const inCI = CI_ENV_VARS.some((v) => Boolean(process.env[v]));

function parsePrivateKeyHex(hex: string, source: string): Uint8Array {
  const trimmed = hex.trim();
  if (!/^[0-9a-fA-F]{64}$/.test(trimmed)) {
    console.error(
      `ERROR: Signing key from ${source} is not a 32-byte hex string ` +
        `(expected 64 hex chars, got ${trimmed.length}).`,
    );
    process.exit(2);
  }
  return hexToBytes(trimmed);
}

const constitutionBytes = readFileSync(constitutionPath);
const hash = sha256(constitutionBytes);

let privateKey: Uint8Array;
let keySource: string;

if (process.env.FPP_SIGNING_KEY) {
  privateKey = parsePrivateKeyHex(process.env.FPP_SIGNING_KEY, 'FPP_SIGNING_KEY env var');
  keySource = 'FPP_SIGNING_KEY env var';
} else if (existsSync(localKeyPath)) {
  privateKey = parsePrivateKeyHex(readFileSync(localKeyPath, 'utf-8'), localKeyPath);
  keySource = localKeyPath;
} else {
  if (inCI) {
    console.error('ERROR: Refusing to mint a new signing key in a CI environment.');
    console.error(
      'CI logs and artifact stores routinely capture stdout and on-disk files; ' +
        'a private key produced here would almost certainly leak.',
    );
    console.error(
      'Provide an existing key out-of-band via the FPP_SIGNING_KEY environment variable.',
    );
    process.exit(2);
  }

  if (!allowGenerate) {
    console.error('ERROR: No signing key found.');
    console.error('  - Set FPP_SIGNING_KEY (hex-encoded 32-byte private key), or');
    console.error(`  - Place an existing key at ${localKeyPath}, or`);
    console.error('  - Re-run with --generate-key to mint a fresh local key.');
    console.error('');
    console.error(
      'For safety, this script never prints private keys. A newly generated key is written ' +
        'only to .signing-key.ed25519.local (gitignored, mode 0600).',
    );
    process.exit(2);
  }

  if (!process.stdout.isTTY) {
    console.error(
      'ERROR: Refusing to mint a new signing key when stdout is not a TTY ' +
        '(detected redirection or capture).',
    );
    console.error(
      'Run interactively, or provide an existing key via FPP_SIGNING_KEY.',
    );
    process.exit(2);
  }

  privateKey = ed.utils.randomPrivateKey();
  // mode on writeFileSync only applies at create time on POSIX; chmod afterward
  // tightens permissions for the overwrite case too. Windows ignores mode bits
  // but will not throw.
  writeFileSync(localKeyPath, bytesToHex(privateKey), { mode: 0o600 });
  try {
    chmodSync(localKeyPath, 0o600);
  } catch {
    // Windows / non-POSIX FS: best-effort only.
  }
  keySource = `${localKeyPath} (newly generated)`;
}

const publicKey = ed.getPublicKey(privateKey);
const signature = ed.sign(hash, privateKey);

writeFileSync(sigPath, bytesToHex(signature));
writeFileSync(pubkeyPath, bytesToHex(publicKey));

const constitutionHash = bytesToHex(hash);
console.log(`Signing key:           ${keySource}`);
console.log(`Constitution SHA-256:  ${constitutionHash}`);
console.log(`Public key written to: ${pubkeyPath}`);
console.log(`Signature written to:  ${sigPath}`);
console.log(`\nVerify with: npx tsx scripts/verify-constitution.ts`);
