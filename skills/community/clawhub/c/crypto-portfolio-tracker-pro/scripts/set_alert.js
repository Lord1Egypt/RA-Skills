#!/usr/bin/env node

/**
 * Price Alert System
 * Set alerts for cryptocurrency price movements
 */

const fs = require('fs');
const path = require('path');

const ALERTS_FILE = path.join(__dirname, '../references/alerts.json');

function loadAlerts() {
  if (!fs.existsSync(ALERTS_FILE)) {
    return [];
  }
  return JSON.parse(fs.readFileSync(ALERTS_FILE, 'utf8'));
}

function saveAlerts(alerts) {
  fs.writeFileSync(ALERTS_FILE, JSON.stringify(alerts, null, 2));
}

function setAlert(symbol, price, direction) {
  const alerts = loadAlerts();
  
  const alert = {
    id: Date.now(),
    symbol: symbol.toUpperCase(),
    price: parseFloat(price),
    direction: direction.toLowerCase(), // 'above' or 'below'
    created: new Date().toISOString(),
    active: true
  };
  
  alerts.push(alert);
  saveAlerts(alerts);
  
  console.log(`✅ Alert set: ${symbol} ${direction} $${price}`);
  console.log(`Alert ID: ${alert.id}`);
}

// Parse command line arguments
const args = process.argv.slice(2);
const symbolIdx = args.indexOf('--symbol');
const priceIdx = args.indexOf('--price');
const directionIdx = args.indexOf('--direction');

if (symbolIdx === -1 || priceIdx === -1 || directionIdx === -1) {
  console.error('Usage: node set_alert.js --symbol BTC --price 50000 --direction above');
  process.exit(1);
}

const symbol = args[symbolIdx + 1];
const price = args[priceIdx + 1];
const direction = args[directionIdx + 1];

setAlert(symbol, price, direction);
