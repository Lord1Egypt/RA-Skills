/**
 * Parse CLI arguments for trade.js.
 *
 * Usage patterns:
 *   spot buy|sell <COIN> <SIZE>
 *   perp open <COIN> long|short <SIZE> [--leverage N] [--cross|--isolated]
 *   perp close <COIN> <SIZE>
 *
 * @param {string[]} args  process.argv.slice(2)
 * @returns {{ mode, action, coin, size, direction, leverage, isCross, confirmed }}
 */
export function parseArgs(args) {
  const confirmed = args.includes('--confirmed');
  const cleanArgs = args.filter(a => a !== '--confirmed');
  const [mode, action, ...rest] = cleanArgs;

  if (!mode || !action) throw new Error('Usage: trade.js <spot|perp> <buy|sell|open|close> ...');

  if (mode === 'spot') {
    if (!['buy', 'sell'].includes(action)) throw new Error(`Unknown spot action: ${action}. Use buy or sell`);
    const [coin, sizeStr] = rest;
    if (!coin) throw new Error('Missing coin argument');
    if (!/^[A-Za-z0-9._/-]{1,20}$/.test(coin)) throw new Error(`Invalid coin format: ${coin}`);
    const size = parseFloat(sizeStr);
    if (!isFinite(size) || size <= 0) throw new Error(`Invalid size: ${sizeStr}`);
    return { mode: 'spot', action, coin, size, direction: null, leverage: null, isCross: true, confirmed };
  }

  if (mode === 'perp') {
    if (action === 'close') {
      const [coin, sizeStr] = rest;
      if (!coin) throw new Error('Missing coin argument');
      if (!/^[A-Za-z0-9._/-]{1,20}$/.test(coin)) throw new Error(`Invalid coin format: ${coin}`);
      const size = parseFloat(sizeStr);
      if (!isFinite(size) || size <= 0) throw new Error(`Invalid size: ${sizeStr}`);
      return { mode: 'perp', action: 'close', coin, size, direction: null, leverage: null, isCross: true, confirmed };
    }

    if (action === 'open') {
      const [coin, direction, sizeStr, ...flags] = rest;
      if (!coin) throw new Error('Missing coin argument');
      if (!/^[A-Za-z0-9._/-]{1,20}$/.test(coin)) throw new Error(`Invalid coin format: ${coin}`);
      if (!['long', 'short'].includes(direction)) throw new Error(`Direction must be long or short, got: ${direction}`);
      const size = parseFloat(sizeStr);
      if (!isFinite(size) || size <= 0) throw new Error(`Invalid size: ${sizeStr}`);

      let leverage = null;
      let isCross = true;
      for (let i = 0; i < flags.length; i++) {
        if (flags[i] === '--leverage' && flags[i + 1]) {
          leverage = parseInt(flags[++i], 10);
          if (isNaN(leverage)) throw new Error(`Invalid leverage value: ${flags[i]}`);
        }
        if (flags[i] === '--cross') isCross = true;
        if (flags[i] === '--isolated') isCross = false;
      }
      if (leverage !== null && (leverage < 1 || leverage > 100)) throw new Error(`Leverage must be between 1 and 100, got: ${leverage}`);
      return { mode: 'perp', action: 'open', coin, size, direction, leverage, isCross, confirmed };
    }
  }

  throw new Error(`Unknown mode/action: ${mode} ${action}`);
}

/**
 * Calculate IOC limit price with configurable slippage budget.
 * Buy: +slippagePct% above mid. Sell: -slippagePct% below mid.
 *
 * @param {boolean} isBuy
 * @param {number} mid  Mid price as a number
 * @param {number} [slippagePct=5]  Slippage percentage (e.g. 5 = 5%)
 * @returns {number}
 */
export function ioPrice(isBuy, mid, slippagePct = 5) {
  const offset = slippagePct / 100;
  return isBuy ? mid * (1 + offset) : mid * (1 - offset);
}

/**
 * Determine the closing order side from position size.
 * szi > 0 = long → close by selling (isBuy = false)
 * szi < 0 = short → close by buying (isBuy = true)
 *
 * @param {number} szi  Signed position size
 * @returns {boolean} isBuy
 */
export function closeDirection(szi) {
  return szi < 0;
}
