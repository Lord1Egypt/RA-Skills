import fs from 'fs';
import readline from 'readline';
import { encryptPrivateKey } from './key-manager.js';

function ask(q: string): Promise<string> {
  const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
  return new Promise((res) => rl.question(q, (a) => { rl.close(); res(a.trim()); }));
}

const out = process.argv.includes('--out') ? process.argv[process.argv.indexOf('--out') + 1] : './secrets/key.json';
const pk = await ask('EVM private key (0x...): ');
const pass = await ask('Passphrase: ');
const enc = encryptPrivateKey(pk, pass);
fs.mkdirSync(out.split('/').slice(0, -1).join('/'), { recursive: true });
fs.writeFileSync(out, JSON.stringify(enc, null, 2));
console.log('Encrypted key saved:', out);
