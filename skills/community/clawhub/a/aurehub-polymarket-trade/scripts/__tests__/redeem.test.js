// scripts/__tests__/redeem.test.js
import { vi, describe, it, expect, afterEach, beforeEach } from 'vitest';
import { filterRedeemable, buildIndexSets, formatRedeemPreview, redeem } from '../redeem.js';

vi.mock('axios', () => ({
  default: { get: vi.fn() },
}));
import axios from 'axios';

vi.mock('../lib/prompt.js', () => ({
  confirm: vi.fn(),
}));
import { confirm } from '../lib/prompt.js';

vi.mock('../lib/gas.js', () => ({
  polyGasOverrides: vi.fn().mockResolvedValue({ maxFeePerGas: 30n, maxPriorityFeePerGas: 30n }),
}));

// Partial mock of ethers — keep real utils (isAddress, formatEther, formatUnits, constants),
// replace only Contract constructor so we can control CTF and ERC20 instances.
vi.mock('ethers', async (importOriginal) => {
  const real = await importOriginal();
  return {
    ...real,
    ethers: {
      ...real.ethers,
      Contract: vi.fn(),
    },
  };
});
import { ethers } from 'ethers';

const makePos = (overrides) => ({
  slug: 'test-market',
  outcome: 'YES',
  outcomeIndex: 0,
  size: '2.0',
  curPrice: '1.0',
  conditionId: '0x00000000000000000000000000000000000000000000000000000000deadbeef',
  redeemable: true,
  negativeRisk: false,
  ...overrides,
});

const makeCfg = () => ({
  yaml: {
    contracts: {
      usdc_e: '0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174',
      ctf_contract: '0x4D97DCd97eC945f40cF65F87097ACe5EA0476045',
    },
    polymarket: { data_url: 'https://data-api.polymarket.com' },
  },
});

const makeProvider = (polEther = '0.1') => ({
  // Return a plain string — ethers v5 BigNumber.from() accepts strings as BigNumberish
  getBalance: vi.fn().mockResolvedValue(
    String(BigInt(Math.floor(parseFloat(polEther) * 1e18)))
  ),
  getFeeData: vi.fn().mockResolvedValue({
    maxPriorityFeePerGas: ethers.BigNumber.from('30000000000'),
    maxFeePerGas:         ethers.BigNumber.from('30000000000'),
  }),
});

afterEach(() => vi.clearAllMocks());

// ── Pure helpers ──────────────────────────────────────────────────────────────

describe('filterRedeemable', () => {
  it('returns empty arrays when no positions', () => {
    const { standard, negRisk } = filterRedeemable([]);
    expect(standard).toHaveLength(0);
    expect(negRisk).toHaveLength(0);
  });

  it('splits redeemable standard vs negRisk', () => {
    const positions = [
      makePos({ redeemable: true,  negativeRisk: false }),
      makePos({ redeemable: true,  negativeRisk: true  }),
      makePos({ redeemable: false, negativeRisk: false }),
    ];
    const { standard, negRisk } = filterRedeemable(positions);
    expect(standard).toHaveLength(1);
    expect(negRisk).toHaveLength(1);
  });

  it('ignores non-redeemable positions entirely', () => {
    const { standard, negRisk } = filterRedeemable([makePos({ redeemable: false })]);
    expect(standard).toHaveLength(0);
    expect(negRisk).toHaveLength(0);
  });
});

describe('buildIndexSets', () => {
  it('outcomeIndex=0 → [1]', () => {
    expect(buildIndexSets(0)).toEqual([1]);
  });
  it('outcomeIndex=1 → [2]', () => {
    expect(buildIndexSets(1)).toEqual([2]);
  });
  it('outcomeIndex=31 throws out-of-range error', () => {
    expect(() => buildIndexSets(31)).toThrow('out of supported range');
  });
});

describe('formatRedeemPreview', () => {
  it('contains slug, outcome, shares, receive', () => {
    const out = formatRedeemPreview([makePos({ slug: 'my-market', outcome: 'YES', size: '3.0' })]);
    expect(out).toContain('my-market');
    expect(out).toContain('YES');
    expect(out).toContain('3.00');
    expect(out).toContain('~$3.00');
  });

  it('sums total correctly', () => {
    const out = formatRedeemPreview([
      makePos({ size: '2.0' }),
      makePos({ slug: 'other', size: '3.0' }),
    ]);
    expect(out).toContain('Total');
    expect(out).toContain('~$5.00');
  });
});

// ── redeem() function ─────────────────────────────────────────────────────────

describe('redeem() — dry-run exits before confirm', () => {
  it('prints preview and returns without executing when dryRun=true', async () => {
    axios.get.mockResolvedValue({ data: [makePos()] });
    const wallet = { address: '0xUser' };
    const provider = makeProvider('0.5');
    // If confirm were called it would hang; dryRun should bypass it entirely
    await expect(
      redeem({ cfg: makeCfg(), provider, wallet, marketFilter: null, dryRun: true }),
    ).resolves.toBeUndefined();
  });
});

describe('redeem() — no redeemable positions', () => {
  it('returns without error when positions API returns empty list', async () => {
    axios.get.mockResolvedValue({ data: [] });
    const wallet = { address: '0xUser' };
    await expect(
      redeem({ cfg: makeCfg(), provider: makeProvider(), wallet, marketFilter: null, dryRun: true }),
    ).resolves.toBeUndefined();
  });
});

describe('redeem() — market filter', () => {
  it('only passes matching slug to preview', async () => {
    axios.get.mockResolvedValue({
      data: [
        makePos({ slug: 'target-market', conditionId: '0x0000000000000000000000000000000000000000000000000000000000001234' }),
        makePos({ slug: 'other-market',  conditionId: '0x0000000000000000000000000000000000000000000000000000000000005678' }),
      ],
    });
    const wallet = { address: '0xUser' };
    const logSpy = vi.spyOn(console, 'log').mockImplementation(() => {});
    try {
      await redeem({ cfg: makeCfg(), provider: makeProvider(), wallet, marketFilter: 'target-market', dryRun: true });
      const output = logSpy.mock.calls.map(c => c.join(' ')).join('\n');
      expect(output).toContain('target-market');
      expect(output).not.toContain('other-market');
    } finally {
      logSpy.mockRestore();
    }
  });
});

describe('redeem() — market filter by conditionId', () => {
  it('filters by conditionId when marketFilter looks like a conditionId', async () => {
    const targetConditionId = '0x0000000000000000000000000000000000000000000000000000000000001234';
    axios.get.mockResolvedValue({
      data: [
        makePos({ slug: 'target-market', conditionId: targetConditionId }),
        makePos({ slug: 'other-market',  conditionId: '0x0000000000000000000000000000000000000000000000000000000000005678' }),
      ],
    });
    const wallet = { address: '0xUser' };
    const logSpy = vi.spyOn(console, 'log').mockImplementation(() => {});
    try {
      await redeem({ cfg: makeCfg(), provider: makeProvider(), wallet, marketFilter: targetConditionId, dryRun: true });
      const output = logSpy.mock.calls.map(c => c.join(' ')).join('\n');
      expect(output).toContain('target-market');
      expect(output).not.toContain('other-market');
    } finally {
      logSpy.mockRestore();
    }
  });
});

describe('redeem() — negRisk-only skip', () => {
  it('returns without error when all redeemable positions are negRisk', async () => {
    axios.get.mockResolvedValue({
      data: [makePos({ redeemable: true, negativeRisk: true })],
    });
    const wallet = { address: '0xUser' };
    await expect(
      redeem({ cfg: makeCfg(), provider: makeProvider(), wallet, marketFilter: null, dryRun: true }),
    ).resolves.toBeUndefined();
  });
});

describe('redeem() — insufficient POL', () => {
  it('throws before any API call when POL < 0.01', async () => {
    const wallet = { address: '0xUser' };
    const provider = makeProvider('0.005');
    await expect(
      redeem({ cfg: makeCfg(), provider, wallet, marketFilter: null, dryRun: false }),
    ).rejects.toThrow('POL');
    expect(axios.get).not.toHaveBeenCalled();
  });
});

// ── Integration tests (non-dry-run, with CTF contract mock) ───────────────────

describe('redeem() — successful single redeem', () => {
  let mockCtfInstance;
  let mockUsdceInstance;

  beforeEach(() => {
    const mockTx = { hash: '0xtxhash', wait: vi.fn().mockResolvedValue({}) };
    mockCtfInstance = {
      redeemPositions: vi.fn().mockResolvedValue(mockTx),
    };
    // USDC.e balanceOf returns 5 USDC.e (6 decimals)
    mockUsdceInstance = {
      balanceOf: vi.fn().mockResolvedValue('5000000'),
    };
    // First call → CTF (redeemPositions), second call → ERC20 (balanceOf).
    // Must use regular functions (not arrows) so they work as constructors with `new`.
    // eslint-disable-next-line prefer-arrow-callback
    ethers.Contract.mockImplementationOnce(function () { return mockCtfInstance; })
                   // eslint-disable-next-line prefer-arrow-callback
                   .mockImplementationOnce(function () { return mockUsdceInstance; });
    confirm.mockResolvedValue(true);
  });

  it('calls CTF.redeemPositions with correct args and returns result', async () => {
    const pos = makePos({ slug: 'win-market', conditionId: '0x000000000000000000000000000000000000000000000000000000000000c0d1', outcomeIndex: 0 });
    axios.get.mockResolvedValue({ data: [pos] });
    const wallet = { address: '0xUser' };

    const results = await redeem({
      cfg: makeCfg(), provider: makeProvider(), wallet, marketFilter: null, dryRun: false,
    });

    expect(mockCtfInstance.redeemPositions).toHaveBeenCalledOnce();
    expect(mockCtfInstance.redeemPositions).toHaveBeenCalledWith(
      '0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174', // usdceAddr
      ethers.constants.HashZero,
      ethers.utils.hexZeroPad('0x000000000000000000000000000000000000000000000000000000000000c0d1', 32),
      [1], // buildIndexSets(0)
      expect.any(Object), // gasOverrides
    );
    expect(results).toHaveLength(1);
    expect(results[0]).toMatchObject({ slug: 'win-market', txHash: '0xtxhash', success: true });
  });
});

describe('redeem() — successful multi-position redeem', () => {
  let mockCtfInstance;
  let mockUsdceInstance;

  beforeEach(() => {
    const makeTx = (hash) => ({ hash, wait: vi.fn().mockResolvedValue({}) });
    mockCtfInstance = {
      redeemPositions: vi.fn()
        .mockResolvedValueOnce(makeTx('0xtx1'))
        .mockResolvedValueOnce(makeTx('0xtx2')),
    };
    mockUsdceInstance = {
      balanceOf: vi.fn().mockResolvedValue('10000000'),
    };
    // eslint-disable-next-line prefer-arrow-callback
    ethers.Contract.mockImplementationOnce(function () { return mockCtfInstance; })
                   // eslint-disable-next-line prefer-arrow-callback
                   .mockImplementationOnce(function () { return mockUsdceInstance; });
    confirm.mockResolvedValue(true);
  });

  it('redeems both positions in sequence and returns 2 results', async () => {
    axios.get.mockResolvedValue({
      data: [
        makePos({ slug: 'market-a', conditionId: '0x000000000000000000000000000000000000000000000000000000000000aaaa', outcomeIndex: 0 }),
        makePos({ slug: 'market-b', conditionId: '0x000000000000000000000000000000000000000000000000000000000000bbbb', outcomeIndex: 1 }),
      ],
    });
    const wallet = { address: '0xUser' };

    const results = await redeem({
      cfg: makeCfg(), provider: makeProvider(), wallet, marketFilter: null, dryRun: false,
    });

    expect(mockCtfInstance.redeemPositions).toHaveBeenCalledTimes(2);
    expect(results).toHaveLength(2);
    expect(results[0]).toMatchObject({ slug: 'market-a', txHash: '0xtx1', success: true });
    expect(results[1]).toMatchObject({ slug: 'market-b', txHash: '0xtx2', success: true });
  });
});

describe('redeem() — user cancels at confirm prompt', () => {
  it('returns undefined and does not call CTF when user declines', async () => {
    axios.get.mockResolvedValue({ data: [makePos()] });
    confirm.mockResolvedValue(false);

    // Set up Contract mock — it should NOT be called in this path (no ctf instantiation
    // happens before the confirm check, but ethers.Contract is called after confirm).
    // We track whether redeemPositions was called by providing a spy CTF mock.
    const mockCtf = { redeemPositions: vi.fn() };
    // eslint-disable-next-line prefer-arrow-callback
    ethers.Contract.mockImplementation(function () { return mockCtf; });

    const wallet = { address: '0xUser' };
    const result = await redeem({
      cfg: makeCfg(), provider: makeProvider(), wallet, marketFilter: null, dryRun: false,
    });

    expect(result).toBeUndefined();
    expect(mockCtf.redeemPositions).not.toHaveBeenCalled();
  });
});

describe('redeem() — mixed standard + negRisk', () => {
  let mockCtfInstance;
  let mockUsdceInstance;

  beforeEach(() => {
    const mockTx = { hash: '0xtxStd', wait: vi.fn().mockResolvedValue({}) };
    mockCtfInstance = { redeemPositions: vi.fn().mockResolvedValue(mockTx) };
    mockUsdceInstance = { balanceOf: vi.fn().mockResolvedValue('3000000') };
    // eslint-disable-next-line prefer-arrow-callback
    ethers.Contract.mockImplementationOnce(function () { return mockCtfInstance; })
                   // eslint-disable-next-line prefer-arrow-callback
                   .mockImplementationOnce(function () { return mockUsdceInstance; });
    confirm.mockResolvedValue(true);
  });

  it('prints negRisk notice AND redeems the standard position', async () => {
    axios.get.mockResolvedValue({
      data: [
        makePos({ slug: 'std-market',     negativeRisk: false, conditionId: '0x000000000000000000000000000000000000000000000000000000000000abcd' }),
        makePos({ slug: 'negrisk-market', negativeRisk: true  }),
      ],
    });
    const wallet = { address: '0xUser' };
    const logSpy = vi.spyOn(console, 'log').mockImplementation(() => {});

    try {
      const results = await redeem({
        cfg: makeCfg(), provider: makeProvider(), wallet, marketFilter: null, dryRun: false,
      });

      const output = logSpy.mock.calls.map(c => c.join(' ')).join('\n');
      expect(output).toContain('negrisk-market');
      expect(output).toContain('Skipped');
      expect(mockCtfInstance.redeemPositions).toHaveBeenCalledOnce();
      expect(results).toHaveLength(1);
      expect(results[0]).toMatchObject({ slug: 'std-market', success: true });
    } finally {
      logSpy.mockRestore();
    }
  });
});

describe('redeem() — positions API returns non-array', () => {
  it('throws "Positions API returned unexpected response" when data is an object', async () => {
    axios.get.mockResolvedValue({ data: { error: 'bad' } });
    const wallet = { address: '0xUser' };

    await expect(
      redeem({ cfg: makeCfg(), provider: makeProvider(), wallet, marketFilter: null, dryRun: false }),
    ).rejects.toThrow('Positions API returned unexpected response');
  });
});

describe('redeem() — invalid CTF address in config', () => {
  it('throws before any API call when ctf_contract is not a valid address', async () => {
    const badCfg = {
      yaml: {
        contracts: {
          usdc_e: '0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174',
          ctf_contract: 'not-an-address',
        },
        polymarket: { data_url: 'https://data-api.polymarket.com' },
      },
    };
    const wallet = { address: '0xUser' };

    await expect(
      redeem({ cfg: badCfg, provider: makeProvider(), wallet, marketFilter: null, dryRun: false }),
    ).rejects.toThrow(/Invalid ctf_contract/i);

    expect(axios.get).not.toHaveBeenCalled();
  });
});
