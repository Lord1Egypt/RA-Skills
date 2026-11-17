import fs from 'fs';
import dotenv from 'dotenv';
import { BorshCoder, Idl } from '@coral-xyz/anchor';
import { bs58 } from '@coral-xyz/anchor/dist/cjs/utils/bytes';
import { streamReadCSV } from '../utils/utils';
import {
  ensureOutputDir,
  idlOutputPath,
  loadOrFetchIdl,
  makeInstructionCoder,
  parseCliArgs,
  resolveAccountType,
  resolveTargetsFromOptions,
  serializeDecoded,
  TargetAccount,
  txLogsPath,
  txParsedPath,
} from './common';

dotenv.config();

interface HeliusInstruction {
  programId?: string;
  accounts?: string[];
  data?: unknown;
  innerInstructions?: HeliusInstruction[];
  [key: string]: unknown;
}

interface DecodedIx {
  name: string;
  data: unknown;
  accountsNamed?: Record<string, string>;
}

function decodeIxDataToBuffer(ixData: unknown): Buffer {
  if (Buffer.isBuffer(ixData)) return ixData;
  if (ixData instanceof Uint8Array) return Buffer.from(ixData);
  if (Array.isArray(ixData)) return Buffer.from(ixData as number[]);
  if (typeof ixData === 'string') {
    // Helius usually returns base58; also accept hex / base64
    try {
      return Buffer.from(bs58.decode(ixData) as Uint8Array);
    } catch {
      if (/^[0-9a-fA-F]+$/.test(ixData) && ixData.length % 2 === 0) {
        return Buffer.from(ixData, 'hex');
      }
      try {
        return Buffer.from(ixData, 'base64');
      } catch {
        return Buffer.alloc(0);
      }
    }
  }
  return Buffer.alloc(0);
}

function safeDecodeByIdl(coder: BorshCoder, data: Buffer): DecodedIx | null {
  try {
    const decoded = coder.instruction.decode(data);
    if (!decoded) return null;
    return {
      name: decoded.name,
      data: serializeDecoded(decoded.data),
    };
  } catch {
    return null;
  }
}

function mapAccountsNamed(
  idl: Idl,
  ixName: string,
  accounts: string[] | undefined,
): Record<string, string> | undefined {
  if (!accounts?.length) return undefined;
  const idlIx = idl.instructions?.find((i) => i.name === ixName);
  if (!idlIx?.accounts?.length) return undefined;

  const named: Record<string, string> = {};
  idlIx.accounts.forEach((acc, idx) => {
    const name = (acc as { name?: string }).name;
    if (name && accounts[idx]) {
      named[name] = accounts[idx];
    }
  });
  return Object.keys(named).length ? named : undefined;
}

function enrichInstruction(
  ix: HeliusInstruction,
  programAddress: string,
  coder: BorshCoder,
  idl: Idl,
): HeliusInstruction {
  const out: HeliusInstruction = { ...ix };

  if (ix.programId === programAddress && ix.data != null) {
    const buf = decodeIxDataToBuffer(ix.data);
    const decoded = safeDecodeByIdl(coder, buf);
    if (decoded) {
      const accountsNamed = mapAccountsNamed(idl, decoded.name, ix.accounts);
      out.parsed = {
        name: decoded.name,
        data: decoded.data,
        ...(accountsNamed ? { accountsNamed } : {}),
      };
    } else {
      out.parsed = null;
    }
  }

  if (Array.isArray(ix.innerInstructions)) {
    out.innerInstructions = ix.innerInstructions.map((inner) =>
      enrichInstruction(inner, programAddress, coder, idl),
    );
  }

  // Helius sometimes nests inner ix under instructions[i].innerInstructions
  // or as top-level innerInstructions — handled by caller for top-level.

  return out;
}

function enrichTx(
  tx: Record<string, unknown>,
  programAddress: string,
  coder: BorshCoder,
  idl: Idl,
): Record<string, unknown> {
  const instructions = (tx.instructions as HeliusInstruction[]) || [];
  const enrichedIx = instructions.map((ix) =>
    enrichInstruction(ix, programAddress, coder, idl),
  );

  const result: Record<string, unknown> = {
    ...tx,
    instructions: enrichedIx,
  };

  // Some payloads put CPI under top-level innerInstructions: [{ index, instructions }]
  const topInner = tx.innerInstructions as
    | Array<{ index?: number; instructions?: HeliusInstruction[] }>
    | undefined;
  if (Array.isArray(topInner)) {
    result.innerInstructions = topInner.map((group) => ({
      ...group,
      instructions: (group.instructions || []).map((ix) =>
        enrichInstruction(ix, programAddress, coder, idl),
      ),
    }));
  }

  return result;
}

async function parseOne(target: TargetAccount) {
  const address = target.address;
  const fpath = txLogsPath(address);
  const outPath = txParsedPath(address);
  console.log(`\n=== s2 parse [${address}] ${fpath} ===`);

  if (!fs.existsSync(fpath)) {
    console.warn(`[${address}] missing ${fpath}, skip (run s1 first)`);
    return;
  }

  const accountType = await resolveAccountType(target);
  console.log(`[${address}] resolved type: ${accountType}`);

  let coder: BorshCoder | null = null;
  let idl: Idl | null = null;

  if (accountType === 'program') {
    idl = await loadOrFetchIdl(address);
    if (!idl) {
      console.error(
        `[${address}] No IDL found on-chain or in output.\n` +
          `  Place an Anchor IDL JSON at: ${idlOutputPath(address)}\n` +
          `  Then re-run s2. Raw txs will still be written without decoded instructions.`,
      );
    } else {
      coder = makeInstructionCoder(idl);
      const names = idl.instructions?.map((i) => i.name) || [];
      console.log(`[${address}] IDL instructions (${names.length}):`, names.join(', '));
    }
  }

  const txList: unknown[] = [];
  let decodedCount = 0;

  await streamReadCSV(fpath, (line, idx) => {
    if (!line) return;
    if (idx % 1000 === 0) console.log(`[${address}]`, idx);

    const data = JSON.parse(line) as Record<string, unknown>;
    if (coder && idl) {
      const enriched = enrichTx(data, address, coder, idl);
      const ixs = (enriched.instructions as HeliusInstruction[]) || [];
      for (const ix of ixs) {
        if (ix.parsed) decodedCount++;
      }
      txList.push(enriched);
    } else {
      txList.push(data);
    }
  });

  ensureOutputDir(address);
  fs.writeFileSync(outPath, JSON.stringify(txList, null, 2));
  console.log(
    `[${address}] done ${txList.length} txs` +
      (accountType === 'program' ? `, decoded ${decodedCount} program ixs` : '') +
      ` → ${outPath}`,
  );
}

async function main() {
  const opts = parseCliArgs();
  const targets = resolveTargetsFromOptions(opts);
  console.log(`targets (${targets.length}):`, targets.map((t) => t.address).join(', '));
  for (const target of targets) {
    await parseOne(target);
  }
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
