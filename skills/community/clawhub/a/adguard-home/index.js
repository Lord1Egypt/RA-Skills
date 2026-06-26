#!/usr/bin/env node

/**
 * AdGuard Home Skill - Secure Version
 * 🛡️ Query AdGuard Home instances for DNS statistics and configuration
 * 
 * Security improvements:
 * - Replaced execSync/curl with native HTTPS requests
 * - Input validation and sanitization
 * - No command injection vulnerabilities
 * - Secure credential handling
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import https from 'https';
import http from 'http';
import { URL } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// ============ Security: Input Validation ============

/**
 * Validate and sanitize instance name (alphanumeric, dash, underscore only)
 */
function sanitizeInstanceName(name) {
  if (!name || typeof name !== 'string') {
    return null;
  }
  const sanitized = name.trim().replace(/[^a-zA-Z0-9_-]/g, '');
  return sanitized.length > 0 && sanitized.length <= 50 ? sanitized : null;
}

/**
 * Validate command against whitelist
 */
const ALLOWED_COMMANDS = new Set([
  'stats', 'top-clients', 'top-blocked', 'health', 
  'status', 'dns-info', 'filter-rules', 'querylog', 
  'clients', 'tls-status'
]);

function validateCommand(cmd) {
  return cmd && ALLOWED_COMMANDS.has(cmd) ? cmd : null;
}

/**
 * Validate integer with range
 */
function validateInt(value, min = 1, max = 100, defaultValue = 10) {
  const parsed = parseInt(value, 10);
  if (isNaN(parsed)) return defaultValue;
  return Math.max(min, Math.min(max, parsed));
}

/**
 * Validate URL format
 */
function validateUrl(urlStr) {
  try {
    const parsed = new URL(urlStr);
    return (parsed.protocol === 'http:' || parsed.protocol === 'https:') && parsed.hostname;
  } catch {
    return false;
  }
}

// ============ Configuration Loading ============

/**
 * Load configuration from environment variables (preferred secure method)
 */
function loadFromEnv() {
  if (process.env.ADGUARD_URL && process.env.ADGUARD_USERNAME && process.env.ADGUARD_PASSWORD) {
    return {
      default: {
        url: process.env.ADGUARD_URL,
        username: process.env.ADGUARD_USERNAME,
        password: process.env.ADGUARD_PASSWORD
      }
    };
  }
  return null;
}

/**
 * Load configuration from workspace file (local development only)
 */
function loadFromWorkspace() {
  // Only check current workspace directory (where the skill is located)
  const workspacePath = path.join(__dirname, 'adguard-instances.json');
  if (fs.existsSync(workspacePath)) {
    try {
      const config = JSON.parse(fs.readFileSync(workspacePath, 'utf8'));
      return config.instances || {};
    } catch (e) {
      console.error('❌ Error loading adguard-instances.json:', e.message);
    }
  }
  return null;
}

// Load configuration: env vars take priority, then workspace file
let instances = loadFromEnv() || loadFromWorkspace() || {};

// ============ HTTP Client (Secure, No execSync) ============

/**
 * Make HTTP POST request with cookie handling
 */
function httpRequest(baseUrl, endpoint, method = 'GET', postData = null, cookie = null) {
  return new Promise((resolve, reject) => {
    const fullUrl = new URL(endpoint, baseUrl);
    const protocol = fullUrl.protocol === 'https:' ? https : http;
    
    const options = {
      hostname: fullUrl.hostname,
      port: fullUrl.port || (fullUrl.protocol === 'https:' ? 443 : 80),
      path: fullUrl.pathname + fullUrl.search,
      method: method,
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      }
    };
    
    if (cookie) {
      options.headers['Cookie'] = cookie;
    }
    
    if (postData) {
      options.headers['Content-Length'] = Buffer.byteLength(postData);
    }
    
    const req = protocol.request(options, (res) => {
      const cookies = res.headers['set-cookie'];
      let cookieValue = null;
      if (cookies) {
        cookieValue = cookies.map(c => c.split(';')[0]).join('; ');
      }
      
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        resolve({
          statusCode: res.statusCode,
          data: data,
          cookie: cookieValue
        });
      });
    });
    
    req.on('error', reject);
    
    if (postData) {
      req.write(postData);
    }
    
    req.end();
  });
}

/**
 * Authenticate and get session cookie
 */
async function authenticate(baseUrl, username, password) {
  const response = await httpRequest(
    baseUrl, 
    '/control/login', 
    'POST', 
    JSON.stringify({ name: username, password: password })
  );
  
  if (response.statusCode !== 200 || !response.cookie) {
    throw new Error(`Authentication failed: HTTP ${response.statusCode}`);
  }
  
  return response.cookie;
}

/**
 * Make authenticated API call
 */
async function apiCall(baseUrl, cookie, endpoint) {
  const response = await httpRequest(baseUrl, endpoint, 'GET', null, cookie);
  
  if (response.statusCode !== 200) {
    throw new Error(`API call failed: HTTP ${response.statusCode}`);
  }
  
  return JSON.parse(response.data);
}

// ============ Main Logic ============

async function main() {
  const args = process.argv.slice(2);
  
  // Security: Validate command
  const command = validateCommand(args[0]) || 'stats';
  
  // Security: Sanitize instance name
  let instanceName = sanitizeInstanceName(args[1]);
  
  // Auto-select if only one instance
  if (!instanceName && Object.keys(instances).length === 1) {
    instanceName = Object.keys(instances)[0];
  }
  
  // Validate instance exists
  if (!instanceName || !instances[instanceName]) {
    if (Object.keys(instances).length === 0) {
      console.error('❌ No AdGuard instances configured.');
      console.error('\n🔒 Secure Configuration Options:');
      console.error('\nOption 1 (Recommended): Environment Variables');
      console.error('  export ADGUARD_URL="http://192.168.1.1:80"');
      console.error('  export ADGUARD_USERNAME="admin"');
      console.error('  export ADGUARD_PASSWORD="your-password"');
      console.error('\nOption 2: 1Password CLI');
      console.error('  export ADGUARD_PASSWORD=$(op read "op://vault/AdGuard/credential")');
      console.error('\nOption 3 (Local Dev Only): Workspace Config');
      console.error('  Create adguard-instances.json in skill directory');
      console.error('  ⚠️ Add to .gitignore - never commit credentials!');
    } else {
      console.error('❌ Instance not found:', instanceName || '(none specified)');
      console.error('📋 Available:', Object.keys(instances).join(', '));
    }
    process.exit(1);
  }
  
  const instance = instances[instanceName];
  const { url, username, password } = instance;
  
  // Security: Validate URL
  if (!validateUrl(url)) {
    console.error('❌ Invalid URL format in instance configuration');
    process.exit(1);
  }
  
  try {
    // Authenticate
    const cookie = await authenticate(url, username, password);
    
    let data;
    switch (command) {
      case 'stats':
        data = await apiCall(url, cookie, '/control/stats');
        console.log(`📊 AdGuard Home Statistics (${instanceName})`);
        console.log(`Total DNS Queries: ${data.num_dns_queries.toLocaleString()}`);
        console.log(`Blocked Requests: ${data.num_blocked_filtering.toLocaleString()} (${((data.num_blocked_filtering / data.num_dns_queries) * 100).toFixed(1)}%)`);
        console.log(`Avg Response Time: ${data.avg_processing_time.toFixed(3)}ms`);
        break;
        
      case 'top-clients':
        data = await apiCall(url, cookie, '/control/stats');
        const clients = {};
        for (const item of data.top_clients) {
          const [ip, count] = Object.entries(item)[0];
          clients[ip] = count;
        }
        console.log(`💻 Top Clients (${instanceName})`);
        Object.entries(clients).slice(0, 10).forEach(([ip, count], i) => {
          console.log(`${i + 1}. ${ip}: ${count.toLocaleString()} queries`);
        });
        break;
        
      case 'top-blocked':
        data = await apiCall(url, cookie, '/control/stats');
        const blocked = {};
        for (const item of data.top_blocked_domains) {
          const [domain, count] = Object.entries(item)[0];
          blocked[domain] = count;
        }
        console.log(`🚫 Top Blocked Domains (${instanceName})`);
        Object.entries(blocked).slice(0, 10).forEach(([domain, count], i) => {
          console.log(`${i + 1}. ${domain}: ${count.toLocaleString()} blocks`);
        });
        break;
        
      case 'health':
        try {
          const healthCheck = await httpRequest(url, '/', 'GET');
          console.log(`✅ Health Check (${instanceName}): HTTP ${healthCheck.statusCode}`);
        } catch (e) {
          console.error(`❌ Health Check (${instanceName}): Failed - ${e.message}`);
        }
        break;
        
      case 'status':
        data = await apiCall(url, cookie, '/control/status');
        console.log(`🔧 AdGuard Home Status (${instanceName})`);
        console.log(`Version: ${data.version}`);
        console.log(`Running: ${data.running ? '✅ Yes' : '❌ No'}`);
        console.log(`Protection: ${data.protection_enabled ? '✅ Enabled' : '❌ Disabled'}`);
        console.log(`DNS Port: ${data.dns_port}`);
        console.log(`HTTP Port: ${data.http_port}`);
        console.log(`Language: ${data.language}`);
        console.log(`DHCP Available: ${data.dhcp_available ? '✅ Yes' : '❌ No'}`);
        break;
        
      case 'dns-info':
        data = await apiCall(url, cookie, '/control/dns_info');
        console.log(`🌐 DNS Configuration (${instanceName})`);
        console.log(`Protection: ${data.protection_enabled ? '✅ Enabled' : '❌ Disabled'}`);
        console.log(`Rate Limit: ${data.ratelimit} req/s`);
        console.log(`Upstream Mode: ${data.upstream_mode}`);
        console.log(`Cache: ${data.cache_enabled ? `✅ ${(data.cache_size / 1024 / 1024).toFixed(0)}MB` : '❌ Disabled'}`);
        console.log(`DNSSEC: ${data.dnssec_enabled ? '✅ Enabled' : '❌ Disabled'}`);
        console.log(`IPv6: ${data.disable_ipv6 ? '❌ Disabled' : '✅ Enabled'}`);
        console.log(`\nUpstream DNS Servers:`);
        data.upstream_dns.forEach((dns, i) => {
          console.log(`  ${i + 1}. ${dns}`);
        });
        break;
        
      case 'filter-rules':
        data = await apiCall(url, cookie, '/control/filtering/status');
        console.log(`🛡️ Filter Rules (${instanceName})`);
        console.log(`Filtering: ${data.enabled ? '✅ Enabled' : '❌ Disabled'}`);
        console.log(`Update Interval: ${data.interval} hours`);
        console.log(`User Rules: ${data.user_rules ? data.user_rules.length : 0} custom rules`);
        console.log(`\nFilter Lists:`);
        if (data.filters && data.filters.length > 0) {
          data.filters.forEach((filter, i) => {
            const status = filter.enabled ? '✅' : '❌';
            console.log(`  ${i + 1}. ${status} ${filter.name} (${filter.rules_count} rules)`);
          });
        } else {
          console.log('  No filter lists configured');
        }
        break;
        
      case 'querylog':
        // Security: Validate limit parameter
        const limit = validateInt(args[2], 1, 100, 10);
        data = await apiCall(url, cookie, `/control/querylog?limit=${limit}&response_status="all"`);
        console.log(`📜 Recent DNS Queries (${instanceName}) - Last ${limit} entries\n`);
        if (data.data && data.data.length > 0) {
          data.data.forEach((entry, i) => {
            const status = entry.reason?.includes('Filtered') ? '🚫 BLOCKED' : '✅ OK';
            const domain = entry.question?.name || 'unknown';
            const client = entry.client || 'unknown';
            const time = new Date(entry.time).toLocaleTimeString();
            console.log(`${i + 1}. [${time}] ${status} ${domain} (${client})`);
            if (entry.rule) {
              console.log(`   Rule: ${entry.rule}`);
            }
          });
        } else {
          console.log('No query log entries found');
        }
        break;
        
      case 'clients':
        data = await apiCall(url, cookie, '/control/clients');
        console.log(`👥 Clients (${instanceName})`);
        if (data.clients && data.clients.length > 0) {
          data.clients.forEach((client, i) => {
            console.log(`${i + 1}. ${client.name || client.ids?.[0] || 'Unknown'}`);
            if (client.use_global_settings === false) {
              console.log(`   Custom settings enabled`);
            }
            if (client.blocking_mode) {
              console.log(`   Blocking mode: ${client.blocking_mode}`);
            }
          });
        } else {
          console.log('No manually configured clients');
        }
        console.log(`\nAuto-discovered clients: ${data.auto_clients?.length || 0}`);
        break;
        
      case 'tls-status':
        data = await apiCall(url, cookie, '/control/tls/status');
        console.log(`🔒 TLS/Encryption Status (${instanceName})`);
        console.log(`TLS Enabled: ${data.enabled ? '✅ Yes' : '❌ No'}`);
        console.log(`Force HTTPS: ${data.force_https ? '✅ Yes' : '❌ No'}`);
        console.log(`Valid Certificate: ${data.valid_cert ? '✅ Yes' : '❌ No'}`);
        console.log(`HTTPS Port: ${data.port_https}`);
        console.log(`DoT Port: ${data.port_dns_over_tls}`);
        console.log(`DoQ Port: ${data.port_dns_over_quic}`);
        console.log(`Allow Unencrypted DoH: ${data.allow_unencrypted_doh ? '✅ Yes' : '❌ No'}`);
        break;
        
      default:
        // Should not reach here due to validateCommand
        console.error('❌ Unknown command');
        process.exit(1);
    }
  } catch (e) {
    console.error('❌ Error:', e.message);
    process.exit(1);
  }
}

main();
