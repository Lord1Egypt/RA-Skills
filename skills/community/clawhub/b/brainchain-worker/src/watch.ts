import type { DecisionReport } from "brainchain-verify";
import { concat, createPublicClient, createWalletClient, keccak256, parseAbi, toBytes, type Address, type Hex, type PrivateKeyAccount } from "viem";

import { brainchainTransport, executorAbi, reason } from "./chain.js";
import { chainOf, type Network } from "./network.js";

/**
 * The calls the constitution's monitor knows, by the function a change calls.
 * A change that crosses a floor is what the guardian's veto is for, and any
 * other call counts as crossing one. Three known calls have no floor, and say
 * what they do instead. Values in the units the contracts take: basis points,
 * seconds, and USDG in 6 decimals.
 */
export const FLOORS: Record<string, { name: string; check: (args: readonly bigint[]) => string[]; does?: string }> = {
  "0x85327a44": {
    name: "setParameters",
    check: (w) =>
      [
        w[0]! < 6_000n && "the change bar falls below 60%",
        w[1]! < 86_400n && "the timelock falls below 24 hours",
        w[2]! > 20n && "more than 20 house tasks a day",
        w[3]! > 10_000_000n && "a house bounty above 10 USDG",
        w[4]! > 50_000_000n && "house spend above 50 USDG a day",
      ].filter((r): r is string => typeof r === "string"),
  },
  "0x00dd15f5": {
    name: "setConfig",
    check: (w) =>
      [
        w[0]! < 1_000n && "the hire bar falls below 10%",
        w[1]! < 6_000n && "the grade bar falls below 60%",
        w[2]! < 6_000n && "the ruling bar falls below 60%",
        (w[5]! < 3_600n || w[6]! < 3_600n || w[7]! < 3_600n) && "a grading, dispute or ruling window under an hour",
        w[8]! < 100_000n && "a minimum bounty under 0.1 USDG",
      ].filter((r): r is string => typeof r === "string"),
  },
  "0x30f738be": { name: "setFee", check: (w) => (w[0]! > 500n ? ["a protocol fee above 5%"] : []) },
  "0x731022ff": {
    name: "setModel",
    check: (w) =>
      [w[1]! === 0n && "a house model with no account", w[2]! > 5_000_000n && "a house model priced above 5 USDG"].filter(
        (r): r is string => typeof r === "string",
      ),
  },
  "0x16c38b3c": { name: "setPaused", check: () => [], does: "pauses or resumes new posts" },
  "0x1f1e4d9f": { name: "setWorkerAllowed", check: () => [], does: "allows or removes a worker" },
  "0xa9059cbb": { name: "transfer", check: () => [], does: "moves house treasury funds" },
};

/** The static words after the selector; a call with dynamic arguments is read as far as its words go. */
export function argumentsOf(data: Hex): readonly bigint[] {
  const body = data.slice(10);
  const words: bigint[] = [];
  for (let i = 0; i + 64 <= body.length; i += 64) words.push(BigInt(`0x${body.slice(i, i + 64)}`));
  return words;
}

/** What a queued change does to the constitution: nothing, the floors it crosses, or, for a known call with no floor, what it does. */
export function judge(data: Hex): { name: string; broken: string[]; does?: string } {
  const selector = data.slice(0, 10).toLowerCase();
  const floor = FLOORS[selector];
  if (!floor) return { name: selector, broken: ["a call the monitor does not know, which counts as breaking a floor"] };
  return { name: floor.name, broken: floor.check(argumentsOf(data)), ...(floor.does ? { does: floor.does } : {}) };
}

export interface QueuedChange {
  changeId: bigint;
  decisionId: bigint;
  target: Address;
  data: Hex;
  eta: bigint;
  block: bigint;
}

export interface WatchChain {
  account: Address;
  head(): Promise<bigint>;
  queued(fromBlock: bigint, toBlock: bigint): Promise<QueuedChange[]>;
  /** Whether a change still waits to run. */
  open(changeId: bigint): Promise<boolean>;
  /** How many decisions the log holds. */
  decisions(): Promise<bigint>;
  /** The account the guardian gate takes vetoes from; absent where the network has no gate. */
  watcher?(): Promise<Address>;
  /** Vetoes through the guardian gate; absent where the network has no gate or the worker holds no watcher key. */
  veto?(changeId: bigint, reason: string): Promise<Hex>;
}

const gateAbi = parseAbi(["function veto(uint256 changeId, string reason)", "function watcher() view returns (address)"]);
const logAbi = parseAbi(["function count() view returns (uint256)"]);

export function createWatchChain(network: Network, account: PrivateKeyAccount): WatchChain {
  const transport = brainchainTransport(network);
  const client = createPublicClient({ chain: chainOf(network), transport, pollingInterval: 1_000 });
  const wallet = createWalletClient({ account, chain: chainOf(network), transport });
  const executor = network.contracts.executor;
  const gate = network.contracts.gate;
  return {
    account: account.address,
    head: () => client.getBlockNumber(),
    async queued(fromBlock, toBlock) {
      const logs = await client.getContractEvents({ address: executor, abi: executorAbi, eventName: "Queued", fromBlock, toBlock });
      return logs.map((log) => ({
        changeId: log.args.changeId!,
        decisionId: log.args.decisionId!,
        target: log.args.target!,
        data: log.args.data!,
        eta: log.args.eta!,
        block: log.blockNumber,
      }));
    },
    async open(changeId) {
      const change = await client.readContract({ address: executor, abi: executorAbi, functionName: "getChange", args: [changeId] });
      return !change.executed && !change.vetoed;
    },
    decisions: () => client.readContract({ address: network.contracts.log, abi: logAbi, functionName: "count" }),
    ...(gate
      ? {
          watcher: () => client.readContract({ address: gate, abi: gateAbi, functionName: "watcher" }),
          async veto(changeId: bigint, why: string) {
            const watcher = await client.readContract({ address: gate, abi: gateAbi, functionName: "watcher" });
            if (watcher.toLowerCase() !== account.address.toLowerCase()) throw new Error(`the gate's watcher is ${watcher}, not this worker`);
            const hash = await wallet.writeContract({ address: gate, abi: gateAbi, functionName: "veto", args: [changeId, why] });
            await client.waitForTransactionReceipt({ hash });
            return hash;
          },
        }
      : {}),
  };
}

/**
 * Refuses a --veto run whose key is not the gate's watcher, which otherwise
 * shows only when a veto is due. A read that fails does not stop the watch: a
 * round outlasts a bad RPC, and each veto reads the watcher again.
 */
export async function requireWatcher(chain: WatchChain, log: (line: string) => void): Promise<void> {
  const watcher = await chain.watcher?.().catch((error: unknown) => {
    log(`could not read the gate's watcher (${reason(error)}); it is read again before any veto`);
    return undefined;
  });
  if (watcher !== undefined && watcher.toLowerCase() !== chain.account.toLowerCase()) {
    throw new Error(`This key cannot veto: the gate's watcher is ${watcher}, not ${chain.account}. Set BRAINCHAIN_WORKER_KEY to the watcher's key, or run watch without --veto.`);
  }
}

/**
 * Re-checks one decision against the chain and the published record; the
 * findings are what disagreed. A decision that verified comes with the record's
 * bytes as served, when the worker reports its rounds. It throws when the
 * decision cannot be checked yet, and the round stops there.
 */
export type Verify = (id: bigint) => Promise<{ findings: string[]; record?: Uint8Array; withheld?: string[] }>;

/** How long after a decision was recorded a record that cannot be read may hold a round's place. */
export const UNREADABLE_MS = 86_400_000;

/**
 * A record that cannot be read stops the round and holds its place, so a host's
 * outage costs no check. Only for a day from the decision's block time: one dead
 * address would otherwise blind a watcher to every decision after it, so past
 * that it is a finding, reported once, and the round moves on.
 */
function unreadable(why: string, recordedAt: string | undefined, now: number): { findings: string[] } {
  if (recordedAt === undefined || !(now - Date.parse(recordedAt) >= UNREADABLE_MS)) throw new Error(why);
  return { findings: [`the record could not be read a day or more after it was recorded: ${why}`] };
}

/**
 * What one decision's checks come to. A check that failed is a finding, whatever
 * else could not be read. A check that could not run says nothing about the
 * decision, so it follows the rule for an unreadable record. A record served
 * without its work leaves its hash checks unrun, which is neither a finding nor a
 * verified decision: `withheld` names them. With `refetch`, a verified decision
 * comes with the record's bytes as served, for the report, and a failure to fetch
 * them follows the same rule.
 */
export async function outcome(
  report: Pick<DecisionReport, "checks" | "withheld" | "recordedAt" | "payloadURI">,
  options: { refetch?: (uri: string) => Promise<Uint8Array>; now?: number } = {},
): Promise<Awaited<ReturnType<Verify>>> {
  const now = options.now ?? Date.now();
  const said = (status: string) => report.checks.filter((c) => c.status === status).map((c) => `${c.name}: ${c.message}`);
  const findings = said("fail");
  if (findings.length > 0) return { findings };
  const unread = said("error");
  if (unread.length > 0) return unreadable(unread.join("; "), report.recordedAt, now);
  if (report.withheld) return { findings, withheld: report.checks.filter((c) => c.status === "skip" && c.name.endsWith("-hash")).map((c) => c.name) };
  if (!options.refetch || !report.payloadURI) return { findings };
  try {
    return { findings, record: await options.refetch(report.payloadURI) };
  } catch (error) {
    return unreadable(reason(error), report.recordedAt, now);
  }
}

/** The service's prefix on a report; the worker signs the prefix and the report's JSON text. */
export const REPORT_PREFIX = "BrainChain watchtower report\n";
/** A report lists at most this many decisions checked and this many findings; a longer round sends several. */
export const MAX_CHECKED = 200;
export const MAX_FINDINGS = 50;

/** The proof a record was fetched: the hash of its bytes followed by the worker's address, which nothing on chain gives away. */
export const fetchProof = (bytes: Uint8Array, worker: Address): Hex => keccak256(concat([bytes, toBytes(worker)]));

export type Report = (checked: { id: bigint; proof: Hex }[], findings: { id: bigint; checks: string[] }[]) => Promise<string>;

/** The service answered and will not take this report, so sending it again would not help. */
export class ReportRefused extends Error {}

/**
 * Sends a round's re-verified decisions to the service, signed by the worker,
 * so a staked worker's watchtower counts toward its mark in hire questions.
 * Resolves to the line to log.
 */
export function createReporter(network: Network, account: PrivateKeyAccount, fetcher: typeof fetch = fetch): Report {
  // The service takes a report only if it was signed later than the last it took, by the second.
  let lastAt = 0;

  async function send(checked: Parameters<Report>[0], findings: Parameters<Report>[1]): Promise<string> {
    lastAt = Math.max(Math.floor(Date.now() / 1000), lastAt + 1);
    const report = {
      worker: account.address,
      chainId: network.chainId,
      log: network.contracts.log,
      at: lastAt,
      checked: checked.map((c) => ({ id: Number(c.id), proof: c.proof })),
      findings: findings.map((f) => ({ id: Number(f.id), checks: f.checks.slice(0, 20).map((c) => c.slice(0, 400)) })),
    };
    const text = JSON.stringify(report);
    const signature = await account.signMessage({ message: `${REPORT_PREFIX}${text}` });
    const response = await fetcher(`${network.service}/watchtowers/reports`, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ report: text, signature }),
      signal: AbortSignal.timeout(20_000),
    });
    const body = (await response.json().catch(() => ({}))) as { error?: string; checked?: number; mark?: { since: string } | null; markAfter?: number };
    if (response.status >= 400 && response.status < 500) throw new ReportRefused(body.error ?? `${response.status} from ${network.service}`);
    if (!response.ok) throw new Error(body.error ?? `${response.status} from ${network.service}`);
    return body.mark
      ? `reported to ${network.name}: ${body.checked} decisions re-verified in all, watchtower mark since ${body.mark.since}`
      : `reported to ${network.name}: ${body.checked} of the ${body.markAfter} re-verified decisions that earn the watchtower mark`;
  }

  return async (checked, findings) => {
    let line = await send(checked.slice(0, MAX_CHECKED), findings.slice(0, MAX_FINDINGS));
    for (let i = 1; MAX_CHECKED * i < checked.length || MAX_FINDINGS * i < findings.length; i++) {
      line = await send(checked.slice(MAX_CHECKED * i, MAX_CHECKED * (i + 1)), findings.slice(MAX_FINDINGS * i, MAX_FINDINGS * (i + 1)));
    }
    return line;
  };
}

/**
 * Watches the chain for the worker: every queued change is judged against the
 * constitution and, with `veto` on, one that crosses a floor is vetoed through
 * the guardian gate; every new decision is re-verified. Each round reports
 * what it found and keeps where it got to.
 */
export function createWatch(options: {
  network: Network;
  chain: WatchChain;
  verify?: Verify;
  /** Sends each round's re-verified decisions and findings to the service, signed; absent when the worker has no key. */
  report?: Report;
  veto: boolean;
  log: (line: string) => void;
  /** Where the first round starts reading; later rounds continue from the last block seen. */
  fromBlock?: bigint;
  /** The log's count when an earlier run stopped, so decisions added since are checked. */
  seenDecision?: bigint;
  /** With no count to pick up from, how many of the latest decisions the first round checks; without it, that round only notes where the log stands. */
  recent?: bigint;
  /** Told how far the checks have got after each round; it may throw, which costs only a repeat of those checks. */
  saw?: (count: bigint) => void;
}) {
  const { network, chain, verify, log } = options;
  let nextBlock = options.fromBlock ?? network.fromBlock;
  let seenDecision = options.seenDecision;
  const judged = new Set<string>();
  /** Vetoes due and not yet landed; each is tried every round until it lands or its change closes. */
  const owed = new Map<string, { id: bigint; why: string }>();
  let findings = 0;
  let incomplete = false;

  async function changes(): Promise<void> {
    const head = await chain.head();
    if (head < nextBlock) return;
    const span = 5_000n;
    for (let from = nextBlock; from <= head; from += span) {
      const to = from + span - 1n < head ? from + span - 1n : head;
      for (const change of await chain.queued(from, to)) {
        const key = change.changeId.toString();
        if (judged.has(key)) continue;
        const { name, broken, does } = judge(change.data);
        // A failed read leaves the change unjudged and the block range unread, so the next round comes back to it.
        const open = await chain.open(change.changeId);
        judged.add(key);
        const why = broken.join("; ");
        if (!open) {
          log(`change ${change.changeId}: ${name} on ${change.target}${broken.length > 0 ? ` broke the constitution (${why})` : ""}; closed, it has run or was vetoed`);
          continue;
        }
        const runsAt = new Date(Number(change.eta) * 1000).toISOString().replace("T", " ").slice(0, 19);
        if (broken.length === 0) {
          log(`change ${change.changeId}: ${name} on ${change.target}${does ? ` ${does}, which no floor covers` : ", within the constitution"}, runs after ${runsAt} UTC`);
          continue;
        }
        findings += 1;
        log(`change ${change.changeId}: ${name} on ${change.target} breaks the constitution (${why}), runs after ${runsAt} UTC`);
        if (options.veto) owed.set(key, { id: change.changeId, why });
      }
    }
    nextBlock = head + 1n;
  }

  async function vetoes(): Promise<void> {
    for (const [key, { id, why }] of owed) {
      try {
        if (!(await chain.open(id))) {
          owed.delete(key);
          log(`change ${id} is closed already, nothing to veto`);
        } else if (!chain.veto) {
          owed.delete(key);
          log(`cannot veto: ${network.name} has no guardian gate this worker can reach`);
        } else {
          const hash = await chain.veto(id, `Breaks the constitution: ${why}`);
          owed.delete(key);
          log(`vetoed change ${id} through the guardian gate: ${hash}`);
        }
      } catch (error) {
        log(`veto of change ${id} failed, tried again next round: ${reason(error)}`);
      }
    }
  }

  async function decisions(): Promise<void> {
    if (!verify) return;
    const count = await chain.decisions();
    if (seenDecision === undefined && options.recent !== undefined) seenDecision = count > options.recent ? count - options.recent : 0n;
    // A log restarted under a new set of contracts has fewer decisions than the count kept from the old one.
    if (seenDecision !== undefined && seenDecision > count) seenDecision = options.recent === undefined ? undefined : count > options.recent ? count - options.recent : 0n;
    if (seenDecision === undefined) {
      seenDecision = count;
      log(`${count} decisions recorded so far; new ones are checked from here`);
      return;
    }
    const checked: { id: bigint; proof: Hex }[] = [];
    const found: { id: bigint; checks: string[] }[] = [];
    let reached = seenDecision;
    for (let id = seenDecision + 1n; id <= count; id++) {
      try {
        const { findings: wrong, record, withheld } = await verify(id);
        if (withheld) {
          log(`decision ${id} withheld: its record is served without the work, so ${withheld.join(" and ")} did not run; the checks that ran agree with the chain`);
        } else if (wrong.length === 0) {
          log(`decision ${id} verified`);
          if (record) checked.push({ id, proof: fetchProof(record, chain.account) });
        } else {
          findings += 1;
          found.push({ id, checks: wrong });
          log(`decision ${id} does not verify: ${wrong.join("; ")}`);
        }
        reached = id;
      } catch (error) {
        // The place stays here, so this decision and the ones after it are checked next time.
        log(`decision ${id} could not be checked, so it is tried again next round: ${reason(error)}`.replace(/\s*\n\s*/g, " "));
        incomplete = true;
        break;
      }
    }
    // Before the place is saved, so a save that fails does not lose the round's work.
    if (options.report && (checked.length > 0 || found.length > 0)) {
      try {
        log(await options.report(checked, found));
      } catch (error) {
        log(`report not taken: ${reason(error)}`);
        incomplete = true;
        // Only an answer from the service settles a report: a refusal would only repeat, and these decisions are checked and sent again otherwise.
        if (!(error instanceof ReportRefused)) reached = seenDecision;
      }
    }
    seenDecision = reached;
    try {
      options.saw?.(reached);
    } catch (error) {
      log(`warning: could not save how far this got, so the next run checks these decisions again: ${reason(error)}`);
    }
  }

  return {
    async round(): Promise<{ findings: number; incomplete: boolean }> {
      incomplete = false;
      try {
        await changes();
      } finally {
        await vetoes();
      }
      await decisions();
      return { findings, incomplete };
    },
  };
}
