#!/usr/bin/env node
/**
 * biolims-server.mjs - Bio-LIMS Persistent HTTP Service
 *
 * Maintains login state, receives commands via HTTP, response time < 200ms
 *
 * Start:
 *   node biolims-server.mjs [port]     # default port 3847
 *
 * Usage:
 *   curl http://localhost:3847/order/DB2602060003
 *   curl http://localhost:3847/order-list?page=1&rows=10
 *   curl -X POST http://localhost:3847/create-order -d '{"order":{...}}'
 */

import crypto from 'crypto';
import http from 'http';
import { URL } from 'url';

// ============================================================================
// Configuration
// ============================================================================
const BASE_URL = process.env.BIOLIMS_URL || 'http://example.com/biolims';
const USERNAME = process.env.BIOLIMS_USER || 'demo';
const PASSWORD = process.env.BIOLIMS_PASSWORD || 'demo';
const DATA_SOURCE = process.env.BIOLIMS_DS || 'demo';
const SOLE_ID = crypto.randomUUID();

const AES_KEY = Buffer.from(process.env.BIOLIMS_AES_KEY || '0000000000000000', 'utf8');
const AES_IV = Buffer.from(process.env.BIOLIMS_AES_IV || '0000000000000000', 'utf8');
const SECRET_KEY = process.env.BIOLIMS_SECRET || 'demo';

const PORT = parseInt(process.argv[2]) || 3847;

// ============================================================================
// Global auth state (in-memory)
// ============================================================================
let authState = {
  token: null,
  xsrf: null,
  cookies: null,
  expiresAt: 0
};

// ============================================================================
// AES Encryption
// ============================================================================
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

// ============================================================================
// Login
// ============================================================================
async function login() {
  console.log('[Auth] Logging in...');
  const start = Date.now();

  const encryptedPassword = encryptPassword(PASSWORD);
  const urlEncodedPassword = encodeURIComponent(encryptedPassword);
  const loginUrl = `${BASE_URL}/user/Login?username=${USERNAME}&password=${urlEncodedPassword}`;

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

  const token = response.headers.get('Token') || response.headers.get('token');
  if (!token) {
    throw new Error('Login failed - no token in response');
  }

  // Extract cookies
  const setCookie = response.headers.get('set-cookie') || '';
  const cookies = setCookie.split(',').map(c => c.split(';')[0].trim()).filter(Boolean);
  
  let xsrf = '';
  for (const cookie of cookies) {
    if (cookie.startsWith('XSRF-TOKEN=')) {
      xsrf = cookie.split('=')[1];
    }
  }

  authState = {
    token,
    xsrf,
    cookies: cookies.join('; '),
    expiresAt: Date.now() + 20 * 60 * 1000 // 20 minutes, with 5-minute buffer
  };

  console.log(`[Auth] Login successful in ${Date.now() - start}ms`);
  return authState;
}

async function ensureAuth() {
  if (!authState.token || Date.now() > authState.expiresAt) {
    await login();
  }
  return authState;
}

// ============================================================================
// API Call
// ============================================================================
async function apiCall(method, apiPath, body = null, retry = true) {
  const auth = await ensureAuth();

  const headers = {
    'Content-Type': 'application/json',
    'Token': auth.token,
    'X-DS': DATA_SOURCE,
    'accept-language': 'zh_CN',
    'X-Sole-ID': SOLE_ID
  };

  if (auth.xsrf) {
    headers['X-XSRF-TOKEN'] = auth.xsrf;
  }
  if (auth.cookies) {
    headers['Cookie'] = auth.cookies;
  }

  const options = { method, headers };
  if (body) {
    options.body = typeof body === 'string' ? body : JSON.stringify(body);
  }

  const response = await fetch(`${BASE_URL}${apiPath}`, options);
  const data = await response.json();

  // Token expired, re-login
  if (data.status === 401 && retry) {
    authState = { token: null, xsrf: null, cookies: null, expiresAt: 0 };
    await login();
    return apiCall(method, apiPath, body, false);
  }

  return data;
}

// ============================================================================
// Route Handlers
// ============================================================================
const routes = {
  // GET /order/:id
  async 'GET /order'(params) {
    const orderId = params.id;
    if (!orderId) return { error: 'order_id parameter required' };
    return await apiCall('POST', '/order/selectOrder', { orderId });
  },

  // GET /order-list?page=1&rows=10
  async 'GET /order-list'(params) {
    const page = parseInt(params.page) || 1;
    const rows = parseInt(params.rows) || 10;

    const result = await apiCall('POST', '/order/selectAllOrderList', {
      bioTechLeaguePagingQuery: { page, rows, sort: {}, query: [] }
    });

    // Simplify output
    if (result.status === 200 && result.data?.result) {
      result.data.result = result.data.result.map(order => ({
        id: order.id,
        firstName: order.firstName,
        lastName: order.lastName,
        gender: order.gender,
        birthDate: order.birthDate,
        phone: order.phone,
        email: order.email,
        productId: order.productId,
        productName: order.productName,
        state: order.state,
        stateName: order.stateName,
        barcode: order.barcode,
        createTime: order.createTime,
        creatorNickname: order.creatorNickname,
        confirmTime: order.confirmTime,
        confirmerNickname: order.confirmerNickname,
        crmCustomerName: order.crmCustomerName,
        inspectionDepartmentName: order.inspectionDepartmentName,
        attendingDoctorName: order.attendingDoctorName
      }));
    }

    return result;
  },

  // GET /order-samples/:id
  async 'GET /order-samples'(params) {
    const orderId = params.id;
    if (!orderId) return { error: 'order_id parameter required' };
    return await apiCall('POST', '/order/selectSampleOrderItem', {
      orderId,
      bioTechLeaguePagingQuery: { page: 1, rows: 100, sort: {}, query: [] }
    });
  },

  // GET /order-fees/:id
  async 'GET /order-fees'(params) {
    const orderId = params.id;
    if (!orderId) return { error: 'order_id parameter required' };
    return await apiCall('POST', '/order/selectFee', { orderId });
  },

  // POST /create-order (body = JSON)
  async 'POST /create-order'(params, body) {
    if (!body) return { error: 'JSON body required' };
    return await apiCall('POST', '/order/saveOrUpdateOrderAllData', body);
  },

  // POST /update-order (body = JSON)
  async 'POST /update-order'(params, body) {
    if (!body) return { error: 'JSON body required' };
    return await apiCall('POST', '/order/saveOrUpdateOrderAllData', body);
  },

  // POST /complete-order/:id
  async 'POST /complete-order'(params) {
    const orderId = params.id;
    if (!orderId) return { error: 'order_id parameter required' };
    return await apiCall('POST', `/order/completeTask?id=${orderId}`, '');
  },

  // POST /cancel-order/:id
  async 'POST /cancel-order'(params) {
    const orderId = params.id;
    if (!orderId) return { error: 'order_id parameter required' };
    return await apiCall('POST', `/order/cancelTask?id=${orderId}`, '');
  },

  // GET /sample-types?page=1&rows=100
  async 'GET /sample-types'(params) {
    const page = parseInt(params.page) || 1;
    const rows = parseInt(params.rows) || 100;
    return await apiCall('POST', '/order/selectPopupsSampleType', {
      page, rows, sort: {}, query: []
    });
  },

  // GET /search-sample-type?name=xxx
  async 'GET /search-sample-type'(params) {
    const name = params.name;
    if (!name) return { error: 'name parameter required' };
    return await apiCall('POST', '/order/selectPopupsSampleType', {
      page: 1,
      rows: 100,
      sort: {},
      pagingSearchOne: { matchMode: ['name'], value: name },
      query: []
    });
  },

  // GET /status - Service Status
  async 'GET /status'() {
    return {
      status: 'ok',
      authenticated: !!authState.token,
      expiresIn: authState.expiresAt ? Math.max(0, Math.floor((authState.expiresAt - Date.now()) / 1000)) : 0,
      uptime: process.uptime()
    };
  }
};

// ============================================================================
// HTTP Server
// ============================================================================
async function handleRequest(req, res) {
  const start = Date.now();
  
  res.setHeader('Content-Type', 'application/json; charset=utf-8');
  res.setHeader('Access-Control-Allow-Origin', '*');

  try {
    const url = new URL(req.url, `http://localhost:${PORT}`);
    const pathname = url.pathname;
    const method = req.method;

    // Parse path parameters (e.g. /order/DB123 -> id=DB123)
    const parts = pathname.split('/').filter(Boolean);
    const routePath = parts[0] ? `/${parts[0]}` : '/';
    const routeKey = `${method} ${routePath}`;

    const params = Object.fromEntries(url.searchParams);
    if (parts[1]) {
      params.id = parts[1];
    }

    // Read body
    let body = null;
    if (method === 'POST') {
      body = await new Promise((resolve, reject) => {
        let data = '';
        req.on('data', chunk => data += chunk);
        req.on('end', () => {
          try {
            resolve(data ? JSON.parse(data) : null);
          } catch (e) {
            reject(new Error('Invalid JSON'));
          }
        });
        req.on('error', reject);
      });
    }

    const handler = routes[routeKey];
    if (!handler) {
      res.statusCode = 404;
      res.end(JSON.stringify({ error: 'Not found', routes: Object.keys(routes) }));
      return;
    }

    const result = await handler(params, body);
    const elapsed = Date.now() - start;
    console.log(`[${method}] ${pathname} - ${elapsed}ms`);

    res.end(JSON.stringify(result, null, 2));
  } catch (error) {
    console.error('[Error]', error.message);
    res.statusCode = 500;
    res.end(JSON.stringify({ error: error.message }));
  }
}

// ============================================================================
// Startup
// ============================================================================
const server = http.createServer(handleRequest);

server.listen(PORT, () => {
  console.log(`
╔══════════════════════════════════════════════════════════╗
║  Bio-LIMS API Server                                     ║
║  http://localhost:${PORT}                                   ║
╠══════════════════════════════════════════════════════════╣
║  Endpoints:                                              ║
║    GET  /order/:id           Query order details             ║
║    GET  /order-list          Order list (?page=1&rows=10)    ║
║    GET  /order-samples/:id   Order samples                   ║
║    GET  /order-fees/:id      Order fees                      ║
║    POST /create-order        Create order (JSON body)        ║
║    POST /update-order        Update order (JSON body)        ║
║    POST /complete-order/:id  Complete order                  ║
║    POST /cancel-order/:id    Cancel order                    ║
║    GET  /sample-types        Sample type list                ║
║    GET  /search-sample-type  Search sample type (?name=xxx)  ║
║    GET  /status              Service status                  ║
╚══════════════════════════════════════════════════════════╝
`);

  // Warmup: login on startup
  login().catch(err => console.error('[Warmup] Login failed:', err.message));
});

// Graceful shutdown
process.on('SIGINT', () => {
  console.log('\n[Server] Shutting down...');
  server.close();
  process.exit(0);
});
