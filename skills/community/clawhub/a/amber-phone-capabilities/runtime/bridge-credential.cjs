// Local installation credential, shared by the bridge and bundled local clients.
// Never serves credentials over HTTP; a tunnel's loopback peer is not authentication.
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
exports.resolveBridgeCredential = function(runtimeDir) {
  // Bundled clients may start outside runtime/ and do not load dotenv/config.
  // Read only this installation's token settings; never export other secrets.
  const envPath = path.join(runtimeDir, '.env');
  const localEnv = fs.existsSync(envPath) ? require('dotenv').parse(fs.readFileSync(envPath)) : {};
  const configured = process.env.BRIDGE_API_TOKEN || localEnv.BRIDGE_API_TOKEN;
  if (configured) return configured;
  const configuredPath = process.env.AMBER_BRIDGE_TOKEN_FILE || localEnv.AMBER_BRIDGE_TOKEN_FILE || path.join('data', 'bridge-api-token');
  const tokenPath = path.resolve(runtimeDir, configuredPath);
  fs.mkdirSync(path.dirname(tokenPath), { recursive: true, mode: 0o700 });
  try { fs.writeFileSync(tokenPath, crypto.randomBytes(32).toString('hex') + '\n', { flag: 'wx', mode: 0o600 }); }
  catch (error) { if (error.code !== 'EEXIST') throw error; }
  const st = fs.lstatSync(tokenPath);
  if (!st.isFile() || st.isSymbolicLink() || (st.mode & 0o077) || (process.getuid && st.uid !== process.getuid())) {
    throw new Error('Bridge credential file must be an owner-only regular file (chmod 600).');
  }
  const token = fs.readFileSync(tokenPath, 'utf8').trim();
  if (!/^[a-f0-9]{64}$/.test(token)) throw new Error('Invalid generated bridge credential file');
  return token;
};
