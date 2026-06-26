#!/usr/bin/env node
/**
 * Create receive order - standalone script
 */

import fs from 'fs';
import path from 'path';
import os from 'os';

const BASE_URL = process.env.BIOLIMS_URL || 'http://your-server/biolims';
const DATA_SOURCE = process.env.BIOLIMS_DS || 'your-datasource';
const TOKEN_CACHE_FILE = path.join(os.tmpdir(), 'biolims_token_node.json');

// Read token and xsrf
function loadAuth() {
  try {
    if (fs.existsSync(TOKEN_CACHE_FILE)) {
      const data = JSON.parse(fs.readFileSync(TOKEN_CACHE_FILE, 'utf8'));
      return {
        token: data.token,
        xsrf: data.xsrf,
        cookies: data.cookies
      };
    }
  } catch (e) {
    // ignore
  }
  return null;
}

async function createReceive() {
  const auth = loadAuth();
  if (!auth || !auth.token) {
    console.log(JSON.stringify({ error: 'No token found. Run order-list first.' }));
    process.exit(1);
  }

  const body = {
    sampleReceive: {
      id: "KXJY2602100001",
      name: "Sample Receive - Test",
      acceptDate: "2026-02-10 00:40",
      isBoard: "0"
    },
    sampleReceiveItems: [
      {
        barCode: "TEST-BARCODE-001",
        patientName: "Test Patient",
        dicSampleType: "cfDNA",
        dicSampleTypeId: "T251130001",
        productId: "CP2511240001",
        productName: "LymphDetect",
        sampleNum: "80",
        unit: "μL",
        isGood: "1",
        nextFlow: "Nucleic Acid Extraction",
        nextFlowId: "SYLX2024000001-NAE"
      }
    ]
  };

  const headers = {
    'Content-Type': 'application/json',
    'Token': auth.token,
    'X-DS': DATA_SOURCE
  };
  
  if (auth.xsrf) {
    headers['X-XSRF-TOKEN'] = auth.xsrf;
  }
  if (auth.cookies) {
    headers['Cookie'] = auth.cookies;
  }

  try {
    const response = await fetch(`${BASE_URL}/samplecenter/clinicalSampleReceive/saveOrUpdateAllData`, {
      method: 'POST',
      headers,
      body: JSON.stringify(body)
    });

    const result = await response.json();
    console.log(JSON.stringify(result, null, 2));
  } catch (err) {
    console.log(JSON.stringify({ error: err.message }));
  }
}

createReceive();
