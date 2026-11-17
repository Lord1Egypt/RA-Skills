import fs from 'fs';
import { ethers } from 'ethers';
import { readFileLastLine, sleep } from './utils';

export interface PullLogsByRPCConfig {
  /** Primary RPC, or ordered list for automatic failover. */
  rpc: string | string[];
  contractAddress: string;
  fromBlock: number;
  toBlock?: number | 'latest';
  pageSize: number;
  /** eth_getLogs topics filter. [] = all logs for address. */
  topics: (string | string[] | null)[];
  /** Retries on the same RPC before rotating (default 3). */
  retriesPerRpc?: number;
}

function normalizeRpcList(rpc: string | string[]): string[] {
  const list = (Array.isArray(rpc) ? rpc : [rpc])
    .map((u) => u.trim())
    .filter(Boolean);
  if (!list.length) {
    throw new Error('At least one RPC URL is required');
  }
  return list;
}

function createProvider(url: string) {
  return new ethers.JsonRpcProvider(url, undefined, { batchMaxCount: 1 });
}

function formatPct(done: number, total: number): string {
  if (total <= 0) return '100.0%';
  return `${Math.min(100, (done / total) * 100).toFixed(1)}%`;
}

export async function pullLogsByRPC(
  cfg: PullLogsByRPCConfig,
  outputPath: string,
) {
  const rpcs = normalizeRpcList(cfg.rpc);
  const retriesPerRpc = cfg.retriesPerRpc ?? 3;
  let rpcIndex = 0;
  let provider = createProvider(rpcs[rpcIndex]);
  console.log(`rpc[${rpcIndex}]: ${rpcs[rpcIndex]} (${rpcs.length} endpoint(s))`);

  async function withRpcFailover<T>(
    label: string,
    fn: (p: ethers.JsonRpcProvider) => Promise<T>,
  ): Promise<T> {
    let lastErr: unknown;
    for (let rotate = 0; rotate < rpcs.length; rotate++) {
      for (let attempt = 1; attempt <= retriesPerRpc; attempt++) {
        try {
          return await fn(provider);
        } catch (err) {
          lastErr = err;
          const msg = err instanceof Error ? err.message : String(err);
          console.warn(
            `${label} failed on rpc[${rpcIndex}] attempt ${attempt}/${retriesPerRpc}: ${msg}`,
          );
          await sleep(2);
        }
      }
      rpcIndex = (rpcIndex + 1) % rpcs.length;
      provider = createProvider(rpcs[rpcIndex]);
      console.warn(`switching RPC → rpc[${rpcIndex}]: ${rpcs[rpcIndex]}`);
    }
    throw new Error(
      `${label} failed on all ${rpcs.length} RPC endpoint(s): ${String(lastErr)}`,
    );
  }

  const latestBlock = await withRpcFailover('getBlockNumber', (p) =>
    p.getBlockNumber(),
  );
  const effectiveToBlock =
    cfg.toBlock == null || cfg.toBlock === 'latest' ? latestBlock : cfg.toBlock;
  console.log(`latestBlock=${latestBlock} targetToBlock=${effectiveToBlock}`);

  let currentFrom = cfg.fromBlock;
  if (fs.existsSync(outputPath)) {
    const lastLine = await readFileLastLine(outputPath);
    if (lastLine) {
      const data = JSON.parse(lastLine);
      if (data.blockNumber != null) {
        const lastBlock = Number(data.blockNumber);
        currentFrom = lastBlock + 1;
        console.log(`resume from block ${currentFrom} (last synced ${lastBlock})`);
      }
    }
  } else {
    fs.writeFileSync(outputPath, '');
  }

  if (currentFrom > effectiveToBlock) {
    console.log('already up to date');
    return;
  }

  const rangeStart = currentFrom;
  const totalBlocks = effectiveToBlock - rangeStart + 1;
  let count = 0;
  const startedAt = Date.now();

  while (currentFrom <= effectiveToBlock) {
    let currentTo = currentFrom + cfg.pageSize - 1;
    if (currentTo > effectiveToBlock) currentTo = effectiveToBlock;

    const reqParams = {
      address: cfg.contractAddress,
      fromBlock: currentFrom,
      toBlock: currentTo,
      topics: cfg.topics || [],
    };

    const logs = await withRpcFailover(
      `getLogs ${currentFrom}-${currentTo}`,
      (p) => p.getLogs(reqParams),
    );
    count += logs.length;

    if (logs.length > 0) {
      fs.appendFileSync(
        outputPath,
        logs.map((item) => `${JSON.stringify(item)}\n`).join(''),
      );
    }

    const doneBlocks = currentTo - rangeStart + 1;
    const elapsedSec = Math.max(1, (Date.now() - startedAt) / 1000);
    const blocksPerSec = doneBlocks / elapsedSec;
    const remainBlocks = effectiveToBlock - currentTo;
    const etaSec = blocksPerSec > 0 ? Math.round(remainBlocks / blocksPerSec) : 0;
    const eta =
      etaSec > 120
        ? `${Math.round(etaSec / 60)}m`
        : etaSec > 0
          ? `${etaSec}s`
          : 'done';

    console.log(
      `[${formatPct(doneBlocks, totalBlocks)}] blocks ${currentFrom}-${currentTo}` +
        ` / ${effectiveToBlock} | +${logs.length} logs (total ${count})` +
        ` | eta~${eta} | rpc[${rpcIndex}]`,
    );

    currentFrom = currentTo + 1;
  }

  console.log(`done: ${count} logs → ${outputPath}`);
}
