const path = require('path');

class CryptoAlertAggregator {
  constructor() {
    this.alerts = [];
    this.listeners = [];
    this.config = {
      cryptoApiKey: process.env.CRYPTO_API_KEY || '',
      twitterApiKey: process.env.TWITTER_API_KEY || '',
      alertWebhook: process.env.ALERT_WEBHOOK || '',
      updateInterval: 60000
    };
  }

  async getAlerts(options = {}) {
    const {
      assets = ['BTC', 'ETH'],
      minVolumeDelta = 0.15,
      twitterSentimentThreshold = 0.6
    } = options;

    const alerts = [];

    for (const asset of assets) {
      const marketData = await this._fetchMarketData(asset);
      const twitterSignal = await this._fetchTwitterSignal(asset);

      if (marketData && marketData.volumeDelta > minVolumeDelta) {
        alerts.push({
          timestamp: new Date().toISOString(),
          asset,
          type: 'volume_spike',
          value: marketData.price,
          change: marketData.priceChange,
          twitterMentions: twitterSignal.mentions,
          sentiment: twitterSignal.sentiment,
          confidence: this._calculateConfidence(marketData, twitterSignal),
          message: `${asset} volume spike detected: ${marketData.volumeDelta.toFixed(2)}% increase`
        });
      }

      if (twitterSignal.sentiment > twitterSentimentThreshold) {
        alerts.push({
          timestamp: new Date().toISOString(),
          asset,
          type: 'sentiment_shift',
          value: marketData.price,
          twitterMentions: twitterSignal.mentions,
          sentiment: twitterSignal.sentiment,
          confidence: twitterSignal.confidence,
          message: `${asset} positive sentiment detected on Twitter (${(twitterSignal.sentiment * 100).toFixed(1)}%)`
        });
      }
    }

    return alerts;
  }

  streamAlerts(callback) {
    this.listeners.push(callback);
    this._startPolling();
  }

  async _fetchMarketData(asset) {
    try {
      if (!this.config.cryptoApiKey) {
        return this._mockMarketData(asset);
      }
      // Placeholder for actual API call
      return this._mockMarketData(asset);
    } catch (err) {
      console.error(`Failed to fetch market data for ${asset}:`, err.message);
      return null;
    }
  }

  async _fetchTwitterSignal(asset) {
    try {
      if (!this.config.twitterApiKey) {
        return this._mockTwitterSignal(asset);
      }
      // Placeholder for actual API call
      return this._mockTwitterSignal(asset);
    } catch (err) {
      console.error(`Failed to fetch Twitter signal for ${asset}:`, err.message);
      return null;
    }
  }

  _mockMarketData(asset) {
    return {
      asset,
      price: Math.random() * 50000 + 20000,
      priceChange: (Math.random() - 0.5) * 10,
      volumeDelta: Math.random() * 0.5,
      timestamp: new Date().toISOString()
    };
  }

  _mockTwitterSignal(asset) {
    return {
      asset,
      mentions: Math.floor(Math.random() * 5000),
      sentiment: Math.random(),
      confidence: 0.7 + Math.random() * 0.3,
      timestamp: new Date().toISOString()
    };
  }

  _calculateConfidence(marketData, twitterSignal) {
    if (!marketData || !twitterSignal) return 0;
    const marketConfidence = Math.min(Math.abs(marketData.volumeDelta) * 2, 1);
    const socialConfidence = twitterSignal.confidence || 0.5;
    return (marketConfidence + socialConfidence) / 2;
  }

  _startPolling() {
    setInterval(async () => {
      const alerts = await this.getAlerts();
      this.listeners.forEach(listener => {
        alerts.forEach(alert => listener(alert));
      });
    }, this.config.updateInterval);
  }

  async main() {
    console.log('Crypto Alert Aggregator initialized');
    return { status: 'ok', version: '1.0.0' };
  }
}

module.exports = new CryptoAlertAggregator();
