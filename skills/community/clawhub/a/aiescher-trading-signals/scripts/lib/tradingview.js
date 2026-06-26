const TradingView = require('@mathieuc/tradingview');

function fetchWithIndicators(symbol, timeframe = '60', range = 50) {
  return new Promise((resolve, reject) => {
    const client = new TradingView.Client();
    const chart = new client.Session.Chart();
    let resolved = false;

    const timer = setTimeout(() => {
      if (!resolved) {
        resolved = true;
        chart.delete();
        client.end();
        reject(new Error('Timeout'));
      }
    }, 15000);

    chart.setMarket(symbol, { timeframe, range });

    chart.onError((...err) => {
      if (!resolved) {
        resolved = true;
        clearTimeout(timer);
        chart.delete();
        client.end();
        reject(new Error(err.join(' ')));
      }
    });

    chart.onUpdate(() => {
      if (!chart.periods || chart.periods.length < 2 || resolved) return;
      resolved = true;
      clearTimeout(timer);
      
      const periods = chart.periods;
      const latest = periods[0];
      const previous = periods[1];
      
      const result = {
        symbol,
        name: chart.infos.description || symbol,
        currency: chart.infos.currency_id || '',
        price: latest.close,
        open: latest.open,
        high: latest.high,
        low: latest.low,
        volume: latest.volume,
        change: latest.close && previous.close ? ((latest.close - previous.close) / previous.close) * 100 : 0,
        timestamp: new Date(latest.time * 1000).toISOString(),
        periods
      };
      
      chart.delete();
      client.end();
      resolve(result);
    });
  });
}

module.exports = { fetchWithIndicators };
