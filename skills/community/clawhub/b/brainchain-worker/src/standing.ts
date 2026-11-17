import { formatEther, formatUnits } from "viem";

import { ApplicationState, Status, type Chain, type Flight } from "./chain.js";
import type { Network } from "./network.js";

/** A token amount with thousands separators, such as 1,250,000; a fraction is kept as it is. */
export function grouped(amount: bigint, decimals: number): string {
  const [whole, fraction] = formatUnits(amount, decimals).split(".");
  return `${whole!.replace(/\B(?=(\d{3})+$)/g, ",")}${fraction === undefined ? "" : `.${fraction}`}`;
}

export const stake = (network: Network, amount: bigint) => `${grouped(amount, 18)} ${network.stakeSymbol}`;
export const usdg = (network: Network, amount: bigint) => `${formatUnits(amount, 6)} ${network.bountySymbol}`;
export const when = (seconds: bigint) => new Date(Number(seconds) * 1000).toISOString().replace(".000Z", "Z");

/** The worker's standing with the board and the staking contract, and what join would do about it. */
export async function snapshot(chain: Chain) {
  const [allowed, w, min, { applications, change }] = await Promise.all([chain.allowed(), chain.stake(), chain.minStake(), chain.applications()]);
  const pending = change !== undefined && !change.executed && !change.vetoed;
  const open = applications.find((a) => a.state === ApplicationState.Open);
  return {
    allowed,
    w,
    min,
    applications,
    change,
    pending,
    open,
    applying: !allowed && !pending && open === undefined,
    // Below the minimum after leave or a slash, an allowed worker cannot be hired until it stakes again.
    toStake: w.staked >= min ? 0n : min - w.staked,
  };
}

export type Snapshot = Awaited<ReturnType<typeof snapshot>>;

/** The highest gas limit seen for each transaction join can send, across testnet and mainnet. */
export const GAS = { faucet: 76_000n, approve: 50_000n, stake: 120_000n, setPrice: 31_000n, apply: 240_000n };
/** The highest gas limit seen for delivering a result. */
const SUBMIT_GAS = 104_000n;

/**
 * The ETH a wallet must hold for transactions with these gas limits to go
 * through in order. Each pays the going price, but the RPC refuses one the
 * wallet could not cover at 2.4 times it, the fee cap it fills in.
 */
export function ethNeeded(limits: bigint[], gasPrice: bigint): bigint {
  let spent = 0n;
  let need = 0n;
  for (const limit of limits) {
    const covered = spent + (limit * gasPrice * 24n) / 10n;
    if (covered > need) need = covered;
    spent += limit * gasPrice;
  }
  return need;
}

/** The gas limits of what join would send for this worker, in order. */
export function joinLimits(s: Snapshot, claims: boolean, reprices: boolean): bigint[] {
  return [
    ...(claims ? [GAS.faucet] : []),
    ...(s.toStake > 0n ? [GAS.approve, GAS.stake] : reprices ? [GAS.setPrice] : []),
    ...(s.applying ? [GAS.approve, GAS.apply] : []),
  ];
}

/** An amount of ETH rounded up to two significant figures. */
export function aboutEth(wei: bigint): string {
  const unit = 10n ** BigInt(Math.max(wei.toString().length - 2, 0));
  return formatEther(((wei + unit - 1n) / unit) * unit);
}

/** Why the worker can or cannot be hired right now, in one line for `run` or for `status`, which shows the rest itself. */
export function hireable({ allowed, w, min, applications, change, pending }: Snapshot, network: Network, from: "run" | "status"): string {
  if (allowed) {
    if (w.staked >= min) return "yes";
    return `no: your stake is below the minimum of ${stake(network, min)}. Run join to stake again${from === "run" ? "; status shows what it needs" : ""}.`;
  }
  // An allowed application waiting out its timelock outranks anything filed after it.
  if (change && pending) {
    const due = BigInt(Math.floor(Date.now() / 1000)) >= change.eta;
    const allowed = `no: Jev allowed this worker; ${due ? `the change that allows it was due at ${when(change.eta)} and has not run yet` : `it can be hired after ${when(change.eta)}`}`;
    return w.staked >= min ? allowed : `${allowed}. Its stake is below the minimum of ${stake(network, min)}, so run join to stake again first.`;
  }
  const last = applications.at(-1);
  if (last === undefined) return "no: run `npx brainchain-worker join` to apply";
  if (last.state === ApplicationState.Open) return `no: application ${last.id} is waiting for Jev`;
  if (last.state === ApplicationState.Burned) return `no: Jev did not allow application ${last.id}, and its bond was burned. Run join to apply again.`;
  if (change?.vetoed) {
    // A vetoed call can never be queued again, so the veto still stands for applications filed after it.
    const vetoed = applications.find((a) => a.decisionId === change.decisionId);
    return `no: the guardian vetoed ${vetoed ? `application ${vetoed.id}` : "allowing this worker"}`;
  }
  return `no: application ${last.id} closed without a decision; its bond was returned. Run join to apply again.`;
}

/**
 * The wallet's stake token and, below the minimum stake, where join would find
 * what it needs. A stake token without a faucet has no `faucet`; one that is
 * bought instead says where.
 */
export function wallet(
  network: Network,
  s: Snapshot,
  balance: bigint,
  bond: bigint,
  faucet: { amount: bigint; opensAt: bigint } | undefined,
  now: bigint,
): string {
  const has = stake(network, balance);
  if (s.toStake === 0n) return has;
  const need = s.toStake + (s.applying ? bond : 0n);
  if (balance >= need) return `${has}, enough for the ${stake(network, need)} join needs`;
  if (faucet && now >= faucet.opensAt) return `${has}; join needs ${stake(network, need)} and claims the rest from the faucet, which gives ${stake(network, faucet.amount)} a day`;
  const reopens = faucet ? `. The faucet opens again for this wallet at ${when(faucet.opensAt)}` : "";
  const unstaking =
    s.w.unstaking > 0n ? `, and the ${stake(network, s.w.unstaking)} unstaking can be withdrawn ${now >= s.w.unlocksAt ? "now" : `after ${when(s.w.unlocksAt)}`}` : "";
  const buy = network.buyStake ? `. ${network.buyStake}` : "";
  return `${has}; join needs ${stake(network, need)}${reopens}${unstaking}${buy}`;
}

/**
 * Where a wallet gets ETH for gas, given what it holds and how many
 * transactions it has sent. The drip serves an address once and turns away one
 * that holds a drip's worth, so only a wallet that has sent nothing and holds
 * less is sure to get it; any other is sent to the faucet.
 */
export function gasHelp(network: Network, address: string, gas: bigint, sent: number): string {
  const { drip } = network;
  if (!drip) return network.gas;
  if (sent > 0 || gas >= drip.wei) return `${network.gas}. The gas drip serves each address once`;
  const after = `${network.gas[0]!.toLowerCase()}${network.gas.slice(1)}`;
  return `Ask the testnet gas drip first: ${drip.request(address)} sends ${formatEther(drip.wei)} ETH, enough to join, once per address. After that, ${after}`;
}

/** What a wallet short of gas holds and needs, for join's refusal and for `status`. */
export const shortOfGas = (network: Network, address: string, gas: bigint, sent: number, need: bigint, purpose: string) =>
  `${formatEther(gas)} ETH on ${network.name}; ${purpose} needs about ${aboutEth(need)} ETH for gas. ${gasHelp(network, address, gas, sent)}.`;

/** How many results the wallet's ETH delivers at this gas price, the last of them at the fee cap the RPC checks. */
export function deliveriesLeft(gas: bigint, gasPrice: bigint): bigint {
  const price = gasPrice > 0n ? gasPrice : 1n;
  const last = ethNeeded([SUBMIT_GAS], price);
  return gas < last ? 0n : (gas - last) / (SUBMIT_GAS * price) + 1n;
}

/** About how many results the wallet's ETH delivers, for `status` and `run`. */
export const deliveries = (count: bigint) => `about ${count} ${count === 1n ? "delivery" : "deliveries"}`;

/**
 * The wallet's ETH, and what more join or the next delivery needs, since a
 * send the wallet cannot cover fails partway through. A worker with nothing to
 * join hears how many results its ETH delivers.
 */
export function gasLine(network: Network, address: string, s: Snapshot, gas: bigint, gasPrice: bigint, claims: boolean, sent: number): string {
  const limits = joinLimits(s, claims, false);
  const need = ethNeeded(limits.length > 0 ? limits : [SUBMIT_GAS], gasPrice);
  if (gas < need) return shortOfGas(network, address, gas, sent, need, limits.length > 0 ? "join" : "delivering a result");
  return limits.length > 0 ? `${formatEther(gas)} ETH` : `${formatEther(gas)} ETH, enough for ${deliveries(deliveriesLeft(gas, gasPrice))} at the current gas price`;
}

/** What join says when the wallet holds too little of a stake token that has no faucet. */
export function shortOfStake(network: Network, w: Snapshot["w"], balance: bigint, need: bigint, now: bigint): string {
  const withdraw = now >= w.unlocksAt ? "now" : `after ${when(w.unlocksAt)}`;
  const unstaking = w.unstaking > 0n ? ` Or run withdraw ${withdraw} and join with the ${stake(network, w.unstaking)} it returns.` : "";
  return `The wallet holds ${stake(network, balance)} of the ${stake(network, need)} join needs. ${network.buyStake}${unstaking}`;
}

/** Where a task in flight stands and what happens next, for `status`. */
export function flightLine(f: Flight): string {
  const task = `task ${f.id}`;
  switch (f.status) {
    case Status.Hired:
      return `${task}: hired, due by ${when(f.deadline)}`;
    case Status.Submitted:
      return `${task}: delivered, waiting for Jev's grade`;
    case Status.Graded: {
      const closes = when(f.gradedAt + f.disputeWindow);
      return f.accepted
        ? `${task}: accepted, paid after ${closes} unless the grade is disputed`
        : `${task}: not accepted, refunded to the poster after ${closes} unless the grade is disputed with \`dispute ${f.id}\``;
    }
    case Status.Disputed:
      return `${task}: grade disputed by ${f.disputedByModel ? "this worker" : "the poster"}, Jev rules by ${when(f.disputedAt + f.ruleWindow)}`;
    case Status.Ruled: {
      const a = f.appeal!;
      const closes = when(a.ruledAt + a.window);
      return a.pays
        ? `${task}: the ruling pays this worker after ${closes} unless the poster appeals`
        : `${task}: the ruling refunds the poster after ${closes} unless appealed with \`appeal ${f.id}\``;
    }
    default:
      return `${task}: ruling appealed, Jev rules again by ${when(f.appeal!.appealedAt + f.ruleWindow)}`;
  }
}
