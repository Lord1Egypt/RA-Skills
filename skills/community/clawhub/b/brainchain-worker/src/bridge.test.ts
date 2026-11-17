import { createServer } from "node:http";
import type { AddressInfo } from "node:net";

import { decodeAbiParameters, decodeFunctionData, encodeAbiParameters, parseAbi, parseEther, parseTransaction, parseUnits, toFunctionSelector, type Address, type Hex } from "viem";
import { privateKeyToAccount } from "viem/accounts";
import { describe, expect, it, vi } from "vitest";

import { bridge, createBridgeChain, type Asset, type BridgeChain } from "./bridge.js";
import { MAINNET, TESTNET } from "./network.js";

const ACCOUNT: Address = "0x00000000000000000000000000000000000000C1";
const TX: Hex = `0x${"fe".repeat(32)}`;

function fakeChain(options: { eth?: bigint; stake?: bigint; bounty?: bigint; cost?: bigint } = {}) {
  const sent: string[] = [];
  const chain: BridgeChain = {
    account: ACCOUNT,
    parentEth: vi.fn(async () => options.eth ?? parseEther("0.01")),
    tokenBalance: vi.fn(async (asset: Exclude<Asset, "eth">) => (asset === "stake" ? (options.stake ?? parseEther("2000000")) : (options.bounty ?? parseUnits("50", 6)))),
    arrivalCost: vi.fn(async () => options.cost ?? parseEther("0.0003")),
    depositEth: vi.fn(async (amount: bigint) => {
      sent.push(`eth ${amount}`);
      return TX;
    }),
    depositToken: vi.fn(async (asset: Exclude<Asset, "eth">, amount: bigint, value: bigint) => {
      sent.push(`${asset} ${amount} value ${value}`);
      return TX;
    }),
  };
  return { chain, sent };
}

async function run(chain: BridgeChain, asset: Asset, amount: string, dry = false, network = MAINNET) {
  const lines: string[] = [];
  await bridge(network, chain, { asset, amount, dry, log: (line) => lines.push(line) });
  return lines;
}

describe("bridge", () => {
  it("deposits ETH through the inbox and says when it arrives", async () => {
    const { chain, sent } = fakeChain();
    const lines = await run(chain, "eth", "0.001");
    expect(sent).toEqual([`eth ${parseEther("0.001")}`]);
    expect(lines).toEqual([
      `bridging 0.001 ETH from Robinhood Chain to ${ACCOUNT} on BrainChain`,
      `sent, arrives on BrainChain in about a minute: ${TX}`,
    ]);
  });

  it("deposits the stake token with the ETH its arrival costs", async () => {
    const { chain, sent } = fakeChain({ cost: parseEther("0.0003") });
    const lines = await run(chain, "stake", "1250000");
    expect(sent).toEqual([`stake ${parseEther("1250000")} value ${parseEther("0.0003")}`]);
    expect(lines[0]).toBe(`bridging 1,250,000 BRAIN from Robinhood Chain to ${ACCOUNT} on BrainChain (sending 0.0003 ETH for its arrival, the unused part refunded there)`);
  });

  it("takes bounty amounts in 6 decimals and sends nothing on a dry run", async () => {
    const { chain, sent } = fakeChain();
    const lines = await run(chain, "bounty", "12.5", true);
    expect(sent).toEqual([]);
    expect(lines[0]).toContain("bridging 12.5 USDG");
    expect(lines[1]).toBe("dry run: nothing sent");
  });

  it("says exactly what the wallet lacks, and sends nothing", async () => {
    const short = fakeChain({ stake: parseEther("1000") });
    await expect(run(short.chain, "stake", "1250000")).rejects.toThrow(`${ACCOUNT} holds 1,000 BRAIN on Robinhood Chain, 1,249,000 short of 1,250,000 BRAIN`);
    const noGas = fakeChain({ eth: parseEther("0.0001") });
    await expect(run(noGas.chain, "bounty", "1")).rejects.toThrow(/holds 0.0001 ETH on Robinhood Chain; about 0.0004 ETH is needed/);
    await expect(run(noGas.chain, "eth", "0.001")).rejects.toThrow(/0.001 ETH plus gas is needed/);
    expect(short.sent).toEqual([]);
    expect(noGas.sent).toEqual([]);
  });

  it("refuses a token the network mints on BrainChain only", async () => {
    const { chain } = fakeChain();
    await expect(run(chain, "eth", "0.001", true, TESTNET)).resolves.toBeDefined();
    (chain.tokenBalance as ReturnType<typeof vi.fn>).mockRejectedValueOnce(new Error("BrainChain testnet's stake token is not bridged from Robinhood Chain testnet"));
    await expect(run(chain, "stake", "1", false, TESTNET)).rejects.toThrow(/not bridged/);
  });
});

describe("depositToken", () => {
  const account = privateKeyToAccount(`0x${"4f".repeat(32)}`);
  const GATEWAY: Address = "0x00000000000000000000000000000000000000A7";
  const GAS_PRICE = 100_000_000n;
  /** What the deposit's arrival costs on BrainChain at twice GAS_PRICE, for its 300,000 gas. */
  const ARRIVAL = 300_000n * GAS_PRICE * 2n;
  const routerAbi = parseAbi(["function outboundTransferCustomRefund(address token, address refundTo, address to, uint256 amount, uint256 maxGas, uint256 gasPriceBid, bytes data) payable returns (bytes)"]);
  const word = (value: bigint) => encodeAbiParameters([{ type: "uint256" }], [value]);

  /** A deposit against one fake RPC standing in for both chains, with no allowance set; returns what it sent. */
  async function deposit(value: bigint) {
    const raw: Hex[] = [];
    const answer = (method: string, params: unknown[]): unknown => {
      switch (method) {
        case "eth_chainId":
          return `0x${MAINNET.bridge!.chainId.toString(16)}`;
        case "eth_gasPrice":
        case "eth_maxPriorityFeePerGas":
          return `0x${GAS_PRICE.toString(16)}`;
        case "eth_call": {
          const { data } = params[0] as { data: Hex };
          return data.startsWith(toFunctionSelector("getGateway(address)")) ? encodeAbiParameters([{ type: "address" }], [GATEWAY]) : word(0n);
        }
        case "eth_getBlockByNumber":
          return { number: "0x10", hash: TX, parentHash: TX, timestamp: "0x1", baseFeePerGas: "0x5f5e100", transactions: [], logsBloom: null, nonce: null };
        case "eth_getTransactionCount":
          return `0x${raw.length.toString(16)}`;
        case "eth_estimateGas":
          return "0x30000";
        case "eth_blockNumber":
          return "0x10";
        case "eth_sendRawTransaction":
          raw.push((params as Hex[])[0]!);
          return `0x${raw.length.toString(16).padStart(64, "0")}`;
        case "eth_getTransactionReceipt":
          return { status: "0x1", blockNumber: "0x10", blockHash: TX, transactionHash: params[0], transactionIndex: "0x0", from: account.address, to: GATEWAY, cumulativeGasUsed: "0x1", gasUsed: "0x1", effectiveGasPrice: "0x1", logs: [], logsBloom: `0x${"00".repeat(256)}`, type: "0x2", contractAddress: null };
        default:
          return undefined;
      }
    };
    const server = createServer((req, res) => {
      let body = "";
      req.on("data", (chunk) => (body += chunk));
      req.on("end", () => {
        const { id, method, params } = JSON.parse(body) as { id: number; method: string; params: unknown[] };
        res.setHeader("content-type", "application/json");
        const result = answer(method, params);
        res.end(JSON.stringify({ jsonrpc: "2.0", id, ...(result === undefined ? { error: { code: -32601, message: `${method} not found` } } : { result }) }));
      });
    });
    await new Promise<void>((resolve) => server.listen(0, "127.0.0.1", resolve));
    const url = `http://127.0.0.1:${(server.address() as AddressInfo).port}`;
    try {
      const network = { ...MAINNET, rpc: url, bridge: { ...MAINNET.bridge!, rpc: url } };
      const outcome = await createBridgeChain(network, account).depositToken("stake", 5n, value).catch((error: Error) => error);
      return { outcome, raw };
    } finally {
      server.close();
      server.closeAllConnections();
    }
  }

  const moved = "The gas price on BrainChain moved after this deposit was priced, so the ETH set aside no longer pays for its arrival. Nothing was sent. Run the command again.";

  it.each([
    ["no longer covers", ARRIVAL - 1n],
    ["covers only", ARRIVAL],
  ])("sends nothing, not even the approval, when the ETH set aside %s the arrival at the current gas price", async (_, value) => {
    const { outcome, raw } = await deposit(value);
    expect((outcome as Error).message).toBe(moved);
    expect(raw).toEqual([]);
  });

  it("approves and then deposits, the rest of the ETH paying for submission", async () => {
    const submission = 777n;
    const { raw } = await deposit(ARRIVAL + submission);
    expect(raw).toHaveLength(2);
    const sent = parseTransaction(raw[1]!);
    expect(sent.value).toBe(ARRIVAL + submission);
    const { args } = decodeFunctionData({ abi: routerAbi, data: sent.data! });
    expect(args[5]).toBe(GAS_PRICE * 2n);
    expect(decodeAbiParameters([{ type: "uint256" }, { type: "bytes" }], args[6])[0]).toBe(submission);
  });
});
