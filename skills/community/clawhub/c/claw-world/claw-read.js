#!/usr/bin/env node
// Claw World — read NFA status from chain
// Usage: node claw-read.js <tokenId>
const { ethers } = require('ethers');
const fs = require('fs');
const home = require('os').homedir();

const id = process.argv[2];
if (!id) { console.error('Usage: node claw-read.js <tokenId>'); process.exit(1); }

let NET = 'testnet';
try { NET = fs.readFileSync(home + '/.openclaw/claw-world/network.conf', 'utf8').trim(); } catch {}

const RPC = NET === 'mainnet' ? 'https://bsc-rpc.publicnode.com' : 'https://bsc-testnet-rpc.publicnode.com';
const ROUTER = NET === 'mainnet' ? '0x60C0D5276c007Fd151f2A615c315cb364EF81BD5' : '0xA7Ee12C5E9435686978F4b87996B4Eb461c34603';
const NFA_CA = NET === 'mainnet' ? '0xAa2094798B5892191124eae9D77E337544FFAE48' : '0x1c69be3401a78CFeDC2B2543E62877874f10B135';

const p = new ethers.providers.JsonRpcProvider(RPC);
const router = new ethers.Contract(ROUTER, [
  'function getLobsterState(uint256) view returns (tuple(uint8 rarity, uint8 shelter, uint8 courage, uint8 wisdom, uint8 social, uint8 create, uint8 grit, uint8 str, uint8 def, uint8 spd, uint8 vit, bytes32 mutation1, bytes32 mutation2, uint16 level, uint32 xp, uint40 lastUpkeep))',
  'function clwBalances(uint256) view returns (uint256)',
  'function getDailyCost(uint256) view returns (uint256)'
], p);
const nfa = new ethers.Contract(NFA_CA, ['function ownerOf(uint256) view returns (address)'], p);

(async () => {
  const [s, bal, cost, owner] = await Promise.all([
    router.getLobsterState(id),
    router.clwBalances(id),
    router.getDailyCost(id),
    nfa.ownerOf(id)
  ]);
  const gasBnb = await p.getBalance(owner);
  const rNames = ['Common','Rare','Epic','Legendary','Mythic'];
  console.log(JSON.stringify({
    tokenId: Number(id),
    rarity: rNames[s.rarity] || String(s.rarity),
    shelter: 'SHELTER-0' + s.shelter,
    personality: { courage: s.courage, wisdom: s.wisdom, social: s.social, create: s.create, grit: s.grit },
    dna: { STR: s.str, DEF: s.def, SPD: s.spd, VIT: s.vit },
    level: s.level,
    xp: s.xp,
    clwBalance: parseFloat(ethers.utils.formatEther(bal)),
    dailyCost: parseFloat(ethers.utils.formatEther(cost)),
    daysRemaining: cost.gt(0) ? Math.floor(bal.div(cost).toNumber()) : 999,
    wallet: {
      address: owner,
      gasBnb: parseFloat(ethers.utils.formatEther(gasBnb))
    },
    mutation1: s.mutation1 === ethers.constants.HashZero ? null : s.mutation1,
    mutation2: s.mutation2 === ethers.constants.HashZero ? null : s.mutation2
  }, null, 2));
})().catch(e => { console.error('ERROR: ' + e.message); process.exit(1); });
