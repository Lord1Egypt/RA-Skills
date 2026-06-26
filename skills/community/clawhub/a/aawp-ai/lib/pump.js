/**
 * AAWP Pump.fun Full Integration
 * Uses @pump-fun/pump-sdk (bonding curve) + @pump-fun/pump-swap-sdk (AMM)
 *
 * Features:
 *   Trading:    buy, sell (bonding curve + AMM auto-detect)
 *   Launch:     createToken, createAndBuy
 *   Pricing:    getQuote, marketCap, bondingCurveInfo
 *   Fees:       creatorFees, distributeFees, createFeeSharing, claimCashback
 *   Incentives: claimIncentives, unclaimedTokens
 *   AMM:        ammBuy, ammSell, deposit, withdraw
 *   Utils:      findPda, isGraduated, tokenProgram detection
 */
'use strict';

const BN = require('bn.js');
const { PublicKey, Connection, Transaction, ComputeBudgetProgram, Keypair, SystemProgram } = require('@solana/web3.js');
const { TOKEN_PROGRAM_ID, TOKEN_2022_PROGRAM_ID } = require('@solana/spl-token');

let _sdk, _pumpSdk, _onlineSdk;

function getPumpSdk() {
  if (!_pumpSdk) _pumpSdk = new (require('@pump-fun/pump-sdk').PumpSdk)();
  return _pumpSdk;
}

function getOnlineSdk(connection) {
  if (!_onlineSdk) _onlineSdk = new (require('@pump-fun/pump-sdk').OnlinePumpSdk)(connection);
  return _onlineSdk;
}

// ─── Helpers ───────────────────────────────────────────────────────────────────

async function detectTokenProgram(connection, mint) {
  const info = await connection.getAccountInfo(new PublicKey(mint));
  if (!info) return TOKEN_PROGRAM_ID;
  return info.owner.equals(new PublicKey('TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb'))
    ? TOKEN_2022_PROGRAM_ID : TOKEN_PROGRAM_ID;
}

async function isGraduated(connection, mint) {
  const { bondingCurvePda } = require('@pump-fun/pump-sdk');
  const pda = bondingCurvePda(mint);
  const info = await connection.getAccountInfo(pda);
  if (!info) return true;
  try {
    const sdk = getPumpSdk();
    const bc = sdk.decodeBondingCurveNullable(info);
    return !bc || bc.complete;
  } catch (e) {
    // Invalid discriminator = not a valid bonding curve account
    return true;
  }
}

async function buildAndSign(connection, ixs, signerPk, signTx) {
  const tx = new Transaction();
  tx.add(ComputeBudgetProgram.setComputeUnitLimit({ units: 300_000 }));
  tx.add(ComputeBudgetProgram.setComputeUnitPrice({ microLamports: 50_000 }));
  tx.add(...ixs);
  const { blockhash, lastValidBlockHeight } = await connection.getLatestBlockhash();
  tx.recentBlockhash = blockhash;
  tx.feePayer = new PublicKey(signerPk);
  const msgBuf = tx.serializeMessage();
  const sig = await signTx(msgBuf);
  tx.addSignature(new PublicKey(signerPk), sig);
  const rawTx = tx.serialize();
  const txSig = await connection.sendRawTransaction(rawTx, { skipPreflight: false, maxRetries: 3 });
  await connection.confirmTransaction({ signature: txSig, blockhash, lastValidBlockHeight }, 'confirmed');
  return txSig;
}

// ─── Trading: Bonding Curve ────────────────────────────────────────────────────

async function buy({ connection, mint, user, solAmount, slippage = 15, signTx }) {
  const {
    PumpSdk, OnlinePumpSdk, getBuyTokenAmountFromSolAmount,
  } = require('@pump-fun/pump-sdk');

  const sdk = getPumpSdk();
  const online = getOnlineSdk(connection);
  const mintPk = new PublicKey(mint);
  const userPk = new PublicKey(user);
  const tokenProgram = await detectTokenProgram(connection, mint);

  const global = await online.fetchGlobal();
  const feeConfig = await online.fetchFeeConfig();
  const { bondingCurveAccountInfo, bondingCurve, associatedUserAccountInfo } =
    await online.fetchBuyState(mintPk, userPk, tokenProgram);

  const solLamports = new BN(solAmount);
  const mintSupply = bondingCurve.tokenTotalSupply.sub(bondingCurve.virtualTokenReserves);

  const expectedTokens = getBuyTokenAmountFromSolAmount({
    global, feeConfig, mintSupply, bondingCurve, amount: solLamports,
  });

  const ixs = await sdk.buyInstructions({
    global, bondingCurveAccountInfo, bondingCurve, associatedUserAccountInfo,
    mint: mintPk, user: userPk,
    amount: expectedTokens, solAmount: solLamports,
    slippage: slippage / 100, tokenProgram,
  });

  const txSig = await buildAndSign(connection, ixs, user, signTx);
  return { signature: txSig, expectedTokens: expectedTokens.toString(), route: 'pump-bonding-curve' };
}

async function sell({ connection, mint, user, tokenAmount, slippage = 15, signTx }) {
  const { PumpSdk, OnlinePumpSdk, getSellSolAmountFromTokenAmount } = require('@pump-fun/pump-sdk');

  const sdk = getPumpSdk();
  const online = getOnlineSdk(connection);
  const mintPk = new PublicKey(mint);
  const userPk = new PublicKey(user);
  const tokenProgram = await detectTokenProgram(connection, mint);

  const global = await online.fetchGlobal();
  const feeConfig = await online.fetchFeeConfig();
  const { bondingCurveAccountInfo, bondingCurve } =
    await online.fetchSellState(mintPk, userPk, tokenProgram);

  const amount = new BN(tokenAmount);
  const mintSupply = bondingCurve.tokenTotalSupply.sub(bondingCurve.virtualTokenReserves);

  const expectedSol = getSellSolAmountFromTokenAmount({
    global, feeConfig, mintSupply, bondingCurve, amount,
  });

  const ixs = await sdk.sellInstructions({
    global, bondingCurveAccountInfo, bondingCurve,
    mint: mintPk, user: userPk,
    amount, solAmount: expectedSol,
    slippage: slippage / 100, tokenProgram, mayhemMode: false,
  });

  const txSig = await buildAndSign(connection, ixs, user, signTx);
  return { signature: txSig, expectedSol: expectedSol.toString(), route: 'pump-bonding-curve' };
}

// ─── Trading: AMM (graduated tokens) ──────────────────────────────────────────

async function ammBuy({ connection, mint, user, solAmount, slippage = 15, signTx }) {
  const { canonicalPumpPoolPda } = require('@pump-fun/pump-sdk');
  const { PumpAmmSdk } = require('@pump-fun/pump-swap-sdk');
  const { OnlinePumpAmmSdk } = require('@pump-fun/pump-swap-sdk');

  const ammSdk = new PumpAmmSdk();
  const ammOnline = new OnlinePumpAmmSdk(connection);

  const mintPk = new PublicKey(mint);
  const userPk = new PublicKey(user);
  const poolPda = canonicalPumpPoolPda(mintPk);

  const swapState = await ammOnline.swapSolanaState(poolPda, userPk);
  const ixs = await ammSdk.buyQuoteInput(swapState, new BN(solAmount), slippage / 100);

  const txSig = await buildAndSign(connection, ixs, user, signTx);
  return { signature: txSig, route: 'pump-amm' };
}

async function ammSell({ connection, mint, user, tokenAmount, slippage = 15, signTx }) {
  const { canonicalPumpPoolPda } = require('@pump-fun/pump-sdk');
  const { PumpAmmSdk, OnlinePumpAmmSdk } = require('@pump-fun/pump-swap-sdk');

  const ammSdk = new PumpAmmSdk();
  const ammOnline = new OnlinePumpAmmSdk(connection);

  const mintPk = new PublicKey(mint);
  const userPk = new PublicKey(user);
  const poolPda = canonicalPumpPoolPda(mintPk);

  const swapState = await ammOnline.swapSolanaState(poolPda, userPk);
  const ixs = await ammSdk.sellBaseInput(swapState, new BN(tokenAmount), slippage / 100);

  const txSig = await buildAndSign(connection, ixs, user, signTx);
  return { signature: txSig, route: 'pump-amm' };
}

// ─── Smart Swap (auto-detect bonding curve vs AMM) ─────────────────────────────

async function smartSwap({ connection, mint, user, action, amount, slippage = 15, signTx }) {
  const graduated = await isGraduated(connection, mint);

  if (action === 'buy') {
    if (graduated) {
      console.log('  [pump] Token graduated → AMM buy');
      return ammBuy({ connection, mint, user, solAmount: amount, slippage, signTx });
    } else {
      console.log('  [pump] Bonding curve buy');
      return buy({ connection, mint, user, solAmount: amount, slippage, signTx });
    }
  } else {
    if (graduated) {
      console.log('  [pump] Token graduated → AMM sell');
      return ammSell({ connection, mint, user, tokenAmount: amount, slippage, signTx });
    } else {
      console.log('  [pump] Bonding curve sell');
      return sell({ connection, mint, user, tokenAmount: amount, slippage, signTx });
    }
  }
}

// ─── Token Launch ──────────────────────────────────────────────────────────────

async function createToken({ connection, user, name, symbol, uri, signTx }) {
  const sdk = getPumpSdk();
  const online = getOnlineSdk(connection);

  const mintKp = Keypair.generate();
  const userPk = new PublicKey(user);

  const ix = await sdk.createV2Instruction({
    mint: mintKp.publicKey, name, symbol, uri,
    creator: userPk, user: userPk,
    mayhemMode: false, cashback: false,
  });

  // createV2 needs mint as signer too — special handling
  const tx = new Transaction();
  tx.add(ComputeBudgetProgram.setComputeUnitLimit({ units: 300_000 }));
  tx.add(ComputeBudgetProgram.setComputeUnitPrice({ microLamports: 50_000 }));
  tx.add(ix);

  const { blockhash, lastValidBlockHeight } = await connection.getLatestBlockhash();
  tx.recentBlockhash = blockhash;
  tx.feePayer = userPk;

  // Partial sign with mint keypair
  tx.partialSign(mintKp);

  // Sign with user (AI signer via daemon)
  const msgBuf = tx.serializeMessage();
  const sig = await signTx(msgBuf);
  tx.addSignature(userPk, sig);

  const rawTx = tx.serialize();
  const txSig = await connection.sendRawTransaction(rawTx, { skipPreflight: false, maxRetries: 3 });
  await connection.confirmTransaction({ signature: txSig, blockhash, lastValidBlockHeight }, 'confirmed');

  return {
    signature: txSig,
    mint: mintKp.publicKey.toBase58(),
    mintKeypair: Buffer.from(mintKp.secretKey).toString('base64'),
  };
}

async function createAndBuy({ connection, user, name, symbol, uri, solAmount, signTx }) {
  const sdk = getPumpSdk();
  const online = getOnlineSdk(connection);
  const { getBuyTokenAmountFromSolAmount } = require('@pump-fun/pump-sdk');

  const mintKp = Keypair.generate();
  const userPk = new PublicKey(user);
  const global = await online.fetchGlobal();

  // For createAndBuy, use initial bonding curve params
  const solLamports = new BN(solAmount);
  // Estimate tokens from initial curve state
  const amount = solLamports; // SDK calculates internally

  const ixs = await sdk.createV2AndBuyInstructions({
    global, mint: mintKp.publicKey, name, symbol, uri,
    creator: userPk, user: userPk,
    amount: solLamports, solAmount: solLamports,
    mayhemMode: false, cashback: false,
  });

  const tx = new Transaction();
  tx.add(ComputeBudgetProgram.setComputeUnitLimit({ units: 400_000 }));
  tx.add(ComputeBudgetProgram.setComputeUnitPrice({ microLamports: 50_000 }));
  tx.add(...ixs);

  const { blockhash, lastValidBlockHeight } = await connection.getLatestBlockhash();
  tx.recentBlockhash = blockhash;
  tx.feePayer = userPk;
  tx.partialSign(mintKp);

  const msgBuf = tx.serializeMessage();
  const sig = await signTx(msgBuf);
  tx.addSignature(userPk, sig);

  const rawTx = tx.serialize();
  const txSig = await connection.sendRawTransaction(rawTx, { skipPreflight: false, maxRetries: 3 });
  await connection.confirmTransaction({ signature: txSig, blockhash, lastValidBlockHeight }, 'confirmed');

  return {
    signature: txSig,
    mint: mintKp.publicKey.toBase58(),
    mintKeypair: Buffer.from(mintKp.secretKey).toString('base64'),
  };
}

// ─── Pricing & Info ────────────────────────────────────────────────────────────

async function bondingCurveInfo(connection, mint) {
  const {
    bondingCurvePda, bondingCurveMarketCap,
    getBuyTokenAmountFromSolAmount, getSellSolAmountFromTokenAmount,
  } = require('@pump-fun/pump-sdk');

  const sdk = getPumpSdk();
  const online = getOnlineSdk(connection);
  const mintPk = new PublicKey(mint);

  const pda = bondingCurvePda(mint);
  const info = await connection.getAccountInfo(pda);
  if (!info) return { exists: false, graduated: true };

  let bc;
  try { bc = sdk.decodeBondingCurveNullable(info); } catch { bc = null; }
  if (!bc) return { exists: false, graduated: true };

  const global = await online.fetchGlobal();
  const feeConfig = await online.fetchFeeConfig();
  const mintSupply = bc.tokenTotalSupply.sub(bc.virtualTokenReserves);

  const mcap = bondingCurveMarketCap({
    mintSupply,
    virtualSolReserves: bc.virtualSolReserves,
    virtualTokenReserves: bc.virtualTokenReserves,
  });

  // Price per token in lamports
  const oneToken = new BN(1_000_000); // 1 token (6 decimals)
  let pricePerToken;
  try {
    pricePerToken = getSellSolAmountFromTokenAmount({
      global, feeConfig, mintSupply, bondingCurve: bc, amount: oneToken,
    });
  } catch { pricePerToken = new BN(0); }

  return {
    exists: true,
    graduated: bc.complete || false,
    virtualSolReserves: bc.virtualSolReserves.toString(),
    virtualTokenReserves: bc.virtualTokenReserves.toString(),
    realSolReserves: bc.realSolReserves ? bc.realSolReserves.toString() : '0',
    realTokenReserves: bc.realTokenReserves ? bc.realTokenReserves.toString() : '0',
    tokenTotalSupply: bc.tokenTotalSupply.toString(),
    mintSupply: mintSupply.toString(),
    marketCapLamports: mcap.toString(),
    marketCapSOL: (parseFloat(mcap.toString()) / 1e9).toFixed(4),
    pricePerTokenLamports: pricePerToken.toString(),
  };
}

async function getQuote(connection, { mint, action, amount }) {
  const {
    getBuyTokenAmountFromSolAmount, getSellSolAmountFromTokenAmount,
    getBuySolAmountFromTokenAmount,
  } = require('@pump-fun/pump-sdk');

  const sdk = getPumpSdk();
  const online = getOnlineSdk(connection);
  const mintPk = new PublicKey(mint);

  const global = await online.fetchGlobal();
  const feeConfig = await online.fetchFeeConfig();

  const { bondingCurvePda } = require('@pump-fun/pump-sdk');
  const pda = bondingCurvePda(mint);
  const info = await connection.getAccountInfo(pda);
  if (!info) throw new Error('No bonding curve (token may be graduated)');
  const bc = sdk.decodeBondingCurve(info);
  const mintSupply = bc.tokenTotalSupply.sub(bc.virtualTokenReserves);

  if (action === 'buy') {
    const tokens = getBuyTokenAmountFromSolAmount({
      global, feeConfig, mintSupply, bondingCurve: bc, amount: new BN(amount),
    });
    return { action: 'buy', inputLamports: amount, outputTokens: tokens.toString() };
  } else if (action === 'sell') {
    const sol = getSellSolAmountFromTokenAmount({
      global, feeConfig, mintSupply, bondingCurve: bc, amount: new BN(amount),
    });
    return { action: 'sell', inputTokens: amount, outputLamports: sol.toString() };
  } else if (action === 'cost') {
    // How much SOL to buy N tokens
    const sol = getBuySolAmountFromTokenAmount({
      global, feeConfig, mintSupply, bondingCurve: bc, amount: new BN(amount),
    });
    return { action: 'cost', targetTokens: amount, costLamports: sol.toString() };
  }
}

// ─── Creator Fees ──────────────────────────────────────────────────────────────

async function getCreatorFeeBalance(connection, creator) {
  const online = getOnlineSdk(connection);
  const balance = await online.getCreatorVaultBalanceBothPrograms(new PublicKey(creator));
  return { balance: balance.toString(), balanceSOL: (parseFloat(balance.toString()) / 1e9).toFixed(6) };
}

async function collectCreatorFees({ connection, creator, user, signTx }) {
  const online = getOnlineSdk(connection);
  const ixs = await online.collectCoinCreatorFeeInstructions(new PublicKey(creator), new PublicKey(user));
  if (!ixs.length) return { signature: null, message: 'No fees to collect' };
  const txSig = await buildAndSign(connection, ixs, user, signTx);
  return { signature: txSig };
}

async function createFeeSharing({ connection, user, mint, shareholders, signTx }) {
  // shareholders: [{ address: string, share: number }]
  const sdk = getPumpSdk();
  const { canonicalPumpPoolPda } = require('@pump-fun/pump-sdk');

  const mintPk = new PublicKey(mint);
  const userPk = new PublicKey(user);
  const graduated = await isGraduated(connection, mint);
  const pool = graduated ? canonicalPumpPoolPda(mintPk) : null;

  const newShareholders = shareholders.map(s => ({
    address: new PublicKey(s.address),
    share: s.share,
  }));

  const ix = await sdk.createFeeSharingConfig({
    creator: userPk, mint: mintPk, pool,
    newShareholders,
  });

  // This is a single IX but createSharingConfigWithSocialRecipients handles social too
  const txSig = await buildAndSign(connection, [ix], user, signTx);
  return { signature: txSig };
}

async function distributeFees({ connection, mint, user, signTx }) {
  const online = getOnlineSdk(connection);
  const { instructions, isGraduated: grad } = await online.buildDistributeCreatorFeesInstructions(new PublicKey(mint));
  if (!instructions.length) return { signature: null, message: 'No fees to distribute' };
  const txSig = await buildAndSign(connection, instructions, user, signTx);
  return { signature: txSig, isGraduated: grad };
}

async function claimCashback({ connection, user, signTx }) {
  const sdk = getPumpSdk();
  const ix = await sdk.claimCashbackInstruction({ user: new PublicKey(user) });
  const txSig = await buildAndSign(connection, [ix], user, signTx);
  return { signature: txSig };
}

// ─── Token Incentives ──────────────────────────────────────────────────────────

async function getUnclaimedIncentives(connection, user) {
  const online = getOnlineSdk(connection);
  const total = await online.getTotalUnclaimedTokensBothPrograms(new PublicKey(user));
  const daily = await online.getCurrentDayTokensBothPrograms(new PublicKey(user));
  return { totalUnclaimed: total.toString(), currentDay: daily.toString() };
}

async function claimIncentives({ connection, user, signTx }) {
  const online = getOnlineSdk(connection);
  const ixs = await online.claimTokenIncentivesBothPrograms(new PublicKey(user), new PublicKey(user));
  if (!ixs.length) return { signature: null, message: 'No incentives to claim' };
  const txSig = await buildAndSign(connection, ixs, user, signTx);
  return { signature: txSig };
}

// ─── AMM Liquidity ─────────────────────────────────────────────────────────────

async function ammDeposit({ connection, mint, user, baseAmount, slippage = 5, signTx }) {
  const { canonicalPumpPoolPda } = require('@pump-fun/pump-sdk');
  const { PumpAmmSdk, OnlinePumpAmmSdk } = require('@pump-fun/pump-swap-sdk');

  const ammSdk = new PumpAmmSdk();
  const ammOnline = new OnlinePumpAmmSdk(connection);
  const poolPda = canonicalPumpPoolPda(new PublicKey(mint));
  const userPk = new PublicKey(user);

  const liquidityState = await ammOnline.liquiditySolanaState(poolPda, userPk);
  const { depositInstructions, maxQuote } = ammSdk.depositBaseInput(liquidityState, new BN(baseAmount), slippage / 100);

  // depositInstructions returns calc result, need to call depositInstructionsInternal
  const result = ammSdk.depositBaseInput(liquidityState, new BN(baseAmount), slippage / 100);
  const ixs = await ammSdk.depositInstructionsInternal(liquidityState, result.lpToken, result.maxBase, result.maxQuote);

  const txSig = await buildAndSign(connection, ixs, user, signTx);
  return { signature: txSig, lpTokens: result.lpToken.toString() };
}

async function ammWithdraw({ connection, mint, user, lpAmount, slippage = 5, signTx }) {
  const { canonicalPumpPoolPda } = require('@pump-fun/pump-sdk');
  const { PumpAmmSdk, OnlinePumpAmmSdk } = require('@pump-fun/pump-swap-sdk');

  const ammSdk = new PumpAmmSdk();
  const ammOnline = new OnlinePumpAmmSdk(connection);
  const poolPda = canonicalPumpPoolPda(new PublicKey(mint));
  const userPk = new PublicKey(user);

  const liquidityState = await ammOnline.liquiditySolanaState(poolPda, userPk);
  const ixs = await ammSdk.withdrawInstructions(liquidityState, new BN(lpAmount), slippage / 100);

  const txSig = await buildAndSign(connection, ixs, user, signTx);
  return { signature: txSig };
}

// ─── Volume Accumulator ────────────────────────────────────────────────────────

async function volumeStats(connection, user) {
  const online = getOnlineSdk(connection);
  try {
    const stats = await online.fetchUserVolumeAccumulatorTotalStats(new PublicKey(user));
    return stats;
  } catch (e) {
    return { error: e.message };
  }
}

async function syncVolume({ connection, user, signTx }) {
  const online = getOnlineSdk(connection);
  const ixs = await online.syncUserVolumeAccumulatorBothPrograms(new PublicKey(user));
  if (!ixs.length) return { signature: null, message: 'Nothing to sync' };
  const txSig = await buildAndSign(connection, ixs, user, signTx);
  return { signature: txSig };
}

// ─── Migrate ───────────────────────────────────────────────────────────────────

async function migrate({ connection, mint, user, withdrawAuthority, signTx }) {
  const sdk = getPumpSdk();
  const tokenProgram = await detectTokenProgram(connection, mint);
  const ix = await sdk.migrateInstruction({
    withdrawAuthority: new PublicKey(withdrawAuthority),
    mint: new PublicKey(mint),
    user: new PublicKey(user),
    tokenProgram,
  });
  const txSig = await buildAndSign(connection, [ix], user, signTx);
  return { signature: txSig };
}

// ─── PDA helpers ───────────────────────────────────────────────────────────────

function pdas(mint) {
  const {
    bondingCurvePda, bondingCurveV2Pda, canonicalPumpPoolPda,
    creatorVaultPda, pumpPoolAuthorityPda, userVolumeAccumulatorPda,
  } = require('@pump-fun/pump-sdk');
  const mintPk = new PublicKey(mint);
  return {
    bondingCurve: bondingCurvePda(mintPk).toBase58(),
    bondingCurveV2: bondingCurveV2Pda(mintPk).toBase58(),
    canonicalPool: canonicalPumpPoolPda(mintPk).toBase58(),
  };
}

module.exports = {
  // Trading
  buy, sell, ammBuy, ammSell, smartSwap,
  // Launch
  createToken, createAndBuy,
  // Pricing
  bondingCurveInfo, getQuote,
  // Fees
  getCreatorFeeBalance, collectCreatorFees,
  createFeeSharing, distributeFees, claimCashback,
  // Incentives
  getUnclaimedIncentives, claimIncentives,
  // AMM Liquidity
  ammDeposit, ammWithdraw,
  // Volume
  volumeStats, syncVolume,
  // Migrate
  migrate,
  // Utils
  isGraduated, detectTokenProgram, pdas, buildAndSign,
};
