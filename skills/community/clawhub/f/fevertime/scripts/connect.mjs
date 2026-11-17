import { execFile } from 'node:child_process';
import { createHash, createPrivateKey, createPublicKey, generateKeyPairSync, randomUUID, sign } from 'node:crypto';
import { link, lstat, mkdir, readFile, unlink, writeFile } from 'node:fs/promises';
import { homedir } from 'node:os';
import { join } from 'node:path';
import { promisify } from 'node:util';

const exec = promisify(execFile);
const origin = 'https://fevertime.xyz';
const uuid = /^[a-f0-9]{8}(?:-[a-f0-9]{4}){3}-[a-f0-9]{12}$/;

async function readPrivate(path) {
  try {
    const stat = await lstat(path);
    if (!stat.isFile() || (stat.mode & 0o077) !== 0) {
      throw new Error('Fevertime identity files must be regular files with owner-only permissions.');
    }
    return JSON.parse(await readFile(path, 'utf8'));
  } catch (error) {
    if (error.code === 'ENOENT') return null;
    throw error;
  }
}

async function createPrivate(path, value) {
  const staging = `${path}.${randomUUID()}.tmp`;
  await writeFile(staging, JSON.stringify(value), { flag: 'wx', mode: 0o600 });
  try {
    await link(staging, path);
  } catch (error) {
    if (error.code !== 'EEXIST') throw error;
  } finally {
    await unlink(staging);
  }
  return readPrivate(path);
}

async function agentAuth(profile, tab, input) {
  // Only the fixed auth entry point receives data. Recheck the page in the evaluated document.
  const fn = `async () => {
    if (location.origin !== ${JSON.stringify(origin)} || location.pathname !== '/agent') {
      return { ok: false, error: { code: 'FEVERTIME_AGENT_PAGE_REQUIRED' } };
    }
    if (window.__bridge?.guide !== ${JSON.stringify(`${origin}/skill.md`)} ||
        typeof window.__bridge.agentAuth !== 'function') {
      return { ok: false, error: { code: 'FEVERTIME_BRIDGE_NOT_READY' } };
    }
    return await window.__bridge.agentAuth(${JSON.stringify(input)});
  }`;
  let result;
  try {
    const { stdout } = await exec('openclaw', [
      'browser', '--json', '--browser-profile', profile, 'evaluate', '--target-id', tab,
      '--timeout-ms', '40000', '--fn', fn,
    ], { timeout: 45000, maxBuffer: 512 * 1024 });
    result = JSON.parse(stdout).result;
  } catch {
    // Child-process errors can include the invocation and its short-lived signature.
    throw new Error('OpenClaw browser evaluation failed. Check the profile, tab, and page evaluation permission.');
  }
  if (!result?.ok) {
    const code = result?.error?.code;
    throw new Error(typeof code === 'string' && /^[A-Za-z0-9_-]{1,80}$/.test(code) ? code : 'FEVERTIME_AUTH_FAILED');
  }
  return result.data;
}

function checkChallenge(data, clientInstanceId, publicKey) {
  const fingerprint = createHash('sha256').update(Buffer.from(publicKey, 'base64url')).digest('base64url');
  const expected = ['heytraders-agent-browser-auth-v1', `origin:${origin}`, `key:${fingerprint}`, `client:${clientInstanceId}`];
  const lines = typeof data?.challenge === 'string' ? data.challenge.split('\n') : [];
  const remaining = data?.expires_at - Math.floor(Date.now() / 1000);
  if (data?.algorithm !== 'Ed25519' || !uuid.test(data.challenge_id) || !Number.isInteger(remaining) ||
      remaining <= 0 || remaining > 125 || lines.length !== 5 ||
      expected.some((line, i) => lines[i] !== line) || !/^nonce:[A-Za-z0-9_-]{43}$/.test(lines[4])) {
    throw new Error('Fevertime returned an invalid or mismatched sign-in challenge.');
  }
}

async function connect(args) {
  const [profile, tab, displayName, country, description] = args;
  const hasProfile = args.length === 5;
  if ((args.length !== 2 && !hasProfile) || !/^[a-zA-Z0-9_-]{1,64}$/.test(profile ?? '') ||
      !/^[a-zA-Z0-9_.:-]{1,128}$/.test(tab ?? '') ||
      (hasProfile && (!displayName.trim() || [...displayName].length > 80 || !/^[A-Z]{2}$/.test(country) ||
        [...description.trim()].length < 10 || [...description].length > 280))) {
    throw new Error('Usage: node connect.mjs <profile> <tab-id> [<display-name> <country> <description>]');
  }

  const root = join(process.env.OPENCLAW_STATE_DIR || join(homedir(), '.openclaw'), 'fevertime', profile);
  const identityPath = join(root, 'identity.json');
  const accountPath = join(root, 'account.json');
  let identity = await readPrivate(identityPath);
  const account = await readPrivate(accountPath);
  const status = await agentAuth(profile, tab, { operation: 'status' });
  if (status.authSource) {
    if (!identity || !status.authenticated || !account || account.agentId !== status.agentId) {
      throw new Error('The browser profile already has a different session. Use a dedicated browser profile.');
    }
    return { authenticated: true, agentId: status.agentId, created: false, nextSteps: status.nextSteps };
  }
  if (!account && !hasProfile) throw new Error('First sign-in requires a public display name, country, and research description.');

  if (!identity) {
    if (account) throw new Error('The stored Fevertime identity key is missing. Restore it before signing in.');
    await mkdir(root, { recursive: true, mode: 0o700 });
    const { privateKey } = generateKeyPairSync('ed25519');
    identity = await createPrivate(identityPath, {
      clientInstanceId: randomUUID(), privateKey: privateKey.export({ format: 'pem', type: 'pkcs8' }),
    });
  }
  const { clientInstanceId } = identity;
  const privateKey = createPrivateKey(identity.privateKey);
  if (privateKey.asymmetricKeyType !== 'ed25519' || !uuid.test(clientInstanceId)) {
    throw new Error('Invalid persisted Fevertime identity.');
  }
  const publicKey = createPublicKey(privateKey).export({ format: 'jwk' }).x;
  const challenge = await agentAuth(profile, tab, {
    operation: 'challenge', publicKey, clientInstanceId, entryClient: 'openclaw',
    ...(!account && hasProfile ? { displayName, country, description, agentKind: 'openclaw' } : {}),
  });
  checkChallenge(challenge, clientInstanceId, publicKey);
  const signature = sign(null, Buffer.from(challenge.challenge, 'utf8'), privateKey).toString('base64url');
  const completed = await agentAuth(profile, tab, { operation: 'complete', challengeId: challenge.challenge_id, signature });
  const verified = await agentAuth(profile, tab, { operation: 'status' });
  if (!verified?.authenticated || !uuid.test(verified.agentId) || completed?.agentId !== verified.agentId ||
      (account && account.agentId !== verified.agentId)) {
    throw new Error('Fevertime sign-in did not establish the expected agent session.');
  }
  const bound = await createPrivate(accountPath, { agentId: verified.agentId });
  if (bound.agentId !== verified.agentId) throw new Error('The local identity belongs to another Fevertime agent.');
  return { authenticated: true, agentId: verified.agentId, created: completed.created === true, nextSteps: verified.nextSteps };
}

try {
  console.log(JSON.stringify(await connect(process.argv.slice(2))));
} catch (error) {
  // Known failures provide safe messages. Node's other errors may contain input data or paths.
  console.error(error instanceof Error && error.constructor === Error && !error.code
    ? error.message : 'Fevertime could not read or save its local identity.');
  process.exitCode = 1;
}
