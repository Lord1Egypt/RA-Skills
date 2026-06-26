#!/usr/bin/env node

const axios = require('axios');
const { spawn } = require('child_process');

const CONFIG = {
  skillpay_api: 'https://api.skillpay.me/v1',
  merchant_key: process.env.SKILLPAY_MERCHANT_KEY || 'sk_91fff75ae2a7a71f8eceadcbcd816e24d57e58d9d04ccca45f0b3856af130aea',
  price_per_use: 0.001,
  currency: 'USDT'
};

async function optimizeTitles(topic, options = {}) {
  const prompt = `You are Sloan, a content strategist. Generate 7 SEO-friendly blog titles about "${topic}".

Requirements:
- Mix of how-to, listicles, guides, and controversial takes
- Include power words (Ultimate, Complete, Essential, Proven)
- Optimal length: 50-60 characters
- Include numbers when appropriate
- Emotional hooks when relevant
${options.keywords ? `- Must include these keywords: ${options.keywords}` : ''}

Return ONLY the titles, numbered 1-7, no explanations.`;

  const result = await new Promise((resolve, reject) => {
    const child = spawn('openclaw', ['agent', '--agent', 'sloan', '-m', prompt], { encoding: 'utf-8', timeout: 60000 });
    let stdout = '';
    child.stdout.on('data', (d) => stdout += d);
    child.on('close', (code) => code === 0 ? resolve(stdout) : reject(new Error('Agent failed')));`,
    { encoding: 'utf-8', timeout: 60000, maxBuffer: 1024 * 1024 }
  );
  
  return { titles: result.trim() };
}

async function processPayment() {
  try {
    const response = await axios.post(`${CONFIG.skillpay_api}/billing/charge`, {
      amount: CONFIG.price_per_use,
      currency: CONFIG.currency,
      merchant_key: CONFIG.merchant_key,
      description: 'Blog title optimization by Sloan'
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
📝 Blog Title Optimizer
Powered by Sloan
━━━━━━━━━━━━━━━━━━━━

Usage:
  blog-title-optimizer <topic> [options]

Options:
  --keywords <keywords>  Target keywords (comma-separated)
  --test                 Test mode (skip payment)

Examples:
  blog-title-optimizer "how to build AI agents"
  blog-title-optimizer "AI tutorial" --keywords "beginners,2026"

Pricing: 0.001 USDT per generation
    `);
    process.exit(0);
  }
  
  const topic = args[0];
  const options = {
    keywords: args.includes('--keywords') ? args[args.indexOf('--keywords') + 1] : null,
    testMode: args.includes('--test')
  };
  
  console.log('📝 Blog Title Optimizer');
  console.log('━━━━━━━━━━━━━━━━━━━━\n');
  
  if (!options.testMode) {
    const payment = await processPayment();
    if (!payment.success) {
      console.log(`💳 Payment Required: ${payment.error}`);
      if (payment.payment_url) console.log(`Top up: ${payment.payment_url}`);
      process.exit(1);
    }
    console.log(`✅ Payment processed: ${payment.transaction_id}\n`);
  } else {
    console.log('🧪 Test mode\n');
  }
  
  console.log(`Optimizing titles for "${topic}"...\n`);
  
  const result = await optimizeTitles(topic, options);
  
  console.log('━━━━━━━━━━━━━━━━━━━━\n');
  console.log(result.titles);
  console.log('\n━━━━━━━━━━━━━━━━━━━━');
  console.log(`💰 Cost: ${CONFIG.price_per_use} ${CONFIG.currency}`);
}

const getArg = (args, flag, def) => {
  const i = args.indexOf(flag);
  return i === -1 || i + 1 >= args.length ? def : args[i + 1];
};

if (require.main === module) main().catch(console.error);
module.exports = { optimizeTitles, processPayment };
