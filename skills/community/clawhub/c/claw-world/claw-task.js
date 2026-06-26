#!/usr/bin/env node
// Claw World — submit task on-chain
// Usage: node claw-task.js <PIN> <NFA_ID> <TASK_TYPE> <XP> <CLAWORLD> <MATCH_SCORE>
// TASK_TYPE: 0=courage, 1=wisdom, 2=social, 3=create, 4=grit
// Claworld: in whole units (e.g. 50 = 50 Claworld)
const { ethers } = require('ethers');
const crypto = require('crypto');
const fs = require('fs');
const home = require('os').homedir();

const [,, pin, nfaId, taskType, xp, clw, score] = process.argv;
if (!pin || !nfaId || !taskType || !xp || !clw || !score) {
  console.error('Usage: node claw-task.js <PIN> <NFA_ID> <TASK_TYPE> <XP> <CLAWORLD> <MATCH_SCORE>');
  process.exit(1);
}

let NET = 'testnet';
try { NET = fs.readFileSync(home + '/.openclaw/claw-world/network.conf', 'utf8').trim(); } catch {}

const RPC = NET === 'mainnet' ? 'https://bsc-rpc.publicnode.com' : 'https://bsc-testnet-rpc.publicnode.com';
const TASK_CA = NET === 'mainnet' ? '0xaed370784536e31BE4A5D0Dbb1bF275c98179D10' : '0x4F8f75D6b0775b065F588F2C11C1Ec79Bb1ECE0E';
const NFA_CA = NET === 'mainnet' ? '0xAa2094798B5892191124eae9D77E337544FFAE48' : '0x1c69be3401a78CFeDC2B2543E62877874f10B135';
const ROUTER_CA = NET === 'mainnet' ? '0x60C0D5276c007Fd151f2A615c315cb364EF81BD5' : '0xA7Ee12C5E9435686978F4b87996B4Eb461c34603';

// Decrypt wallet
const data = JSON.parse(fs.readFileSync(home + '/.openclaw/claw-world/wallet.json', 'utf8'));
const key = crypto.scryptSync(pin, 'claw-world-salt', 32);
const iv = Buffer.from(data.iv, 'hex');
const dc = crypto.createDecipheriv('aes-256-cbc', key, iv);
let pk = dc.update(data.encrypted, 'hex', 'utf8');
pk += dc.final('utf8');

const provider = new ethers.providers.JsonRpcProvider(RPC);
const wallet = new ethers.Wallet(pk, provider);
const task = new ethers.Contract(TASK_CA, [
  'function ownerCompleteTypedTask(uint256,uint8,uint32,uint256,uint16)'
], wallet);
const nfaC = new ethers.Contract(NFA_CA, [
  'function ownerOf(uint256) view returns (address)'
], provider);
const router = new ethers.Contract(ROUTER_CA, [
  'function processUpkeep(uint256)'
], wallet);

(async () => {
  // Pre-check: verify this wallet owns the NFA
  const myAddr = wallet.address;
  const nfaOwner = await nfaC.ownerOf(nfaId);
  if (nfaOwner.toLowerCase() !== myAddr.toLowerCase()) {
    console.error('NOT_OWNER: NFA #' + nfaId + ' is owned by ' + nfaOwner + ', not this wallet ' + myAddr);
    console.error('Please transfer the NFA to this wallet first (use the "Transfer to OpenClaw" button on the website)');
    process.exit(1);
  }

  // Step 1: Process upkeep (deduct daily Claworld costs)
  try {
    const upkeepTx = await router.processUpkeep(nfaId, { gasLimit: 200000 });
    await upkeepTx.wait();
    console.log('UPKEEP_PROCESSED');
  } catch (e) {
    if (!e.message.includes('revert')) console.log('UPKEEP_SKIPPED: ' + e.message);
  }

  // Step 2: Submit task as NFA owner
  console.log('SUBMITTING task: NFA #' + nfaId + ', type=' + taskType + ', xp=' + xp + ', clw=' + clw + ', score=' + score);
  const tx = await task.ownerCompleteTypedTask(
    nfaId, taskType, xp,
    ethers.utils.parseEther(clw),
    score,
    { gasLimit: 500000 }
  );
  console.log('TX_SENT: ' + tx.hash);
  const r = await tx.wait();
  console.log('TX_CONFIRMED: block=' + r.blockNumber + ' gas=' + r.gasUsed.toString());
})().catch(e => {
  console.error('TX_FAILED: ' + e.message);
  process.exit(1);
});
