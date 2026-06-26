const express = require('express');
const { auditCode } = require('./audit');

const app = express();
app.use(express.json({ limit: '2mb' }));

// Health check
app.get('/health', (req, res) => {
  res.json({ status: 'ok', service: 'code-audit', price: '$0.25/scan' });
});

// x402 Payment Required middleware
// In production, use @x402/express. For now, we check x402-payment header.
function requirePayment(req, res, next) {
  // Check for x402 payment header or query param
  const payment = req.headers['x402-payment'] || req.query.payment;
  
  if (!payment) {
    res.status(402).json({
      error: 'payment_required',
      service: 'code-audit',
      price: '$0.25',
      instructions: 'Include x402-payment header or ?payment=1 to authorize $0.25 charge'
    });
    return;
  }
  
  // In full x402 impl: verify payment token, extract amount
  // For now: assume payment = "1" means authorized
  next();
}

// Main audit endpoint
app.post('/audit', requirePayment, async (req, res) => {
  try {
    const { code, language } = req.body;
    
    if (!code || typeof code !== 'string') {
      res.status(400).json({ error: 'missing_code', message: 'Provide code to audit' });
      return;
    }
    
    if (code.length > 500000) {
      res.status(400).json({ error: 'code_too_large', message: 'Max 500KB' });
      return;
    }
    
    const result = await auditCode(code, language || 'python');
    res.json(result);
  } catch (e) {
    res.status(500).json({ error: 'audit_failed', message: e.message });
  }
});

// Convenience: open webhook for agents
app.post('/webhook', requirePayment, async (req, res) => {
  const result = await auditCode(req.body.code || '', req.body.language);
  res.json(result);
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Code Audit service listening on port ${PORT}`);
  console.log(`Price: $0.25 per scan`);
});

module.exports = app;