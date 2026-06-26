#!/usr/bin/env node
/**
 * Utility script: Scan barcode to add sample to receive order
 */

import crypto from 'crypto';
import fs from 'fs';
import path from 'path';
import os from 'os';

// Configuration
const BASE_URL = process.env.BIOLIMS_URL || 'http://your-server/biolims';
const USERNAME = process.env.BIOLIMS_USER || 'your-username';
const PASSWORD = process.env.BIOLIMS_PASSWORD || 'your-password-here';
const DATA_SOURCE = process.env.BIOLIMS_DS || 'your-datasource';
const SOLE_ID = crypto.randomUUID();

const AES_KEY = Buffer.from(process.env.BIOLIMS_AES_KEY || 'your-16byte-key!', 'utf8');
const AES_IV = Buffer.from(process.env.BIOLIMS_AES_IV || 'your-16byte-iv!!', 'utf8');
const SECRET_KEY = process.env.BIOLIMS_SECRET || 'your-secret-key';

function encryptPassword(password) {
  const timestamp = Date.now();
  const data = JSON.stringify({
    password,
    captCode: '',
    time: timestamp,
    secretKey: SECRET_KEY
  });

  const cipher = crypto.createCipheriv('aes-128-cbc', AES_KEY, AES_IV);
  let encrypted = cipher.update(data, 'utf8', 'base64');
  encrypted += cipher.final('base64');
  return encrypted;
}

async function login() {
  const encryptedPassword = encryptPassword(PASSWORD);
  const urlEncodedPassword = encodeURIComponent(encryptedPassword);
  const loginUrl = `${BASE_URL}/user/Login?username=${USERNAME}&password=${urlEncodedPassword}`;

  console.error('Logging in...');
  const response = await fetch(loginUrl, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'code': DATA_SOURCE,
      'X-DS': DATA_SOURCE,
      'accept-language': 'zh_CN',
      'X-Sole-ID': SOLE_ID
    }
  });

  const result = await response.json();
  console.error('Login response:', JSON.stringify(result));
  
  if (result.status === 200 && result.data) {
    return result.data.token;
  }
  throw new Error(`Login failed: ${result.msg || 'Unknown error'}`);
}

async function apiCall(method, endpoint, body, token) {
  const url = `${BASE_URL}${endpoint}`;
  
  const options = {
    method,
    headers: {
      'Content-Type': 'application/json',
      'code': DATA_SOURCE,
      'X-DS': DATA_SOURCE,
      'token': token,
      'accept-language': 'zh_CN',
      'X-Sole-ID': SOLE_ID
    }
  };

  if (body !== undefined) {
    options.body = typeof body === 'string' ? body : JSON.stringify(body);
  }

  console.error('API call:', url);
  const response = await fetch(url, options);
  return await response.json();
}

// Main logic
async function main() {
  const barcode = process.argv[2];
  const receiveId = process.argv[3];

  if (!barcode || !receiveId) {
    console.log(JSON.stringify({ error: 'Usage: node scan-sample.mjs <barcode> <receive_id>' }));
    process.exit(1);
  }

  // Login to get a new token first
  const token = await login();
  console.error('Got token:', token ? token.substring(0, 20) + '...' : 'null');

  // Call scanBarcode
  const body = { 
    sampleReceive: {
      id: receiveId,
      name: 'Sample Receive for DB2602100003',
      acceptDate: '2026-02-10 02:40',
      isBoard: '0'
    },
    barCode: barcode
  };

  const result = await apiCall('POST', '/samplecenter/clinicalSampleReceive/scanBarcode', body, token);
  console.log(JSON.stringify(result, null, 2));
}

main().catch(err => {
  console.log(JSON.stringify({ error: err.message }));
  process.exit(1);
});
