import { BaseError, ContractFunctionExecutionError, ContractFunctionRevertedError, encodeErrorResult, InsufficientFundsError, parseAbi, parseEther, parseGwei, type Address, type Hex } from "viem";
import { describe, expect, it, vi } from "vitest";

import { explainRevert, reason, Status } from "./chain.js";
import { appeal, Appealed, dispute, Ruled, type DisputeChain, type DisputeTask } from "./dispute.js";
import { MAINNET, TESTNET } from "./network.js";

const WORKER = "0x00000000000000000000000000000000000000c1" as Address;
const POSTER = "0x00000000000000000000000000000000000000a1" as Address;
const NOW = 1_800_000_000n;
const TX = `0x${"ab".repeat(32)}` as Hex;
const APPROVAL = `0x${"cd".repeat(32)}` as Hex;
const CLAIM = `0x${"ef".repeat(32)}` as Hex;

function fake(
  task: Partial<DisputeTask>,
  terms = { window: 3_600n, ruledAt: NOW - 60n, pays: false },
  balance = 10_000_000n,
  gas: { eth?: bigint; allowance?: bigint; sent?: number } = {},
  faucet = { amount: 100_000_000n, opensAt: 0n },
) {
  const chain = {
    account: WORKER,
    now: vi.fn(async () => NOW),
    task: vi.fn(async () => ({
      status: Status.Graded,
      poster: POSTER,
      payee: WORKER,
      accepted: false,
      disputed: false,
      gradedAt: NOW - 60n,
      disputeWindow: 3_600n,
      ruleWindow: 21_600n,
      ...task,
    })),
    appealOf: vi.fn(async () => terms),
    appealBond: vi.fn(async () => 1_250_000n),
    bountyBalance: vi.fn(async () => balance),
    bountyFaucet: vi.fn(async () => faucet),
    claimBounty: vi.fn(async () => CLAIM),
    ethBalance: vi.fn(async () => gas.eth ?? parseEther("0.001")),
    sent: vi.fn(async () => gas.sent ?? 5),
    gasPrice: vi.fn(async () => parseGwei("0.1")),
    allowance: vi.fn(async () => gas.allowance ?? 0n),
    approveBounty: vi.fn(async (): Promise<Hex | undefined> => APPROVAL),
    dispute: vi.fn(async () => TX),
    appeal: vi.fn(async () => TX),
  } satisfies DisputeChain;
  return chain;
}

describe("dispute", () => {
  it("disputes a grade on work the worker delivered, inside the window", async () => {
    const chain = fake({});
    const lines: string[] = [];
    await dispute(TESTNET, chain, 7n, (l) => lines.push(l));
    expect(chain.dispute).toHaveBeenCalledWith(7n);
    expect(lines[0]).toBe(`Disputed the grade on task 7 (it rejected the work): ${TX}`);
  });

  it("refuses a stranger, a second dispute, an ungraded task and a closed window", async () => {
    await expect(dispute(TESTNET, fake({ payee: POSTER }), 7n, () => {})).rejects.toThrow("is neither");
    await expect(dispute(TESTNET, fake({ disputed: true }), 7n, () => {})).rejects.toThrow("not waiting on a dispute");
    await expect(dispute(TESTNET, fake({ status: Status.Submitted }), 7n, () => {})).rejects.toThrow("not waiting on a dispute");
    await expect(dispute(TESTNET, fake({ gradedAt: NOW - 3_601n }), 7n, () => {})).rejects.toThrow("closed at");
    await expect(dispute(TESTNET, fake({ status: 0 }), 7n, () => {})).rejects.toThrow("There is no task 7");
  });
});

describe("appeal", () => {
  it("approves the bond and appeals a ruling that went against the worker", async () => {
    const chain = fake({ status: Ruled });
    const lines: string[] = [];
    await appeal(TESTNET, chain, 7n, (l) => lines.push(l));
    expect(chain.approveBounty).toHaveBeenCalledWith(1_250_000n);
    expect(chain.appeal).toHaveBeenCalledWith(7n);
    expect(lines[0]).toBe(`Appealed the ruling on task 7 with a 1.25 tUSDG bond: ${TX}`);
  });

  it("leaves the appeal to the poster when the ruling pays the worker", async () => {
    const chain = fake({ status: Ruled }, { window: 3_600n, ruledAt: NOW - 60n, pays: true });
    await expect(appeal(TESTNET, chain, 7n, () => {})).rejects.toThrow("pays the model, so only the poster");
    expect(chain.appeal).not.toHaveBeenCalled();
  });

  it("says why a task cannot be appealed", async () => {
    await expect(appeal(TESTNET, fake({ status: Status.Disputed }), 7n, () => {})).rejects.toThrow("still waiting for Jev's ruling");
    await expect(appeal(TESTNET, fake({ status: Appealed }), 7n, () => {})).rejects.toThrow("already under appeal");
    await expect(appeal(TESTNET, fake({ status: Status.Paid }), 7n, () => {})).rejects.toThrow("no ruling open to appeal");
    await expect(appeal(TESTNET, fake({ status: Ruled }, { window: 3_600n, ruledAt: NOW - 3_601n, pays: false }), 7n, () => {})).rejects.toThrow("closed at");
  });

  it("claims test USDG from its faucet first when the wallet holds less than the bond, and refuses while the faucet is closed", async () => {
    // A worker's first task is rejected and it loses the dispute: it has never been paid, so it holds no tUSDG.
    const chain = fake({ status: Ruled }, undefined, 0n);
    const lines: string[] = [];
    await appeal(TESTNET, chain, 7n, (l) => lines.push(l));
    expect(chain.claimBounty).toHaveBeenCalledOnce();
    expect(chain.claimBounty.mock.invocationCallOrder[0]).toBeLessThan(chain.approveBounty.mock.invocationCallOrder[0]!);
    expect(chain.appeal).toHaveBeenCalledWith(7n);
    expect(lines.slice(0, 2)).toEqual(["Claiming tUSDG from the testnet faucet for the bond...", `Claimed: ${CLAIM}`]);

    const closed = fake({ status: Ruled }, undefined, 1_000_000n, {}, { amount: 100_000_000n, opensAt: NOW + 600n });
    await expect(appeal(TESTNET, closed, 7n, () => {})).rejects.toThrow(
      "The appeal bond is 1.25 tUSDG, and this wallet holds 1. The tUSDG faucet allows one claim a day, and this wallet can claim again at 2027-01-15T08:10:00Z. Run appeal again then, before the appeal window closes at 2027-01-15T08:59:00Z.",
    );
    const late = fake({ status: Ruled }, undefined, 0n, {}, { amount: 100_000_000n, opensAt: NOW + 7_200n });
    await expect(appeal(TESTNET, late, 7n, () => {})).rejects.toThrow("can claim again at 2027-01-15T10:00:00Z, after the appeal window closes at 2027-01-15T08:59:00Z.");
    for (const refused of [closed, late]) {
      expect(refused.claimBounty).not.toHaveBeenCalled();
      expect(refused.approveBounty).not.toHaveBeenCalled();
    }
  });

  it("counts the faucet claim's gas before sending anything", async () => {
    // Enough for the approval and the appeal, not for the claim before them.
    const chain = fake({ status: Ruled }, undefined, 0n, { eth: parseEther("0.000039") });
    await expect(appeal(TESTNET, chain, 7n, () => {})).rejects.toThrow(`${WORKER} holds 0.000039 ETH on BrainChain testnet; the appeal needs about 0.000047 ETH for gas.`);
    expect(chain.claimBounty).not.toHaveBeenCalled();
  });

  it("sends a mainnet wallet short of the bond to the bridge", async () => {
    const chain = fake({ status: Ruled }, undefined, 1_000_000n);
    await expect(appeal(MAINNET, chain, 7n, () => {})).rejects.toThrow(
      "The appeal bond is 1.25 USDG, and this wallet holds 1. Bridge more with `npx brainchain-worker bridge --bounty <amount>`.",
    );
    expect(chain.claimBounty).not.toHaveBeenCalled();
    expect(chain.approveBounty).not.toHaveBeenCalled();
  });

  it("refuses before sending anything when the wallet cannot pay the gas of both the approval and the appeal", async () => {
    // What the wallet in the report held: enough for the approval, not for the appeal after it.
    const chain = fake({ status: Ruled }, undefined, undefined, { eth: parseEther("0.0000295") });
    const refusal = appeal(TESTNET, chain, 7n, () => {});
    await expect(refusal).rejects.toThrow(
      `${WORKER} holds 0.0000295 ETH on BrainChain testnet; the appeal needs about 0.000039 ETH for gas. Get Robinhood Chain testnet ETH from https://faucet.testnet.chain.robinhood.com`,
    );
    await expect(refusal).rejects.toThrow(/Nothing was sent\.$/);
    expect(chain.approveBounty).not.toHaveBeenCalled();
    expect(chain.appeal).not.toHaveBeenCalled();

    // With the bond already approved only the appeal is sent, so only its gas counts.
    const approved = fake({ status: Ruled }, undefined, undefined, { eth: parseEther("0.000034"), allowance: 1_250_000n });
    approved.approveBounty.mockResolvedValue(undefined);
    await appeal(TESTNET, approved, 7n, () => {});
    expect(approved.appeal).toHaveBeenCalledWith(7n);

    // The report's second attempt: the bond approved, 0.0000208 ETH left, and a raw selector where words belonged.
    const second = fake({ status: Ruled }, undefined, undefined, { eth: parseEther("0.0000208345"), allowance: 1_250_000n });
    await expect(appeal(TESTNET, second, 7n, () => {})).rejects.toThrow(`${WORKER} holds 0.0000208345 ETH on BrainChain testnet; the appeal needs about 0.000034 ETH for gas.`);
    expect(second.appeal).not.toHaveBeenCalled();
  });

  it("says the approval went through when the appeal after it fails", async () => {
    const chain = fake({ status: Ruled });
    chain.appeal.mockRejectedValue(new BaseError("Execution reverted with reason: gas required exceeds allowance (86810).", { cause: new InsufficientFundsError() }));
    const failure = appeal(TESTNET, chain, 7n, () => {});
    await expect(failure).rejects.toThrow(`The board was approved to take the 1.25 tUSDG bond (${APPROVAL}), and then the appeal failed: The wallet holds too little ETH`);
    await expect(failure).rejects.toThrow("The approval stands, so running appeal again before 2027-01-15T08:59:00Z sends only the appeal.");
    await expect(failure).rejects.not.toThrow("Nothing was sent");

    // Nothing was approved this time, so the appeal's own error stands alone.
    const again = fake({ status: Ruled }, undefined, undefined, { allowance: 1_250_000n });
    again.approveBounty.mockResolvedValue(undefined);
    again.appeal.mockRejectedValue(new Error("Transaction reverted"));
    await expect(appeal(TESTNET, again, 7n, () => {})).rejects.toThrow(/^Transaction reverted$/);
  });
});

describe("the board's errors", () => {
  const abi = parseAbi(["error FailedInnerCall()", "error NotAppellant()"]);
  const reverted = (errorName: "FailedInnerCall" | "NotAppellant") =>
    new ContractFunctionExecutionError(new ContractFunctionRevertedError({ abi, data: encodeErrorResult({ abi, errorName }), functionName: "appeal" }), {
      abi,
      functionName: "appeal",
    });

  it("reads a revert that only the gas cap caused as a wallet short of gas, and leaves a real one as it is", async () => {
    // The RPC runs the estimate with no more gas than the wallet pays for, and the bond's transfer runs out inside it.
    expect(reason(await explainRevert(reverted("FailedInnerCall"), async () => "0x"))).toBe(
      "The wallet holds too little ETH to pay for this transaction's gas, so it was not sent. `brainchain-worker status` shows what it holds",
    );
    const real = reverted("NotAppellant");
    expect(
      await explainRevert(real, async () => {
        throw real;
      }),
    ).toBe(real);
    expect(reason(real)).toBe('The contract function "appeal" reverted: only the side the ruling went against can appeal it (NotAppellant)');
    expect(reason(reverted("FailedInnerCall"))).toBe('The contract function "appeal" reverted: a token transfer inside the call failed without a reason (FailedInnerCall)');
    const other = new Error("fetch failed");
    expect(await explainRevert(other, async () => "0x")).toBe(other);
    // A selector no ABI here knows is still a revert to check.
    const unknown = new ContractFunctionExecutionError(new ContractFunctionRevertedError({ abi: [], data: "0x12345678", functionName: "appeal" }), { abi: [], functionName: "appeal" });
    expect(reason(await explainRevert(unknown, async () => "0x"))).toMatch(/^The wallet holds too little ETH/);
  });
});
