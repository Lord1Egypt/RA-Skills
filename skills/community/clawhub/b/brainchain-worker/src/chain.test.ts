import { createServer, type IncomingMessage, type ServerResponse } from "node:http";
import type { AddressInfo } from "node:net";

import { afterAll, beforeAll, describe, expect, it, vi } from "vitest";
import {
  BaseError,
  ContractFunctionExecutionError,
  encodeEventTopics,
  encodeFunctionResult,
  InsufficientFundsError,
  ContractFunctionRevertedError,
  createPublicClient,
  encodeErrorResult,
  http,
  HttpRequestError,
  keccak256,
  toBytes,
  toFunctionSelector,
} from "viem";
import { privateKeyToAccount } from "viem/accounts";

import { taskBoardAbi, workerStakingAbi } from "./abi.js";
import { appealAbi, createChain, erc20Abi, faucetReopens, fetchBrief, PermanentError, reason, requireChainId, resultMessage, Status, submitFailure, unhealthy, workerId } from "./chain.js";
import { resolveNetwork, TESTNET } from "./network.js";
import { flightLine } from "./standing.js";

const brief = JSON.stringify({ title: "Haiku", brief: "Write a haiku about rollups", levels: ["Great", "Fine", "Poor"], passIndex: 1 });
const briefHash = keccak256(toBytes(brief));
const dataURI = `data:application/json;base64,${Buffer.from(brief).toString("base64")}`;

function reverted(abi: typeof taskBoardAbi | typeof workerStakingAbi | typeof erc20Abi, errorName: string, functionName: string, args?: unknown[]) {
  const data = encodeErrorResult({ abi, errorName, args } as Parameters<typeof encodeErrorResult>[0]);
  const revert = new ContractFunctionRevertedError({ abi, data, functionName });
  return new ContractFunctionExecutionError(revert, { abi, functionName, args: [] });
}

describe("fetchBrief", () => {
  it("checks a brief against its hash", async () => {
    expect(await fetchBrief(dataURI, briefHash)).toBe(brief);
    await expect(fetchBrief(dataURI, keccak256(toBytes("other")))).rejects.toThrow(PermanentError);
    await expect(fetchBrief("http://example.com/brief.json", briefHash)).rejects.toThrow("neither");
  });

  it("fetches only from public hosts", async () => {
    const fetcher = vi.fn<typeof fetch>();
    for (const host of ["127.0.0.1", "2130706433", "[::1]", "localhost", "api.localhost", "printer.local", "metadata.google.internal", "intranet"]) {
      await expect(fetchBrief(`https://${host}/brief.json`, briefHash, fetcher)).rejects.toThrow("not a public host");
    }
    expect(fetcher).not.toHaveBeenCalled();
    const ok = vi.fn<typeof fetch>(async () => new Response(brief));
    expect(await fetchBrief("https://briefs.example.com/1.json", briefHash, ok)).toBe(brief);
  });

  it("stops reading a brief past 256 KB", async () => {
    let pulled = 0;
    const endless = new ReadableStream<Uint8Array>({
      pull(controller) {
        pulled += 1;
        controller.enqueue(new Uint8Array(64 * 1024));
      },
    });
    await expect(fetchBrief("https://briefs.example.com/big.json", briefHash, async () => new Response(endless))).rejects.toThrow("larger than 256 KB");
    expect(pulled).toBeLessThan(10);
  });
});

describe("chain helpers", () => {
  it("derives the staking id", () => {
    expect(workerId("0x00000000000000000000000000000000000000C1")).toBe(`0x${"0".repeat(62)}c1`);
  });

  it("signs a result upload with the v2 message", () => {
    const hash = `0x${"ab".repeat(32)}` as const;
    expect(resultMessage(274630, "0xC74564F100e70F95346A6e399ebf1Ce14309C8B6", 7n, hash)).toBe(
      `BrainChain result v2\nchain 274630\nboard 0xc74564f100e70f95346a6e399ebf1ce14309c8b6\ntask 7\nhash ${hash}`,
    );
  });

  it("makes a submit that can never succeed permanent", () => {
    expect(submitFailure(reverted(taskBoardAbi, "TooLate", "submit"))).toEqual(new PermanentError("The deadline passed before the result could be submitted"));
    expect(submitFailure(reverted(taskBoardAbi, "BadStatus", "submit"))).toBeInstanceOf(PermanentError);
    const other = reverted(taskBoardAbi, "NotWorker", "submit");
    expect(submitFailure(other)).toBe(other);
  });

  it("names the contract error a call reverted with, in words where it has some", () => {
    expect(reason(reverted(workerStakingAbi, "Locked", "withdraw"))).toBe('The contract function "withdraw" reverted: the stake is still locked (Locked)');
    expect(reason(reverted(workerStakingAbi, "NotHeld", "withdraw"))).toBe('The contract function "withdraw" reverted. (NotHeld)');
  });

  it("reads when the faucet opens again from its TooSoon revert", () => {
    expect(faucetReopens(reverted(erc20Abi, "TooSoon", "faucet", [1_793_462_553n]))).toBe(1_793_462_553n);
    expect(faucetReopens(reverted(workerStakingAbi, "Locked", "withdraw"))).toBeUndefined();
    expect(faucetReopens(new Error("fetch failed"))).toBeUndefined();
  });

  it("names the RPC by host only", () => {
    const error = new HttpRequestError({ url: "https://rpc.example.com/v2/secret-api-key", details: "fetch failed" });
    expect(reason(error)).toBe("Could not reach rpc.example.com (fetch failed)");
    expect(reason(new BaseError("Request failed", { cause: error }))).not.toContain("secret-api-key");
  });

  it("refuses an RPC URL that does not parse without printing it", () => {
    for (const rpc of ["rpc.example.com/v2/APIKEYSECRET123", "https//rpc.example.com/v2/APIKEYSECRET123", "rpc.example.com:8545/APIKEYSECRET123"]) {
      expect(() => resolveNetwork({ BRAINCHAIN_RPC_URL: rpc })).toThrow("BRAINCHAIN_RPC_URL is not a valid URL");
      expect(() => resolveNetwork({ BRAINCHAIN_RPC_URL: rpc })).not.toThrow("APIKEYSECRET123");
    }
    expect(resolveNetwork({ BRAINCHAIN_RPC_URL: "https://rpc.example.com/v2/key\n" }).rpc).toBe("https://rpc.example.com/v2/key");
    expect(resolveNetwork({ BRAINCHAIN_RPC_URL: " \n", BRAINCHAIN_SERVICE_URL: " " })).toMatchObject({ rpc: TESTNET.rpc, service: TESTNET.service });
  });

  it("says the RPC answered when it did, and cuts the answer to one short line", () => {
    const line = reason(new HttpRequestError({ url: "https://rpc.example.com/v2/APIKEYSECRET123", details: JSON.stringify(`gateway\ttimeout ${"x".repeat(300)}`), status: 504 }));
    expect(line).toMatch(/^rpc\.example\.com answered 504 \(gateway timeout x+…\)$/);
    expect(line.length).toBe("rpc.example.com answered 504 ()".length + 160);
    expect(line).not.toMatch(/[\x00-\x1f]/);
    expect(line).not.toContain("APIKEYSECRET123");
  });

  it("takes a BrainChain service over https only, or http on this machine", () => {
    expect(resolveNetwork({ BRAINCHAIN_SERVICE_URL: "https://brain.example.com/" }).service).toBe("https://brain.example.com");
    expect(resolveNetwork({ BRAINCHAIN_SERVICE_URL: "http://127.0.0.1:3000" }).service).toBe("http://127.0.0.1:3000");
    expect(resolveNetwork({ BRAINCHAIN_SERVICE_URL: "http://localhost:3000" }).service).toBe("http://localhost:3000");
    expect(() => resolveNetwork({ BRAINCHAIN_SERVICE_URL: "http://brain.example.com" })).toThrow("https");
  });

  it("names the service's host when it fails its health check, and tells a late service from a down one", async () => {
    const service = "https://brain.example.com/v1";
    const ok = vi.fn<typeof fetch>(async () => new Response('{"ok":true}'));
    expect(await unhealthy(service, ok)).toBeUndefined();
    expect(ok.mock.calls[0]![0]).toBe("https://brain.example.com/v1/health");
    expect(await unhealthy(service, async () => new Response('{"ok":false}', { status: 503 }))).toBe(
      "the BrainChain service at brain.example.com reports it is behind (503); results still upload, and grading may be late",
    );
    expect(await unhealthy(service, async () => new Response("bad gateway", { status: 502 }))).toBe(
      "the BrainChain service at brain.example.com answered its health check with 502; results are uploaded there, so delivery can fail until it recovers",
    );
    expect(
      await unhealthy("http://localhost:1", async () => {
        throw new TypeError("fetch failed");
      }),
    ).toBe("could not reach the BrainChain service at localhost:1; results are uploaded there, so none can be delivered until it answers");
  });
});

describe("a wallet short of gas", () => {
  const plain = "The wallet holds too little ETH to pay for this transaction's gas, so it was not sent. `brainchain-worker status` shows what it holds";

  it("is said plainly, in the words of either failure", () => {
    const estimate = new BaseError("Execution reverted with reason: gas required exceeds allowance (38928).");
    expect(reason(estimate)).toBe(plain);
    const send = new BaseError("The total cost (gas * gas fee + value) of executing this transaction exceeds the balance of the account.", { cause: new InsufficientFundsError() });
    expect(reason(send)).toBe(plain);
  });

  it("is not confused with a token's own allowance", () => {
    expect(reason(new BaseError("ERC20: transfer amount exceeds allowance"))).toBe("ERC20: transfer amount exceeds allowance");
  });
});

describe("requireChainId", () => {
  it("refuses an RPC serving another chain, and leaves one that does not answer to the commands", async () => {
    await expect(requireChainId(TESTNET, async () => 46_630)).rejects.toThrow("BRAINCHAIN_RPC_URL serves chain 46630; BrainChain testnet is chain 274630.");
    await expect(requireChainId(TESTNET, async () => 274_630)).resolves.toBeUndefined();
    await expect(
      requireChainId(TESTNET, async () => {
        throw new Error("no answer");
      }),
    ).resolves.toBeUndefined();
  });
});

type RpcRequest = { id: number; method: string; params: [{ topics?: unknown[]; data?: string } | string, ...unknown[]] };

/** A JSON-RPC server on this machine that answers each request with `answer`, or with its error when it returns one. */
async function mockRpc(answer: (request: RpcRequest) => unknown) {
  const reply = (request: RpcRequest) => {
    const result = answer(request);
    return result instanceof Error
      ? { jsonrpc: "2.0", id: request.id, error: { code: 3, message: result.message, data: (result as Error & { data?: string }).data } }
      : { jsonrpc: "2.0", id: request.id, result };
  };
  const server = createServer((req, res) => {
    let body = "";
    req.on("data", (chunk) => (body += chunk));
    req.on("end", () => {
      const request = JSON.parse(body) as RpcRequest | RpcRequest[];
      res.setHeader("content-type", "application/json");
      res.end(JSON.stringify(Array.isArray(request) ? request.map(reply) : reply(request)));
    });
  });
  await new Promise<void>((resolve) => server.listen(0, "127.0.0.1", resolve));
  return { url: `http://127.0.0.1:${(server.address() as AddressInfo).port}`, close: () => server.close() };
}

const ZERO = `0x${"0".repeat(64)}` as const;
const word = (n: bigint | number) => `0x${n.toString(16).padStart(64, "0")}`;
const topicOf = (request: RpcRequest) => {
  const first = (request.params[0] as { topics?: unknown[] }).topics?.[0];
  return Array.isArray(first) ? first[0] : first;
};
const rpcLog = (address: string, topics: string[], data = "0x", blockNumber = "0x900") => ({
  address,
  topics,
  data,
  blockNumber,
  transactionHash: `0x${"77".repeat(32)}`,
  logIndex: "0x0",
  blockHash: ZERO,
  transactionIndex: "0x0",
  removed: false,
});

describe("record", () => {
  it("counts a ruled or appealed task as in flight, since the stake can still be at risk, and says what each waits for", async () => {
    const account = privateKeyToAccount(`0x${"4f".repeat(32)}`);
    const id = workerId(account.address);
    const hired = encodeEventTopics({ abi: taskBoardAbi, eventName: "WorkerHired" })[0];
    let status: number = Status.Ruled;
    const rpc = await mockRpc((request) => {
      if (request.method === "eth_chainId") return "0x430c6";
      if (request.method === "eth_blockNumber") return "0x1000";
      if (request.method === "eth_getLogs") return topicOf(request) === hired ? [rpcLog(TESTNET.contracts.taskBoard, [hired, word(1), id, word(1)])] : [];
      if (request.method !== "eth_call") return "0x";
      const data = (request.params[0] as { data: string }).data;
      if (data.startsWith(toFunctionSelector("appealOf(uint256)"))) {
        const appeal = { window: 3600n, bondBps: 2500, ruledAt: 100n, pays: false, confident: false, appellant: account.address, bond: 250_000n, appealedAt: 200n };
        return encodeFunctionResult({ abi: appealAbi, functionName: "appealOf", result: appeal });
      }
      const task = {
        poster: account.address,
        bounty: 1_000_000n,
        deadline: 2_000_000_000n,
        status,
        accepted: false,
        disputed: true,
        disputedByModel: true,
        model: id,
        briefHash: ZERO,
        resultHash: ZERO,
        submittedAt: 1n,
        gradedAt: 2n,
        disputedAt: 3n,
        postedAt: 1n,
        payee: account.address,
        feeRecipient: account.address,
        feeBps: 300,
        hireThresholdBps: 1500,
        gradeThresholdBps: 8000,
        ruleThresholdBps: 8000,
        gradeWindow: 3600n,
        disputeWindow: 3600n,
        ruleWindow: 21600n,
      };
      return encodeFunctionResult({ abi: taskBoardAbi, functionName: "get", result: task });
    });
    try {
      const chain = createChain({ ...TESTNET, rpc: rpc.url }, account);
      const lines: string[] = [];
      for (const each of [Status.Ruled, Status.Appealed, Status.Hired, Status.Disputed]) {
        status = each;
        const { inFlight } = await chain.record();
        expect(inFlight).toHaveLength(1);
        lines.push(flightLine(inFlight[0]!));
      }
      expect(lines).toEqual([
        "task 1: the ruling refunds the poster after 1970-01-01T01:01:40Z unless appealed with `appeal 1`",
        "task 1: ruling appealed, Jev rules again by 1970-01-01T06:03:20Z",
        "task 1: hired, due by 2033-05-18T03:33:20Z",
        "task 1: grade disputed by this worker, Jev rules by 1970-01-01T06:00:03Z",
      ]);
      status = Status.Paid;
      expect(await chain.record()).toMatchObject({ paid: 1, inFlight: [] });
    } finally {
      rpc.close();
    }
  });
});

describe("settlement", () => {
  const account = privateKeyToAccount(`0x${"4f".repeat(32)}`);
  const id = workerId(account.address);
  const [paidTopic] = encodeEventTopics({ abi: taskBoardAbi, eventName: "BountyPaid" });
  const [refundedTopic] = encodeEventTopics({ abi: taskBoardAbi, eventName: "BountyRefunded" });
  const [slashedTopic] = encodeEventTopics({ abi: workerStakingAbi, eventName: "Slashed" });

  async function settled(status: number) {
    const refund = rpcLog(TESTNET.contracts.taskBoard, [refundedTopic, word(45), word(BigInt(account.address))], word(1_000_000) + word(3).slice(2));
    const rpc = await mockRpc((request) => {
      if (request.method === "eth_blockNumber") return "0x1000";
      if (request.method === "eth_call") {
        const task = { poster: account.address, bounty: 1_000_000n, deadline: 0n, status, accepted: false, disputed: false, disputedByModel: false, model: id, briefHash: ZERO, resultHash: ZERO, submittedAt: 0n, gradedAt: 0n, disputedAt: 0n, postedAt: 0n, payee: account.address, feeRecipient: account.address, feeBps: 250, hireThresholdBps: 0, gradeThresholdBps: 0, ruleThresholdBps: 0, gradeWindow: 0n, disputeWindow: 0n, ruleWindow: 0n };
        return encodeFunctionResult({ abi: taskBoardAbi, functionName: "get", result: task });
      }
      if (request.method === "eth_getLogs") {
        const topic = topicOf(request);
        if (topic === paidTopic) return [rpcLog(TESTNET.contracts.taskBoard, [paidTopic, word(45), id, word(BigInt(account.address))], word(1_000_000) + word(25_000).slice(2))];
        if (topic === refundedTopic) return [refund];
        return [];
      }
      if (request.method === "eth_getBlockByNumber") return { number: "0x900", hash: ZERO, parentHash: ZERO, timestamp: "0x6909d7c2", transactions: [], logsBloom: null, nonce: null };
      if (request.method === "eth_getTransactionReceipt") {
        const slash = (who: string, amount: bigint, contract = TESTNET.contracts.staking) => rpcLog(contract, [slashedTopic, word(BigInt(who))], word(amount));
        const logs = [
          refund,
          slash(account.address, 100n * 10n ** 18n),
          slash("0x00000000000000000000000000000000000000d1", 7n),
          slash(account.address, 9n, "0x00000000000000000000000000000000000000e1"),
        ];
        return { transactionHash: `0x${"77".repeat(32)}`, blockHash: ZERO, blockNumber: "0x900", status: "0x1", logs, from: account.address, to: TESTNET.contracts.taskBoard, gasUsed: "0x1", cumulativeGasUsed: "0x1", effectiveGasPrice: "0x1", transactionIndex: "0x0", type: "0x2", logsBloom: `0x${"0".repeat(512)}`, contractAddress: null };
      }
      return "0x";
    });
    try {
      return await createChain({ ...TESTNET, rpc: rpc.url }, account).settlement(45n);
    } finally {
      rpc.close();
    }
  }

  it("reads what a paid task paid after fees, and when", async () => {
    expect(await settled(Status.Paid)).toEqual({ paid: true, amount: 975_000n, at: 0x6909d7c2n });
  });

  it("reads why a task was refunded, and the stake slashed from this worker in the same transaction", async () => {
    expect(await settled(Status.Refunded)).toEqual({ paid: false, reason: 3, slashed: 100n * 10n ** 18n });
  });

  it("is undefined while the task has not settled", async () => {
    expect(await settled(Status.Ruled)).toBeUndefined();
  });
});

describe("a send the gas cap made revert", () => {
  it("is read as a wallet short of gas when the same call passes without the cap, and keeps its own error when it does not", async () => {
    const account = privateKeyToAccount(`0x${"4f".repeat(32)}`);
    let callPasses = true;
    const failedInnerCall = toFunctionSelector("FailedInnerCall()");
    const rpc = await mockRpc((request) => {
      switch (request.method) {
        case "eth_chainId":
          return "0x430c6";
        case "eth_getTransactionCount":
          return "0x1";
        case "eth_getBlockByNumber":
          return { number: "0x900", hash: ZERO, parentHash: ZERO, timestamp: "0x1", baseFeePerGas: "0x5f5e100", transactions: [], logsBloom: null, nonce: null };
        case "eth_maxPriorityFeePerGas":
          return "0x0";
        case "eth_estimateGas":
          return Object.assign(new Error("execution reverted"), { data: failedInnerCall });
        case "eth_call":
          return callPasses ? "0x" : Object.assign(new Error("execution reverted"), { data: failedInnerCall });
        default:
          return "0x";
      }
    });
    try {
      const chain = createChain({ ...TESTNET, rpc: rpc.url }, account);
      expect(reason(await chain.withdraw().catch((error: unknown) => error))).toBe(
        "The wallet holds too little ETH to pay for this transaction's gas, so it was not sent. `brainchain-worker status` shows what it holds",
      );
      callPasses = false;
      expect(reason(await chain.withdraw().catch((error: unknown) => error))).toBe(
        'The contract function "withdraw" reverted: a token transfer inside the call failed without a reason (FailedInnerCall)',
      );
    } finally {
      rpc.close();
    }
  });
});

describe("answers from a real server", () => {
  const page = (title: string) => `<!doctype html>\n<html lang="en">\n\t<head><title>${title}</title></head>\x07\n${"<p>filler</p>\n".repeat(80)}</html>`;
  const json = (status: number, body: unknown) => (res: ServerResponse) => {
    res.writeHead(status, { "content-type": "application/json" });
    res.end(JSON.stringify(body));
  };
  const html = (status: number) => (res: ServerResponse) => {
    res.writeHead(status, { "content-type": "text/html" });
    res.end(page(`${status}`));
  };
  const routes: Record<string, (res: ServerResponse, req: IncomingMessage) => void> = {
    "/page200": html(200),
    "/page404": html(404),
    "/page502": html(502),
    "/page429": html(429),
    "/echo": (res, req) => {
      res.writeHead(404, { "content-type": "text/plain" });
      res.end(`Cannot POST ${req.url}`);
    },
    "/auth": json(401, { jsonrpc: "2.0", id: 1, error: { code: -32600, message: "Must be authenticated!" } }),
    "/limit": json(429, { jsonrpc: "2.0", id: 1, error: { code: 429, message: "Your app has exceeded its compute units per second capacity" } }),
    "/rest": (res, req) => json(200, { args: {}, headers: { Authorization: req.headers.authorization }, url: `http://rest.example${req.url}` })(res),
    "/missing": json(200, { error: "Not Found" }),
    "/rpc": json(200, { jsonrpc: "2.0", id: 1, result: "0x10" }),
    "/nodeerror": json(200, { jsonrpc: "2.0", id: 1, error: { code: -32000, message: "the node says this is wrong" } }),
    "/headersback": (res, req) => {
      res.writeHead(500, { "content-type": "text/plain" });
      res.end(`upstream refused auth=${req.headers.authorization ?? ""} raw=${Buffer.from((req.headers.authorization ?? "").replace("Basic ", ""), "base64").toString().split(":")[1] ?? ""}`);
    },
    "/results/html403": html(403),
    "/results/refused": json(403, { error: "Only the hired worker can upload a result" }),
  };
  const server = createServer((req, res) => {
    const route = Object.keys(routes).find((path) => req.url!.startsWith(path));
    req.resume();
    req.on("end", () => routes[route!]!(res, req));
  });
  let host = "";

  beforeAll(async () => {
    await new Promise<void>((resolve) => server.listen(0, "127.0.0.1", resolve));
    host = `127.0.0.1:${(server.address() as AddressInfo).port}`;
  });
  afterAll(() => {
    server.close();
    server.closeAllConnections();
  });

  const rpc = async (path: string) => {
    const client = createPublicClient({ transport: http(`http://${host}${path}`, { retryCount: 0 }) });
    return reason(await client.getBlockNumber().catch((error: unknown) => error));
  };

  it("says a web page that answered 200, 404 or 405 is not an RPC", async () => {
    expect(await rpc("/page200/APIKEYSECRET123")).toBe(`${host} answered, but not as an RPC`);
    expect(await rpc("/page404/APIKEYSECRET123")).toBe(`${host} answered 404 with a web page, not as an RPC`);
  });

  it("names the host when JSON that is no RPC reply answers 200, without the URL's path or credentials", async () => {
    const account = privateKeyToAccount(`0x${"4f".repeat(32)}`);
    const now = (path: string) => createChain({ ...TESTNET, rpc: `http://${host}${path}` }, account).now().catch((error: unknown) => reason(error));
    expect(await now("/rest/APIKEYSECRET123")).toBe(`${host} answered, but not as an RPC ({"args":{},"headers":{},"url":"http://rest.example…"})`);
    const echoed = await createChain({ ...TESTNET, rpc: `http://user:PASSWORDSECRET9@${host}/rest` }, account).now().catch((error: unknown) => reason(error));
    expect(echoed).toBe(`${host} answered, but not as an RPC ({"args":{},"headers":{"Authorization":"Basic …"},"url":"http://rest.example/rest"})`);
    expect(await now("/missing")).toBe(`${host} answered, but not as an RPC ({"error":"Not Found"})`);
    expect(await createChain({ ...TESTNET, rpc: `http://${host}/rpc` }, account).ethBalance()).toBe(16n);
  });

  it("keeps the status of an error page from a proxy in front of the RPC", async () => {
    expect(await rpc("/page502/APIKEYSECRET123")).toBe(`${host} answered 502 with a web page`);
    expect(await rpc("/page429")).toBe(`${host} answered 429 with a web page`);
  });

  it("names the host, the status and the provider's message when it refuses the request", async () => {
    expect(await rpc("/auth/APIKEYSECRET123")).toBe(`${host} answered 401 (Must be authenticated!)`);
    expect(await rpc("/limit")).toBe(`${host} answered 429 (Your app has exceeded its compute units per second capacity)`);
  });

  it("never prints the URL's path when an answer echoes it", async () => {
    const line = await rpc("/echo/v2/APIKEYSECRET123?key=QUERYSECRET456");
    expect(line).toBe(`${host} answered 404 (Cannot POST …)`);
    expect(await rpc("/echo/APIKEYSECRET123")).not.toContain("APIKEYSECRET123");
  });

  describe("an RPC URL that holds a credential", () => {
    const secretUrl = (path: string) => `http://user:PASSWORDSECRET9@${host}${path}`;
    const withEnv = async (url: string) => {
      vi.stubEnv("BRAINCHAIN_RPC_URL", url);
      try {
        const client = createPublicClient({ transport: http(url, { retryCount: 0 }) });
        return reason(await client.getBlockNumber().catch((error: unknown) => error));
      } finally {
        vi.unstubAllEnvs();
      }
    };

    it("prints none of a non-2xx answer, which can echo the credential in any form", async () => {
      expect(await withEnv(secretUrl("/headersback/v1/APIKEYSECRET123?k=QUERYSECRET456"))).toBe(`${host} answered 500`);
      expect(await withEnv(`http://${host}/headersback/APIKEYSECRET123`)).toBe(`${host} answered 500`);
    });

    it("still says when the answer was a web page", async () => {
      expect(await withEnv(secretUrl("/page502/x"))).toBe(`${host} answered 502 with a web page`);
    });

    it("strips an echoed Authorization value wherever the answer is printed", async () => {
      const client = createPublicClient({ transport: http(secretUrl("/headersback"), { retryCount: 0 }) });
      const line = reason(await client.getBlockNumber().catch((error: unknown) => error));
      expect(line).toContain("auth=Basic …");
      expect(line).not.toContain(btoa("user:PASSWORDSECRET9"));
    });

    it("gives no part of a JSON-RPC error's text, and the RPC's own words when the URL holds nothing", async () => {
      expect(await withEnv(secretUrl("/nodeerror"))).toBe(`${host} refused the request (JSON-RPC error -32000)`);
      expect(await rpc("/nodeerror")).toBe(`${host} refused the request: the node says this is wrong`);
    });
  });

  it("gives up on a result only when the service itself refuses it", async () => {
    const network = { ...TESTNET, service: `http://${host}/results/html403` };
    const account = privateKeyToAccount(`0x${"4f".repeat(32)}`);
    const edge = createChain(network, account).publish(7n, "work");
    await expect(edge).rejects.toThrow("Uploading the result failed (403): no reason given");
    await expect(edge).rejects.not.toBeInstanceOf(PermanentError);
    const refused = createChain({ ...network, service: `http://${host}/results/refused` }, account).publish(7n, "work");
    await expect(refused).rejects.toThrow(new PermanentError("The service refused the result (403): Only the hired worker can upload a result"));
    await expect(refused).rejects.toBeInstanceOf(PermanentError);
  });
});
