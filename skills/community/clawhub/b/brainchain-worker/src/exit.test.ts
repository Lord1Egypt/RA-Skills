import type { Address, Hex } from "viem";
import { describe, expect, it, vi } from "vitest";

import { decodeFunctionData, erc20Abi } from "viem";

import { createServer } from "node:http";
import type { AddressInfo } from "node:net";

import { privateKeyToAccount } from "viem/accounts";

import { createExitChain, exit, exitCalldata, exitFee, exitTerms, isSolanaAddress, type ExitChain, type ExitTerms } from "./exit.js";
import { MAINNET, TESTNET } from "./network.js";
import { checkReturn } from "./relay.js";
import { split } from "./solana.js";

const DESK = TESTNET.exitDesk;
const TOKEN = TESTNET.contracts.bountyToken;
const terms: ExitTerms = { desk: DESK, token: TOKEN, payoutChainId: 46630, payoutToken: "0x00000000000000000000000000000000000000a1", feeBps: 50, minFeeUnits: "10000", minUnits: "1000000", maxUnits: "100000000" };
const TX = `0x${"ab".repeat(32)}` as Hex;
const SOLANA = "7xKXtg2CW87d97TXJSDpbD5jBkheTqA83TZRuJosgAsU";

const mainnetTerms: ExitTerms = { ...terms, desk: MAINNET.exitDesk, token: MAINNET.contracts.bountyToken, payoutChainId: 4663 };

function fetchWith(records: unknown[], named: unknown = terms) {
  const queue = [...records];
  return vi.fn(async (url: string) => {
    if (url.endsWith("/exits")) return new Response(JSON.stringify(named));
    const next = queue.length > 1 ? queue.shift() : queue[0];
    return next === undefined ? new Response("{}", { status: 404 }) : new Response(JSON.stringify({ exits: [next] }));
  }) as unknown as typeof fetch;
}

function chainWith(balance: bigint) {
  const sent: { to: Address; amount: bigint; solana?: string }[] = [];
  const chain: ExitChain = {
    account: "0x0000000000000000000000000000000000000077",
    bountyBalance: vi.fn(async () => balance),
    unmined: vi.fn(async () => 0),
    sendToDesk: vi.fn(async (_token, to, amount, solana) => {
      sent.push({ to, amount, ...(solana ? { solana } : {}) });
      return TX;
    }),
  };
  return { chain, sent };
}

const quiet = () => {
  const lines: string[] = [];
  return { lines, log: (l: string) => lines.push(l) };
};

describe("exit", () => {
  it("sends the whole balance to the desk and reports the payout", async () => {
    const { chain, sent } = chainWith(5_000_000n);
    const { lines, log } = quiet();
    await exit(TESTNET, chain, { dry: false, log, fetchImpl: fetchWith([{ state: "waiting", reason: "x", net: "4975000", fee: "25000" }, { state: "paid", net: "4975000", fee: "25000", payoutTx: TX }]), sleep: async () => {} });
    expect(sent).toEqual([{ to: DESK, amount: 5_000_000n }]);
    expect(lines.at(-1)).toMatch(/Paid on the parent chain: 4\.975 tUSDG/);
  });

  it("refuses an exit below the minimum or above the balance, before sending", async () => {
    const { chain, sent } = chainWith(5_000_000n);
    await expect(exit(TESTNET, chain, { amount: "0.5", dry: false, log: () => {}, fetchImpl: fetchWith([]) })).rejects.toThrow(/at least 1 tUSDG/);
    await expect(exit(TESTNET, chain, { amount: "6", dry: false, log: () => {}, fetchImpl: fetchWith([]) })).rejects.toThrow(/less than 6 tUSDG/);
    expect(sent).toHaveLength(0);
  });

  it("keeps --to-solana to mainnet and to real Solana addresses", async () => {
    const { chain } = chainWith(5_000_000n);
    await expect(exit(TESTNET, chain, { toSolana: SOLANA, dry: true, log: () => {}, fetchImpl: fetchWith([]) })).rejects.toThrow(/mainnet only/);
    await expect(exit(MAINNET, chain, { toSolana: "not-an-address", dry: true, log: () => {}, fetchImpl: fetchWith([]) })).rejects.toThrow(/not the address of a Solana wallet/);
  });

  it("refuses a token or a desk this release does not know, before anything is read or signed", async () => {
    const evil = "0x000000000000000000000000000000000000dEaD" as Address;
    const { chain, sent } = chainWith(5_000_000n);
    for (const [named, line] of [
      [{ ...terms, token: TESTNET.contracts.stakeToken }, `names the token ${TESTNET.contracts.stakeToken} for an exit, and BrainChain testnet's tUSDG is ${TOKEN}. Nothing was sent.`],
      [{ ...terms, desk: evil }, `names the desk ${evil}, and this release of brainchain-worker pays only ${DESK}. Nothing was sent.`],
    ] as const) {
      for (const dry of [true, false]) await expect(exit(TESTNET, chain, { dry, log: () => {}, fetchImpl: fetchWith([], named) })).rejects.toThrow(line);
    }
    expect(chain.bountyBalance).not.toHaveBeenCalled();
    expect(sent).toHaveLength(0);
    await exit(TESTNET, chain, { dry: true, log: () => {}, fetchImpl: fetchWith([], { ...terms, token: TOKEN.toLowerCase(), desk: DESK.toLowerCase() }) });
  });

  it("treats a held exit as final: says who holds it and why, and exits 1", async () => {
    const { chain } = chainWith(5_000_000n);
    const { lines, log } = quiet();
    const sleep = vi.fn(async () => {});
    try {
      await exit(TESTNET, chain, { dry: false, log, fetchImpl: fetchWith([{ state: "held", net: "4975000", fee: "25000", reason: "Relay will not refund the Solana move (DEPOSIT_ADDRESS_MISMATCH)" }]), sleep });
      expect(process.exitCode).toBe(1);
    } finally {
      process.exitCode = 0;
    }
    expect(sleep).not.toHaveBeenCalled();
    expect(lines.at(-1)).toBe(`The desk holds this exit for a person: Relay will not refund the Solana move (DEPOSIT_ADDRESS_MISMATCH). Nothing more is sent for it until it is settled; follow it at ${TESTNET.service}/exits/${TX}.`);
  });

  it("says what a long wait can still come to, with the hold where one can happen", async () => {
    const { chain } = chainWith(5_000_000n);
    for (const [network, toSolana, named, line] of [
      [TESTNET, undefined, terms, "The desk pays it or sends it back within a day; follow it at"],
      [MAINNET, SOLANA, mainnetTerms, "Within a day the desk pays it or sends it back, or holds it for a person if Relay has not settled the move; follow it at"],
    ] as const) {
      const { lines, log } = quiet();
      await exit(network, chain, { ...(toSolana ? { toSolana } : {}), dry: false, log, waitMs: -1, fetchImpl: fetchWith([{ state: "waiting", net: "1", fee: "1" }], named), sleep: async () => {} });
      expect(lines.at(-1)).toContain(line);
    }
  });

  it("opens an exit to Solana with where it is paid, not the parent chain's arrival", async () => {
    const { chain } = chainWith(2_000_000n);
    const { lines, log } = quiet();
    await exit(MAINNET, chain, { toSolana: SOLANA, dry: true, log, fetchImpl: fetchWith([], mainnetTerms) });
    expect(lines[0]).toBe(`Exit 2 USDG from BrainChain: 1.99 USDG after a 0.01 USDG fee is paid as USDC on Solana to ${SOLANA}, less Relay's own fee. The desk prices that move once the transfer arrives; one that would cost more than 3% (or 0.50 USD) is paid in USDG on the parent chain (chain 4663) instead.`);
  });

  it("names the way forward above the maximum, with or without --amount, since nothing was sent", async () => {
    const { chain, sent } = chainWith(500_000_000n);
    for (const amount of [undefined, "150"]) {
      await expect(exit(TESTNET, chain, { ...(amount ? { amount } : {}), dry: false, log: () => {}, fetchImpl: fetchWith([]) })).rejects.toThrow("An exit is at most 100 tUSDG, and nothing was sent. Give --amount up to that, and send the rest in another exit.");
    }
    expect(sent).toHaveLength(0);
  });

  it("will not send while an earlier transaction of the wallet is unmined, since it may be an exit", async () => {
    const { chain, sent } = chainWith(5_000_000n);
    vi.mocked(chain.unmined).mockResolvedValue(1);
    await expect(exit(TESTNET, chain, { dry: false, log: () => {}, fetchImpl: fetchWith([]) })).rejects.toThrow("not mined yet, which may be an earlier exit, and another run would send another transfer. Nothing was sent");
    expect(sent).toHaveLength(0);
  });

  it("names the Solana address in the transfer and reports the desk's payout there", async () => {
    const { chain, sent } = chainWith(5_000_000n);
    const { lines, log } = quiet();
    await exit(MAINNET, chain, { toSolana: SOLANA, dry: false, log, fetchImpl: fetchWith([{ state: "paid", net: "4975000", fee: "25000", payoutTx: TX, solana: SOLANA, relayRequest: "0xreq" }], mainnetTerms), sleep: async () => {} });
    expect(sent).toEqual([{ to: MAINNET.exitDesk, amount: 5_000_000n, solana: SOLANA }]);
    expect(lines.at(-1)).toMatch(/Paid on Solana: 4\.975 USDG as USDC to 7xKX/);
  });
});

describe("pieces", () => {
  it("prices an exit like the desk", () => {
    expect(exitFee(10_000_000n, terms)).toBe(50_000n);
    expect(exitFee(1_000_000n, terms)).toBe(10_000n);
  });
  it("puts the Solana address after a plain transfer's arguments", () => {
    const plain = exitCalldata(DESK, 5n);
    expect(decodeFunctionData({ abi: erc20Abi, data: plain }).args).toEqual([DESK, 5n]);
    const named = exitCalldata(DESK, 5n, SOLANA);
    expect(named.startsWith(plain)).toBe(true);
    expect((named.length - plain.length) / 2).toBe(32);
  });
  it("knows a Solana address", () => {
    expect(isSolanaAddress(SOLANA)).toBe(true);
    expect(isSolanaAddress("0x0000000000000000000000000000000000000077")).toBe(false);
  });
  it("refuses addresses no wallet spends from: off the curve, all zero, and the programs that are on it", () => {
    // A program-derived address, Relay's vault's.
    expect(isSolanaAddress("7uTT8Xi5RWXzy7h9XL244GRgEycDYDhLjr3ZyNdXi8pZ")).toBe(false);
    expect(isSolanaAddress("11111111111111111111111111111111")).toBe(false);
    for (const program of ["TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA", "TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb", "ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL", "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v", "99vQwtBwYtrqqD9YSXbdum3KBdxPAVxYTaQ3cfnJSrN2"]) {
      expect(isSolanaAddress(program), program).toBe(false);
    }
  });
  it("refuses a Relay quote that loses more than 3%, or 0.50 USD on a small move", () => {
    expect(() => checkReturn({ inUsd: 100, outUsd: 95 })).toThrow(/keep 5\.00 USD of 100\.00, more than the 3\.00/);
    expect(() => checkReturn({ inUsd: 100, outUsd: 97.5 })).not.toThrow();
    expect(() => checkReturn({ inUsd: 3, outUsd: 2.87 })).not.toThrow();
    expect(() => checkReturn({ inUsd: 3, outUsd: 2.4 })).toThrow(/0\.50/);
  });
  it("splits Solana USDC between gas and stake", () => {
    expect(split(10_000_000n, 2_000_000n, true)).toEqual({ gas: 2_000_000n, stake: 8_000_000n });
    expect(() => split(2_000_000n, 2_000_000n, true)).toThrow(/more than the 2 USDC/);
  });
});

describe("exit terms", () => {
  const answering = (status: number, body: string) => (async () => new Response(body, { status })) as unknown as typeof fetch;
  const host = "brain.example.com";
  const service = `https://${host}`;

  it("says the exits are off, and which service could not be read and why, with nothing sent", async () => {
    await expect(exitTerms(service, answering(404, "{}"))).rejects.toThrow("Fast exits are off on this network");
    await expect(exitTerms(service, (async () => Promise.reject(new TypeError("fetch failed"))) as unknown as typeof fetch)).rejects.toThrow(`Could not reach the BrainChain service at ${host} for the exit terms. Nothing was sent.`);
    await expect(exitTerms(service, answering(502, "bad gateway"))).rejects.toThrow(`The BrainChain service at ${host} answered 502 when asked for the exit terms. Nothing was sent.`);
    const form = `The BrainChain service at ${host} named the exit terms in a form exit cannot read. Nothing was sent.`;
    for (const body of ["{}", "<html>", "null", JSON.stringify({ ...terms, minUnits: 5 }), JSON.stringify({ ...terms, desk: "nope" }), JSON.stringify({ ...terms, feeBps: "50" })]) {
      await expect(exitTerms(service, answering(200, body)), body).rejects.toThrow(form);
    }
    await expect(exitTerms(service, answering(200, JSON.stringify(terms)))).resolves.toEqual(terms);
  });
});

describe("a transfer that was sent and not confirmed", () => {
  it("names the transaction and that another run sends another transfer", async () => {
    const account = privateKeyToAccount(`0x${"4f".repeat(32)}`);
    const answers: Record<string, unknown> = {
      eth_chainId: `0x${TESTNET.chainId.toString(16)}`,
      eth_getTransactionCount: "0x0",
      eth_estimateGas: "0x5208",
      eth_gasPrice: "0x1",
      eth_maxPriorityFeePerGas: "0x1",
      eth_getBlockByNumber: { number: "0x1", baseFeePerGas: "0x1", timestamp: "0x1", transactions: [], hash: `0x${"11".repeat(32)}` },
      eth_sendRawTransaction: TX,
      eth_getTransactionReceipt: null,
      eth_blockNumber: "0x1",
      eth_getTransactionByHash: null,
    };
    const server = createServer((req, res) => {
      let body = "";
      req.on("data", (chunk) => (body += chunk));
      req.on("end", () => {
        const answer = (call: { id: number; method: string }) => ({ jsonrpc: "2.0", id: call.id, result: answers[call.method] ?? null });
        const parsed = JSON.parse(body) as { id: number; method: string } | { id: number; method: string }[];
        res.setHeader("content-type", "application/json");
        res.end(JSON.stringify(Array.isArray(parsed) ? parsed.map(answer) : answer(parsed)));
      });
    });
    await new Promise<void>((resolve) => server.listen(0, "127.0.0.1", resolve));
    try {
      const network = { ...TESTNET, rpc: `http://127.0.0.1:${(server.address() as AddressInfo).port}` };
      const chain = createExitChain(network, account, 50);
      expect(await chain.unmined()).toBe(0);
      await expect(chain.sendToDesk(TOKEN, DESK, 5n)).rejects.toThrow(`The transfer to the desk was sent (${TX}) and could not be confirmed`);
      await expect(chain.sendToDesk(TOKEN, DESK, 5n)).rejects.toThrow(`Follow it at ${TESTNET.service}/exits/${TX} before running exit again: another run sends another transfer.`);
    } finally {
      server.close();
      server.closeAllConnections();
    }
  });
});
