import { api3Contracts } from '@api3/dapi-management';

function main() {
  console.log('Supported chains:');
  api3Contracts.CHAINS.forEach((chain) =>
    console.log(`- ${chain.name} [alias: ${chain.alias}] (id: ${chain.id})`)
  );
}

main();
