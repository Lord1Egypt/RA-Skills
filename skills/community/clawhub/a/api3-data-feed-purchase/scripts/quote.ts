import { ethers } from 'ethers';
import { prepareSubscription, findChainById } from './utils.ts';
import dotenv from 'dotenv';

dotenv.config();

async function main() {
  const [,, chainId, dapiName, deviationArg] = process.argv;
  if (!chainId || !dapiName || !deviationArg) throw new Error('Usage: ts-node scripts/quote.ts <chainId> <dapiName> <deviationThresholdInPercentage>');
  const deviationThresholdInPercentage = Number(deviationArg);
  if (isNaN(deviationThresholdInPercentage) || deviationThresholdInPercentage <= 0) throw new Error('deviationThresholdInPercentage must be a positive number (e.g. 0.5, 1, 2.5, 5)');

  const { duration, price, fundsToSend, sponsorWallet } = await prepareSubscription(null, chainId, dapiName, deviationThresholdInPercentage);
  const chain = findChainById(chainId);

  console.log('*'.repeat(50));
  console.log(`dAPI:      ${dapiName}`);
  console.log(`Chain:     ${chain.name} (id: ${chainId})`);
  console.log(`Deviation: ${deviationThresholdInPercentage}%`);
  console.log(`Duration:  ${duration}s (${Math.round(duration / 86400)} days)`);
  console.log(`Price:     ${ethers.formatEther(price)} ETH`);
  console.log(`Amount to send: ${ethers.formatEther(fundsToSend)} ETH`);
  console.log(`Sponsor wallet: ${sponsorWallet}`);
  console.log('*'.repeat(50));
}

main();
