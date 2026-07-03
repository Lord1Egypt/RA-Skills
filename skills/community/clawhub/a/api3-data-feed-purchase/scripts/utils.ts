import { ethers } from 'ethers';
import { StandardMerkleTree } from '@openzeppelin/merkle-tree';
import { api3Contracts, dapiManagementMerkleTreeData, api3ApiIntegrations, dapis, deriveSponsorWalletAddress } from '@api3/dapi-management';

type SupportedChain = (typeof api3Contracts.CHAINS)[number];
type Api3MarketV2Contract = ReturnType<typeof api3Contracts.Api3MarketV2__factory.connect>;
type PricingLeaf = {
  value: [encodedDapiName: string, chainId: string | number, updateParameters: string, duration: string, price: string];
  proof: string[];
};
type PricingMerkleTree = {
  merkleRoot: string;
  leaves: PricingLeaf[];
};
type Beacon = {
  airnodeAddress: string;
  templateId: string;
  beaconId: string;
};
type SignedBeaconUpdate = {
  airnode: string;
  templateId: string;
  timestamp: ethers.BigNumberish;
  encodedValue: string;
  signature: string;
};
type SignedApiResponse = {
  data: Record<string, SignedBeaconUpdate>;
};
type BuildCalldataArgs = {
  beacons: Beacon[];
  beaconIds: string[];
  isRegistered: boolean;
  beaconTimestamps: readonly bigint[];
  dataFeedTimestamp: bigint;
  dataFeedDetails: string;
  encodedDapiName: string;
  chainId: string;
  dapiName: string;
  provider: ethers.Provider;
};

export function findChainByAlias(alias: string): SupportedChain {
  const chain = api3Contracts.CHAINS.find((c) => c.alias.toLowerCase() === alias.toLowerCase());
  if (!chain) {
    throw new Error(`Chain with alias ${alias} not found in chains exported by @api3/contracts package`);
  }
  return chain;
}


export function findChainById(chainId: string): SupportedChain {
  const targetChain = api3Contracts.CHAINS.find((chain) => chain.id === chainId);
  if (!targetChain) {
    throw new Error(`Chain ${chainId} is not supported`);
  }
  return targetChain;
}

function getDefaultRpcUrl(chain: SupportedChain): string {
  const defaultProvider = chain.providers.find((provider) => provider.alias === 'default');
  if (!defaultProvider) {
    throw new Error(`Chain ${chain.id} does not define a default RPC provider`);
  }
  if (!defaultProvider.rpcUrl) {
    throw new Error(`Chain ${chain.id} default RPC provider does not include an RPC URL`);
  }
  return defaultProvider.rpcUrl;
}

function getMarketAddress(chainId: string): string {
  const deploymentAddresses = api3Contracts.deploymentAddresses.Api3MarketV2 as Record<string, string>;
  const marketAddress = deploymentAddresses[chainId];
  if (!marketAddress) {
    throw new Error(`Api3MarketV2 not deployed on chain ${chainId}`);
  }
  return marketAddress;
}


const HUNDRED_PERCENT = 100_000_000n;
const ONE_DAY_SECS = 24 * 60 * 60;
const DEFAULT_DAPP_ID = 1n;

export async function prepareSubscription(
  walletMnemonic: string |  null,
  chainId: string,
  dapiName: string,
  deviationThresholdInPercentage: number
) {
  const targetChain = findChainById(chainId);
  const rpcUrl = getDefaultRpcUrl(targetChain);
  const provider = new ethers.JsonRpcProvider(rpcUrl);
  const signerOrProvider = walletMnemonic ? ethers.Wallet.fromPhrase(walletMnemonic).connect(provider) : provider;

  const marketAddress = getMarketAddress(chainId);
  const market = api3Contracts.Api3MarketV2__factory.connect(marketAddress, signerOrProvider);

  const encodedDapiName = ethers.encodeBytes32String(dapiName);
  const updateParameters = encodeUpdateParameters(deviationThresholdInPercentage);
  const dataFeedId = getDataFeedId(encodedDapiName);

  const pricingMt = await fetchPricingMt(chainId, dapiName);
  const pricingEntry = findPricingLeaf(pricingMt, encodedDapiName, chainId, updateParameters);
  if (!pricingEntry) throw new Error(`No pricing entry for ${dapiName} on chain ${chainId} with deviation ${deviationThresholdInPercentage}%`);
  const duration = parseInt(pricingEntry.value[3]);
  const price = BigInt(pricingEntry.value[4]);

  const sponsorWallet = deriveSponsorWalletAddress(encodedDapiName);
  const expectedBalance = await market.computeExpectedSponsorWalletBalanceAfterSubscriptionIsAdded(
    encodedDapiName, updateParameters, duration, price
  );
  const currentSponsorBalance = await provider.getBalance(sponsorWallet);
  const pricePerDay = price / BigInt(Math.round(duration / 86400));
  const fundsToSend = computeFundsToSend(expectedBalance, pricePerDay, currentSponsorBalance);

  return { provider, market, rpcUrl, marketAddress, encodedDapiName, updateParameters, dataFeedId, pricingMt, pricingEntry, duration, price, sponsorWallet, fundsToSend };
}

export async function fetchPricingMt(chainId: string, dapiName: string): Promise<PricingMerkleTree> {
  const path = dapiName.replace('/', '-');
  const response = await fetch(`https://api3dao.github.io/data-feeds/market/dapi-pricing/${chainId}/${path}.json`);
  if (!response.ok) {
    throw new Error(`Failed to fetch pricing Merkle tree for ${dapiName} on chain ${chainId}`);
  }
  return response.json() as Promise<PricingMerkleTree>;
}

export function encodeUpdateParameters(deviationThresholdInPercentage: number): string {
  const deviationThreshold = BigInt(Math.round((deviationThresholdInPercentage * Number(HUNDRED_PERCENT)) / 100));
  return ethers.AbiCoder.defaultAbiCoder().encode(
    ['uint256', 'uint256', 'uint256'],
    [deviationThreshold, 0n, 86400n]
  );
}

export function findPricingLeaf(
  pricingMt: PricingMerkleTree,
  encodedDapiName: string,
  chainId: string,
  updateParameters: string
): PricingLeaf {
  return pricingMt.leaves.find(
    (entry: PricingLeaf) =>
      entry.value[0] === encodedDapiName &&
      String(entry.value[1]) === String(chainId) &&
      entry.value[2] === updateParameters
  )!;
}

export function getDataFeedId(encodedDapiName: string): string {
  const entry = dapiManagementMerkleTreeData.merkleTreeValues.find((e) => e[0] === encodedDapiName);
  if (!entry) throw new Error(`Management tree entry not found for ${encodedDapiName}`);
  return entry[1];
}

export function resolveBeacons(dapiName: string) {
  const { getAirnodeAddressByAlias, getOisTitleByFeedNameAndAirnodeAddress, deriveTemplateId } = api3ApiIntegrations;
  const dapiEntry = dapis.find((d) => d.name === dapiName);
  if (!dapiEntry) throw new Error(`dAPI ${dapiName} not found in registry`);

  const beacons: Beacon[] = dapiEntry.providers.map((providerAlias) => {
    const airnodeAddress = getAirnodeAddressByAlias(providerAlias);
    const oisTitle = getOisTitleByFeedNameAndAirnodeAddress(dapiName, airnodeAddress);
    const templateId = deriveTemplateId({ feedName: dapiName, oisTitle, airnodeAddress });
    const beaconId = ethers.solidityPackedKeccak256(['address', 'bytes32'], [airnodeAddress, templateId]);
    return { airnodeAddress, templateId, beaconId };
  });

  const beaconIds = beacons.map((b) => b.beaconId);
  const dataFeedDetails = (() => {
    if (beacons.length === 1) {
      const [beacon] = beacons;
      if (!beacon) {
        throw new Error(`Expected a single beacon for ${dapiName}`);
      }
      return ethers.AbiCoder.defaultAbiCoder().encode(['address', 'bytes32'], [beacon.airnodeAddress, beacon.templateId]);
    }

    return ethers.AbiCoder.defaultAbiCoder().encode(
      ['address[]', 'bytes32[]'],
      [beacons.map((beacon) => beacon.airnodeAddress), beacons.map((beacon) => beacon.templateId)]
    );
  })();

  return { beacons, beaconIds, dataFeedDetails };
}

export async function checkDataFeedState(market: Api3MarketV2Contract, dataFeedId: string, dataFeedDetails: string) {
  const { returndata } = await market.tryMulticall.staticCall([
    market.interface.encodeFunctionData('getDataFeedData', [dataFeedId]),
    market.interface.encodeFunctionData('registerDataFeed', [dataFeedDetails]),
    market.interface.encodeFunctionData('getDataFeedData', [dataFeedId]),
  ]);
  const dataFeedBeforeRegistration = market.interface.decodeFunctionResult('getDataFeedData', returndata[0]);
  const beaconValuesBeforeReg = dataFeedBeforeRegistration[3] as readonly unknown[];
  const dataFeedAfterRegistration = market.interface.decodeFunctionResult('getDataFeedData', returndata[2]);
  const dataFeedTimestamp = dataFeedAfterRegistration[2] as bigint;
  const beaconTimestamps = dataFeedAfterRegistration[4] as readonly bigint[];
  return {
    isRegistered: beaconValuesBeforeReg.length !== 0,
    dataFeedTimestamp,
    beaconTimestamps,
  };
}

export async function buildCalldata(market: Api3MarketV2Contract, { beacons, beaconIds, isRegistered, beaconTimestamps, dataFeedTimestamp, dataFeedDetails, encodedDapiName, chainId, dapiName, provider }: BuildCalldataArgs) {
  const calldata: string[] = [];
  const now = Math.floor(Date.now() / 1000);

  if (!isRegistered) {
    calldata.push(market.interface.encodeFunctionData('registerDataFeed', [dataFeedDetails]));
  }

  const staleBeacons = beacons.filter((_, i: number) => Number(beaconTimestamps[i]) + ONE_DAY_SECS < now);
  for (const beacon of staleBeacons) {
    const resp = await fetch(`https://signed-api.api3.org/public/${beacon.airnodeAddress}`);
    if (!resp.ok) {
      throw new Error(`Failed to fetch signed API data for airnode ${beacon.airnodeAddress}`);
    }
    const json = await resp.json() as SignedApiResponse;
    const signed = json.data[beacon.beaconId];
    if (!signed) continue;
    calldata.push(
      market.interface.encodeFunctionData('updateBeaconWithSignedData', [
        signed.airnode, signed.templateId, signed.timestamp, signed.encodedValue, signed.signature,
      ])
    );
  }

  if (beacons.length > 1 && Number(dataFeedTimestamp) + ONE_DAY_SECS < now) {
    calldata.push(market.interface.encodeFunctionData('updateBeaconSetWithBeacons', [beaconIds]));
  }

  const proxyAddress = api3Contracts.computeApi3ReaderProxyV1Address(chainId, dapiName, DEFAULT_DAPP_ID, '0x');
  const proxyCode = await provider.getCode(proxyAddress);
  if (proxyCode === '0x') {
    calldata.push(market.interface.encodeFunctionData('deployApi3ReaderProxyV1', [encodedDapiName, DEFAULT_DAPP_ID, '0x']));
  }

  return { calldata, staleBeacons, proxyDeployed: proxyCode !== '0x' };
}

export function encodeMerkleData(
  encodedDapiName: string,
  dataFeedId: string,
  sponsorWallet: string,
  pricingMerkleRoot: string,
  pricingProof: string[]
): string {
  const managementTree = StandardMerkleTree.of(
    dapiManagementMerkleTreeData.merkleTreeValues,
    ['bytes32', 'bytes32', 'address']
  );
  return ethers.AbiCoder.defaultAbiCoder().encode(
    ['bytes32', 'bytes32[]', 'bytes32', 'bytes32[]'],
    [managementTree.root, managementTree.getProof([encodedDapiName, dataFeedId, sponsorWallet]), pricingMerkleRoot, pricingProof]
  );
}

export function computeFundsToSend(expectedBalance: bigint, pricePerDay: bigint, currentSponsorBalance: bigint): bigint {
  const rawFunds = expectedBalance + pricePerDay - currentSponsorBalance;
  return rawFunds > 0n ? rawFunds : 0n;
}
