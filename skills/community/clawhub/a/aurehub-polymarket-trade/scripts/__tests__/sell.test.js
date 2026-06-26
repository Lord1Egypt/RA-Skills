// scripts/__tests__/sell.test.js
import { vi, describe, it, expect, beforeEach, afterEach } from 'vitest';

// ── vi.mock() calls are hoisted to the top of the file by vitest.
// Do NOT reference module-level variables inside the factory — they won't be
// initialized yet. Wire up mock implementations in beforeEach instead.

vi.mock('@polymarket/clob-client', () => ({
  Side:          { SELL: 'SELL', BUY: 'BUY' },
  OrderType:     { FOK: 'FOK' },
  SignatureType: { EOA: 0 },
  ClobClient:    vi.fn(),
}));

vi.mock('../lib/clob.js', () => ({
  createL2Client: vi.fn(),
}));

vi.mock('../lib/config.js', () => ({
  loadConfig:    vi.fn(),
  resolveRpcUrl: vi.fn().mockReturnValue('http://localhost:8545'),
}));

vi.mock('../lib/signer.js', () => ({
  createSigner: vi.fn(),
}));

vi.mock('../lib/prompt.js', () => ({
  confirm: vi.fn(),
}));

vi.mock('../lib/gas.js', () => ({
  polyGasOverrides: vi.fn().mockResolvedValue({ maxFeePerGas: 30n, maxPriorityFeePerGas: 30n }),
}));

vi.mock('../setup.js', () => ({
  runTradeEnvCheck:  vi.fn(),
  runBrowseEnvCheck: vi.fn(),
}));

// Polymarket token IDs are large decimal numeric strings — they must be parseable
// by ethers.BigNumber.from() since sell() calls: ctf.balanceOf(addr, BigNumber.from(tokenID))
// These constants are declared here for use in test assertions (after imports).
// The vi.mock factory below is hoisted, so it inlines the same values directly.
const TOKEN_YES = '52114319501245915516055106046884209969926127482827954674443846427813813222426';
const TOKEN_NO  = '52114319501245915516055106046884209969926127482827954674443846427813813222427';

vi.mock('../browse.js', () => ({
  extractTokenIds: vi.fn((market) => ({
    YES: market._yesTokenId ?? '52114319501245915516055106046884209969926127482827954674443846427813813222426',
    NO:  market._noTokenId  ?? '52114319501245915516055106046884209969926127482827954674443846427813813222427',
  })),
  resolveMarket: vi.fn(),
}));

// Partial mock of ethers — keep real BigNumber/utils, replace Contract constructor
vi.mock('ethers', async (importOriginal) => {
  const real = await importOriginal();
  return {
    ...real,
    ethers: {
      ...real.ethers,
      // Contract is replaced — actual instance is returned by getContractMock()
      // which is set up per-test. We use a module-level placeholder here
      // because the factory is hoisted and can't close over test state.
      // The real wiring happens via the mockEthersContract helper below.
      Contract: vi.fn(),
    },
  };
});

// ── Imports under test (after vi.mock declarations) ───────────────────────────
import { ethers }          from 'ethers';
import { sell }            from '../trade.js';
import { confirm }         from '../lib/prompt.js';
import { createL2Client }  from '../lib/clob.js';

// ── Reusable mock objects (created fresh each test via beforeEach) ─────────────

let mockClientInstance;
let mockCtfInstance;
let mockCtfSigned;

beforeEach(() => {
  // ClobClient instance returned by createL2Client
  mockClientInstance = {
    getNegRisk:        vi.fn(),
    getTickSize:       vi.fn(),
    getOrderBook:      vi.fn(),
    createMarketOrder: vi.fn(),
    postOrder:         vi.fn(),
    getTrades:         vi.fn(),
  };
  createL2Client.mockResolvedValue(mockClientInstance);

  // CTF ERC1155 contract instance (returned by ethers.Contract)
  mockCtfSigned = {
    setApprovalForAll: vi.fn(),
  };
  mockCtfInstance = {
    balanceOf:        vi.fn(),
    isApprovedForAll: vi.fn(),
    connect:          vi.fn().mockReturnValue(mockCtfSigned),
  };

  // Wire ethers.Contract to return our CTF mock.
  // Must use a real function (not arrow) so it can be used as a constructor.
  // eslint-disable-next-line prefer-arrow-callback
  ethers.Contract.mockImplementation(function () { return mockCtfInstance; });
});

afterEach(() => vi.clearAllMocks());

// ── Helpers ───────────────────────────────────────────────────────────────────

function makeMarket(overrides = {}) {
  return {
    question:           'Will it rain tomorrow?',
    active:             true,
    neg_risk:           false,
    min_incentive_size: '1',
    clobTokenIds:       '["token-yes-123","token-no-456"]',
    outcomes:           '["Yes","No"]',
    outcomePrices:      '["0.6","0.4"]',
    ...overrides,
  };
}

function makeProvider(polEther = '0.5') {
  const polWei = ethers.BigNumber.from(
    String(BigInt(Math.floor(parseFloat(polEther) * 1e18))),
  );
  return {
    getBalance: vi.fn().mockResolvedValue(polWei),
    getFeeData: vi.fn().mockResolvedValue({
      maxPriorityFeePerGas: { lt: () => false, toString: () => '30000000000' },
      maxFeePerGas:         { lt: () => false, toString: () => '30000000000' },
    }),
  };
}

function makeWallet(address = '0xUserWallet') {
  return { address };
}

function makeCfg() {
  return {
    yaml: {
      contracts: {
        ctf_contract:      '0x4D97DCd97eC945f40cF65F87097ACe5EA0476045',
        ctf_exchange:      '0x4bFb41d5B3570DeFd03C39a9A4D8dE6Bd8B8982E',
        neg_risk_exchange: '0xC5d563A36AE78145C45a50134d48A1215220f80a',
      },
      safety: { warn_threshold_usd: 50, confirm_threshold_usd: 500 },
    },
  };
}

// Convert a share float to ethers.BigNumber with 6 decimals (as the contract returns)
function sharesWei(amount) {
  return ethers.utils.parseUnits(String(amount), 6);
}

// Configure the happy-path mock state
function setupHappyPath({
  sharesHeld      = 10,
  polEther        = '0.5',
  negRisk         = false,
  bestBid         = '0.60',
  alreadyApproved = false,
} = {}) {
  mockCtfInstance.balanceOf.mockResolvedValue(sharesWei(sharesHeld));
  mockCtfInstance.isApprovedForAll.mockResolvedValue(alreadyApproved);
  mockCtfSigned.setApprovalForAll.mockResolvedValue({ wait: vi.fn().mockResolvedValue({}) });

  mockClientInstance.getNegRisk.mockResolvedValue(negRisk);
  mockClientInstance.getTickSize.mockResolvedValue('0.01');
  mockClientInstance.getOrderBook.mockResolvedValue({
    bids: [{ price: bestBid, size: '100' }],
    asks: [{ price: '0.65', size: '100' }],
  });
  mockClientInstance.createMarketOrder.mockResolvedValue({});
  mockClientInstance.postOrder.mockResolvedValue({ success: true, status: 'matched', orderID: 'order-abc' });
  mockClientInstance.getTrades.mockResolvedValue([]);

  confirm.mockResolvedValue(true);
}

// ── Tests ─────────────────────────────────────────────────────────────────────

describe('sell() — input validation', () => {
  it('throws "Invalid side" for an unrecognised side value', async () => {
    await expect(
      sell({ market: makeMarket(), side: 'MAYBE', amount: 5, cfg: makeCfg(), provider: makeProvider(), wallet: makeWallet() }),
    ).rejects.toThrow('Invalid side');
  });

  it('throws "Invalid side" when side is lowercase', async () => {
    await expect(
      sell({ market: makeMarket(), side: 'yes', amount: 5, cfg: makeCfg(), provider: makeProvider(), wallet: makeWallet() }),
    ).rejects.toThrow('Invalid side');
  });

  it('throws "Invalid amount" when amount is 0', async () => {
    await expect(
      sell({ market: makeMarket(), side: 'YES', amount: 0, cfg: makeCfg(), provider: makeProvider(), wallet: makeWallet() }),
    ).rejects.toThrow('Invalid amount');
  });

  it('throws "Invalid amount" when amount is negative', async () => {
    await expect(
      sell({ market: makeMarket(), side: 'YES', amount: -5, cfg: makeCfg(), provider: makeProvider(), wallet: makeWallet() }),
    ).rejects.toThrow('Invalid amount');
  });

  it('throws "Invalid amount" when amount is NaN', async () => {
    await expect(
      sell({ market: makeMarket(), side: 'YES', amount: NaN, cfg: makeCfg(), provider: makeProvider(), wallet: makeWallet() }),
    ).rejects.toThrow('Invalid amount');
  });

  it('throws "Invalid amount" when amount is Infinity', async () => {
    await expect(
      sell({ market: makeMarket(), side: 'YES', amount: Infinity, cfg: makeCfg(), provider: makeProvider(), wallet: makeWallet() }),
    ).rejects.toThrow('Invalid amount');
  });
});

describe('sell() — CTF balance check', () => {
  beforeEach(() => {
    // Provide just enough mocks to get past createL2Client and into the balance check
    mockClientInstance.getNegRisk.mockResolvedValue(false);
    mockClientInstance.getTickSize.mockResolvedValue('0.01');
    mockClientInstance.getOrderBook.mockResolvedValue({
      bids: [{ price: '0.60', size: '100' }],
      asks: [],
    });
  });

  it('throws "Insufficient" when wallet holds fewer shares than amount', async () => {
    mockCtfInstance.balanceOf.mockResolvedValue(sharesWei(3)); // only 3 shares

    await expect(
      sell({ market: makeMarket(), side: 'YES', amount: 10, cfg: makeCfg(), provider: makeProvider(), wallet: makeWallet() }),
    ).rejects.toThrow('Insufficient');
  });
});

describe('sell() — hard stops', () => {
  it('throws when POL balance is below 0.01', async () => {
    setupHappyPath();

    await expect(
      sell({ market: makeMarket(), side: 'YES', amount: 5, cfg: makeCfg(), provider: makeProvider('0.005'), wallet: makeWallet() }),
    ).rejects.toThrow('POL');
  });

  it('throws when market is closed (active: false)', async () => {
    setupHappyPath();

    await expect(
      sell({ market: makeMarket({ active: false }), side: 'YES', amount: 5, cfg: makeCfg(), provider: makeProvider(), wallet: makeWallet() }),
    ).rejects.toThrow('CLOSED');
  });

  it('throws when estimated proceeds are below min order size', async () => {
    // bestBid=$0.10, amount=5 shares → estUsdce=$0.50; minOrderSize=$5 → fail
    setupHappyPath({ bestBid: '0.10' });

    await expect(
      sell({ market: makeMarket({ min_incentive_size: '5' }), side: 'YES', amount: 5, cfg: makeCfg(), provider: makeProvider(), wallet: makeWallet() }),
    ).rejects.toThrow(/min/i);
  });
});

describe('sell() — user confirmation (safety gates)', () => {
  it('returns undefined (no throw) when user cancels at warn prompt', async () => {
    // 100 shares × $0.60 = $60 → triggers warn gate (threshold $50)
    setupHappyPath({ sharesHeld: 200, bestBid: '0.60' });
    confirm.mockResolvedValue(false); // user cancels

    const result = await sell({
      market:   makeMarket({ min_incentive_size: '1' }),
      side:     'YES',
      amount:   100,
      cfg:      makeCfg(),
      provider: makeProvider(),
      wallet:   makeWallet(),
    });

    expect(result).toBeUndefined();
    expect(mockClientInstance.postOrder).not.toHaveBeenCalled();
  });
});

describe('sell() — successful sell', () => {
  it('returns the postOrder result on a happy-path sell', async () => {
    setupHappyPath({ sharesHeld: 20, alreadyApproved: true });

    const result = await sell({
      market:   makeMarket(),
      side:     'YES',
      amount:   5,
      cfg:      makeCfg(),
      provider: makeProvider(),
      wallet:   makeWallet(),
    });

    expect(result).toMatchObject({ success: true, status: 'matched', orderID: 'order-abc' });
    expect(mockClientInstance.postOrder).toHaveBeenCalledOnce();
  });

  it('passes Side.SELL to createMarketOrder', async () => {
    setupHappyPath({ sharesHeld: 20, alreadyApproved: true });

    await sell({ market: makeMarket(), side: 'YES', amount: 5, cfg: makeCfg(), provider: makeProvider(), wallet: makeWallet() });

    expect(mockClientInstance.createMarketOrder).toHaveBeenCalledWith(
      expect.objectContaining({ side: 'SELL' }),
      expect.any(Object),
    );
  });

  it('sells NO side correctly', async () => {
    setupHappyPath({ sharesHeld: 20, alreadyApproved: true });

    const result = await sell({
      market:   makeMarket(),
      side:     'NO',
      amount:   5,
      cfg:      makeCfg(),
      provider: makeProvider(),
      wallet:   makeWallet(),
    });

    expect(result).toMatchObject({ success: true });
    expect(mockClientInstance.createMarketOrder).toHaveBeenCalledWith(
      expect.objectContaining({ tokenID: TOKEN_NO }),
      expect.any(Object),
    );
  });
});

describe('sell() — operator approval', () => {
  it('calls setApprovalForAll(operator, true) when not yet approved', async () => {
    setupHappyPath({ sharesHeld: 20, alreadyApproved: false });

    await sell({ market: makeMarket(), side: 'YES', amount: 5, cfg: makeCfg(), provider: makeProvider(), wallet: makeWallet() });

    expect(mockCtfSigned.setApprovalForAll).toHaveBeenCalledWith(
      expect.stringMatching(/^0x/),
      true,
      expect.any(Object),
    );
  });

  it('skips setApprovalForAll when operator already approved', async () => {
    setupHappyPath({ sharesHeld: 20, alreadyApproved: true });

    await sell({ market: makeMarket(), side: 'YES', amount: 5, cfg: makeCfg(), provider: makeProvider(), wallet: makeWallet() });

    expect(mockCtfSigned.setApprovalForAll).not.toHaveBeenCalled();
  });

  it('uses neg_risk_exchange as operator when negRisk=true', async () => {
    setupHappyPath({ sharesHeld: 20, alreadyApproved: false, negRisk: true });
    const cfg = makeCfg();

    await sell({ market: makeMarket(), side: 'YES', amount: 5, cfg, provider: makeProvider(), wallet: makeWallet() });

    const negRiskExchange = cfg.yaml.contracts.neg_risk_exchange;
    expect(mockCtfSigned.setApprovalForAll).toHaveBeenCalledWith(
      negRiskExchange,
      true,
      expect.any(Object),
    );
  });
});

describe('sell() — FOK rejection', () => {
  it('throws and revokes approval when postOrder returns { success: false }', async () => {
    setupHappyPath({ sharesHeld: 20, alreadyApproved: false });
    mockCtfSigned.setApprovalForAll
      // first call: approve
      .mockResolvedValueOnce({ wait: vi.fn().mockResolvedValue({}) })
      // second call (revoke): also succeeds
      .mockResolvedValueOnce({ wait: vi.fn().mockResolvedValue({}) });
    mockClientInstance.postOrder.mockResolvedValue({ success: false, errorMsg: 'no liquidity' });

    await expect(
      sell({ market: makeMarket(), side: 'YES', amount: 5, cfg: makeCfg(), provider: makeProvider(), wallet: makeWallet() }),
    ).rejects.toThrow(/not filled/i);

    // Second setApprovalForAll call should revoke (false)
    expect(mockCtfSigned.setApprovalForAll).toHaveBeenCalledTimes(2);
    expect(mockCtfSigned.setApprovalForAll).toHaveBeenLastCalledWith(
      expect.stringMatching(/^0x/),
      false,
      expect.any(Object),
    );
  });
});

describe('sell() — network error on postOrder', () => {
  it('resolves with fill details when fill found in trade history after network error', async () => {
    setupHappyPath({ sharesHeld: 20, alreadyApproved: true });
    mockClientInstance.postOrder.mockRejectedValue(new Error('Network timeout'));

    const nowSec = Math.floor(Date.now() / 1000);
    const recentTrade = { id: 'fill-xyz', status: 'matched', timestamp: String(nowSec - 10) };
    mockClientInstance.getTrades.mockResolvedValue([recentTrade]);

    const result = await sell({
      market:   makeMarket(),
      side:     'YES',
      amount:   5,
      cfg:      makeCfg(),
      provider: makeProvider(),
      wallet:   makeWallet(),
    });

    expect(result).toMatchObject({ success: true, orderID: 'fill-xyz', status: 'matched' });
  });

  it('throws and revokes approval when network error and no fill found in history', async () => {
    setupHappyPath({ sharesHeld: 20, alreadyApproved: false });
    mockCtfSigned.setApprovalForAll
      .mockResolvedValueOnce({ wait: vi.fn().mockResolvedValue({}) })  // approve
      .mockResolvedValueOnce({ wait: vi.fn().mockResolvedValue({}) }); // revoke
    mockClientInstance.postOrder.mockRejectedValue(new Error('ECONNRESET'));
    mockClientInstance.getTrades.mockResolvedValue([]);

    await expect(
      sell({ market: makeMarket(), side: 'YES', amount: 5, cfg: makeCfg(), provider: makeProvider(), wallet: makeWallet() }),
    ).rejects.toThrow(/fill status unknown/i);

    // Revoke call: setApprovalForAll(operator, false)
    expect(mockCtfSigned.setApprovalForAll).toHaveBeenCalledTimes(2);
    expect(mockCtfSigned.setApprovalForAll).toHaveBeenLastCalledWith(
      expect.stringMatching(/^0x/),
      false,
      expect.any(Object),
    );
  });
});

describe('sell() — no bids in orderbook', () => {
  it('falls back to $0.50/share estimate when orderbook has no bids', async () => {
    setupHappyPath({ sharesHeld: 20, alreadyApproved: true });
    mockClientInstance.getOrderBook.mockResolvedValue({ bids: [], asks: [] });

    // 5 shares × $0.50 = $2.50; minOrderSize=$1 → should proceed
    const result = await sell({
      market:   makeMarket({ min_incentive_size: '1' }),
      side:     'YES',
      amount:   5,
      cfg:      makeCfg(),
      provider: makeProvider(),
      wallet:   makeWallet(),
    });

    expect(result).toMatchObject({ success: true });
  });
});

describe('sell() — dry-run', () => {
  it('returns { dryRun: true } without calling postOrder or setApprovalForAll', async () => {
    setupHappyPath({ sharesHeld: 20, alreadyApproved: false });

    const result = await sell({
      market:   makeMarket(),
      side:     'YES',
      amount:   5,
      cfg:      makeCfg(),
      provider: makeProvider(),
      wallet:   makeWallet(),
      dryRun:   true,
    });

    expect(result).toMatchObject({ dryRun: true });
    expect(mockClientInstance.postOrder).not.toHaveBeenCalled();
    expect(mockCtfSigned.setApprovalForAll).not.toHaveBeenCalled();
  });

  it('still calls createMarketOrder in dry-run', async () => {
    setupHappyPath({ sharesHeld: 20 });

    await sell({
      market:   makeMarket(),
      side:     'YES',
      amount:   5,
      cfg:      makeCfg(),
      provider: makeProvider(),
      wallet:   makeWallet(),
      dryRun:   true,
    });

    expect(mockClientInstance.createMarketOrder).toHaveBeenCalledOnce();
  });

  it('skips safety gate confirm calls in dry-run', async () => {
    setupHappyPath({ sharesHeld: 200, bestBid: '0.60' });

    // 100 shares × $0.60 = $60 — would trigger warn gate normally
    await sell({
      market:   makeMarket({ min_incentive_size: '1' }),
      side:     'YES',
      amount:   100,
      cfg:      makeCfg(),
      provider: makeProvider(),
      wallet:   makeWallet(),
      dryRun:   true,
    });

    expect(confirm).not.toHaveBeenCalled();
  });

  it('still enforces hard stops in dry-run (market closed)', async () => {
    setupHappyPath({ sharesHeld: 20 });

    await expect(
      sell({
        market:   makeMarket({ active: false }),
        side:     'YES',
        amount:   5,
        cfg:      makeCfg(),
        provider: makeProvider(),
        wallet:   makeWallet(),
        dryRun:   true,
      }),
    ).rejects.toThrow('CLOSED');
  });

  it('still enforces CTF balance check in dry-run', async () => {
    setupHappyPath({ sharesHeld: 3 }); // only 3 shares, trying to sell 10

    await expect(
      sell({
        market:   makeMarket(),
        side:     'YES',
        amount:   10,
        cfg:      makeCfg(),
        provider: makeProvider(),
        wallet:   makeWallet(),
        dryRun:   true,
      }),
    ).rejects.toThrow('Insufficient');
  });
});
