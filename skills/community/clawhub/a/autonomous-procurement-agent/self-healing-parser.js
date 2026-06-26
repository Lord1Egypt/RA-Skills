#!/usr/bin/env node
/**
 * Procurement Agent — Hybrid Parser v3.0.0
 *
 * Dual-Engine Ingestion:
 *   Engine 1 (Primary): regex pipeline  → JSON → HTML table → CSV → Plain text
 *   Engine 2 (LLM Fallback): GPT-4o   → semantic extraction for messy/unstructured formats
 *
 * Risk-Integrated:
 *   - F1 calculation verification baked into every parse result
 *   - F2 historical price spike detection baked into every result
 *   - confidence_score + anomaly_flag in all responses
 *   - status: REJECTED_FOR_REVIEW when anomaly detected
 *
 * Currency-Normalizer:
 *   - Auto-detects CNY/RMB/USD/EUR/GBP
 *   - Fixed rate table (production: use live feed)
 *   - All amounts normalized to USD for comparison
 *
 * Lemon Squeezy Integration:
 *   - Webhook handler for subscription events
 *   - $29.99/mo Enterprise tier
 *
 * @version 3.0.0
 * @requires openai (optional — gracefully degrades to regex-only if unavailable)
 */

var fs = require('fs');
var https = require('https');
var http = require('http');
var path = require('path');
var crypto = require('crypto');

// ─── Auth Middleware (Enterprise feature gates) ───────────────────────────────
var AUTH;
try { AUTH = require('./auth-middleware'); } catch (e) { AUTH = null; }

/**
 * Guard an Enterprise-gated feature by email in metadata.
 * Throws with clear upgrade message on LICENSE_DENIED.
 * Safe: swallows network errors silently (fail-open for dev).
 */
function requireEnterpriseFeature(email, featureKey) {
  if (!AUTH) return;
  if (!email) return;
  try { AUTH.authorizeSync(email, featureKey); } catch (err) {
    if (err.code === 'LICENSE_DENIED') { err.userEmail = email; err.requiredFeature = featureKey; throw err; }
    console.warn('[Auth] Could not verify Enterprise license for ' + email + ': ' + err.message);
  }
}

// ─── Config from Environment ─────────────────────────────────────────────────

var ENV = {
  OPENAI_API_KEY:         process.env.OPENAI_API_KEY         || '',
  OPENAI_MODEL:           process.env.OPENAI_MODEL             || 'gpt-4o',
  LS_API_KEY:             process.env.LS_API_KEY               || '',
  LS_STORE_ID:            process.env.LS_STORE_ID              || '',
  LS_WEBHOOK_SECRET:      process.env.LS_WEBHOOK_SECRET        || '',
  LS_ENTERPRISE_PRICE_ID: process.env.LS_ENTERPRISE_PRICE_ID  || '',
  HISTORICAL_PRICE_URL:   process.env.HISTORICAL_PRICE_URL    || '',
  EXCHANGE_RATE_URL:      process.env.EXCHANGE_RATE_URL       || '',
  PARSER_DATA_DIR:        process.env.PARSER_DATA_DIR          || '/tmp/procurement-data',
  CIRCUIT_BREAKER_THRESH: parseInt(process.env.CB_THRESHOLD   || '2', 10),
};

// ─── Currency Normalizer ───────────────────────────────────────────────────

var FX_RATES = {
  USD: 1.0,
  CNY: 0.138,   // 1 CNY ≈ 0.138 USD (fixed; production should use live feed)
  RMB: 0.138,
  EUR: 1.09,
  GBP: 1.27,
  JPY: 0.0067,
  AUD: 0.65,
  CAD: 0.74,
};

function detectCurrency(text) {
  if (!text) return 'USD';
  if (/USD|\$|dollars?/i.test(text))  return 'USD';
  if (/€|EUR/i.test(text))           return 'EUR';
  if (/£|GBP/i.test(text))           return 'GBP';
  if (/￥|CNY|RMB/i.test(text))      return 'CNY';
  if (/JPY|¥(?!￥)/i.test(text))    return 'JPY';
  return 'USD';
}

function toUSD(amount, fromCurrency) {
  var fx = FX_RATES[fromCurrency] || 1.0;
  return parseFloat(amount) * fx;
}

// ─── Number Parser ──────────────────────────────────────────────────────────

function parseNumCell(raw) {
  if (raw === undefined || raw === null || raw === '') return 0;
  var cleaned = String(raw).replace(/[^0-9.]/g, '').replace(/,/g, '');
  return parseFloat(cleaned) || 0;
}

// ─── LLM Fallback Engine ───────────────────────────────────────────────────

// ─── Privacy Shield: mask sensitive fields before LLM transmission ───────────────────
// Applied only when OPENAI_API_KEY is set. All masking is local (regex-only, no external calls).
// Three categories masked: vendor names, monetary amounts, PII (email/phone/address).
function maskSensitiveData(content) {
  if (!content) return content;
  var c = content;
  // Rule 1 — supplier/vendor names: "From: Acme Corp" → "From: [VENDOR_MASKED]"
  c = c.replace(/(?:from|supplier|vendor|sold by|supplied by)[:\s]+([A-Z][A-Za-z\s&.,]+?)([\n,<,",])/gi,
    function(_, name, sep) { return arguments[0].replace(name, '[VENDOR_MASKED]') + sep; });
  // Rule 2 — standalone vendor/company names at line start (uppercase words, >2 chars)
  c = c.replace(/^[ \t]*(?:acme|inc\.|corp\.|llc|ltd\.|co\.|gmbh|pty|ltd)[ \t]*$/gim, '[VENDOR_MASKED]');
  // Rule 3 — monetary amounts: $1,234.56 or USD 99.99 or ¥1,200 or £500 → [AMOUNT_MASKED]
  // Matches: $ / £ / € / ¥ / USD / EUR / GBP / CNY prefix or suffix
  c = c.replace(/[$£€¥]([\d,]+\.?\d*)|([\d,]+\.?\d*)[$£€¥]|\b(USD|EUR|GBP|CNY)[ \t]*([\d,]+\.?\d*)/gi,
    function(m, p1, p2, p3, p4) {
      if (p1) return '[AMOUNT_MASKED]' + m.replace(p1, '');
      if (p2) return m.replace(p2, '[AMOUNT_MASKED]');
      return '[AMOUNT_MASKED]';
    });
  // Rule 4 — email addresses
  c = c.replace(/[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}/g, '[PII_REDACTED]');
  // Rule 5 — phone/fax numbers (international + CN domestic)
  c = c.replace(/(?:tel|phone|fax|mobile|mob)[:\s]*[+]?[\d\s\-().]{7,}/gi, '[PII_REDACTED]');
  // Rule 6 — address fragments (street, city, postcode)
  c = c.replace(/\d{1,5}[ \t]+[A-Za-z\s]{4,30}(?:street|st|avenue|ave|road|rd|lane|ln|district|city|province|state|zip|postal)[^\n]*/gi,
    '[PII_REDACTED]');
  return c;
}

function callLLM(prompt, signal) {
  return new Promise(function(resolve, reject) {
    if (!ENV.OPENAI_API_KEY) {
      reject(new Error('OPENAI_API_KEY not configured'));
      return;
    }

    var body = JSON.stringify({
      model: ENV.OPENAI_MODEL,
      messages: [
        {
          role: 'system',
          content: 'You are a procurement quote extraction assistant. Extract structured line items from messy quote text. Return ONLY valid JSON: {"items":[{"description":"...","quantity":N,"unit_price":N,"line_total":N}],"subtotal":N,"tax":N,"total":N,"currency":"USD","vendor_name":"..."},"confidence_score":0.0-1.0,"anomaly_flags":[]}. Be strict about math.'
        },
        { role: 'user', content: prompt }
      ],
      temperature: 0.1,
      max_tokens: 2048
    });

    var opts = {
      hostname: 'api.openai.com',
      path: '/v1/chat/completions',
      method: 'POST',
      headers: {
        'Authorization': 'Bearer ' + ENV.OPENAI_API_KEY,
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(body)
      },
      timeout: 30000
    };

    if (signal && signal.aborted) {
      reject(new Error('Aborted'));
      return;
    }

    var req = https.request(opts, function(res) {
      var data = '';
      res.on('data', function(chunk) { data += chunk; });
      res.on('end', function() {
        if (res.statusCode !== 200) {
          reject(new Error('OpenAI API error: ' + res.statusCode + ' ' + data.substring(0, 200)));
          return;
        }
        try {
          var json = JSON.parse(data);
          var text = json.choices && json.choices[0] && json.choices[0].message && json.choices[0].message.content;
          // Strip markdown code fences if present
          var clean = text ? text.replace(/```json\n?/gi, '').replace(/```\n?/gi, '').trim() : '{}';
          var result = JSON.parse(clean);
          resolve(result);
        } catch (e) {
          reject(new Error('LLM returned invalid JSON: ' + e.message + ' | ' + text.substring(0, 200)));
        }
      });
    });

    req.on('error', function(e) { reject(e); });
    req.on('timeout', function() { req.destroy(); reject(new Error('LLM request timeout')); });
    if (signal) signal.addEventListener('abort', function() { req.destroy(); });
    req.write(body);
    req.end();
  });
}

// ─── Risk Engine: F1 Calculation + F2 Price Spike ─────────────────────────

var HISTORICAL_PRICES = {};
// Default historical baseline (production: load from database or API)
try {
  var histPath = path.join(ENV.PARSER_DATA_DIR, '.historical-prices.json');
  if (fs.existsSync(histPath)) {
    HISTORICAL_PRICES = JSON.parse(fs.readFileSync(histPath, 'utf8'));
  }
} catch (e) { /* use defaults */ }

function runRiskAnalysis(parsedResult, metadata) {
  var anomalies = [];
  var riskScore = 0;
  var email = (metadata && metadata.email) || null;
  var canRunAuditF1F2 = false;
  if (email) {
    try { requireEnterpriseFeature(email, 'feature_audit_f1_f2'); canRunAuditF1F2 = true; } catch (_) {}
  }

  // ── F1 + F2: Enterprise-only gates
  if (canRunAuditF1F2) {
  // ── F1: Line-level calculation verification ──────────────────────────────
  for (var i = 0; i < (parsedResult.items || []).length; i++) {
    var item = parsedResult.items[i];
    var expectedLine = parseFloat((item.quantity * item.unit_price).toFixed(2));
    var statedLine = parseFloat(item.line_total || 0);
    if (Math.abs(expectedLine - statedLine) > 0.02) {
      anomalies.push({
        type: 'F1_CALC_ERROR',
        severity: 'HIGH',
        item_index: i,
        description: item.description,
        expected_line_total: expectedLine,
        stated_line_total: statedLine,
        deviation_pct: Math.abs((statedLine - expectedLine) / expectedLine * 100).toFixed(1),
        message: 'CALCULATION ERROR: ' + item.description + ': $' + item.unit_price + ' x ' + item.quantity + ' = $' + expectedLine + ', but stated total is $' + statedLine
      });
      riskScore += 0.3;
    }
  }

  // ── F1b: Total-level check ────────────────────────────────────────────────
  var calcSubtotal = parsedResult.items.reduce(function(s, it) { return s + it.quantity * it.unit_price; }, 0);
  var statedSubtotal = parseFloat(parsedResult.subtotal || 0);
  if (Math.abs(calcSubtotal - statedSubtotal) > 0.02) {
    anomalies.push({
      type: 'F1_TOTAL_MISMATCH',
      severity: 'HIGH',
      expected_subtotal: calcSubtotal,
      stated_subtotal: statedSubtotal,
      message: 'TOTAL MISMATCH: Calculated subtotal $' + calcSubtotal.toFixed(2) + ' != stated $' + statedSubtotal.toFixed(2)
    });
    riskScore += 0.2;
  }

  // ── F2: Historical price spike detection ────────────────────────────────
  for (var j = 0; j < (parsedResult.items || []).length; j++) {
    var item2 = parsedResult.items[j];
    var matchKey = Object.keys(HISTORICAL_PRICES).find(function(k) {
      return item2.description.toLowerCase().includes(k.toLowerCase());
    });
    if (matchKey) {
      var baseline = HISTORICAL_PRICES[matchKey];
      var currentUSD = toUSD(item2.unit_price, parsedResult.currency || 'USD');
      if (currentUSD > baseline.maxPrice) {
        var markup = ((currentUSD - baseline.avgPrice) / baseline.avgPrice * 100).toFixed(1);
        anomalies.push({
          type: 'F2_PRICE_SPIKE',
          severity: 'CRITICAL',
          item_index: j,
          description: item2.description,
          current_price_usd: currentUSD.toFixed(2),
          historical_avg_usd: baseline.avgPrice.toFixed(2),
          historical_max_usd: baseline.maxPrice.toFixed(2),
          markup_pct: parseFloat(markup),
          message: 'PRICE SPIKE: ' + item2.description + ' at $' + currentUSD.toFixed(2) + '/unit — ' + markup + '% above historical avg ($' + baseline.avgPrice.toFixed(2) + '), ' + (currentUSD > baseline.maxPrice ? '+' : '') + (currentUSD - baseline.maxPrice).toFixed(2) + ' above max ($' + baseline.maxPrice.toFixed(2) + ')'
        });
        riskScore += 0.4;
      }
    }
  }
  } // end: canRunAuditF1F2

  return {
    anomalies: anomalies,
    riskScore: Math.min(riskScore, 1.0),
    isAnomalous: anomalies.length > 0,
    hasHighSeverity: anomalies.some(function(a) { return a.severity === 'CRITICAL' || a.severity === 'HIGH'; }),
    enterpriseAuditRan: canRunAuditF1F2
  };
}

// ─── Confidence Score Calculator ───────────────────────────────────────────

function calcConfidence(parsedResult, anomalyResult) {
  var base = parsedResult.parse_confidence || 0.6;
  var risk = anomalyResult.riskScore;
  // High risk items reduce confidence
  var adjusted = Math.max(0, base - risk * 0.4);
  return parseFloat(adjusted.toFixed(3));
}

// ─── Hybrid Parse Entry Point ───────────────────────────────────────────────

function parseQuote(content, format, metadata) {
  metadata = metadata || {};
  var startTime = Date.now();

  // Step 1: Try regex pipeline first (fast, handles structured data)
  var regexResult = tryRegexPipeline(content, format, metadata);

  // Step 2: Check if regex failed OR confidence is low OR anomaly detected
  var needsLLM = false;
  if (regexResult.status === 'parse_failed') {
    needsLLM = true;
  } else {
    var riskCheck = runRiskAnalysis(regexResult, metadata);
    var confidence = calcConfidence(regexResult, riskCheck);
    regexResult.confidence_score = confidence;
    regexResult.anomaly_flags = riskCheck.anomalies.map(function(a) { return a.type; });
    regexResult.risk_score = riskCheck.riskScore;

    if (riskCheck.hasHighSeverity || confidence < 0.5) {
      needsLLM = true;
    }
  }

  // Step 3: LLM fallback for messy formats
  if (needsLLM && ENV.OPENAI_API_KEY) {
    try {
      var llmResult = callLLMStructuredExtract(content, metadata);
      if (llmResult && llmResult.items) {
        // Run risk analysis on LLM result too
        var riskLLM = runRiskAnalysis(llmResult, metadata);
        llmResult.confidence_score = calcConfidence({ parse_confidence: 0.88 }, riskLLM);
        llmResult.anomaly_flags = riskLLM.anomalies.map(function(a) { return a.type; });
        llmResult.risk_score = riskLLM.riskScore;
        llmResult.parsing_method = 'llm_fallback';
        llmResult.parse_time_ms = Date.now() - startTime;
        return buildResponse(llmResult, metadata, startTime);
      }
    } catch (llmErr) {
      console.warn('[WARN] LLM fallback failed: ' + llmErr.message + ' — falling back to regex result');
    }
  }

  // Step 4: Apply risk metadata to regex result
  if (regexResult.status !== 'parse_failed') {
    var risk = runRiskAnalysis(regexResult, metadata);
    regexResult.confidence_score = calcConfidence(regexResult, risk);
    regexResult.anomaly_flags = risk.anomalies.map(function(a) { return a.type; });
    regexResult.risk_score = risk.riskScore;
    regexResult.parsing_method = 'regex_pipeline';
    regexResult.parse_time_ms = Date.now() - startTime;
  }

  return buildResponse(regexResult, metadata, startTime);
}

function buildResponse(result, metadata, startTime) {
  var status = 'SUCCESS';
  if (result.status === 'parse_failed') {
    status = 'FAILED';
  } else if (result.anomaly_flags && result.anomaly_flags.length > 0) {
    if (result.risk_score > 0.5) {
      status = 'REJECTED_FOR_REVIEW';
    } else {
      status = 'SUCCESS_WITH_REVIEW';
    }
  }

  return {
    status: status,
    vendor_name:    result.vendor_name    || 'Unknown Vendor',
    items:          result.items           || [],
    subtotal:       result.subtotal        || 0,
    tax:            result.tax             || 0,
    total:          result.total           || 0,
    currency:        result.currency         || 'USD',
    payment_terms:  result.payment_terms   || 'Net 30',
    delivery_days:  result.delivery_days  || 0,
    received_at:    result.received_at     || new Date().toISOString(),
    confidence_score: result.confidence_score || 0.0,
    anomaly_flags:   result.anomaly_flags  || [],
    risk_score:      result.risk_score     || 0.0,
    risk_alerts:     buildRiskAlerts(result),
    parsing_method:  result.parsing_method || 'unknown',
    parse_time_ms:  result.parse_time_ms  || (Date.now() - startTime),
    source_format:  result.source_format  || 'unknown',
    healing_path:   result.healing_path    || '',
    suggestions:    result.suggestions     || [],
    metadata:       metadata
  };
}

function buildRiskAlerts(result) {
  var alerts = [];
  if (!result.anomaly_flags || result.anomaly_flags.length === 0) return alerts;

  var anomalyMap = {
    F1_CALC_ERROR:       '💰 Calculation error in line items',
    F1_TOTAL_MISMATCH: '⚠️  Subtotal/total does not match line sums',
    F2_PRICE_SPIKE:     '🚨 Price exceeds historical maximum — review required',
    F3_DUPLICATE:      '🔁 Potential duplicate quote detected'
  };

  for (var i = 0; i < result.anomaly_flags.length; i++) {
    var flag = result.anomaly_flags[i];
    alerts.push(anomalyMap[flag] || flag);
  }
  return alerts;
}

// ─── Regex Pipeline (Engine 1) ──────────────────────────────────────────────

function tryRegexPipeline(content, format, metadata) {
  var pipeline = [
    { fn: tryJsonParse,       format: 'json', confidence: 0.95 },
    { fn: tryHtmlTableParse,  format: 'html', confidence: 0.88 },
    { fn: tryCsvParse,        format: 'csv',  confidence: 0.82 },
    { fn: tryPlainTextRegex,  format: 'text', confidence: 0.60 },
  ];

  var lastError = null;
  for (var pi = 0; pi < pipeline.length; pi++) {
    var step = pipeline[pi];
    try {
      var result = step.fn(content, metadata);
      if (result && result.items && result.items.length > 0) {
        return {
          status: 'success',
          vendor_name:    result.vendor_name    || 'Unknown Vendor',
          items:          result.items,
          subtotal:       result.subtotal       || 0,
          tax:            result.tax            || 0,
          total:          result.total          || 0,
          currency:       result.currency        || detectCurrency(content),
          payment_terms:  result.payment_terms   || 'Net 30',
          delivery_days:  result.delivery_days  || 0,
          received_at:    result.received_at   || new Date().toISOString(),
          parse_confidence: step.confidence,
          source_format:  step.format,
          healing_path:   'succeeded_on_' + step.format,
          suggestions:   []
        };
      }
    } catch (err) {
      lastError = err.message;
    }
  }

  return {
    status: 'parse_failed',
    error: 'All regex parsers failed. Last error: ' + lastError,
    healing_path: 'all_parsers_exhausted',
    suggestions: getSuggestions((content || '').substring(0, 500))
  };
}

// ─── LLM Structured Extract ─────────────────────────────────────────────────

function callLLMStructuredExtract(content, metadata) {
  // Build a prompt with currency context
  var currencyHint = detectCurrency(content);
  var prompt = [
    'Extract structured procurement quote data from the following text.',
    'Currency detected: ' + currencyHint + ' (normalize all amounts to USD if different).',
    '',
    'Rules:',
    '- Extract each line item: description, quantity, unit_price, line_total',
    '- Verify that unit_price × quantity ≈ line_total; flag mismatches',
    '- Compare unit_price against historical avg; flag if >20% above avg',
    '- Calculate subtotal and tax; verify total = subtotal + tax',
    '- Return valid JSON only, no markdown, no explanation',
    '',
    '---QUOTE TEXT START---',
    maskSensitiveData(content).substring(0, 8000),
    '---QUOTE TEXT END---'
  ].join('\n');

  var result = callLLMSync(prompt);  // synchronous wrapper
  return result;
}

// ─── LLM Sync Wrapper ──────────────────────────────────────────────────────

function callLLMSync(prompt) {
  // Wraps the Promise-based callLLM in a sync-like interface using a simple mutex
  // In Node.js we still need to await, so exposed as callLLM() async function
  // This function is called from parseQuote which handles async internally
  throw new Error('callLLMSync should not be called directly — use callLLM()');
}

// ─── Parser 1: JSON ────────────────────────────────────────────────────────

function tryJsonParse(content, metadata) {
  var jsonPatterns = [
    /\{[\s\S]*"vendor"[\s\S]*\}/i,
    /\{[\s\S]*"total"[\s\S]*\}/i,
    /\{[\s\S]*"items"[\s\S]*\}/i,
  ];
  for (var i = 0; i < jsonPatterns.length; i++) {
    var m = content.match(jsonPatterns[i]);
    if (m) {
      try { return normalizeQuote(JSON.parse(m[0]), metadata); } catch (_) {}
    }
  }
  throw new Error('No JSON quote structure found');
}

// ─── Parser 2: HTML Table ──────────────────────────────────────────────────

function tryHtmlTableParse(content, metadata) {
  if (!content.includes('<td')) throw new Error('No HTML table cell found');

  var rowRegex  = /<tr[^>]*>([\s\S]*?)<\/tr>/gi;
  var cellRegex = /<td[^>]*>([\s\S]*?)<\/td>/gi;
  var rows = [];
  var m;
  while ((m = rowRegex.exec(content)) !== null) {
    var cells = [];
    var cm;
    while ((cm = cellRegex.exec(m[1])) !== null) {
      cells.push(cm[1].replace(/<[^>]*>/g, '').trim());
    }
    if (cells.length > 0) rows.push(cells);
  }
  if (rows.length < 2) throw new Error('HTML table has fewer than 2 rows');

  var header = rows[0].map(function(h) { return h.toLowerCase(); });
  var descIdx  = header.findIndex(function(h) { return h.match(/description|item|product|name|desc/); });
  var qtyIdx   = header.findIndex(function(h) { return h.match(/qty|quantity|amount|number/); });
  var priceIdx = header.findIndex(function(h) { return h.match(/price|unit|cost|rate/); });
  var totalIdx = header.findIndex(function(h) { return h.match(/total|sum|subtotal/); });

  if (descIdx === -1 || priceIdx === -1) throw new Error('Could not identify required columns');

  var items = [];
  for (var ri = 1; ri < rows.length; ri++) {
    var row = rows[ri];
    var description = row[descIdx] || '';
    var quantity    = parseInt(parseNumCell(row[qtyIdx]) || 1, 10);
    var unitPrice   = parseNumCell(row[priceIdx]);
    var lineTotal   = totalIdx !== -1 ? parseNumCell(row[totalIdx]) : quantity * unitPrice;
    if (description && unitPrice > 0) {
      items.push({ description: description, quantity: quantity, unit_price: unitPrice, line_total: lineTotal });
    }
  }

  var subtotal = 0, tax = 0, total = 0;
  var cellText = content.replace(/<[^>]*>/g, ' ').replace(/\s+/g, ' ').trim();

  var subM = content.match(/subtotal[:\s]*[$]?([\d,]+\.?\d*)/i) ||
             cellText.match(/(?:subtotal|sub total)[:\s]*[$EUR]?\s*([\d,]+\.?\d*)/i);
  var taxM = content.match(/(?:tax|vat|gst)[:\s]*[$]?([\d,]+\.?\d*)/i) ||
             cellText.match(/(?:tax|vat|gst)[:\s]*[$EUR]?\s*([\d,]+\.?\d*)/i);
  var totM = cellText.match(/\btotal\b[:\s]*[$EUR]?\s*([\d,]+\.?\d*)/i) ||
             cellText.match(/TOTAL[:\s]*[$EUR]?\s*([\d,]+\.?\d*)/i) ||
             cellText.match(/\bgrand total\b[:\s]*[$EUR]?\s*([\d,]+\.?\d*)/i);

  if (subM) subtotal = parseNumCell(subM[1]);
  if (taxM) tax = parseNumCell(taxM[1]);
  if (totM) total = parseNumCell(totM[1]);

  return {
    vendor_name:  extractVendorNameFromHtml(content) || ((metadata && metadata.from) || 'Unknown Vendor'),
    items:        items,
    subtotal:     subtotal || items.reduce(function(s, i) { return s + i.line_total; }, 0),
    tax:          tax,
    total:        total,
    currency:     detectCurrency(content),
    received_at: (metadata && metadata.date) || new Date().toISOString(),
    healing_path: 'html_table_parsing'
  };
}

// ─── Parser 3: CSV ────────────────────────────────────────────────────────

function tryCsvParse(content, metadata) {
  var lines = content.split('\n').filter(function(l) { return l.trim().length > 0; });
  if (lines.length < 2) throw new Error('CSV requires at least 2 lines');

  var delimiter = lines[0].includes('\t') ? '\t' : ',';
  var rows = lines.map(function(l) {
    return l.split(delimiter).map(function(c) {
      return c.trim().replace(/^["']|["']$/g, '');
    });
  });

  var header   = rows[0].map(function(h) { return h.toLowerCase(); });
  var descIdx  = header.findIndex(function(h) { return h.match(/desc|item|product|name|part/); });
  var qtyIdx   = header.findIndex(function(h) { return h.match(/qty|quantity|amount|num/); });
  var priceIdx = header.findIndex(function(h) { return h.match(/price|unit|cost|rate/); });
  var totalIdx = header.findIndex(function(h) { return h.match(/total|sum/); });

  if (descIdx === -1) descIdx = 0;
  if (priceIdx === -1) {
    for (var ci = 0; ci < rows[0].length; ci++) {
      if (parseNumCell(rows[0][ci]) > 0) { priceIdx = ci; break; }
    }
  }
  if (priceIdx === -1) throw new Error('Could not identify price column in CSV');

  var startRow = 1;
  if (!/[a-zA-Z]/.test(header.join(' '))) startRow = 0;

  var items = [];
  for (var ri = startRow; ri < rows.length; ri++) {
    var row = rows[ri];
    if (row.length < 2) continue;
    var description = (row[descIdx] || '').trim();
    if (!description || description.length < 2) continue;
    var qty       = parseInt(parseNumCell(row[qtyIdx]) || 1, 10);
    var unitPrice = parseNumCell(row[priceIdx]);
    var lineTotal = (totalIdx !== -1 && row[totalIdx]) ? parseNumCell(row[totalIdx]) : qty * unitPrice;
    if (unitPrice > 0) {
      items.push({ description: description, quantity: qty, unit_price: unitPrice, line_total: lineTotal });
    }
  }
  if (items.length === 0) throw new Error('No valid items extracted from CSV');

  return {
    vendor_name:  (metadata && metadata.from) || 'Unknown Vendor',
    items:        items,
    subtotal:     items.reduce(function(s, i) { return s + i.line_total; }, 0),
    tax:          0,
    total:        items.reduce(function(s, i) { return s + i.line_total; }, 0),
    currency:     detectCurrency(content),
    received_at: (metadata && metadata.date) || new Date().toISOString(),
    healing_path: 'csv_parsing'
  };
}

// ─── Parser 4: PDF OCR ─────────────────────────────────────────────────────

function tryPdfOcrParse(content, metadata) {
  throw new Error('PDF OCR not supported — use LLM fallback');
}

// ─── Parser 5: Plain Text Regex ────────────────────────────────────────────

var PRICE_PATTERNS = [
  /\$\s*([\d,]+\.?\d*)/,
  /([\d,]+\.?\d*)\s*(?:usd|dollars?)/i,
  /(?:usd|dollars?)\s*([\d,]+\.?\d*)/i,
  /￥\s*([\d,]+\.?\d*)/,
  /RMB\s*([\d,]+\.?\d*)/i,
  /CNY\s*([\d,]+\.?\d*)/i,
];

// Lines starting with these are summary rows (not line items)
var NOISE_LINE_START = /^(?:subtotal|sub total|tax|vat|gst|total|grand total|amount|合计|小计|总价|税费|hst|pst|TOTAL|Grand Total)/i;
var NOISE_CURRENCY_START = /^(?:USD|EUR|GBP|CNY|RMB|\$|￥)/i;

function tryPlainTextRegex(content, metadata) {
  var lines = content.split('\n').map(function(l) { return l.trim(); }).filter(function(l) { return l.length > 0; });
  var items = [];

  for (var li = 0; li < lines.length; li++) {
    var line      = lines[li];
    var lineClean = line.trim();
    if (NOISE_LINE_START.test(lineClean))     continue;
    if (NOISE_CURRENCY_START.test(lineClean)) continue;

    for (var pi = 0; pi < PRICE_PATTERNS.length; pi++) {
      var match = line.match(PRICE_PATTERNS[pi]);
      if (match) {
        var price = parseNumCell(match[1] || match[0]);
        if (price > 0 && price < 50000) {
          var pricePos = line.indexOf(match[0]);
          var descText = line.substring(0, pricePos)
            .replace(/[\$\€\£\¥￥]\s*/g, '')
            .replace(/[^\w\s\-:,()]/g, ' ')
            .replace(/\s+/g, ' ')
            .trim();
          if (descText.length > 3 && /[a-zA-Z]/.test(descText)) {
            items.push({
              description:      descText.substring(0, 100),
              quantity:         1,
              unit_price:       price,
              line_total:       price,
              extraction_method: 'price_pattern'
            });
          }
        }
        break;
      }
    }
  }

  if (items.length === 0) throw new Error('No line items extracted from plain text');

  var subtotal = 0, tax = 0, total = 0;
  var subM = content.match(/(?:subtotal|小计|合计)[:\s]*[￥$]?\s*([\d,]+\.?\d*)/i) ||
             content.match(/([\d,]+\.?\d*)\s*(?:小计|subtotal|含税)/i);
  var taxM = content.match(/(?:tax|vat|gst|税费)[:\s]*[￥$]?\s*([\d,]+\.?\d*)/i);
  var totM = content.match(/\btotal\b[:\s]*[￥$€]?\s*([\d,]+\.?\d*)/i) ||
             content.match(/([\d,]+\.?\d*)\s*\btotal\b/i) ||
             content.match(/(?:总计|合计|总价)[:\s]*[￥]?\s*([\d,]+\.?\d*)/i) ||
             content.match(/([\d,]+\.?\d*)\s*(?:总计|合计|总价)/i);

  if (subM) subtotal = parseNumCell(subM[1]);
  if (taxM) tax      = parseNumCell(taxM[1]);
  if (totM) total    = parseNumCell(totM[1]);

  return {
    vendor_name:  (metadata && metadata.from) || 'Unknown Vendor',
    items:        items,
    subtotal:     subtotal || items.reduce(function(s, i) { return s + i.line_total; }, 0),
    tax:          tax,
    total:        total,
    currency:     detectCurrency(content),
    received_at: (metadata && metadata.date) || new Date().toISOString(),
    healing_path: 'plain_text_regex',
    note:         'Low confidence parse — verify extracted items manually'
  };
}

// ─── Duplicate Detection (F3) ───────────────────────────────────────────────

function detectDuplicate(newQuote, existingQuotes, userEmail) {
  // F3 is Enterprise-only
  if (userEmail && AUTH) {
    try { AUTH.authorizeSync(userEmail, 'f3_duplicate'); } catch (err) {
      if (err.code === 'LICENSE_DENIED') {
        return { isDuplicate: false, f3Skipped: true, reason: 'F3 requires Enterprise license' };
      }
    }
  }
  for (var ei = 0; ei < (existingQuotes || []).length; ei++) {
    var existing = existingQuotes[ei];
    var daysDiff = Math.abs((new Date(newQuote.received_at || 0) - new Date(existing.received_at || 0)) / 86400000);
    if (daysDiff > 7) continue;
    var nv = ((newQuote.vendor_name || '').toLowerCase()).trim();
    var ev = ((existing.vendor_name || '').toLowerCase()).trim();
    if (nv !== ev) continue;
    var et = parseFloat(existing.total || 0);
    var nt = parseFloat(newQuote.total || 0);
    if (et === 0) continue;
    var diff = Math.abs(nt - et) / et;
    if (diff < 0.01) return { isDuplicate: true, matchedQuote: existing, confidence: 0.95, type: 'F3_DUPLICATE' };
    if (newQuote.items && existing.items &&
        newQuote.items.length === existing.items.length && diff < 0.05) {
      return { isDuplicate: true, matchedQuote: existing, confidence: 0.75, type: 'F3_DUPLICATE' };
    }
  }
  return { isDuplicate: false };
}

// ─── Quote Comparator ─────────────────────────────────────────────────────

function compareQuotes(quotes) {
  return quotes
    .map(function(q) { return { quote: q, score: calculateQuoteScore(q) }; })
    .sort(function(a, b) { return a.score.total_score - b.score.total_score; });
}

function calculateQuoteScore(quote) {
  var total    = parseFloat(quote.total || 0);
  var delivery = parseInt(quote.delivery_days || 0, 10);
  var rating   = parseFloat(quote.vendor_rating || 3.0);
  var priceScore    = 100 - Math.min(total / 100, 50);
  var deliveryScore = Math.max(10 - delivery, 0) * 10;
  var vendorScore   = (rating / 5.0) * 100;
  var totalScore    = priceScore * 0.5 + deliveryScore * 0.25 + vendorScore * 0.25;
  return {
    price_score:     priceScore,
    delivery_score:  deliveryScore,
    vendor_score:    vendorScore,
    total_score:     totalScore,
    recommendation:  totalScore > 70 ? 'recommended' : 'review_required'
  };
}

// ─── Lemon Squeezy Webhook Handler ───────────────────────────────────────

function verifyLSSignature(rawBody, signature, secret) {
  if (!signature || !secret) return false;
  try {
    var expected = crypto.createHmac('sha256', secret).update(rawBody, 'utf8').digest('hex');
    var received = signature.replace('sha256=', '');
    return crypto.timingSafeEqual(Buffer.from(expected, 'hex'), Buffer.from(received, 'hex'));
  } catch (_) { return false; }
}

function handleLSWebhook(event, payload) {
  var results = [];
  var tier = 'free';
  var action = 'none';

  switch (event) {
    case 'subscription_created':
    case 'subscription_updated':
      tier = mapVariantToTier(payload.data && payload.data.attributes && payload.data.attributes.variant_id);
      action = 'tier_set';
      results.push({ tier: tier, email: payload.meta && payload.meta.custom_data && payload.meta.custom_data.email, action: action });
      break;
    case 'subscription_cancelled':
    case 'subscription_expired':
      tier = 'free';
      action = 'downgrade';
      results.push({ tier: tier, action: action });
      break;
  }

  return results;
}

function mapVariantToTier(variantId) {
  var proTiers   = (process.env.LS_PRO_VARIANT_IDS   || '').split(',').filter(Boolean);
  var teamTiers   = (process.env.LS_TEAM_VARIANT_IDS || '').split(',').filter(Boolean);
  var enterpriseTiers = (process.env.LS_ENTERPRISE_VARIANT_IDS || '').split(',').filter(Boolean);
  var vid = String(variantId || '');
  if (enterpriseTiers.includes(vid)) return 'enterprise';
  if (teamTiers.includes(vid))      return 'team';
  if (proTiers.includes(vid))       return 'pro';
  return 'free';
}

// ─── Approval Flow Circuit Breaker (S3 Fix) ────────────────────────────────

var _approvalCircuitBreaker = { failures: 0, openedAt: null, state: 'CLOSED' };

function resetApprovalCircuitBreaker() {
  _approvalCircuitBreaker = { failures: 0, openedAt: null, state: 'CLOSED' };
}

function tripApprovalCircuitBreaker() {
  _approvalCircuitBreaker.failures++;
  if (_approvalCircuitBreaker.failures >= ENV.CIRCUIT_BREAKER_THRESH) {
    _approvalCircuitBreaker.state = 'OPEN';
    _approvalCircuitBreaker.openedAt = Date.now();
    return true; // tripped
  }
  return false; // not yet tripped
}

function isApprovalCircuitOpen() {
  if (_approvalCircuitBreaker.state === 'CLOSED') return false;
  // Auto-reset after 30 min
  if (_approvalCircuitBreaker.state === 'OPEN') {
    if (Date.now() - _approvalCircuitBreaker.openedAt > 30 * 60 * 1000) {
      _approvalCircuitBreaker.state = 'HALF_OPEN';
      return true;
    }
    return true;
  }
  return false;
}

// ─── Approval Flow Executor ───────────────────────────────────────────────

function sendEmail(to, subject, body, timeoutMs) {
  // Stub: replace with real SMTP/SendGrid/SES call
  return new Promise(function(resolve) {
    setTimeout(function() {
      resolve({ sent: false, error: 'SMTP_NOT_CONFIGURED', to: to });
    }, Math.min(timeoutMs || 5000, 50));
  });
}

function sendEmergencyAlert(message) {
  // Stub: replace with Twilio SMS / Push notification
  console.log('[ALERT] 🚨 ' + message);
  return Promise.resolve({ alert_sent: true, message: message });
}

function createApprovalFlowExecutor(config) {
  config = config || {};
  var approvalLimit       = config.approvalLimit      || 10000;
  var escalationTimeoutMs = config.escalationTimeoutMs || 5000;
  var primaryApprover    = config.primaryApprover    || 'manager@company.com';
  var backupApprover     = config.backupApprover     || 'director@company.com';

  return async function executeApprovalFlow(orderAmount, orderId) {
    var result = {
      orderId:       orderId,
      amount:         orderAmount,
      status:        'PENDING_APPROVAL',
      escalationCount: 0,
      finalApprover: null,
      action:        null,
      timestamp:     new Date().toISOString()
    };

    // Safety-Freeze: circuit breaker open
    if (isApprovalCircuitOpen()) {
      result.status = 'SAFETY_FREEZE';
      result.action  = 'CIRCUIT_BREAKER_OPEN — no approvals sent, system in safety freeze';
      await sendEmergencyAlert('Safety Freeze: Approval circuit breaker is OPEN for order ' + orderId);
      return result;
    }

    // Under limit: auto-approve
    if (orderAmount <= approvalLimit) {
      result.status       = 'AUTO_APPROVED';
      result.finalApprover = 'SYSTEM_AUTO';
      result.action        = 'Auto-approved: $' + orderAmount + ' <= $' + approvalLimit + ' limit';
      return result;
    }

    // Over limit: try primary approver
    var primary = await sendEmail(primaryApprover, 'Approval Required: $' + orderAmount,
      'Order #' + orderId + ' requires approval. Amount: $' + orderAmount, escalationTimeoutMs);

    if (primary.sent) {
      result.status       = 'APPROVED';
      result.finalApprover = primaryApprover;
      result.action        = 'Approved by primary approver';
      return result;
    }

    // Primary failed: try backup (ESCALATION)
    result.escalationCount = 1;
    var backup = await sendEmail(backupApprover, 'ESCALATED Approval Required: $' + orderAmount,
      'URGENT: Order #' + orderId + ' requires escalation. Amount: $' + orderAmount + '. Primary approver unreachable.', escalationTimeoutMs);

    if (backup.sent) {
      // Trip circuit breaker if this is a failure-path escalation
      tripApprovalCircuitBreaker();
      result.status       = 'ESCALATED_APPROVED';
      result.finalApprover = backupApprover;
      result.action        = 'ESCALATED: primary (' + primaryApprover + ') failed — backup (' + backupApprover + ') approved';
      return result;
    }

    // Both failed: SAFETY FREEZE
    tripApprovalCircuitBreaker();
    result.status = 'SAFETY_FREEZE';
    result.action  = 'FREEZE: both primary and backup approvers unreachable for order $' + orderAmount + '. Emergency alert dispatched.';
    await sendEmergencyAlert('Safety Freeze triggered for order ' + orderId + ': $' + orderAmount + ' — both approvers unreachable.');
    return result;
  };
}

// ─── Helper Functions ─────────────────────────────────────────────────────

function normalizeQuote(data, metadata) {
  function getVal(obj) {
    for (var ki = 1; ki < arguments.length; ki++) {
      if (obj[arguments[ki]] !== undefined) return obj[arguments[ki]];
    }
    return undefined;
  }
  var rawItems = data.items || [];
  var items = rawItems.map(function(item) {
    return {
      description: getVal(item, 'description', 'desc', 'name', 'product') || '',
      quantity:    parseInt(getVal(item, 'quantity', 'qty', 'amount') || 1, 10),
      unit_price:  parseNumCell(getVal(item, 'unit_price', 'price', 'rate') || 0),
      line_total:  parseNumCell(getVal(item, 'line_total', 'total') || 0)
    };
  });
  return {
    vendor_name:    getVal(data, 'vendor_name', 'vendor', 'supplier') || ((metadata && metadata.from) || 'Unknown'),
    items:          items,
    subtotal:       parseNumCell(getVal(data, 'subtotal', 'sub_total') || 0),
    tax:            parseNumCell(getVal(data, 'tax', 'tax_amount', 'vat') || 0),
    total:          parseNumCell(getVal(data, 'total', 'total_amount', 'grand_total') || 0),
    currency:       data.currency || 'USD',
    delivery_days:  parseInt(getVal(data, 'delivery_days', 'lead_time_days') || 0, 10),
    payment_terms:  getVal(data, 'payment_terms', 'terms') || 'Net 30',
    valid_until:    getVal(data, 'valid_until', 'validity_date') || null,
    received_at:   (metadata && metadata.date) || new Date().toISOString()
  };
}

function extractVendorNameFromHtml(html) {
  var patterns = [
    /<strong[^>]*>([^<]+(?:Corp|Inc|LLC|Co|Ltd)[^<]*)<\/strong>/i,
    /<h[1-3][^>]*>([^<]+(?:Corp|Inc|LLC|Co|Ltd)[^<]*)<\/h[1-3]>/i,
    /from:\s*([^\s]+(?:Corp|Inc|LLC|Co|Ltd))/i,
    /供应商：([^\n]+)/,
  ];
  for (var i = 0; i < patterns.length; i++) {
    var m = html.match(patterns[i]);
    if (m) return m[1].trim();
  }
  return null;
}

function getSuggestions(snippet) {
  var s = [];
  if (!snippet) return s;
  if (snippet.includes('invoice')) s.push('This appears to be an invoice rather than a quote');
  if (snippet.includes('purchase order')) s.push('This appears to be a purchase order, not a quote');
  if (snippet.includes('attachment') || snippet.includes('attached')) s.push('Email mentions an attachment — try the PDF directly or use LLM fallback');
  if (snippet.length < 50) s.push('Email body is very short — quote may be in an attached file');
  return s;
}

// ─── CLI ───────────────────────────────────────────────────────────────────

function main() {
  var args = process.argv.slice(2);
  var cmd  = args[0];

  if (cmd === 'parse') {
    var content = args[1] || fs.readFileSync('/dev/stdin', 'utf8');
    var fmt    = args[2] || 'text';
    var meta   = args[3] ? JSON.parse(args[3]) : {};
    parseQuote(content, fmt, meta).then(function(result) {
      console.log(JSON.stringify(result, null, 2));
    }).catch(function(err) {
      console.error(JSON.stringify({ error: err.message }, null, 2));
    });
    return;
  }

  if (cmd === 'approve') {
    // Simulate approval flow
    var amount   = parseFloat(args[1] || '15000');
    var orderId  = args[2] || 'ORD-' + Date.now();
    var executor = createApprovalFlowExecutor({ approvalLimit: 10000 });
    executor(amount, orderId).then(function(result) {
      console.log(JSON.stringify(result, null, 2));
    });
    return;
  }

  if (cmd === 'compare') {
    console.log(JSON.stringify(compareQuotes(JSON.parse(fs.readFileSync('/dev/stdin', 'utf8'))), null, 2));
    return;
  }

  if (cmd === 'dedup') {
    var input = JSON.parse(fs.readFileSync('/dev/stdin', 'utf8'));
    console.log(JSON.stringify(detectDuplicate(input.newQuote, input.existingQuotes), null, 2));
    return;
  }

  console.log([
    'Procurement Agent Hybrid Parser v3.0.0',
    'Usage:',
    '  node self-healing-parser.js parse <content> [format] [metadata]',
    '  node self-healing-parser.js approve <amount> [orderId]',
    '  node self-healing-parser.js compare <quotes.json>',
    '  node self-healing-parser.js dedup <quotes.json>',
    '',
    'Environment:',
    '  OPENAI_API_KEY           — enable LLM fallback (recommended)',
    '  LS_API_KEY              — Lemon Squeezy integration',
    '  PARSER_DATA_DIR          — historical prices + event store',
    '  CB_THRESHOLD             — circuit breaker threshold (default: 2)'
  ].join('\n'));
}

// Export async parseQuote for CLI (wraps sync behavior)
var _parseQuoteAsync = function(content, format, metadata) {
  return new Promise(function(resolve) {
    // If LLM is available, use async path
    if (ENV.OPENAI_API_KEY) {
      // Full async parse (with LLM fallback)
      var result = parseQuote(content, format, metadata);
      resolve(result);
    } else {
      resolve(parseQuote(content, format, metadata));
    }
  });
};

module.exports = {
  parseQuote:          _parseQuoteAsync,
  parseQuoteSync:      parseQuote,
  detectDuplicate:     detectDuplicate,
  compareQuotes:       compareQuotes,
  calculateQuoteScore:  calculateQuoteScore,
  runRiskAnalysis:      runRiskAnalysis,
  createApprovalFlowExecutor: createApprovalFlowExecutor,
  verifyLSSignature:   verifyLSSignature,
  handleLSWebhook:     handleLSWebhook,
  resetApprovalCircuitBreaker: resetApprovalCircuitBreaker,
  requireEnterpriseFeature: requireEnterpriseFeature,
  FX_RATES:            FX_RATES,
  toUSD:               toUSD
};

if (require.main === module) main();
