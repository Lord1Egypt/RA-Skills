// Copyright (c) Galleon Labs. MIT License.
// Offline comparison of supplied observations; does not verify on-chain settlement.
export function settlement(input) {
  const { status, substatus, expectedChain, receivedChain, expectedToken, receivedToken, minimumRaw, receivedRaw } = input;
  if (typeof status !== 'string') throw new Error('status is required');
  const result = { state: 'unresolved', minimumMet: null, evidence: 'supplied observations only; verify destination receipt and recipient' };
  if (status !== 'DONE') { result.state = status === 'PENDING' ? 'pending' : 'unresolved'; return result; }
  if (substatus === 'REFUNDED') { result.state = 'refunded'; return result; }
  if (substatus === 'PARTIAL') { result.state = 'partial'; return result; }
  if (substatus !== 'COMPLETED') return result;
  if (!Number.isSafeInteger(expectedChain) || expectedChain <= 0 || !Number.isSafeInteger(receivedChain) || receivedChain <= 0) throw new Error('Positive chain IDs required');
  const addr = /^0x[0-9a-fA-F]{40}$/;
  if (!addr.test(expectedToken) || !addr.test(receivedToken)) throw new Error('EVM token addresses required');
  if (expectedChain !== receivedChain || expectedToken.toLowerCase() !== receivedToken.toLowerCase()) { result.state = 'asset-mismatch'; return result; }
  if (typeof minimumRaw !== 'string' || typeof receivedRaw !== 'string' || !/^\d+$/.test(minimumRaw) || !/^\d+$/.test(receivedRaw)) throw new Error('Raw amounts must be unsigned integer strings');
  result.minimumMet = BigInt(receivedRaw) >= BigInt(minimumRaw);
  result.state = result.minimumMet ? 'reported-delivery-awaiting-chain-proof' : 'below-minimum';
  return result;
}
if (import.meta.url === new URL(process.argv[1], 'file:').href) {
  if (process.argv[2] === '--help') { console.log('Usage: node scripts/settlement.mjs JSON\nJSON: status, substatus; COMPLETED also needs expectedChain, receivedChain, expectedToken, receivedToken, minimumRaw, receivedRaw. Offline EVM observations only.'); process.exit(0); }
  try { console.log(JSON.stringify(settlement(JSON.parse(process.argv[2])), null, 2)); }
  catch (error) { console.error(error instanceof SyntaxError ? 'Invalid JSON input; use --help for the expected fields' : error.message); process.exitCode = 1; }
}
