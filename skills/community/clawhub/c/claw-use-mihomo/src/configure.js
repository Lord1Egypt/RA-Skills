import { existsSync, mkdirSync, readFileSync, renameSync, unlinkSync, writeFileSync } from 'fs';
import { spawnSync } from 'child_process';
import { dirname, join } from 'path';
import { parse as parseYaml, stringify as stringifyYaml } from 'yaml';
import { findBinary, getConfigDir } from './platform.js';
import { parseProxyUrl, fetchSubscription } from './subscribe.js';
import { log } from './logger.js';

const CONFIG_TEMPLATE = {
  'mixed-port': 7890,
  'allow-lan': false,
  'bind-address': '*',
  mode: 'rule',
  'log-level': 'info',
  'external-controller': '0.0.0.0:9090',
  'unified-delay': true,
  'tcp-concurrent': true,
  ipv6: true,
  dns: {
    enable: true,
    ipv6: true,
    'enhanced-mode': 'fake-ip',
    'fake-ip-range': '198.18.0.1/16',
    'default-nameserver': ['223.5.5.5', '119.29.29.29'],
    nameserver: ['223.5.5.5', '119.29.29.29'],
    fallback: ['https://cloudflare-dns.com/dns-query', 'https://dns.google/dns-query'],
    'fallback-filter': {
      geoip: true,
      'geoip-code': 'CN'
    }
  },
  tun: {
    enable: true,
    stack: 'system',
    'dns-hijack': ['any:53'],
    'auto-route': true,
    'auto-detect-interface': true
  }
};

function isPlainObject(value) {
  return Boolean(value) && typeof value === 'object' && !Array.isArray(value);
}

function validateProxy(proxy, index, source) {
  if (!isPlainObject(proxy)) {
    throw new Error(`${source}: proxy #${index + 1} must be an object`);
  }

  for (const key of ['name', 'type', 'server', 'port']) {
    if (proxy[key] === undefined || proxy[key] === null || proxy[key] === '') {
      throw new Error(`${source}: proxy #${index + 1} is missing '${key}'`);
    }
  }

  if (!Number.isFinite(Number(proxy.port)) || Number(proxy.port) <= 0) {
    throw new Error(`${source}: proxy #${index + 1} has invalid 'port'`);
  }
}

function validateClashConfig(doc, source) {
  if (!isPlainObject(doc)) {
    throw new Error(`${source}: config must be a YAML object`);
  }

  if (!Array.isArray(doc.proxies) || doc.proxies.length === 0) {
    throw new Error(`${source}: 'proxies' must be a non-empty array`);
  }

  if (!Array.isArray(doc['proxy-groups']) || doc['proxy-groups'].length === 0) {
    throw new Error(`${source}: 'proxy-groups' must be a non-empty array`);
  }

  if (!Array.isArray(doc.rules) || doc.rules.length === 0) {
    throw new Error(`${source}: 'rules' must be a non-empty array`);
  }

  doc.proxies.forEach((proxy, index) => validateProxy(proxy, index, source));
  return doc;
}

function parseAndValidateYaml(content, source) {
  let parsed;
  try {
    parsed = parseYaml(content);
  } catch (error) {
    throw new Error(`${source}: invalid YAML - ${error.message}`);
  }

  return validateClashConfig(parsed, source);
}

function buildConfigFromProxies(proxies) {
  const proxyNames = proxies.map(proxy => proxy.name);

  return {
    ...CONFIG_TEMPLATE,
    proxies,
    'proxy-groups': [
      {
        name: '🚀节点选择',
        type: 'select',
        proxies: ['♻️自动选择', 'DIRECT', ...proxyNames]
      },
      {
        name: '♻️自动选择',
        type: 'url-test',
        url: 'https://www.gstatic.com/generate_204',
        interval: 300,
        tolerance: 50,
        proxies: proxyNames
      }
    ],
    rules: ['GEOIP,cn,DIRECT', 'MATCH,🚀节点选择']
  };
}

function ensureGroupIncludesProxy(group, proxyName) {
  if (!Array.isArray(group.proxies)) group.proxies = [];
  if (!group.proxies.includes(proxyName)) {
    group.proxies.push(proxyName);
  }
}

function runOptionalMihomoValidation(tempPath, config) {
  const binaryPath = config?.mihomo?.binaryPath || findBinary();
  if (!binaryPath) {
    log('Skipping optional mihomo -t validation: binary not found');
    return;
  }

  const result = spawnSync(binaryPath, ['-t', '-d', dirname(tempPath), '-f', tempPath], {
    encoding: 'utf8',
    stdio: ['ignore', 'pipe', 'pipe']
  });

  if (result.error) {
    log(`Optional mihomo -t validation failed to start: ${result.error.message}`);
    return;
  }

  if (result.status !== 0) {
    const message = (result.stderr || result.stdout || '').trim() || 'unknown error';
    log(`Optional mihomo -t validation failed (non-blocking): ${message}`);
  }
}

function atomicWriteConfig(configPath, yamlContent, config) {
  mkdirSync(dirname(configPath), { recursive: true });

  const tempPath = `${configPath}.tmp-${process.pid}-${Date.now()}`;
  const backupPath = `${configPath}.bak`;

  writeFileSync(tempPath, yamlContent, 'utf8');
  const validatedConfig = parseAndValidateYaml(readFileSync(tempPath, 'utf8'), tempPath);
  runOptionalMihomoValidation(tempPath, config);

  try {
    if (existsSync(backupPath)) {
      unlinkSync(backupPath);
    }

    if (existsSync(configPath)) {
      renameSync(configPath, backupPath);
    }

    renameSync(tempPath, configPath);
    return validatedConfig;
  } catch (error) {
    if (!existsSync(configPath) && existsSync(backupPath)) {
      try {
        renameSync(backupPath, configPath);
      } catch {}
    }
    throw error;
  } finally {
    if (existsSync(tempPath)) {
      unlinkSync(tempPath);
    }
  }
}

export async function configure(subscriptionUrl, config) {
  const configDir = getConfigDir();
  const configPath = config?.mihomo?.configPath || join(configDir, 'config.yaml');

  log(`Fetching subscription: ${subscriptionUrl}`);
  const sub = await fetchSubscription(subscriptionUrl);

  let yamlContent;

  if (sub.format === 'clash') {
    const clashConfig = sub.config || parseAndValidateYaml(sub.raw, 'subscription');
    yamlContent = stringifyYaml(clashConfig);
    log('Validated clash-format subscription');
  } else {
    const builtConfig = validateClashConfig(buildConfigFromProxies(sub.proxies), 'generated config');
    yamlContent = stringifyYaml(builtConfig);
  }

  const writtenConfig = atomicWriteConfig(configPath, yamlContent, config);
  log(`Config written to ${configPath}`);

  const nodeCount = writtenConfig.proxies.length;
  const groupCount = writtenConfig['proxy-groups'].length;

  return { configured: true, nodes: nodeCount, groups: groupCount, path: configPath };
}

export async function addNode(proxyUrl, config) {
  const configPath = config?.mihomo?.configPath || join(getConfigDir(), 'config.yaml');

  if (!existsSync(configPath)) {
    throw new Error(`Config not found: ${configPath}. Run 'mihomod config' first.`);
  }

  const proxy = parseProxyUrl(proxyUrl);
  log(`Parsed: ${proxy.name} (${proxy.type}) -> ${proxy.server}:${proxy.port}`);

  const content = readFileSync(configPath, 'utf8');
  const parsedConfig = parseAndValidateYaml(content, configPath);

  parsedConfig.proxies.push(proxy);

  const targetGroups = new Set([config?.selector, '🚀节点选择', '♻️自动选择'].filter(Boolean));
  for (const group of parsedConfig['proxy-groups']) {
    if (targetGroups.has(group.name)) {
      ensureGroupIncludesProxy(group, proxy.name);
    }
  }

  atomicWriteConfig(configPath, stringifyYaml(parsedConfig), config);

  return { added: true, name: proxy.name, type: proxy.type, server: proxy.server, port: proxy.port };
}
