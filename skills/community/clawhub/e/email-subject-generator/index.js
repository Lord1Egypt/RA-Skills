#!/usr/bin/env node

const axios = require('axios');
const { spawn } = require('child_process');

const CONFIG = {
  skillpay_api: 'https://api.skillpay.me/v1',
  merchant_key: process.env.SKILLPAY_MERCHANT_KEY || 'sk_91fff75ae2a7a71f8eceadcbcd816e24d57e58d9d04ccca45f0b3856af130aea',
  price_per_use: 0.001,
  currency: 'USDT'
};

async function generateSubjects(topic, options = {}) {
  const prompt = `You are Sloan, an email marketing expert. Generate 10 email subject lines for "${topic}".

Guidelines:
- Mix of curiosity, urgency, and benefit-driven
- Use power words: You, Free, New, Exclusive, Limited
- Optimal length: 40-50 characters
- Avoid spam triggers: FREE (caps), !!!, 100%
- Include numbers when relevant
- Personalization placeholders: {name}, {company}
${options.purpose ? `- Purpose: ${options.purpose}` : ''}

Return ONLY the subject lines, numbered 1-10, no explanations.`;

  const result = await new Promise((resolve, reject) => {
    const child = spawn('openclaw', ['agent', '--agent', 'sloan', '-m', prompt], {
      encoding: 'utf-8',
      timeout: 60000
    });
    let stdout = '';
    child.stdout.on('data', (d) => stdout += d);
    child.on('close', (code) => code === 0 ? resolve(stdout) : reject(new Error('Agent failed')));
  });
  
  return { subjects: result.trim() };
}

async function processPayment() {
  try {
    const response = await axios.post(`${CONFIG.skillpay_api}/billing/charge`, {
      amount: CONFIG.price_per_use,
      currency: CONFIG.currency,
      merchant_key: CONFIG.merchant_key,
      description: 'Email subject generation by Sloan'
    }, { headers: { 'Content-Type': 'application/json' }, timeout: 10000 });
    
    return { success: true, transaction_id: response.data.transaction_id || response.data.id };
  } catch (error) {
    return {
      success: false,
      error: error.response?.data?.message || error.message,
      payment_url: 'https://skillpay.me/topup'
    };
  }
}

async function main() {
  const args = process.argv.slice(2);
  
  if (args.length === 0 || args.includes('--help')) {
    console.log(`
📧 Email Subject Line Generator
Powered by Sloan
━━━━━━━━━━━━━━━━━━━━

Usage:
  email-subject-generator <topic> [options]

Options:
  --purpose <type>  Email purpose (newsletter, sales, announcement)
  --test            Test mode (skip payment)

Examples:
  email-subject-generator "product launch"
  email-subject-generator "weekly update" --purpose newsletter

Pricing: 0.001 USDT per generation
    `);
    process.exit(0);
  }
  
  const topic = args[0];
  const options = {
    purpose: args.includes('--purpose') ? args[args.indexOf('--purpose') + 1] : null,
    testMode: args.includes('--test')
  };
  
  console.log('📧 Email Subject Line Generator');
  console.log('━━━━━━━━━━━━━━━━━━━━\n');
  
  if (!options.testMode) {
    const payment = await processPayment();
    if (!payment.success) {
      console.log(`💳 Payment Required: ${payment.error}`);
      if (payment.payment_url) console.log(`Top up: ${payment.payment_url}`);
      process.exit(1);
    }
    console.log(`✅ Payment: ${payment.transaction_id}\n`);
  } else {
    console.log('🧪 Test mode\n');
  }
  
  console.log(`Generating subjects for "${topic}"...\n`);
  
  const result = await generateSubjects(topic, options);
  
  console.log('━━━━━━━━━━━━━━━━━━━━\n');
  console.log(result.subjects);
  console.log('\n━━━━━━━━━━━━━━━━━━━━');
  console.log(`💰 Cost: ${CONFIG.price_per_use} ${CONFIG.currency}`);
}

if (require.main === module) main().catch(console.error);
module.exports = { generateSubjects, processPayment };
