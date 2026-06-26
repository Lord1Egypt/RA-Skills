import { ethers } from 'ethers';
import {
  findChainByAlias,
  getApi3Market,
  initializeStaticProvider,
  computeSubscriptionPrices,
  readPricingMerkleTree,
  getBeaconSetUpdateCalldata,
  getBeaconsUpdateCalldatas,
  getDataFeedRegistrationCalldatas,
  getDeployProxyCalldatas,
  prepareBeaconsData,
  buySubscription,
} from '@api3/dapi-management';
import dotenv from 'dotenv';

dotenv.config();

const GAS_PRICE_MULTIPLIER = 1.5;

async function main() {
  const args = process.argv.slice(2);
  if (args.length < 3) {
    console.error('Usage: ts-node buy.ts <dapiName> <chainAlias> <deviationThreshold>');
    process.exit(1);
  }

  if (!process.env.WALLET_MNEMONIC) {
    console.error('WALLET_MNEMONIC environment variable is required to run this script.');
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
  const wallet = ethers.Wallet.fromPhrase(process.env.WALLET_MNEMONIC!).connect(provider);

  const { api3Market } = getApi3Market(chain.id, wallet);
  const { merkleTreeRoot, subscriptions: merkleTreeSubscriptions } = await readPricingMerkleTree(chain.id, dapiName);
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

  console.log('Preparing data for activation...');
  const { beaconIds, airnodes, templateIds, dataFeedId, isRegistered, beaconsNeedingUpdate, updateBeaconSet } =
    await prepareBeaconsData(api3Market, dapiName);

  const registrationCalldatas = !isRegistered
    ? await getDataFeedRegistrationCalldatas(api3Market, airnodes, templateIds)
    : [];
  const beaconsUpdateCalldatas = await getBeaconsUpdateCalldatas(api3Market, beaconsNeedingUpdate);
  const beaconSetUpdateCalldatas = updateBeaconSet ? getBeaconSetUpdateCalldata(api3Market, beaconIds) : [];
  const deployProxyCalldatas = await getDeployProxyCalldatas(api3Market, dapiName, chain.id, provider);
  
  const purchasePreparationCalldatas = [
    ...registrationCalldatas,
    ...beaconsUpdateCalldatas,
    ...beaconSetUpdateCalldatas,
    ...deployProxyCalldatas,
  ];

  console.log('Executing purchase transaction...');
  const tx = await buySubscription(
    purchasePreparationCalldatas,
    api3Market,
    dapiName,
    dataFeedId,
    subscription,
    merkleTreeRoot,
    GAS_PRICE_MULTIPLIER
  );

  console.log('Transaction sent. Waiting for confirmation...', { hash: tx.hash });
  await tx.wait();
  console.log('Transaction confirmed successfully!', { hash: tx.hash });
}

main();
