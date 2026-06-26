/**
 * BTC价格数据获取
 * 使用Binance API（免费，无需API Key）
 */

const BINANCE_API = 'https://api.binance.com';

/**
 * 获取BTC当前价格
 */
async function getCurrentPrice() {
  const url = `${BINANCE_API}/api/v3/ticker/price?symbol=BTCUSDT`;
  const resp = await fetch(url);
  const data = await resp.json();
  return parseFloat(data.price);
}

/**
 * 获取K线数据
 * @param {string} interval - K线周期: 1m, 5m, 15m, 1h, 4h, 1d
 * @param {number} limit - 返回数量
 */
async function getKlines(interval = '15m', limit = 50) {
  const url = `${BINANCE_API}/api/v3/klines?symbol=BTCUSDT&interval=${interval}&limit=${limit}`;
  const resp = await fetch(url);
  const data = await resp.json();
  
  return data.map(k => ({
    openTime: k[0],
    open: parseFloat(k[1]),
    high: parseFloat(k[2]),
    low: parseFloat(k[3]),
    close: parseFloat(k[4]),
    volume: parseFloat(k[5]),
    closeTime: k[6]
  }));
}

/**
 * 获取24小时行情
 */
async function get24hTicker() {
  const url = `${BINANCE_API}/api/v3/ticker/24hr?symbol=BTCUSDT`;
  const resp = await fetch(url);
  const data = await resp.json();
  
  return {
    priceChange: parseFloat(data.priceChange),
    priceChangePercent: parseFloat(data.priceChangePercent),
    volume: parseFloat(data.volume),
    quoteVolume: parseFloat(data.quoteVolume),
    highPrice: parseFloat(data.highPrice),
    lowPrice: parseFloat(data.lowPrice)
  };
}

module.exports = {
  getCurrentPrice,
  getKlines,
  get24hTicker
};
