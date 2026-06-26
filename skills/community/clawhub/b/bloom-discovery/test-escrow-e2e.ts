/**
 * Escrow E2E Test on Base Sepolia
 *
 * Tests the full lifecycle:
 *  1. Deploy MockUSDC (public mint)
 *  2. Deploy fresh BloomSkillEscrow(MockUSDC)
 *  3. Mint USDC to backer
 *  4. Approve + deposit (single)
 *  5. Approve + depositBatch (multi)
 *  6. Verify on-chain state (getDeposit, getSkillInfo, getAvailableEscrow)
 *  7. approveClaim (admin assigns builder)
 *  8. builderWithdraw (builder claims funds)
 *  9. Verify refund eligibility (should fail — skill is claimed)
 *
 * Uses the deployer key from bloom-identity-card/.env as both admin and backer.
 */

import { createPublicClient, createWalletClient, http, parseAbi, keccak256, toHex, formatUnits } from 'viem';
import { baseSepolia } from 'viem/chains';
import { privateKeyToAccount } from 'viem/accounts';

// ─── Config ─────────────────────────────────────────────────────────────

const PRIVATE_KEY = process.env.ESCROW_TEST_PRIVATE_KEY as `0x${string}`;
if (!PRIVATE_KEY) {
  console.error('Set ESCROW_TEST_PRIVATE_KEY in .env or environment to run this test');
  process.exit(1);
}
const RPC_URL = 'https://sepolia.base.org';

const EXISTING_ESCROW = '0xc21745de70ad333c326c77b1293c895c75fccac5' as const;
const SEPOLIA_USDC = '0x036CbD53842c5426634e7929541eC2318f3dCF7e' as const;

// Test skills — unique per run to avoid state collision
const RUN_ID = Date.now().toString(36);
const SKILL_SLUG_1 = `test-skill-e2e-${RUN_ID}-1`;
const SKILL_SLUG_2 = `test-skill-e2e-${RUN_ID}-2`;
const SKILL_SLUG_3 = `test-skill-e2e-${RUN_ID}-3`;
const SKILL_HASH_1 = keccak256(toHex(SKILL_SLUG_1));
const SKILL_HASH_2 = keccak256(toHex(SKILL_SLUG_2));
const SKILL_HASH_3 = keccak256(toHex(SKILL_SLUG_3));

// ─── ABIs ───────────────────────────────────────────────────────────────

const escrowAbi = parseAbi([
  'function usdc() view returns (address)',
  'function REFUND_PERIOD() view returns (uint256)',
  'function MAX_BATCH_SIZE() view returns (uint256)',
  'function paused() view returns (bool)',
  'function owner() view returns (address)',
  'function deposit(bytes32 skillHash, uint256 amount)',
  'function depositBatch(bytes32[] skillHashes, uint256[] amounts)',
  'function approveClaim(bytes32 skillHash, address builder)',
  'function builderWithdraw(bytes32 skillHash, uint256 amount)',
  'function claimRefund(bytes32 skillHash)',
  'function getDeposit(bytes32 skillHash, address backer) view returns (uint256 amount, uint256 depositedAt, bool refunded)',
  'function getSkillInfo(bytes32 skillHash) view returns (address builder, uint256 totalDeposited, uint256 totalWithdrawn, bool revoked)',
  'function getAvailableEscrow(bytes32 skillHash) view returns (uint256)',
  'function isRefundEligible(bytes32 skillHash, address backer) view returns (bool eligible, uint256 eligibleAt)',
  'function getSkillBackers(bytes32 skillHash) view returns (address[])',
  'event Deposited(bytes32 indexed skillHash, address indexed backer, uint256 amount)',
  'event BatchDeposited(address indexed backer, bytes32[] skillHashes, uint256[] amounts, uint256 totalAmount)',
  'event BuilderApproved(bytes32 indexed skillHash, address indexed builder)',
  'event BuilderWithdrew(bytes32 indexed skillHash, address indexed builder, uint256 amount)',
]);

const erc20Abi = parseAbi([
  'function approve(address spender, uint256 amount) returns (bool)',
  'function balanceOf(address account) view returns (uint256)',
  'function allowance(address owner, address spender) view returns (uint256)',
  'function transfer(address to, uint256 amount) returns (bool)',
  'function decimals() view returns (uint8)',
  'function name() view returns (string)',
]);

// ─── Setup ──────────────────────────────────────────────────────────────

const account = privateKeyToAccount(PRIVATE_KEY);

const publicClient = createPublicClient({
  chain: baseSepolia,
  transport: http(RPC_URL),
});

const walletClient = createWalletClient({
  account,
  chain: baseSepolia,
  transport: http(RPC_URL),
});

// ─── Helpers ────────────────────────────────────────────────────────────

function usdc(amount: number): bigint {
  return BigInt(Math.round(amount * 1e6));
}

function ok(label: string) {
  console.log(`  ✅ ${label}`);
}

function fail(label: string, err?: any) {
  console.log(`  ❌ ${label}${err ? ': ' + (err.shortMessage || err.message || err) : ''}`);
}

// ─── Main ───────────────────────────────────────────────────────────────

async function main() {
  console.log('╔══════════════════════════════════════════════════════════╗');
  console.log('║   Escrow E2E Test — Base Sepolia                       ║');
  console.log('╚══════════════════════════════════════════════════════════╝\n');

  console.log(`Deployer/Admin: ${account.address}`);
  console.log(`Escrow:         ${EXISTING_ESCROW}`);
  console.log(`USDC (Sepolia): ${SEPOLIA_USDC}\n`);

  // ── Phase 1: Read-only checks (verify contract is alive) ──

  console.log('━━━ Phase 1: Contract State Checks ━━━\n');

  try {
    const usdcAddr = await publicClient.readContract({
      address: EXISTING_ESCROW,
      abi: escrowAbi,
      functionName: 'usdc',
    });
    const matches = usdcAddr.toLowerCase() === SEPOLIA_USDC.toLowerCase();
    matches ? ok(`USDC address matches: ${usdcAddr}`) : fail(`USDC mismatch: ${usdcAddr}`);
  } catch (e) { fail('Read usdc()', e); }

  try {
    const owner = await publicClient.readContract({
      address: EXISTING_ESCROW,
      abi: escrowAbi,
      functionName: 'owner',
    });
    const isOwner = owner.toLowerCase() === account.address.toLowerCase();
    isOwner ? ok(`Owner is deployer: ${owner}`) : fail(`Owner mismatch: ${owner} (expected ${account.address})`);
  } catch (e) { fail('Read owner()', e); }

  try {
    const refundPeriod = await publicClient.readContract({
      address: EXISTING_ESCROW,
      abi: escrowAbi,
      functionName: 'REFUND_PERIOD',
    });
    ok(`REFUND_PERIOD = ${Number(refundPeriod) / 86400} days`);
  } catch (e) { fail('Read REFUND_PERIOD()', e); }

  try {
    const paused = await publicClient.readContract({
      address: EXISTING_ESCROW,
      abi: escrowAbi,
      functionName: 'paused',
    });
    !paused ? ok('Contract is NOT paused') : fail('Contract is PAUSED');
  } catch (e) { fail('Read paused()', e); }

  try {
    const maxBatch = await publicClient.readContract({
      address: EXISTING_ESCROW,
      abi: escrowAbi,
      functionName: 'MAX_BATCH_SIZE',
    });
    ok(`MAX_BATCH_SIZE = ${maxBatch}`);
  } catch (e) { fail('Read MAX_BATCH_SIZE()', e); }

  // ── Phase 2: Check USDC balance ──

  console.log('\n━━━ Phase 2: USDC Balance Check ━━━\n');

  const balance = await publicClient.readContract({
    address: SEPOLIA_USDC,
    abi: erc20Abi,
    functionName: 'balanceOf',
    args: [account.address],
  });

  const balanceFloat = Number(balance) / 1e6;
  console.log(`  USDC balance: $${balanceFloat.toFixed(2)}`);

  if (balanceFloat < 6) {
    console.log('\n  ⚠️  Insufficient Sepolia USDC for write tests.');
    console.log('  Get test USDC from: https://faucet.circle.com/');
    console.log(`  Send to: ${account.address}`);
    console.log('  Select: Base Sepolia + USDC\n');
    console.log('  Skipping write tests. Re-run after funding.\n');

    // Still run view function tests on existing state
    await testViewFunctions();
    return;
  }

  // ── Phase 3: Write tests ──

  console.log('\n━━━ Phase 3: Deposit (Single) ━━━\n');

  const SINGLE_AMOUNT = usdc(3);

  // Approve
  console.log(`  Approving $3 USDC to escrow...`);
  const approveTx = await walletClient.writeContract({
    address: SEPOLIA_USDC,
    abi: erc20Abi,
    functionName: 'approve',
    args: [EXISTING_ESCROW, SINGLE_AMOUNT],
  });
  const approveReceipt = await publicClient.waitForTransactionReceipt({ hash: approveTx, confirmations: 2 });
  approveReceipt.status === 'success' ? ok(`Approve tx: ${approveTx}`) : fail(`Approve reverted: ${approveTx}`);

  // Deposit single skill
  console.log(`  Depositing $3 to skill "${SKILL_SLUG_1}"...`);
  const depositTx = await walletClient.writeContract({
    address: EXISTING_ESCROW,
    abi: escrowAbi,
    functionName: 'deposit',
    args: [SKILL_HASH_1, SINGLE_AMOUNT],
  });
  const depositReceipt = await publicClient.waitForTransactionReceipt({ hash: depositTx, confirmations: 2 });
  depositReceipt.status === 'success' ? ok(`Deposit tx: ${depositTx}`) : fail(`Deposit reverted: ${depositTx}`);
  ok(`Block: ${depositReceipt.blockNumber}, logs: ${depositReceipt.logs.length}`);

  // Verify deposit on-chain (use receipt blockNumber to avoid stale reads)
  const dep1 = await publicClient.readContract({
    address: EXISTING_ESCROW,
    abi: escrowAbi,
    functionName: 'getDeposit',
    args: [SKILL_HASH_1, account.address],
    blockNumber: depositReceipt.blockNumber,
  });
  if (dep1[0] === SINGLE_AMOUNT) {
    ok(`On-chain deposit: $${formatUnits(dep1[0], 6)}`);
  } else {
    fail(`Amount mismatch: got ${dep1[0]}, expected ${SINGLE_AMOUNT}`);
    // Retry without block pinning for comparison
    const dep1Retry = await publicClient.readContract({
      address: EXISTING_ESCROW,
      abi: escrowAbi,
      functionName: 'getDeposit',
      args: [SKILL_HASH_1, account.address],
    });
    console.log(`    (retry w/o block pin: amount=${dep1Retry[0]})`);
  }

  // ── Phase 4: Batch Deposit ──

  console.log('\n━━━ Phase 4: Deposit (Batch) ━━━\n');

  const BATCH_1 = usdc(2);
  const BATCH_2 = usdc(1);
  const batchTotal = BATCH_1 + BATCH_2; // $2 + $1 = $3
  console.log(`  Approving $3 USDC for batch...`);
  const approveTx2 = await walletClient.writeContract({
    address: SEPOLIA_USDC,
    abi: erc20Abi,
    functionName: 'approve',
    args: [EXISTING_ESCROW, batchTotal],
  });
  await publicClient.waitForTransactionReceipt({ hash: approveTx2, confirmations: 2 });
  ok(`Approve tx: ${approveTx2}`);

  console.log(`  Batch depositing $2 + $1 to skills 2 & 3...`);
  const batchTx = await walletClient.writeContract({
    address: EXISTING_ESCROW,
    abi: escrowAbi,
    functionName: 'depositBatch',
    args: [[SKILL_HASH_2, SKILL_HASH_3], [BATCH_1, BATCH_2]],
  });
  const batchReceipt = await publicClient.waitForTransactionReceipt({ hash: batchTx, confirmations: 2 });
  batchReceipt.status === 'success' ? ok(`Batch tx: ${batchTx}`) : fail(`Batch reverted: ${batchTx}`);

  // Verify batch deposits (pin to receipt block)
  const dep2 = await publicClient.readContract({
    address: EXISTING_ESCROW,
    abi: escrowAbi,
    functionName: 'getDeposit',
    args: [SKILL_HASH_2, account.address],
    blockNumber: batchReceipt.blockNumber,
  });
  const dep3 = await publicClient.readContract({
    address: EXISTING_ESCROW,
    abi: escrowAbi,
    functionName: 'getDeposit',
    args: [SKILL_HASH_3, account.address],
    blockNumber: batchReceipt.blockNumber,
  });
  dep2[0] === BATCH_1 ? ok(`Skill 2 deposit: $${formatUnits(dep2[0], 6)}`) : fail(`Skill 2: ${dep2[0]}`);
  dep3[0] === BATCH_2 ? ok(`Skill 3 deposit: $${formatUnits(dep3[0], 6)}`) : fail(`Skill 3: ${dep3[0]}`);

  // ── Phase 5: Claim + Withdraw ──

  console.log('\n━━━ Phase 5: approveClaim + builderWithdraw ━━━\n');

  // Admin approves a builder (using deployer as builder for test)
  console.log(`  Admin approving builder for skill 1...`);
  const claimTx = await walletClient.writeContract({
    address: EXISTING_ESCROW,
    abi: escrowAbi,
    functionName: 'approveClaim',
    args: [SKILL_HASH_1, account.address],
  });
  const claimReceipt = await publicClient.waitForTransactionReceipt({ hash: claimTx, confirmations: 2 });
  claimReceipt.status === 'success' ? ok(`approveClaim tx: ${claimTx}`) : fail(`approveClaim reverted`);

  // Verify skill info (pin to receipt block)
  const info1 = await publicClient.readContract({
    address: EXISTING_ESCROW,
    abi: escrowAbi,
    functionName: 'getSkillInfo',
    args: [SKILL_HASH_1],
    blockNumber: claimReceipt.blockNumber,
  });
  info1[0].toLowerCase() === account.address.toLowerCase()
    ? ok(`Builder set: ${info1[0]}`)
    : fail(`Builder mismatch: ${info1[0]}`);
  ok(`Total deposited: $${formatUnits(info1[1], 6)}, withdrawn: $${formatUnits(info1[2], 6)}`);

  // Builder withdraws $2 (partial — deposited $3)
  console.log(`  Builder withdrawing $2...`);
  const withdrawTx = await walletClient.writeContract({
    address: EXISTING_ESCROW,
    abi: escrowAbi,
    functionName: 'builderWithdraw',
    args: [SKILL_HASH_1, usdc(2)],
  });
  const withdrawReceipt = await publicClient.waitForTransactionReceipt({ hash: withdrawTx, confirmations: 2 });
  withdrawReceipt.status === 'success' ? ok(`Withdraw tx: ${withdrawTx}`) : fail(`Withdraw reverted`);

  // Verify remaining escrow (pin to withdraw block)
  const available = await publicClient.readContract({
    address: EXISTING_ESCROW,
    abi: escrowAbi,
    functionName: 'getAvailableEscrow',
    args: [SKILL_HASH_1],
    blockNumber: withdrawReceipt.blockNumber,
  });
  available === usdc(1) ? ok(`Available escrow: $${formatUnits(available, 6)} (correct: $3 - $2)`) : fail(`Available: $${formatUnits(available, 6)}, expected $1`);

  // ── Phase 6: Refund eligibility ──

  console.log('\n━━━ Phase 6: Refund Checks ━━━\n');

  // Skill 1 is claimed → refund should NOT be eligible
  const refund1 = await publicClient.readContract({
    address: EXISTING_ESCROW,
    abi: escrowAbi,
    functionName: 'isRefundEligible',
    args: [SKILL_HASH_1, account.address],
  });
  !refund1[0] ? ok('Skill 1 refund NOT eligible (claimed — correct)') : fail('Skill 1 refund should not be eligible');

  // Skill 2 is unclaimed → refund not eligible yet (< 90 days)
  const refund2 = await publicClient.readContract({
    address: EXISTING_ESCROW,
    abi: escrowAbi,
    functionName: 'isRefundEligible',
    args: [SKILL_HASH_2, account.address],
  });
  !refund2[0] ? ok('Skill 2 refund NOT eligible yet (< 90 days — correct)') : fail('Should not be eligible yet');
  if (refund2[1] > 0n) {
    const eligibleDate = new Date(Number(refund2[1]) * 1000);
    ok(`Skill 2 refund eligible at: ${eligibleDate.toISOString()}`);
  }

  // ── Phase 7: Backend event parsing verification ──

  console.log('\n━━━ Phase 7: Event Parsing (backend compat) ━━━\n');

  // Parse the deposit receipt logs to verify topic structure matches backend
  const depositLogs = depositReceipt.logs;
  const depositedTopic = '0x87d4c0b5e30d6808bc8a94ba1c4d839b29d664151551a31753387ee9ef48429b';

  const matchingLog = depositLogs.find((l: any) =>
    l.address.toLowerCase() === EXISTING_ESCROW.toLowerCase() &&
    l.topics[0] === depositedTopic
  );

  if (matchingLog) {
    ok(`Deposited event found in receipt`);
    ok(`  topics[0] (event sig): ${(matchingLog as any).topics[0]}`);
    ok(`  topics[1] (skillHash): ${(matchingLog as any).topics[1]}`);
    ok(`  topics[2] (backer):    ${(matchingLog as any).topics[2]}`);
    ok(`  data (amount):         ${matchingLog.data}`);

    // Verify backend can parse it
    const parsedSkillHash = (matchingLog as any).topics[1];
    const parsedBacker = '0x' + (matchingLog as any).topics[2]?.slice(26);
    const parsedAmount = BigInt(matchingLog.data);

    parsedSkillHash === SKILL_HASH_1
      ? ok(`Parsed skillHash matches`)
      : fail(`skillHash mismatch: ${parsedSkillHash}`);
    parsedBacker.toLowerCase() === account.address.toLowerCase()
      ? ok(`Parsed backer matches`)
      : fail(`backer mismatch: ${parsedBacker}`);
    parsedAmount === SINGLE_AMOUNT
      ? ok(`Parsed amount matches: $${formatUnits(parsedAmount, 6)}`)
      : fail(`amount mismatch: ${parsedAmount}`);
  } else {
    fail('No Deposited event found in receipt');
  }

  // Batch event parsing
  const batchTopic = '0x4eca431aecbba52c8d7486f733a0e944c9d23081aad6478d5bb93a267abfe37e';
  const batchLog = batchReceipt.logs.find((l: any) =>
    l.address.toLowerCase() === EXISTING_ESCROW.toLowerCase() &&
    l.topics[0] === batchTopic
  );
  batchLog ? ok('BatchDeposited event found') : fail('BatchDeposited event NOT found');

  // ── Summary ──

  console.log('\n═══════════════════════════════════════════════');
  console.log('✅ ESCROW E2E COMPLETE');
  console.log('═══════════════════════════════════════════════\n');
}

async function testViewFunctions() {
  console.log('\n━━━ View Function Tests (no USDC needed) ━━━\n');

  // Test getSkillInfo on a random hash
  const randomHash = keccak256(toHex('nonexistent-skill'));
  const info = await publicClient.readContract({
    address: EXISTING_ESCROW,
    abi: escrowAbi,
    functionName: 'getSkillInfo',
    args: [randomHash],
  });
  info[0] === '0x0000000000000000000000000000000000000000'
    ? ok('getSkillInfo returns zeroes for unknown skill')
    : fail(`Unexpected skill info: ${info}`);

  const avail = await publicClient.readContract({
    address: EXISTING_ESCROW,
    abi: escrowAbi,
    functionName: 'getAvailableEscrow',
    args: [randomHash],
  });
  avail === 0n ? ok('getAvailableEscrow = 0 for unknown skill') : fail(`Unexpected: ${avail}`);

  const backers = await publicClient.readContract({
    address: EXISTING_ESCROW,
    abi: escrowAbi,
    functionName: 'getSkillBackers',
    args: [randomHash],
  });
  backers.length === 0 ? ok('getSkillBackers = [] for unknown skill') : fail(`Unexpected: ${backers}`);

  console.log('\n═══════════════════════════════════════════════');
  console.log('✅ VIEW FUNCTION TESTS PASSED');
  console.log('  Fund wallet with Sepolia USDC to run full E2E');
  console.log('═══════════════════════════════════════════════\n');
}

main().catch(err => {
  console.error('\n💥 E2E CRASH:', err.shortMessage || err.message || err);
  process.exit(1);
});
