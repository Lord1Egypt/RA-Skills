#!/usr/bin/env node
/**
 * biolims-client.mjs - Lightweight HTTP client
 *
 * Usage:
 *   node biolims-client.mjs /status
 *   node biolims-client.mjs /order-list?page=1&rows=10
 *   node biolims-client.mjs /order/DB2602060003
 */

const endpoint = process.argv[2] || '/status';
const url = `http://localhost:3847${endpoint.startsWith('/') ? '' : '/'}${endpoint}`;

fetch(url)
  .then(r => r.text())
  .then(console.log)
  .catch(e => console.error('Error:', e.message));
