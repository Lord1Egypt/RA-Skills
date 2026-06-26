/**
 * A2A Secret Manager
 * Manages node secrets for EvoMap hub connectivity
 */

const https = require('https');
const http = require('http');
const fs = require('fs');
const path = require('path');

const HUB_URL = process.env.EVOMAP_HUB_URL || 'https://evomap.ai';
const NODE_ID = process.env.EVOMAP_NODE_ID;

/**
 * Make HTTP request
 * @param {string} urlStr - URL to request
 * @param {object} options - Request options
 * @returns {Promise<object>} - Response data
 */
function makeRequest(urlStr, options = {}) {
  return new Promise((resolve, reject) => {
    const url = new URL(urlStr);
    const lib = url.protocol === 'https:' ? https : http;
    
    const reqOptions = {
      hostname: url.hostname,
      port: url.port || (url.protocol === 'https:' ? 443 : 80),
      path: url.pathname + url.search,
      method: options.method || 'GET',
      headers: {
        'Content-Type': 'application/json',
        ...(options.headers || {})
      }
    };
    
    const req = lib.request(reqOptions, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const parsed = JSON.parse(data);
          resolve({ status: res.statusCode, data: parsed });
        } catch (e) {
          resolve({ status: res.statusCode, data: data });
        }
      });
    });
    
    req.on('error', reject);
    
    if (options.body) {
      req.write(JSON.stringify(options.body));
    }
    req.end();
  });
}

/**
 * Get node ID from various sources
 * @returns {string|null} - Node ID
 */
function getNodeId() {
  // Try environment variable first
  if (NODE_ID) return NODE_ID;
  
  // Try to read from node config
  const configPaths = [
    path.join(process.cwd(), '.evomap', 'node.json'),
    path.join(process.cwd(), 'evomap', 'node.json'),
    path.join(process.env.HOME || '', '.evomap', 'node.json')
  ];
  
  for (const configPath of configPaths) {
    try {
      if (fs.existsSync(configPath)) {
        const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
        if (config.node_id) return config.node_id;
      }
    } catch (e) {}
  }
  
  return null;
}

/**
 * Get stored secret
 * @returns {string|null} - Current secret
 */
function getStoredSecret() {
  const secretPaths = [
    path.join(process.cwd(), '.evomap', 'secret'),
    path.join(process.cwd(), '.evomap', 'node_secret'),
    path.join(process.env.HOME || '', '.evomap', 'secret')
  ];
  
  for (const secretPath of secretPaths) {
    try {
      if (fs.existsSync(secretPath)) {
        return fs.readFileSync(secretPath, 'utf8').trim();
      }
    } catch (e) {}
  }
  
  return process.env.EVOMAP_NODE_SECRET || null;
}

/**
 * Save secret to storage
 * @param {string} secret - Secret to save
 * @param {string} storagePath - Optional custom path
 */
function saveSecret(secret, storagePath = null) {
  const targetPath = storagePath || path.join(process.cwd(), '.evomap', 'secret');
  
  // Ensure directory exists
  const dir = path.dirname(targetPath);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
  
  fs.writeFileSync(targetPath, secret, 'utf8');
  return targetPath;
}

/**
 * Check if current secret is valid
 * @param {string} nodeId - Node ID
 * @param {string} secret - Current secret
 * @returns {Promise<object>} - Validation result
 */
async function validateSecret(nodeId, secret) {
  try {
    const response = await makeRequest(`${HUB_URL}/a2a/validate`, {
      method: 'POST',
      body: {
        protocol: 'gep-a2a',
        protocol_version: '1.0.0',
        message_type: 'validate',
        sender_id: nodeId,
        auth: { node_secret: secret }
      }
    });
    
    return {
      valid: response.status === 200,
      status: response.status,
      data: response.data
    };
  } catch (e) {
    return { valid: false, error: e.message };
  }
}

/**
 * Rotate the node secret
 * @param {string} nodeId - Node ID
 * @param {string} currentSecret - Current secret (optional)
 * @returns {Promise<object>} - Rotation result with new secret
 */
async function rotateSecret(nodeId, currentSecret = null) {
  const payload = {
    protocol: 'gep-a2a',
    protocol_version: '1.0.0',
    message_type: 'hello',
    sender_id: nodeId,
    payload: { rotate_secret: true }
  };
  
  // Add auth if we have a current secret
  if (currentSecret) {
    payload.auth = { node_secret: currentSecret };
  }
  
  try {
    const response = await makeRequest(`${HUB_URL}/a2a/hello`, {
      method: 'POST',
      body: payload
    });
    
    if (response.status === 200 && response.data.node_secret) {
      return {
        success: true,
        newSecret: response.data.node_secret,
        nodeId: response.data.node_id || nodeId,
        data: response.data
      };
    }
    
    return {
      success: false,
      status: response.status,
      error: response.data.error || 'Rotation failed',
      data: response.data
    };
  } catch (e) {
    return { success: false, error: e.message };
  }
}

/**
 * Full secret management workflow
 * @param {object} options - Options
 * @returns {Promise<object>} - Result
 */
async function manageSecret(options = {}) {
  const nodeId = options.nodeId || getNodeId();
  
  if (!nodeId) {
    return { success: false, error: 'Node ID not found. Set EVOMAP_NODE_ID or create node config.' };
  }
  
  const currentSecret = options.secret || getStoredSecret();
  
  // If force rotate or no current secret, rotate
  if (options.forceRotate || !currentSecret) {
    console.log(`Rotating secret for node ${nodeId}...`);
    const result = await rotateSecret(nodeId, currentSecret);
    
    if (result.success) {
      const savedPath = saveSecret(result.newSecret, options.storagePath);
      console.log(`New secret saved to: ${savedPath}`);
      return { success: true, action: 'rotated', ...result, savedPath };
    }
    
    return result;
  }
  
  // Validate current secret
  console.log(`Validating current secret for node ${nodeId}...`);
  const validation = await validateSecret(nodeId, currentSecret);
  
  if (validation.valid) {
    console.log('Current secret is valid.');
    return { success: true, action: 'validated', valid: true };
  }
  
  // Secret is invalid, rotate
  console.log('Current secret is invalid. Rotating...');
  const result = await rotateSecret(nodeId, currentSecret);
  
  if (result.success) {
    const savedPath = saveSecret(result.newSecret, options.storagePath);
    console.log(`New secret saved to: ${savedPath}`);
    return { success: true, action: 'rotated', ...result, savedPath };
  }
  
  return { success: false, action: 'rotate_failed', ...result };
}

/**
 * Get secret status
 * @returns {object} - Status info
 */
function getStatus() {
  const nodeId = getNodeId();
  const secret = getStoredSecret();
  
  return {
    nodeId: nodeId || 'not configured',
    hasSecret: !!secret,
    secretPreview: secret ? `${secret.substring(0, 8)}...` : null,
    hubUrl: HUB_URL
  };
}

/**
 * Main entry point
 */
async function main() {
  const command = process.argv[2] || 'status';
  
  switch (command) {
    case 'status':
      console.log('A2A Secret Status:');
      console.log(JSON.stringify(getStatus(), null, 2));
      break;
      
    case 'rotate':
      const rotateResult = await manageSecret({ forceRotate: true });
      console.log(JSON.stringify(rotateResult, null, 2));
      process.exit(rotateResult.success ? 0 : 1);
      break;
      
    case 'validate':
      const validateResult = await manageSecret();
      console.log(JSON.stringify(validateResult, null, 2));
      process.exit(validateResult.success ? 0 : 1);
      break;
      
    case 'auto':
      const autoResult = await manageSecret();
      console.log(JSON.stringify(autoResult, null, 2));
      process.exit(autoResult.success ? 0 : 1);
      break;
      
    default:
      console.log('Usage: node index.js [status|rotate|validate|auto]');
      console.log('  status   - Show current secret status');
      console.log('  rotate   - Force rotate the secret');
      console.log('  validate - Check if current secret is valid');
      console.log('  auto     - Auto-manage: validate and rotate if needed');
  }
}

module.exports = {
  getNodeId,
  getStoredSecret,
  saveSecret,
  validateSecret,
  rotateSecret,
  manageSecret,
  getStatus,
  main
};

if (require.main === module) {
  main();
}
