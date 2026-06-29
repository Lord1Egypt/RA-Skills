import { api3ApiIntegrations, dapis, dapiManagementMerkleTreeData } from '@api3/dapi-management';
import { ethers } from 'ethers';

async function fetchFeedValue(signedApiUrl: string, dataFeedId: string) {
  const response = await fetch(signedApiUrl);
  if (!response.ok) {
    throw new Error(`request failed with status ${response.status}`);
  }

  const { data } = await response.json();
  const entry = data[dataFeedId];
  if (!entry) {
    return null;
  }

  const decodedValue = ethers.AbiCoder.defaultAbiCoder().decode(['int256'], entry.encodedValue)[0];
  return {
    value: ethers.formatUnits(decodedValue, 18),
    timestamp: new Date(Number(entry.timestamp) * 1000).toISOString(),
  };
}

async function main() {
  const merkleTreeTimestamp = dapiManagementMerkleTreeData.timestamp;
  console.log(
    `Note that this dAPI configuration is updated at ${new Date(merkleTreeTimestamp * 1000).toISOString()} and may not reflect the latest changes.\n`
  );

  const [feedName] = process.argv.slice(2);
  if (!feedName) {
    console.error('Usage: ts-node explore-data-feeds.ts <feedName>');
    process.exit(1);
  }

  const dapi = dapis.find((d) => d.name === feedName);
  if (!dapi) {
    console.error(`Feed not found: ${feedName}`);
    process.exit(1);
  }

  const apiData = Object.values(api3ApiIntegrations.apisData).filter(
    (api) =>
      Object.values(api.supportedFeedsInBatches).flat(2).includes(feedName) &&
      !api.alias.includes('-mock')
  );

  if (apiData.length === 0) {
    console.error(`No providers found for feed: ${feedName}`);
    process.exit(1);
  }

  console.log('Providers that support this feed:');
  console.log(apiData.map((api) => `- ${api.alias}`));

  const aggregationProviders = apiData
    .filter((api) => dapi.providers.includes(api.alias))
    .map((api) => `- ${api.alias}`);
  console.log('Providers that are used in the aggregation of this feed:');
  console.log(aggregationProviders);

  for (const api of apiData) {
    const dataFeedId = api3ApiIntegrations.deriveDataFeedId(feedName, api.airnode);
    const signedApiUrl = `https://signed-api.api3.org/public/${api.airnode}`;

    console.log('*'.repeat(50));
    console.log(`- API Alias: ${api.alias}`);
    console.log(`- Data Feed ID: ${dataFeedId}`);
    console.log(`- Signed API URL: ${signedApiUrl}`);
    console.log(`- Homepage: ${api.homepageUrl}`);

    try {
      const result = await fetchFeedValue(signedApiUrl, dataFeedId);
      if (result) {
        console.log(`- Value: ${result.value}`);
        console.log(`- Timestamp: ${result.timestamp}`);
      } else {
        console.log(`- Value: no entry found for this Data Feed ID in the Signed API response`);
      }
    } catch (error) {
      console.log(`- Value: failed to fetch from Signed API (${(error as Error).message})`);
    }
  }
}

main();
