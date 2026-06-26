#!/usr/bin/env node
/**
 * generate-pi.js — Proforma Invoice Generator
 *
 * Generates a structured PI from product catalog and order details.
 * Usage: node generate-pi.js --buyer "Company" --products "prod-001:5,prod-002:2" --terms "FOB Shanghai"
 */

import { readFileSync, writeFileSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const CATALOG_PATH = join(__dirname, '..', 'catalog.json');

function loadCatalog() {
  return JSON.parse(readFileSync(CATALOG_PATH, 'utf-8'));
}

function findProduct(catalog, productId) {
  for (const category of catalog.categories) {
    const product = category.products.find(p => p.id === productId);
    if (product) return { ...product, category: category.name };
  }
  return null;
}

function generatePI({ buyer, items, terms, currency = 'USD', validDays = 15 }) {
  const catalog = loadCatalog();
  const today = new Date().toISOString().split('T')[0];
  const piNumber = `PI-${Date.now().toString(36).toUpperCase()}`;

  const lineItems = items.map(({ productId, quantity }, index) => {
    const product = findProduct(catalog, productId);
    if (!product) return { error: `Product not found: ${productId}` };

    return {
      no: index + 1,
      product: product.name,
      model: product.model,
      description: product.description,
      quantity,
      unit_price: '(To be quoted)',
      total: '(To be quoted)',
      lead_time: `${product.lead_time_days} days`,
    };
  });

  const pi = {
    document: 'PROFORMA INVOICE',
    pi_number: piNumber,
    date: today,
    valid_until: new Date(Date.now() + validDays * 86400000).toISOString().split('T')[0],
    seller: {
      company: catalog.company || '{{company_name}}',
      address: '{{company_address}}',
      contact: '{{sales_contact}}',
    },
    buyer: {
      company: buyer,
      address: '(To be filled)',
      contact: '(To be filled)',
    },
    currency,
    items: lineItems,
    terms: {
      trade: terms,
      payment: catalog.payment_terms?.[0] || 'T/T 30% + 70%',
      shipping: `${Math.max(...items.map(i => findProduct(catalog, i.productId)?.lead_time_days || 30))} days after deposit`,
    },
    notes: [
      'Prices subject to confirmation at time of order.',
      'Bank details will be provided upon order confirmation.',
      `This PI is valid for ${validDays} days.`,
    ],
  };

  return pi;
}

// CLI
const args = process.argv.slice(2);
function getArg(name) {
  const idx = args.indexOf(`--${name}`);
  return idx >= 0 ? args[idx + 1] : null;
}

const buyer = getArg('buyer') || 'Sample Buyer Co.';
const productsStr = getArg('products') || 'prod-001:1';
const terms = getArg('terms') || 'FOB';

const items = productsStr.split(',').map(p => {
  const [productId, qty] = p.split(':');
  return { productId, quantity: parseInt(qty) || 1 };
});

const pi = generatePI({ buyer, items, terms });
const output = JSON.stringify(pi, null, 2);
console.log(output);

const outFile = getArg('output');
if (outFile) {
  writeFileSync(outFile, output);
  console.error(`\nSaved to: ${outFile}`);
}
