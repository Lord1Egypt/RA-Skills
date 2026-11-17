import fs from 'fs';
import dotenv from 'dotenv';
import { Connection, PublicKey } from '@solana/web3.js';
import { readFileLastLine } from '../utils/utils';
import {
  ensureIdlSaved,
  ensureOutputDir,
  getConnection,
  getHeliusApiKey,
  parseCliArgs,
  resolveTargetsFromOptions,
  TargetAccount,
  txLogsPath,
} from './common';

dotenv.config();

async function pullOne(target: TargetAccount, limit: number | null, recent: boolean) {
  const address = target.address;
  ensureOutputDir(address);
  const fpath = txLogsPath(address);
  console.log(`\n=== s1 pull [${address}]${limit ? ` limit=${limit}` : ''}${recent ? ' recent' : ''} ===`);

  await ensureIdlSaved(address);

  if (recent && limit) {
    const txs = await pullRecentTxs(address, limit);
    fs.writeFileSync(fpath, txs.map((t) => JSON.stringify(t)).join('\n') + (txs.length ? '\n' : ''));
    console.log(`[${address}] done, pulled ${txs.length} recent txs → ${fpath}`);
    return;
  }

  // Incremental historical pull (asc) via Helius
  const pageSize = 100;
  let latestTxSignature = '';

  let lastLine = '';
  if (fs.existsSync(fpath)) {
    lastLine = (await readFileLastLine(fpath)).replaceAll(' ', '');
    if (!lastLine) {
      lastLine = await readFileLastLine(fpath);
    }
  }

  if (lastLine) {
    try {
      const data = JSON.parse(lastLine);
      latestTxSignature = data.signature;
      console.log('resume after signature', latestTxSignature);
    } catch {
      console.warn('could not parse last line, starting fresh file');
      fs.writeFileSync(fpath, '');
    }
  } else {
    fs.writeFileSync(fpath, '');
  }

  let count = 0;
  while (true) {
    const dataList = await pullTxHelius(address, pageSize, latestTxSignature);

    if (!Array.isArray(dataList)) {
      console.error('unexpected response', dataList);
      break;
    }
    if (!dataList.length) {
      break;
    }

    count += dataList.length;
    console.log(`[${address}] count`, count);

    for (const item of dataList) {
      fs.appendFileSync(fpath, `${JSON.stringify(item)}\n`);
    }

    latestTxSignature = dataList[dataList.length - 1].signature;
    console.log(latestTxSignature);

    if (limit && count >= limit) {
      break;
    }
  }

  console.log(`[${address}] done, pulled ${count} txs → ${fpath}`);
}

async function pullRecentTxs(address: string, limit: number): Promise<unknown[]> {
  // Prefer Helius enhanced txs when key is present; else public RPC.
  try {
    getHeliusApiKey();
    console.log(`[${address}] using Helius (desc, limit=${limit})`);
    return await pullTxHelius(address, limit, undefined, 'desc');
  } catch {
    console.log(`[${address}] no HELIUS_API_KEY, using public Solana RPC`);
    return await pullRecentViaRpc(address, limit);
  }
}

async function pullRecentViaRpc(address: string, limit: number): Promise<unknown[]> {
  const connection = getConnection();
  const pubkey = new PublicKey(address);
  const sigInfos = await connection.getSignaturesForAddress(pubkey, { limit });
  console.log(`[${address}] got ${sigInfos.length} signatures`);

  const out: unknown[] = [];
  // Keep oldest→newest within the recent window
  const ordered = [...sigInfos].reverse();

  for (let i = 0; i < ordered.length; i++) {
    const info = ordered[i];
    let tx: Awaited<ReturnType<Connection['getParsedTransaction']>> = null;

    for (let attempt = 0; attempt < 8; attempt++) {
      try {
        tx = await connection.getParsedTransaction(info.signature, {
          maxSupportedTransactionVersion: 0,
        });
        break;
      } catch (err) {
        const msg = String(err);
        if (msg.includes('Too many requests') || msg.includes('429')) {
          const waitMs = Math.min(30_000, 1000 * 2 ** attempt);
          console.warn(`RPC rate limited, retry in ${waitMs}ms (${attempt + 1}/8)`);
          await sleep(waitMs);
          continue;
        }
        throw err;
      }
    }

    out.push(normalizeParsedTx(info.signature, info.blockTime ?? null, tx));
    if ((i + 1) % 10 === 0 || i + 1 === ordered.length) {
      console.log(`[${address}] fetched ${i + 1}/${ordered.length}`);
    }
    // gentle pacing for public RPC
    await sleep(200);
  }

  return out;
}

function normalizeParsedTx(
  signature: string,
  blockTime: number | null,
  tx: Awaited<ReturnType<Connection['getParsedTransaction']>>,
): Record<string, unknown> {
  if (!tx) {
    return { signature, timestamp: blockTime, instructions: [], error: 'tx not found' };
  }

  const message = tx.transaction.message;
  const accountKeys = message.accountKeys.map((k) =>
    typeof k === 'string' ? k : k.pubkey.toBase58(),
  );

  const instructions = message.instructions.map((ix) => {
    if ('parsed' in ix) {
      return {
        programId: ix.programId.toBase58(),
        parsed: ix.parsed,
        program: (ix as { program?: string }).program,
        accounts: [] as string[],
        data: null,
      };
    }
    const accounts = (ix.accounts as (number | PublicKey)[]).map((idx) =>
      typeof idx === 'number' ? accountKeys[idx] || String(idx) : idx.toBase58(),
    );
    return {
      programId: ix.programId.toBase58(),
      accounts,
      data: ix.data,
    };
  });

  const innerInstructions =
    tx.meta?.innerInstructions?.map((group) => ({
      index: group.index,
      instructions: group.instructions.map((ix) => {
        if ('parsed' in ix) {
          return {
            programId: ix.programId.toBase58(),
            parsed: ix.parsed,
            program: (ix as { program?: string }).program,
            accounts: [] as string[],
            data: null,
          };
        }
        const accounts = (ix.accounts as (number | PublicKey)[]).map((idx) =>
          typeof idx === 'number' ? accountKeys[idx] || String(idx) : idx.toBase58(),
        );
        return {
          programId: ix.programId.toBase58(),
          accounts,
          data: ix.data,
        };
      }),
    })) || [];

  return {
    signature,
    timestamp: blockTime,
    slot: tx.slot,
    feePayer: accountKeys[0],
    instructions,
    innerInstructions,
    source: 'rpc',
  };
}

async function main() {
  const opts = parseCliArgs();
  const targets = resolveTargetsFromOptions(opts);
  console.log(
    `targets (${targets.length}):`,
    targets.map((t) => t.address).join(', '),
  );
  for (const target of targets) {
    await pullOne(target, opts.limit, opts.recent);
  }
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});

async function sleep(ms: number) {
  await new Promise((r) => setTimeout(r, ms));
}

async function pullTxHelius(
  address: string,
  pageSize: number,
  latestTxSignature?: string,
  sortOrder: 'asc' | 'desc' = 'asc',
) {
  const apiKey = getHeliusApiKey();
  const params: string[] = [
    `api-key=${apiKey}`,
    `limit=${pageSize}`,
    `sort-order=${sortOrder}`,
  ];
  if (latestTxSignature && sortOrder === 'asc') {
    params.push(`after-signature=${latestTxSignature}`);
  }

  const url = `https://api.helius.xyz/v0/addresses/${address}/transactions?${params.join('&')}`;

  for (let attempt = 0; attempt < 8; attempt++) {
    const response = await fetch(url, {
      method: 'GET',
      headers: {},
    });
    const text = await response.text();

    if (response.status === 429 || text.includes('Too Many Requests')) {
      const waitMs = Math.min(60_000, 2000 * 2 ** attempt);
      console.warn(`rate limited, retry in ${waitMs}ms (attempt ${attempt + 1})`);
      await sleep(waitMs);
      continue;
    }

    if (!response.ok) {
      throw new Error(`Helius ${response.status}: ${text.slice(0, 200)}`);
    }

    try {
      return JSON.parse(text);
    } catch {
      throw new Error(`Invalid JSON from Helius: ${text.slice(0, 200)}`);
    }
  }

  throw new Error('Helius rate limited after retries');
}
