import { ethers } from 'ethers';
import {
  findChainByAlias,
  getApi3Market,
  initializeStaticProvider,
  computeSubscriptionPrices,
  readPricingMerkleTree,
} from '@api3/dapi-management';

async function main() {
  const args = process.argv.slice(2);
  if (args.length < 3) {
    console.error('Usage: ts-node quote.ts <dapiName> <chainAlias> <deviationThreshold>');
    process.exit(1);
  }

  const [dapiName, chainAlias, devThresholdStr] = args;
  const deviationThreshold = Number(devThresholdStr);
  const chain = findChainByAlias(chainAlias);
  if (!chain) {
    console.error(`Chain not found: ${chainAlias}`);
    process.exit(1);
  }
  const provider = initializeStaticProvider(chain.alias);
  const { api3Market } = getApi3Market(chain.id, provider);
  const { subscriptions: merkleTreeSubscriptions } = await readPricingMerkleTree(chain.id, dapiName);
  const subscriptions = await computeSubscriptionPrices(api3Market, dapiName, provider, merkleTreeSubscriptions);
  const subscription = subscriptions.find(
    (sub) => sub.updateParameters.deviationThreshold === deviationThreshold
  );

  if (!subscription) {
    console.error('No subscription found matching the deviation threshold.', {
      dapiName,
      chainAlias,
      deviationThreshold,
      availableSubscriptions: subscriptions.map(s => s.updateParameters.deviationThreshold)
    });
    process.exit(1);
  }

  const priceInEther = ethers.formatEther(BigInt(subscription.price));
  console.log('Parameters and Calculated Price:', {
    "Feed Name": dapiName,
    "Chain": chainAlias,
    "Heartbeat Interval": subscription.updateParameters.heartbeatInterval,
    "Deviation Threshold": subscription.updateParameters.deviationThreshold,
    "Subscription Duration": subscription.duration,
    "Price (ETH)": priceInEther
  });

}

main();
