import { dapis } from '@api3/dapi-management';

function main() {
  console.log('Available dAPIs:');
  dapis
    .filter((dapi) => dapi.stage === 'active')
    .forEach((dapi) => console.log(`- ${dapi.name}`));
}

main();
