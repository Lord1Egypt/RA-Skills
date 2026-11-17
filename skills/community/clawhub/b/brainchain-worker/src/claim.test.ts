import { parseEther, type Address, type Hex } from "viem";
import { describe, expect, it, vi } from "vitest";

import { claim, MAX_CLAIM, type IncomeChain } from "./claim.js";
import { MAINNET, TESTNET } from "./network.js";

const ACCOUNT: Address = "0x00000000000000000000000000000000000000C1";
const TX: Hex = `0x${"fe".repeat(32)}`;
const OWNED = `https://brain.usebrainchain.com/proofs/274663/owned/${ACCOUNT}`;

function fakeChain(dues: Record<string, bigint>, gas = parseEther("0.001")) {
  return {
    account: ACCOUNT,
    due: vi.fn(async (ids: bigint[]) => ids.map((id) => dues[id.toString()] ?? 0n)),
    ethBalance: vi.fn(async () => gas),
    claimMany: vi.fn(async (ids: bigint[]) => ({ tx: TX, paid: ids.reduce((sum, id) => sum + (dues[id.toString()] ?? 0n), 0n) })),
  } satisfies IncomeChain;
}

const listing = (body: unknown, status = 200) => vi.fn<typeof fetch>(async () => Response.json(body, { status }));

async function run(chain: IncomeChain, fetcher: typeof fetch, options: { dry?: boolean; network?: typeof MAINNET } = {}) {
  const lines: string[] = [];
  const connect = vi.fn((_income: Address) => chain);
  await claim(options.network ?? MAINNET, connect, { dry: options.dry ?? false, log: (line) => lines.push(line), fetcher });
  return { lines, connect };
}

describe("claim", () => {
  it("pays every Proof with income due in one claimMany and prints the total and the hash", async () => {
    const chain = fakeChain({ "1": parseEther("0.00040043125"), "7": parseEther("0.0002") });
    const fetcher = listing({ tokens: ["7", "4", "1", "4"] });
    const { lines, connect } = await run(chain, fetcher);

    expect(connect).toHaveBeenCalledWith("0xeb1b4168D4b87D3d9F0D64E13B7071251BBB63b7");
    expect(fetcher.mock.calls[0]![0]).toBe(OWNED);
    expect(chain.due).toHaveBeenCalledWith([1n, 4n, 7n]);
    expect(chain.claimMany).toHaveBeenCalledOnce();
    expect(chain.claimMany).toHaveBeenCalledWith([1n, 7n]);
    expect(lines).toEqual([
      ["  Proof  Due (ETH)", "  1      0.00040043125", "  4      0", "  7      0.0002", "  Total  0.00060043125"].join("\n"),
      "Claiming 0.00060043125 ETH for 2 Proofs on Robinhood Chain...",
      `Paid 0.00060043125 ETH to ${ACCOUNT} (${TX}).`,
    ]);
  });

  it("sends nothing on a dry run", async () => {
    const chain = fakeChain({ "3": parseEther("0.0004") }, 0n);
    const { lines } = await run(chain, listing({ tokens: ["3"] }), { dry: true });
    expect(chain.claimMany).not.toHaveBeenCalled();
    expect(chain.ethBalance).not.toHaveBeenCalled();
    expect(lines.at(-1)).toBe("Dry run, nothing sent: claim would pay 0.0004 ETH for 1 Proof.");
  });

  it("says so when nothing is due", async () => {
    const chain = fakeChain({});
    const { lines } = await run(chain, listing({ tokens: ["2", "5"] }));
    expect(chain.claimMany).not.toHaveBeenCalled();
    expect(lines.at(-1)).toBe("Nothing is due on the worker's 2 Proofs yet.");
  });

  it("says so when the worker holds no Proofs", async () => {
    const chain = fakeChain({});
    const { lines } = await run(chain, listing({ tokens: [] }));
    expect(chain.due).not.toHaveBeenCalled();
    expect(lines).toEqual([`The BrainChain service lists no Proofs held by ${ACCOUNT} on Robinhood Chain, so there is nothing to claim.`]);
  });

  it("says testnet Proofs earn no income without asking for the key or the service", async () => {
    const fetcher = listing({ tokens: ["1"] });
    const { lines, connect } = await run(fakeChain({}), fetcher, { network: TESTNET });
    expect(connect).not.toHaveBeenCalled();
    expect(fetcher).not.toHaveBeenCalled();
    expect(lines).toEqual(["Proofs on Robinhood Chain testnet earn no income, so there is nothing to claim. Mainnet Proofs are claimed with BRAINCHAIN_NETWORK=mainnet."]);
  });

  it("says the wallet needs ETH on Robinhood Chain for gas", async () => {
    const chain = fakeChain({ "1": parseEther("0.0004") }, 0n);
    await expect(run(chain, listing({ tokens: ["1"] }))).rejects.toThrow(
      `${ACCOUNT} has no ETH on Robinhood Chain to pay gas for the claim. Send it a little ETH on Robinhood Chain and run claim again.`,
    );
    expect(chain.claimMany).not.toHaveBeenCalled();
  });

  it("claims at most 200 Proofs at a time and says how many are left", async () => {
    const ids = Array.from({ length: MAX_CLAIM + 3 }, (_, i) => String(i + 1));
    const chain = fakeChain(Object.fromEntries(ids.map((id) => [id, 1n])));
    const { lines } = await run(chain, listing({ tokens: ids }));
    expect(chain.claimMany.mock.calls[0]![0]).toHaveLength(MAX_CLAIM);
    expect(chain.claimMany.mock.calls[0]![0].at(-1)).toBe(200n);
    expect(lines.at(-1)).toBe(`Paid 0.0000000000000002 ETH to ${ACCOUNT} (${TX}). 3 more Proofs have income due: run claim again.`);
  });

  it("names a service that does not list Proofs yet, or answers in a form it cannot read", async () => {
    await expect(run(fakeChain({}), listing({ error: "Not Found" }, 404))).rejects.toThrow(
      "The BrainChain service at brain.usebrainchain.com does not list Proofs by holder yet. Try claim again later.",
    );
    await expect(run(fakeChain({}), listing({}, 502))).rejects.toThrow("The BrainChain service at brain.usebrainchain.com answered 502");
    for (const body of [{}, { tokens: "1" }, { tokens: [1] }, { tokens: ["0x1"] }, null]) {
      await expect(run(fakeChain({}), listing(body))).rejects.toThrow("in a form claim cannot read");
    }
    const down = vi.fn<typeof fetch>(async () => {
      throw new TypeError("fetch failed");
    });
    await expect(run(fakeChain({}), down)).rejects.toThrow("Could not reach the BrainChain service at brain.usebrainchain.com");
  });
});
