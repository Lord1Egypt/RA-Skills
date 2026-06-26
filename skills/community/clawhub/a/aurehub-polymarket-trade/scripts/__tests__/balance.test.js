import { vi, describe, it, expect, afterEach } from 'vitest';
import { formatBalances, fetchPositions } from '../balance.js';

vi.mock('axios', () => ({
  default: { get: vi.fn() },
}));

// ── formatBalances (existing tests, updated for toFixed(2) USDC.e) ────────────

describe('formatBalances', () => {
  it('formats address and all three balances', () => {
    const result = { address: '0xABC', pol: '0.1234', usdce: '100.000000', clob: '50.00', positions: [] };
    const out = formatBalances(result);
    expect(out).toContain('0xABC');
    expect(out).toContain('0.1234');
    expect(out).toContain('$100.00');   // toFixed(2) — was '100.000000'
    expect(out).toContain('50.00');
  });

  it('omits CLOB line when clob is null', () => {
    const result = { address: '0xABC', pol: '0.1234', usdce: '100.000000', clob: null, positions: [] };
    const out = formatBalances(result);
    expect(out).not.toContain('CLOB');
  });

  it('renders Positions section when positions present', () => {
    const b = {
      address: '0xabc', pol: '0.1000', usdce: '100.500000', clob: null,
      positions: [
        { outcome: 'YES', slug: 'bitcoin-100k-2025', size: '42.5', curPrice: '0.72', currentValue: '30.60' },
      ],
    };
    const out = formatBalances(b);
    expect(out).toContain('Positions');
    expect(out).toContain('YES');
    expect(out).toContain('bitcoin-100k-2025');
    expect(out).toContain('42.50');
  });

  it('omits Positions section when positions is empty', () => {
    const b = { address: '0xabc', pol: '0.1000', usdce: '100.00', clob: null, positions: [] };
    const out = formatBalances(b);
    expect(out).not.toContain('Positions');
  });

  it('formats USDC.e to 2 decimal places', () => {
    const b = { address: '0xabc', pol: '0.1000', usdce: '100.500000', clob: null, positions: [] };
    const out = formatBalances(b);
    expect(out).toContain('$100.50');
    expect(out).not.toContain('100.500000');
  });
});

// ── fetchPositions ────────────────────────────────────────────────────────────

describe('fetchPositions', () => {
  afterEach(() => vi.clearAllMocks());

  it('returns positions array on success', async () => {
    const { default: axios } = await import('axios');
    axios.get.mockResolvedValue({
      data: [
        { outcome: 'YES', slug: 'bitcoin-100k-2025', size: '42.5', curPrice: '0.72', currentValue: '30.60', title: 'Will BTC reach $100k?' },
      ],
    });
    const result = await fetchPositions('0xabc', { yaml: {} });
    expect(result).toHaveLength(1);
    expect(result[0].outcome).toBe('YES');
    expect(result[0].slug).toBe('bitcoin-100k-2025');
  });

  it('returns [] on network error (silent skip)', async () => {
    const { default: axios } = await import('axios');
    axios.get.mockRejectedValue(new Error('Network error'));
    const result = await fetchPositions('0xabc', { yaml: {} });
    expect(result).toEqual([]);
  });

  it('uses data_url from config when set', async () => {
    const { default: axios } = await import('axios');
    axios.get.mockResolvedValue({ data: [] });
    await fetchPositions('0xabc', { yaml: { polymarket: { data_url: 'https://custom.example.com' } } });
    expect(axios.get).toHaveBeenCalledWith(
      expect.stringContaining('https://custom.example.com'),
      expect.any(Object),
    );
  });
});
