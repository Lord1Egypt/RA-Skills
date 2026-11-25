import { execFile } from 'node:child_process';
import { createHmac, randomUUID } from 'node:crypto';
import { readFile } from 'node:fs/promises';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { promisify } from 'node:util';

const exec = promisify(execFile);
const runtimeDir = dirname(fileURLToPath(import.meta.url));
const setupEnv = resolve(runtimeDir, '.env');
const requestTimeout = 5000;

async function packageVersion(path) {
  return JSON.parse(await readFile(path, 'utf8')).version;
}

async function loadedSkillVersion() {
  const { stdout } = await exec('openclaw', ['skills', 'info', 'amber-voice-assistant', '--json'], {
    timeout: requestTimeout,
  });
  const skill = JSON.parse(stdout);
  if (skill.eligible !== true || skill.modelVisible === false) {
    throw new Error('Amber is unavailable to the active OpenClaw agent. Check that the skill is enabled.');
  }
  return skill.clawhub?.installedVersion
    ?? await packageVersion(resolve(dirname(skill.filePath), 'runtime', 'package.json'));
}

function publicBase(configured) {
  const url = new URL(configured);
  if (url.protocol !== 'https:' || url.username || url.password || url.search || url.hash) {
    throw new Error('Set PUBLIC_BASE_URL to the HTTPS URL of your Amber tunnel.');
  }
  return url.href.replace(/\/+$/, '');
}

async function health(base, request) {
  const response = await request(`${base}/healthz`);
  if (!response.ok || (await response.json()).ok !== true) throw new Error('No healthy Amber response');
  return {
    version: response.headers.get('x-amber-version'),
    instance: response.headers.get('x-amber-instance'),
  };
}

async function signatureCheck(request, url, body, headers, signature, expectedStatus) {
  const post = (extra) => request(url, { method: 'POST', body, headers: { ...headers, ...extra } });
  const unsigned = await post({});
  if (unsigned.status !== 401) {
    await unsigned.body?.cancel();
    throw new Error('Unsigned webhook was not rejected');
  }
  await unsigned.body?.cancel();
  const signed = await post(signature);
  await signed.body?.cancel();
  if (signed.status !== expectedStatus) throw new Error('Signed webhook was not accepted');
}

async function checkTwilio(cfg, base, request) {
  const { default: twilio } = await import('twilio');
  const url = `${base}/twilio/status`;
  const secret = cfg.VOICE_WEBHOOK_SECRET || cfg.TWILIO_AUTH_TOKEN;
  if (!secret) throw new Error('Missing Twilio webhook credentials');
  const signature = twilio.getExpectedTwilioSignature(secret, url, {});
  await signatureCheck(request, url, '', { 'Content-Type': 'application/x-www-form-urlencoded' },
    { 'X-Twilio-Signature': signature }, 204);
}

async function checkOpenAI(cfg, base, request) {
  const secret = cfg.OPENAI_WEBHOOK_SECRET;
  if (!secret) throw new Error('Missing OpenAI webhook secret');
  const key = secret.startsWith('whsec_') ? Buffer.from(secret.slice(6), 'base64') : secret;
  const body = JSON.stringify({ type: 'amber.preflight' });
  const id = randomUUID();
  const timestamp = String(Math.floor(Date.now() / 1000));
  const signature = createHmac('sha256', key).update(`${id}.${timestamp}.${body}`).digest('base64');
  await signatureCheck(request, `${base}/openai/webhook`, body, {
    'Content-Type': 'application/json',
    'webhook-id': id,
    'webhook-timestamp': timestamp,
  }, { 'webhook-signature': `v1,${signature}` }, 200);
}

export async function firstCallCheck(cfg, {
  fetchRequest = fetch,
  skillVersion = loadedSkillVersion,
} = {}) {
  const checks = [];
  const pass = (message) => checks.push({ status: 'pass', message });
  const fail = (message) => checks.push({ status: 'fail', message });
  const request = (url, options = {}) => fetchRequest(url, {
    ...options,
    redirect: 'error',
    signal: AbortSignal.timeout(requestTimeout),
    headers: { 'ngrok-skip-browser-warning': '1', ...options.headers },
  });
  const expected = await packageVersion(resolve(runtimeDir, 'package.json'));

  if ((cfg.AMBER_AGENT_PLATFORM || 'openclaw') === 'openclaw') {
    let active;
    try {
      active = await skillVersion();
    } catch {
      fail('Could not verify the Amber skill in OpenClaw. Start its gateway and check that amber-voice-assistant is enabled for the active agent.');
    }
    if (active === expected) pass(`OpenClaw is using Amber ${expected}.`);
    else if (active) fail(`OpenClaw is using Amber ${active}. Select your ${expected} skill and move any older Amber skill copies out of its skill search paths.`);
  }

  const port = Number(cfg.PORT || 8000);
  let local;
  try {
    if (!Number.isInteger(port) || port < 1 || port > 65535) throw new Error('Invalid runtime port');
    local = await health(`http://127.0.0.1:${port}`, request);
  } catch {
    fail('Amber did not respond locally. Confirm PORT, then run npm ci, npm run build, and npm start from this runtime directory.');
    return checks;
  }
  if (local.version !== expected || !local.instance) {
    fail(`The local bridge does not match this Amber build (${expected}). Rebuild and restart the bridge from this runtime directory.`);
    return checks;
  }
  pass(`Amber bridge ${expected} is running on port ${port}.`);

  let base;
  try {
    base = publicBase(cfg.PUBLIC_BASE_URL);
    const remote = await health(base, request);
    if (remote.version !== local.version || remote.instance !== local.instance) {
      fail(`PUBLIC_BASE_URL reaches a different bridge. Point the tunnel to this Amber bridge on port ${port}.`);
      return checks;
    }
  } catch {
    fail(`The public HTTPS URL could not reach Amber. Check PUBLIC_BASE_URL and the tunnel forwarding to port ${port}.`);
    return checks;
  }
  pass('Your public HTTPS URL reaches this Amber bridge.');

  if ((cfg.VOICE_PROVIDER || 'twilio') === 'twilio') {
    try {
      await checkTwilio(cfg, base, request);
      pass('Twilio webhook accepts a valid signature and rejects unsigned requests.');
    } catch {
      fail('Twilio webhook signature check failed. Check TWILIO_AUTH_TOKEN or VOICE_WEBHOOK_SECRET, set TWILIO_WEBHOOK_STRICT=true, and verify the proxy forwards the public HTTPS host.');
    }
  }
  try {
    await checkOpenAI(cfg, base, request);
    pass('OpenAI webhook accepts a valid signature and rejects unsigned requests.');
  } catch {
    fail('OpenAI webhook signature check failed. Check OPENAI_WEBHOOK_SECRET and verify the tunnel forwards the webhook body and headers unchanged.');
  }
  return checks;
}

export async function runFirstCallCheck() {
  let cfg;
  try {
    const { default: dotenv } = await import('dotenv');
    cfg = dotenv.parse(await readFile(setupEnv));
  } catch (error) {
    const message = error.code === 'ENOENT'
      ? 'Amber configuration is missing. Run npm run setup first.'
      : 'Amber could not load its setup configuration. Install dependencies with npm ci and check that runtime/.env is readable.';
    console.log(message);
    return false;
  }

  const checks = await firstCallCheck({ ...cfg, ...process.env });
  for (const { status, message } of checks) {
    console.log(`  ${status === 'pass' ? '✓' : '✗'} ${message}`);
  }
  const passed = checks.every(({ status }) => status === 'pass');
  console.log(passed
    ? '  Ready for a test call once the Twilio and OpenAI webhook URLs are saved in their provider consoles.'
    : '  Fix the items above, then rerun npm run setup -- --check.');
  return passed;
}
