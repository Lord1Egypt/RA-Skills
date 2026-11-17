import { mkdtempSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

import { Keypair, PublicKey, SendTransactionError, VersionedTransaction, type Connection } from "@solana/web3.js";
import bs58 from "bs58";
import { parseEther, type Address } from "viem";
import { afterEach, describe, expect, it, vi } from "vitest";

import { NATIVE, SOLANA_USDC, type RelayQuote, type SvmItem } from "./relay.js";
import {
  ASSOCIATED_TOKEN_PROGRAM,
  createSolanaFunding,
  depositProblem,
  DEPOSITORY_STATE,
  DEPOSITORY_VAULT,
  DEPOSITORY_VAULT_USDC,
  fundFromSolana,
  PARENT_ETH_KEEP,
  RELAY_DEPOSITORY,
  sendSvmStep,
  solanaKeypair,
  split,
  TOKEN_PROGRAM,
  unsettled,
  usdcAccount,
  type SolanaFunding,
} from "./solana.js";

const WORKER: Address = "0x611357db1876d7E7809a5b751c9A15c0E3BAc965";
const STAKE: Address = "0xC80333bf7f4078e14Ce5b6e223aF607aDcA44418";
const SIGNER = Keypair.fromSeed(new Uint8Array(32).fill(7));
const OWNER = SIGNER.publicKey.toBase58();

/** The one instruction of every quote Relay answered for USDC on Solana: wallets with and without USDC, both currencies, four amounts. */
function deposit(amount: bigint, owner = OWNER): SvmItem {
  const le = Buffer.alloc(8);
  le.writeBigUInt64LE(amount);
  const key = (pubkey: string, isSigner = false, isWritable = false) => ({ pubkey, isSigner, isWritable });
  return {
    instructions: [
      {
        programId: RELAY_DEPOSITORY,
        keys: [
          key(DEPOSITORY_STATE),
          key(owner, true, true),
          key(owner),
          key(DEPOSITORY_VAULT),
          key(SOLANA_USDC),
          key(usdcAccount(owner), false, true),
          key(DEPOSITORY_VAULT_USDC, false, true),
          key(TOKEN_PROGRAM),
          key(ASSOCIATED_TOKEN_PROGRAM),
          key("11111111111111111111111111111111"),
        ],
        data: `0b9c60da27a3b413${le.toString("hex")}${"07".repeat(32)}`,
      },
    ],
    addressLookupTableAddresses: ["Hm9fUgcn7qwDaiNTFiGh6pNtVATgnaRcmK6Bbx6EMZfP"],
  };
}

function quote(amount: bigint, currency: string, out: bigint, id = "0xrequest"): RelayQuote {
  return {
    requestId: id,
    steps: [{ id: "deposit", requestId: id, items: [{ data: deposit(amount) }] }],
    inUsd: 2,
    outUsd: 1.97,
    outAmount: out,
    outFormatted: currency === NATIVE ? "0.0006" : "55000",
    recipient: WORKER,
    outCurrency: currency,
    outChainId: 4663,
  };
}

const want = (amount: bigint, currency = NATIVE) => ({ owner: OWNER, amount, recipient: WORKER, currency, chainId: 4663 });

describe("the depository accounts", () => {
  const program = new PublicKey(RELAY_DEPOSITORY);
  const pda = (seed: string) => PublicKey.findProgramAddressSync([Buffer.from(seed)], program)[0].toBase58();

  it("are the addresses Relay's program derives, and a real quote's owner account is this formula's", () => {
    expect(pda("relay_depository")).toBe(DEPOSITORY_STATE);
    expect(pda("vault")).toBe(DEPOSITORY_VAULT);
    expect(usdcAccount(DEPOSITORY_VAULT)).toBe(DEPOSITORY_VAULT_USDC);
    // From a quote Relay answered for this wallet.
    expect(usdcAccount("Hd58GSJfP7DGMm79bLsBTbRoGyZYvmXRd3y9SUTNhSHr")).toBe("Bq5HfoKfZg17XZz8cMkCv9EsL1dHCgiaBrJXsAJebf1j");
  });
});

describe("depositProblem", () => {
  const amount = 2_000_000n;
  const withItem = (item: SvmItem, base = quote(amount, NATIVE, 1n)): RelayQuote => ({ ...base, steps: [{ id: "deposit", items: [{ data: item }] }] });
  const changed = (change: (item: SvmItem) => void) => {
    const item = deposit(amount);
    change(item);
    return depositProblem(withItem(item), want(amount));
  };

  it("takes the deposit Relay quotes", () => {
    expect(depositProblem(quote(amount, NATIVE, 1n), want(amount))).toBeUndefined();
    expect(depositProblem(quote(amount, STAKE.toLowerCase(), 1n), want(amount, STAKE))).toBeUndefined();
  });

  it("refuses the auditor's stand-in: a plain token transfer out of the wallet", () => {
    const le = Buffer.alloc(8);
    le.writeBigUInt64LE(50_000_000n);
    const evil: SvmItem = {
      addressLookupTableAddresses: [],
      instructions: [
        {
          programId: TOKEN_PROGRAM,
          keys: [
            { pubkey: usdcAccount(OWNER), isSigner: false, isWritable: true },
            { pubkey: "4Nd1mBQtrMJVYVfKf2PJy9NZUZdTAsp7D4xWLs4gDB4T", isSigner: false, isWritable: true },
            { pubkey: OWNER, isSigner: true, isWritable: false },
          ],
          data: `03${le.toString("hex")}`,
        },
      ],
    };
    expect(depositProblem(withItem(evil), want(amount))).toBe(`it calls the program ${TOKEN_PROGRAM}, not Relay's depository`);
  });

  it("refuses another amount, instruction, account or signer", () => {
    expect(depositProblem(quote(50_000_000n, NATIVE, 1n), want(amount))).toBe("it deposits 50 USDC, not the 2 asked for");
    expect(changed((item) => item.instructions.push(item.instructions[0]!))).toBe("it carries 2 instructions where a deposit has one");
    expect(changed((item) => (item.instructions.length = 0))).toBe("it carries 0 instructions where a deposit has one");
    expect(changed((item) => (item.instructions[0]!.data = `deadbeefdeadbeef${item.instructions[0]!.data.slice(16)}`))).toBe("it calls Relay's depository for something other than a token deposit");
    expect(changed((item) => (item.instructions[0]!.keys[6]!.pubkey = "4Nd1mBQtrMJVYVfKf2PJy9NZUZdTAsp7D4xWLs4gDB4T"))).toBe(`its account 6 is 4Nd1mBQtrMJVYVfKf2PJy9NZUZdTAsp7D4xWLs4gDB4T, not ${DEPOSITORY_VAULT_USDC}`);
    expect(changed((item) => (item.instructions[0]!.keys[2]!.pubkey = "4Nd1mBQtrMJVYVfKf2PJy9NZUZdTAsp7D4xWLs4gDB4T"))).toContain("its account 2");
    expect(changed((item) => item.instructions[0]!.keys.pop())).toBe("it names 9 accounts where a deposit names 10");
    expect(changed((item) => (item.instructions[0]!.keys[0]!.isSigner = true))).toBe("it asks another account to sign");
  });

  it("refuses a quote it cannot read rather than sign around it", () => {
    const base = quote(amount, NATIVE, 1n);
    expect(depositProblem({ ...base, steps: [{ id: "deposit", items: [{}] }] } as unknown as RelayQuote, want(amount))).toBe("it is in a form this command cannot read");
    expect(changed((item) => ((item.instructions[0]!.keys as unknown as unknown[])[3] = null))).toBe("it is in a form this command cannot read");
  });

  it("refuses more or other steps, and a quote that pays someone else or something else", () => {
    expect(depositProblem({ ...quote(amount, NATIVE, 1n), steps: [] }, want(amount))).toBe("it is not one deposit");
    const base = quote(amount, NATIVE, 1n);
    expect(depositProblem({ ...base, steps: [{ id: "approve", items: base.steps[0]!.items }] }, want(amount))).toBe("it is not one deposit");
    expect(depositProblem({ ...base, steps: [{ id: "deposit", items: [] }] }, want(amount))).toBe("it is not one deposit");
    expect(depositProblem({ ...base, recipient: "0x000000000000000000000000000000000000dEaD" }, want(amount))).toBe(`it pays 0x000000000000000000000000000000000000dEaD, not ${WORKER}`);
    const { recipient: _, ...unnamed } = base;
    expect(depositProblem(unnamed, want(amount))).toBe(`it pays no named recipient, not ${WORKER}`);
    expect(depositProblem({ ...base, outCurrency: STAKE }, want(amount))).toBe("it does not pay the currency asked for on Robinhood Chain");
    expect(depositProblem({ ...base, outChainId: 1 }, want(amount))).toBe("it does not pay the currency asked for on Robinhood Chain");
  });
});

describe("preview", () => {
  afterEach(() => void vi.unstubAllGlobals());

  const answering = (outUsd: number, item: SvmItem, recipient = WORKER) =>
    vi.fn(async () =>
      Response.json({
        details: { recipient, currencyIn: { amountUsd: "100" }, currencyOut: { amountUsd: String(outUsd), amount: "5", amountFormatted: "5", currency: { address: STAKE.toLowerCase(), chainId: 4663 } } },
        steps: [{ id: "deposit", requestId: "0xrequest", items: [{ data: item }] }],
      }),
    );

  it("gives the stake token's leg 5% and the ETH leg 3%, and refuses before signing a quote that is not the deposit asked for", async () => {
    const funding = createSolanaFunding(SIGNER, 4663);
    vi.stubGlobal("fetch", answering(96, deposit(100_000_000n)));
    await expect(funding.preview(STAKE, 100_000_000n, WORKER)).resolves.toMatchObject({ outAmount: 5n, recipient: WORKER });
    vi.stubGlobal("fetch", answering(94, deposit(100_000_000n)));
    await expect(funding.preview(STAKE, 100_000_000n, WORKER)).rejects.toThrow("more than the 5.00 this command accepts (5%, or 0.50 USD on a small move). Nothing was sent");
    vi.stubGlobal("fetch", answering(96, deposit(100_000_000n)));
    await expect(funding.preview(NATIVE, 100_000_000n, WORKER)).rejects.toThrow("more than the 3.00 this command accepts (3%, or 0.50 USD on a small move). Nothing was sent");
    vi.stubGlobal("fetch", answering(96, deposit(50_000_000n)));
    await expect(funding.preview(STAKE, 100_000_000n, WORKER)).rejects.toThrow("Relay's quote was refused before signing: it deposits 50 USDC, not the 100 asked for. Nothing was sent.");
  });
});

describe("split", () => {
  it("leaves on Solana what --gas-usdc does not take when there is no --stake, and never spends more than --usdc", () => {
    expect(split(20_000_000n, 2_000_000n, false)).toEqual({ gas: 2_000_000n, stake: 0n });
    expect(split(20_000_000n, 1_000_000n, false)).toEqual({ gas: 1_000_000n, stake: 0n });
    expect(split(1_000_000n, 2_000_000n, false)).toEqual({ gas: 1_000_000n, stake: 0n });
  });
});

/** A wallet on the parent chain, what each send lands in it and what its deposits to BrainChain cost. */
function rig(options: { eth?: bigint; stake?: bigint; landsEth?: bigint; landsStake?: bigint; arrival?: bigint; quoteEth?: bigint; quoteStake?: bigint } = {}) {
  const wallet = { eth: options.eth ?? 0n, stake: options.stake ?? 0n };
  const log: string[] = [];
  const bridged: ["eth" | "stake", bigint][] = [];
  const sent: RelayQuote[] = [];
  const previews: string[] = [];
  const funding: SolanaFunding = {
    owner: OWNER,
    usdcBalance: vi.fn(async () => 50_000_000n),
    solBalance: vi.fn(async () => 10_000_000n),
    preview: vi.fn(async (currency: string, amount: bigint) => {
      previews.push(currency);
      return currency === NATIVE ? quote(amount, NATIVE, options.quoteEth ?? parseEther("0.001"), "0xgas") : quote(amount, currency, options.quoteStake ?? parseEther("55000"), "0xstake");
    }),
    send: vi.fn(async (q: RelayQuote) => {
      sent.push(q);
      if (q.requestId === "0xgas") wallet.eth += options.landsEth ?? parseEther("0.001");
      else wallet.stake += options.landsStake ?? parseEther("55000");
      return `sig-${q.requestId}`;
    }),
  };
  const run = (extra: Partial<Parameters<typeof fundFromSolana>[0]> = {}) =>
    fundFromSolana({
      funding,
      worker: WORKER,
      usdc: "20",
      stake: true,
      stakeToken: STAKE,
      dry: false,
      log: (line) => log.push(line),
      parentEth: async () => wallet.eth,
      parentStake: async () => wallet.stake,
      bridgeOn: async (asset, amount) => {
        bridged.push([asset, amount]);
        if (asset === "stake") {
          wallet.stake -= amount;
          wallet.eth -= options.arrival ?? parseEther("0.0001");
        } else wallet.eth -= amount;
      },
      sleep: async () => {},
      ...extra,
    });
  return { wallet, log, bridged, sent, previews, funding, run };
}

describe("fund", () => {
  it("bridges only what this run brought, however much the wallet already held", async () => {
    const r = rig({ eth: parseEther("1"), stake: parseEther("500000") });
    await r.run();
    expect(r.bridged).toEqual([
      ["stake", parseEther("55000")],
      // What arrived, less what the stake's deposit paid for its arrival.
      ["eth", parseEther("0.0009")],
    ]);
    expect(r.wallet).toEqual({ eth: parseEther("1"), stake: parseEther("500000") });
    expect(r.log.at(-1)).toContain("Done.");
  });

  it("leaves a little ETH on Robinhood Chain when the wallet held none", async () => {
    const r = rig();
    await r.run();
    expect(r.bridged.at(-1)).toEqual(["eth", parseEther("0.0009") - PARENT_ETH_KEEP]);
    expect(r.wallet.eth).toBe(PARENT_ETH_KEEP);
  });

  it("never bridges more than the quote, so a deposit from elsewhere stays out of it", async () => {
    const r = rig({ landsEth: parseEther("0.5"), landsStake: parseEther("70000"), arrival: 0n });
    await r.run();
    expect(r.bridged).toEqual([
      ["stake", parseEther("55000")],
      ["eth", parseEther("0.001")],
    ]);
  });

  it("says so when there is no ETH to send on beyond the little it keeps", async () => {
    const r = rig({ landsEth: PARENT_ETH_KEEP, quoteEth: PARENT_ETH_KEEP, arrival: 0n });
    await r.run({ stake: false });
    expect(r.bridged).toEqual([]);
    expect(r.log).toContain("Not enough ETH to send on to BrainChain beyond what stays for gas on Robinhood Chain.");
  });

  it("stops and says what the wallet holds when the increase cannot be established", async () => {
    const r = rig({ eth: parseEther("1"), stake: parseEther("500000"), landsEth: 0n, landsStake: 0n });
    await expect(r.run()).rejects.toThrow(
      `Relay reports the move settled, but the wallet on Robinhood Chain shows no increase, so what this run brought cannot be told from what it held. It holds 1 ETH and 500000 of the stake token, and held 1 ETH and 500000 before. Nothing was bridged. This run already brought 0.0006 ETH and 55000 of the stake token to ${WORKER} on Robinhood Chain; \`brainchain-worker bridge\` moves that on to BrainChain, and running fund again moves more USDC.`,
    );
    expect(r.bridged).toEqual([]);
  });

  it("waits out an RPC that lags Relay's word", async () => {
    const r = rig({ eth: parseEther("1") });
    let reads = 0;
    await r.run({ parentEth: async () => (reads++ < 3 ? parseEther("1") : r.wallet.eth), stake: false });
    expect(r.bridged).toEqual([["eth", parseEther("0.001")]]);
  });

  it("sends nothing when the balances cannot be read first", async () => {
    const r = rig();
    await expect(r.run({ parentEth: async () => Promise.reject(new Error("rpc down")) })).rejects.toThrow("Could not read the worker's balances on Robinhood Chain, so what this run brings could not be told from what it holds: rpc down. Nothing was sent.");
    expect(r.funding.send).not.toHaveBeenCalled();
  });

  it("spends only --gas-usdc without --stake, says where the rest stays, and checks the wallet for that much", async () => {
    const r = rig();
    await r.run({ stake: false, gasUsdc: "1", dry: true });
    expect(r.log[0]).toBe(`From ${OWNER} on Solana: 1 USDC to ETH for gas, for ${WORKER}. The other 19 USDC stays on Solana.`);
    expect(r.previews).toEqual([NATIVE]);
    expect(r.funding.preview).toHaveBeenCalledWith(NATIVE, 1_000_000n, WORKER);
    const poor = rig();
    vi.mocked(poor.funding.usdcBalance).mockResolvedValue(3_000_000n);
    await poor.run({ stake: false, dry: true });
    expect(poor.log[0]).toContain("2 USDC to ETH for gas");
    vi.mocked(poor.funding.usdcBalance).mockResolvedValue(1_000_000n);
    await expect(poor.run({ stake: false, dry: true })).rejects.toThrow("holds 1 USDC, less than 2");
  });

  it("signs the quotes it priced, each once, with no second quote to refuse after the first leg moved", async () => {
    const r = rig();
    await r.run();
    expect(r.funding.preview).toHaveBeenCalledTimes(2);
    expect(r.sent.map((q) => q.requestId)).toEqual(["0xgas", "0xstake"]);
  });

  it("names what moved when the second leg or a bridge fails, and never says nothing was sent", async () => {
    const second = rig();
    vi.mocked(second.funding.send).mockImplementationOnce(async () => "sig-gas").mockRejectedValueOnce(new Error("Solana refused the deposit, so its USDC did not move: blockhash"));
    const failure = await second.run().catch((error: Error) => error.message);
    expect(failure).toBe(`Solana refused the deposit, so its USDC did not move: blockhash. This run already brought 0.0006 ETH to ${WORKER} on Robinhood Chain; \`brainchain-worker bridge\` moves that on to BrainChain, and running fund again moves more USDC.`);
    expect(second.bridged).toEqual([]);

    const bridge = rig();
    await expect(bridge.run({ bridgeOn: async () => Promise.reject(new Error("holds too little ETH")) })).rejects.toThrow(`holds too little ETH. This run already brought 0.0006 ETH and 55000 of the stake token to ${WORKER}`);

    const first = rig();
    vi.mocked(first.funding.send).mockRejectedValueOnce(new Error("Relay reports a refund"));
    await expect(first.run()).rejects.toThrow(/^Relay reports a refund$/);
  });

  it("keeps the stake's bridge out of what it names once it has gone", async () => {
    const r = rig({ eth: parseEther("1") });
    let reads = 0;
    const parentEth = async () => {
      if (reads++ === 2) throw new Error("rpc down");
      return r.wallet.eth;
    };
    await expect(r.run({ parentEth })).rejects.toThrow(`rpc down. This run already brought 0.0006 ETH to ${WORKER} on Robinhood Chain`);
    expect(r.bridged.map(([asset]) => asset)).toEqual(["stake"]);
  });
});

describe("unsettled", () => {
  it("says a refund only when Relay reports one, and asks for a check before another run otherwise", () => {
    expect(unsettled("success", "0xreq", "sig", OWNER)).toBeUndefined();
    expect(unsettled("refund", "0xreq", "sig", OWNER)).toBe(`Relay reports a refund for request 0xreq: the USDC of Solana transaction sig goes back to ${OWNER}. Check the wallet before running fund again.`);
    for (const status of ["failure", "pending"] as const) {
      const line = unsettled(status, "0xreq", "sig", OWNER)!;
      expect(line).toBe(`Relay has not settled request 0xreq (it reports "${status}"). The USDC left the wallet in Solana transaction sig. Check https://api.relay.link/intents/status/v2?requestId=0xreq before running fund again: another run moves USDC again.`);
      expect(line).not.toContain("refund");
      expect(line).not.toContain("Nothing was sent");
    }
  });
});

describe("sendSvmStep", () => {
  const connection = (overrides: Partial<Record<keyof Connection, unknown>> = {}) =>
    ({
      getAddressLookupTable: vi.fn(async () => ({ value: null })),
      getLatestBlockhash: vi.fn(async () => ({ blockhash: "GHtXQBsoZHVnNFa9YevAzFr17DJjgHXk3ycTKD5xD3Zi", lastValidBlockHeight: 100 })),
      sendTransaction: vi.fn(async () => "ignored"),
      confirmTransaction: vi.fn(async () => ({ value: { err: null } })),
      ...overrides,
    }) as unknown as Connection;

  it("signs the checked instruction with the agent's key and returns the transaction's id", async () => {
    const c = connection();
    const signature = await sendSvmStep(c, SIGNER, deposit(2_000_000n));
    const sent = vi.mocked(c.sendTransaction).mock.calls[0]![0] as VersionedTransaction;
    expect(bs58.encode(sent.signatures[0]!)).toBe(signature);
    expect(sent.message.compiledInstructions).toHaveLength(1);
    expect(sent.message.staticAccountKeys[sent.message.compiledInstructions[0]!.programIdIndex]!.toBase58()).toBe(RELAY_DEPOSITORY);
  });

  it("says the USDC did not move only when Solana refused the send or the transaction failed", async () => {
    const refused = new SendTransactionError({ action: "send", signature: "s", transactionMessage: "Blockhash not found", logs: [] });
    await expect(sendSvmStep(connection({ sendTransaction: vi.fn(async () => Promise.reject(refused)) }), SIGNER, deposit(1n))).rejects.toThrow("Solana refused the deposit, so its USDC did not move");
    await expect(sendSvmStep(connection({ confirmTransaction: vi.fn(async () => ({ value: { err: { InstructionError: [0, "Custom"] } } })) }), SIGNER, deposit(1n))).rejects.toThrow(/failed, so its USDC did not move: \{"InstructionError"/);
  });

  it("says to check before another run when it cannot tell", async () => {
    const lost = connection({ confirmTransaction: vi.fn(async () => Promise.reject(new Error("socket hang up"))) });
    const failure = await sendSvmStep(lost, SIGNER, deposit(1n)).catch((error: Error) => error.message);
    expect(failure).toMatch(/^the Solana transaction \w+ could not be confirmed \(socket hang up\)\. Check it before running fund again: if it landed, its USDC left the wallet, and another run moves USDC again\.$/);
    expect(failure).not.toContain("did not move");
    const timeout = connection({ sendTransaction: vi.fn(async () => Promise.reject(new Error("fetch failed"))) });
    await expect(sendSvmStep(timeout, SIGNER, deposit(1n))).rejects.toThrow("could not be confirmed (fetch failed)");
  });
});

describe("solanaKeypair", () => {
  const file = (text: string) => {
    const path = join(mkdtempSync(join(tmpdir(), "brainchain-solana-")), "id.json");
    writeFileSync(path, text);
    return path;
  };

  it("reads a key or a keypair file, expanding the home folder as the worker's key file does", () => {
    const secret = JSON.stringify([...SIGNER.secretKey]);
    expect(solanaKeypair({ BRAINCHAIN_SOLANA_KEY: bs58.encode(SIGNER.secretKey) }).publicKey.toBase58()).toBe(OWNER);
    expect(solanaKeypair({ BRAINCHAIN_SOLANA_KEY_FILE: file(secret) }).publicKey.toBase58()).toBe(OWNER);
    vi.stubEnv("HOME", join(file(secret), ".."));
    try {
      expect(solanaKeypair({ BRAINCHAIN_SOLANA_KEY_FILE: "~/id.json" }).publicKey.toBase58()).toBe(OWNER);
    } finally {
      vi.unstubAllEnvs();
    }
  });

  it("refuses two sources, since the wrong wallet would pay, and says which file it could not read", () => {
    const path = file(JSON.stringify([...SIGNER.secretKey]));
    expect(() => solanaKeypair({ BRAINCHAIN_SOLANA_KEY: "x", BRAINCHAIN_SOLANA_KEY_FILE: path })).toThrow("not both");
    expect(() => solanaKeypair({ BRAINCHAIN_SOLANA_KEY_FILE: `${path}.absent` })).toThrow(`names ${path}.absent, which could not be read (ENOENT)`);
  });
});
