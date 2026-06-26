import { ethers } from 'ethers';
import { api3Contracts, findChainByAlias } from '@api3/dapi-management';

const { Api3ReaderProxyV1__factory } = api3Contracts;

async function readFeed(proxyAddress: string, rpcUrl: string) {
  const provider = new ethers.JsonRpcProvider(rpcUrl);
  const proxy = Api3ReaderProxyV1__factory.connect(proxyAddress, provider);

  const { value, timestamp } = await proxy.read();

  console.log('value     :', ethers.formatUnits(value, 18));
  console.log('timestamp :', new Date(Number(timestamp) * 1000).toISOString());
}

async function main() {
  const [, , proxyAddress, chainAlias] = process.argv;

  if (!proxyAddress || !chainAlias) {
    console.error('Usage: ts-node scripts/read-data-feed.ts <proxyAddress> <chainAlias>');
    process.exit(1);
  }

  const chain = findChainByAlias(chainAlias);
  if (!chain) {
    console.error(`Couldn't find chain with alias: ${chainAlias}. Please double-check the alias.`);
    process.exit(1);
  }

  const rpcUrl = chain.providers.find((p) => p.alias === 'default')?.rpcUrl;
  if (!rpcUrl) {
    console.error(`No default RPC URL found for chain: ${chainAlias}. Please give feedback to the API3 team about this.`);
    process.exit(1);
  }

  await readFeed(proxyAddress, rpcUrl);
}

main();
