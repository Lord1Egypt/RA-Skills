import express from 'express';
import cors from 'cors';
import axios from 'axios';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const PORT = 3000;

app.use(cors());
app.use(express.json());
app.use(express.static('public'));

const SIGNALS_FILE = path.join(process.env.HOME, 'apex-ia-skill', 'sinais.json');

// ============================================
// API: Preços em tempo real
// ============================================
app.get('/api/prices', async (req, res) => {
  try {
    const symbols = ['BTCUSDT', 'ETHUSDT', 'BCHUSDT', 'SOLUSDT', 'ADAUSDT', 'LTCUSDT', 'LINKUSDT'];
    const prices = {};
    
    for (const symbol of symbols) {
      const response = await axios.get(`https://api.binance.com/api/v3/ticker/24hr?symbol=${symbol}`);
      prices[symbol] = {
        price: parseFloat(response.data.lastPrice),
        change24h: parseFloat(response.data.priceChangePercent),
        volume: parseFloat(response.data.volume),
        high: parseFloat(response.data.highPrice),
        low: parseFloat(response.data.lowPrice)
      };
    }
    
    res.json(prices);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// ============================================
// API: Klines para gráfico
// ============================================
app.get('/api/klines', async (req, res) => {
  const { symbol = 'BTCUSDT', interval = '1h', limit = 50 } = req.query;
  try {
    const response = await axios.get(`https://api.binance.com/api/v3/klines`, {
      params: { symbol, interval, limit }
    });
    const klines = response.data.map(k => ({
      time: k[0],
      open: parseFloat(k[1]),
      high: parseFloat(k[2]),
      low: parseFloat(k[3]),
      close: parseFloat(k[4]),
      volume: parseFloat(k[5])
    }));
    res.json(klines);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// ============================================
// API: Sinais salvos
// ============================================
app.get('/api/signals', (req, res) => {
  try {
    if (fs.existsSync(SIGNALS_FILE)) {
      const signals = JSON.parse(fs.readFileSync(SIGNALS_FILE, 'utf-8'));
      res.json(signals.slice(-50).reverse());
    } else {
      res.json([]);
    }
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// ============================================
// API: Scan manual
// ============================================
function calcSMA(data, length) {
  const sma = [];
  for (let i = length - 1; i < data.length; i++) {
    const sum = data.slice(i - length + 1, i + 1).reduce((a, b) => a + b, 0);
    sma.push(sum / length);
  }
  return sma;
}

app.get('/api/scan', async (req, res) => {
  try {
    const symbols = ['BTCUSDT', 'ETHUSDT', 'BCHUSDT', 'SOLUSDT', 'ADAUSDT'];
    const results = [];
    
    for (const symbol of symbols) {
      const response = await axios.get(`https://api.binance.com/api/v3/klines`, {
        params: { symbol, interval: '1h', limit: 100 }
      });
      const closes = response.data.map(k => parseFloat(k[4]));
      
      const sma8 = calcSMA(closes, 8);
      const sma21 = calcSMA(closes, 21);
      
      if (sma8.length >= 2 && sma21.length >= 2) {
        const curr8 = sma8[sma8.length - 1];
        const curr21 = sma21[sma21.length - 1];
        const prev8 = sma8[sma8.length - 2];
        const prev21 = sma21[sma21.length - 2];
        
        const crossUp = prev8 <= prev21 && curr8 > curr21;
        const crossDown = prev8 >= prev21 && curr8 < curr21;
        const trend = curr8 > curr21 ? 'bullish' : 'bearish';
        const price = closes[closes.length - 1];
        
        results.push({ symbol, trend, price, crossUp, crossDown });
      } else {
        results.push({ symbol, error: 'Dados insuficientes' });
      }
    }
    
    res.json(results);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// ============================================
// Iniciar servidor
// ============================================
app.listen(PORT, () => {
  console.log(`\n🦞 APEX IA WebApp rodando em:`);
  console.log(`   🌐 http://localhost:${PORT}\n`);
});
