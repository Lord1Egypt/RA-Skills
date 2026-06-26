import { api3Contracts } from '@api3/dapi-management';

function main() {
  const chains = api3Contracts.CHAINS.map((chain) => ({
    id: chain.id,
    name: chain.name,
    alias: chain.alias,
  }));
  console.log('Supported chains:');
  chains.forEach((chain) => console.log(`- ${chain.name} [alias: ${chain.alias}] (id: ${chain.id})`));
}

main();