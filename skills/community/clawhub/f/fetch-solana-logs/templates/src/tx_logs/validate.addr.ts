import { isSolanaAddress } from '../utils/utils';
import { parseCliArgs, resolveTargetsFromOptions, targetsConfigPath } from './common';
import fs from 'fs';

/**
 * Validate Solana address(es) via isSolanaAddress before pull/parse.
 *
 *   pnpm validate -- --addr <ADDR>
 *   pnpm validate          # reads target_solana_addr.json
 */
function main() {
  const opts = parseCliArgs();
  let addresses = opts.addresses;

  if (!addresses.length) {
    if (!fs.existsSync(targetsConfigPath)) {
      console.error(`No addresses. Pass --addr or create ${targetsConfigPath}`);
      process.exit(1);
    }
    const raw = JSON.parse(fs.readFileSync(targetsConfigPath, 'utf8'));
    addresses = Array.isArray(raw)
      ? raw.map((x: unknown) => (typeof x === 'string' ? x : String((x as { address?: string })?.address || '')))
      : [];
  }

  if (!addresses.length) {
    console.error('No addresses to validate');
    process.exit(1);
  }

  let ok = true;
  for (const addr of addresses) {
    const valid = isSolanaAddress(addr);
    console.log(`${valid ? 'OK' : 'INVALID'}\t${addr}`);
    if (!valid) ok = false;
  }

  if (!ok) {
    console.error('One or more addresses failed isSolanaAddress(); abort.');
    process.exit(1);
  }

  // Also exercise the shared resolver (throws on invalid)
  resolveTargetsFromOptions({ addresses, limit: null, recent: false });
  console.log(`validated ${addresses.length} Solana address(es)`);
}

main();
