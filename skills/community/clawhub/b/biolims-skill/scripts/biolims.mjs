#!/usr/bin/env node
/**
 * biolims.mjs - Bio-LIMS API Script (Node.js Version)
 *
 * Usage:
 *   node biolims.mjs order <order_id>
 *   node biolims.mjs order-list [page] [rows]
 *   node biolims.mjs order-samples <order_id>
 *   node biolims.mjs order-fees <order_id>
 *   node biolims.mjs create-order '<json>'
 *   node biolims.mjs update-order '<json>'
 *   node biolims.mjs complete-order <order_id>
 *   node biolims.mjs cancel-order <order_id>
 *   node biolims.mjs sample-types [page] [rows]
 *   node biolims.mjs search-sample-type <name>
 * 
 * ============================================================================
 * Experiment Center API Documentation
 * ============================================================================
 * 
 * 1. Query all experiment list
 *    URL: /experimentalcenter/experiment/selectExperimentFlowMain
 *    Parameters: {
 *      "bioTechLeaguePagingQuery": {"page":1,"rows":20,"sort":{},"pagingSearchOne":{},"query":[]},
 *      "sort": {},
 *      "pagingSearchOne": {},
 *      "query": [],
 *      "tableData": [],
 *      "page": 1,
 *      "rows": 20,
 *      "totalRecords": "33",
 *      "databaseTableSuffix": "NAE"
 *    }
 * 
 * 2. Query all components and field values in an experiment
 *    URL: /experimentalcenter/experiment/selectOrAddExperimentFlowTemplate
 *    Parameters: {
 *      "experimentFlowId": "NA20260021",  // Experiment ID
 *      "flow": "Activity_0uh63rf",         // Flow node ID
 *      "databaseTableSuffix": "NAE"        // Experiment type suffix
 *    }
 *
 *    Response description:
 *    - stepDetails: Contains all components
 *    - type="detailTable": Detail table (sample list)
 *    - type="resultTable": Result table
 *    - value: JSON string of field values
 *    - propList: Field name definitions
 *
 *    ⚠️ Important: When modifying field values, only modify the values in "value", do not change other content, otherwise it will cause component display issues in the experiment!
 * 
 * 3. Change product type
 *    Need to obtain from the detailTable returned by experiment-template:
 *    - stepItemId: Component ID (jsonDatas[].id, the one with type=detailTable)
 *    - Sample detail ID: The id field of each sample in the value JSON
 *
 *    Then call the change-product command
 * 
 * ============================================================================
 * 4. Save experiment data (updateExperimentFlow) - Modify result table sample data
 * ============================================================================
 * 
 *    URL: /experimentalcenter/experiment/updateExperimentFlow
 * 
 * ============================================================================
 * 5. Complete Experiment API - Three Methods
 * ============================================================================
 *
 *    ⚠️ Important: Before completing an experiment, ensure:
 *    1. Samples have been added to the experiment
 *    2. generate-result has been called to generate the result table
 *    3. update-result has been called to fill in required result table fields:
 *       - result, resultId (result)
 *       - nextFlow, nextFlowId, databaseTableSuffixTwo (next flow direction)
 * 
 *    ┌──────────────────────────────────────────────────────────────────────────┐
 *    │ Method 1: complete-experiment (Recommended - Simplest)                   │
 *    ├──────────────────────────────────────────────────────────────────────────┤
 *    │ Command: biolims.mjs complete-experiment <suffix> <experiment_id> [flow_id] │
 *    │                                                                          │
 *    │ Features:                                                                │
 *    │ - Automatically fetches experiment template data                         │
 *    │ - Automatically extracts required stepId and templateId                  │
 *    │ - Automatically checks if result table is filled                         │
 *    │ - No need to manually build JSON file                                    │
 *    │                                                                          │
 *    │ Examples:                                                                │
 *    │   node biolims.mjs complete-experiment NAE NA20260041                    │
 *    │   node biolims.mjs complete-experiment LP LP20260015 Activity_1nzvwkd   │
 *    └──────────────────────────────────────────────────────────────────────────┘
 * 
 *    ┌──────────────────────────────────────────────────────────────────────────┐
 *    │ Method 2: complete-step (Requires manually building JSON)                 │
 *    ├──────────────────────────────────────────────────────────────────────────┤
 *    │ Command: biolims.mjs complete-step @<json file>                         │
 *    │                                                                          │
 *    │ Parameter format:                                                        │
 *    │ {                                                                        │
 *    │   "id": "<stepDetails[0].id>",         // Step detail ID                 │
 *    │   "databaseTableSuffix": "NAE",        // Experiment type suffix         │
 *    │   "experimentId": "<template_id>",     // ⚠️ Template ID, NOT experiment ID! │
 *    │   "stepState": "1",                    // Step state (1=complete)        │
 *    │   "mainId": "NA20260041"               // Experiment ID                  │
 *    │ }                                                                        │
 *    │                                                                          │
 *    │ Example:                                                                 │
 *    │   node biolims.mjs complete-step @/tmp/complete.json                     │
 *    └──────────────────────────────────────────────────────────────────────────┘
 * 
 *    ┌──────────────────────────────────────────────────────────────────────────┐
 *    │ Method 3: Directly call updateExperimentFlowNext API (Low-level method)   │
 *    ├──────────────────────────────────────────────────────────────────────────┤
 *    │ URL: POST /experimentalcenter/experiment/updateExperimentFlowNext        │
 *    │                                                                          │
 *    │ Parameter format:                                                        │
 *    │ {                                                                        │
 *    │   "id": "<stepDetails[0].id>",         // Step detail ID                 │
 *    │   "databaseTableSuffix": "NAE",        // Experiment type suffix         │
 *    │   "experimentId": "<template_id>",     // ⚠️ Template ID, NOT experiment ID! │
 *    │   "stepState": "1",                    // Step state (1=complete)        │
 *    │   "mainId": "NA20260041"               // Experiment ID                  │
 *    │ }                                                                        │
 *    │                                                                          │
 *    │ Example (using curl):                                                    │
 *    │   curl -X POST http://your-server/biolims/experimentalcenter/         │
 *    │     experiment/updateExperimentFlowNext \                                │
 *    │     -H "Content-Type: application/json" \                                │
 *    │     -H "Token: $TOKEN" \                                                 │
 *    │     -H "X-XSRF-TOKEN: $XSRF" \                                           │
 *    │     -H "Cookie: $COOKIES" \                                              │
 *    │     -H "X-DS: droplet" \                                                 │
 *    │     -d '{"id":"d1275f3f035d89adfa4434da0ba2481d",                       │
 *    │           "databaseTableSuffix":"NAE",                                   │
 *    │           "experimentId":"6fa91347e20156174243b334965fbb67",            │
 *    │           "stepState":"1",                                               │
 *    │           "mainId":"NA20260041"}'                                        │
 *    └──────────────────────────────────────────────────────────────────────────┘
 * 
 *    ┌──────────────────────────────────────────────────────────────────────────┐
 *    │ Complete Workflow Example (using NAE as example)                          │
 *    ├──────────────────────────────────────────────────────────────────────────┤
 *    │ 1. Create experiment:                                                    │
 *    │    node biolims.mjs quick-create-experiment NAE <protocol_id> <exp_id>  │
 *    │                                                                          │
 *    │ 2. Add samples:                                                          │
 *    │    node biolims.mjs experiment-add-samples NAE <exp_id> <flow_id>       │
 *    │      "<sample_pool_id1,sample_pool_id2,...>"                             │
 *    │                                                                          │
 *    │ 3. Change product type (if needed):                                      │
 *    │    node biolims.mjs change-product '@/path/to/change-product.json'     │
 *    │                                                                          │
 *    │ 4. Generate result table:                                                │
 *    │    node biolims.mjs generate-result NAE <exp_id> <flow_id>              │
 *    │                                                                          │
 *    │ 5. Query next flow direction:                                             │
 *    │    node biolims.mjs select-next-flow NAE SYLX2024000001                 │
 *    │      "<result_id1,result_id2,...>"                                       │
 *    │                                                                          │
 *    │ 6. Update result table (set result and next flow direction):              │
 *    │    node biolims.mjs update-result NAE <exp_id> <flow_id>                │
 *    │      '[{"id":"<result_id>","result":"Qualified","resultId":"1",        │
 *    │         "nextFlow":"Library Preparation","nextFlowId":"SYLX2024000007", │
 *    │         "databaseTableSuffixTwo":"LP"}]'                                │
 *    │                                                                          │
 *    │ 7. Complete experiment (choose one of three methods):                     │
 *    │    Method 1 (Recommended):                                              │
 *    │      node biolims.mjs complete-experiment NAE <exp_id>                  │
 *    │    Method 2:                                                              │
 *    │      node biolims.mjs complete-step @/tmp/complete.json                 │
 *    │    Method 3:                                                              │
 *    │      curl -X POST .../updateExperimentFlowNext -d '<json>'              │
 *    └──────────────────────────────────────────────────────────────────────────┘
 * 
 *    ┌──────────────────────────────────────────────────────────────────────────┐
 *    │ Common Flow Node ID Mapping                                               │
 *    ├──────────────────────────────────────────────────────────────────────────┤
 *    │ Experiment Type | Flow Node ID       | Description                      │
 *    ├──────────────────────────────────────────────────────────────────────────┤
 *    │ NAE     | Activity_1vzdimw     | Nucleic Acid Extraction              │
 *    │ LP      | Activity_1nzvwkd     | Library Preparation                  │
 *    │ E       | Activity_1d0j2yv     | Enrichment                           │
 *    │ Se      | Activity_0mo5x5t     | Sequencing                           │
 *    └──────────────────────────────────────────────────────────────────────────┘
 * 
 *    ┌──────────────────────────────────────────────────────────────────────────┐
 *    │ Next Flow Direction ID Mapping                                            │
 *    ├──────────────────────────────────────────────────────────────────────────┤
 *    │ Flow Name               | nextFlowId       | databaseTableSuffixTwo       │
 *    ├──────────────────────────────────────────────────────────────────────────┤
 *    │ Library Preparation   | SYLX2024000007   | LP                           │
 *    │ Enrichment            | SYLX2024000003   | E                            │
 *    │ Sequencing            | SYLX2024000008   | Se                           │
 *    │ Sample Storage        | SampleIn         | SampleIn                     │
 *    │ Stop Experimental     | StopExperimental | StopExperimental             │
 *    └──────────────────────────────────────────────────────────────────────────┘
 * 
 * ============================================================================
 * 6. Save experiment data (updateExperimentFlow) - Modify result table sample data
 * ============================================================================
 * 
 *    URL: /experimentalcenter/experiment/updateExperimentFlow
 *    
 *    Parameter structure:
 *    {
 *      "id": "<template_id>",              // ⚠️ Must be template ID, not experimentId
 *      "peopleGroupsId": "",
 *      "peopleGroupsName": "",
 *      "stepDetails": [...],               // Contains all components, keep original structure
 *      "databaseTableSuffix": "NAE",
 *      "lastStep": true,
 *      "experimentId": "NA20260021",       // Experiment ID
 *      "logArr": {...}                     // Operation log
 *    }
 *
 *    ⚠️ Key requirements:
 *    1. The id field is the template ID (e.g. c1e1f4afb9938472f5ffb9ef5b575cdd), not the experiment ID
 *    2. stepDetails must contain all components (detailTable, material, equipment, editor, resultTable, attachment)
 *    3. Only modify data in value, do not modify propList, menuList, etc.
 *    4. logArr.resultBox records modification logs
 *
 *    When modifying result table samples, the following fields are required:
 *    ┌─────────────────────┬──────────────────────────────────────────────────┐
 *    │ Field Name          │ Description                                      │
 *    ├─────────────────────┼──────────────────────────────────────────────────┤
 *    │ nextFlowId          │ Next flow direction ID (query via select-next-flow first) │
 *    │ databaseTableSuffixTwo │ Next experiment type suffix (e.g. LP, SampleIn) │
 *    │ nextFlow            │ Next flow display name (e.g. Library Preparation) │
 *    │ result              │ Result (e.g. Qualified)                          │
 *    │ resultId            │ Result ID (1=Qualified)                          │
 *    │ changeField         │ List of modified fields, comma-separated (e.g. "nextFlow,result,A260/A280") │
 *    │ flag                │ Flag (false)                                     │
 *    └─────────────────────┴──────────────────────────────────────────────────┘
 *
 *    Next flow direction query:
 *    Command: select-next-flow <suffix> <model_id> <result_ids>
 *    Example: select-next-flow NAE SYLX2024000001 "id1,id2"
 *
 *    Response result mapping:
 *    ┌─────────────────────┬────────────────┬─────────────────────┐
 *    │ Display Name        │ nextFlowId     │ databaseTableSuffixTwo │
 *    ├─────────────────────┼────────────────┼─────────────────────┤
 *    │ Sample Storage      │ SampleIn       │ SampleIn            │
 *    │ Library Preparation │ SYLX2024000007 │ LP                  │
 *    │ Stop Experimental   │ StopExperimental │ StopExperimental  │
 *    └─────────────────────┴────────────────┴─────────────────────┘
 *    
 *    Complete example (modify result table data for two samples):
 *
 *    1. Query next flow direction:
 *       node biolims.mjs select-next-flow NAE SYLX2024000001 "b84edd64c89e5418993ff1dda9f269b5,d9b2ada1035a0b5a17b261dfcc67e4f5"
 *    
 *    2. Build save parameters (JSON file):
 *       Each sample in the result table value needs to add:
 *       {
 *         "nextFlowId": "SYLX2024000007",
 *         "databaseTableSuffixTwo": "LP",
 *         "nextFlow": "Library Preparation",
 *         "result": "Qualified",
 *         "resultId": "1",
 *         "changeField": "nextFlow,result,A260/A280,A260/A230",
 *         "A260/A280": 30,
 *         "A260/A230": 40,
 *         "flag": false
 *       }
 *    
 *    3. Save:
 *       node biolims.mjs experiment-save "@/path/to/update.json"
 *    
 * ============================================================================
 */

import crypto from 'crypto';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import os from 'os';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

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

const TOKEN_CACHE_FILE = path.join(os.tmpdir(), 'biolims_token_node.json');

// ============================================================================
// Token Cache
// ============================================================================
let cachedAuth = null;

function loadTokenCache() {
  try {
    if (fs.existsSync(TOKEN_CACHE_FILE)) {
      const data = JSON.parse(fs.readFileSync(TOKEN_CACHE_FILE, 'utf8'));
      const now = Math.floor(Date.now() / 1000);
      if (data.expires_at > now) {
        return data;
      }
    }
  } catch (e) {
    // ignore
  }
  return null;
}

function saveTokenCache(auth) {
  try {
    fs.writeFileSync(TOKEN_CACHE_FILE, JSON.stringify(auth));
  } catch (e) {
    // ignore
  }
}

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
// HTTP Request (using native fetch)
// ============================================================================
async function login() {
  const encryptedPassword = encryptPassword(PASSWORD);
  const urlEncodedPassword = encodeURIComponent(encryptedPassword);
  const loginUrl = `${BASE_URL}/user/Login?username=${USERNAME}&password=${urlEncodedPassword}`;

  const response = await fetch(loginUrl, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'code': DATA_SOURCE,
      'X-DS': DATA_SOURCE,
      'accept-language': 'en',
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

  const auth = {
    token,
    xsrf,
    cookies: cookies.join('; '),
    expires_at: Math.floor(Date.now() / 1000) + 25 * 60 // 25 minutes
  };

  saveTokenCache(auth);
  cachedAuth = auth;
  return auth;
}

async function getAuth() {
  if (cachedAuth && cachedAuth.expires_at > Math.floor(Date.now() / 1000)) {
    return cachedAuth;
  }

  const cached = loadTokenCache();
  if (cached) {
    cachedAuth = cached;
    return cached;
  }

  return await login();
}

async function apiCall(method, apiPath, body = null, retry = true) {
  const auth = await getAuth();

  const headers = {
    'Content-Type': 'application/json',
    'Token': auth.token,
    'X-DS': DATA_SOURCE,
    'accept-language': 'en',
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

  // If token expired, re-login and retry
  if (data.status === 401 && retry) {
    cachedAuth = null;
    try { fs.unlinkSync(TOKEN_CACHE_FILE); } catch (e) {}
    await login();
    return apiCall(method, apiPath, body, false);
  }

  return data;
}

// ============================================================================
// Command Handlers
// ============================================================================

// ============================================================================
// Helper Functions - Dynamically get flow node ID
// ============================================================================

/**
 * Extract userTask node ID (flow node ID) from templateId XML
 */
function extractUserTaskIdFromTemplate(templateIdStr) {
  if (!templateIdStr) return null;
  // Parse XML in templateId, extract the id attribute of <userTask> node
  const userTaskMatch = templateIdStr.match(/<userTask[^>]*\sid="([^"]+)"/);
  if (userTaskMatch && userTaskMatch[1]) {
    return userTaskMatch[1];
  }
  return null;
}

/**
 * Dynamically get the flow node ID (userTask ID) of an experiment
 */
async function getFlowIdFromExperiment(suffix, experimentId) {
  // Call selectnodeexperimenter to get template info
  const resp = await apiCall('POST', '/experimentalcenter/experiment/selectnodeexperimenter', {
    bioTechLeaguePagingQuery: { page: 1, rows: 9999 },
    page: 1,
    rows: 9999,
    id: experimentId,
    databaseTableSuffix: suffix,
    templateCode: ''
  });

  if (resp.status !== 200 || !resp.data) {
    return null;
  }

  // Extract templateId from response data
  const templateId = resp.data.templateId;
  if (!templateId) {
    return null;
  }

  // If templateId is a JSON string, parse it first
  let templateIdStr = templateId;
  try {
    if (typeof templateId === 'string' && templateId.startsWith('{')) {
      const parsed = JSON.parse(templateId);
      templateIdStr = parsed.renderConfig || '';
    }
  } catch (e) {
    // Not JSON, use as-is
  }

  // Extract userTask ID from XML
  const userTaskId = extractUserTaskIdFromTemplate(templateIdStr);
  return userTaskId;
}

const commands = {
  async order(orderId) {
    if (!orderId) return { error: 'Usage: biolims.mjs order <order_id>' };
    return await apiCall('POST', '/order/selectOrder', { orderId });
  },

  async 'order-list'(page = '1', rows = '10') {
    const result = await apiCall('POST', '/order/selectAllOrderList', {
      bioTechLeaguePagingQuery: {
        page: parseInt(page),
        rows: parseInt(rows),
        sort: {},
        query: []
      }
    });

    // Simplify output, remove customFieldValue
    if (result.status === 200 && result.data?.result) {
      result.data.result = result.data.result.map(order => ({
        id: order.id,
        name: order.name,
        gender: order.gender,
        age: order.age,
        birthDate: order.birthDate,
        phone: order.phone,
        email: order.email,
        idCard: order.idCard,
        medicalNumber: order.medicalNumber,
        productId: order.productId,
        productName: order.productName,
        diagnosis: order.diagnosis,
        state: order.state,
        stateName: order.stateName,
        progress: order.progress,
        barcode: order.barcode,
        createTime: order.createTime,
        creatorNickname: order.creatorNickname,
        confirmTime: order.confirmTime,
        confirmerNickname: order.confirmerNickname,
        commissionerNickname: order.commissionerNickname,
        crmCustomerName: order.crmCustomerName,
        inspectionDepartmentName: order.inspectionDepartmentName,
        attendingDoctorName: order.attendingDoctorName,
        provinceName: order.provinceName
      }));
    }

    return result;
  },

  async 'order-samples'(orderId) {
    if (!orderId) return { error: 'Usage: biolims.mjs order-samples <order_id>' };
    return await apiCall('POST', '/order/selectSampleOrderItem', {
      orderId,
      bioTechLeaguePagingQuery: { page: 1, rows: 100, sort: {}, query: [] }
    });
  },

  async 'order-fees'(orderId) {
    if (!orderId) return { error: 'Usage: biolims.mjs order-fees <order_id>' };
    return await apiCall('POST', '/order/selectFee', { orderId });
  },

  async 'create-order'(jsonArg) {
    if (!jsonArg) return { error: 'Usage: biolims.mjs create-order \'<json>\' or @<filepath>' };
    
    let jsonBody = jsonArg;
    if (jsonArg.startsWith('@')) {
      const filePath = jsonArg.slice(1);
      if (!fs.existsSync(filePath)) {
        return { error: `File not found: ${filePath}` };
      }
      jsonBody = fs.readFileSync(filePath, 'utf8');
    }

    return await apiCall('POST', '/order/saveOrUpdateOrderAllData', JSON.parse(jsonBody));
  },

  async 'update-order'(jsonArg) {
    if (!jsonArg) return { error: 'Usage: biolims.mjs update-order \'<json>\' or @<filepath>' };
    
    let jsonBody = jsonArg;
    if (jsonArg.startsWith('@')) {
      const filePath = jsonArg.slice(1);
      if (!fs.existsSync(filePath)) {
        return { error: `File not found: ${filePath}` };
      }
      jsonBody = fs.readFileSync(filePath, 'utf8');
    }

    return await apiCall('POST', '/order/saveOrUpdateOrderAllData', JSON.parse(jsonBody));
  },

  async 'complete-order'(orderId) {
    if (!orderId) return { error: 'Usage: biolims.mjs complete-order <order_id>' };
    return await apiCall('POST', `/order/completeTask?id=${orderId}`, '');
  },

  async 'cancel-order'(orderId) {
    if (!orderId) return { error: 'Usage: biolims.mjs cancel-order <order_id>' };
    return await apiCall('POST', `/order/cancelTask?id=${orderId}`, '');
  },

  async 'sample-types'(page = '1', rows = '100') {
    return await apiCall('POST', '/order/selectPopupsSampleType', {
      page: parseInt(page),
      rows: parseInt(rows),
      sort: {},
      query: []
    });
  },

  async 'get-products'(page = '1', rows = '9999') {
    return await apiCall('POST', '/order/selectProductByCategory', {
      bioTechLeaguePagingQuery: { page: parseInt(page), rows: parseInt(rows), sort: {}, pagingSearchOne: {}, query: [] },
      page: parseInt(page),
      rows: parseInt(rows),
      sort: {},
      pagingSearchOne: {},
      query: []
    });
  },

  async 'search-sample-type'(name) {
    if (!name) return { error: 'Usage: biolims.mjs search-sample-type <sample_type_name>' };
    return await apiCall('POST', '/order/selectPopupsSampleType', {
      page: 1,
      rows: 100,
      sort: {},
      pagingSearchOne: { matchMode: ['name'], value: name },
      query: []
    });
  },

  async 'get-order-custom-fields'(flag = '104-mainTable') {
    // flag: 104-mainTable (order main table) or 104-sampleTable (sample sub-table)
    return await apiCall('GET', `/system/custom/selAllFields?flag=${flag}`, null);
  },

  // ==================== Sample Receive Commands ====================

  async 'receive-list'(page = '1', rows = '10') {
    return await apiCall('POST', '/samplecenter/clinicalSampleReceive/getSampleReceiveList', {
      bioTechLeaguePagingQuery: {
        page: parseInt(page),
        rows: parseInt(rows),
        sort: {},
        query: []
      }
    });
  },

  async 'receive'(receiveId) {
    if (!receiveId) return { error: 'Usage: biolims.mjs receive <receive_id>' };
    return await apiCall('POST', '/samplecenter/clinicalSampleReceive/getSampleReceive', { id: receiveId });
  },

  async 'receive-samples'(receiveId, page = '1', rows = '50') {
    if (!receiveId) return { error: 'Usage: biolims.mjs receive-samples <receive_id> [page] [rows]' };
    return await apiCall('POST', '/samplecenter/clinicalSampleReceive/getSampleReceiveItemList', {
      sampleReceiveId: receiveId,
      bioTechLeaguePagingQuery: {
        page: parseInt(page),
        rows: parseInt(rows),
        sort: {},
        query: []
      }
    });
  },

  async 'scan-barcode'(barcode, receiveId = '') {
    if (!barcode) {
      return { error: 'Usage: biolims.mjs scan-barcode <barcode> [receive_id]\n\nNote: receive_id is optional, a new receive order will be created automatically if not provided' };
    }
    
    // Use simplified sampleReceive structure, directly call scanBarcode API
    const body = { 
      sampleReceive: {
        id: receiveId || '',
        acceptDate: new Date().toLocaleString('sv-SE', { hour12: false }).replace(',', ''),
        state: '3',
        stateName: 'NEW',
        receiveType: '',
        ysfs: '',
        expressCompanyId: '',
        expressCompanyName: '',
        transportTypeId: '',
        transportTypeName: '',
        confirmerUsername: '',
        confirmerNickname: '',
        confirmTime: '',
        isBoard: '0'
      },
      barCode: barcode
    };
    return await apiCall('POST', '/samplecenter/clinicalSampleReceive/scanBarcode', body);
  },

  async 'scan-order'(orderCode, receiveId = '') {
    if (!orderCode) return { error: 'Usage: biolims.mjs scan-order <order_code> [receive_id]' };
    const body = { orderCode };
    if (receiveId) {
      body.sampleReceive = { id: receiveId };
    }
    return await apiCall('POST', '/samplecenter/clinicalSampleReceive/scanOrderCode', body);
  },

  async 'get-orders-for-receive'(page = '1', rows = '50') {
    return await apiCall('POST', '/samplecenter/clinicalSampleReceive/getOrderInfo', {
      bioTechLeaguePagingQuery: {
        page: parseInt(page),
        rows: parseInt(rows),
        sort: {},
        query: []
      }
    });
  },

  async 'next-flow-list'(itemIds) {
    // itemIds is a comma-separated string of sample detail IDs (not product IDs)
    // e.g.: "51f69f52656627dff6a0227cbf710c45,91ac0a21b9e68a4a4108a583975a306b"
    if (!itemIds) {
      return { error: 'Usage: biolims.mjs next-flow-list <item_id1,item_id2,...>\n\nParameter description: Provide sample detail IDs (sampleReceiveItems.id), not product IDs' };
    }
    const ids = itemIds.split(',').map(id => id.trim());
    const body = {
      ids,
      modelId: 'ClinicalSampleReceive',
      bioTechLeaguePagingQuery: {
        page: 1,
        rows: 100,
        sort: {},
        pagingSearchOne: {},
        query: []
      },
      page: 1,
      rows: 100,
      sort: {},
      pagingSearchOne: {},
      query: []
    };
    return await apiCall('POST', '/samplecenter/clinicalSampleReceive/getNextFlowListNew', body);
  },

  async 'complete-receive'(receiveId) {
    if (!receiveId) return { error: 'Usage: biolims.mjs complete-receive <receive_id>' };
    return await apiCall('POST', `/samplecenter/clinicalSampleReceive/completeTask?id=${receiveId}`, '');
  },

  async 'create-receive'(jsonArg) {
    if (!jsonArg) return { error: 'Usage: biolims.mjs create-receive \'<json>\' or @<filepath>' };
    
    let jsonBody = jsonArg;
    if (jsonArg.startsWith('@')) {
      const filePath = jsonArg.slice(1);
      if (!fs.existsSync(filePath)) {
        return { error: `File not found: ${filePath}` };
      }
      jsonBody = fs.readFileSync(filePath, 'utf8');
    }

    const data = JSON.parse(jsonBody);
    // Ensure listlogs exists, backend requires this field
    if (!data.listlogs) {
      data.listlogs = [];
    }
    return await apiCall('POST', '/samplecenter/clinicalSampleReceive/saveOrUpdateAllData', data);
  },

  async 'update-receive'(jsonArg) {
    if (!jsonArg) return { error: 'Usage: biolims.mjs update-receive \'<json>\' or @<filepath>' };
    
    let jsonBody = jsonArg;
    if (jsonArg.startsWith('@')) {
      const filePath = jsonArg.slice(1);
      if (!fs.existsSync(filePath)) {
        return { error: `File not found: ${filePath}` };
      }
      jsonBody = fs.readFileSync(filePath, 'utf8');
    }

    const inputData = JSON.parse(jsonBody);
    
    // Get receive order ID
    const receiveId = inputData.sampleReceive?.id;
    if (!receiveId) {
      return { error: 'sampleReceive.id is required when updating a receive order' };
    }

    // Get current receive order full info (search from list, since getSampleReceive may return null)
    const listData = await apiCall('POST', '/samplecenter/clinicalSampleReceive/getSampleReceiveList', {
      bioTechLeaguePagingQuery: { page: 1, rows: 100, sort: {}, query: [] }
    });
    
    let currentReceive = null;
    if (listData.status === 200 && listData.data?.result) {
      currentReceive = listData.data.result.find(r => r.id === receiveId);
    }
    
    if (!currentReceive) {
      return { error: `Receive order ${receiveId} does not exist` };
    }

    // Get current sample detail list
    const itemsData = await apiCall('POST', '/samplecenter/clinicalSampleReceive/getSampleReceiveItemList', {
      sampleReceiveId: receiveId,
      bioTechLeaguePagingQuery: { page: 1, rows: 100, sort: {}, query: [] }
    });
    
    const currentItems = itemsData.status === 200 ? (itemsData.data?.result || []) : [];
    
    // Merge receive order main table info (user input overrides current values)
    const mergedReceive = {
      id: currentReceive.id,
      code: currentReceive.code,
      name: currentReceive.name,
      acceptDate: currentReceive.acceptDate,
      isBoard: currentReceive.isBoard || '0',
      state: currentReceive.state || '3',
      receiveTypeCode: currentReceive.receiveTypeCode || 'Clinical',
      classify: currentReceive.classify,
      type: currentReceive.type,
      expressNum: currentReceive.expressNum,
      expressCompanyId: currentReceive.expressCompanyId,
      transportTypeId: currentReceive.transportTypeId,
      projectId: currentReceive.projectId,
      projectName: currentReceive.projectName,
      ...inputData.sampleReceive  // User input overrides
    };
    
    // Merge sample details (match by id, user input overrides current values)
    let mergedItems = [];
    if (inputData.sampleReceiveItems && inputData.sampleReceiveItems.length > 0) {
      for (const inputItem of inputData.sampleReceiveItems) {
        // Find current sample
        const currentItem = currentItems.find(item => item.id === inputItem.id);
        
        if (currentItem) {
          // Merge: current values + user input overrides
          mergedItems.push({
            id: currentItem.id,
            sampleReceive: currentItem.sampleReceive,
            sampleCode: currentItem.sampleCode,
            orderCode: currentItem.orderCode,
            barCode: currentItem.barCode,
            sampleTypeId: currentItem.sampleTypeId,
            sampleType: currentItem.sampleType,
            dicSampleTypeId: currentItem.dicSampleTypeId || currentItem.sampleTypeId,
            dicSampleType: currentItem.dicSampleType || currentItem.sampleType,
            productId: currentItem.productId,
            productName: currentItem.productName,
            method: currentItem.method || '1',
            unit: currentItem.unit,
            sampleNum: currentItem.sampleNum,
            gender: currentItem.gender,
            isGood: currentItem.isGood || '1',
            nextFlowId: currentItem.nextFlowId,
            nextFlow: currentItem.nextFlow,
            note: currentItem.note,
            samplingDate: currentItem.samplingDate,
            expirationDate: currentItem.expirationDate,
            periodOfValidity: currentItem.periodOfValidity,
            samplingSite: currentItem.samplingSite,
            customFieldValue: currentItem.customFieldValue,
            ...inputItem  // User input overrides
          });
        } else {
          // New sample, add directly
          mergedItems.push(inputItem);
        }
      }
    } else {
      // No sample updates provided, keep current samples
      mergedItems = currentItems.map(item => ({
        id: item.id,
        sampleReceive: item.sampleReceive,
        sampleCode: item.sampleCode,
        orderCode: item.orderCode,
        barCode: item.barCode,
        sampleTypeId: item.sampleTypeId,
        sampleType: item.sampleType,
        dicSampleTypeId: item.dicSampleTypeId || item.sampleTypeId,
        dicSampleType: item.dicSampleType || item.sampleType,
        productId: item.productId,
        productName: item.productName,
        method: item.method || '1',
        unit: item.unit,
        sampleNum: item.sampleNum,
        gender: item.gender,
        isGood: item.isGood || '1',
        nextFlowId: item.nextFlowId,
        nextFlow: item.nextFlow,
        note: item.note,
        samplingDate: item.samplingDate,
        expirationDate: item.expirationDate,
        periodOfValidity: item.periodOfValidity,
        samplingSite: item.samplingSite,
        customFieldValue: item.customFieldValue
      }));
    }
    
    const finalData = {
      sampleReceive: mergedReceive,
      sampleReceiveItems: mergedItems,
      listlogs: inputData.listlogs || []
    };
    
    return await apiCall('POST', '/samplecenter/clinicalSampleReceive/saveOrUpdateAllData', finalData);
  },

  async 'delete-receive-item'(receiveId, itemIds, isBoard = '0') {
    if (!receiveId || !itemIds) {
      return { error: 'Usage: biolims.mjs delete-receive-item <receive_id> <item_id1,item_id2,...> [isBoard]' };
    }
    const ids = itemIds.split(',').map(id => id.trim());
    return await apiCall('POST', '/samplecenter/clinicalSampleReceive/deleteSampleReceiveItem', {
      ids,
      sampleReceiveId: receiveId,
      sampleReceive: {
        id: receiveId,
        isBoard: isBoard
      }
    });
  },

  // ============================================================================
  // Hole Plate Management Commands
  // ============================================================================

  async 'auto-add-board'(receiveId, rowNum, colNum, plateNumber) {
    if (!receiveId || !rowNum || !colNum || !plateNumber) {
      return { error: 'Usage: biolims.mjs auto-add-board <receive_id> <row_num> <col_num> <plate_number>\n\nExample: biolims.mjs auto-add-board KXJY2602100008 8 12 P001' };
    }
    return await apiCall('POST', '/samplecenter/clinicalSampleReceive/autoAddBoard', {
      id: receiveId,
      rowNum: parseInt(rowNum),
      colNum: parseInt(colNum),
      banHao: plateNumber
    });
  },

  async 'clear-hole-plate'(receiveId, plateNumber) {
    if (!receiveId || !plateNumber) {
      return { error: 'Usage: biolims.mjs clear-hole-plate <receive_id> <plate_number>\n\nExample: biolims.mjs clear-hole-plate KXJY2602100008 P001' };
    }
    return await apiCall('POST', '/samplecenter/clinicalSampleReceive/clearHolePlate', {
      id: receiveId,
      counts: plateNumber
    });
  },

  async 'delete-hole-plate'(receiveId, plateNumber) {
    if (!receiveId || !plateNumber) {
      return { error: 'Usage: biolims.mjs delete-hole-plate <receive_id> <plate_number>\n\nExample: biolims.mjs delete-hole-plate KXJY2602100008 P001' };
    }
    return await apiCall('POST', '/samplecenter/clinicalSampleReceive/deleteHolePlate', {
      id: receiveId,
      counts: plateNumber
    });
  },

  async 'change-sample-location'(sampleItemId, x, y, plateNumber) {
    if (!sampleItemId || !x || !y || !plateNumber) {
      return { error: 'Usage: biolims.mjs change-sample-location <sample_item_id> <x> <y> <plate_number>\n\nExample: biolims.mjs change-sample-location ITEM001 3 5 P001' };
    }
    return await apiCall('POST', '/samplecenter/clinicalSampleReceive/changeSampleLocation', {
      sampleReceiveItemId: sampleItemId,
      x: parseInt(x),
      y: parseInt(y),
      counts: plateNumber
    });
  },

  // ============================================================================
  // Experiment Center Commands (Experiment Center)
  // ============================================================================

  // ============================================================================
  // Experiment Type Configuration Query (read-only, from masterdata module)
  // ============================================================================

  async 'experiment-type-config-list'(page = '1', rows = '20') {
    // Query experiment type configuration list (read-only permission)
    // URL: POST /masterdata/ExperimentalTypeConfiguration/ExperimentalTypeConfigurationListDTO
    // Response fields:
    //   - experimentalTypeName: Experiment type name
    //   - platform: Platform
    //   - databaseTableSuffix: Database table suffix
    //   - code: Experiment code identifier
    //   - state: Whether active
    return await apiCall('POST', '/masterdata/ExperimentalTypeConfiguration/ExperimentalTypeConfigurationListDTO', {
      bioTechLeaguePagingQuery: {
        page: parseInt(page),
        rows: parseInt(rows),
        sort: {},
        pagingSearchOne: {},
        query: []
      },
      sort: {},
      pagingSearchOne: {},
      query: [],
      tableData: [],
      page: parseInt(page),
      rows: parseInt(rows),
      totalRecords: '0',
      isQuery: '1'
    });
  },

  async 'experiment-types'() {
    return await apiCall('POST', '/experimentalcenter/experiment/selectPopupsExperimentType', {
      page: 1,
      rows: 100,
      sort: {},
      query: []
    });
  },

  async 'experiment-protocols'(suffix) {
    if (!suffix) {
      return { error: 'Usage: biolims.mjs experiment-protocols <suffix>\n\nParameter description:\n  suffix: Experiment type suffix (nae/lp/e/se)\n    nae - Nucleic Acid Extraction\n    lp  - Library Preparation\n    e   - Enrichment\n    se  - Sequencing' };
    }
    return await apiCall('POST', '/experimentalcenter/experiment/selectExperimentFlow', {
      databaseTableSuffix: suffix,
      bioTechLeaguePagingQuery: {
        page: 1,
        rows: 100,
        sort: {},
        query: []
      }
    });
  },

  async 'experiment-experimenters'(experimentId, suffix) {
    if (!experimentId || !suffix) {
      return { error: 'Usage: biolims.mjs experiment-experimenters <experiment_id> <suffix>\n\nParameter description:\n  experiment_id: Experiment ID (pass empty string "" for new experiments)\n  suffix: Experiment type suffix (nae/lp/e/se)' };
    }
    return await apiCall('POST', '/experimentalcenter/experiment/selectnodeexperimenter', {
      id: experimentId || '',
      databaseTableSuffix: suffix
    });
  },

  // ============================================================================
  // Quick Create Experiment Commands (Quick Create Experiment)
  // ============================================================================

  /**
   * Get all options needed for creating an experiment (flow list + experimenter list)
   * One call returns all dropdown options needed, for AI to display to user for selection
  /**
   * Strategy: Extract flow and experimenter info from existing experiments, more reliable than calling dropdown APIs directly
   */
  async 'get-create-experiment-options'(suffix) {
    if (!suffix) {
      return {
        error: 'Usage: biolims.mjs get-create-experiment-options <suffix>\n\n' +
               'Parameter description:\n' +
               '  suffix: Experiment type suffix (HS/WK/FJ1129/SJCX)\n\n' +
               'Function: Get all dropdown options needed for creating an experiment in one call\n' +
               '  - Experiment type info\n' +
               '  - Available experiment flow list (extracted from historical experiments)\n' +
               '  - Available experimenter list (extracted from historical experiments)\n\n' +
               'Example:\n' +
               '  biolims.mjs get-create-experiment-options NAE'
      };
    }

    // 1. Dynamically query experiment type configuration from masterdata module
    const configResult = await apiCall('POST', '/masterdata/ExperimentalTypeConfiguration/ExperimentalTypeConfigurationListDTO', {
      bioTechLeaguePagingQuery: {
        page: 1,
        rows: 100,
        sort: {},
        pagingSearchOne: {},
        query: []
      },
      sort: {},
      pagingSearchOne: {},
      query: [],
      tableData: [],
      page: 1,
      rows: 100,
      totalRecords: '0',
      isQuery: '1'
    });

    let typeInfo = null;
    if (configResult.status === 200 && configResult.data?.result) {
      // Find matching suffix from configuration list
      typeInfo = configResult.data.result.find(
        item => item.databaseTableSuffix === suffix.toUpperCase()
      );
    }

    if (!typeInfo) {
      return { 
        error: `Unknown experiment type suffix: ${suffix}\n\n` +
               `Please call experiment-type-config-list first to query all available experiment type configurations.\n` +
               `Supported suffix values: ${configResult.status === 200 ? configResult.data?.result?.map(i => i.databaseTableSuffix).join(', ') : 'unknown'}`
      };
    }

    // Extract flow and experimenter info from existing experiments (more reliable)
    const listResult = await apiCall('POST', '/experimentalcenter/experiment/selectExperimentFlowMain', {
      databaseTableSuffix: suffix.toUpperCase(),
      bioTechLeaguePagingQuery: { page: 1, rows: 100, sort: {}, query: [] }
    });

    // Use Map for deduplication
    const protocolsMap = new Map();
    const experimentersMap = new Map();

    if (listResult.status === 200 && listResult.data?.result) {
      for (const exp of listResult.data.result) {
        // Extract flow
        if (exp.experimentFlowId && exp.experimentFlowName) {
          protocolsMap.set(exp.experimentFlowId, {
            id: exp.experimentFlowId,
            name: exp.experimentFlowName
          });
        }
        // Extract experimenters (may be comma-separated multiple people)
        if (exp.peopleGroupsId && exp.peopleGroupsName) {
          const ids = exp.peopleGroupsId.split(',');
          const names = exp.peopleGroupsName.split(',');
          for (let i = 0; i < ids.length; i++) {
            const id = ids[i].trim();
            const name = names[i]?.trim() || id.toUpperCase();
            if (id) {
              experimentersMap.set(id, { id, name });
            }
          }
        }
      }
    }

    const protocols = Array.from(protocolsMap.values());
    const experimenters = Array.from(experimentersMap.values());

    return {
      status: 200,
      data: {
        experimentType: {
          suffix: typeInfo.databaseTableSuffix || suffix.toUpperCase(),
          id: typeInfo.id || '',
          name: typeInfo.experimentalTypeName || suffix.toUpperCase(),
          code: typeInfo.code || '',
          platform: typeInfo.platform || '',
          state: typeInfo.state || ''
        },
        protocols: protocols,
        experimenters: experimenters,
        usage: 'Use quick-create-experiment <suffix> <protocol_id> <experimenter_id> to create an experiment'
      }
    };
  },

  /**
   * Quick create experiment
   * Only need to provide experiment type suffix, flow ID and experimenter ID, other fields are auto-filled
   */
  async 'quick-create-experiment'(suffix, protocolId, experimenterId, experimenterName) {
    if (!suffix || !protocolId || !experimenterId) {
      return {
        error: 'Usage: biolims.mjs quick-create-experiment <suffix> <protocol_id> <experimenter_id> [experimenter_name]\n\n' +
               'Parameter description:\n' +
               '  suffix: Experiment type suffix (HS/WK/FJ1129/SJCX)\n' +
               '  protocol_id: Experiment flow ID (get from get-create-experiment-options)\n' +
               '  experimenter_id: Experimenter ID (get from get-create-experiment-options)\n' +
               '  experimenter_name: Experimenter name (optional, defaults to ID)\n\n' +
               'Example:\n' +
               '  biolims.mjs quick-create-experiment NAE ETF2026000004 yq YQ\n\n' +
               '⚠️ Recommended to call get-create-experiment-options first to get available options'
      };
    }

    // 1. Dynamically query experiment type configuration from masterdata module
    const configResult = await apiCall('POST', '/masterdata/ExperimentalTypeConfiguration/ExperimentalTypeConfigurationListDTO', {
      bioTechLeaguePagingQuery: {
        page: 1,
        rows: 100,
        sort: {},
        pagingSearchOne: {},
        query: []
      },
      sort: {},
      pagingSearchOne: {},
      query: [],
      tableData: [],
      page: 1,
      rows: 100,
      totalRecords: '0',
      isQuery: '1'
    });

    let typeInfo = null;
    if (configResult.status === 200 && configResult.data?.result) {
      // Find matching suffix from configuration list
      typeInfo = configResult.data.result.find(
        item => item.databaseTableSuffix === suffix.toUpperCase()
      );
    }

    if (!typeInfo) {
      return { 
        error: `Unknown experiment type suffix: ${suffix}\n\n` +
               `Please call experiment-type-config-list first to query all available experiment type configurations.\n` +
               `Supported suffix values: ${configResult.status === 200 ? configResult.data?.result?.map(i => i.databaseTableSuffix).join(', ') : 'unknown'}`
      };
    }

    // Get flow name from existing experiments (more reliable than calling dropdown API directly)
    const listResult = await apiCall('POST', '/experimentalcenter/experiment/selectExperimentFlowMain', {
      databaseTableSuffix: suffix.toUpperCase(),
      bioTechLeaguePagingQuery: { page: 1, rows: 50, sort: {}, query: [] }
    });

    let protocolName = protocolId;
    if (listResult.status === 200 && listResult.data?.result) {
      const matchingExp = listResult.data.result.find(exp => exp.experimentFlowId === protocolId);
      if (matchingExp) {
        protocolName = matchingExp.experimentFlowName;
      }
    }

    // Build complete parameters for creating experiment
    const createPayload = {
      name: null,
      type: typeInfo.id,
      typeName: typeInfo.experimentalTypeName || suffix.toUpperCase(),
      databaseTableSuffix: suffix.toUpperCase(),
      code: typeInfo.code,
      experimentFlowId: protocolId,
      experimentFlowName: protocolName,
      peopleGroupsId: experimenterId,
      peopleGroupsName: experimenterName || experimenterId.toUpperCase(),
      detection: null,
      gruopId: '',
      sampleId: null
    };

    return await apiCall('POST', '/experimentalcenter/experiment/addExperimentFlowMain', createPayload);
  },

  async 'create-experiment'(jsonArg) {
    if (!jsonArg) {
      return {
        error: 'Usage: biolims.mjs create-experiment \'<json>\' or @<filepath>\n\n' +
               'Required fields:\n' +
               '  - type: Experiment type ID (e.g. SYLX2024000001)\n' +
               '  - typeName: Experiment type name (e.g. Nucleic Acid Extraction)\n' +
               '  - databaseTableSuffix: Experiment type suffix (NAE/LP/E/Se)\n' +
               '  - code: Experiment type code (NA/LP/E/Se)\n' +
               '  - experimentFlowId: Experiment flow ID (e.g. ETF2026000004)\n' +
               '  - experimentFlowName: Experiment flow name\n' +
               '  - peopleGroupsId: Experimenter ID (e.g. yq)\n' +
               '  - peopleGroupsName: Experimenter name (e.g. YQ)\n\n' +
               'Optional fields:\n' +
               '  - name: Experiment description (can be null)\n' +
               '  - detection: Detection project (can be null)\n' +
               '  - gruopId: Group ID (can be empty string)\n' +
               '  - sampleId: Sample ID (can be null)\n\n' +
               'Example:\n' +
               '{\n' +
               '  "name": null,\n' +
               '  "type": "SYLX2024000001",\n' +
               '  "typeName": "Nucleic Acid Extraction",\n' +
               '  "databaseTableSuffix": "NAE",\n' +
               '  "code": "NA",\n' +
               '  "experimentFlowId": "ETF2026000004",\n' +
               '  "experimentFlowName": "Lymph cfDNA Extraction and QC",\n' +
               '  "peopleGroupsId": "yq",\n' +
               '  "peopleGroupsName": "YQ",\n' +
               '  "detection": null,\n' +
               '  "gruopId": "",\n' +
               '  "sampleId": null\n' +
               '}'
      };
    }

    let jsonBody = jsonArg;
    if (jsonArg.startsWith('@')) {
      const filePath = jsonArg.slice(1);
      if (!fs.existsSync(filePath)) {
        return { error: `File not found: ${filePath}` };
      }
      jsonBody = fs.readFileSync(filePath, 'utf8');
    }

    return await apiCall('POST', '/experimentalcenter/experiment/addExperimentFlowMain', JSON.parse(jsonBody));
  },

  async 'experiment-list'(suffix, page = '1', rows = '10') {
    if (!suffix) {
      return { error: 'Usage: biolims.mjs experiment-list <suffix> [page] [rows]\n\nParameter description:\n  suffix: Experiment type suffix (nae/lp/e/se)' };
    }
    return await apiCall('POST', '/experimentalcenter/experiment/selectExperimentFlowMain', {
      databaseTableSuffix: suffix,
      bioTechLeaguePagingQuery: {
        page: parseInt(page),
        rows: parseInt(rows),
        sort: {},
        query: []
      }
    });
  },

  async 'experiment-detail'(experimentId, suffix) {
    if (!experimentId || !suffix) {
      return { error: 'Usage: biolims.mjs experiment-detail <experiment_id> <suffix>\n\nParameter description:\n  experiment_id: Experiment ID\n  suffix: Experiment type suffix (nae/lp/e/se)' };
    }
    return await apiCall('POST', '/experimentalcenter/experiment/selectExperimentById', {
      id: experimentId,
      databaseTableSuffix: suffix
    });
  },

  async 'experiment-save'(jsonArg) {
    if (!jsonArg) {
      return {
        error: 'Usage: biolims.mjs experiment-save \'<json>\' or @<filepath>\n\n' +
               'Required fields:\n' +
               '  - databaseTableSuffix: Experiment type suffix (nae/lp/e/se)\n' +
               '  - experimentId: Experiment ID\n' +
               '  - stepDetails: Step data object\n\n' +
               'Optional fields:\n' +
               '  - logArr: Operation log object'
      };
    }

    let jsonBody = jsonArg;
    if (jsonArg.startsWith('@')) {
      const filePath = jsonArg.slice(1);
      if (!fs.existsSync(filePath)) {
        return { error: `File not found: ${filePath}` };
      }
      jsonBody = fs.readFileSync(filePath, 'utf8');
    }

    return await apiCall('POST', '/experimentalcenter/experiment/updateExperimentFlow', JSON.parse(jsonBody));
  },

  // ============================================================================
  // Simplified Result Table Update Commands (Simplified Result Table Update)
  // ============================================================================

  /**
   * update-result - Simplified result table update command
  /**
   * Automatically fetches complete stepDetails, only updates specified fields, preserves all other content
  /**
   * Usage: biolims.mjs update-result <suffix> <experiment_id> <flow_id> '<updates_json>'
  /**
   * updates_json format:
   * [
   *   {
   *     "id": "Result table sample ID",
   *     "result": "Qualified",
   *     "nextFlow": "Enrichment",
   *     "nextFlowId": "SYLX2024000003",
   *     "databaseTableSuffixTwo": "E",
   *     // ... other fields to update
   *   }
   * ]
  /**
   * Or a single object (automatically converted to array):
   * {
   *   "id": "Result table sample ID",
   *   "result": "Qualified",
   *   ...
   * }
   */
  async 'update-result'(suffix, experimentId, flowId, updatesArg) {
    if (!suffix || !experimentId || !flowId || !updatesArg) {
      return {
        error: 'Usage: biolims.mjs update-result <suffix> <experiment_id> <flow_id> \'<updates_json>\'\n\n' +
               'Parameter description:\n' +
               '  suffix: Experiment type suffix (HS/WK/FJ1129/SJCX)\n' +
               '  experiment_id: Experiment ID (e.g. LP20260015)\n' +
               '  flow_id: Flow node ID (e.g. Activity_1nzvwkd)\n' +
               '  updates_json: Fields to update (JSON format, supports @filepath)\n\n' +
               'Examples:\n' +
               '  # Update single sample result\n' +
               '  biolims.mjs update-result LP LP20260015 Activity_1nzvwkd \'{\n' +
               '    "id": "d9fcd20e9947118520d32fc65f1d4e6f",\n' +
               '    "result": "Qualified",\n' +
               '    "nextFlow": "Enrichment",\n' +
               '    "nextFlowId": "SYLX2024000003",\n' +
               '    "databaseTableSuffixTwo": "E"\n' +
               '  }\'\n\n' +
               '  # Update multiple samples\n' +
               '  biolims.mjs update-result NAE NA20260028 Activity_1vzdimw \'[\n' +
               '    {"id": "id1", "result": "Qualified", "nextFlow": "Library Preparation", ...},\n' +
               '    {"id": "id2", "result": "Qualified", "nextFlow": "Library Preparation", ...}\n' +
               '  ]\'\n\n' +
               'Common update fields:\n' +
               '  - result: Result (Qualified/Unqualified)\n' +
               '  - resultId: Result ID (1=Qualified)\n' +
               '  - nextFlow: Next flow direction display name\n' +
               '  - nextFlowId: Next flow direction ID\n' +
               '  - databaseTableSuffixTwo: Next experiment type suffix'
      };
    }

    // 1. Parse update data
    let updatesJson = updatesArg;
    if (updatesArg.startsWith('@')) {
      const filePath = updatesArg.slice(1);
      if (!fs.existsSync(filePath)) {
        return { error: `File not found: ${filePath}` };
      }
      updatesJson = fs.readFileSync(filePath, 'utf8');
    }

    let updates;
    try {
      updates = JSON.parse(updatesJson);
    } catch (e) {
      return { error: `JSON parse failed: ${e.message}` };
    }

    // If single object, convert to array
    if (!Array.isArray(updates)) {
      updates = [updates];
    }

    // Validate each update has an id
    for (const update of updates) {
      if (!update.id) {
        return { error: 'Each update object must contain an "id" field (result table sample ID)' };
      }
    }

    // 2. Get current experiment template data
    const templateResp = await apiCall('POST', '/experimentalcenter/experiment/selectOrAddExperimentFlowTemplate', {
      experimentFlowId: experimentId,
      flow: flowId,
      databaseTableSuffix: suffix
    });

    if (templateResp.status !== 200) {
      return { error: `Failed to get experiment template: ${templateResp.msg || JSON.stringify(templateResp)}` };
    }

    const templateData = templateResp.data;
    if (!templateData || !templateData.stepDetails || templateData.stepDetails.length === 0) {
      return { error: 'Experiment template data is empty or has incorrect format' };
    }

    // 3. Find result table component and update
    let resultTableFound = false;
    let updatedSampleCodes = [];
    
    for (const step of templateData.stepDetails) {
      if (!step.jsonDatas) continue;
      
      for (const component of step.jsonDatas) {
        if (component.type === 'resultTable' && component.value) {
          resultTableFound = true;
          
          // Parse current result table data
          let resultItems;
          try {
            resultItems = JSON.parse(component.value);
          } catch (e) {
            return { error: `Result table value parse failed: ${e.message}` };
          }

          // Update matching samples
          for (const item of resultItems) {
            const updateData = updates.find(u => u.id === item.id);
            if (updateData) {
              // Record modified fields
              const changedFields = [];
              
              // Only update specified fields, preserve all other content
              for (const [key, value] of Object.entries(updateData)) {
                if (key !== 'id') {  // id doesn't need updating
                  item[key] = value;
                  changedFields.push(key);
                }
              }
              
              // Add changeField and flag
              item.changeField = changedFields.join(',');
              item.flag = false;
              
              updatedSampleCodes.push(item.sampleCode || item.id);
            }
          }

          // Re-serialize (keep compact format)
          component.value = JSON.stringify(resultItems);
          
          // Clean propList/menuList/productList, only keep necessary ones
          // Note: These fields need to keep original values, do not clear to "[]"
        }
        
        // For non-result-table components, clean value to simplified format to reduce data size
        // But preserve original structure
        if (component.type !== 'resultTable' && component.type !== 'detailTable') {
          // Preserve original value, no modification
        }
      }
    }

    if (!resultTableFound) {
      return { error: 'Result table component not found (type=resultTable)' };
    }

    if (updatedSampleCodes.length === 0) {
      return { error: 'No matching sample IDs found, please check the ids in updates' };
    }

    // 4. Build save request
    const savePayload = {
      id: templateData.id,
      peopleGroupsId: templateData.peopleGroupsId || '',
      peopleGroupsName: templateData.peopleGroupsName || '',
      stepDetails: templateData.stepDetails,
      databaseTableSuffix: suffix,
      lastStep: true,
      experimentId: experimentId,
      logArr: {
        resultBox: updatedSampleCodes.map(code => ({
          sampleCode: code,
          changeField: updates.find(u => u.id === code)?.changeField || 
                       Object.keys(updates[0]).filter(k => k !== 'id').join(',')
        }))
      }
    };

    // 5. Save
    const saveResp = await apiCall('POST', '/experimentalcenter/experiment/updateExperimentFlow', savePayload);

    if (saveResp.status === 200) {
      return {
        status: 200,
        msg: 'OK',
        data: {
          updatedSamples: updatedSampleCodes,
          count: updatedSampleCodes.length
        }
      };
    } else {
      return saveResp;
    }
  },

  /**
   * update-detail - Simplified detail table update command
  /**
   * Automatically fetches complete stepDetails, only updates specified fields, preserves all other content
  /**
   * Usage: biolims.mjs update-detail <suffix> <experiment_id> <flow_id> '<updates_json>'
   */
  async 'update-detail'(suffix, experimentId, flowId, updatesArg) {
    if (!suffix || !experimentId || !flowId || !updatesArg) {
      return {
        error: 'Usage: biolims.mjs update-detail <suffix> <experiment_id> <flow_id> \'<updates_json>\'\n\n' +
               'Parameter description:\n' +
               '  suffix: Experiment type suffix (HS/WK/FJ1129/SJCX)\n' +
               '  experiment_id: Experiment ID\n' +
               '  flow_id: Flow node ID\n' +
               '  updates_json: Fields to update (JSON format, supports @filepath)\n\n' +
               'Example:\n' +
               '  biolims.mjs update-detail LP LP20260015 Activity_1nzvwkd \'{\n' +
               '    "id": "Sample detail ID",\n' +
               '    "SCN": 25.5,\n' +
               '    "VOL": 8.0\n' +
               '  }\''
      };
    }

    // 1. Parse update data
    let updatesJson = updatesArg;
    if (updatesArg.startsWith('@')) {
      const filePath = updatesArg.slice(1);
      if (!fs.existsSync(filePath)) {
        return { error: `File not found: ${filePath}` };
      }
      updatesJson = fs.readFileSync(filePath, 'utf8');
    }

    let updates;
    try {
      updates = JSON.parse(updatesJson);
    } catch (e) {
      return { error: `JSON parse failed: ${e.message}` };
    }

    if (!Array.isArray(updates)) {
      updates = [updates];
    }

    for (const update of updates) {
      if (!update.id) {
        return { error: 'Each update object must contain an "id" field (detail table sample ID)' };
      }
    }

    // 2. Get current experiment template data
    const templateResp = await apiCall('POST', '/experimentalcenter/experiment/selectOrAddExperimentFlowTemplate', {
      experimentFlowId: experimentId,
      flow: flowId,
      databaseTableSuffix: suffix
    });

    if (templateResp.status !== 200) {
      return { error: `Failed to get experiment template: ${templateResp.msg || JSON.stringify(templateResp)}` };
    }

    const templateData = templateResp.data;
    if (!templateData || !templateData.stepDetails || templateData.stepDetails.length === 0) {
      return { error: 'Experiment template data is empty or has incorrect format' };
    }

    // 3. Find detail table component and update
    let detailTableFound = false;
    let updatedSampleCodes = [];
    
    for (const step of templateData.stepDetails) {
      if (!step.jsonDatas) continue;
      
      for (const component of step.jsonDatas) {
        if (component.type === 'detailTable' && component.value) {
          detailTableFound = true;
          
          let detailItems;
          try {
            detailItems = JSON.parse(component.value);
          } catch (e) {
            return { error: `Detail table value parse failed: ${e.message}` };
          }

          for (const item of detailItems) {
            const updateData = updates.find(u => u.id === item.id);
            if (updateData) {
              for (const [key, value] of Object.entries(updateData)) {
                if (key !== 'id') {
                  item[key] = value;
                }
              }
              updatedSampleCodes.push(item.sampleCode || item.id);
            }
          }

          component.value = JSON.stringify(detailItems);
        }
      }
    }

    if (!detailTableFound) {
      return { error: 'Detail table component not found (type=detailTable)' };
    }

    if (updatedSampleCodes.length === 0) {
      return { error: 'No matching sample IDs found' };
    }

    // 4. Save
    const savePayload = {
      id: templateData.id,
      peopleGroupsId: templateData.peopleGroupsId || '',
      peopleGroupsName: templateData.peopleGroupsName || '',
      stepDetails: templateData.stepDetails,
      databaseTableSuffix: suffix,
      lastStep: true,
      experimentId: experimentId,
      logArr: {}
    };

    const saveResp = await apiCall('POST', '/experimentalcenter/experiment/updateExperimentFlow', savePayload);

    if (saveResp.status === 200) {
      return {
        status: 200,
        msg: 'OK',
        data: {
          updatedSamples: updatedSampleCodes,
          count: updatedSampleCodes.length
        }
      };
    } else {
      return saveResp;
    }
  },

  // ============================================================================
  // Sample Pool Management Commands (Sample Pool Management)
  // ============================================================================

  async 'experiment-sample-pool'(suffix, page = '1', rows = '10', experimentId = null) {
    // Legacy suffix to type (experiment type ID) mapping (backward compatible)
    const SUFFIX_TO_TYPE = {
      'HS':     'SYLX2024000015',  // Nucleic Acid Extraction (new)
      'WK':     'SYLX2024000014',  // Library Preparation (new)
      'FJ1129': 'SYLX2024000017',  // Enrichment (new)
      'SJCX':   'SYLX2024000003',  // Sequencing
      'NAE':    'SYLX2024000001',  // Nucleic Acid Extraction
      'LP':     'SYLX2024000007',  // Library Preparation
      'E':      'SYLX2024000003',  // Enrichment
      'Se':     'SYLX2024000008'   // Sequencing
    };

    if (!suffix) {
      return {
        error: 'Usage: biolims.mjs experiment-sample-pool <suffix> [page] [rows] [experiment_id]\n\n' +
               'Parameter description:\n' +
               '  suffix: Experiment type suffix (e.g. HS/WK/FJ1129/SJCX/Cell_Culture/Treatment etc.)\n' +
               '  page: Page number (optional, default 1)\n' +
               '  rows: Rows per page (optional, default 10)\n' +
               '  experiment_id: Experiment ID (optional, e.g. CC20260002; queries first experiment of this type if not provided)\n\n' +
               'Function: Query pending samples in the sample pool\n\n' +
               'Examples:\n' +
               '  biolims.mjs experiment-sample-pool HS              # Query nucleic acid extraction sample pool\n' +
               '  biolims.mjs experiment-sample-pool Cell_Culture    # Query cell culture sample pool\n' +
               '  biolims.mjs experiment-sample-pool LP 1 50         # Query library preparation sample pool\n' +
               '  biolims.mjs experiment-sample-pool Cell_Culture 1 20 CC20260003  # Query specific experiment'
      };
    }

    // 1. First query experiment type configuration to get type ID
    let type = SUFFIX_TO_TYPE[suffix];
    let experimentFlowId = experimentId;  // Use the provided experiment ID
    let flow = null;
    let index = 4;

    // Call experiment type configuration query API
    const configResult = await apiCall('POST', '/masterdata/ExperimentalTypeConfiguration/ExperimentalTypeConfigurationListDTO', {
      bioTechLeaguePagingQuery: { page: 1, rows: 100, sort: {}, pagingSearchOne: {}, query: [] },
      sort: {}, pagingSearchOne: {}, query: [], tableData: [], page: 1, rows: 100, totalRecords: '0', isQuery: '1'
    });

    let typeInfo = null;
    if (configResult.status === 200 && configResult.data?.result) {
      typeInfo = configResult.data.result.find(item => item.databaseTableSuffix === suffix);
    }

    if (typeInfo) {
      // Use queried experiment type ID
      type = typeInfo.id;  // e.g. SYLX2026000013
      
      // Query flow info for this experiment type
      const flowResult = await apiCall('POST', '/experimentalcenter/experiment/selectExperimentFlowMain', {
        databaseTableSuffix: suffix,
        bioTechLeaguePagingQuery: { page: 1, rows: 50, sort: {}, query: [] }
      });

      if (flowResult.status === 200 && flowResult.data?.result?.length > 0) {
        // If experimentId provided, find matching; otherwise use first
        let flowInfo;
        if (experimentId) {
          flowInfo = flowResult.data.result.find(item => item.experimentFlowId === experimentId || 
                  (item.templateId && typeof item.templateId === 'string' && item.templateId.includes(experimentId)));
        }
        if (!flowInfo) {
          flowInfo = flowResult.data.result[0];
        }
        
        // Parse flow node ID from templateId XML
        if (flowInfo.templateId) {
          try {
            const templateObj = typeof flowInfo.templateId === 'string' ? JSON.parse(flowInfo.templateId) : flowInfo.templateId;
            const renderConfig = templateObj.renderConfig || '';
            // Parse userTask id from XML
            const userTaskMatch = renderConfig.match(/<userTask[^>]+id="([^"]+)"/);
            if (userTaskMatch) {
              flow = userTaskMatch[1];
            }
          } catch (e) {
            // XML parsing failed, using default
          }
        }
      }
    } else if (!type) {
      // Neither a known suffix nor found in config
      return {
        error: `Unknown experiment type suffix: ${suffix}\n\n` +
               `Please call experiment-type-config-list to query all available experiment type configs.\n` +
               `Supported suffixes: ${configResult.status === 200 ? configResult.data?.result?.map(i => i.databaseTableSuffix).join(', ') : 'Unknown'}`
      };
    }

    // If flow not resolved, use default
    if (!flow) {
      flow = 'Activity_1h3w2cm';  // Cell_Culture default flow
    }

    // If no experimentId, use first experiment ID
    if (!experimentFlowId) {
      const flowResult = await apiCall('POST', '/experimentalcenter/experiment/selectExperimentFlowMain', {
        databaseTableSuffix: suffix,
        bioTechLeaguePagingQuery: { page: 1, rows: 50, sort: {}, query: [] }
      });
      if (flowResult.status === 200 && flowResult.data?.result?.length > 0) {
        // Try to parse experiment ID from templateId (if exists)
        experimentFlowId = suffix === 'Cell_Culture' ? 'CC20260002' : null;
      }
    }

    const payload = {
      bioTechLeaguePagingQuery: {
        page: parseInt(page),
        rows: parseInt(rows),
        sort: {
          sortFiled: 'original_sample_code',
          isCustomed: false,
          sortOrder: 1
        },
        pagingSearchOne: {},
        query: []
      },
      sort: {},
      pagingSearchOne: {},
      query: [],
      tableData: [],
      page: parseInt(page),
      rows: parseInt(rows),
      databaseTableSuffix: suffix,
      type: type,
      index: index,
      experimentFlowId: experimentFlowId,
      flow: flow,
      testProject: null
    };
    return await apiCall('POST', '/experimentalcenter/experiment/selectSamplePool', payload);
  },


  async 'experiment-sample-pool-by-code'(suffix, sampleCode) {
    if (!suffix || !sampleCode) {
      return {
        error: 'Usage: biolims.mjs experiment-sample-pool-by-code <suffix> <sample_code>\n\n' +
               'Parameters:\n' +
               '  suffix: Experiment type suffix (HS/WK/FJ1129/SJCX)\n' +
               '  sample_code: Sample code\n\n' +
               'Function:Query sample info by sample code in sample pool'
      };
    }
    return await apiCall('POST', '/experimentalcenter/experiment/selectSamplePoolBySampleCode', {
      databaseTableSuffix: suffix,
      sampleCode: sampleCode
    });
  },

  async 'experiment-add-samples'(suffix, experimentId, flowId, sampleIds) {
    if (!suffix || !experimentId || !sampleIds) {
      return {
        error: 'Usage:biolims.mjs experiment-add-samples <suffix> <experiment_id> [flow_id] <sample_ids>\n\n' +
               'Parameters:\n' +
               '  suffix: Experiment type suffix (HS/WK/FJ1129/SJCX)\n' +
               '  experiment_id: Experiment ID (e.g. HS20260002)\n' +
               '  flow_id: Flow node ID (optional, auto-queried from experiment by default)\n' +
               '  sample_ids: Sample ID list from pool (comma-separated, pool record id field)\n\n' +
               'Example:\n' +
               '  biolims.mjs experiment-add-samples HS HS20260002 "62e731ae2be5a15a2264aaffc7caa9a4"\n' +
               '  biolims.mjs experiment-add-samples HS HS20260002 Activity_00me3he "id1,id2"\n\n' +
               'Function:Select samples from pool to add to experiment'
      };
    }

    // If only 3 args, 3rd is sampleIds, need to dynamically query flowId
    let actualFlowId = flowId;
    let actualSampleIds = sampleIds;
    if (!sampleIds || sampleIds === undefined) {
      // flowId is actually sampleIds
      actualSampleIds = flowId;
      // Dynamically query flowId
      actualFlowId = await getFlowIdFromExperiment(suffix, experimentId);
      if (!actualFlowId) {
        return { error: `Cannot auto-get flow node ID, please specify flow_id manually. Experiment: ${experimentId}` };
      }
    }

    const ids = actualSampleIds.split(',').map(id => id.trim());
    return await apiCall('POST', '/experimentalcenter/experiment/addExperimentSamplePool', {
      ids: ids,
      experimentFlowId: experimentId,
      flow: actualFlowId,
      databaseTableSuffix: suffix
    });
  },
  async 'experiment-remove-samples'(suffix, experimentId, sampleIds) {
    if (!suffix || !experimentId || !sampleIds) {
      return {
        error: 'Usage: biolims.mjs experiment-remove-samples <suffix> <experiment_id> <sample_ids>\n\n' +
               'Parameters:\n' +
               '  suffix: Experiment type suffix (HS/WK/FJ1129/SJCX)\n' +
               '  experiment_id: Experiment ID\n' +
               '  sample_ids: Sample detail ID list (comma-separated)\n\n' +
               'Function:Remove samples from experiment, return to pool'
      };
    }
    const ids = sampleIds.split(',').map(id => id.trim());
    return await apiCall('POST', '/experimentalcenter/experiment/deleteSamplePool', {
      databaseTableSuffix: suffix,
      id: experimentId,
      ids: ids
    });
  },

  async 'experiment-add-samples-to-step'(suffix, experimentId, templateItemId, sampleIds) {
    if (!suffix || !experimentId || !templateItemId || !sampleIds) {
      return {
        error: 'Usage: biolims.mjs experiment-add-samples-to-step <suffix> <experiment_id> <template_item_id> <sample_ids>\n\n' +
               'Parameters:\n' +
               '  suffix: Experiment type suffix (HS/WK/FJ1129/SJCX)\n' +
               '  experiment_id: Experiment ID\n' +
               '  template_item_id: Template field ID\n' +
               '  sample_ids: Sample ID list (comma-separated)\n\n' +
               'Function:Add samples from pending pool to experiment step template'
      };
    }
    const ids = sampleIds.split(',').map(id => id.trim());
    return await apiCall('POST', '/experimentalcenter/experiment/addExperimentSamplePool', {
      databaseTableSuffix: suffix,
      id: experimentId,
      ids: ids,
      templateItemId: templateItemId
    });
  },

  // ============================================================================
  // Sample Mixing Commands (Sample Mixing)
  // ============================================================================

  async 'experiment-mix-samples'(suffix, experimentId, sampleIds) {
    if (!suffix || !experimentId || !sampleIds) {
      return {
        error: 'Usage: biolims.mjs experiment-mix-samples <suffix> <experiment_id> <sample_ids>\n\n' +
               'Parameters:\n' +
               '  suffix: Experiment type suffix (HS/WK/FJ1129/SJCX)\n' +
               '  experiment_id: Experiment ID\n' +
               '  sample_ids: Sample IDs to mix (comma-separated)\n\n' +
               'Function:Merge multiple samples into one mixed sample'
      };
    }
    const ids = sampleIds.split(',').map(id => id.trim());
    return await apiCall('POST', '/experimentalcenter/experiment/mixSample', {
      databaseTableSuffix: suffix,
      id: experimentId,
      ids: ids
    });
  },

  async 'experiment-cancel-mix'(suffix, experimentId, sampleIds) {
    if (!suffix || !experimentId || !sampleIds) {
      return {
        error: 'Usage: biolims.mjs experiment-cancel-mix <suffix> <experiment_id> <sample_ids>\n\n' +
               'Parameters:\n' +
               '  suffix: Experiment type suffix (HS/WK/FJ1129/SJCX)\n' +
               '  experiment_id: Experiment ID\n' +
               '  sample_ids: Sample IDs to cancel mix (comma-separated)\n\n' +
               'Function:Cancel sample mixing'
      };
    }
    const ids = sampleIds.split(',').map(id => id.trim());
    return await apiCall('POST', '/experimentalcenter/experiment/cancelMaxSample', {
      databaseTableSuffix: suffix,
      id: experimentId,
      ids: ids
    });
  },

  // ============================================================================
  // Experiment Type & Flow Management (Extended)
  // ============================================================================

  async 'experiment-types-by-role'(page = '1', rows = '10') {
    return await apiCall('POST', '/experimentalcenter/experiment/selectPopupsExperimentTypeByRole', {
      page: parseInt(page),
      rows: parseInt(rows),
      sort: {},
      query: []
    });
  },

  async 'experiment-types-user-role'(page = '1', rows = '10') {
    return await apiCall('POST', '/experimentalcenter/experiment/selectPopupsExperimentTypeUserRole', {
      page: parseInt(page),
      rows: parseInt(rows),
      sort: {},
      query: []
    });
  },

  async 'create-experiment-flow'(jsonArg) {
    if (!jsonArg) {
      return { error: 'Usage: biolims.mjs create-experiment-flow \'<json>\'\n\nRequired fields: name, databaseTableSuffix, experimentTypeId' };
    }
    let jsonBody = jsonArg;
    if (jsonArg.startsWith('@')) {
      const filePath = jsonArg.slice(1);
      if (!fs.existsSync(filePath)) return { error: `File not found: ${filePath}` };
      jsonBody = fs.readFileSync(filePath, 'utf8');
    }
    return await apiCall('POST', '/experimentalcenter/experiment/addExperimentFlow', JSON.parse(jsonBody));
  },

  async 'create-experiment-flow-new'(jsonArg) {
    if (!jsonArg) {
      return { error: 'Usage: biolims.mjs create-experiment-flow-new \'<json>\'' };
    }
    let jsonBody = jsonArg;
    if (jsonArg.startsWith('@')) {
      const filePath = jsonArg.slice(1);
      if (!fs.existsSync(filePath)) return { error: `File not found: ${filePath}` };
      jsonBody = fs.readFileSync(filePath, 'utf8');
    }
    return await apiCall('POST', '/experimentalcenter/experiment/addExperimentFlowNew', JSON.parse(jsonBody));
  },

  async 'experiment-flow-by-product'(suffix, productId) {
    if (!suffix || !productId) {
      return { error: 'Usage: biolims.mjs experiment-flow-by-product <suffix> <product_id>' };
    }
    return await apiCall('POST', '/experimentalcenter/experiment/selectExperimentFlowByProductId', {
      productId: productId,
      databaseTableSuffix: suffix
    });
  },

  async 'experiment-flow-by-id'(suffix, flowId) {
    if (!suffix || !flowId) {
      return { error: 'Usage: biolims.mjs experiment-flow-by-id <suffix> <flow_id>' };
    }
    return await apiCall('POST', '/experimentalcenter/experiment/selectExperimentFlowById', {
      id: flowId,
      databaseTableSuffix: suffix
    });
  },

  async 'create-experiment-with-items'(jsonArg) {
    if (!jsonArg) {
      return { error: 'Usage: biolims.mjs create-experiment-with-items \'<json>\'' };
    }
    let jsonBody = jsonArg;
    if (jsonArg.startsWith('@')) {
      const filePath = jsonArg.slice(1);
      if (!fs.existsSync(filePath)) return { error: `File not found: ${filePath}` };
      jsonBody = fs.readFileSync(filePath, 'utf8');
    }
    return await apiCall('POST', '/experimentalcenter/experiment/addExperimentFlowMainAndItems', JSON.parse(jsonBody));
  },

  // ============================================================================
  // Experiment Order Query & Update
  // ============================================================================

  async 'update-experiment'(jsonArg) {
    if (!jsonArg) {
      return { error: 'Usage: biolims.mjs update-experiment \'<json>\'' };
    }
    let jsonBody = jsonArg;
    if (jsonArg.startsWith('@')) {
      const filePath = jsonArg.slice(1);
      if (!fs.existsSync(filePath)) return { error: `File not found: ${filePath}` };
      jsonBody = fs.readFileSync(filePath, 'utf8');
    }
    return await apiCall('POST', '/experimentalcenter/experiment/updateExperiment', JSON.parse(jsonBody));
  },

  async 'update-experiment-by-id'(suffix, experimentId) {
    if (!suffix || !experimentId) {
      return { error: 'Usage: biolims.mjs update-experiment-by-id <suffix> <experiment_id>' };
    }
    return await apiCall('POST', `/experimentalcenter/experiment/updateExperimentById?tableName=${suffix}&id=${experimentId}`, {});
  },

  async 'submit-experiment'(jsonArg) {
    if (!jsonArg) {
      return { error: 'Usage: biolims.mjs submit-experiment \'<json>\'' };
    }
    let jsonBody = jsonArg;
    if (jsonArg.startsWith('@')) {
      const filePath = jsonArg.slice(1);
      if (!fs.existsSync(filePath)) return { error: `File not found: ${filePath}` };
      jsonBody = fs.readFileSync(filePath, 'utf8');
    }
    return await apiCall('POST', '/experimentalcenter/experiment/submit', JSON.parse(jsonBody));
  },

  async 'get-experiment-info'(suffix, experimentId) {
    if (!suffix || !experimentId) {
      return { error: 'Usage: biolims.mjs get-experiment-info <suffix> <experiment_id>' };
    }
    return await apiCall('POST', '/experimentalcenter/experiment/getExperimentInfo', {
      id: experimentId,
      databaseTableSuffix: suffix
    });
  },

  async 'experiment-result-info'(resultTable, templateItemId) {
    if (!resultTable || !templateItemId) {
      return { error: 'Usage: biolims.mjs experiment-result-info <result_table> <template_item_id>' };
    }
    return await apiCall('POST', `/experimentalcenter/experiment/selectExperimentResultInfo?resultTable=${resultTable}&templateItemId=${templateItemId}`, {});
  },

  async 'experiment-node-info'(suffix, experimentId, flowId) {
    if (!suffix || !experimentId || !flowId) {
      return { error: 'Usage: biolims.mjs experiment-node-info <suffix> <experiment_id> <flow_id>' };
    }
    return await apiCall('POST', '/experimentalcenter/experiment/selectNodeInfo', {
      id: experimentId,
      databaseTableSuffix: suffix,
      flowId: flowId
    });
  },

  async 'experiment-template'(suffix, experimentId, flowId, templateId = '') {
    if (!suffix || !experimentId || !flowId) {
      return { 
        error: 'Usage: biolims.mjs experiment-template <suffix> <experiment_id> <flow_id>\n\n' +
               'Parameters:\n' +
               '  suffix: Experiment type suffix (HS/WK/FJ1129/SJCX)\n' +
               '  experiment_id: Experiment ID (e.g. NA20260021)\n' +
               '  flow_id: Flow node ID (e.g. Activity_0uh63rf)\n\n' +
               'Response:\n' +
               '  stepDetails: Contains all components\n' +
               '  - type="detailTable": Detail table (sample list)\n' +
               '  - type="resultTable": Result table\n' +
               '  - value: JSON string of field values\n' +
               '  - propList: Field name definitions\n\n' +
               '⚠️ Important:When modifying field values, only change values in value, do not touch other content!\n' +
               '        Otherwise it will cause component display issues!\n\n' +
               'Example:\n' +
               '  biolims.mjs experiment-template NAE NA20260021 Activity_0uh63rf\n\n' +
               'Get sample detail ID for modifying products:\n' +
               '  1. Find component with type="detailTable" in stepDetails\n' +
               '  2. stepItemId = id field of that component\n' +
               '  3. Sample detail ID = id field of each sample in value JSON'
      };
    }
    return await apiCall('POST', '/experimentalcenter/experiment/selectOrAddExperimentFlowTemplate', {
      experimentFlowId: experimentId,
      flow: flowId,
      databaseTableSuffix: suffix
    });
  },

  async 'select-next-flow'(suffix, modelId, resultIds) {
    if (!suffix || !modelId || !resultIds) {
      return {
        error: 'Usage: biolims.mjs select-next-flow <suffix> <model_id> <result_ids>\n\n' +
               'Parameters:\n' +
               '  suffix: Experiment type suffix (HS/WK/FJ1129/SJCX)\n' +
               '  model_id: Experiment type ID (e.g. SYLX2024000001)\n' +
               '  result_ids: Sample ID list from result table (comma-separated)\n\n' +
               'Function:Query available next flows for result table samples\n\n' +
               'Example:\n' +
               '  biolims.mjs select-next-flow NAE SYLX2024000001 "id1,id2"'
      };
    }
    const ids = resultIds.split(',').map(id => id.trim());
    return await apiCall('POST', '/experimentalcenter/experiment/selectNextFlow', {
      bioTechLeaguePagingQuery: { page: 1, rows: 9999 },
      page: 1,
      rows: 9999,
      modelId: modelId,
      ids: ids,
      databaseTableSuffix: suffix
    });
  },

  // ============================================================================
  // Step Template Management
  // ============================================================================

  async 'delete-custom-table'(suffix, experimentId, templateItemId, rowIds) {
    if (!suffix || !experimentId || !templateItemId || !rowIds) {
      return { error: 'Usage: biolims.mjs delete-custom-table <suffix> <experiment_id> <template_item_id> <row_ids>' };
    }
    const ids = rowIds.split(',').map(id => id.trim());
    return await apiCall('POST', '/experimentalcenter/experiment/deleteCustomTableData', {
      id: experimentId,
      databaseTableSuffix: suffix,
      ids: ids,
      templateItemId: templateItemId
    });
  },

  // ============================================================================
  // Sample Pool Management (Internal API)
  // ============================================================================

  async 'add-sample-to-pool-controller'(type, samplesJson) {
    if (!type || !samplesJson) {
      return { error: 'Usage: biolims.mjs add-sample-to-pool-controller <type> \'<samples_json>\'' };
    }
    let samples = samplesJson;
    if (samplesJson.startsWith('@')) {
      const filePath = samplesJson.slice(1);
      if (!fs.existsSync(filePath)) return { error: `File not found: ${filePath}` };
      samples = fs.readFileSync(filePath, 'utf8');
    }
    return await apiCall('POST', `/experimentalcenter/experiment/addSampleToSamplePoolController?type=${type}`, JSON.parse(samples));
  },

  async 'add-sample-to-pool-fegin'(type, samplesJson) {
    if (!type || !samplesJson) {
      return { error: 'Usage: biolims.mjs add-sample-to-pool-fegin <type> \'<samples_json>\'' };
    }
    let samples = samplesJson;
    if (samplesJson.startsWith('@')) {
      const filePath = samplesJson.slice(1);
      if (!fs.existsSync(filePath)) return { error: `File not found: ${filePath}` };
      samples = fs.readFileSync(filePath, 'utf8');
    }
    return await apiCall('POST', `/experimentalcenter/experiment/addSampleToSamplePoolFegin?type=${type}`, JSON.parse(samples));
  },

  async 'add-sample-pool-by-apply'(jsonArg) {
    if (!jsonArg) {
      return { error: 'Usage: biolims.mjs add-sample-pool-by-apply \'<json>\'' };
    }
    let jsonBody = jsonArg;
    if (jsonArg.startsWith('@')) {
      const filePath = jsonArg.slice(1);
      if (!fs.existsSync(filePath)) return { error: `File not found: ${filePath}` };
      jsonBody = fs.readFileSync(filePath, 'utf8');
    }
    return await apiCall('POST', '/experimentalcenter/experiment/addExperimentSamplePoolBySampleApplyItems', JSON.parse(jsonBody));
  },

  async 'add-sample-pool-by-ticket'(jsonArg) {
    if (!jsonArg) {
      return { error: 'Usage: biolims.mjs add-sample-pool-by-ticket \'<json>\'' };
    }
    let jsonBody = jsonArg;
    if (jsonArg.startsWith('@')) {
      const filePath = jsonArg.slice(1);
      if (!fs.existsSync(filePath)) return { error: `File not found: ${filePath}` };
      jsonBody = fs.readFileSync(filePath, 'utf8');
    }
    return await apiCall('POST', '/experimentalcenter/experiment/addExperimentSamplePoolByTicket', JSON.parse(jsonBody));
  },

  // ============================================================================
  // Result Management
  // ============================================================================

  async 'generate-result'(suffix, experimentId, flowId, code) {
    if (!suffix || !experimentId || !flowId) {
      return {
        error: 'Usage: biolims.mjs generate-result <suffix> <experiment_id> <flow_id> [code]\n\n' +
               'Parameters:\n' +
               '  suffix: Experiment type suffix (HS/WK/FJ1129/SJCX)\n' +
               '  experiment_id: Experiment ID (e.g. NA20260021)\n' +
               '  flow_id: Flow node ID (e.g. Activity_0uh63rf)\n' +
               '  code: Experiment type code (optional, default NA/LP/E/Se）\n\n' +
               'Default code mapping:\n' +
               '  NAE → NA\n' +
               '  LP  → LP\n' +
               '  E   → E\n' +
               '  Se  → Se\n\n' +
               '⚠️ Note: This command checks if result table already has data. Existing results cannot be regenerated.\n\n' +
               'Example:\n' +
               '  biolims.mjs generate-result NAE NA20260021 Activity_0uh63rf'
      };
    }

    // Default code mapping (HS/WK/FJ1129/SJCX)
    const SUFFIX_TO_CODE = {
      'HS': 'HS',
      'WK': 'WK',
      'FJ1129': 'FI',
      'SJCX': 'SJCX',
      // Legacy mapping compatibility
      'NAE': 'NA',
      'LP': 'LP',
      'E': 'E',
      'Se': 'Se'
    };
    const actualCode = code || SUFFIX_TO_CODE[suffix] || suffix;

    // 1. First query template, check if result table has data
    const templateResult = await apiCall('POST', '/experimentalcenter/experiment/selectOrAddExperimentFlowTemplate', {
      experimentFlowId: experimentId,
      flow: flowId,
      databaseTableSuffix: suffix
    });

    if (templateResult.status !== 200) {
      return { error: 'Failed to query experiment template', detail: templateResult };
    }

    // 2. Find result table
    const stepDetails = templateResult.data?.stepDetails;
    if (!stepDetails || stepDetails.length === 0) {
      return { error: 'Experiment step details not found' };
    }

    const jsonDatas = stepDetails[0]?.jsonDatas;
    if (!jsonDatas) {
      return { error: 'Step data not found' };
    }

    const resultTable = jsonDatas.find(d => d.type === 'resultTable');
    if (!resultTable) {
      return { error: 'Result table component not found' };
    }

    // 3. Check if result table already has data
    let resultData = [];
    try {
      resultData = JSON.parse(resultTable.value || '[]');
    } catch (e) {
      resultData = [];
    }

    if (resultData.length > 0) {
      return {
        error: 'Result table already has data, cannot regenerate',
        existingResults: resultData.length,
        samples: resultData.map(r => ({
          sampleCode: r.sampleCode,
          originalSampleCode: r.originalSampleCode,
          productType: r.productType,
          result: r.result || '(to be filled)'
        }))
      };
    }

    // 4. Result table empty, can generate results
    // Note: addExperimentResult id is stepDetails[0].id, not resultTable id
    const stepDetailId = stepDetails[0]?.id;
    if (!stepDetailId) {
      return { error: 'Step detail ID not found (stepDetails[0].id)' };
    }

    return await apiCall('POST', '/experimentalcenter/experiment/addExperimentResult', {
      id: stepDetailId,
      databaseTableSuffix: suffix,
      code: actualCode
    });
  },

  async 'add-experiment-result'(jsonArg) {
    if (!jsonArg) {
      return {
        error: 'Usage: biolims.mjs add-experiment-result \'<json>\'\n\n' +
               'Required fields:\n' +
               '  - id: Step ID (stepDetails[0].id，not the id in jsonDatas!)\n' +
               '  - databaseTableSuffix: Experiment type suffix (NAE/LP/E/Se)\n' +
               '  - code: Experiment type code (NA/LP/E/Se)\n\n' +
               '⚠️ Important:\n' +
               '  1. id is stepDetails[0].id, not the resultTable component id\n' +
               '  2. Must verify resultTable has no data before generating\n' +
               '  3. Existing results cannot be regenerated\n\n' +
               'How to get stepId:\n' +
               '  1. Call experiment-template to query experiment\n' +
               '  2. Use stepDetails[0].id as id parameter\n\n' +
               'Example:\n' +
               '{\n' +
               '  "id": "6095b63224facabbd104b89d614f6dc0",\n' +
               '  "databaseTableSuffix": "NAE",\n' +
               '  "code": "NA"\n' +
               '}'
      };
    }
    let jsonBody = jsonArg;
    if (jsonArg.startsWith('@')) {
      const filePath = jsonArg.slice(1);
      if (!fs.existsSync(filePath)) return { error: `File not found: ${filePath}` };
      jsonBody = fs.readFileSync(filePath, 'utf8');
    }
    return await apiCall('POST', '/experimentalcenter/experiment/addExperimentResult', JSON.parse(jsonBody));
  },

  async 'select-result-by-sample'(suffix, sampleCode) {
    if (!suffix || !sampleCode) {
      return { error: 'Usage: biolims.mjs select-result-by-sample <suffix> <sample_code>' };
    }
    return await apiCall('POST', `/experimentalcenter/experiment/selectresultTableData?sampleCode=${sampleCode}`, {
      databaseTableSuffix: suffix
    });
  },

  async 'select-result-multi'(jsonArg) {
    if (!jsonArg) {
      return { error: 'Usage: biolims.mjs select-result-multi \'<json>\'' };
    }
    let jsonBody = jsonArg;
    if (jsonArg.startsWith('@')) {
      const filePath = jsonArg.slice(1);
      if (!fs.existsSync(filePath)) return { error: `File not found: ${filePath}` };
      jsonBody = fs.readFileSync(filePath, 'utf8');
    }
    return await apiCall('POST', '/experimentalcenter/experiment/selectresultTableDatas', JSON.parse(jsonBody));
  },

  async 'delete-experiment-data'(jsonArg) {
    if (!jsonArg) {
      return { error: 'Usage: biolims.mjs delete-experiment-data \'<json>\'' };
    }
    let jsonBody = jsonArg;
    if (jsonArg.startsWith('@')) {
      const filePath = jsonArg.slice(1);
      if (!fs.existsSync(filePath)) return { error: `File not found: ${filePath}` };
      jsonBody = fs.readFileSync(filePath, 'utf8');
    }
    return await apiCall('POST', '/experimentalcenter/experiment/delete', JSON.parse(jsonBody));
  },

  async 'return-result'(jsonArg) {
    if (!jsonArg) {
      return { error: 'Usage: biolims.mjs return-result \'<json>\'' };
    }
    let jsonBody = jsonArg;
    if (jsonArg.startsWith('@')) {
      const filePath = jsonArg.slice(1);
      if (!fs.existsSync(filePath)) return { error: `File not found: ${filePath}` };
      jsonBody = fs.readFileSync(filePath, 'utf8');
    }
    return await apiCall('POST', '/experimentalcenter/experiment/returnResult', JSON.parse(jsonBody));
  },

  // ============================================================================
  // Split Operations
  // ============================================================================

  async 'split-sample'(jsonArg) {
    if (!jsonArg) {
      return { error: 'Usage: biolims.mjs split-sample \'<json>\'' };
    }
    let jsonBody = jsonArg;
    if (jsonArg.startsWith('@')) {
      const filePath = jsonArg.slice(1);
      if (!fs.existsSync(filePath)) return { error: `File not found: ${filePath}` };
      jsonBody = fs.readFileSync(filePath, 'utf8');
    }
    return await apiCall('POST', '/experimentalcenter/experiment/split', JSON.parse(jsonBody));
  },

  async 'split-sub-product'(jsonArg) {
    if (!jsonArg) {
      return { error: 'Usage: biolims.mjs split-sub-product \'<json>\'' };
    }
    let jsonBody = jsonArg;
    if (jsonArg.startsWith('@')) {
      const filePath = jsonArg.slice(1);
      if (!fs.existsSync(filePath)) return { error: `File not found: ${filePath}` };
      jsonBody = fs.readFileSync(filePath, 'utf8');
    }
    return await apiCall('POST', '/experimentalcenter/experiment/splitSubProduct', JSON.parse(jsonBody));
  },

  async 'split-sub-product-by-number'(jsonArg) {
    if (!jsonArg) {
      return { error: 'Usage: biolims.mjs split-sub-product-by-number \'<json>\'' };
    }
    let jsonBody = jsonArg;
    if (jsonArg.startsWith('@')) {
      const filePath = jsonArg.slice(1);
      if (!fs.existsSync(filePath)) return { error: `File not found: ${filePath}` };
      jsonBody = fs.readFileSync(filePath, 'utf8');
    }
    return await apiCall('POST', '/experimentalcenter/experiment/splitSubProductByNumber', JSON.parse(jsonBody));
  },

  async 'split-locus'(jsonArg) {
    if (!jsonArg) {
      return { error: 'Usage: biolims.mjs split-locus \'<json>\'' };
    }
    let jsonBody = jsonArg;
    if (jsonArg.startsWith('@')) {
      const filePath = jsonArg.slice(1);
      if (!fs.existsSync(filePath)) return { error: `File not found: ${filePath}` };
      jsonBody = fs.readFileSync(filePath, 'utf8');
    }
    return await apiCall('POST', '/experimentalcenter/experiment/splitLocus', JSON.parse(jsonBody));
  },

  // ============================================================================
  // Product Management
  // ============================================================================

  async 'query-product-type'(suffix, experimentId) {
    if (!suffix || !experimentId) {
      return { error: 'Usage: biolims.mjs query-product-type <suffix> <experiment_id>' };
    }
    return await apiCall('POST', '/experimentalcenter/experiment/queryProductType', {
      databaseTableSuffix: suffix,
      id: experimentId
    });
  },

  async 'change-product'(jsonArg) {
    if (!jsonArg) {
      return {
        error: 'Usage: biolims.mjs change-product \'<json>\' or @<filepath>\n\n' +
               'Required fields:\n' +
               '  - id: stepItemId of sample detail table (component ID)\n' +
               '  - ids: Sample detail ID array\n' +
               '  - databaseTableSuffix: Experiment type suffix (NAE/LP/E/Se)\n' +
               '  - productList: Product list JSON string\n\n' +
               '⚠️ How to get stepItemId and sample detail ID:\n' +
               '  1. First call experiment-template to query components:\n' +
               '     biolims.mjs experiment-template NAE NA20260021 Activity_0uh63rf\n' +
               '  2. Find component with type="detailTable" in stepDetails\n' +
               '  3. stepItemId = id field of that component (e.g. "146631c388ef2d55027768a9d680bd8d")\n' +
               '  4. Sample detail ID = parse value JSON, get id field of each sample\n\n' +
               'Product list format:\n' +
               '  [{"productTypeId":"T251130001","productType":"cfDNA","productNum":3,"code":"CD"}]\n\n' +
               'Multiple products:\n' +
               '  [{"productTypeId":"T251130001","productType":"cfDNA","productNum":3,"code":"CD"},\n' +
               '   {"productTypeId":"T250724002","productType":"Whole Blood","productNum":1,"code":"WBC"}]\n\n' +
               'Common product types:\n' +
               '  - cfDNA: productTypeId=T251130001, code=CD\n' +
               '  - Whole Blood: productTypeId=T250724002, code=WBC\n' +
               '  - Genomic DNA: productTypeId=T241101003, code=GD\n\n' +
               'Complete operation example:\n' +
               '  # Step 1: Query experiment components to get IDs\n' +
               '  biolims.mjs experiment-template NAE NA20260021 Activity_0uh63rf\n' +
               '  # Get stepItemId and sample id from response\n\n' +
               '  # Step 2: Modify product type\n' +
               '  biolims.mjs change-product \'{\n' +
               '    "id": "146631c388ef2d55027768a9d680bd8d",\n' +
               '    "ids": ["ad644cbed18c20e2f5aaf4c5b07b0929"],\n' +
               '    "databaseTableSuffix": "NAE",\n' +
               '    "productList": "[{\\"productTypeId\\":\\"T251130001\\",\\"productType\\":\\"cfDNA\\",\\"productNum\\":2,\\"code\\":\\"CD\\"}]"\n' +
               '  }\''
      };
    }
    let jsonBody = jsonArg;
    if (jsonArg.startsWith('@')) {
      const filePath = jsonArg.slice(1);
      if (!fs.existsSync(filePath)) return { error: `File not found: ${filePath}` };
      jsonBody = fs.readFileSync(filePath, 'utf8');
    }
    return await apiCall('POST', '/experimentalcenter/experiment/changeProduct', JSON.parse(jsonBody));
  },

  async 'select-sub-product'(suffix, experimentId) {
    if (!suffix || !experimentId) {
      return { error: 'Usage: biolims.mjs select-sub-product <suffix> <experiment_id>' };
    }
    return await apiCall('POST', '/experimentalcenter/experiment/selectziProduct', {
      databaseTableSuffix: suffix,
      id: experimentId
    });
  },

  // ============================================================================
  // Reagent & Equipment Management
  // ============================================================================

  async 'delete-material-instrument'(jsonArg) {
    if (!jsonArg) {
      return { error: 'Usage: biolims.mjs delete-material-instrument \'<json>\'' };
    }
    let jsonBody = jsonArg;
    if (jsonArg.startsWith('@')) {
      const filePath = jsonArg.slice(1);
      if (!fs.existsSync(filePath)) return { error: `File not found: ${filePath}` };
      jsonBody = fs.readFileSync(filePath, 'utf8');
    }
    return await apiCall('POST', '/experimentalcenter/experiment/deleteMaterialAndInstrument', JSON.parse(jsonBody));
  },

  async 'mark-reagent-consumed'(jsonArg) {
    if (!jsonArg) {
      return { error: 'Usage: biolims.mjs mark-reagent-consumed \'<json>\'' };
    }
    let jsonBody = jsonArg;
    if (jsonArg.startsWith('@')) {
      const filePath = jsonArg.slice(1);
      if (!fs.existsSync(filePath)) return { error: `File not found: ${filePath}` };
      jsonBody = fs.readFileSync(filePath, 'utf8');
    }
    return await apiCall('POST', '/experimentalcenter/experiment/markReagentLotConsumed', JSON.parse(jsonBody));
  },

  // ============================================================================
  // Flow Advancement & Tracing
  // ============================================================================

  async 'select-experiment-process'(suffix, productId) {
    if (!suffix || !productId) {
      return { error: 'Usage: biolims.mjs select-experiment-process <suffix> <product_id>' };
    }
    return await apiCall('POST', '/experimentalcenter/experiment/selectExperimentProcess', {
      databaseTableSuffix: suffix,
      productId: productId
    });
  },

  // ============================================================================
  // Sample Pool Advanced Operations
  // ============================================================================

  async 'select-pool-by-table-id'(tableName, poolId) {
    if (!tableName || !poolId) {
      return { error: 'Usage: biolims.mjs select-pool-by-table-id <table_name> <pool_id>' };
    }
    return await apiCall('POST', `/experimentalcenter/experiment/selectAllByPoolTableId?tableName=${tableName}&id=${poolId}`, {});
  },

  async 'delete-pool-by-id'(platformId, poolId) {
    if (!platformId || !poolId) {
      return { error: 'Usage: biolims.mjs delete-pool-by-id <platform_id> <pool_id>' };
    }
    return await apiCall('POST', `/experimentalcenter/experiment/delExperimentPoolById?platformId=${platformId}&id=${poolId}`, {});
  },

  async 'select-pool-by-codes'(tableName, sampleCodes) {
    if (!tableName || !sampleCodes) {
      return { error: 'Usage: biolims.mjs select-pool-by-codes <table_name> <sample_codes>' };
    }
    return await apiCall('POST', `/experimentalcenter/experiment/selExperimentPoolBySampleCodes?tableName=${tableName}`,
      sampleCodes.split(',').map(s => s.trim())
    );
  },

  async 'delete-pool-by-codes'(tableName, sampleCodes) {
    if (!tableName || !sampleCodes) {
      return { error: 'Usage: biolims.mjs delete-pool-by-codes <table_name> <sample_codes>' };
    }
    return await apiCall('POST', `/experimentalcenter/experiment/delExperimentPoolBySampleCodes?tableName=${tableName}`,
      sampleCodes.split(',').map(s => s.trim())
    );
  },

  async 'delete-pool-or-next'(tableName, experimentId) {
    if (!tableName || !experimentId) {
      return { error: 'Usage: biolims.mjs delete-pool-or-next <table_name> <experiment_id>' };
    }
    return await apiCall('POST', `/experimentalcenter/experiment/delExperimentPoolOrnextById?tableName=${tableName}&id=${experimentId}`, {});
  },

  // ============================================================================
  // QC Management
  // ============================================================================

  async 'select-qc-list'(page = '1', rows = '10') {
    return await apiCall('POST', '/experimentalcenter/experiment/selectPopupsQualityControl', {
      page: parseInt(page),
      rows: parseInt(rows),
      sort: {},
      query: []
    });
  },

  async 'add-qc'(jsonArg) {
    if (!jsonArg) {
      return { error: 'Usage: biolims.mjs add-qc \'<json>\'' };
    }
    let jsonBody = jsonArg;
    if (jsonArg.startsWith('@')) {
      const filePath = jsonArg.slice(1);
      if (!fs.existsSync(filePath)) return { error: `File not found: ${filePath}` };
      jsonBody = fs.readFileSync(filePath, 'utf8');
    }
    return await apiCall('POST', '/experimentalcenter/experiment/addQualityControl', JSON.parse(jsonBody));
  },

  async 'submit-qc'(jsonArg) {
    if (!jsonArg) {
      return { error: 'Usage: biolims.mjs submit-qc \'<json>\'' };
    }
    let jsonBody = jsonArg;
    if (jsonArg.startsWith('@')) {
      const filePath = jsonArg.slice(1);
      if (!fs.existsSync(filePath)) return { error: `File not found: ${filePath}` };
      jsonBody = fs.readFileSync(filePath, 'utf8');
    }
    return await apiCall('POST', '/experimentalcenter/experiment/submitQualityControl', JSON.parse(jsonBody));
  },

  async 'select-qc-result'(suffix, sampleCode) {
    if (!suffix || !sampleCode) {
      return { error: 'Usage: biolims.mjs select-qc-result <suffix> <sample_code>' };
    }
    return await apiCall('POST', `/experimentalcenter/experiment/selectQualityResultTableData?sampleCode=${sampleCode}`, {
      databaseTableSuffix: suffix
    });
  },

  async 'select-qc-results'(jsonArg) {
    if (!jsonArg) {
      return { error: 'Usage: biolims.mjs select-qc-results \'<json>\'' };
    }
    let jsonBody = jsonArg;
    if (jsonArg.startsWith('@')) {
      const filePath = jsonArg.slice(1);
      if (!fs.existsSync(filePath)) return { error: `File not found: ${filePath}` };
      jsonBody = fs.readFileSync(filePath, 'utf8');
    }
    return await apiCall('POST', '/experimentalcenter/experiment/selectQualityResultTableDatas', JSON.parse(jsonBody));
  },

  async 'select-qc-template-item'(suffix, sampleId) {
    if (!suffix || !sampleId) {
      return { error: 'Usage: biolims.mjs select-qc-template-item <suffix> <sample_id>' };
    }
    return await apiCall('POST', '/experimentalcenter/experiment/selectQualitycenterExperimentTemplateItemBySampleId', {
      databaseTableSuffix: suffix,
      id: sampleId
    });
  },

  async 'save-qc-template-item'(suffix, sampleCode, itemsJson) {
    if (!suffix || !sampleCode || !itemsJson) {
      return { error: 'Usage: biolims.mjs save-qc-template-item <suffix> <sample_code> \'<items_json>\'' };
    }
    let items = itemsJson;
    if (itemsJson.startsWith('@')) {
      const filePath = itemsJson.slice(1);
      if (!fs.existsSync(filePath)) return { error: `File not found: ${filePath}` };
      items = fs.readFileSync(filePath, 'utf8');
    }
    return await apiCall('POST', '/experimentalcenter/experiment/saveQualitycenterExperimentTemplateItemBySampleId', {
      databaseTableSuffix: suffix,
      sampleCode: sampleCode,
      qualitycenterExperimentTemplateItems: JSON.parse(items)
    });
  },

  // ============================================================================
  // Popup Queries
  // ============================================================================

  async 'select-personnel-group'(page = '1', rows = '10') {
    return await apiCall('POST', '/experimentalcenter/experiment/selectPopupsPersonnelGroup', {
      page: parseInt(page),
      rows: parseInt(rows),
      sort: {},
      query: []
    });
  },

  async 'select-unit'(page = '1', rows = '999') {
    return await apiCall('POST', '/experimentalcenter/experiment/selectUnit', {
      page: parseInt(page),
      rows: parseInt(rows),
      sort: {},
      query: []
    });
  },

  async 'select-dictionary'(type, page = '1', rows = '10') {
    if (!type) {
      return { error: 'Usage: biolims.mjs select-dictionary <type> [page] [rows]' };
    }
    return await apiCall('POST', `/experimentalcenter/experiment/selectDictionary?type=${type}`, {
      page: parseInt(page),
      rows: parseInt(rows),
      sort: {},
      query: []
    });
  },

  async 'index-query'(page = '1', rows = '10') {
    return await apiCall('POST', '/experimentalcenter/experiment/indexQuery', {
      page: parseInt(page),
      rows: parseInt(rows),
      sort: {},
      query: []
    });
  },

  // ============================================================================
  // Batch Operations
  // ============================================================================

  async 'batch-warehousing'(suffix, experimentId, itemIds) {
    if (!suffix || !experimentId || !itemIds) {
      return { error: 'Usage: biolims.mjs batch-warehousing <suffix> <experiment_id> <item_ids>' };
    }
    const ids = itemIds.split(',').map(id => id.trim());
    return await apiCall('POST', '/experimentalcenter/experiment/batchWarehousing', {
      databaseTableSuffix: suffix,
      id: experimentId,
      ids: ids
    });
  },

  async 'batch-export'(suffix, experimentId, itemIds) {
    if (!suffix || !experimentId || !itemIds) {
      return { error: 'Usage: biolims.mjs batch-export <suffix> <experiment_id> <item_ids>' };
    }
    const ids = itemIds.split(',').map(id => id.trim());
    return await apiCall('POST', '/experimentalcenter/experiment/batchExport', {
      databaseTableSuffix: suffix,
      id: experimentId,
      ids: ids
    });
  },

  async 'batch-write'(filePath, jsonData) {
    if (!filePath || !jsonData) {
      return { error: 'Usage: biolims.mjs batch-write <file_path> \'<json_data>\'\n\nNote: This command requires multipart/form-data, use frontend' };
    }
    return { error: 'This command requires file upload, use frontend or dedicated upload tool' };
  },

  async 'save-tapestation-data'(suffix, experimentIds, samplesJson) {
    if (!suffix || !experimentIds || !samplesJson) {
      return { error: 'Usage: biolims.mjs save-tapestation-data <suffix> <experiment_ids> \'<samples_json>\'' };
    }
    let samples = samplesJson;
    if (samplesJson.startsWith('@')) {
      const filePath = samplesJson.slice(1);
      if (!fs.existsSync(filePath)) return { error: `File not found: ${filePath}` };
      samples = fs.readFileSync(filePath, 'utf8');
    }
    const ids = experimentIds.split(',').map(id => id.trim());
    return await apiCall('POST', `/experimentalcenter/experiment/saveTapeStationData?databaseTableSuffix=${suffix}&ids=${ids.join(',')}`, JSON.parse(samples));
  },

  // ============================================================================
  // Barcode Scanning
  // ============================================================================

  async 'experiment-scan'(jsonArg) {
    if (!jsonArg) {
      return { error: 'Usage: biolims.mjs experiment-scan \'<json>\'' };
    }
    let jsonBody = jsonArg;
    if (jsonArg.startsWith('@')) {
      const filePath = jsonArg.slice(1);
      if (!fs.existsSync(filePath)) return { error: `File not found: ${filePath}` };
      jsonBody = fs.readFileSync(filePath, 'utf8');
    }
    return await apiCall('POST', '/experimentalcenter/experiment/ExperimentDetailScan', JSON.parse(jsonBody));
  },

  async 'experiment-scan2'(jsonArg) {
    if (!jsonArg) {
      return { error: 'Usage: biolims.mjs experiment-scan2 \'<json>\'' };
    }
    let jsonBody = jsonArg;
    if (jsonArg.startsWith('@')) {
      const filePath = jsonArg.slice(1);
      if (!fs.existsSync(filePath)) return { error: `File not found: ${filePath}` };
      jsonBody = fs.readFileSync(filePath, 'utf8');
    }
    return await apiCall('POST', '/experimentalcenter/experiment/ExperimentDetailScan2', JSON.parse(jsonBody));
  },

  // ============================================================================
  // Auto-save & Records
  // ============================================================================

  async 'auto-save-experiment'(jsonArg) {
    if (!jsonArg) {
      return { error: 'Usage: biolims.mjs auto-save-experiment \'<json>\'' };
    }
    let jsonBody = jsonArg;
    if (jsonArg.startsWith('@')) {
      const filePath = jsonArg.slice(1);
      if (!fs.existsSync(filePath)) return { error: `File not found: ${filePath}` };
      jsonBody = fs.readFileSync(filePath, 'utf8');
    }
    return await apiCall('POST', '/experimentalcenter/experiment/autoSave', JSON.parse(jsonBody));
  },

  async 'generate-experiment-record'(jsonArg) {
    if (!jsonArg) {
      return { error: 'Usage: biolims.mjs generate-experiment-record \'<json>\'' };
    }
    let jsonBody = jsonArg;
    if (jsonArg.startsWith('@')) {
      const filePath = jsonArg.slice(1);
      if (!fs.existsSync(filePath)) return { error: `File not found: ${filePath}` };
      jsonBody = fs.readFileSync(filePath, 'utf8');
    }
    return await apiCall('POST', '/experimentalcenter/experiment/generateExperimentalRecord', JSON.parse(jsonBody));
  },

  async 'select-quality-records'(batch) {
    if (!batch) {
      return { error: 'Usage: biolims.mjs select-quality-records <batch>' };
    }
    return await apiCall('POST', `/experimentalcenter/experiment/selectExperimentQualityRecords?batch=${batch}`, {});
  },

  // ============================================================================
  // Template Operations
  // ============================================================================

  async 'handle-experiment-sheet'(experimentId) {
    if (!experimentId) {
      return { error: 'Usage: biolims.mjs handle-experiment-sheet <experiment_id>' };
    }
    return await apiCall('POST', `/experimentalcenter/experiment/handleexperimentsheet?id=${experimentId}`, {});
  },

  async 'editing-template'(jsonArg) {
    if (!jsonArg) {
      return { error: 'Usage: biolims.mjs editing-template \'<json>\'' };
    }
    let jsonBody = jsonArg;
    if (jsonArg.startsWith('@')) {
      const filePath = jsonArg.slice(1);
      if (!fs.existsSync(filePath)) return { error: `File not found: ${filePath}` };
      jsonBody = fs.readFileSync(filePath, 'utf8');
    }
    return await apiCall('POST', '/experimentalcenter/experiment/editingTemplate', JSON.parse(jsonBody));
  },

  async 'import-template-button'(jsonArg) {
    if (!jsonArg) {
      return { error: 'Usage: biolims.mjs import-template-button \'<json>\'' };
    }
    let jsonBody = jsonArg;
    if (jsonArg.startsWith('@')) {
      const filePath = jsonArg.slice(1);
      if (!fs.existsSync(filePath)) return { error: `File not found: ${filePath}` };
      jsonBody = fs.readFileSync(filePath, 'utf8');
    }
    return await apiCall('POST', '/experimentalcenter/experiment/importTemplateButton', JSON.parse(jsonBody));
  },

  async 'import-template-execute'(jsonArg) {
    if (!jsonArg) {
      return { error: 'Usage: biolims.mjs import-template-execute \'<json>\'' };
    }
    let jsonBody = jsonArg;
    if (jsonArg.startsWith('@')) {
      const filePath = jsonArg.slice(1);
      if (!fs.existsSync(filePath)) return { error: `File not found: ${filePath}` };
      jsonBody = fs.readFileSync(filePath, 'utf8');
    }
    return await apiCall('POST', '/experimentalcenter/experiment/importTemplateButton/importTemplate', JSON.parse(jsonBody));
  },

  // ============================================================================
  // Well Plate Operations
  // ============================================================================

  async 'delete-hole'(jsonArg) {
    if (!jsonArg) {
      return { error: 'Usage: biolims.mjs delete-hole \'<json>\'' };
    }
    let jsonBody = jsonArg;
    if (jsonArg.startsWith('@')) {
      const filePath = jsonArg.slice(1);
      if (!fs.existsSync(filePath)) return { error: `File not found: ${filePath}` };
      jsonBody = fs.readFileSync(filePath, 'utf8');
    }
    return await apiCall('POST', '/experimentalcenter/experiment/deleteHole', JSON.parse(jsonBody));
  },

  // ============================================================================
  // Other Operations
  // ============================================================================

  async 'experiment-order-change'(jsonArg) {
    if (!jsonArg) {
      return { error: 'Usage: biolims.mjs experiment-order-change \'<json>\'' };
    }
    let jsonBody = jsonArg;
    if (jsonArg.startsWith('@')) {
      const filePath = jsonArg.slice(1);
      if (!fs.existsSync(filePath)) return { error: `File not found: ${filePath}` };
      jsonBody = fs.readFileSync(filePath, 'utf8');
    }
    return await apiCall('POST', '/experimentalcenter/experiment/experimentOrderChange', JSON.parse(jsonBody));
  },

  async 'get-experiments-by-sample'(jsonArg) {
    if (!jsonArg) {
      return { error: 'Usage: biolims.mjs get-experiments-by-sample \'<json>\'' };
    }
    let jsonBody = jsonArg;
    if (jsonArg.startsWith('@')) {
      const filePath = jsonArg.slice(1);
      if (!fs.existsSync(filePath)) return { error: `File not found: ${filePath}` };
      jsonBody = fs.readFileSync(filePath, 'utf8');
    }
    return await apiCall('POST', '/experimentalcenter/experiment/getExperimentsBySampleId', JSON.parse(jsonBody));
  },

  async 'get-experiment-result-by-id'(jsonArg) {
    if (!jsonArg) {
      return { error: 'Usage: biolims.mjs get-experiment-result-by-id \'<json>\'' };
    }
    let jsonBody = jsonArg;
    if (jsonArg.startsWith('@')) {
      const filePath = jsonArg.slice(1);
      if (!fs.existsSync(filePath)) return { error: `File not found: ${filePath}` };
      jsonBody = fs.readFileSync(filePath, 'utf8');
    }
    return await apiCall('POST', '/experimentalcenter/experiment/getExperimentResultById', JSON.parse(jsonBody));
  },

  // ============================================================================
  // Complete Experiment Step (updateExperimentFlowNext)
  // ============================================================================

  async 'complete-experiment'(suffix, experimentId, flowId) {
    if (!suffix || !experimentId) {
      return {
        error: 'Usage:biolims.mjs complete-experiment <suffix> <experiment_id> [flow_id]\n\n' +
               'Parameters:\n' +
               '  suffix: Experiment type suffix (HS/WK/FJ1129/SJCX)\n' +
               '  experiment_id: Experiment ID (e.g. HS20260002)\n' +
               '  flow_id: Flow node ID (optional, auto-queried from experiment by default)\n\n' +
               'Function:\n' +
               '  Auto-get experiment template, extract step ID and template ID, then complete experiment.\n' +
               '  No need to manually build JSON file.\n\n' +
               '⚠️ Prerequisites:\n' +
               '  1. Experiment must have samples added\n' +
               '  2. Result table must be generated (call generate-result)\n' +
               '  3. Result table required fields filled (use update-result):\n' +
               '     - result, resultId\n' +
               '     - nextFlow, nextFlowId, databaseTableSuffixTwo\n\n' +
               'Example:\n' +
               '  biolims.mjs complete-experiment HS HS20260002\n' +
               '  biolims.mjs complete-experiment WK WK20260015 Activity_0637pjm'
      };
    }

    // If flowId not provided, query dynamically
    let actualFlowId = flowId;
    if (!actualFlowId) {
      actualFlowId = await getFlowIdFromExperiment(suffix, experimentId);
      if (!actualFlowId) {
        return { error: `Cannot auto-get flow node ID, please specify flow_id manually. Experiment: ${experimentId}` };
      }
    }

    // 1. Get experiment template data
    const templateResp = await apiCall('POST', '/experimentalcenter/experiment/selectOrAddExperimentFlowTemplate', {
      experimentFlowId: experimentId,
      flow: actualFlowId,
      databaseTableSuffix: suffix
    });

    if (templateResp.status !== 200) {
      return { error: `Failed to get experiment template: ${templateResp.msg || JSON.stringify(templateResp)}` };
    }

    const templateData = templateResp.data;
    if (!templateData || !templateData.stepDetails || templateData.stepDetails.length === 0) {
      return { error: 'Experiment template data is empty or has incorrect format' };
    }

    // 2. Extract required IDs
    const templateId = templateData.id;  // Template ID
    const stepId = templateData.stepDetails[0].id;  // Step detail ID

    if (!templateId || !stepId) {
      return { error: `Cannot get required IDs: templateId=${templateId}, stepId=${stepId}` };
    }

    // 3. Check if result table has required fields
    let resultTableOk = false;
    let missingFields = [];
    
    for (const step of templateData.stepDetails) {
      if (!step.jsonDatas) continue;
      for (const component of step.jsonDatas) {
        if (component.type === 'resultTable' && component.value) {
          try {
            const resultItems = JSON.parse(component.value);
            if (resultItems.length === 0) {
              return { error: 'Result table is empty, call generate-result first' };
            }
            
            // Check required fields of first sample
            const sample = resultItems[0];
            const requiredFields = ['result', 'nextFlow', 'nextFlowId', 'databaseTableSuffixTwo'];
            for (const field of requiredFields) {
              if (!sample[field]) {
                missingFields.push(field);
              }
            }
            
            if (missingFields.length === 0) {
              resultTableOk = true;
            }
          } catch (e) {
            return { error: `Result table parse failed: ${e.message}` };
          }
        }
      }
    }

    if (missingFields.length > 0) {
      return { 
        error: `Result table missing required fields: ${missingFields.join(', ')}\n\n` +
               'Please use update-result to set these fields first, e.g.:\n' +
               `biolims.mjs update-result ${suffix} ${experimentId} ${actualFlowId} '{"id":"sample_id","result":"Qualified","resultId":"1","nextFlow":"Library Preparation","nextFlowId":"SYLX2024000007","databaseTableSuffixTwo":"LP"}'`
      };
    }

    // 4. Build completion request
    const completePayload = {
      id: stepId,
      databaseTableSuffix: suffix,
      experimentId: templateId,
      stepState: '1',
      mainId: experimentId
    };

    // 5. Call completion API
    const completeResp = await apiCall('POST', '/experimentalcenter/experiment/updateExperimentFlowNext', completePayload);

    if (completeResp.status === 200) {
      return {
        status: 200,
        msg: 'OK',
        data: {
          experimentId: experimentId,
          templateId: templateId,
          stepId: stepId,
          message: `Experiment ${experimentId} completed`
        }
      };
    } else {
      return completeResp;
    }
  },

  async 'complete-step'(jsonArg) {
    if (!jsonArg) {
      return {
        error: 'Usage: biolims.mjs complete-step \'<json>\' or @<filepath>\n\n' +
               'Required fields:\n' +
               '  - id: stepDetails[0].id (Step detail ID)\n' +
               '  - databaseTableSuffix: Experiment type suffix (NAE/LP/E/Se)\n' +
               '  - experimentId: Template ID (experiment-template returned data.id)\n' +
               '  - stepState: Step status (1=Complete)\n' +
               '  - mainId: Experiment ID (e.g. NA20260021)\n\n' +
               'Example:\n' +
               '{\n' +
               '  "id": "6095b63224facabbd104b89d614f6dc0",\n' +
               '  "databaseTableSuffix": "NAE",\n' +
               '  "experimentId": "c1e1f4afb9938472f5ffb9ef5b575cdd",\n' +
               '  "stepState": "1",\n' +
               '  "mainId": "NA20260021"\n' +
               '}'
      };
    }
    let jsonBody = jsonArg;
    if (jsonArg.startsWith('@')) {
      const filePath = jsonArg.slice(1);
      if (!fs.existsSync(filePath)) return { error: `File not found: ${filePath}` };
      jsonBody = fs.readFileSync(filePath, 'utf8');
    }
    return await apiCall('POST', '/experimentalcenter/experiment/updateExperimentFlowNext', JSON.parse(jsonBody));
  },

  // ============================================================================
  // Sequencing QC (Sequencing QC) - 13 APIs
  // ============================================================================

  async 'seq-qc-list'(page = '1', rows = '10') {
    return await apiCall('POST', '/experimentalcenter/sequencingQc/findAllSequencingQcList', {
      bioTechLeaguePagingQuery: {
        page: parseInt(page),
        rows: parseInt(rows),
        sort: {},
        query: [],
        pagingSearchOne: {},
        fuzzySearch: {}
      }
    });
  },

  async 'seq-qc-detail'(qcId) {
    if (!qcId) {
      return { error: 'Usage: biolims.mjs seq-qc-detail <qc_id>\n\nParameters:\n  qc_id: QC order ID' };
    }
    return await apiCall('POST', '/experimentalcenter/sequencingQc/findSequencingQcOne', {
      id: qcId
    });
  },

  async 'save-seq-qc'(jsonArg) {
    if (!jsonArg) {
      return {
        error: 'Usage: biolims.mjs save-seq-qc \'<json>\' or @<filepath>\n\n' +
               'Required fields:\n' +
               '  sequencingQc: QC main table object (must include id)\n' +
               '    - id: QC order ID (required, cannot be empty)\n' +
               '    - description: QC description\n' +
               '    - refNo: Reference number\n' +
               '    - fcNo: FC number\n' +
               '    - machineNo: Machine number\n' +
               '    - flowcellId: Flowcell ID\n' +
               '    - status: Status\n' +
               '  sequencingQcItem: QC detail list (optional)\n\n' +
               'Example:\n' +
               '{\n' +
               '  "sequencingQc": {\n' +
               '    "id": "uuid-1234",\n' +
               '    "description": "First batch sequencing QC",\n' +
               '    "refNo": "REF001",\n' +
               '    "flowcellId": "FC0115001"\n' +
               '  },\n' +
               '  "sequencingQcItem": [\n' +
               '    {\n' +
               '      "id": "item-1",\n' +
               '      "sampleCode": "SAMPLE001",\n' +
               '      "method": "qualified"\n' +
               '    }\n' +
               '  ]\n' +
               '}'
      };
    }
    let jsonBody = jsonArg;
    if (jsonArg.startsWith('@')) {
      const filePath = jsonArg.slice(1);
      if (!fs.existsSync(filePath)) {
        return { error: `File not found: ${filePath}` };
      }
      jsonBody = fs.readFileSync(filePath, 'utf8');
    }
    return await apiCall('POST', '/experimentalcenter/sequencingQc/saveSequencingQc', JSON.parse(jsonBody));
  },

  async 'seq-qc-custom-fields'(tableType = 'itemTable') {
    // Get sequencing QC custom field config
    // tableType: mainTable or itemTable
    // Sequencing QCmodule number: 257
    // - 257-mainTable: main table custom fields
    // - 257-itemTable: item table custom fields
    const flag = `257-${tableType}`;
    return await apiCall('GET', `/system/custom/selAllFields?flag=${flag}`, null);
  },

  async 'get-seq-qc-custom-fields'(flag = '257-itemTable') {
    // Get sequencing QC custom field config
    // flag: 257-mainTable or 257-itemTable
    return await apiCall('GET', `/system/custom/selAllFields?flag=${flag}`, null);
  },

  async 'seq-qc-item-list'(qcId, page = '1', rows = '10') {
    if (!qcId) {
      return { error: 'Usage: biolims.mjs seq-qc-item-list <qc_id> [page] [rows]\n\nParameters:\n  qc_id: QC order ID' };
    }
    return await apiCall('POST', '/experimentalcenter/sequencingQc/findAllSequencingQcDetailList', {
      id: qcId,
      bioTechLeaguePagingQuery: {
        page: parseInt(page),
        rows: parseInt(rows),
        sort: {},
        query: []
      }
    });
  },

  async 'delete-seq-qc-item'(itemIds) {
    if (!itemIds) {
      return {
        error: 'Usage: biolims.mjs delete-seq-qc-item <item_ids>\n\n' +
               'Parameters:\n' +
               '  item_ids: QC detail ID list (comma-separated)\n\n' +
               'Example:biolims.mjs delete-seq-qc-item "item-uuid-1,item-uuid-2"'
      };
    }
    const ids = itemIds.split(',').map(id => id.trim());
    return await apiCall('POST', '/experimentalcenter/sequencingQc/deleteSequencingQcDetail', {
      ids: ids
    });
  },

  async 'transact-seq-qc'(qcId) {
    if (!qcId) {
      return {
        error: 'Usage: biolims.mjs transact-seq-qc <qc_id>\n\n' +
               'Parameters:\n' +
               '  qc_id: QC order ID\n\n' +
               'Function:Process QC order (complete workflow), change status from In Progress to Completed'
      };
    }
    return await apiCall('POST', '/experimentalcenter/sequencingQc/transactChargeSequencingQc', {
      id: qcId
    });
  },

  async 'export-seq-qc'(qcId) {
    if (!qcId) {
      return {
        error: 'Usage: biolims.mjs export-seq-qc <qc_id>\n\n' +
               'Parameters:\n' +
               '  qc_id: QC order ID\n\n' +
               'Function:Export QC data to Excel file'
      };
    }
    return await apiCall('POST', '/experimentalcenter/sequencingQc/exportSequencingQc', {
      id: qcId
    });
  },

  async 'import-seq-qc'(filePath, qcId) {
    if (!filePath || !qcId) {
      return {
        error: 'Usage: biolims.mjs import-seq-qc <file_path> <qc_id>\n\n' +
               'Parameters:\n' +
               '  file_path: Excel file path\n' +
               '  qc_id: QC order ID\n\n' +
               'Note:This command requires file upload, use frontend interface'
      };
    }
    return {
      error: 'Excel import requires multipart/form-data, use frontend interface'
    };
  },

  async 'recall-seq-qc'(qcId) {
    if (!qcId) {
      return {
        error: 'Usage: biolims.mjs recall-seq-qc <qc_id>\n\n' +
               'Parameters:\n' +
               '  qc_id: QC order ID\n\n' +
               'Function:Recall QC order, change status from Completed back to In Progress'
      };
    }
    return await apiCall('POST', '/experimentalcenter/sequencingQc/updateSequencingQcById', {
      id: qcId
    });
  },

  
  async 'seq-qc-complete'(qcId) {
    // Complete QC (workflow)
    if (!qcId) {
      return { error: 'Usage:biolims.mjs seq-qc-complete <qc_id>' };
    }
    
    // Step 1: Query workflow action list
    const actionsResult = await apiCall('POST', '/system/activiti/HandleTasks/selectHandleTasks', {
      appTypeTableId: 'SequencingQc'
    });
    
    if (actionsResult.status !== 200 || !actionsResult.data || !actionsResult.data.length) {
      return { error: 'Failed to get handle actions', details: actionsResult };
    }
    
    // Find "Finish" or "Complete" action
    const finishAction = actionsResult.data.find(a => a.actionName === 'Finish' || a.actionName === 'Complete');
    if (!finishAction) {
      return { error: 'Finish action not found', availableActions: actionsResult.data };
    }
    
    // Step 2: Call HandleTasks to complete QC
    const completeResult = await apiCall('POST', '/system/activiti/HandleTasks/HandleTasks', {
      appTypeTableId: finishAction.id,
      contentid: qcId,
      formName: 'Sequencing QC',
      note: ''
    });
    
    return completeResult;
  },

async 'seq-qc-edit-template'(jsonArg) {
    if (!jsonArg) {
      return {
        error: 'Usage: biolims.mjs seq-qc-edit-template \'<json>\'\n\n' +
               'Function:Edit QC template online'
      };
    }
    let jsonBody = jsonArg;
    if (jsonArg.startsWith('@')) {
      const filePath = jsonArg.slice(1);
      if (!fs.existsSync(filePath)) {
        return { error: `File not found: ${filePath}` };
      }
      jsonBody = fs.readFileSync(filePath, 'utf8');
    }
    return await apiCall('POST', '/experimentalcenter/sequencingQc/editingTemplate', JSON.parse(jsonBody));
  },

  async 'seq-qc-import-template-btn'(jsonArg) {
    if (!jsonArg) {
      return {
        error: 'Usage: biolims.mjs seq-qc-import-template-btn \'<json>\'\n\n' +
               'Function:Get template import button action'
      };
    }
    let jsonBody = jsonArg;
    if (jsonArg.startsWith('@')) {
      const filePath = jsonArg.slice(1);
      if (!fs.existsSync(filePath)) {
        return { error: `File not found: ${filePath}` };
      }
      jsonBody = fs.readFileSync(filePath, 'utf8');
    }
    return await apiCall('POST', '/experimentalcenter/sequencingQc/importTemplateButton', JSON.parse(jsonBody));
  },

  async 'seq-qc-import-template'(jsonArg) {
    if (!jsonArg) {
      return {
        error: 'Usage: biolims.mjs seq-qc-import-template \'<json>\'\n\n' +
               'Function:Import edited template data'
      };
    }
    let jsonBody = jsonArg;
    if (jsonArg.startsWith('@')) {
      const filePath = jsonArg.slice(1);
      if (!fs.existsSync(filePath)) {
        return { error: `File not found: ${filePath}` };
      }
      jsonBody = fs.readFileSync(filePath, 'utf8');
    }
    return await apiCall('POST', '/experimentalcenter/sequencingQc/importTemplateButton/importTemplate', JSON.parse(jsonBody));
  },

  async 'update-seq-qc-by-sample'(flowcellId, samplesJson) {
    if (!flowcellId || !samplesJson) {
      return {
        error: 'Usage: biolims.mjs update-seq-qc-by-sample <flowcell_id> \'<samples_json>\'\n\n' +
               'Parameters:\n' +
               '  flowcell_id: Flowcell ID\n' +
               '  samples_json: Sample data JSON array\n\n' +
               'Function:External API update QC items (requires JWT auth)\n\n' +
               'Example:\n' +
               '[\n' +
               '  {\n' +
               '    "sample_id": "SAMPLE001",\n' +
               '    "method": "qualified",\n' +
               '    "lod_score": "15",\n' +
               '    "custom_field1": "value1"\n' +
               '  }\n' +
               ']'
      };
    }
    let samples = samplesJson;
    if (samplesJson.startsWith('@')) {
      const filePath = samplesJson.slice(1);
      if (!fs.existsSync(filePath)) {
        return { error: `File not found: ${filePath}` };
      }
      samples = fs.readFileSync(filePath, 'utf8');
    }
    return await apiCall('POST', `/experimentalcenter/sequencingQc/updateSequencingQcItemBySampleId?flowcell_id=${flowcellId}`, JSON.parse(samples));
  },

  // ==================== Report Distribution Module Commands ====================

  async 'report-pending-list'(page = '1', rows = '50') {
    // Query pending report list(state='1' means pending report)
    // Usage:biolims.mjs report-pending-list [page] [rows]
    // Example:biolims.mjs report-pending-list 1 50
    return await apiCall('POST', '/experimentalcenter/inspectionreport/report/selectReportPending', {
      bioTechLeaguePagingQuery: {
        page: parseInt(page),
        rows: parseInt(rows),
        sort: { sortFiled: 'create_date', sortOrder: '-1' },
        pagingSearchOne: {},
        query: []
      },
      sort: { sortFiled: 'create_date', sortOrder: '-1' },
      pagingSearchOne: {},
      query: [],
      tableData: [],
      page: parseInt(page),
      rows: parseInt(rows),
      totalRecords: '0',
      state: '1'
    });
  },

  async 'report-writer-list'(page = '1', rows = '50') {
    // Query assignable writers
    return await apiCall('POST', '/experimentalcenter/inspectionreport/report/selectPersonnelGroupUser', {
      bioTechLeaguePagingQuery: {
        page: parseInt(page),
        rows: parseInt(rows),
        sort: {},
        query: []
      },
      page: parseInt(page),
      rows: parseInt(rows)
    });
  },

  async 'report-assign-writer'(jsonArg) {
    // Assign writer
    if (!jsonArg) {
      return { error: 'Usage:biolims.mjs report-assign-writer \'<json>\' or @<filepath>' };
    }
    let jsonBody = jsonArg;
    if (jsonArg.startsWith('@')) {
      const filePath = jsonArg.slice(1);
      if (!fs.existsSync(filePath)) {
        return { error: `File not found: ${filePath}` };
      }
      jsonBody = fs.readFileSync(filePath, 'utf8');
    }
    return await apiCall('POST', '/experimentalcenter/inspectionreport/report/insertUsers', JSON.parse(jsonBody));
  },

  async 'report-generate'(jsonArg) {
    // Generate report (state='1' Merge generate，'0' Single generate)
    // URL: POST /experimentalcenter/inspectionreport/report/insertReports
    // Usage:biolims.mjs report-generate '<json>' or @<filepath>
    // Example:biolims.mjs report-generate '@/path/to/generate.json'
    // Key: state="1"=Merge generate，changeEvent=0，Samples must be same order same batch
    if (!jsonArg) {
      return { error: 'Usage:biolims.mjs report-generate \'<json>\' or @<filepath>' };
    }
    let jsonBody = jsonArg;
    if (jsonArg.startsWith('@')) {
      const filePath = jsonArg.slice(1);
      if (!fs.existsSync(filePath)) {
        return { error: `File not found: ${filePath}` };
      }
      jsonBody = fs.readFileSync(filePath, 'utf8');
    }
    return await apiCall('POST', '/experimentalcenter/inspectionreport/report/insertReports', JSON.parse(jsonBody));
  },

  async 'report-list'(page = '1', rows = '20', state = '') {
    // Query report list
    const params = {
      bioTechLeaguePagingQuery: {
        page: parseInt(page),
        rows: parseInt(rows),
        sort: {},
        query: []
      },
      page: parseInt(page),
      rows: parseInt(rows)
    };
    if (state) {
      params.state = state;  // 0=Cancel，1=Complete，3=New，15=Pending modification，20=In progress
    }
    return await apiCall('POST', '/experimentalcenter/inspectionreport/report/reportlist', params);
  },

  async 'report-detail'(reportId, type = 'edit') {
    // Query report details (type: 'edit' Edit mode，'view' View mode)
    if (!reportId) {
      return { error: 'Usage:biolims.mjs report-detail <report_id> [type]' };
    }
    return await apiCall('POST', '/experimentalcenter/inspectionreport/report/selectReportTemplateOne', {
      sampleReportId: reportId,
      type: type
    });
  },

  async 'report-items'(reportId, page = '1', rows = '20') {
    // Query report sample details
    if (!reportId) {
      return { error: 'Usage:biolims.mjs report-items <report_id> [page] [rows]' };
    }
    return await apiCall('POST', '/experimentalcenter/inspectionreport/report/selectReportItem', {
      bioTechLeaguePagingQuery: {
        page: parseInt(page),
        rows: parseInt(rows),
        sort: {},
        pagingSearchOne: {},
        query: []
      },
      sort: {},
      pagingSearchOne: {},
      query: [],
      tableData: [],
      page: parseInt(page),
      rows: parseInt(rows),
      id: reportId
    });
  },

  async 'report-templates'(page = '1', rows = '10') {
    // Query available report templates
    return await apiCall('POST', '/experimentalcenter/inspectionreport/report/Pop-upsReportTemplate', {
      bioTechLeaguePagingQuery: {
        page: parseInt(page),
        rows: parseInt(rows),
        sort: {},
        pagingSearchOne: {},
        query: []
      },
      sort: {},
      pagingSearchOne: {},
      query: [],
      tableData: [],
      page: parseInt(page),
      rows: parseInt(rows)
    });
  },

  async 'report-save'(jsonArg) {
    // Save report basic info
    if (!jsonArg) {
      return { error: 'Usage:biolims.mjs report-save \'<json>\' or @<filepath>' };
    }
    let jsonBody = jsonArg;
    if (jsonArg.startsWith('@')) {
      const filePath = jsonArg.slice(1);
      if (!fs.existsSync(filePath)) {
        return { error: `File not found: ${filePath}` };
      }
      jsonBody = fs.readFileSync(filePath, 'utf8');
    }
    return await apiCall('POST', '/experimentalcenter/inspectionreport/report/saveReport', JSON.parse(jsonBody));
  },

  async 'report-file-generate'(reportId) {
    // Generate report file (Word)
    if (!reportId) {
      return { error: 'Usage:biolims.mjs report-file-generate <report_id>' };
    }
    // Use ReportGeneration API for Word file
    return await apiCall('POST', '/experimentalcenter/inspectionreport/report/ReportGeneration', {
      reportId: reportId
    });
  },

  async 'report-sending-list'(state = '1', page = '1', rows = '20') {
    // Query report send list (state: 1=Pending send，2=Sent，3=All)
    // URL: POST /experimentalcenter/inspectionreport/report/selectReportSend
    return await apiCall('POST', '/experimentalcenter/inspectionreport/report/selectReportSend', {
      bioTechLeaguePagingQuery: {
        page: parseInt(page),
        rows: parseInt(rows),
        sort: {},
        pagingSearchOne: {},
        query: []
      },
      sort: {},
      pagingSearchOne: {},
      query: [],
      tableData: [],
      page: parseInt(page),
      rows: parseInt(rows),
      state: state
    });
  },

  async 'report-send-confirm'(jsonArg) {
    // Confirm send report (email)
    if (!jsonArg) {
      return { error: 'Usage:biolims.mjs report-send-confirm \'<json>\' or @<filepath>' };
    }
    let jsonBody = jsonArg;
    if (jsonArg.startsWith('@')) {
      const filePath = jsonArg.slice(1);
      if (!fs.existsSync(filePath)) {
        return { error: `File not found: ${filePath}` };
      }
      jsonBody = fs.readFileSync(filePath, 'utf8');
    }
    return await apiCall('POST', '/experimentalcenter/inspectionreport/report/confirm', JSON.parse(jsonBody));
  },

  async 'report-send-offline'(jsonArg) {
    // Mark as offline send (express)
    if (!jsonArg) {
      return { error: 'Usage:biolims.mjs report-send-offline \'<json>\' or @<filepath>' };
    }
    let jsonBody = jsonArg;
    if (jsonArg.startsWith('@')) {
      const filePath = jsonArg.slice(1);
      if (!fs.existsSync(filePath)) {
        return { error: `File not found: ${filePath}` };
      }
      jsonBody = fs.readFileSync(filePath, 'utf8');
    }
    return await apiCall('POST', '/experimentalcenter/inspectionreport/report/sendReportSampleState', JSON.parse(jsonBody));
  },

  async 'report-recall'(jsonArg) {
    // Recall sent report
    if (!jsonArg) {
      return { error: 'Usage:biolims.mjs report-recall \'<json>\' or @<filepath>' };
    }
    let jsonBody = jsonArg;
    if (jsonArg.startsWith('@')) {
      const filePath = jsonArg.slice(1);
      if (!fs.existsSync(filePath)) {
        return { error: `File not found: ${filePath}` };
      }
      jsonBody = fs.readFileSync(filePath, 'utf8');
    }
    return await apiCall('POST', '/experimentalcenter/inspectionreport/report/recall', JSON.parse(jsonBody));
  },

  async 'report-complete'(reportId) {
    // Complete report (workflow)
    if (!reportId) {
      return { error: 'Usage:biolims.mjs report-complete <report_id>' };
    }
    
    // Step 1: Query workflow action list
    const actionsResult = await apiCall('POST', '/system/activiti/HandleTasks/selectHandleTasks', {
      appTypeTableId: 'SampleReport'
    });
    
    if (actionsResult.status !== 200 || !actionsResult.data || !actionsResult.data.length) {
      return { error: 'Failed to get handle actions', details: actionsResult };
    }
    
    // Find "Finish" or "Complete" action
    let finishAction = actionsResult.data.find(a => a.actionName === 'Finish' || a.actionName === 'Complete');
    if (!finishAction) {
      return { error: 'Finish/Complete action not found', availableActions: actionsResult.data };
    }
    
    // Step 2: Call HandleTasks to complete report
    const completeResult = await apiCall('POST', '/system/activiti/HandleTasks/HandleTasks', {
      appTypeTableId: finishAction.id,
      contentid: reportId,
      formName: 'Report',
      note: ''
    });
    
    return completeResult;
  },

  async 'select-handle-actions'(appTypeTableId = 'SampleReport') {
    // Query workflow actions (debug)
    return await apiCall('POST', '/system/activiti/HandleTasks/selectHandleTasks', {
      appTypeTableId: appTypeTableId
    });
  },

  // ============================================================================
  // Experiment Template (Experiment Template) - Base: /masterdata/experimentTemplate
  // ============================================================================

  async 'et-list'(page = '1', rows = '10', filter = '') {
    // Query template list (exclude voided state=30)
    const query = filter
      ? [[{ fieldName: 'templateName', operator: 'and', matchMode: 'contains', value: filter }]]
      : [];
    return await apiCall('POST', '/masterdata/experimentTemplate/ExperimentTemplateList', {
      page: parseInt(page), rows: parseInt(rows), query
    });
  },

  async 'et-detail'(templateId, mode = 'view') {
    // Query template details (3-level: main->steps->components)
    if (!templateId) return { error: 'Usage: biolims.mjs et-detail <template_id> [view|edit]' };
    return await apiCall('POST', '/masterdata/experimentTemplate/selectTemplateItemUpgrade', {
      id: templateId, type: mode
    });
  },

async 'et-create'(jsonArg) {
    // Create or update template (no id=create, with id=update)
    // Supports two modes:
    // 1. JSON mode: biolims.mjs et-create '<json>' or @<filepath>
    // 2. Interactive mode: biolims.mjs et-create（guides creation when no args）
    
    if (!jsonArg) {
      // Interactive: guide user to create simplified template
      console.log('📝 Experiment Template Creation Wizard (Simplified)');
      console.log('');
      console.log('This mode creates a template with:');
      console.log('  - 1 step');
      console.log('  - 2 components: detailTable + resultTable');
      console.log('');
      
      // 1. Query experiment types
      const expTypesResult = await apiCall('POST', '/masterdata/experimentTemplate/selectPopupsExperimentType', {});
      if (expTypesResult.status !== 200 || !expTypesResult.data?.result?.length) {
        return { error: 'Cannot get experiment type list, please try later' };
      }
      const expTypes = expTypesResult.data.result;
      console.log('📋 Available experiment types:');
      expTypes.forEach((t, i) => {
        console.log('   ' + (i + 1) + '. ' + t.experimentalTypeName + ' (' + t.id + ')');
      });
      console.log('');
      console.log('⚠️ Interactive mode requires readline, please use JSON file to create template');
      console.log('');
      console.log('Usage:biolims.mjs et-create @<json_file>');
      console.log('');
      return { 
        status: 200, 
        msg: 'Please use JSON file to create template',
        data: { expTypes, hint: 'use_json_file' }
      };
    }
    
    let body = jsonArg;
    if (jsonArg.startsWith('@')) {
      const fp = jsonArg.slice(1);
      if (!fs.existsSync(fp)) return { error: 'File not found: ' + fp };
      body = fs.readFileSync(fp, 'utf8');
    }
    return await apiCall('POST', '/masterdata/experimentTemplate/AddExperimentTemplate', JSON.parse(body));
  },
  async 'et-copy'(templateId) {
    // Deep copy template (steps, components, FastDFS attachments)
    if (!templateId) return { error: 'Usage: biolims.mjs et-copy <template_id>' };
    return await apiCall('POST', '/masterdata/experimentTemplate/copySop', { id: templateId });
  },

  async 'et-cancel'(...ids) {
    // Void template (creator only, state->30)
    if (!ids.length) return { error: 'Usage: biolims.mjs et-cancel <id1> [id2 ...]' };
    return await apiCall('POST', '/masterdata/experimentTemplate/cancelTemplate', { ids });
  },

  async 'et-complete'(templateId) {
    // Complete template (workflow, state->1, auto-register custom fields)
    if (!templateId) return { error: 'Usage: biolims.mjs et-complete <template_id>' };
    return await apiCall('POST', `/masterdata/experimentTemplate/updateExperimentTemplate?id=${templateId}`, {});
  },

  async 'et-step-add'(templateId, stepId, index = '1') {
    // Add step (index=1 below, index=0 above)
    if (!templateId || !stepId) return { error: 'Usage: biolims.mjs et-step-add <template_id> <step_id> <1|0>' };
    return await apiCall('POST', '/masterdata/experimentTemplate/updateExperimentTemplateSteps', {
      templateId, stepId, index: parseInt(index)
    });
  },

  async 'et-step-delete'(stepId) {
    // Delete step (cascade delete all components)
    if (!stepId) return { error: 'Usage: biolims.mjs et-step-delete <step_uuid>' };
    return await apiCall('POST', '/masterdata/experimentTemplate/deleteExperimentTemplate', { templateId: stepId });
  },

  async 'et-reagent-delete'(...ids) {
    // Delete reagent association
    if (!ids.length) return { error: 'Usage: biolims.mjs et-reagent-delete <id1> [id2 ...]' };
    return await apiCall('POST', '/masterdata/experimentTemplate/deleteReagentItemUpgradeOne', { reagentItemUpgradeId: ids });
  },

  async 'et-instrument-delete'(...ids) {
    // Delete equipment association
    if (!ids.length) return { error: 'Usage: biolims.mjs et-instrument-delete <id1> [id2 ...]' };
    return await apiCall('POST', '/masterdata/experimentTemplate/deleteCosItemUpgradeOne', { cosItemUpgradeId: ids });
  },

  async 'et-formula-list'(templateId, itemId, page = '1', rows = '10') {
    // Query formula list
    if (!templateId || !itemId) return { error: 'Usage: biolims.mjs et-formula-list <template_id> <item_id> [page] [rows]' };
    return await apiCall('POST', '/masterdata/experimentTemplate/selectTemplateUpgradeFormula', {
      templateId, templateItemUpgradeId: itemId,
      bioTechLeaguePagingQuery: { page: parseInt(page), rows: parseInt(rows), query: [] }
    });
  },

  async 'et-formula-update'(jsonArg) {
    // Batch update formulas
    if (!jsonArg) return { error: 'Usage: biolims.mjs et-formula-update \'<json_array>\' or @<filepath>' };
    let body = jsonArg;
    if (jsonArg.startsWith('@')) {
      const fp = jsonArg.slice(1);
      if (!fs.existsSync(fp)) return { error: `File not found: ${fp}` };
      body = fs.readFileSync(fp, 'utf8');
    }
    return await apiCall('POST', '/masterdata/experimentTemplate/updateTemplateUpgradeFormula', JSON.parse(body));
  },

  async 'et-formula-delete'(...ids) {
    // Batch delete formulas
    if (!ids.length) return { error: 'Usage: biolims.mjs et-formula-delete <id1> [id2 ...]' };
    return await apiCall('POST', '/masterdata/experimentTemplate/deleteTemplateUpgradeFormula', ids);
  },

  async 'et-threshold-list'(templateId, itemId) {
    // Query threshold list
    if (!templateId || !itemId) return { error: 'Usage: biolims.mjs et-threshold-list <template_id> <item_id>' };
    return await apiCall('POST', '/masterdata/experimentTemplate/selectTemplateReferenceUpgrade', {
      templateId, templateItemUpgradeId: itemId
    });
  },

  async 'et-threshold-update'(jsonArg) {
    // Batch update thresholds
    if (!jsonArg) return { error: 'Usage: biolims.mjs et-threshold-update \'<json_array>\' or @<filepath>' };
    let body = jsonArg;
    if (jsonArg.startsWith('@')) {
      const fp = jsonArg.slice(1);
      if (!fs.existsSync(fp)) return { error: `File not found: ${fp}` };
      body = fs.readFileSync(fp, 'utf8');
    }
    return await apiCall('POST', '/masterdata/experimentTemplate/updateTemplateReferenceUpgrade', JSON.parse(body));
  },

  async 'et-threshold-delete'(...ids) {
    // Batch delete thresholds
    if (!ids.length) return { error: 'Usage: biolims.mjs et-threshold-delete <id1> [id2 ...]' };
    return await apiCall('POST', '/masterdata/experimentTemplate/deleteTemplateReferenceUpgrade', ids);
  },

  async 'et-threshold-add'(templateId, tableCode, tableCodeId) {
    // Add threshold via popup
    if (!templateId) return { error: 'Usage: biolims.mjs et-threshold-add <template_id> <table_code> <table_code_id>' };
    return await apiCall('POST', '/masterdata/experimentTemplate/addPopupsReferenceUpgrade', {
      templateId, tableCode, tableCodeId
    });
  },

  async 'et-reagents'(page = '1', rows = '10') {
    // Popup select reagent
    return await apiCall('POST', '/masterdata/experimentTemplate/ReagentsList', {
      page: parseInt(page), rows: parseInt(rows), query: []
    });
  },

  async 'query-material-batch'(materialId, page = '1', rows = '20') {
    // Query material batch info
    // URL: POST /masterdata/ProcessExecution/queryMaterialInfo
    if (!materialId) {
      return { error: 'Usage:biolims.mjs query-material-batch <material_id> [page] [rows]' };
    }
    return await apiCall('POST', '/masterdata/ProcessExecution/queryMaterialInfo', {
      bioTechLeaguePagingQuery: {
        page: parseInt(page),
        rows: parseInt(rows),
        sort: {},
        pagingSearchOne: {},
        query: []
      },
      sort: {},
      pagingSearchOne: {},
      query: [],
      tableData: [],
      page: parseInt(page),
      rows: parseInt(rows),
      totalRecords: '1',
      id: materialId
    });
  },

  async 'et-instruments'(page = '1', rows = '20') {
    // Query all equipment list
    // URL: POST /procurement/instrument/InstrumentData/AllInstrumentData
    // Params: {"page":1,"rows":20,"sort":{"sortFiled":"create_date","sortOrder":"-1"},"pagingSearchOne":{},"query":[]}
    return await apiCall('POST', '/procurement/instrument/InstrumentData/AllInstrumentData', {
      page: parseInt(page),
      rows: parseInt(rows),
      sort: { sortFiled: 'create_date', sortOrder: '-1' },
      pagingSearchOne: {},
      query: []
    });
  },

  async 'et-exp-types'(page = '1', rows = '20') {
    // Query experiment type list
    // URL: POST /masterdata/ExperimentalTypeConfiguration/ExperimentalTypeConfigurationListDTO
    return await apiCall('POST', '/masterdata/ExperimentalTypeConfiguration/ExperimentalTypeConfigurationListDTO', {
      bioTechLeaguePagingQuery: {
        page: parseInt(page),
        rows: parseInt(rows),
        sort: {},
        pagingSearchOne: {},
        query: []
      },
      sort: {},
      pagingSearchOne: {},
      query: [],
      tableData: [],
      page: parseInt(page),
      rows: parseInt(rows),
      totalRecords: '8',
      isQuery: '1'
    });
  },

  async 'et-sample-types'() {
    // Query sample types
    return await apiCall('POST', '/masterdata/experimentTemplate/SampleTypeAll', {});
  },

  async 'et-approvers'(groupId) {
    // Query approver list
    // URL: POST /system/PersonnelGroup/selectgroupusernewpublic
    if (!groupId) return { error: 'Usage:biolims.mjs et-approvers <group_id>' };
    return await apiCall('POST', '/system/PersonnelGroup/selectgroupusernewpublic', {
      moduleId: 'ETemplateConfigLatest',
      field: 'auditor',
      bioTechLeaguePagingQuery: { page: 1, rows: 9999, sort: {}, pagingSearchOne: {}, query: [] },
      page: 1,
      rows: 9999,
      sort: {},
      pagingSearchOne: {},
      query: []
    });
  },

  async 'et-groups'(page = '1', rows = '20') {
    // Query experiment group list
    return await apiCall('POST', '/masterdata/experimentTemplate/selectPopupsPersonnelGroup', {
      bioTechLeaguePagingQuery: {
        page: parseInt(page),
        rows: parseInt(rows),
        sort: {},
        pagingSearchOne: {},
        query: []
      },
      sort: {},
      pagingSearchOne: {},
      query: [],
      tableData: [],
      page: parseInt(page),
      rows: parseInt(rows),
      totalRecords: '0'
    });
  },

  async 'et-custom-fields'(templateId, itemId = '') {
    // Query custom fields (for calculated columns)
    if (!templateId) return { error: 'Usage: biolims.mjs et-custom-fields <template_id> [item_id]' };
    return await apiCall('POST', '/masterdata/experimentTemplate/selectCustomFieldByParam', {
      templateId, templateItemUpgradeId: itemId
    });
  },

  async 'et-check-sql'(sql) {
    // Validate SQL syntax
    if (!sql) return { error: 'Usage: biolims.mjs et-check-sql \'<sql_statement>\'' };
    return await apiCall('POST', '/masterdata/experimentTemplate/checkSql', { checkSql: sql });
  },

  async 'et-all-completed'(page = '1', rows = '10') {
    // Query all completed templates (state=1)
    return await apiCall('POST', '/masterdata/experimentTemplate/selectExperimentTemplateAll', {
      page: parseInt(page), rows: parseInt(rows), query: []
    });
  }
};

// ============================================================================
// Main Entry
// ============================================================================
async function main() {
  const [,, command, ...args] = process.argv;

  if (!command || !commands[command]) {
    console.log(JSON.stringify({
      error: 'Unknown command. All 96 commands integrated!\n\n' +
             '===== Order Management =====\n' +
             'order | order-list | create-order | update-order | order-samples | order-fees | complete-order | cancel-order | sample-types | search-sample-type\n\n' +
             '===== Sample Receive =====\n' +
             'receive-list | receive | receive-samples | scan-barcode | create-receive | update-receive | complete-receive\n\n' +
             '===== Experiment Center (83 commands) =====\n' +
             'Basic: experiment-types | experiment-protocols | experiment-experimenters | create-experiment | experiment-list | experiment-detail | experiment-save | experiment-complete-step\n' +
             'Sample Pool: experiment-sample-pool | experiment-sample-pool-by-code | experiment-add-samples | experiment-remove-samples | experiment-add-samples-to-step\n' +
             'Mix/Split: experiment-mix-samples | experiment-cancel-mix | split-sample | split-sub-product | split-sub-product-by-number | split-locus\n' +
             'Results: add-experiment-result | select-result-by-sample | select-result-multi | delete-experiment-data | return-result\n' +
             'QC: select-qc-list | add-qc | submit-qc | select-qc-result | select-qc-results | select-qc-template-item | save-qc-template-item\n' +
             'Products: query-product-type | change-product | select-sub-product\n' +
             'Flow: select-next-flow | select-experiment-process | experiment-flow-by-product | experiment-flow-by-id\n' +
             'Batch: batch-warehousing | batch-export | batch-write | save-tapestation-data\n' +
             'Query: select-personnel-group | select-unit | select-dictionary | index-query\n\n' +
             '===== Sequencing QC (13 commands) =====\n' +
             'seq-qc-list | seq-qc-detail | save-seq-qc | seq-qc-item-list | delete-seq-qc-item | transact-seq-qc | export-seq-qc | import-seq-qc | recall-seq-qc | seq-qc-edit-template | seq-qc-import-template-btn | seq-qc-import-template | update-seq-qc-by-sample\n\n' +
             'More: use "node biolims.mjs --help-full" to see full command list'
    }));
    process.exit(1);
  }

  try {
    const result = await commands[command](...args);
    console.log(JSON.stringify(result, null, 2));
  } catch (error) {
    console.log(JSON.stringify({ error: error.message }));
    process.exit(1);
  }
}

main();
