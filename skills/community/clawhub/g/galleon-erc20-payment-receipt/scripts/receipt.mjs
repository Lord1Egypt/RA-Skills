import { open } from "node:fs/promises";
import { pathToFileURL } from "node:url";

const transferTopic = "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef";
const addressPattern = /^0x[0-9a-f]{40}$/i;
const hashPattern = /^0x[0-9a-f]{64}$/i;
const quantityPattern = /^0x(?:0|[1-9a-f][0-9a-f]{0,63})$/i;
const indexedAddress = /^0x0{24}[0-9a-f]{40}$/i;
const zeroAddress = "0x" + "0".repeat(40);

function field(value, pattern, name) {
  if (typeof value !== "string" || !pattern.test(value)) throw new Error(`Invalid ${name}`);
  return value.toLowerCase();
}

function blockHeader(block) {
  return {
    number: BigInt(field(block?.number, quantityPattern, "header number")),
    hash: field(block?.hash, hashPattern, "header hash"),
  };
}

export function reconcile(input) {
  const expected = input?.expected;
  const tx = field(expected?.transactionHash, hashPattern, "expected transaction hash");
  const token = field(expected?.token, addressPattern, "expected token");
  const sender = field(expected?.sender, addressPattern, "expected sender");
  const recipient = field(expected?.recipient, addressPattern, "expected recipient");
  if ([token, sender, recipient].includes(zeroAddress) || sender === recipient) throw new Error("Expected payment requires distinct accounts and nonzero addresses");
  if (!Number.isSafeInteger(expected.chainId) || expected.chainId < 1) throw new Error("Invalid expected chain ID");
  if (typeof expected.amountRaw !== "string" || !/^[1-9][0-9]{0,77}$/.test(expected.amountRaw) || BigInt(expected.amountRaw) >= 2n ** 256n) throw new Error("Invalid positive raw amount");
  const result = { chainId: expected.chainId, transactionHash: tx, token, sender, recipient, expectedRaw: expected.amountRaw };
  const state = (status, evidence = {}) => ({ ...result, status, ...evidence });
  if (BigInt(field(input.chainId, quantityPattern, "RPC chain ID")) !== BigInt(expected.chainId)) return state("chain-mismatch");
  const r = input.receipt;
  if (r === null) return state("receipt-unavailable");
  if (field(r?.transactionHash, hashPattern, "receipt transaction hash") !== tx) return state("transaction-mismatch");
  const hash = field(r.blockHash, hashPattern, "receipt block hash");
  const number = BigInt(field(r.blockNumber, quantityPattern, "receipt block number"));
  if (input.canonicalBlock == null) return state("canonical-block-unavailable");
  const canonical = blockHeader(input.canonicalBlock);
  if (canonical.number !== number || canonical.hash !== hash) return state("canonical-block-mismatch");
  let finality = "unverified";
  if (input.finalizedBlock != null) {
    const finalized = blockHeader(input.finalizedBlock);
    if (finalized.number === number && finalized.hash !== hash) return state("finalized-block-mismatch");
    finality = finalized.number >= number ? "rpc-finalized" : "awaiting-finality";
  }
  const inclusion = { blockHash: hash, blockNumber: number.toString(), finality };
  if (r.status === "0x0") return state("reverted", inclusion);
  if (r.status !== "0x1" || !Array.isArray(r.logs) || r.logs.length > 10000) throw new Error("Invalid receipt status or logs");

  const seen = new Set();
  const matches = [];
  let outgoing = 0n;
  for (const log of r.logs) {
    const emitter = field(log?.address, addressPattern, "log emitter");
    if (!Array.isArray(log.topics)) throw new Error("Invalid log topics");
    if (emitter !== token || log.topics[0]?.toLowerCase() !== transferTopic) continue;
    if (log.removed !== undefined && log.removed !== false) return state("conflicting-log", inclusion);
    if (field(log.transactionHash, hashPattern, "log transaction hash") !== tx ||
        field(log.blockHash, hashPattern, "log block hash") !== hash ||
        BigInt(field(log.blockNumber, quantityPattern, "log block number")) !== number) return state("conflicting-log", inclusion);
    const index = BigInt(field(log.logIndex, quantityPattern, "log index")).toString();
    if (seen.has(index)) return state("conflicting-log", inclusion);
    seen.add(index);
    if (log.topics.length !== 3) return state("nonstandard-transfer-log", inclusion);
    const from = "0x" + field(log.topics[1], indexedAddress, "indexed sender").slice(-40);
    const to = "0x" + field(log.topics[2], indexedAddress, "indexed recipient").slice(-40);
    const amount = BigInt(field(log.data, hashPattern, "transfer amount"));
    if (from === sender && to === recipient) matches.push({ logIndex: index, amountRaw: amount.toString() });
    if (from === recipient && to !== recipient) outgoing += amount;
  }
  const gross = matches.reduce((sum, match) => sum + BigInt(match.amountRaw), 0n);
  const evidence = { ...inclusion, matches, senderToRecipientRaw: gross.toString(), recipientOutgoingRaw: outgoing.toString() };
  if (!matches.length) return state("no-matching-transfer", evidence);
  if (gross !== BigInt(expected.amountRaw)) return state("amount-mismatch", evidence);
  if (matches.length !== 1) return state("multiple-transfers-review", evidence);
  if (outgoing > 0n) return state("recipient-forwarded-review", evidence);
  return state("transfer-event-matched", evidence);
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  let file;
  try {
    if (process.argv.length !== 3) throw new Error("Supply one receipt evidence JSON file");
    file = await open(process.argv[2], "r");
    const stat = await file.stat();
    if (!stat.isFile() || stat.size > 4 * 1024 * 1024) throw new Error("Supply a regular JSON file up to 4 MiB");
    console.log(JSON.stringify(reconcile(JSON.parse(await file.readFile("utf8"))), null, 2));
  } catch (error) {
    console.error(error instanceof SyntaxError ? "Invalid evidence JSON" : error.message);
    process.exitCode = 1;
  } finally {
    await file?.close();
  }
}
