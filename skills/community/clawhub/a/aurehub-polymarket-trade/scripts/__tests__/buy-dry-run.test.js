// scripts/__tests__/buy-dry-run.test.js
import { vi, describe, it, expect, beforeEach, afterEach } from 'vitest';

vi.mock('@polymarket/clob-client', () => ({
  Side:          { SELL: 'SELL', BUY: 'BUY' },
  OrderType:     { FOK: 'FOK' },
  SignatureType: { EOA: 0 },
  ClobClient:    vi.fn(),
}));

vi.mock('../lib/clob.js', () => ({ createL2Client: vi.fn() }));
vi.mock('../lib/config.js', () => ({
  loadConfig:    vi.fn(),
  resolveRpcUrl: vi.fn().mockReturnValue('http://localhost:8545'),
}));
vi.mock('../lib/signer.js', () => ({ createSigner: vi.fn() }));
vi.mock('../lib/prompt.js', () => ({ confirm: vi.fn() }));
vi.mock('../lib/gas.js', () => ({
  polyGasOverrides: vi.fn().mockResolvedValue({ maxFeePerGas: 30n, maxPriorityFeePerGas: 30n }),
}));
vi.mock('../lib/swap.js', () => ({
  getSwapQuote:  vi.fn(),
  swapPolToUsdc: vi.fn(),
}));
vi.mock('../setup.js', () => ({
  runTradeEnvCheck:  vi.fn(),
  runBrowseEnvCheck: vi.fn(),
}));
vi.mock('../browse.js', () => ({
  extractTokenIds: vi.fn(() => ({
    YES: '52114319501245915516055106046884209969926127482827954674443846427813813222426',
    NO:  '52114319501245915516055106046884209969926127482827954674443846427813813222427',
  })),
  resolveMarket: vi.fn(),
}));

vi.mock('ethers', async (importOriginal) => {
  const real = await importOriginal();
  return { ...real, ethers: { ...real.ethers, Contract: vi.fn() } };
});

import { ethers }         from 'ethers';
import { buy }            from '../trade.js';
import { confirm }        from '../lib/prompt.js';
import { createL2Client } from '../lib/clob.js';

let mockClientInstance;
let mockUsdceInstance;
let mockUsdceSigned;

beforeEach(() => {
  mockClientInstance = {
    getNegRisk:        vi.fn().mockResolvedValue(false),
    getTickSize:       vi.fn().mockResolvedValue('0.01'),
    getOrderBook:      vi.fn().mockResolvedValue({
      asks: [{ price: '0.65', size: '100' }],
      bids: [],
    }),
    createMarketOrder: vi.fn().mockResolvedValue({ tokenID: 'tok', amount: 10 }),
    postOrder:         vi.fn().mockResolvedValue({ success: true, status: 'matched', orderID: 'ord-1' }),
    getTrades:         vi.fn().mockResolvedValue([]),
  };
  createL2Client.mockResolvedValue(mockClientInstance);

  mockUsdceSigned = {
    approve: vi.fn().mockResolvedValue({ wait: vi.fn().mockResolvedValue({}) }),
  };
  mockUsdceInstance = {
    balanceOf:   vi.fn(),
    allowance:   vi.fn(),
    connect:     vi.fn().mockReturnValue(mockUsdceSigned),
  };
  ethers.Contract.mockImplementation(function () { return mockUsdceInstance; });
  confirm.mockResolvedValue(true);
});

afterEach(() => vi.clearAllMocks());

function makeMarket(overrides = {}) {
  return { active: true, neg_risk: false, min_incentive_size: '1', ...overrides };
}

function makeProvider(polEther = '0.5') {
  const polWei = ethers.BigNumber.from(String(BigInt(Math.floor(parseFloat(polEther) * 1e18))));
  return {
    getBalance: vi.fn().mockResolvedValue(polWei),
    getFeeData: vi.fn().mockResolvedValue({
      maxPriorityFeePerGas: { lt: () => false, toString: () => '30000000000' },
      maxFeePerGas:         { lt: () => false, toString: () => '30000000000' },
    }),
  };
}

function makeWallet(address = '0xUserWallet') { return { address }; }

function makeCfg() {
  return {
    yaml: {
      contracts: {
        ctf_exchange:      '0x4bFb41d5B3570DeFd03C39a9A4D8dE6Bd8B8982E',
        neg_risk_exchange: '0xC5d563A36AE78145C45a50134d48A1215220f80a',
        usdc_e:            '0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174',
      },
      safety: { warn_threshold_usd: 50, confirm_threshold_usd: 500 },
    },
  };
}

function setupHappyPath({ usdceBal = '100.0' } = {}) {
  mockUsdceInstance.balanceOf.mockResolvedValue(
    ethers.utils.parseUnits(usdceBal, 6),
  );
  mockUsdceInstance.allowance.mockResolvedValue(
    ethers.utils.parseUnits('1000', 6), // sufficient allowance
  );
}

describe('buy() — dry-run', () => {
  it('returns { dryRun: true } without calling postOrder or approve', async () => {
    setupHappyPath();

    const result = await buy({
      market:   makeMarket(),
      side:     'YES',
      amount:   10,
      cfg:      makeCfg(),
      provider: makeProvider(),
      wallet:   makeWallet(),
      dryRun:   true,
    });

    expect(result).toMatchObject({ dryRun: true });
    expect(mockClientInstance.postOrder).not.toHaveBeenCalled();
    expect(mockUsdceSigned.approve).not.toHaveBeenCalled();
  });

  it('still calls createMarketOrder in dry-run (order construction is read-only)', async () => {
    setupHappyPath();

    await buy({
      market:   makeMarket(),
      side:     'YES',
      amount:   10,
      cfg:      makeCfg(),
      provider: makeProvider(),
      wallet:   makeWallet(),
      dryRun:   true,
    });

    expect(mockClientInstance.createMarketOrder).toHaveBeenCalledOnce();
  });

  it('skips safety gate confirm calls in dry-run', async () => {
    setupHappyPath({ usdceBal: '300.0' }); // sufficient for $200 buy

    // amount $200 would normally trigger warn gate
    await buy({
      market:   makeMarket(),
      side:     'YES',
      amount:   200,
      cfg:      makeCfg(),
      provider: makeProvider(),
      wallet:   makeWallet(),
      dryRun:   true,
    });

    expect(confirm).not.toHaveBeenCalled();
  });

  it('still enforces hard stops in dry-run (market closed)', async () => {
    setupHappyPath();

    await expect(
      buy({
        market:   makeMarket({ active: false }),
        side:     'YES',
        amount:   10,
        cfg:      makeCfg(),
        provider: makeProvider(),
        wallet:   makeWallet(),
        dryRun:   true,
      }),
    ).rejects.toThrow('CLOSED');
  });

  it('still enforces hard stops in dry-run (insufficient POL gas)', async () => {
    setupHappyPath(); // USDC.e sufficient, but POL < 0.01

    await expect(
      buy({
        market:   makeMarket(),
        side:     'YES',
        amount:   10,
        cfg:      makeCfg(),
        provider: makeProvider('0.005'), // 0.005 POL < 0.01 minimum
        wallet:   makeWallet(),
        dryRun:   true,
      }),
    ).rejects.toThrow('POL');
  });
});
