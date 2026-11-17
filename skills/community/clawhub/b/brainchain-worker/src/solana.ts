// `fund --from-solana`: an agent that lives on Solana funds its BrainChain worker in one command. Relay turns its USDC
// on Solana into ETH (and, with --stake, BRAIN) for the worker's wallet on Robinhood Chain in about a second, signed by
// the agent's Solana key; `bridge` then moves on to BrainChain what this run brought. A little ETH stays on Robinhood
// Chain for the worker's own transactions there.

import { readFileSync } from "node:fs";

import bs58 from "bs58";
import { AddressLookupTableAccount, Connection, Keypair, PublicKey, SendTransactionError, TransactionInstruction, TransactionMessage, VersionedTransaction } from "@solana/web3.js";
import { formatEther, formatUnits, parseUnits, type Address } from "viem";

import { reason } from "./chain.js";
import { expandHome } from "./key.js";
import { checkReturn, MAX_LOSS, MAX_STAKE_LOSS, NATIVE, RELAY_API, RelayError, relayQuote, SOLANA_CHAIN_ID, SOLANA_USDC, waitForRelay, type RelayQuote, type RelayStatus, type SvmItem } from "./relay.js";

export const SOLANA_RPC = "https://api.mainnet-beta.solana.com";
/** USDC turned into ETH for gas, unless --gas-usdc says otherwise. */
export const DEFAULT_GAS_USDC = "2";
/** ETH left on Robinhood Chain when the rest goes to BrainChain: enough for a token deposit and a few transactions there. */
export const PARENT_ETH_KEEP = 300_000_000_000_000n;
/** How often a balance is read after Relay reports a move settled, and how far apart: the chain's RPC can lag Relay's word. */
const ARRIVAL_READS = 10;
const ARRIVAL_WAIT_MS = 3_000;

/** Relay's depository program, the instruction that deposits a token into it, and the accounts it keeps. */
export const RELAY_DEPOSITORY = "99vQwtBwYtrqqD9YSXbdum3KBdxPAVxYTaQ3cfnJSrN2";
const DEPOSIT_TOKEN = "0b9c60da27a3b413";
export const DEPOSITORY_STATE = "Dodg2HifwU8rmaVVyMyUZDGTRbqAJTyVYxXPwcbNpBKc";
export const DEPOSITORY_VAULT = "7uTT8Xi5RWXzy7h9XL244GRgEycDYDhLjr3ZyNdXi8pZ";
export const DEPOSITORY_VAULT_USDC = "4nvJ5zWdVspxJiNZzB127U6amPH98SFFkBx2JZrAduia";
export const TOKEN_PROGRAM = "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA";
export const ASSOCIATED_TOKEN_PROGRAM = "ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL";
const SYSTEM_PROGRAM = "11111111111111111111111111111111";

/** A wallet's associated token account for USDC. */
export function usdcAccount(owner: string): string {
  const seeds = [new PublicKey(owner).toBuffer(), new PublicKey(TOKEN_PROGRAM).toBuffer(), new PublicKey(SOLANA_USDC).toBuffer()];
  return PublicKey.findProgramAddressSync(seeds, new PublicKey(ASSOCIATED_TOKEN_PROGRAM))[0].toBase58();
}

/** The Solana key from BRAINCHAIN_SOLANA_KEY (base58) or BRAINCHAIN_SOLANA_KEY_FILE (a Solana CLI keypair file). */
export function solanaKeypair(env: NodeJS.ProcessEnv = process.env): Keypair {
  const file = env.BRAINCHAIN_SOLANA_KEY_FILE?.trim();
  const inline = env.BRAINCHAIN_SOLANA_KEY?.trim();
  if (file && inline) throw new Error("Set BRAINCHAIN_SOLANA_KEY or BRAINCHAIN_SOLANA_KEY_FILE, not both");
  const raw = file ? readKeyFile(file) : inline;
  if (!raw) throw new Error("Set BRAINCHAIN_SOLANA_KEY to the Solana wallet's secret key (base58), or BRAINCHAIN_SOLANA_KEY_FILE to its keypair file");
  try {
    const bytes = raw.startsWith("[") ? Uint8Array.from(JSON.parse(raw) as number[]) : bs58.decode(raw);
    return Keypair.fromSecretKey(bytes);
  } catch {
    throw new Error("The Solana key must be a 64-byte secret key, in base58 or as a keypair file's JSON array");
  }
}

function readKeyFile(path: string): string {
  const file = expandHome(path);
  try {
    return readFileSync(file, "utf8").trim();
  } catch (error) {
    throw new Error(`BRAINCHAIN_SOLANA_KEY_FILE names ${file}, which could not be read (${(error as NodeJS.ErrnoException).code ?? "unknown error"})`);
  }
}

/** How a USDC amount splits between gas and stake. Without --stake, what gas does not take stays on Solana. */
export function split(usdc: bigint, gasUsdc: bigint, stake: boolean): { gas: bigint; stake: bigint } {
  if (!stake) return { gas: usdc < gasUsdc ? usdc : gasUsdc, stake: 0n };
  if (usdc <= gasUsdc) throw new Error(`With --stake the amount must be more than the ${formatUnits(gasUsdc, 6)} USDC kept for gas`);
  return { gas: gasUsdc, stake: usdc - gasUsdc };
}

interface DepositWanted {
  owner: string;
  amount: bigint;
  recipient: string;
  currency: string;
  chainId: number;
}

/**
 * What is wrong with a quote's Solana side, or undefined when it is the one
 * thing this command signs: one deposit into Relay's depository, of the USDC
 * asked for, from this wallet's own token account, paying the worker on the
 * parent chain. Every field a real quote carries is checked, so anything else
 * Relay's API answers is refused.
 */
export function depositProblem(quote: RelayQuote, want: DepositWanted): string | undefined {
  try {
    return readDeposit(quote, want);
  } catch {
    return "it is in a form this command cannot read";
  }
}

function readDeposit(quote: RelayQuote, want: DepositWanted): string | undefined {
  const [step, ...others] = quote.steps;
  if (step === undefined || others.length > 0 || step.id !== "deposit" || step.items?.length !== 1) return "it is not one deposit";
  const { instructions } = step.items[0]!.data as SvmItem;
  if (!Array.isArray(instructions) || instructions.length !== 1) return `it carries ${Array.isArray(instructions) ? instructions.length : "no"} instructions where a deposit has one`;
  const { programId, data, keys } = instructions[0]!;
  if (programId !== RELAY_DEPOSITORY) return `it calls the program ${programId}, not Relay's depository`;
  const bytes = Buffer.from(String(data).replace(/^0x/, ""), "hex");
  if (bytes.length !== 48 || bytes.subarray(0, 8).toString("hex") !== DEPOSIT_TOKEN) return "it calls Relay's depository for something other than a token deposit";
  const amount = bytes.readBigUInt64LE(8);
  if (amount !== want.amount) return `it deposits ${formatUnits(amount, 6)} USDC, not the ${formatUnits(want.amount, 6)} asked for`;
  const accounts = [DEPOSITORY_STATE, want.owner, want.owner, DEPOSITORY_VAULT, SOLANA_USDC, usdcAccount(want.owner), DEPOSITORY_VAULT_USDC, TOKEN_PROGRAM, ASSOCIATED_TOKEN_PROGRAM, SYSTEM_PROGRAM];
  if (!Array.isArray(keys) || keys.length !== accounts.length) return `it names ${Array.isArray(keys) ? keys.length : "no"} accounts where a deposit names ${accounts.length}`;
  const wrong = accounts.findIndex((account, i) => keys[i]!.pubkey !== account);
  if (wrong >= 0) return `its account ${wrong} is ${keys[wrong]!.pubkey}, not ${accounts[wrong]}`;
  if (keys.some((key, i) => key.isSigner !== (i === 1))) return "it asks another account to sign";
  if (quote.recipient?.toLowerCase() !== want.recipient.toLowerCase()) return `it pays ${quote.recipient ?? "no named recipient"}, not ${want.recipient}`;
  if (quote.outCurrency?.toLowerCase() !== want.currency.toLowerCase() || quote.outChainId !== want.chainId) return "it does not pay the currency asked for on Robinhood Chain";
  return undefined;
}

const notConfirmed = (signature: string, why: unknown) =>
  new Error(`the Solana transaction ${signature} could not be confirmed (${reason(why)}). Check it before running fund again: if it landed, its USDC left the wallet, and another run moves USDC again.`);

/** Sends Relay's Solana deposit: its instructions, compiled against its lookup tables, signed by the agent's key. Each failure says whether the USDC moved. */
export async function sendSvmStep(connection: Connection, keypair: Keypair, item: SvmItem): Promise<string> {
  const instructions = item.instructions.map(
    (i) =>
      new TransactionInstruction({
        programId: new PublicKey(i.programId),
        keys: i.keys.map((k) => ({ pubkey: new PublicKey(k.pubkey), isSigner: k.isSigner, isWritable: k.isWritable })),
        data: Buffer.from(i.data.replace(/^0x/, ""), "hex"),
      }),
  );
  const tables: AddressLookupTableAccount[] = [];
  for (const address of item.addressLookupTableAddresses) {
    const table = (await connection.getAddressLookupTable(new PublicKey(address))).value;
    if (table) tables.push(table);
  }
  const { blockhash, lastValidBlockHeight } = await connection.getLatestBlockhash("confirmed");
  const message = new TransactionMessage({ payerKey: keypair.publicKey, recentBlockhash: blockhash, instructions }).compileToV0Message(tables);
  const transaction = new VersionedTransaction(message);
  transaction.sign([keypair]);
  // A signed transaction's first signature is its id, known whether or not the send comes back.
  const signature = bs58.encode(transaction.signatures[0]!);
  try {
    await connection.sendTransaction(transaction, { maxRetries: 3 });
  } catch (error) {
    if (error instanceof SendTransactionError) throw new Error(`Solana refused the deposit, so its USDC did not move: ${error.message.split("\n")[0]}`);
    throw notConfirmed(signature, error);
  }
  const confirmed = await connection.confirmTransaction({ signature, blockhash, lastValidBlockHeight }, "confirmed").catch((error: unknown) => {
    throw notConfirmed(signature, error);
  });
  if (confirmed.value.err) throw new Error(`the Solana transaction ${signature} failed, so its USDC did not move: ${JSON.stringify(confirmed.value.err)}`);
  return signature;
}

/** What to say about a deposit Relay has not filled, or undefined once it has. Only `refund` says the USDC is back; `failure` is usually not final, and `pending` is a wait that ran out. */
export function unsettled(status: RelayStatus, requestId: string, signature: string, owner: string): string | undefined {
  if (status === "success") return undefined;
  if (status === "refund") return `Relay reports a refund for request ${requestId}: the USDC of Solana transaction ${signature} goes back to ${owner}. Check the wallet before running fund again.`;
  return `Relay has not settled request ${requestId} (it reports "${status}"). The USDC left the wallet in Solana transaction ${signature}. Check ${RELAY_API}/intents/status/v2?requestId=${requestId} before running fund again: another run moves USDC again.`;
}

export interface SolanaFunding {
  /** Quotes the move and checks its price and its deposit without sending anything. */
  preview(currency: string, amount: bigint, recipient: Address): Promise<RelayQuote>;
  /** Signs a checked quote's deposit, sends it, waits for Relay to fill it, and returns the Solana signature. */
  send(quote: RelayQuote): Promise<string>;
  usdcBalance(): Promise<bigint>;
  solBalance(): Promise<bigint>;
  owner: string;
}

export function createSolanaFunding(keypair: Keypair, parentChainId: number, rpc = SOLANA_RPC): SolanaFunding {
  const connection = new Connection(rpc, "confirmed");
  const owner = keypair.publicKey.toBase58();
  return {
    owner,
    async usdcBalance() {
      const accounts = await connection.getParsedTokenAccountsByOwner(keypair.publicKey, { mint: new PublicKey(SOLANA_USDC) });
      return accounts.value.reduce((sum, a) => sum + BigInt(a.account.data.parsed.info.tokenAmount.amount as string), 0n);
    },
    async solBalance() {
      return BigInt(await connection.getBalance(keypair.publicKey));
    },
    async preview(currency, amount, recipient) {
      const quote = await relayQuote({ user: owner, recipient, originChainId: SOLANA_CHAIN_ID, destinationChainId: parentChainId, originCurrency: SOLANA_USDC, destinationCurrency: currency, amount });
      checkReturn(quote, currency === NATIVE ? MAX_LOSS : MAX_STAKE_LOSS);
      const problem = depositProblem(quote, { owner, amount, recipient, currency, chainId: parentChainId });
      if (problem) throw new RelayError(`Relay's quote was refused before signing: ${problem}. Nothing was sent.`);
      return quote;
    },
    async send(quote) {
      const signature = await sendSvmStep(connection, keypair, quote.steps[0]!.items[0]!.data as SvmItem);
      const problem = unsettled(await waitForRelay(quote.requestId), quote.requestId, signature, owner);
      if (problem) throw new Error(problem);
      return signature;
    },
  };
}

/** The least SOL the wallet needs to pay Solana's fees for the deposits. */
export const MIN_LAMPORTS = 2_000_000n;

/** What a move added to a balance, no more than was quoted, so a deposit from elsewhere stays out of it. */
async function arrival(read: () => Promise<bigint>, before: bigint, quoted: bigint, sleep: (ms: number) => Promise<void>): Promise<{ held: bigint; brought: bigint }> {
  let held = await read();
  for (let tries = 1; held <= before && tries < ARRIVAL_READS; tries++) {
    await sleep(ARRIVAL_WAIT_MS);
    held = await read();
  }
  const rise = held > before ? held - before : 0n;
  return { held, brought: rise < quoted ? rise : quoted };
}

export async function fundFromSolana(
  options: {
    funding: SolanaFunding;
    worker: Address;
    usdc: string;
    gasUsdc?: string;
    stake: boolean;
    stakeToken?: Address;
    dry: boolean;
    log: (line: string) => void;
    /** The worker's balances on the parent chain, read before and after the moves. */
    parentEth: () => Promise<bigint>;
    parentStake: () => Promise<bigint>;
    /** Moves an amount from the parent chain to BrainChain once it has landed; `bridge` in the CLI. */
    bridgeOn: (asset: "eth" | "stake", amount: bigint) => Promise<void>;
    sleep?: (ms: number) => Promise<void>;
  },
): Promise<void> {
  const { funding, log } = options;
  const sleep = options.sleep ?? ((ms: number) => new Promise((r) => setTimeout(r, ms)));
  const usdc = parseUnits(options.usdc, 6);
  const gasUsdc = parseUnits(options.gasUsdc ?? DEFAULT_GAS_USDC, 6);
  const parts = split(usdc, gasUsdc, options.stake);
  if (options.stake && !options.stakeToken) throw new Error("This network's stake token is not on the parent chain");
  const spends = parts.gas + parts.stake;
  const [held, lamports] = await Promise.all([funding.usdcBalance(), funding.solBalance()]);
  if (held < spends) throw new Error(`The Solana wallet ${funding.owner} holds ${formatUnits(held, 6)} USDC, less than ${formatUnits(spends, 6)}`);
  if (lamports < MIN_LAMPORTS) throw new Error(`The Solana wallet ${funding.owner} needs about 0.002 SOL for Solana's fees; it holds ${formatUnits(lamports, 9)}`);
  const stays = usdc > spends ? ` The other ${formatUnits(usdc - spends, 6)} USDC stays on Solana.` : "";
  log(`From ${funding.owner} on Solana: ${formatUnits(parts.gas, 6)} USDC to ETH for gas${parts.stake ? ` and ${formatUnits(parts.stake, 6)} USDC to the stake token` : ""}, for ${options.worker}.${stays}`);
  // Both legs are priced and checked before either moves, and those same quotes are signed, so a refused leg never leaves the other spent alone.
  const gasQuote = await funding.preview(NATIVE, parts.gas, options.worker);
  const stakeQuote = parts.stake ? await funding.preview(options.stakeToken!, parts.stake, options.worker) : undefined;
  log(`Relay quotes ${gasQuote.outFormatted} ETH${stakeQuote ? ` and ${stakeQuote.outFormatted} of the stake token` : ""}.`);
  if (options.dry) {
    log("Dry run, nothing sent.");
    return;
  }
  // Read before anything moves: only what this run adds goes on to BrainChain, never what the wallet already held.
  const readStake = () => (stakeQuote ? options.parentStake() : Promise.resolve(0n));
  const [ethBefore, stakeBefore] = await Promise.all([options.parentEth(), readStake()]).catch((error: unknown) => {
    throw new Error(`Could not read the worker's balances on Robinhood Chain, so what this run brings could not be told from what it holds: ${reason(error).replace(/\.$/, "")}. Nothing was sent.`);
  });

  const onParent = new Map<"eth" | "stake", string>();
  try {
    const gas = await funding.send(gasQuote);
    onParent.set("eth", `${gasQuote.outFormatted} ETH`);
    log(`ETH arrived on Robinhood Chain: ${gasQuote.outFormatted} ETH (Solana ${gas}).`);
    if (stakeQuote) {
      const stake = await funding.send(stakeQuote);
      onParent.set("stake", `${stakeQuote.outFormatted} of the stake token`);
      log(`Stake token arrived on Robinhood Chain: ${stakeQuote.outFormatted} (Solana ${stake}).`);
    }
    const eth = await arrival(options.parentEth, ethBefore, gasQuote.outAmount, sleep);
    const stake = stakeQuote ? await arrival(options.parentStake, stakeBefore, stakeQuote.outAmount, sleep) : undefined;
    if (eth.brought === 0n || stake?.brought === 0n) {
      const holds = `${formatEther(eth.held)} ETH${stake ? ` and ${formatEther(stake.held)} of the stake token` : ""}`;
      const had = `${formatEther(ethBefore)} ETH${stake ? ` and ${formatEther(stakeBefore)}` : ""}`;
      throw new Error(`Relay reports the move settled, but the wallet on Robinhood Chain shows no increase, so what this run brought cannot be told from what it held. It holds ${holds}, and held ${had} before. Nothing was bridged.`);
    }
    // The stake goes first: its deposit pays for its arrival in ETH on the parent chain, out of what the ETH bridge would take.
    if (stake) {
      await options.bridgeOn("stake", stake.brought);
      onParent.delete("stake");
    }
    const left = await options.parentEth();
    const spent = eth.held > left ? eth.held - left : 0n;
    const ours = eth.brought > spent ? eth.brought - spent : 0n;
    const room = left > PARENT_ETH_KEEP ? left - PARENT_ETH_KEEP : 0n;
    const onward = ours < room ? ours : room;
    if (onward === 0n) log("Not enough ETH to send on to BrainChain beyond what stays for gas on Robinhood Chain.");
    else await options.bridgeOn("eth", onward);
  } catch (error) {
    const moved = [...onParent.values()].join(" and ");
    if (!moved) throw new Error(reason(error));
    throw new Error(`${reason(error).replace(/\.?$/, ".")} This run already brought ${moved} to ${options.worker} on Robinhood Chain; \`brainchain-worker bridge\` moves that on to BrainChain, and running fund again moves more USDC.`);
  }
  log("Done. `brainchain-worker status` shows the balances on BrainChain once the deposits arrive, in about a minute.");
}
