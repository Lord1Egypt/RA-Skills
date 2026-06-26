import { describe, it, expect } from 'vitest';
import { parseLimitArgs } from '../limit-order.js';

describe('parseLimitArgs — place', () => {
  it('parses spot buy', () => {
    expect(parseLimitArgs(['place', 'spot', 'buy', 'ETH', '3000', '0.1'])).toEqual({
      subcommand: 'place', mode: 'spot', action: 'buy', coin: 'ETH',
      price: 3000, size: 0.1, leverage: null, isCross: true,
      orderId: null, newPrice: null, newSize: null, confirmed: false, reduceOnly: false, triggerPrice: null, tpsl: null,
    });
  });

  it('parses spot sell', () => {
    expect(parseLimitArgs(['place', 'spot', 'sell', 'BTC', '50000', '0.05'])).toMatchObject({
      subcommand: 'place', mode: 'spot', action: 'sell', coin: 'BTC',
      price: 50000, size: 0.05,
    });
  });

  it('parses perp long with leverage and --isolated', () => {
    const r = parseLimitArgs(['place', 'perp', 'long', 'ETH', '3000', '0.1', '--leverage', '10', '--isolated']);
    expect(r).toMatchObject({
      subcommand: 'place', mode: 'perp', action: 'long', coin: 'ETH',
      price: 3000, size: 0.1, leverage: 10, isCross: false,
    });
  });

  it('parses perp short with --cross (default)', () => {
    const r = parseLimitArgs(['place', 'perp', 'short', 'BTC', '60000', '0.01']);
    expect(r.action).toBe('short');
    expect(r.isCross).toBe(true);
    expect(r.leverage).toBeNull();
  });

  it('sets reduceOnly=true when --reduce-only flag is present', () => {
    const r = parseLimitArgs(['place', 'perp', 'short', 'ETH', '3500', '0.1', '--reduce-only', '--confirmed']);
    expect(r.reduceOnly).toBe(true);
    expect(r.confirmed).toBe(true);
  });

  it('strips --reduce-only from positional args', () => {
    const r = parseLimitArgs(['place', 'spot', 'sell', 'ETH', '3000', '0.1', '--reduce-only']);
    expect(r).toMatchObject({ action: 'sell', coin: 'ETH', price: 3000, size: 0.1, reduceOnly: true });
  });

  it('parses trigger order with --trigger-price and --sl', () => {
    const r = parseLimitArgs(['place', 'perp', 'short', 'ETH', '3200', '0.1', '--trigger-price', '3056', '--sl', '--reduce-only', '--confirmed']);
    expect(r).toMatchObject({
      subcommand: 'place', mode: 'perp', action: 'short', coin: 'ETH',
      price: 3200, size: 0.1, triggerPrice: 3056, tpsl: 'sl',
      reduceOnly: true, confirmed: true,
    });
  });

  it('parses trigger order with --tp', () => {
    const r = parseLimitArgs(['place', 'perp', 'short', 'ETH', '3200', '0.1', '--trigger-price', '3408', '--tp', '--reduce-only']);
    expect(r).toMatchObject({ triggerPrice: 3408, tpsl: 'tp', reduceOnly: true });
  });

  it('throws when --trigger-price is used without --tp or --sl', () => {
    expect(() => parseLimitArgs(['place', 'perp', 'short', 'ETH', '3200', '0.1', '--trigger-price', '3056'])).toThrow(/--tp or --sl/);
  });

  it('throws when --tp is used without --trigger-price', () => {
    expect(() => parseLimitArgs(['place', 'perp', 'short', 'ETH', '3200', '0.1', '--tp'])).toThrow(/--trigger-price/);
  });

  it('throws when both --tp and --sl are used', () => {
    expect(() => parseLimitArgs(['place', 'perp', 'short', 'ETH', '3200', '0.1', '--trigger-price', '3056', '--tp', '--sl'])).toThrow(/both/);
  });

  it('throws on invalid trigger price', () => {
    expect(() => parseLimitArgs(['place', 'perp', 'short', 'ETH', '3200', '0.1', '--trigger-price', '0', '--sl'])).toThrow(/trigger price/i);
  });

  it('throws on invalid price (zero)', () => {
    expect(() => parseLimitArgs(['place', 'spot', 'buy', 'ETH', '0', '0.1'])).toThrow(/price/i);
  });

  it('throws on invalid size (negative)', () => {
    expect(() => parseLimitArgs(['place', 'spot', 'buy', 'ETH', '3000', '-1'])).toThrow(/size/i);
  });

  it('throws on missing coin', () => {
    expect(() => parseLimitArgs(['place', 'spot', 'buy'])).toThrow(/coin/i);
  });

  it('throws on leverage out of range', () => {
    expect(() => parseLimitArgs(['place', 'perp', 'long', 'ETH', '3000', '0.1', '--leverage', '0'])).toThrow(/leverage/i);
  });

  it('throws on unknown spot action', () => {
    expect(() => parseLimitArgs(['place', 'spot', 'hold', 'ETH', '3000', '0.1'])).toThrow(/action/i);
  });

  it('throws on unknown perp direction', () => {
    expect(() => parseLimitArgs(['place', 'perp', 'both', 'ETH', '3000', '0.1'])).toThrow(/direction/i);
  });
});

describe('parseLimitArgs — list', () => {
  it('parses list with no args', () => {
    expect(parseLimitArgs(['list'])).toMatchObject({ subcommand: 'list', coin: null });
  });

  it('parses list --coin ETH', () => {
    expect(parseLimitArgs(['list', '--coin', 'ETH'])).toMatchObject({ subcommand: 'list', coin: 'ETH' });
  });

  it('throws on invalid --coin format', () => {
    expect(() => parseLimitArgs(['list', '--coin', '!!!'])).toThrow(/coin/i);
  });
});

describe('parseLimitArgs — --confirmed flag', () => {
  it('sets confirmed=true for place with --confirmed', () => {
    const r = parseLimitArgs(['place', 'spot', 'buy', 'ETH', '3000', '0.1', '--confirmed']);
    expect(r.confirmed).toBe(true);
    expect(r.coin).toBe('ETH');
    expect(r.size).toBe(0.1);
  });

  it('sets confirmed=true for modify with --confirmed', () => {
    const r = parseLimitArgs(['modify', '99', '--price', '2900', '--confirmed']);
    expect(r.confirmed).toBe(true);
    expect(r.orderId).toBe(99);
    expect(r.newPrice).toBe(2900);
  });

  it('defaults confirmed=false when --confirmed is absent', () => {
    expect(parseLimitArgs(['place', 'spot', 'buy', 'ETH', '3000', '0.1']).confirmed).toBe(false);
  });
});

describe('parseLimitArgs — cancel', () => {
  it('parses cancel with orderId', () => {
    expect(parseLimitArgs(['cancel', '12345'])).toMatchObject({
      subcommand: 'cancel', orderId: 12345,
    });
  });

  it('throws on missing orderId', () => {
    expect(() => parseLimitArgs(['cancel'])).toThrow(/orderId/i);
  });

  it('throws on non-integer orderId', () => {
    expect(() => parseLimitArgs(['cancel', 'abc'])).toThrow(/orderId/i);
  });
});

describe('parseLimitArgs — modify', () => {
  it('parses modify with --price only', () => {
    expect(parseLimitArgs(['modify', '99', '--price', '2900'])).toMatchObject({
      subcommand: 'modify', orderId: 99, newPrice: 2900, newSize: null,
    });
  });

  it('parses modify with --price and --size', () => {
    expect(parseLimitArgs(['modify', '99', '--price', '2900', '--size', '0.2'])).toMatchObject({
      subcommand: 'modify', orderId: 99, newPrice: 2900, newSize: 0.2,
    });
  });

  it('throws on missing --price', () => {
    expect(() => parseLimitArgs(['modify', '99'])).toThrow(/--price/i);
  });

  it('throws on invalid --price (zero)', () => {
    expect(() => parseLimitArgs(['modify', '99', '--price', '0'])).toThrow(/price/i);
  });

  it('throws on non-integer orderId', () => {
    expect(() => parseLimitArgs(['modify', '1.5', '--price', '2900'])).toThrow(/orderId/i);
  });
});

describe('parseLimitArgs — unknown subcommand', () => {
  it('throws on unknown subcommand', () => {
    expect(() => parseLimitArgs(['bogus'])).toThrow(/subcommand/i);
  });

  it('throws on empty args', () => {
    expect(() => parseLimitArgs([])).toThrow();
  });
});
