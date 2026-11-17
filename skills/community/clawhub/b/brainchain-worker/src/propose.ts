import {
  BaseError,
  createPublicClient,
  createWalletClient,
  decodeErrorResult,
  decodeFunctionData,
  encodeFunctionData,
  ExecutionRevertedError,
  getAddress,
  isAddress,
  isHex,
  parseAbi,
  parseEventLogs,
  size,
  type Abi,
  type AbiParameter,
  type Address,
  type Hex,
  type PrivateKeyAccount,
} from "viem";

import { erc20Errors, transferErrors } from "./abi.js";
import { bondsAbi, brainchainTransport, callVetoed, erc20Abi, executorAbi, openProposalOf, RECEIPT_MS } from "./chain.js";
import { chainOf, type Network } from "./network.js";
import { gasHelp, stake, when } from "./standing.js";

/** Every call the executor can be asked to make, by the contract it calls. */
export const GOVERNED = {
  board: parseAbi([
    "struct Config { uint16 hireThresholdBps; uint16 gradeThresholdBps; uint16 ruleThresholdBps; uint64 minDuration; uint64 maxDuration; uint64 gradeWindow; uint64 disputeWindow; uint64 ruleWindow; uint128 minBounty; }",
    "function setConfig(Config config)",
    "struct AppealConfig { uint64 window; uint16 bondBps; }",
    "function setAppealConfig(AppealConfig config)",
    "function setFee(uint16 feeBps, address feeRouter)",
    "function setPaused(bool paused)",
    "function setWorkerAllowed(address account, bool allowed)",
  ]),
  executor: parseAbi([
    "function setParameters(uint16 changeThresholdBps, uint64 timelock, uint32 houseTasksPerDay, uint128 maxHouseBounty, uint128 houseSpendPerDay)",
    "function transfer(address to, uint256 amount)",
  ]),
  registry: parseAbi(["function setModel(bytes32 id, address account, uint128 price, bool active)"]),
} as const satisfies Record<string, Abi>;

export type Target = keyof typeof GOVERNED;
const TARGETS = Object.keys(GOVERNED) as Target[];

/** What the brain reads from a proposal's URI, cut to the lengths it keeps, in UTF-16 units as a JavaScript string counts them. */
export const LIMITS = { title: 120, rationale: 1_500, current: 300, proposed: 300 } as const;
/** The most the brain reads of a whole case as JSON; past it, the case reads as blank and Jev decides on the call alone. */
export const CASE_BYTES = 4_096;

const proposalsAbi = parseAbi([
  "event Expired(uint256 indexed id)",
  "function decideWithin() view returns (uint64)",
]);
const executorReadsAbi = parseAbi(["function changeThresholdBps() view returns (uint16)"]);

// The reverts a governed call can hit, so a rehearsal names the rule it broke.
const callErrorsAbi = [
  ...parseAbi(["error BadConfig()", "error BadFee()", "error ZeroAddress()", "error NotOwner()", "error NotSelf()", "error NotGuardian()", "error AccountShapedId()", "error UnknownModel()"]),
  ...erc20Errors,
  ...transferErrors,
] as const;

/** Mirrors ProposalBonds.State. */
const State = { None: 0, Open: 1, Returned: 2, Burned: 3 } as const;

export class ProposalError extends Error {}

export interface Call {
  target: Target;
  address: Address;
  data: Hex;
  /** The call as a person reads it, such as setFee(300, 0x…). */
  text: string;
}

function functions(target: Target): string[] {
  return GOVERNED[target].filter((item) => item.type === "function").map((item) => item.name);
}

/** A JSON value as the ABI parameter it is passed for: integers become bigints, tuples objects. */
export function coerce(param: AbiParameter, value: unknown): unknown {
  const name = param.name ?? param.type;
  const fail = (expected: string) => new ProposalError(`${name} must be ${expected}, not ${JSON.stringify(value)}`);
  if (/^u?int\d*$/.test(param.type)) {
    const signed = param.type.startsWith("int");
    if (typeof value === "number" && Number.isSafeInteger(value)) return BigInt(value);
    if (typeof value === "string" && (signed ? /^-?\d+$/ : /^\d+$/).test(value)) return BigInt(value);
    throw fail(`a whole number${signed ? "" : " from 0"}, as a JSON number or a string of digits`);
  }
  if (param.type === "bool") {
    if (typeof value === "boolean") return value;
    throw fail("true or false");
  }
  if (param.type === "address") {
    if (typeof value === "string" && isAddress(value, { strict: false })) return getAddress(value);
    throw fail("an address");
  }
  const bytes = /^bytes(\d+)$/.exec(param.type);
  if (bytes) {
    if (typeof value === "string" && isHex(value) && size(value) === Number(bytes[1])) return value.toLowerCase();
    throw fail(`${bytes[1]} bytes of hex`);
  }
  if (param.type === "tuple" && "components" in param) {
    const parts = param.components;
    if (Array.isArray(value) && value.length === parts.length) {
      return Object.fromEntries(parts.map((part, i) => [part.name, coerce(part, value[i])]));
    }
    if (typeof value === "object" && value !== null && !Array.isArray(value)) {
      const given = value as Record<string, unknown>;
      const extra = Object.keys(given).filter((key) => !parts.some((part) => part.name === key));
      if (extra.length > 0) throw new ProposalError(`${name} has no field ${extra[0]}; its fields are ${parts.map((p) => p.name).join(", ")}`);
      return Object.fromEntries(
        parts.map((part) => {
          if (!(part.name! in given)) throw new ProposalError(`${name} is missing ${part.name}; give every field: ${parts.map((p) => p.name).join(", ")}`);
          return [part.name, coerce(part, given[part.name!])];
        }),
      );
    }
    throw fail(`an object with ${parts.map((p) => p.name).join(", ")}`);
  }
  throw fail(param.type);
}

const show = (value: unknown): string => {
  if (typeof value === "bigint") return value.toString();
  if (Array.isArray(value)) return `(${value.map(show).join(", ")})`;
  if (typeof value === "object" && value !== null) return `{${Object.entries(value).map(([k, v]) => `${k}: ${show(v)}`).join(", ")}}`;
  return String(value);
};

function resolveTarget(network: Network, target: string): { target: Target; address: Address } {
  const addresses: Record<Target, Address> = { board: network.contracts.taskBoard, executor: network.contracts.executor, registry: network.contracts.registry };
  const named = TARGETS.find((t) => t === target || addresses[t].toLowerCase() === target.toLowerCase());
  if (!named) throw new ProposalError(`--target is board, executor or registry, not "${target}"`);
  return { target: named, address: addresses[named] };
}

/**
 * The call a proposal asks the executor to make, from --call and --args or
 * from raw --data, refused here when the executor would refuse it anyway.
 */
export function buildCall(network: Network, proposer: Address, input: { target: string; call?: string; args?: string; data?: string }): Call {
  const { target, address } = resolveTarget(network, input.target);
  const abi = GOVERNED[target] as Abi;
  const offered = `The ${target} takes ${functions(target).join(", ")}`;
  let data: Hex;
  if (input.data !== undefined) {
    if (input.call !== undefined || input.args !== undefined) throw new ProposalError("Give either --data or --call with --args, not both");
    if (!isHex(input.data) || input.data.length < 10) throw new ProposalError("--data must be the call's hex calldata, starting 0x");
    data = input.data.toLowerCase() as Hex;
  } else {
    if (!input.call) throw new ProposalError(`--call is required: the function to call. ${offered}.`);
    const fn = abi.find((item) => item.type === "function" && item.name === input.call);
    if (!fn || fn.type !== "function") throw new ProposalError(`${offered}, not ${input.call}. setGuardian and setOwner are never queued.`);
    let args: unknown;
    try {
      args = JSON.parse(input.args ?? "[]");
    } catch {
      throw new ProposalError(`--args must be a JSON array, such as '[300, "0x…"]'`);
    }
    if (!Array.isArray(args) || args.length !== fn.inputs.length) {
      throw new ProposalError(`${fn.name} takes ${fn.inputs.length} argument${fn.inputs.length === 1 ? "" : "s"} (${fn.inputs.map((p) => p.name).join(", ")}), given as a JSON array in --args`);
    }
    data = encodeFunctionData({ abi, functionName: fn.name, args: fn.inputs.map((param, i) => coerce(param, args[i])) });
  }
  let decoded: { functionName: string; args?: readonly unknown[] };
  try {
    decoded = decodeFunctionData({ abi, data });
  } catch {
    throw new ProposalError(`${offered}; the selector ${data.slice(0, 10)} is none of them`);
  }
  if (encodeFunctionData({ abi, functionName: decoded.functionName, args: decoded.args } as never).toLowerCase() !== data) {
    throw new ProposalError("--data has bytes beyond the call's arguments");
  }
  const args = decoded.args ?? [];
  if (target === "board" && decoded.functionName === "setWorkerAllowed" && args[1] === true && String(args[0]).toLowerCase() === proposer.toLowerCase()) {
    throw new ProposalError("Allowing your own wallet to work is an application: run join, which stakes and applies in one go");
  }
  return { target, address, data, text: `${decoded.functionName}(${args.map(show).join(", ")})` };
}

export interface Case {
  title: string;
  rationale: string;
  current?: string;
  proposed?: string;
}

/** The proposal's URI: base64 JSON the brain shows Jev as the proposer's case. */
export function caseURI(call: Call, input: Case): string {
  const title = input.title.trim();
  const rationale = input.rationale.trim();
  if (!title) throw new ProposalError(`--title is required, up to ${LIMITS.title} characters`);
  if (!rationale) throw new ProposalError(`--rationale is required: why the change is better, up to ${LIMITS.rationale} characters. Jev reads it to decide.`);
  const body = { title, rationale, current: input.current?.trim() ?? "", proposed: input.proposed?.trim() || call.text };
  for (const key of Object.keys(LIMITS) as (keyof typeof LIMITS)[]) {
    if (body[key].length > LIMITS[key]) throw new ProposalError(`--${key} is at most ${LIMITS[key]} characters`);
  }
  const json = Buffer.from(JSON.stringify(body));
  if (json.byteLength > CASE_BYTES) throw new ProposalError(`The case is ${json.byteLength} bytes as JSON, and Jev reads at most ${CASE_BYTES}, which text outside the Latin alphabet reaches before the character limits. Shorten it.`);
  return `data:application/json;base64,${json.toString("base64")}`;
}

export interface Proposal {
  id: bigint;
  proposer: Address;
  bond: bigint;
  createdAt: bigint;
  state: number;
  /** When Jev's window closes, fixed when the call was proposed. */
  deadline: bigint;
}

/** What propose and proposal need from BrainChain. */
export interface ProposalChain {
  account: Address;
  now(): Promise<bigint>;
  ethBalance(): Promise<bigint>;
  /** How many transactions the wallet has sent. */
  sent(): Promise<number>;
  stakeBalance(): Promise<bigint>;
  bond(): Promise<bigint>;
  decideWithin(): Promise<bigint>;
  changeThresholdBps(): Promise<bigint>;
  timelock(): Promise<bigint>;
  vetoed(call: Call): Promise<boolean>;
  /** The open proposal for this exact call, from any wallet, or 0n. */
  openProposal(call: Call): Promise<bigint>;
  /** The revert the call would hit if the executor made it now, or undefined when it would succeed. */
  rehearse(call: Call): Promise<string | undefined>;
  /** Approves the bond if needed, proposes, waits for the receipt and returns the proposal's id. */
  propose(call: Call, uri: string, bond: bigint): Promise<{ id: bigint; tx: Hex }>;
  get(id: bigint): Promise<Proposal>;
  /** How an open proposal ended: the decision it was settled on, or expiry. */
  outcome(id: bigint): Promise<{ decisionId: bigint; adopted: boolean } | "expired" | undefined>;
  /** The change a decision queued, if it queued one. */
  queued(decisionId: bigint): Promise<{ changeId: bigint; eta: bigint; executed: boolean; vetoed: boolean } | undefined>;
}

const LOG_RANGE = 50_000n;

export function createProposals(network: Network, account: PrivateKeyAccount): ProposalChain {
  const chain = chainOf(network);
  const transport = brainchainTransport(network);
  const client = createPublicClient({ chain, transport, pollingInterval: 1_000 });
  const wallet = createWalletClient({ account, chain, transport });
  const { bonds, executor, stakeToken } = network.contracts;
  const proposals = { address: bonds, abi: [...bondsAbi, ...proposalsAbi] } as const;

  async function scan<T>(fetch: (fromBlock: bigint, toBlock: bigint) => Promise<T[]>): Promise<T[]> {
    const to = await client.getBlockNumber();
    const all: T[] = [];
    for (let start = network.fromBlock; start <= to; start += LOG_RANGE) {
      all.push(...(await fetch(start, start + LOG_RANGE - 1n < to ? start + LOG_RANGE - 1n : to)));
    }
    return all;
  }

  async function send(request: Parameters<typeof wallet.writeContract>[0]) {
    const hash = await wallet.writeContract(request);
    const receipt = await client.waitForTransactionReceipt({ hash, timeout: RECEIPT_MS });
    if (receipt.status !== "success") throw new Error(`Transaction ${hash} reverted`);
    return receipt;
  }

  return {
    account: account.address,
    now: async () => (await client.getBlock()).timestamp,
    ethBalance: () => client.getBalance({ address: account.address }),
    sent: () => client.getTransactionCount({ address: account.address }),
    stakeBalance: () => client.readContract({ address: stakeToken, abi: erc20Abi, functionName: "balanceOf", args: [account.address] }),
    bond: () => client.readContract({ ...proposals, functionName: "bond" }),
    decideWithin: () => client.readContract({ ...proposals, functionName: "decideWithin" }),
    changeThresholdBps: async () => BigInt(await client.readContract({ address: executor, abi: executorReadsAbi, functionName: "changeThresholdBps" })),
    timelock: () => client.readContract({ address: executor, abi: executorAbi, functionName: "timelock" }),
    vetoed: (call) => callVetoed(client, executor, call.address, call.data),
    openProposal: (call) => openProposalOf(client, network, call.address, call.data),
    async rehearse(call) {
      try {
        await client.call({ account: executor, to: call.address, data: call.data });
        return undefined;
      } catch (error) {
        // Only a revert says the call would fail; an RPC that cannot be reached is a failure of its own.
        const reverted = error instanceof BaseError ? error.walk((e) => e instanceof ExecutionRevertedError) : null;
        if (!(error instanceof BaseError) || !reverted) throw error;
        const raw = error.walk((e) => typeof (e as { data?: unknown }).data === "string") as { data?: Hex } | null;
        try {
          if (raw?.data) {
            const decoded = decodeErrorResult({ abi: callErrorsAbi, data: raw.data });
            // A plain Solidity revert carries its reason as text, and its error's name says nothing.
            if ((decoded.errorName as string) === "Error") return String(decoded.args?.[0]);
            return `${decoded.errorName}, the contract's check on these values`;
          }
        } catch {
          // Not one of the contracts' own errors; the node's message says more.
        }
        return error.shortMessage;
      }
    },
    async propose(call, uri, bond) {
      const allowance = await client.readContract({ address: stakeToken, abi: erc20Abi, functionName: "allowance", args: [account.address, bonds] });
      if (allowance < bond) await send({ address: stakeToken, abi: erc20Abi, functionName: "approve", args: [bonds, bond] });
      const receipt = await send({ ...proposals, functionName: "propose", args: [call.address, call.data, uri] });
      const [log] = parseEventLogs({ abi: bondsAbi, eventName: "Proposed", logs: receipt.logs }).filter((l) => l.address.toLowerCase() === bonds.toLowerCase());
      if (!log) throw new Error(`The proposal landed in ${receipt.transactionHash} but logged no id`);
      return { id: log.args.id, tx: receipt.transactionHash };
    },
    async get(id) {
      const p = await client.readContract({ ...proposals, functionName: "get", args: [id] });
      return { id, proposer: p.proposer, bond: p.bond, createdAt: p.createdAt, state: p.state, deadline: p.deadline };
    },
    async outcome(id) {
      const [settled, expired] = await Promise.all([
        scan((fromBlock, toBlock) => client.getContractEvents({ ...proposals, eventName: "Settled", args: { id }, fromBlock, toBlock })),
        scan((fromBlock, toBlock) => client.getContractEvents({ ...proposals, eventName: "Expired", args: { id }, fromBlock, toBlock })),
      ]);
      if (settled[0]) return { decisionId: settled[0].args.decisionId!, adopted: settled[0].args.adopted! };
      return expired[0] ? "expired" : undefined;
    },
    async queued(decisionId) {
      const [log] = await scan((fromBlock, toBlock) => client.getContractEvents({ address: executor, abi: executorAbi, eventName: "Queued", args: { decisionId }, fromBlock, toBlock }));
      if (!log) return undefined;
      const change = await client.readContract({ address: executor, abi: executorAbi, functionName: "getChange", args: [log.args.changeId!] });
      return { changeId: log.args.changeId!, eta: change.eta, executed: change.executed, vetoed: change.vetoed };
    },
  };
}

const hours = (seconds: bigint) => `${Number(seconds) / 3600} hours`;
const days = (seconds: bigint) => `${Number(seconds) / 86_400} days`;
const percent = (bps: bigint) => `${Number(bps) / 100}%`;

export async function propose(
  network: Network,
  chain: ProposalChain,
  call: Call,
  uri: string,
  options: { dry: boolean; log: (line: string) => void },
): Promise<void> {
  const { log } = options;
  const [bond, balance, gas, within, threshold, timelock, vetoed, open, revert] = await Promise.all([
    chain.bond(),
    chain.stakeBalance(),
    chain.ethBalance(),
    chain.decideWithin(),
    chain.changeThresholdBps(),
    chain.timelock(),
    chain.vetoed(call),
    chain.openProposal(call),
    chain.rehearse(call),
  ]);
  if (vetoed) throw new ProposalError(`The guardian vetoed ${call.text} on the ${call.target}, so the executor does not queue it until the admin reopens that function`);
  if (open > 0n) throw new ProposalError(`Proposal ${open} already asks for ${call.text} on the ${call.target} and is still open, and the contract takes one at a time. Follow it with \`npx brainchain-worker proposal ${open}\`.`);
  if (revert) throw new ProposalError(`${call.text} would fail if the executor made it now (${revert}), so the bond would be burned for nothing`);
  log(`Proposal on ${network.name}
  Call      ${call.text} on the ${call.target} (${call.address})
  Data      ${call.data}
  Bond      ${stake(network, bond)}, returned if Jev adopts the change with at least ${percent(threshold)} confidence, burned otherwise
  Decision  within ${days(within)}; an adopted change runs ${hours(timelock)} later`);
  if (options.dry) {
    log("Dry run, nothing sent.");
    return;
  }
  if (balance < bond) {
    const buy = network.buyStake ? ` ${network.buyStake}` : "";
    throw new Error(`The wallet holds ${stake(network, balance)} of the ${stake(network, bond)} bond.${buy}`);
  }
  if (gas === 0n) throw new Error(`${chain.account} has no ETH on ${network.name} for gas. ${gasHelp(network, chain.account, 0n, await chain.sent())}.`);
  log(`Bonding ${stake(network, bond)} and proposing...`);
  const { id, tx } = await chain.propose(call, uri, bond);
  log(`Proposal ${id} is waiting for Jev (${tx}). Follow it with \`npx brainchain-worker proposal ${id}\`.`);
}

export async function proposal(network: Network, chain: ProposalChain, id: bigint, log: (line: string) => void): Promise<void> {
  const p = await chain.get(id);
  if (p.state === State.None) throw new ProposalError(`There is no proposal ${id} on ${network.name}`);
  const head = `Proposal ${id} by ${p.proposer}, bond ${stake(network, p.bond)}`;
  if (p.state === State.Open) {
    const now = await chain.now();
    const after = now > p.deadline ? `its window closed at ${when(p.deadline)}, so anyone can return the bond by calling expire on ${network.contracts.bonds}` : `Jev decides by ${when(p.deadline)}`;
    log(`${head}\n  Waiting for Jev: ${after}.`);
    return;
  }
  const outcome = await chain.outcome(id);
  if (outcome === "expired") {
    log(`${head}\n  Not decided in its window; the bond was returned.`);
    return;
  }
  if (outcome === undefined) {
    log(`${head}\n  ${p.state === State.Returned ? "Settled, bond returned" : "Settled, bond burned"}.`);
    return;
  }
  if (!outcome.adopted) {
    log(`${head}\n  Jev kept the current setting (decision ${outcome.decisionId}); the bond was burned.`);
    return;
  }
  const change = await chain.queued(outcome.decisionId);
  const state = !change
    ? "not queued yet"
    : change.executed
      ? `change ${change.changeId} has run`
      : change.vetoed
        ? `change ${change.changeId} was vetoed by the guardian`
        : `change ${change.changeId} runs from ${when(change.eta)}`;
  log(`${head}\n  Jev adopted it (decision ${outcome.decisionId}) and the bond was returned; ${state}.`);
}
