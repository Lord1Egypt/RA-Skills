import { ethers } from 'ethers';
import { api3Contracts } from '@api3/dapi-management';

async function readFeed(proxyAddress: string, rpcUrl: string) {
  const provider = new ethers.JsonRpcProvider(rpcUrl);
  const proxy = api3Contracts.Api3ReaderProxyV1__factory.connect(proxyAddress, provider);
  const { value, timestamp } = await proxy.read();
  console.log('value     :', ethers.formatUnits(value, 18));
  console.log('timestamp :', new Date(Number(timestamp) * 1000).toISOString());
}

async function main() {
  const feedName = process.argv[2];
  if (!feedName) {
    console.error('Usage: ts-node read-data-feed.ts <feedName>');
    process.exit(1);
  }

  const chainAlias = process.argv[3];
  if (!chainAlias) {
    console.error('Usage: ts-node read-data-feed.ts <feedName> <chainAlias>');
    process.exit(1);
  }

  const chain = api3Contracts.CHAINS.find((c) => c.alias === chainAlias);
  if (!chain) {
    console.error(`Chain not found: ${chainAlias}`);
    process.exit(1);
  }

  const proxyAddress = api3Contracts.computeApi3ReaderProxyV1Address(chain.id, feedName, 1n, '0x');
  console.log('Proxy address:', proxyAddress);

  await readFeed(proxyAddress, chain.providers.find((p) => p.alias === 'default')!.rpcUrl!);
}

main();
