#!/usr/bin/env node
/**
 * Crypto Price Alerts - Alert Manager
 */

const ccxt = require('ccxt');
const fs = require('fs');
const path = require('path');

const ALERTS_FILE = path.join(process.env.HOME, '.openclaw/workspace/data/price_alerts.json');

function loadAlerts() {
  try {
    if (fs.existsSync(ALERTS_FILE)) {
      return JSON.parse(fs.readFileSync(ALERTS_FILE, 'utf8'));
    }
  } catch (e) {}
  return [];
}

function saveAlerts(alerts) {
  const dir = path.dirname(ALERTS_FILE);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
  fs.writeFileSync(ALERTS_FILE, JSON.stringify(alerts, null, 2));
}

async function checkAlerts() {
  const alerts = loadAlerts();
  if (alerts.length === 0) {
    console.log(JSON.stringify({ message: 'No active alerts' }));
    return;
  }

  const exchange = new ccxt.binance();
  const triggered = [];

  for (const alert of alerts) {
    try {
      const ticker = await exchange.fetchTicker(alert.symbol);
      const currentPrice = ticker.last;

      let isTriggered = false;
      if (alert.condition === 'above' && currentPrice >= alert.targetPrice) {
        isTriggered = true;
      } else if (alert.condition === 'below' && currentPrice <= alert.targetPrice) {
        isTriggered = true;
      }

      if (isTriggered) {
        triggered.push({
          ...alert,
          currentPrice,
          triggeredAt: new Date().toISOString()
        });
      }
    } catch (e) {
      console.error(`Error checking ${alert.symbol}:`, e.message);
    }
  }

  if (triggered.length > 0) {
    // Remove triggered alerts
    const remaining = alerts.filter(a => 
      !triggered.some(t => t.id === a.id)
    );
    saveAlerts(remaining);

    console.log(JSON.stringify({
      triggered: triggered,
      message: `${triggered.length} alert(s) triggered!`
    }, null, 2));
  } else {
    console.log(JSON.stringify({ message: 'No alerts triggered' }));
  }
}

const action = process.argv[2];

if (action === 'check') {
  checkAlerts();
} else if (action === 'list') {
  const alerts = loadAlerts();
  console.log(JSON.stringify({ alerts }, null, 2));
} else if (action === 'add') {
  const symbol = process.argv[3];
  const condition = process.argv[4];
  const targetPrice = parseFloat(process.argv[5]);
  
  const alerts = loadAlerts();
  alerts.push({
    id: Date.now().toString(),
    symbol,
    condition,
    targetPrice,
    createdAt: new Date().toISOString()
  });
  saveAlerts(alerts);
  console.log(JSON.stringify({ message: 'Alert added', alerts }, null, 2));
} else if (action === 'remove') {
  const id = process.argv[3];
  let alerts = loadAlerts();
  alerts = alerts.filter(a => a.id !== id);
  saveAlerts(alerts);
  console.log(JSON.stringify({ message: 'Alert removed', alerts }, null, 2));
} else {
  console.log('Usage: node alert_manager.js [check|list|add|remove]');
}
