import { ContractConfigs } from './contract';
import { logsJsonPath, logsTxtPath } from './paths';
import { streamReadLines } from './utils/utils';
import fs from 'fs';

async function main() {
  for (const config of ContractConfigs) {
    console.log('processing:', config.address);
    console.log('chainId', config.chainId);
    console.log('events', config.eventNames);

    const filePath = logsTxtPath(config.address, config.chainId);
    const parsedLogsMap: Record<string, NonNullable<ReturnType<typeof config.parseLog>>> =
      {};

    await streamReadLines(filePath, (line) => {
      if (!line) {
        return;
      }
      const log = config.parseLog(JSON.parse(line));
      if (!log) {
        return;
      }
      parsedLogsMap[`${log.txHash}-${log.logIndex}`] = log;
    });

    console.log('count', Object.keys(parsedLogsMap).length);

    fs.writeFileSync(
      logsJsonPath(config.address, config.chainId),
      JSON.stringify(Object.values(parsedLogsMap), null, 2),
    );
  }
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
