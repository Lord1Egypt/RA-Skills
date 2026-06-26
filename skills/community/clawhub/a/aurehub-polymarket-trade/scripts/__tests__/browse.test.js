import { vi, describe, it, expect, afterEach } from 'vitest';
import { formatMarketOutput, extractTokenIds, resolveMarket, search } from '../browse.js';

const mockMarket = {
  question: 'Will BTC reach $100k by Dec 2025?',
  active: true,
  neg_risk: false,
  tokens: [
    { outcome: 'Yes', token_id: '712345', price: 0.72 },
    { outcome: 'No',  token_id: '523456', price: 0.28 },
  ],
  min_incentive_size: '5',
};

const mockOrderbooks = {
  '712345': { bids: [{ price: '0.71', size: '100' }], asks: [{ price: '0.73', size: '200' }] },
  '523456': { bids: [{ price: '0.27', size: '80'  }], asks: [{ price: '0.29', size: '150' }] },
};

describe('formatMarketOutput', () => {
  it('includes market question', () => {
    const out = formatMarketOutput(mockMarket, mockOrderbooks);
    expect(out).toContain('Will BTC reach $100k');
  });

  it('shows YES and NO token prices', () => {
    const out = formatMarketOutput(mockMarket, mockOrderbooks);
    expect(out).toContain('YES');
    expect(out).toContain('NO');
    expect(out).toContain('0.72');
  });

  it('shows neg_risk flag', () => {
    const out = formatMarketOutput({ ...mockMarket, neg_risk: true }, mockOrderbooks);
    expect(out).toContain('neg_risk: true');
  });

  it('shows token IDs', () => {
    const out = formatMarketOutput(mockMarket, mockOrderbooks);
    expect(out).toContain('712345');
  });

  it('shows min order size', () => {
    const out = formatMarketOutput(mockMarket, mockOrderbooks);
    expect(out).toContain('Min order');
    expect(out).toContain('$5');
  });

  it('renders — fallbacks when orderbooks and marketInfo are missing', () => {
    const out = formatMarketOutput(mockMarket, {});
    expect(out).toContain('—');
    expect(out).toContain('Will BTC reach $100k');
  });

  it('shows best bid/ask (last entry) not worst (first entry) when orderbook has multiple levels', () => {
    // Polymarket bids sorted ascending (worst first), asks descending (worst first)
    // best bid = bids.at(-1), best ask = asks.at(-1)
    const deepOrderbooks = {
      '712345': {
        bids: [{ price: '0.01', size: '10' }, { price: '0.65', size: '50' }, { price: '0.71', size: '100' }],
        asks: [{ price: '0.99', size: '10' }, { price: '0.80', size: '50' }, { price: '0.73', size: '100' }],
      },
      '523456': { bids: [], asks: [] },
    };
    const out = formatMarketOutput(mockMarket, deepOrderbooks);
    expect(out).toContain('0.71'); // best bid
    expect(out).toContain('0.73'); // best ask
    expect(out).not.toContain('0.01'); // worst bid must not appear
    expect(out).not.toContain('0.99'); // worst ask must not appear
  });
});

describe('extractTokenIds', () => {
  it('returns YES and NO token IDs from tokens array (CLOB format)', () => {
    const ids = extractTokenIds(mockMarket);
    expect(ids.YES).toBe('712345');
    expect(ids.NO).toBe('523456');
  });

  it('returns YES and NO token IDs from clobTokenIds string (Gamma keyword format)', () => {
    const gammaMarket = {
      question: 'Will BTC hit 100k?',
      active: true,
      clobTokenIds: '["53135072abc","60869871def"]',
      outcomes: '["Yes","No"]',
    };
    const ids = extractTokenIds(gammaMarket);
    expect(ids.YES).toBe('53135072abc');
    expect(ids.NO).toBe('60869871def');
  });

  it('returns null/null when neither tokens nor clobTokenIds present', () => {
    const ids = extractTokenIds({ question: 'test', active: true });
    expect(ids.YES).toBeNull();
    expect(ids.NO).toBeNull();
  });
});

describe('formatMarketOutput with Gamma keyword format', () => {
  it('shows token IDs from clobTokenIds', () => {
    const gammaMarket = {
      question: 'Will BTC hit 100k?',
      active: true,
      neg_risk: false,
      clobTokenIds: '["53135072abc","60869871def"]',
      outcomes: '["Yes","No"]',
      outcomePrices: '["0.72","0.28"]',
      min_incentive_size: '5',
    };
    const out = formatMarketOutput(gammaMarket, {});
    expect(out).toContain('53135072abc');
    expect(out).toContain('60869871def');
  });

  it('shows prices from outcomePrices when tokens array absent', () => {
    const gammaMarket = {
      question: 'Will BTC hit 100k?',
      active: true,
      neg_risk: false,
      clobTokenIds: '["53135072abc","60869871def"]',
      outcomes: '["Yes","No"]',
      outcomePrices: '["0.72","0.28"]',
    };
    const out = formatMarketOutput(gammaMarket, {});
    expect(out).toContain('0.72');
    expect(out).toContain('0.28');
  });
});

// ── search (Events API path) ───────────────────────────────────────────────────

describe('search', () => {
  afterEach(() => vi.clearAllMocks());

  it('fetches events without q param and filters client-side by event title', async () => {
    const { default: axios } = await import('axios');
    const activeMarket = {
      question: 'Will BTC hit 100k by end of 2025?',
      active: true,
      closed: false,
      conditionId: 'cond123',
      clobTokenIds: '["tokenA","tokenB"]',
      outcomes: '["Yes","No"]',
      outcomePrices: '["0.65","0.35"]',
    };
    const closedMarket = { ...activeMarket, question: 'Old closed market', active: true, closed: true };
    const unrelatedMarket = { ...activeMarket, question: 'Will it rain tomorrow?' };
    axios.get.mockImplementation(url => {
      if (url.includes('/events')) return Promise.resolve({
        data: [
          { title: 'Bitcoin 2025 predictions', markets: [activeMarket, closedMarket] },
          { title: 'Weather forecasts', markets: [unrelatedMarket] },
        ],
      });
      return Promise.resolve({ data: {} });
    });
    const logSpy = vi.spyOn(console, 'log').mockImplementation(() => {});
    await search('bitcoin', { yaml: {} });
    const output = logSpy.mock.calls.map(c => c[0]).join('\n');
    expect(output).toContain('Will BTC hit 100k');
    expect(output).not.toContain('Old closed market');
    expect(output).not.toContain('Will it rain tomorrow');
    // Must NOT include q= in the URL — Gamma API ignores it
    expect(axios.get).toHaveBeenCalledWith(
      expect.stringContaining('/events?active=true&closed=false'),
      expect.any(Object),
    );
    expect(axios.get).not.toHaveBeenCalledWith(
      expect.stringContaining('?q='),
      expect.any(Object),
    );
    logSpy.mockRestore();
  });

  it('resolves conditionId directly via CLOB and displays market', async () => {
    const { default: axios } = await import('axios');
    const clobMarket = {
      question: 'Will BTC hit $100k?',
      active: true,
      condition_id: '0x' + 'a'.repeat(64),
      minimum_order_size: '5',
      tokens: [
        { token_id: 'tok-yes', outcome: 'Yes', price: 0.6 },
        { token_id: 'tok-no',  outcome: 'No',  price: 0.4 },
      ],
    };
    axios.get.mockImplementation(() => Promise.resolve({ data: clobMarket }));
    const logSpy = vi.spyOn(console, 'log').mockImplementation(() => {});
    await search('0x' + 'a'.repeat(64), { yaml: {} });
    const output = logSpy.mock.calls.map(c => c[0]).join('\n');
    expect(output).toContain('Will BTC hit $100k');
    // Must NOT call the events endpoint for a conditionId query
    expect(axios.get).not.toHaveBeenCalledWith(
      expect.stringContaining('/events'),
      expect.any(Object),
    );
    logSpy.mockRestore();
  });

  it('matches on market question when event title does not contain keyword', async () => {
    const { default: axios } = await import('axios');
    const btcMarket = {
      question: 'Will Bitcoin reach $200k in 2026?',
      active: true, closed: false, conditionId: 'cond-btc',
      clobTokenIds: '["t1","t2"]', outcomes: '["Yes","No"]', outcomePrices: '["0.3","0.7"]',
    };
    const unrelatedMarket = { ...btcMarket, question: 'Will Elon buy Twitter again?', conditionId: 'cond-elon' };
    axios.get.mockImplementation(url => {
      if (url.includes('/events')) return Promise.resolve({
        data: [{ title: 'Crypto markets 2026', markets: [btcMarket, unrelatedMarket] }],
      });
      return Promise.resolve({ data: {} });
    });
    const logSpy = vi.spyOn(console, 'log').mockImplementation(() => {});
    await search('bitcoin', { yaml: {} });
    const output = logSpy.mock.calls.map(c => c[0]).join('\n');
    expect(output).toContain('Will Bitcoin reach $200k');
    expect(output).not.toContain('Will Elon buy Twitter');
    logSpy.mockRestore();
  });
});

// ── resolveMarket ─────────────────────────────────────────────────────────────

vi.mock('axios', () => ({
  default: { get: vi.fn() },
}));

// Use a different name to avoid collision with the existing mockMarket const above
const mockSlugMarket = {
  question: 'Will BTC reach $100k by Dec 2025?',
  slug: 'bitcoin-100k-2025',
  active: true,
  tokens: [],
};

describe('resolveMarket', () => {
  afterEach(() => vi.clearAllMocks());

  it('returns market when exact slug found via ?slug= filter', async () => {
    const { default: axios } = await import('axios');
    axios.get.mockResolvedValue({ data: [mockSlugMarket] });
    const result = await resolveMarket('bitcoin-100k-2025', { yaml: {} });
    expect(result).toEqual(mockSlugMarket);
    expect(axios.get).toHaveBeenCalledWith(
      expect.stringContaining('markets?slug=bitcoin-100k-2025'),
      expect.any(Object),
    );
  });

  it('falls back to client-side keyword search when slug lookup returns empty array', async () => {
    const { default: axios } = await import('axios');
    axios.get
      .mockResolvedValueOnce({ data: [] })  // slug lookup → no match
      .mockResolvedValueOnce({ data: [{ title: 'Bitcoin 100k prediction', markets: [mockSlugMarket] }] }); // events fallback
    const result = await resolveMarket('bitcoin 100k', { yaml: {} });
    expect(result).toEqual(mockSlugMarket);
    expect(axios.get).toHaveBeenCalledWith(
      expect.stringContaining('/events?active=true&closed=false'),
      expect.any(Object),
    );
  });

  it('calls process.exit(1) and prints list when multiple results found', async () => {
    const { default: axios } = await import('axios');
    const exitSpy = vi.spyOn(process, 'exit').mockImplementation(() => { throw new Error('process.exit'); });
    const errSpy = vi.spyOn(console, 'error').mockImplementation(() => {});
    const market2 = { ...mockSlugMarket, slug: 'bitcoin-200k-2025', question: 'Will BTC reach $200k?' };
    axios.get
      .mockResolvedValueOnce({ data: [] })  // slug lookup → no match
      .mockResolvedValueOnce({ data: [{ title: 'Bitcoin predictions', markets: [mockSlugMarket, market2] }] }); // events fallback
    await expect(resolveMarket('bitcoin', { yaml: {} })).rejects.toThrow('process.exit');
    expect(exitSpy).toHaveBeenCalledWith(1);
    expect(errSpy).toHaveBeenCalledWith(expect.stringContaining('Found 2 markets matching "bitcoin"'));
    expect(errSpy).toHaveBeenCalledWith(expect.stringContaining('Specify the exact slug'));
    exitSpy.mockRestore();
    errSpy.mockRestore();
  });

  it('throws Market not found when keyword search returns no results', async () => {
    const { default: axios } = await import('axios');
    axios.get
      .mockResolvedValueOnce({ data: [] })   // slug lookup → no match
      .mockResolvedValueOnce({ data: [] });  // events fallback → no matching events
    await expect(resolveMarket('nonexistent-market', { yaml: {} })).rejects.toThrow('Market not found: nonexistent-market');
  });

  it('falls through slug error and propagates keyword search error', async () => {
    const { default: axios } = await import('axios');
    const err403 = Object.assign(new Error('Forbidden'), { response: { status: 403 } });
    axios.get
      .mockRejectedValueOnce(err403)   // slug lookup → any error, silently caught
      .mockRejectedValueOnce(err403);  // events fallback → 403 propagates
    await expect(resolveMarket('some-slug', { yaml: {} })).rejects.toThrow('Forbidden');
  });
});
