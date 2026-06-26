/**
 * Binance Trading Skill
 * Supports spot and futures trading
 */

const https = require("https");
const crypto = require("crypto");

// Binance API Configuration (使用环境变量)
const API_KEY = process.env.BINANCE_API_KEY || "";
const SECRET_KEY = process.env.BINANCE_SECRET_KEY || "";

// API Endpoints
const SPOT_API = "https://api.binance.com";
const FUTURES_API = "https://fapi.binance.com";

// Generate signature
function sign(queryString, secret) {
  return crypto.createHmac("sha256", secret).update(queryString).digest("hex");
}

// Make request
function request(url, method = "GET", data = null, needSign = true) {
  return new Promise((resolve, reject) => {
    const urlObj = new URL(url);
    let query = urlObj.search || "";
    
    if (needSign) {
      const params = new URLSearchParams();
      if (data) {
        for (const [key, value] of Object.entries(data)) {
          params.append(key, value);
        }
      }
      params.append("timestamp", Date.now());
      const signature = sign(params.toString(), SECRET_KEY);
      params.append("signature", signature);
      query = "?" + params.toString();
    } else if (data) {
      query = "?" + new URLSearchParams(data).toString();
    }
    
    const options = {
      hostname: urlObj.hostname,
      port: 443,
      path: urlObj.pathname + query,
      method: method,
      headers: {
        "Content-Type": "application/json",
        "X-MBX-APIKEY": API_KEY
      }
    };
    
    const req = https.request(options, (res) => {
      let body = "";
      res.on("data", chunk => body += chunk);
      res.on("end", () => {
        try {
          const json = JSON.parse(body);
          resolve({ ok: res.statusCode === 200, status: res.statusCode, data: json });
        } catch (e) {
          resolve({ ok: res.statusCode === 200, status: res.statusCode, data: body });
        }
      });
    });
    
    req.on("error", reject);
    if (data && !needSign) req.write(JSON.stringify(data));
    req.end();
  });
}

const binance_tools = {
  // ========== Spot API ==========
  
  // Get account balance (spot)
  binance_spot_balance: async (params) => {
    try {
      const res = await request(`${SPOT_API}/api/v3/account`, "GET", null, true);
      if (!res.ok) return { content: [{ type: "text", text: `Error: ${res.data.msg || "Unknown"}` }], details: { success: false } };
      
      const balances = res.data.balances
        .filter(b => parseFloat(b.free) > 0 || parseFloat(b.locked) > 0)
        .map(b => `${b.asset}: ${parseFloat(b.free).toFixed(6)} (free) / ${parseFloat(b.locked).toFixed(6)} (locked)`)
        .join("\n");
      
      return {
        content: [{ type: "text", text: `Spot Account Balance:\n\n${balances || "No balance"}` }],
        details: { success: true, balances: res.data.balances }
      };
    } catch (e) {
      return { content: [{ type: "text", text: `Error: ${e.message}` }], details: { success: false } };
    }
  },
  
  // Spot ticker
  binance_spot_ticker: async (params) => {
    try {
      const { symbol = "BTCUSDT" } = params;
      const res = await request(`${SPOT_API}/api/v3/ticker/24hr`, "GET", { symbol: symbol.toUpperCase() }, false);
      if (!res.ok) return { content: [{ type: "text", text: `Error: ${res.data.msg}` }], details: { success: false } };
      
      const t = res.data;
      return {
        content: [{ type: "text", text: `${symbol} Spot Ticker:\n\nPrice: ${t.lastPrice}\n24h Change: ${t.priceChangePercent}%\nHigh: ${t.highPrice}\nLow: ${t.lowPrice}\nVolume: ${t.volume}` }],
        details: { success: true, ticker: res.data }
      };
    } catch (e) {
      return { content: [{ type: "text", text: `Error: ${e.message}` }], details: { success: false } };
    }
  },
  
  // Place spot order
  binance_spot_order: async (params) => {
    try {
      const { symbol, side, type = "MARKET", quantity, price } = params;
      if (!symbol || !side || !quantity) {
        return { content: [{ type: "text", text: "Missing params: symbol, side, quantity" }], details: { success: false } };
      }
      
      const data = {
        symbol: symbol.toUpperCase(),
        side: side.toUpperCase(),
        type: type.toUpperCase(),
        quantity: parseFloat(quantity)
      };
      
      if (price && type === "LIMIT") {
        data.price = parseFloat(price);
        data.timeInForce = "GTC";
      }
      
      const res = await request(`${SPOT_API}/api/v3/order`, "POST", data, true);
      if (!res.ok) return { content: [{ type: "text", text: `Order failed: ${res.data.msg}` }], details: { success: false } };
      
      return {
        content: [{ type: "text", text: `Spot Order Success!\n\nOrder ID: ${res.data.orderId}\nSymbol: ${res.data.symbol}\nSide: ${res.data.side}\nQuantity: ${res.data.executedQty}` }],
        details: { success: true, order: res.data }
      };
    } catch (e) {
      return { content: [{ type: "text", text: `Order failed: ${e.message}` }], details: { success: false } };
    }
  },
  
  // Get spot open orders
  binance_spot_orders: async (params) => {
    try {
      const { symbol } = params;
      const data = symbol ? { symbol: symbol.toUpperCase() } : {};
      const res = await request(`${SPOT_API}/api/v3/openOrders`, "GET", data, true);
      if (!res.ok) return { content: [{ type: "text", text: `Error: ${res.data.msg}` }], details: { success: false } };
      
      if (res.data.length === 0) {
        return { content: [{ type: "text", text: "No open spot orders" }], details: { success: true } };
      }
      
      const orders = res.data.map(o => `${o.symbol} ${o.side} ${o.type} ${o.origQty} @ ${o.price || "MARKET"}`).join("\n");
      return { content: [{ type: "text", text: `Open Spot Orders:\n\n${orders}` }], details: { success: true, orders: res.data } };
    } catch (e) {
      return { content: [{ type: "text", text: `Error: ${e.message}` }], details: { success: false } };
    }
  },
  
  // ========== Futures API ==========
  
  // Futures account balance
  binance_futures_balance: async (params) => {
    try {
      const res = await request(`${FUTURES_API}/fapi/v2/account`, "GET", null, true);
      if (!res.ok) return { content: [{ type: "text", text: `Error: ${res.data.msg || "Unknown"}` }], details: { success: false } };
      
      const total = parseFloat(res.data.totalWalletBalance);
      const unrealized = parseFloat(res.data.totalUnrealizedProfit);
      
      return {
        content: [{ type: "text", text: `Futures Account:\n\nTotal: ${total} USDT\nUnrealized PnL: ${unrealized} USDT` }],
        details: { success: true, balance: res.data }
      };
    } catch (e) {
      return { content: [{ type: "text", text: `Error: ${e.message}` }], details: { success: false } };
    }
  },
  
  // Futures ticker
  binance_futures_ticker: async (params) => {
    try {
      const { symbol = "BTCUSDT" } = params;
      const res = await request(`${FUTURES_API}/fapi/v1/ticker/24hr`, "GET", { symbol: symbol.toUpperCase() }, false);
      if (!res.ok) return { content: [{ type: "text", text: `Error: ${res.data.msg}` }], details: { success: false } };
      
      const t = res.data;
      return {
        content: [{ type: "text", text: `${symbol} Futures Ticker:\n\nPrice: ${t.lastPrice}\n24h Change: ${t.priceChangePercent}%\nHigh: ${t.highPrice}\nLow: ${t.lowPrice}\nVolume: ${t.volume}\nFunding Rate: ${t.fundingRate}` }],
        details: { success: true, ticker: res.data }
      };
    } catch (e) {
      return { content: [{ type: "text", text: `Error: ${e.message}` }], details: { success: false } };
    }
  },
  
  // Place futures order
  binance_futures_order: async (params) => {
    try {
      const { symbol, side, positionSide = "BOTH", type = "MARKET", quantity, price, stopPrice } = params;
      if (!symbol || !side || !quantity) {
        return { content: [{ type: "text", text: "Missing params: symbol, side, quantity" }], details: { success: false } };
      }
      
      const data = {
        symbol: symbol.toUpperCase(),
        side: side.toUpperCase(),
        positionSide: positionSide.toUpperCase(),
        type: type.toUpperCase(),
        quantity: parseFloat(quantity)
      };
      
      if (price && type !== "MARKET") {
        data.price = parseFloat(price);
        data.timeInForce = "GTC";
      }
      
      if (stopPrice) {
        data.stopPrice = parseFloat(stopPrice);
      }
      
      const res = await request(`${FUTURES_API}/fapi/v1/order`, "POST", data, true);
      if (!res.ok) return { content: [{ type: "text", text: `Order failed: ${res.data.msg}` }], details: { success: false } };
      
      return {
        content: [{ type: "text", text: `Futures Order Success!\n\nOrder ID: ${res.data.orderId}\nSymbol: ${res.data.symbol}\nSide: ${res.data.side} (${res.data.positionSide})\nQuantity: ${res.data.origQty}` }],
        details: { success: true, order: res.data }
      };
    } catch (e) {
      return { content: [{ type: "text", text: `Order failed: ${e.message}` }], details: { success: false } };
    }
  },
  
  // Get futures positions
  binance_futures_positions: async (params) => {
    try {
      const res = await request(`${FUTURES_API}/fapi/v2/positionRisk`, "GET", null, true);
      if (!res.ok) return { content: [{ type: "text", text: `Error: ${res.data.msg}` }], details: { success: false } };
      
      const positions = res.data.filter(p => parseFloat(p.positionAmt) !== 0);
      if (positions.length === 0) {
        return { content: [{ type: "text", text: "No open futures positions" }], details: { success: true } };
      }
      
      const text = positions.map(p => {
        const pnl = parseFloat(p.unrealizedProfit).toFixed(2);
        return `${p.symbol} ${p.positionSide}\n  Qty: ${p.positionAmt} | Entry: ${p.entryPrice}\n  PnL: ${pnl} USDT`;
      }).join("\n\n");
      
      return { content: [{ type: "text", text: `Futures Positions:\n\n${text}` }], details: { success: true, positions } };
    } catch (e) {
      return { content: [{ type: "text", text: `Error: ${e.message}` }], details: { success: false } };
    }
  },
  
  // Get futures open orders
  binance_futures_open_orders: async (params) => {
    try {
      const res = await request(`${FUTURES_API}/fapi/v1/openOrders`, "GET", null, true);
      if (!res.ok) return { content: [{ type: "text", text: `Error: ${res.data.msg}` }], details: { success: false } };
      
      if (res.data.length === 0) {
        return { content: [{ type: "text", text: "No open futures orders" }], details: { success: true } };
      }
      
      const orders = res.data.map(o => `${o.symbol} ${o.side} ${o.type} ${o.origQty} @ ${o.price || "MARKET"}`).join("\n");
      return { content: [{ type: "text", text: `Open Futures Orders:\n\n${orders}` }], details: { success: true, orders: res.data } };
    } catch (e) {
      return { content: [{ type: "text", text: `Error: ${e.message}` }], details: { success: false } };
    }
  },
  
  // Get order book
  binance_futures_book: async (params) => {
    try {
      const { symbol = "BTCUSDT", limit = 20 } = params;
      const res = await request(`${FUTURES_API}/fapi/v1/depth`, "GET", { symbol: symbol.toUpperCase(), limit }, false);
      if (!res.ok) return { content: [{ type: "text", text: `Error: ${res.data.msg}` }], details: { success: false } };
      
      const bids = res.data.bids.slice(0, 5).map(b => `${b[0]} @ ${b[1]}`).join("\n");
      const asks = res.data.asks.slice(0, 5).map(a => `${a[0]} @ ${a[1]}`).join("\n");
      
      return {
        content: [{ type: "text", text: `${symbol.toUpperCase()} Order Book:\n\nBids:\n${bids}\n\nAsks:\n${asks}` }],
        details: { success: true, bids: res.data.bids, asks: res.data.asks }
      };
    } catch (e) {
      return { content: [{ type: "text", text: `Error: ${e.message}` }], details: { success: false } };
    }
  },
  
  // Set leverage
  binance_futures_leverage: async (params) => {
    try {
      const { symbol, leverage } = params;
      if (!symbol || !leverage) {
        return { content: [{ type: "text", text: "Missing params: symbol, leverage" }], details: { success: false } };
      }
      
      const res = await request(`${FUTURES_API}/fapi/v1/leverage`, "POST", {
        symbol: symbol.toUpperCase(),
        leverage: parseInt(leverage)
      }, true);
      
      if (!res.ok) return { content: [{ type: "text", text: `Error: ${res.data.msg}` }], details: { success: false } };
      
      return { content: [{ type: "text", text: `${symbol.toUpperCase()} leverage set to ${leverage}x` }], details: { success: true } };
    } catch (e) {
      return { content: [{ type: "text", text: `Error: ${e.message}` }], details: { success: false } };
    }
  },
  
  // Close futures position
  binance_futures_close: async (params) => {
    try {
      const { symbol, positionSide = "BOTH" } = params;
      if (!symbol) return { content: [{ type: "text", text: "Need symbol" }], details: { success: false } };
      
      const posRes = await request(`${FUTURES_API}/fapi/v2/positionRisk`, "GET", { symbol: symbol.toUpperCase() }, true);
      if (!posRes.ok) return { content: [{ type: "text", text: "Failed to get position" }], details: { success: false } };
      
      const position = posRes.data.find(p => p.symbol === symbol.toUpperCase() && parseFloat(p.positionAmt) !== 0);
      if (!position) return { content: [{ type: "text", text: "No position" }], details: { success: false } };
      
      const amount = Math.abs(parseFloat(position.positionAmt));
      const side = parseFloat(position.positionAmt) > 0 ? "SELL" : "BUY";
      
      const res = await request(`${FUTURES_API}/fapi/v1/order`, "POST", {
        symbol: symbol.toUpperCase(),
        side: side,
        positionSide: positionSide.toUpperCase(),
        type: "MARKET",
        quantity: amount,
        reduceOnly: true
      }, true);
      
      if (!res.ok) return { content: [{ type: "text", text: `Close failed: ${res.data.msg}` }], details: { success: false } };
      
      return { content: [{ type: "text", text: `${symbol.toUpperCase()} closed! Qty: ${amount}` }], details: { success: true } };
    } catch (e) {
      return { content: [{ type: "text", text: `Close failed: ${e.message}` }], details: { success: false } };
    }
  },
  
  // ========== General ==========
  
  // Test connection
  binance_ping: async (params) => {
    try {
      const spotRes = await request(`${SPOT_API}/api/v3/ping`, "GET", null, false);
      const futuresRes = await request(`${FUTURES_API}/fapi/v1/ping`, "GET", null, false);
      
      return {
        content: [{ type: "text", text: `Binance Connection:\n\nSpot: ${spotRes.ok ? "OK" : "Failed"}\nFutures: ${futuresRes.ok ? "OK" : "Failed"}` }],
        details: { success: spotRes.ok && futuresRes.ok, spot: spotRes.ok, futures: futuresRes.ok }
      };
    } catch (e) {
      return { content: [{ type: "text", text: `Connection failed: ${e.message}` }], details: { success: false } };
    }
  },
  
  // Get klines
  binance_kline: async (params) => {
    try {
      const { symbol = "BTCUSDT", interval = "1h", limit = 100 } = params;
      const res = await request(`${SPOT_API}/api/v3/klines`, "GET", {
        symbol: symbol.toUpperCase(),
        interval,
        limit
      }, false);
      
      if (!res.ok) return { content: [{ type: "text", text: "Failed to get klines" }], details: { success: false } };
      
      const klines = res.data.slice(-5).map(k => ({
        time: new Date(k[0]).toLocaleString(),
        open: k[1],
        high: k[2],
        low: k[3],
        close: k[4],
        volume: k[5]
      }));
      
      let text = `${symbol.toUpperCase()} Klines (${interval}):\n\n`;
      klines.forEach(k => {
        text += `${k.time} | O: ${k.open} H: ${k.high} L: ${k.low} C: ${k.close}\n`;
      });
      
      return { content: [{ type: "text", text }], details: { success: true, klines } };
    } catch (e) {
      return { content: [{ type: "text", text: `Error: ${e.message}` }], details: { success: false } };
    }
  }
};

module.exports = { binance_tools };
