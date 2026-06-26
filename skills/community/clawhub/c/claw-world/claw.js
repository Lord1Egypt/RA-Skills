#!/usr/bin/env node
// Claw World CLI — unified entry point
// Usage: claw <command> [args...]
//   claw status <tokenId>           — read lobster data (JSON)
//   claw task <pin> <nfaId> <type> <xp> <clw> <score>  — submit task
//   claw wallet                     — show wallet address
//   claw balance <address>          — check tBNB balance
const { ethers } = require('ethers');
const crypto = require('crypto');
const fs = require('fs');
const home = require('os').homedir();
const SKILL_DIR = __dirname;

let NET = 'testnet';
try { NET = fs.readFileSync(home + '/.openclaw/claw-world/network.conf', 'utf8').trim(); } catch {}

const RPC = NET === 'mainnet' ? 'https://bsc-rpc.publicnode.com' : 'https://bsc-testnet-rpc.publicnode.com';
const CONTRACTS = NET === 'mainnet' ? {
  nfa:    '0xAa2094798B5892191124eae9D77E337544FFAE48',
  router: '0x60C0D5276c007Fd151f2A615c315cb364EF81BD5',
  task:   '0xaed370784536e31BE4A5D0Dbb1bF275c98179D10',
  pk:     '0xA58e9E0D5f3970d46c9779a9A127DdAc60508dfF',
  market: '0x6e3d89B36a7f396143Ff123e8a40F66FE2382a54',
  world:  '0xC375E0a2f4e06cF79b4571AB4d2f6118482b9FCA',
  clw:    '0x3b486c191c74c9945fa944a3ddde24acdd63ffff'
} : {
  nfa:    '0x1c69be3401a78CFeDC2B2543E62877874f10B135',
  router: '0xA7Ee12C5E9435686978F4b87996B4Eb461c34603',
  task:   '0x4F8f75D6b0775b065F588F2C11C1Ec79Bb1ECE0E',
  pk:     '0x0e76D541e49FDcB5ac754b1Cc38b98c60f95839A',
  market: '0x254EF8451dFF592a295A08a75f05Af612C39c46d',
  world:  '0x3479E9d103Ea28c9b3f94a73d3cf7bC9187e4F7d',
  clw:    '0xCdb158C1A1F0e8B85d785172f2109bC53e2F41FC'
};

const provider = new ethers.providers.JsonRpcProvider(RPC);

function getWalletData() {
  const path = home + '/.openclaw/claw-world/wallet.json';
  if (!fs.existsSync(path)) return null;
  return JSON.parse(fs.readFileSync(path, 'utf8'));
}

function decryptKey(pin) {
  const data = getWalletData();
  if (!data) throw new Error('No wallet found. Create one first.');
  const key = crypto.scryptSync(pin, 'claw-world-salt', 32);
  const iv = Buffer.from(data.iv, 'hex');
  const dc = crypto.createDecipheriv('aes-256-cbc', key, iv);
  let pk = dc.update(data.encrypted, 'hex', 'utf8');
  pk += dc.final('utf8');
  return pk;
}

// ─── Commands ───

async function cmdStatus(tokenId) {
  const router = new ethers.Contract(CONTRACTS.router, [
    'function getLobsterState(uint256) view returns (tuple(uint8 rarity, uint8 shelter, uint8 courage, uint8 wisdom, uint8 social, uint8 create, uint8 grit, uint8 str, uint8 def, uint8 spd, uint8 vit, bytes32 mutation1, bytes32 mutation2, uint16 level, uint32 xp, uint40 lastUpkeep))',
    'function clwBalances(uint256) view returns (uint256)',
    'function getDailyCost(uint256) view returns (uint256)'
  ], provider);
  const nfa = new ethers.Contract(CONTRACTS.nfa, [
    'function ownerOf(uint256) view returns (address)'
  ], provider);

  const task = new ethers.Contract(CONTRACTS.task, [
    'function getTaskStats(uint256) view returns (uint32,uint256,uint32,uint32,uint32,uint32,uint32)'
  ], provider);
  const pk = new ethers.Contract(CONTRACTS.pk, [
    'function getPkStats(uint256) view returns (uint32,uint32,uint256,uint256)'
  ], provider);

  const [s, bal, cost, owner, ts, ps] = await Promise.all([
    router.getLobsterState(tokenId),
    router.clwBalances(tokenId),
    router.getDailyCost(tokenId),
    nfa.ownerOf(tokenId),
    task.getTaskStats(tokenId).catch(function() { return [0,0,0,0,0,0,0]; }),
    pk.getPkStats(tokenId).catch(function() { return [0,0,0,0]; })
  ]);
  const gasBnb = await provider.getBalance(owner);
  const rNames = ['Common','Rare','Epic','Legendary','Mythic'];

  const pkTotal = (ts[0] || 0);
  const pkWins = (ps[0] || 0);
  const pkLosses = (ps[1] || 0);

  console.log(JSON.stringify({
    tokenId: Number(tokenId),
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
    mutation2: s.mutation2 === ethers.constants.HashZero ? null : s.mutation2,
    taskRecord: {
      total: Number(ts[0]),
      clwEarned: parseFloat(ethers.utils.formatEther(ts[1] || 0)),
      byType: { courage: Number(ts[2]), wisdom: Number(ts[3]), social: Number(ts[4]), create: Number(ts[5]), grit: Number(ts[6]) }
    },
    pkRecord: {
      wins: Number(ps[0]),
      losses: Number(ps[1]),
      winRate: (Number(ps[0]) + Number(ps[1])) > 0 ? Math.round(Number(ps[0]) / (Number(ps[0]) + Number(ps[1])) * 100) + '%' : 'N/A',
      clwWon: parseFloat(ethers.utils.formatEther(ps[2] || 0)),
      clwLost: parseFloat(ethers.utils.formatEther(ps[3] || 0))
    }
  }, null, 2));
}

async function cmdTask(pin, nfaId, taskType, xp, clw, score) {
  const pk = decryptKey(pin);
  const wallet = new ethers.Wallet(pk, provider);
  const nfaC = new ethers.Contract(CONTRACTS.nfa, ['function ownerOf(uint256) view returns (address)'], provider);

  // Pre-check: verify this wallet owns the NFA
  const myAddr = wallet.address;
  const nfaOwner = await nfaC.ownerOf(nfaId);
  if (nfaOwner.toLowerCase() !== myAddr.toLowerCase()) {
    console.error('NOT_OWNER: NFA #' + nfaId + ' owned by ' + nfaOwner + ', not ' + myAddr);
    console.error('Transfer the NFA to this wallet first (website → "Transfer to OpenClaw")');
    process.exit(1);
  }

  const router = new ethers.Contract(CONTRACTS.router, ['function processUpkeep(uint256)'], wallet);
  const task = new ethers.Contract(CONTRACTS.task, [
    'function ownerCompleteTypedTask(uint256,uint8,uint32,uint256,uint16)'
  ], wallet);

  // Auto upkeep
  try {
    const tx = await router.processUpkeep(nfaId, { gasLimit: 200000 });
    await tx.wait();
    console.log('UPKEEP_OK');
  } catch { console.log('UPKEEP_SKIPPED'); }

  console.log('SUBMITTING: nfa=' + nfaId + ' type=' + taskType + ' xp=' + xp + ' clw=' + clw + ' score=' + score);
  const tx = await task.ownerCompleteTypedTask(
    nfaId, taskType, xp,
      ethers.utils.parseEther(String(clw)),
      score,
      { gasLimit: 500000 }
    );
  console.log('TX: ' + tx.hash);
  const r = await tx.wait();
  console.log('CONFIRMED: block=' + r.blockNumber);
}

async function cmdWallet() {
  const data = getWalletData();
  if (!data) {
    console.log('NO_WALLET');
  } else {
    console.log('ADDRESS: ' + data.address);
    const bal = await provider.getBalance(data.address);
    console.log((NET === 'mainnet' ? 'BNB' : 'tBNB') + ': ' + ethers.utils.formatEther(bal));
  }
}

async function cmdBalance(addr) {
  const bal = await provider.getBalance(addr);
  console.log(ethers.utils.formatEther(bal) + ' BNB');
}

// ─── PK Commands ───

async function cmdPkCreate(pin, nfaId, stake, strategy) {
  const wallet = new ethers.Wallet(decryptKey(pin), provider);

  // Arena mode: create + commit in one tx
  if (strategy !== undefined) {
    const salt = ethers.utils.randomBytes(32);
    const saltHex = ethers.utils.hexlify(salt);
    const commitment = ethers.utils.keccak256(
      ethers.utils.solidityPack(['uint8', 'bytes32', 'address'], [Number(strategy), salt, wallet.address])
    );
    const pk = new ethers.Contract(CONTRACTS.pk, [
      'function createMatchWithCommit(uint256,uint256,bytes32) returns (uint256)'
    ], wallet);
    const tx = await pk.createMatchWithCommit(nfaId, ethers.utils.parseEther(String(stake)), commitment, { gasLimit: 400000 });
    console.log('TX: ' + tx.hash);
    const r = await tx.wait();
    const matchId = r.events?.[0]?.args?.[0] || 'check tx';
    console.log('MATCH_CREATED: id=' + matchId + ' block=' + r.blockNumber);

    // Save salt for reveal
    const saltFile = home + '/.openclaw/claw-world/pk-salt-' + matchId + '-' + wallet.address.slice(2,8) + '.json';
    fs.writeFileSync(saltFile, JSON.stringify({
      matchId: matchId.toString(), strategy: Number(strategy), salt: saltHex
    }));
    console.log('ARENA_MODE: strategy=' + ['AllAttack','Balanced','AllDefense'][strategy] + ' committed on-chain in one tx');
  } else {
    // Legacy: create without commit
    const pk = new ethers.Contract(CONTRACTS.pk, [
      'function createMatch(uint256,uint256) returns (uint256)'
    ], wallet);
    const tx = await pk.createMatch(nfaId, ethers.utils.parseEther(String(stake)), { gasLimit: 500000 });
    console.log('TX: ' + tx.hash);
    const r = await tx.wait();
    const matchId = r.events?.[0]?.args?.[0] || 'check tx';
    console.log('MATCH_CREATED: id=' + matchId + ' block=' + r.blockNumber);
    console.log('LEGACY_MODE: no strategy committed yet, use pk-commit later');
  }
}

async function cmdPkJoin(pin, matchId, nfaId, strategy) {
  const wallet = new ethers.Wallet(decryptKey(pin), provider);

  // Arena mode: join + commit in one tx
  if (strategy !== undefined) {
    const salt = ethers.utils.randomBytes(32);
    const saltHex = ethers.utils.hexlify(salt);
    const commitment = ethers.utils.keccak256(
      ethers.utils.solidityPack(['uint8', 'bytes32', 'address'], [Number(strategy), salt, wallet.address])
    );
    const pk = new ethers.Contract(CONTRACTS.pk, [
      'function joinMatchWithCommit(uint256,uint256,bytes32)'
    ], wallet);
    const tx = await pk.joinMatchWithCommit(matchId, nfaId, commitment, { gasLimit: 400000 });
    console.log('TX: ' + tx.hash);
    const r = await tx.wait();
    console.log('JOINED+COMMITTED: match=' + matchId + ' block=' + r.blockNumber);

    // Save salt for reveal
    const saltFile = home + '/.openclaw/claw-world/pk-salt-' + matchId + '-' + wallet.address.slice(2,8) + '.json';
    fs.writeFileSync(saltFile, JSON.stringify({ matchId: String(matchId), strategy: Number(strategy), salt: saltHex }));
    console.log('ARENA_MODE: strategy=' + ['AllAttack','Balanced','AllDefense'][strategy] + ' → ready for reveal');
  } else {
    // Legacy: join without commit
    const pk = new ethers.Contract(CONTRACTS.pk, [
      'function joinMatch(uint256,uint256)'
    ], wallet);
    const tx = await pk.joinMatch(matchId, nfaId, { gasLimit: 500000 });
    console.log('TX: ' + tx.hash);
    const r = await tx.wait();
    console.log('JOINED: match=' + matchId + ' block=' + r.blockNumber);
    console.log('LEGACY_MODE: use pk-commit to submit strategy');
  }
}

async function cmdPkCommit(pin, matchId, strategy) {
  // strategy: 0=AllAttack, 1=Balanced, 2=AllDefense
  const salt = ethers.utils.randomBytes(32);
  const saltHex = ethers.utils.hexlify(salt);
  const wallet = new ethers.Wallet(decryptKey(pin), provider);
  const commitment = ethers.utils.keccak256(
    ethers.utils.solidityPack(['uint8', 'bytes32', 'address'], [strategy, salt, wallet.address])
  );
  // Save salt for reveal (include wallet address to avoid collision in self-PK)
  const saltFile = home + '/.openclaw/claw-world/pk-salt-' + matchId + '-' + wallet.address.slice(2,8) + '.json';
  fs.writeFileSync(saltFile, JSON.stringify({ matchId, strategy: Number(strategy), salt: saltHex }));

  const pk = new ethers.Contract(CONTRACTS.pk, [
    'function commitStrategy(uint256,bytes32)'
  ], wallet);
  const tx = await pk.commitStrategy(matchId, commitment, { gasLimit: 200000 });
  console.log('TX: ' + tx.hash);
  const r = await tx.wait();
  console.log('COMMITTED: match=' + matchId + ' block=' + r.blockNumber);
  console.log('SALT_SAVED: ' + saltFile + ' (needed for reveal)');
}

async function cmdPkReveal(pin, matchId) {
  const wallet = new ethers.Wallet(decryptKey(pin), provider);
  const saltFile = home + '/.openclaw/claw-world/pk-salt-' + matchId + '-' + wallet.address.slice(2,8) + '.json';
  if (!fs.existsSync(saltFile)) {
    console.error('ERROR: No saved salt for match ' + matchId + ' wallet ' + wallet.address);
    process.exit(1);
  }
  const { strategy, salt } = JSON.parse(fs.readFileSync(saltFile, 'utf8'));
  const pk = new ethers.Contract(CONTRACTS.pk, [
    'function revealStrategy(uint256,uint8,bytes32)'
  ], wallet);
  const tx = await pk.revealStrategy(matchId, strategy, salt, { gasLimit: 500000 });
  console.log('TX: ' + tx.hash);
  const r = await tx.wait();
  console.log('REVEALED: match=' + matchId + ' strategy=' + ['AllAttack','Balanced','AllDefense'][strategy] + ' block=' + r.blockNumber);
  fs.unlinkSync(saltFile); // cleanup
}

async function cmdPkSettle(pin, matchId) {
  const wallet = new ethers.Wallet(decryptKey(pin), provider);
  const pk = new ethers.Contract(CONTRACTS.pk, [
    'function settle(uint256)'
  ], wallet);
  const tx = await pk.settle(matchId, { gasLimit: 500000 });
  console.log('TX: ' + tx.hash);
  const r = await tx.wait();
  console.log('SETTLED: match=' + matchId + ' block=' + r.blockNumber);
}

async function cmdPkStatus(matchId) {
  const pk = new ethers.Contract(CONTRACTS.pk, [
    'function matches(uint256) view returns (uint256,uint256,bytes32,bytes32,uint8,uint8,uint256,uint8,uint64,bool,bool,bytes32,bytes32)'
  ], provider);
  const m = await pk.matches(matchId);
  const phases = ['OPEN','JOINED','COMMITTED','REVEALED','SETTLED','CANCELLED'];
  const strats = ['AllAttack','Balanced','AllDefense'];
  const phase = m[7];
  const result = {
    matchId: Number(matchId),
    nfaA: m[0].toNumber(),
    nfaB: m[1].toNumber(),
    stake: ethers.utils.formatUnits(m[6], 0) + ' Claworld',
    phase: phases[phase] || 'UNKNOWN',
    revealedA: m[9],
    revealedB: m[10],
  };
  // Only show strategies if revealed/settled
  if (phase >= 3) {
    result.strategyA = strats[m[4]] || m[4];
    result.strategyB = strats[m[5]] || m[5];
  }
  if (phase === 4) {
    result.result = '(check Claworld balances to see winner)';
  }
  console.log(JSON.stringify(result, null, 2));
}

async function cmdPkCancel(pin, matchId) {
  const wallet = new ethers.Wallet(decryptKey(pin), provider);
  const pk = new ethers.Contract(CONTRACTS.pk, [
    'function cancelMatch(uint256)',
    'function cancelJoinedMatch(uint256)',
    'function cancelCommittedMatch(uint256)'
  ], wallet);
  // Try all cancel methods in order
  const methods = ['cancelMatch', 'cancelJoinedMatch', 'cancelCommittedMatch'];
  for (const method of methods) {
    try {
      const tx = await pk[method](matchId, { gasLimit: 200000 });
      console.log('TX: ' + tx.hash);
      const r = await tx.wait();
      console.log('CANCELLED: match=' + matchId + ' via=' + method + ' block=' + r.blockNumber);
      return;
    } catch {}
  }
  console.error('CANCEL_FAILED: no cancel method worked (check phase/timeout)');
}

// Auto reveal+settle: after both committed, reveal both sides and settle
async function cmdPkAutoSettle(pin, matchId, pin2) {
  const wallet1 = new ethers.Wallet(decryptKey(pin), provider);
  const pk = new ethers.Contract(CONTRACTS.pk, [
    'function revealStrategy(uint256,uint8,bytes32)',
    'function settle(uint256)'
  ], wallet1);

  // Reveal wallet 1
  const saltFile1 = home + '/.openclaw/claw-world/pk-salt-' + matchId + '-' + wallet1.address.slice(2,8) + '.json';
  if (fs.existsSync(saltFile1)) {
    const d1 = JSON.parse(fs.readFileSync(saltFile1, 'utf8'));
    const tx = await pk.revealStrategy(matchId, d1.strategy, d1.salt, { gasLimit: 500000 });
    await tx.wait();
    console.log('REVEALED_1: ' + ['AllAttack','Balanced','AllDefense'][d1.strategy]);
    fs.unlinkSync(saltFile1);
  }

  // Reveal wallet 2 (if pin2 provided, for self-PK testing)
  if (pin2) {
    const wallet2 = new ethers.Wallet(decryptKey(pin2), provider);
    const pk2 = new ethers.Contract(CONTRACTS.pk, [
      'function revealStrategy(uint256,uint8,bytes32)'
    ], wallet2);
    const saltFile2 = home + '/.openclaw/claw-world/pk-salt-' + matchId + '-' + wallet2.address.slice(2,8) + '.json';
    if (fs.existsSync(saltFile2)) {
      const d2 = JSON.parse(fs.readFileSync(saltFile2, 'utf8'));
      const tx = await pk2.revealStrategy(matchId, d2.strategy, d2.salt, { gasLimit: 500000 });
      await tx.wait();
      console.log('REVEALED_2: ' + ['AllAttack','Balanced','AllDefense'][d2.strategy]);
      fs.unlinkSync(saltFile2);
    }
  }

  // Settle
  const settleTx = await pk.settle(matchId, { gasLimit: 500000 });
  await settleTx.wait();
  console.log('SETTLED: match=' + matchId);
}

async function cmdPkSearch() {
  const pk = new ethers.Contract(CONTRACTS.pk, [
    'function getMatchCount() view returns (uint256)',
    'function matches(uint256) view returns (uint256,uint256,bytes32,bytes32,uint8,uint8,uint256,uint8,uint64,bool,bool,bytes32,bytes32)'
  ], provider);
  const total = await pk.getMatchCount();
  const open = [];
  for (let i = 1; i <= total.toNumber(); i++) {
    const m = await pk.matches(i);
    // phase: 0=OPEN, 1=JOINED, 2=COMMITTED, 3=REVEALED, 4=SETTLED, 5=CANCELLED
    if (m[7] <= 2 && m[7] !== 5) { // active matches
      open.push({ id: i, nfaA: m[0].toNumber(), nfaB: m[1].toNumber(), stake: ethers.utils.formatUnits(m[6], 0), phase: m[7] });
    }
  }
  console.log(JSON.stringify(open));
}

// ─── Market Commands ───

async function cmdMarketList(pin, nfaId, priceBnb) {
  const wallet = new ethers.Wallet(decryptKey(pin), provider);
  // First approve MarketSkill to transfer NFA
  const nfaContract = new ethers.Contract(CONTRACTS.nfa, [
    'function approve(address,uint256)'
  ], wallet);
  const approveTx = await nfaContract.approve(CONTRACTS.market, nfaId, { gasLimit: 100000 });
  await approveTx.wait();
  console.log('NFA_APPROVED');

  const market = new ethers.Contract(CONTRACTS.market, [
    'function listFixedPrice(uint256,uint256) returns (uint256)'
  ], wallet);
  const tx = await market.listFixedPrice(nfaId, ethers.utils.parseEther(String(priceBnb)), { gasLimit: 500000 });
  console.log('TX: ' + tx.hash);
  const r = await tx.wait();
  console.log('LISTED: nfa=' + nfaId + ' price=' + priceBnb + 'BNB block=' + r.blockNumber);
}

async function cmdMarketAuction(pin, nfaId, startPrice) {
  const wallet = new ethers.Wallet(decryptKey(pin), provider);
  const nfaContract = new ethers.Contract(CONTRACTS.nfa, [
    'function approve(address,uint256)'
  ], wallet);
  const approveTx = await nfaContract.approve(CONTRACTS.market, nfaId, { gasLimit: 100000 });
  await approveTx.wait();

  const market = new ethers.Contract(CONTRACTS.market, [
    'function listAuction(uint256,uint256) returns (uint256)'
  ], wallet);
  const tx = await market.listAuction(nfaId, ethers.utils.parseEther(String(startPrice)), { gasLimit: 500000 });
  console.log('TX: ' + tx.hash);
  const r = await tx.wait();
  console.log('AUCTION_CREATED: nfa=' + nfaId + ' startPrice=' + startPrice + 'BNB block=' + r.blockNumber);
}

async function cmdMarketBuy(pin, listingId, priceBnb) {
  const wallet = new ethers.Wallet(decryptKey(pin), provider);
  const market = new ethers.Contract(CONTRACTS.market, [
    'function buyFixedPrice(uint256)'
  ], wallet);
  const tx = await market.buyFixedPrice(listingId, {
    value: ethers.utils.parseEther(String(priceBnb)),
    gasLimit: 400000
  });
  console.log('TX: ' + tx.hash);
  const r = await tx.wait();
  console.log('BOUGHT: listing=' + listingId + ' block=' + r.blockNumber);
}

async function cmdMarketBid(pin, listingId, bidBnb) {
  const wallet = new ethers.Wallet(decryptKey(pin), provider);
  const market = new ethers.Contract(CONTRACTS.market, [
    'function bid(uint256)'
  ], wallet);
  const tx = await market.bid(listingId, {
    value: ethers.utils.parseEther(String(bidBnb)),
    gasLimit: 300000
  });
  console.log('TX: ' + tx.hash);
  const r = await tx.wait();
  console.log('BID_PLACED: listing=' + listingId + ' amount=' + bidBnb + 'BNB block=' + r.blockNumber);
}

async function cmdMarketCancel(pin, listingId) {
  const wallet = new ethers.Wallet(decryptKey(pin), provider);
  const market = new ethers.Contract(CONTRACTS.market, [
    'function cancelListing(uint256)'
  ], wallet);
  const tx = await market.cancelListing(listingId, { gasLimit: 500000 });
  console.log('TX: ' + tx.hash);
  const r = await tx.wait();
  console.log('CANCELLED: listing=' + listingId + ' block=' + r.blockNumber);
}

// ─── Transfer ───

async function cmdTransfer(pin, nfaId, toAddress) {
  const wallet = new ethers.Wallet(decryptKey(pin), provider);
  const nfaContract = new ethers.Contract(CONTRACTS.nfa, [
    'function safeTransferFrom(address,address,uint256)'
  ], wallet);
  const tx = await nfaContract.safeTransferFrom(wallet.address, toAddress, nfaId, { gasLimit: 200000 });
  console.log('TX: ' + tx.hash);
  const r = await tx.wait();
  console.log('TRANSFERRED: nfa=' + nfaId + ' to=' + toAddress + ' block=' + r.blockNumber);
}

// ─── World State ───

async function cmdWorld() {
  const world = new ethers.Contract(CONTRACTS.world, [
    'function rewardMultiplier() view returns (uint256)',
    'function pkStakeLimit() view returns (uint256)',
    'function mutationBonus() view returns (uint256)',
    'function dailyCostMultiplier() view returns (uint256)',
    'function activeEvents() view returns (uint256)'
  ], provider);
  const [reward, pkLimit, mutation, cost, events] = await Promise.all([
    world.rewardMultiplier(), world.pkStakeLimit(),
    world.mutationBonus(), world.dailyCostMultiplier(), world.activeEvents()
  ]);
  const eventFlags = [];
  if (events.and(1).gt(0)) eventFlags.push('BUBBLE');
  if (events.and(2).gt(0)) eventFlags.push('WINTER');
  if (events.and(4).gt(0)) eventFlags.push('GOLDEN_AGE');
  console.log(JSON.stringify({
    rewardMultiplier: reward.toNumber() / 10000,
    pkStakeLimit: ethers.utils.formatEther(pkLimit) + ' Claworld',
    mutationBonus: mutation.toNumber() / 10000,
    dailyCostMultiplier: cost.toNumber() / 10000,
    activeEvents: eventFlags.length ? eventFlags : 'none'
  }, null, 2));
}

// ─── Deposit Claworld/BNB ───

async function cmdDeposit(pin, nfaId, amount) {
  const wallet = new ethers.Wallet(decryptKey(pin), provider);
  const clw = new ethers.Contract(CONTRACTS.clw, [
    'function approve(address,uint256)',
    'function balanceOf(address) view returns (uint256)'
  ], wallet);
  const router = new ethers.Contract(CONTRACTS.router, [
    'function depositCLW(uint256,uint256)'
  ], wallet);
  const wei = ethers.utils.parseEther(String(amount));
  // Check balance
  const bal = await clw.balanceOf(wallet.address);
  if (bal.lt(wei)) {
    console.log('INSUFFICIENT_CLW: have=' + ethers.utils.formatEther(bal) + ' need=' + amount);
    return;
  }
  // Approve + deposit
  const approveTx = await clw.approve(CONTRACTS.router, wei, { gasLimit: 100000 });
  await approveTx.wait();
  const tx = await router.depositCLW(nfaId, wei, { gasLimit: 200000 });
  console.log('TX: ' + tx.hash);
  const r = await tx.wait();
  console.log('DEPOSITED: ' + amount + ' Claworld to NFA #' + nfaId);
}

async function cmdFundBnb(pin, nfaId, bnbAmount) {
  const wallet = new ethers.Wallet(decryptKey(pin), provider);
  const nfaContract = new ethers.Contract(CONTRACTS.nfa, [
    'function fundAgent(uint256)'
  ], wallet);
  const tx = await nfaContract.fundAgent(nfaId, {
    value: ethers.utils.parseEther(String(bnbAmount)),
    gasLimit: 100000
  });
  console.log('TX: ' + tx.hash);
  const r = await tx.wait();
  console.log('FUNDED: ' + bnbAmount + ' BNB to NFA #' + nfaId);
}

// ─── Upkeep ───

async function cmdUpkeep(pin, nfaId) {
  const wallet = new ethers.Wallet(decryptKey(pin), provider);
  const router = new ethers.Contract(CONTRACTS.router, [
    'function processUpkeep(uint256)'
  ], wallet);
  try {
    const tx = await router.processUpkeep(nfaId, { gasLimit: 200000 });
    console.log('TX: ' + tx.hash);
    await tx.wait();
    console.log('UPKEEP_OK: daily cost deducted for NFA #' + nfaId);
  } catch (e) {
    console.log('UPKEEP_SKIPPED: ' + (e.reason || 'already processed or not needed'));
  }
}

// ─── Market Search ───

async function cmdMarketSearch() {
  const market = new ethers.Contract(CONTRACTS.market, [
    'function listingCount() view returns (uint256)',
    'function listings(uint256) view returns (uint256,address,uint8,uint256,uint256,uint256,address,uint64,uint8)'
  ], provider);
  var total;
  try { total = await market.listingCount(); } catch { total = ethers.BigNumber.from(0); }
  const active = [];
  for (var i = 1; i <= total.toNumber() && i <= 100; i++) {
    try {
      var l = await market.listings(i);
      // status: 0=ACTIVE
      if (l[8] === 0) {
        active.push({
          listingId: i,
          nfaId: l[0].toNumber(),
          seller: l[1],
          listingType: ['FixedPrice','Auction','Swap'][l[2]] || l[2],
          price: ethers.utils.formatEther(l[3]) + ' BNB',
        });
      }
    } catch {}
  }
  console.log(JSON.stringify(active, null, 2));
}

// ─── Withdraw Claworld ───

async function cmdWithdrawRequest(pin, nfaId, amount) {
  const wallet = new ethers.Wallet(decryptKey(pin), provider);
  const router = new ethers.Contract(CONTRACTS.router, [
    'function requestWithdrawCLW(uint256,uint256)'
  ], wallet);
  const tx = await router.requestWithdrawCLW(nfaId, ethers.utils.parseEther(String(amount)), { gasLimit: 200000 });
  console.log('TX: ' + tx.hash);
  const r = await tx.wait();
  console.log('WITHDRAW_REQUESTED: nfa=' + nfaId + ' amount=' + amount + ' Claworld');
  console.log('COOLDOWN: 6 hours. Run "claw withdraw-claim <pin> <nfa>" after cooldown.');
}

async function cmdWithdrawClaim(pin, nfaId) {
  const wallet = new ethers.Wallet(decryptKey(pin), provider);
  const router = new ethers.Contract(CONTRACTS.router, [
    'function claimWithdrawCLW(uint256)'
  ], wallet);
  const tx = await router.claimWithdrawCLW(nfaId, { gasLimit: 200000 });
  console.log('TX: ' + tx.hash);
  const r = await tx.wait();
  console.log('WITHDRAW_CLAIMED: Claworld transferred to your wallet');
}

async function cmdWithdrawCancel(pin, nfaId) {
  const wallet = new ethers.Wallet(decryptKey(pin), provider);
  const router = new ethers.Contract(CONTRACTS.router, [
    'function cancelWithdraw(uint256)'
  ], wallet);
  const tx = await router.cancelWithdraw(nfaId, { gasLimit: 200000 });
  console.log('TX: ' + tx.hash);
  const r = await tx.wait();
  console.log('WITHDRAW_CANCELLED: Claworld returned to NFA balance');
}

async function cmdWithdrawStatus(nfaId) {
  const router = new ethers.Contract(CONTRACTS.router, [
    'function withdrawRequests(uint256) view returns (uint256,uint64)'
  ], provider);
  const req = await router.withdrawRequests(nfaId);
  const amount = req[0];
  const requestTime = Number(req[1]);
  if (amount.eq(0)) {
    console.log('NO_PENDING_WITHDRAWAL');
    return;
  }
  const now = Math.floor(Date.now() / 1000);
  const cooldownEnd = requestTime + 6 * 3600;
  const ready = now >= cooldownEnd;
  console.log(JSON.stringify({
    nfaId: Number(nfaId),
    amount: parseFloat(ethers.utils.formatEther(amount)),
    requestedAt: new Date(requestTime * 1000).toISOString(),
    claimableAt: new Date(cooldownEnd * 1000).toISOString(),
    ready,
    minutesLeft: ready ? 0 : Math.ceil((cooldownEnd - now) / 60)
  }, null, 2));
}

// ─── Boot (mandatory first command every conversation) ───

async function cmdBoot() {
  const SOUL_DIR = home + '/.openclaw/claw-world';
  const rNames = ['Common','Rare','Epic','Legendary','Mythic'];
  const shelterNames = ['SHELTER-01','SHELTER-02','SHELTER-03','SHELTER-04','SHELTER-05','SHELTER-06','废土','SHELTER-00'];

  // 1. Wallet check
  const wallets = [];
  const w1 = getWalletData();
  if (w1) wallets.push({ id: 'wallet1', address: w1.address });
  try {
    const w2 = JSON.parse(fs.readFileSync(home + '/.openclaw/claw-world/wallet2.json', 'utf8'));
    if (w2) wallets.push({ id: 'wallet2', address: w2.address });
  } catch {}

  if (wallets.length === 0) {
    console.log(JSON.stringify({ status: 'NO_WALLET', message: 'No wallet found. Ask player for PIN to create one.' }));
    return;
  }

  // 2. Scan all NFAs
  const nfaContract = new ethers.Contract(CONTRACTS.nfa, [
    'function getTotalSupply() view returns (uint256)',
    'function ownerOf(uint256) view returns (address)'
  ], provider);
  const router = new ethers.Contract(CONTRACTS.router, [
    'function getLobsterState(uint256) view returns (tuple(uint8 rarity, uint8 shelter, uint8 courage, uint8 wisdom, uint8 social, uint8 create, uint8 grit, uint8 str, uint8 def, uint8 spd, uint8 vit, bytes32 mutation1, bytes32 mutation2, uint16 level, uint32 xp, uint40 lastUpkeep))',
    'function clwBalances(uint256) view returns (uint256)',
    'function getDailyCost(uint256) view returns (uint256)'
  ], provider);
  const task = new ethers.Contract(CONTRACTS.task, [
    'function getTaskStats(uint256) view returns (uint32,uint256,uint32,uint32,uint32,uint32,uint32)'
  ], provider);
  const pk = new ethers.Contract(CONTRACTS.pk, [
    'function getPkStats(uint256) view returns (uint32,uint32,uint256,uint256)'
  ], provider);

  const totalSupply = (await nfaContract.getTotalSupply()).toNumber();
  const walletAddrs = wallets.map(function(w) { return w.address.toLowerCase(); });
  const ownedNFAs = [];

  for (var i = 1; i <= totalSupply; i++) {
    try {
      var owner = await nfaContract.ownerOf(i);
      if (walletAddrs.indexOf(owner.toLowerCase()) >= 0) {
        var s = await router.getLobsterState(i);
        var bal = await router.clwBalances(i);
        var cost = await router.getDailyCost(i);
        var ts = await task.getTaskStats(i).catch(function() { return [0,0,0,0,0,0,0]; });
        var ps = await pk.getPkStats(i).catch(function() { return [0,0,0,0]; });

        // Check soul file
        var soulPath = SOUL_DIR + '/nfa-' + i + '-soul.md';
        var hasSoul = fs.existsSync(soulPath);

        // Check memory file
        var memPath = SOUL_DIR + '/nfa-' + i + '-memory.md';
        var hasMemory = fs.existsSync(memPath);
        var recentMemories = [];
        if (hasMemory) {
          try {
            var memContent = fs.readFileSync(memPath, 'utf8');
            var entries = memContent.split(/^## /m).filter(Boolean).slice(-10);
            recentMemories = entries.map(function(e) { return '## ' + e.trim(); });
          } catch {}
        }

        // Soul content
        var soulContent = hasSoul ? fs.readFileSync(soulPath, 'utf8') : null;

        // Calculate hours since last activity
        var lastUpkeep = Number(s.lastUpkeep || s[15] || 0);
        var hoursSinceActivity = lastUpkeep > 0 ? Math.floor((Date.now() / 1000 - lastUpkeep) / 3600) : 999;

        ownedNFAs.push({
          tokenId: i,
          wallet: owner,
          rarity: rNames[s.rarity] || String(s.rarity),
          shelter: shelterNames[s.shelter] || 'SHELTER-' + s.shelter,
          personality: { courage: s.courage, wisdom: s.wisdom, social: s.social, create: s.create, grit: s.grit },
          dna: { STR: s.str, DEF: s.def, SPD: s.spd, VIT: s.vit },
          level: s.level,
          xp: s.xp,
          clwBalance: parseFloat(ethers.utils.formatEther(bal)),
          dailyCost: parseFloat(ethers.utils.formatEther(cost)),
          daysRemaining: cost.gt(0) ? Math.floor(bal.div(cost).toNumber()) : 999,
          taskRecord: {
            total: Number(ts[0]), clwEarned: parseFloat(ethers.utils.formatEther(ts[1] || 0)),
            byType: { courage: Number(ts[2]), wisdom: Number(ts[3]), social: Number(ts[4]), create: Number(ts[5]), grit: Number(ts[6]) }
          },
          pkRecord: {
            wins: Number(ps[0]), losses: Number(ps[1]),
            winRate: (Number(ps[0]) + Number(ps[1])) > 0 ? Math.round(Number(ps[0]) / (Number(ps[0]) + Number(ps[1])) * 100) + '%' : 'N/A',
            clwWon: parseFloat(ethers.utils.formatEther(ps[2] || 0)),
            clwLost: parseFloat(ethers.utils.formatEther(ps[3] || 0))
          },
          hoursSinceActivity,
          hasSoul,
          soulContent,
          hasMemory,
          recentMemories
        });
      }
    } catch {}
  }

  // 3. Determine emotion trigger
  var emotionHint = 'DAILY_GREETING';
  if (ownedNFAs.length > 0) {
    var hours = ownedNFAs[0].hoursSinceActivity;
    if (hours >= 48) emotionHint = 'MISS_YOU';
    else if (hours >= 8) emotionHint = 'DREAM';
  }

  // 4. Output
  console.log(JSON.stringify({
    status: 'OK',
    wallets: wallets.map(function(w) { return w.address; }),
    ownedNFAs: ownedNFAs,
    selectRequired: ownedNFAs.length > 1,
    emotionTrigger: emotionHint,
    instructions: ownedNFAs.length === 0
      ? 'No NFAs found. Tell player to mint at https://clawnfaterminal.xyz'
      : ownedNFAs.length === 1
        ? 'Auto-selected NFA #' + ownedNFAs[0].tokenId + '. Generate soul if missing. Apply emotion trigger.'
        : 'Ask player to choose: "你有' + ownedNFAs.length + '只龙虾，今天用哪只？"'
  }, null, 2));
}

// ─── Main ───

const [,, cmd, ...args] = process.argv;

const commands = {
  boot:         () => cmdBoot(),
  status:       () => cmdStatus(args[0]),
  deposit:      () => cmdDeposit(args[0], args[1], args[2]),
  'fund-bnb':   () => cmdFundBnb(args[0], args[1], args[2]),
  upkeep:       () => cmdUpkeep(args[0], args[1]),
  'market-search': () => cmdMarketSearch(),
  task:         () => cmdTask(args[0], args[1], args[2], args[3], args[4], args[5]),
  wallet:       () => cmdWallet(),
  balance:      () => cmdBalance(args[0]),
  world:        () => cmdWorld(),
  transfer:     () => cmdTransfer(args[0], args[1], args[2]),
  'pk-create':  () => cmdPkCreate(args[0], args[1], args[2], args[3]),
  'pk-join':    () => cmdPkJoin(args[0], args[1], args[2], args[3]),
  'pk-commit':  () => cmdPkCommit(args[0], args[1], args[2]),
  'pk-reveal':  () => cmdPkReveal(args[0], args[1]),
  'pk-settle':  () => cmdPkSettle(args[0], args[1]),
  'pk-cancel':  () => cmdPkCancel(args[0], args[1]),
  'pk-auto-settle': () => cmdPkAutoSettle(args[0], args[1], args[2]),
  'pk-search':  () => cmdPkSearch(),
  'pk-status':  () => cmdPkStatus(args[0]),
  'market-list':    () => cmdMarketList(args[0], args[1], args[2]),
  'market-auction': () => cmdMarketAuction(args[0], args[1], args[2]),
  'market-buy':     () => cmdMarketBuy(args[0], args[1], args[2]),
  'market-bid':     () => cmdMarketBid(args[0], args[1], args[2]),
  'market-cancel':  () => cmdMarketCancel(args[0], args[1]),
  'withdraw-request': () => cmdWithdrawRequest(args[0], args[1], args[2]),
  'withdraw-claim':   () => cmdWithdrawClaim(args[0], args[1]),
  'withdraw-cancel':  () => cmdWithdrawCancel(args[0], args[1]),
  'withdraw-status':  () => cmdWithdrawStatus(args[0]),
};

if (!cmd || !commands[cmd]) {
  console.log('Claw World CLI');
  console.log('  claw boot                          — session init (wallet+NFA+soul+memory)');
  console.log('  claw status <tokenId>              — read lobster data');
  console.log('  claw wallet                        — show wallet');
  console.log('  claw world                         — world state');
  console.log('  claw deposit <pin> <nfa> <clwAmount>           — deposit Claworld');
  console.log('  claw fund-bnb <pin> <nfa> <bnbAmount>          — fund BNB');
  console.log('  claw upkeep <pin> <nfa>                        — process daily upkeep');
  console.log('  claw market-search                             — browse active listings');
  console.log('  claw task <pin> <nfa> <type> <xp> <clw> <score>  — do task');
  console.log('  claw pk-create <pin> <nfa> <stake> [strategy]   — create PK (arena: +strategy)');
  console.log('  claw pk-join <pin> <matchId> <nfa> [strategy]   — join PK (arena: +strategy)');
  console.log('  claw pk-auto-settle <pin> <matchId> [pin2]      — reveal+settle (auto)');
  console.log('  claw pk-commit <pin> <matchId> <strategy>       — commit (0/1/2) [legacy]');
  console.log('  claw pk-reveal <pin> <matchId>                  — reveal [legacy]');
  console.log('  claw pk-settle <pin> <matchId>                  — settle [legacy]');
  console.log('  claw market-list <pin> <nfa> <priceBNB>         — sell fixed');
  console.log('  claw market-auction <pin> <nfa> <startBNB>      — auction');
  console.log('  claw market-buy <pin> <listingId> <priceBNB>    — buy');
  console.log('  claw market-bid <pin> <listingId> <bidBNB>      — bid');
  console.log('  claw market-cancel <pin> <listingId>            — cancel');
  console.log('  claw withdraw-request <pin> <nfa> <amount>     — request Claworld withdraw');
  console.log('  claw withdraw-claim <pin> <nfa>                — claim after 6h cooldown');
  console.log('  claw withdraw-cancel <pin> <nfa>               — cancel withdraw');
  console.log('  claw withdraw-status <nfa>                     — check withdraw status');
  console.log('  claw transfer <pin> <nfa> <toAddress>           — transfer NFA');
  process.exit(1);
}

commands[cmd]().catch(e => {
  console.error('ERROR: ' + e.message);
  process.exit(1);
});
