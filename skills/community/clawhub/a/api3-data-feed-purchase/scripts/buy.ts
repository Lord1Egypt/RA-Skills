import { ethers } from 'ethers';
import {
  prepareSubscription,
  resolveBeacons,
  checkDataFeedState,
  buildCalldata,
  encodeMerkleData,
} from './utils.ts';
import dotenv from 'dotenv';

dotenv.config();

async function main() {
  console.log('*'.repeat(50));
  console.log('Starting buy script...');

  const walletMnemonic = process.env.WALLET_MNEMONIC;
  if (!walletMnemonic) throw new Error('WALLET_MNEMONIC is not set');

  const [,, chainId, dapiName, deviationArg] = process.argv;
  if (!chainId || !dapiName || !deviationArg) throw new Error('Usage: ts-node scripts/buy.ts <chainId> <dapiName> <deviationThresholdInPercentage>');
  const deviationThresholdInPercentage = Number(deviationArg);
  if (isNaN(deviationThresholdInPercentage) || deviationThresholdInPercentage <= 0) throw new Error('deviationThresholdInPercentage must be a positive number (e.g. 0.5, 1, 2.5, 5)');

  const { provider, market, rpcUrl, marketAddress, encodedDapiName, updateParameters, dataFeedId, pricingMt, pricingEntry, duration, price, sponsorWallet, fundsToSend } =
    await prepareSubscription(walletMnemonic, chainId, dapiName, deviationThresholdInPercentage);
  console.log(`Chain: ${chainId} | RPC: ${rpcUrl}`);
  console.log(`Market contract: ${marketAddress}`);
  console.log(`Sponsor wallet: ${sponsorWallet} | Duration: ${duration}s | Price: ${ethers.formatEther(price)} ETH | Amount to send: ${ethers.formatEther(fundsToSend)} ETH`);

  const { beacons, beaconIds, dataFeedDetails } = resolveBeacons(dapiName);
  const { isRegistered, dataFeedTimestamp, beaconTimestamps } = await checkDataFeedState(market, dataFeedId, dataFeedDetails);
  const { calldata } = await buildCalldata(market, {
    beacons, beaconIds, isRegistered, beaconTimestamps, dataFeedTimestamp,
    dataFeedDetails, encodedDapiName, chainId, dapiName, provider,
  });

  const merkleData = encodeMerkleData(
    encodedDapiName,
    dataFeedId,
    sponsorWallet,
    pricingMt.merkleRoot,
    pricingEntry.proof
  );

  const gasEstimate = await market.multicallAndBuySubscription.estimateGas(
    calldata, encodedDapiName, dataFeedId, sponsorWallet,
    updateParameters, duration, price, merkleData,
    { value: fundsToSend }
  );
  const gasLimit = gasEstimate + gasEstimate / 10n;

  const tx = await market.tryMulticallAndBuySubscription(
    calldata, encodedDapiName, dataFeedId, sponsorWallet,
    updateParameters, duration, price, merkleData,
    { gasLimit, value: fundsToSend }
  );
  console.log(`Transaction: ${tx.hash}`);
  await tx.wait();
  console.log(`Confirmed: ${tx.hash}`);
}

main();
