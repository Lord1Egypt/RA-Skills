// Copyright (c) Galleon Labs. MIT License.
// Offline tick arithmetic only; no RPC, prices, calldata or signing.
export function ticks({ lower, upper, spacing, current }) {
  for (const [key, value] of Object.entries({ lower, upper, spacing, current })) {
    if (!Number.isSafeInteger(value)) throw new Error(`${key} must be a safe integer`);
  }
  if (spacing <= 0 || spacing > 887272 || lower >= upper) throw new Error('Invalid spacing or ordered range');
  const min = Math.ceil(-887272 / spacing) * spacing;
  const max = Math.floor(887272 / spacing) * spacing;
  if (lower < min || upper > max || current < -887272 || current > 887272) throw new Error('Ticks outside usable bounds');
  const tickLower = Math.floor(lower / spacing) * spacing;
  const tickUpper = Math.ceil(upper / spacing) * spacing;
  return { tickLower, tickUpper, active: current >= tickLower && current < tickUpper,
    principal: current < tickLower ? 'token0' : current >= tickUpper ? 'token1' : 'both',
    evidence: 'offline arithmetic; token order and live state unverified' };
}
if (import.meta.url === new URL(process.argv[1], 'file:').href) {
  if (process.argv[2] === '--help') { console.log('Usage: node scripts/ticks.mjs JSON\nJSON: integer lower, upper, spacing, current. Offline arithmetic only.'); process.exit(0); }
  try { console.log(JSON.stringify(ticks(JSON.parse(process.argv[2])), null, 2)); }
  catch (error) { console.error(error instanceof SyntaxError ? 'Invalid JSON input; use --help for the expected fields' : error.message); process.exitCode = 1; }
}
