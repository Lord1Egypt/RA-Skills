const fs = require('fs');
const path = require('path');

function loadCredentialsFile(file = path.join(__dirname, '..', 'config', 'IMAP_CREDENTIALS.js')) {
  if (!fs.existsSync(file)) return {};
  const loaded = require(file);
  const profileName = process.env.IMAP_PROFILE || loaded.defaultProfile;
  if (loaded.profiles && profileName && loaded.profiles[profileName]) return loaded.profiles[profileName];
  if (loaded.profiles && !profileName) {
    const first = Object.keys(loaded.profiles)[0];
    return first ? loaded.profiles[first] : {};
  }
  return loaded;
}

function loadDotEnv(file = path.join(__dirname, '..', '.env')) {
  if (!fs.existsSync(file)) return;
  const lines = fs.readFileSync(file, 'utf8').split(/\r?\n/);
  for (const line of lines) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith('#')) continue;
    const eq = trimmed.indexOf('=');
    if (eq === -1) continue;
    const key = trimmed.slice(0, eq).trim();
    let value = trimmed.slice(eq + 1).trim();
    if ((value.startsWith('"') && value.endsWith('"')) || (value.startsWith("'") && value.endsWith("'"))) {
      value = value.slice(1, -1);
    }
    if (key && process.env[key] === undefined) process.env[key] = value;
  }
}

function required(name) {
  const value = process.env[name];
  if (!value) {
    throw new Error(`Missing required environment variable: ${name}. Copy .env.example to .env and fill it.`);
  }
  return value;
}

function getImapConfig() {
  loadDotEnv();
  const credentials = loadCredentialsFile();
  return {
    user: credentials.user || credentials.IMAP_USER || required('IMAP_USER'),
    password: credentials.password || credentials.IMAP_PASSWORD || required('IMAP_PASSWORD'),
    host: credentials.host || credentials.IMAP_HOST || process.env.IMAP_HOST || 'imap.qq.com',
    port: Number(credentials.port || credentials.IMAP_PORT || process.env.IMAP_PORT || 993),
    tls: String(credentials.tls ?? credentials.IMAP_TLS ?? process.env.IMAP_TLS ?? 'true') !== 'false',
    tlsOptions: { rejectUnauthorized: String(credentials.rejectUnauthorized ?? credentials.IMAP_REJECT_UNAUTHORIZED ?? process.env.IMAP_REJECT_UNAUTHORIZED ?? 'false') === 'true' },
    connTimeout: Number(credentials.connTimeout || credentials.IMAP_CONN_TIMEOUT || process.env.IMAP_CONN_TIMEOUT || 20000),
    authTimeout: Number(credentials.authTimeout || credentials.IMAP_AUTH_TIMEOUT || process.env.IMAP_AUTH_TIMEOUT || 20000),
  };
}

function getMailbox() {
  loadDotEnv();
  const credentials = loadCredentialsFile();
  return credentials.mailbox || credentials.MAILBOX || process.env.MAILBOX || 'INBOX';
}

function getMailWebUser() {
  loadDotEnv();
  const credentials = loadCredentialsFile();
  const user = credentials.mailWebUser || credentials.MAIL_WEB_USER || process.env.MAIL_WEB_USER || credentials.user || credentials.IMAP_USER || process.env.IMAP_USER || '';
  return String(user).split('@')[0];
}

module.exports = { loadDotEnv, getImapConfig, getMailbox, getMailWebUser };
