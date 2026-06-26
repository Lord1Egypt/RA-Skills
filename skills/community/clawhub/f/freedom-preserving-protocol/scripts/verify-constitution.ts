import { readFileSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import * as ed from '@noble/ed25519';
import { sha512 } from '@noble/hashes/sha512';
import { sha256 } from '@noble/hashes/sha256';
import { hexToBytes, bytesToHex } from '@noble/hashes/utils';

ed.etc.sha512Sync = (...m) => sha512(ed.etc.concatBytes(...m));

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = resolve(__dirname, '..');

const constitutionPath = resolve(root, 'constitution.json');
const sigPath = resolve(root, 'signature.ed25519.txt');
const pubkeyPath = resolve(root, 'pubkey.ed25519.txt');

try {
  const constitutionBytes = readFileSync(constitutionPath);
  const hash = sha256(constitutionBytes);

  const signatureHex = readFileSync(sigPath, 'utf-8').trim();
  const pubkeyHex = readFileSync(pubkeyPath, 'utf-8').trim();

  const signature = hexToBytes(signatureHex);
  const publicKey = hexToBytes(pubkeyHex);

  const valid = ed.verify(signature, hash, publicKey);

  console.log(`Constitution SHA-256: ${bytesToHex(hash)}`);
  console.log(`Public key:           ${pubkeyHex}`);
  console.log(`Signature valid:      ${valid ? 'YES' : 'NO'}`);

  if (!valid) {
    console.error('\nWARNING: Signature verification FAILED.');
    console.error('The constitution.json may have been tampered with.');
    console.error('Do NOT adopt this constitution.');
    process.exit(1);
  }

  console.log('\nConstitution integrity verified. Safe to adopt.');
} catch (err: any) {
  if (err.code === 'ENOENT') {
    console.error(`Missing file: ${err.path}`);
    console.error('Run "npm run sign" first to generate signature and public key.');
  } else {
    console.error('Verification failed:', err.message);
  }
  process.exit(1);
}
