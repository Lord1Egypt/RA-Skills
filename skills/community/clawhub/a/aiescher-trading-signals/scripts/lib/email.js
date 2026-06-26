const https = require('https');
const fs = require('fs');

function sendEmail(to, subject, htmlBody) {
  const credentialsPath = process.env.HOME + '/.config/resend/credentials.json';
  
  if (!fs.existsSync(credentialsPath)) {
    return Promise.reject(new Error('Resend credentials not found'));
  }
  
  const credentials = JSON.parse(fs.readFileSync(credentialsPath, 'utf8'));
  const apiKey = credentials.api_key;

  const payload = JSON.stringify({
    from: 'noreply@resend.dev',
    to: [to],
    subject: subject,
    html: htmlBody
  });

  return new Promise((resolve, reject) => {
    const req = https.request({
      hostname: 'api.resend.com',
      path: '/emails',
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${apiKey}`,
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(payload)
      }
    }, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          resolve(JSON.parse(data));
        } else {
          reject(new Error(`HTTP ${res.statusCode}: ${data}`));
        }
      });
    });
    req.on('error', reject);
    req.write(payload);
    req.end();
  });
}

function formatSignalsEmail(results, title = 'Trading Signals') {
  const now = new Date().toLocaleString('de-DE');
  
  let html = `<!DOCTYPE html>
<html>
<head>
<style>
body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 800px; margin: 0 auto; }
h1 { color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }
h2 { color: #34495e; margin-top: 30px; }
table { border-collapse: collapse; width: 100%; margin: 15px 0; }
th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }
th { background-color: #3498db; color: white; }
tr:nth-child(even) { background-color: #f2f2f2; }
.buy { color: #27ae60; font-weight: bold; }
.sell { color: #e74c3c; font-weight: bold; }
.strong { background-color: #fff3cd; }
.medium { background-color: #e8f5e9; }
.weak { background-color: #f3e5f5; }
.footer { margin-top: 40px; padding-top: 20px; border-top: 1px solid #ddd; color: #7f8c8d; font-size: 0.9em; }
</style>
</head>
<body>
<h1>📈 ${title}</h1>
<p><strong>Erstellt:</strong> ${now}</p>
`;

  // Summary
  const allSignals = results.flatMap(r => r.signals.map(s => ({ ...s, asset: r.name, symbol: r.symbol })));
  const buySignals = allSignals.filter(s => s.type === 'BUY');
  const sellSignals = allSignals.filter(s => s.type === 'SELL');
  
  html += '<h2>📊 Signal-Übersicht</h2>';
  html += `<p><span class="buy">🟢 Kauf-Signale: ${buySignals.length}</span> | <span class="sell">🔴 Verkauf-Signale: ${sellSignals.length}</span></p>`;
  
  if (allSignals.length > 0) {
    html += '<table><tr><th>Asset</th><th>Typ</th><th>Grund</th><th>Stärke</th></tr>';
    
    // Sort by strength: strong first
    const strengthOrder = { strong: 0, medium: 1, weak: 2 };
    allSignals.sort((a, b) => strengthOrder[a.strength] - strengthOrder[b.strength]);
    
    for (const signal of allSignals) {
      const typeClass = signal.type === 'BUY' ? 'buy' : 'sell';
      const strengthClass = signal.strength;
      html += `<tr class="${strengthClass}"><td>${signal.asset}</td><td class="${typeClass}">${signal.type}</td><td>${signal.reason}</td><td>${signal.strength}</td></tr>`;
    }
    html += '</table>';
  }
  
  // Detailed analysis
  html += '<h2>📉 Detaillierte Analyse</h2>';
  for (const result of results) {
    html += `<h3>${result.name} (${result.symbol})</h3>`;
    html += `<p><strong>Preis:</strong> ${result.price?.toFixed(2) || 'n/a'} (${result.change?.toFixed(2) || 0}%)</p>`;
    html += `<p><strong>RSI:</strong> ${result.rsi?.toFixed(1) || 'n/a'} | <strong>SMA20:</strong> ${result.sma20?.toFixed(2) || 'n/a'} | <strong>SMA50:</strong> ${result.sma50?.toFixed(2) || 'n/a'}</p>`;
    
    if (result.signals.length > 0) {
      html += '<ul>';
      for (const signal of result.signals) {
        const emoji = signal.type === 'BUY' ? '🟢' : '🔴';
        html += `<li>${emoji} <strong>${signal.type}</strong> - ${signal.reason} (${signal.strength})</li>`;
      }
      html += '</ul>';
    } else {
      html += '<p>✅ Keine klaren Signale</p>';
    }
  }
  
  html += `<div class="footer">
    <p>Report generiert: ${now}</p>
    <p>Escher – Trading Signal Assistant</p>
  </div>`;
  
  html += '</body></html>';
  return html;
}

module.exports = { sendEmail, formatSignalsEmail };
