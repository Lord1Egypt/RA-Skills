/**
 * deposit.js --confirmed simulation tests
 *
 * Spins up a lightweight in-process mock JSON-RPC server that pretends to be
 * Arbitrum One (chainId 42161). No real network calls, no real funds moved.
 *
 * The WDK vault is used for real signing (private key decrypted locally),
 * but the signed transaction is submitted to our mock server which ignores it
 * and returns a deterministic fake txHash + receipt.
 *
 * Coverage:
 *   - Happy path: preview → confirmed → Transfer event verified
 *   - No Transfer event in receipt → script exits 1 with structured error
 *   - tx.wait() RPC error → script exits 1 with txHash preserved in stderr
 *   - Insufficient USDC balance → exits 1
 *   - Zero ETH balance → exits 1
 *   - Wrong chainId → exits 1
 */

import { createServer } from 'http';
import { spawn } from 'child_process';         // async — does NOT block event loop
import { describe, it, expect, beforeAll, afterAll } from 'vitest';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import { AbiCoder, keccak256, toUtf8Bytes, zeroPadValue, getBytes } from 'ethers';

const __dir = dirname(fileURLToPath(import.meta.url));
const DEPOSIT_JS = join(__dir, '..', 'deposit.js');

// ---------------------------------------------------------------------------
// Constants matching deposit.js
// ---------------------------------------------------------------------------
const BRIDGE  = '0x2df1c51e09aecf9cacb7bc98cb1742757f163df7';
const USDC    = '0xaf88d065e77c8cc2239327c5edb3a432268e5831'; // lowercase for log matching
const WALLET  = '0x77dde3ee0fd0fca2f1fc9c3ac9c7af6a573ae61c'; // test wallet (lowercase)

const coder = AbiCoder.defaultAbiCoder();
const TRANSFER_TOPIC = keccak256(toUtf8Bytes('Transfer(address,address,uint256)'));
// No static FAKE_TX_HASH — we compute the real keccak256(rawTx) per test run
const BLOCK_NUM      = '0x1312d00';

// ---------------------------------------------------------------------------
// Mock RPC helpers
// ---------------------------------------------------------------------------

function makeReceipt(amountUSDC6, txHash = '0x' + 'ab'.repeat(32)) {
  return {
    transactionHash:   txHash,
    hash:              txHash,       // ethers v6 alias
    blockHash:         '0x' + 'ff'.repeat(32),
    blockNumber:       BLOCK_NUM,
    status:            '0x1',
    gasUsed:           '0xfe50',
    cumulativeGasUsed: '0xfe50',
    effectiveGasPrice: '0x3b9aca00',
    from:              WALLET,
    to:                USDC,
    type:              '0x2',
    transactionIndex:  '0x0',
    index:             '0x0',        // ethers v6 requires this alias
    logsBloom:         '0x' + '0'.repeat(512),
    contractAddress:   null,
    logs: [{
      address:          USDC,
      topics: [
        TRANSFER_TOPIC,
        zeroPadValue(WALLET, 32),
        zeroPadValue(BRIDGE, 32),
      ],
      data:             '0x' + coder.encode(['uint256'], [BigInt(amountUSDC6)]).slice(2),
      logIndex:         '0x0',
      index:            '0x0',       // ethers v6 requires this alias
      transactionIndex: '0x0',
      transactionHash:  txHash,
      blockHash:        '0x' + 'ff'.repeat(32),
      blockNumber:      BLOCK_NUM,
      removed:          false,
    }],
  };
}

/** Build a mock Arbitrum RPC handler with configurable behaviour. */
function makeHandler({ usdcBalance6 = 100_000_000, ethWei = 10_000_000_000_000_000n, receiptOverride = undefined } = {}) {
  // ethers v6 validates that eth_sendRawTransaction returns keccak256(rawTx).
  // We compute it dynamically and store for eth_getTransactionReceipt lookups.
  let lastTxHash = null;

  return function handle(method, params) {
    switch (method) {
      case 'eth_chainId':              return '0xa4b1';  // 42161
      case 'net_version':              return '42161';
      case 'eth_blockNumber':          return BLOCK_NUM;
      case 'eth_getBalance':           return '0x' + ethWei.toString(16);
      case 'eth_getTransactionCount':  return '0x0';
      case 'eth_gasPrice':             return '0x3b9aca00';
      case 'eth_maxPriorityFeePerGas': return '0x3b9aca00';
      case 'eth_estimateGas':          return '0x186a0';
      case 'eth_feeHistory': return {
        baseFeePerGas: ['0x5f5e100', '0x5f5e100'],
        gasUsedRatio:  [0.5],
        oldestBlock:   '0x1312cff',
        reward:        [['0x3b9aca00']],
      };
      case 'eth_getBlockByNumber': return {
        baseFeePerGas: '0x5f5e100',
        number:        BLOCK_NUM,
        hash:          '0x' + 'ee'.repeat(32),
        parentHash:    '0x' + 'dd'.repeat(32),
        timestamp:     '0x67f7b000',
        transactions:  [],
        gasLimit:      '0x1c9c380',
        gasUsed:       '0x0',
        miner:         '0x' + '0'.repeat(40),
        difficulty:    '0x0',
        totalDifficulty: '0x0',
        extraData:     '0x',
        size:          '0x100',
        nonce:         '0x0000000000000000',
        uncles:        [],
        sha3Uncles:    '0x' + '0'.repeat(64),
        stateRoot:     '0x' + '0'.repeat(64),
        transactionsRoot: '0x' + '0'.repeat(64),
        receiptsRoot:  '0x' + '0'.repeat(64),
        logsBloom:     '0x' + '0'.repeat(512),
        mixHash:       '0x' + '0'.repeat(64),
      };
      case 'eth_call': {
        const sig = ((params[0]?.data) || '').slice(0, 10).toLowerCase();
        if (sig === '0x313ce567') // decimals()
          return '0x' + coder.encode(['uint8'], [6]).slice(2);
        if (sig === '0x70a08231') // balanceOf(address)
          return '0x' + coder.encode(['uint256'], [BigInt(usdcBalance6)]).slice(2);
        return '0x';
      }
      case 'eth_sendRawTransaction': {
        // Compute the real tx hash so ethers v6 validation passes
        lastTxHash = keccak256(getBytes(params[0]));
        return lastTxHash;
      }
      case 'eth_getTransactionReceipt': {
        const hash = (params[0] || '').toLowerCase();
        if (!lastTxHash || hash !== lastTxHash.toLowerCase()) return null;
        if (receiptOverride !== undefined) {
          // Inject the real txHash so ethers doesn't reject the receipt
          return receiptOverride === null ? null : { ...receiptOverride, transactionHash: lastTxHash };
        }
        return makeReceipt(10_000_000, lastTxHash);
      }
      default:
        return null;
    }
  };
}

/** Start a mock JSON-RPC HTTP server. Returns { url, close }. */
async function startMockRpc(handler) {
  return new Promise((resolve) => {
    const srv = createServer((req, res) => {
      let body = '';
      req.on('data', chunk => { body += chunk; });
      req.on('end', () => {
        let rpcId = null;
        try {
          const parsed = JSON.parse(body);
          const reqs = Array.isArray(parsed) ? parsed : [parsed];
          const results = reqs.map(r => {
            rpcId = r.id;
            const result = handler(r.method, r.params || []);
            return { jsonrpc: '2.0', id: r.id, result: result ?? null };
          });
          const out = Array.isArray(parsed) ? results : results[0];
          res.writeHead(200, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify(out));
        } catch (e) {
          res.writeHead(200, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify({ jsonrpc: '2.0', id: rpcId, error: { code: -32603, message: e.message } }));
        }
      });
    });
    srv.listen(0, '127.0.0.1', () => {
      const { port } = srv.address();
      resolve({ url: `http://127.0.0.1:${port}`, close: () => srv.close() });
    });
  });
}

/**
 * Run deposit.js ASYNC — does NOT block the event loop, allowing the
 * in-process mock RPC server to respond to the child's HTTP requests.
 */
function runDeposit(args, rpcUrl, timeoutMs = 30_000) {
  return new Promise((resolve) => {
    const stdoutChunks = [];
    const stderrChunks = [];
    const proc = spawn(process.execPath, [DEPOSIT_JS, ...args], {
      env: { ...process.env, ARBITRUM_RPC_URL: rpcUrl },
    });
    proc.stdout.on('data', d => stdoutChunks.push(d));
    proc.stderr.on('data', d => stderrChunks.push(d));

    const timer = setTimeout(() => { proc.kill('SIGTERM'); }, timeoutMs);

    proc.on('close', (code) => {
      clearTimeout(timer);
      const parse = raw => raw.split('\n').filter(Boolean).map(l => {
        try { return JSON.parse(l); } catch { return l; }
      });
      resolve({
        stdout: parse(stdoutChunks.join('')),
        stderr: parse(stderrChunks.join('')),
        exitCode: code,
      });
    });
  });
}

// ---------------------------------------------------------------------------
// Tests
// ---------------------------------------------------------------------------

describe('deposit.js --confirmed (mock Arbitrum RPC)', () => {
  let rpc;

  beforeAll(async () => {
    rpc = await startMockRpc(makeHandler({ usdcBalance6: 100_000_000 })); // 100 USDC
  });

  afterAll(() => rpc?.close());

  // --- Happy path ---

  it('preview only (no --confirmed): exits 0, outputs preview JSON', async () => {
    const { stdout, exitCode } = await runDeposit(['10'], rpc.url);
    expect(exitCode).toBe(0);
    expect(stdout).toHaveLength(1);
    expect(stdout[0]).toMatchObject({
      preview:              true,
      action:               'Deposit USDC -> Hyperliquid L1',
      amount_usdc:          10,
      network:              'Arbitrum One',
      destination:          'Hyperliquid L1',
      requiresConfirm:      false,   // 10 < 100 threshold
      requiresDoubleConfirm: false,
    });
    expect(stdout[0].from_address).toBe(stdout[0].to_hl_address);
    expect(stdout[0].estimated_credit_time).toBe('~1 minute');
  });

  it('requiresConfirm=true for amount >= 100 USDC', async () => {
    const { stdout, exitCode } = await runDeposit(['100'], rpc.url);
    expect(exitCode).toBe(0);
    expect(stdout[0].requiresConfirm).toBe(true);
    expect(stdout[0].requiresDoubleConfirm).toBe(false);
  });

  it('requiresDoubleConfirm=true for amount >= 1000 USDC', async () => {
    const bigRpc = await startMockRpc(makeHandler({ usdcBalance6: 2_000_000_000 })); // 2000 USDC
    try {
      const { stdout, exitCode } = await runDeposit(['1000'], bigRpc.url);
      expect(exitCode).toBe(0);
      expect(stdout[0].requiresDoubleConfirm).toBe(true);
    } finally {
      bigRpc.close();
    }
  });

  it('--confirmed: outputs preview + submitted + confirmed, exits 0', async () => {
    const { stdout, exitCode, stderr } = await runDeposit(['10', '--confirmed'], rpc.url);
    expect(exitCode).toBe(0, `stderr: ${JSON.stringify(stderr)}`);
    expect(stdout).toHaveLength(3);

    // Line 1: preview
    expect(stdout[0]).toMatchObject({ preview: true, amount_usdc: 10 });

    // Line 2: submitted
    expect(stdout[1]).toMatchObject({
      type:   'submitted',
      txHash: expect.stringMatching(/^0x[0-9a-f]{64}$/),
      status: 'pending',
    });
    const txHash = stdout[1].txHash;

    // Line 3: confirmed (same txHash as submitted)
    expect(stdout[2]).toMatchObject({
      type:        'confirmed',
      txHash,
      amount_usdc: 10,
      status:      'success',
    });
    expect(stdout[2].blockNumber).toBeDefined();
    expect(stdout[2].gasUsed).toBeDefined();
    expect(stdout[2].note).toContain('~1 minute');
  });

  // --- Error paths ---

  it('exits 1 when receipt has no Transfer event', async () => {
    // receiptOverride = {} base; handler injects real txHash at runtime
    const noTransferRpc = await startMockRpc(makeHandler({
      usdcBalance6: 100_000_000,
      receiptOverride: {
        blockNumber:       BLOCK_NUM,
        status:            '0x1',
        gasUsed:           '0xfe50',
        index:             '0x0',
        transactionIndex:  '0x0',
        logs:              [],   // ← no Transfer event
        logsBloom:         '0x' + '0'.repeat(512),
        cumulativeGasUsed: '0xfe50',
        effectiveGasPrice: '0x3b9aca00',
        type:              '0x2',
        from:              WALLET,
        to:                USDC,
        blockHash:         '0x' + 'ff'.repeat(32),
        contractAddress:   null,
      },
    }));
    try {
      const { stderr, exitCode } = await runDeposit(['10', '--confirmed'], noTransferRpc.url);
      expect(exitCode).toBe(1);
      expect(stderr[0]).toMatchObject({
        error:  expect.stringContaining('no Transfer event'),
        txHash: expect.stringMatching(/^0x[0-9a-f]{64}$/),
      });
    } finally {
      noTransferRpc.close();
    }
  });

  it('exits 1 when tx.wait() fails (reverted receipt), preserves txHash in stderr', async () => {
    // Return a reverted receipt (status: 0x0) — ethers throws TransactionReverted
    // Our catch block re-emits the txHash for manual recovery
    const revertedRpc = await startMockRpc(makeHandler({
      usdcBalance6: 100_000_000,
      receiptOverride: {
        blockNumber:       BLOCK_NUM,
        status:            '0x0',  // reverted
        gasUsed:           '0xfe50',
        index:             '0x0',
        transactionIndex:  '0x0',
        logs:              [],
        logsBloom:         '0x' + '0'.repeat(512),
        cumulativeGasUsed: '0xfe50',
        effectiveGasPrice: '0x3b9aca00',
        type:              '0x2',
        from:              WALLET,
        to:                USDC,
        blockHash:         '0x' + 'ff'.repeat(32),
        contractAddress:   null,
      },
    }));
    try {
      const { stderr, exitCode } = await runDeposit(['10', '--confirmed'], revertedRpc.url);
      expect(exitCode).toBe(1);
      const allStderr = JSON.stringify(stderr);
      // txHash should appear in stderr so the user can recover manually
      expect(allStderr).toMatch(/0x[0-9a-f]{64}/);
    } finally {
      revertedRpc.close();
    }
  });

  it('exits 1 when USDC balance is insufficient', async () => {
    const poorRpc = await startMockRpc(makeHandler({ usdcBalance6: 4_000_000 })); // 4 USDC
    try {
      const { stderr, exitCode } = await runDeposit(['10', '--confirmed'], poorRpc.url);
      expect(exitCode).toBe(1);
      expect(stderr[0]).toMatchObject({ error: expect.stringContaining('Insufficient USDC') });
    } finally {
      poorRpc.close();
    }
  });

  it('exits 1 when ETH balance is zero', async () => {
    const noEthRpc = await startMockRpc(makeHandler({ usdcBalance6: 100_000_000, ethWei: 0n }));
    try {
      const { stderr, exitCode } = await runDeposit(['10', '--confirmed'], noEthRpc.url);
      expect(exitCode).toBe(1);
      expect(stderr[0]).toMatchObject({ error: expect.stringContaining('ETH') });
    } finally {
      noEthRpc.close();
    }
  });

  it('exits 1 when RPC returns wrong chainId', async () => {
    const wrongChainRpc = await startMockRpc((method) => {
      if (method === 'eth_chainId') return '0x1';  // Ethereum mainnet
      if (method === 'net_version') return '1';
      return null;
    });
    try {
      const { stderr, exitCode } = await runDeposit(['10'], wrongChainRpc.url);
      expect(exitCode).toBe(1);
      expect(stderr[0]).toMatchObject({ error: expect.stringContaining('Wrong network') });
    } finally {
      wrongChainRpc.close();
    }
  });
});
