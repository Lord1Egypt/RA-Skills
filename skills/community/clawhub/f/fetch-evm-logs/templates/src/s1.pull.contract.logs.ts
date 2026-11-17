import { pullLogsByRPC } from './utils/utils.pull.log';
import { ContractConfigs } from './contract';
import { ensureContractOutputDir, logsTxtPath } from './paths';

async function main() {
  for (const config of ContractConfigs) {
    ensureContractOutputDir(config.address, config.chainId);
    const topics = config.getTopics();
    console.log('processing:', config.address);
    console.log('chainId', config.chainId);
    console.log('events', config.eventNames);
    console.log('topics', topics);

    await pullLogsByRPC(
      {
        rpc: config.rpc,
        contractAddress: config.address,
        fromBlock: config.startBlock,
        toBlock: config.endBlock,
        pageSize: 1000,
        topics,
      },
      logsTxtPath(config.address, config.chainId),
    );
  }
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
