import { createHash } from 'node:crypto';
import { createReadStream, openAsBlob } from 'node:fs';
import { lstat, open, readFile, rename, stat, unlink, writeFile } from 'node:fs/promises';
import { basename, dirname, resolve } from 'node:path';
import { setTimeout as delay } from 'node:timers/promises';
import { pathToFileURL } from 'node:url';
import { x402Client, x402HTTPClient } from '@x402/core/client';
import { decodePaymentRequiredHeader, decodePaymentResponseHeader } from '@x402/core/http';
import { ExactEvmScheme } from '@x402/evm/exact/client';
import { createSIWxPayload, encodeSIWxHeader } from '@x402/extensions/sign-in-with-x';

const NETWORK = 'eip155:8453';
const USDC = '0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913';
const DEFAULT_API = 'https://api.speechischeap.com/v2';
// Payment can be confirmed in the background, which starts the 300-second upload window.
const PENDING_UPLOAD_INTERVAL_MS = 30_000;
const PENDING_UPLOAD_REPLAYS = 20;
class UsageError extends Error {}
class UploadRejected extends UsageError {}

function apiBase(env) {
  const url = new URL(env.SIC_X402_API_BASE || DEFAULT_API);
  const local = url.protocol === 'http:' && ['localhost', '127.0.0.1'].includes(url.hostname);
  if (url.username || url.password || (url.protocol !== 'https:' && !local)) {
    throw new UsageError('SIC_X402_API_BASE must use HTTPS, or localhost for tests.');
  }
  return url.toString().replace(/\/$/, '');
}

export function maxAtomic(usd) {
  if (typeof usd !== 'string' || !/^\d+(?:\.\d{1,6})?$/.test(usd)) throw new UsageError('--max-usd must be a positive USD decimal with at most six fractional digits.');
  const [whole, fraction = ''] = usd.split('.');
  const amount = BigInt(whole) * 1_000_000n + BigInt(fraction.padEnd(6, '0'));
  if (amount <= 0n) throw new UsageError('--max-usd must be positive.');
  return amount;
}

function httpUrl(value, name) {
  let url;
  try { url = new URL(value); } catch { throw new UsageError(`${name} requires an HTTP or HTTPS URL.`); }
  if (!['https:', 'http:'].includes(url.protocol) || url.username || url.password) throw new UsageError(`${name} requires a URL without credentials.`);
}

export function parseArgs(args) {
  const [command, ...rest] = args;
  if (!['transcribe', 'resume', 'status', 'cancel'].includes(command)) throw new UsageError('Usage: asr.sh --x402 transcribe|resume|status|cancel. See SKILL.md.');
  if (command === 'status' || command === 'cancel') {
    if (rest.length !== 1 || !rest[0] || rest[0].startsWith('--')) throw new UsageError(`${command} requires one job ID.`);
    return { command, jobId: rest[0] };
  }
  const parsed = { command, body: {} };
  const flags = { '--speakers': 'can_parse_speakers', '--words': 'can_parse_words', '--labels': 'can_label_audio',
    '--private': 'is_private', '--split-channel': 'is_split_channel' };
  const strings = { '--url': 'input_url', '--webhook': 'webhook_url', '--language': 'language', '--format': 'output_format', '--user-agent': 'user_agent' };
  const numbers = { '--duration': 'input_duration', '--confidence': 'minimum_confidence', '--segment-duration': 'segment_duration' };
  for (let i = 0; i < rest.length; i++) {
    const arg = rest[i];
    if (flags[arg]) { parsed.body[flags[arg]] = true; continue; }
    if (arg === '--stream') throw new UsageError('x402 supports asynchronous transcription. Remove --stream.');
    if (![...Object.keys(strings), ...Object.keys(numbers), '--state', '--file', '--max-usd'].includes(arg)) throw new UsageError('Unknown x402 option. See SKILL.md.');
    const value = rest[++i];
    if (!value || value.startsWith('--')) throw new UsageError(`Missing value for ${arg}.`);
    if (strings[arg]) parsed.body[strings[arg]] = value;
    else if (numbers[arg]) parsed.body[numbers[arg]] = Number(value);
    else parsed[arg.slice(2)] = value;
  }
  if (!parsed.state) throw new UsageError('--state is required for safe payment replay.');
  if (command === 'resume') {
    if (rest.length !== 2 || rest[0] !== '--state') throw new UsageError('resume accepts only --state; it reuses the saved request and proof.');
    return parsed;
  }
  const duration = parsed.body.input_duration;
  if (!Number.isFinite(duration) || duration < 6 || duration > 86_400) throw new UsageError('--duration must be a number from 6 to 86400 seconds.');
  if (Boolean(parsed.file) === Boolean(parsed.body.input_url)) throw new UsageError('Choose exactly one --url or --file.');
  if (parsed.body.input_url) httpUrl(parsed.body.input_url, '--url');
  if (parsed.body.webhook_url) httpUrl(parsed.body.webhook_url, '--webhook');
  if (parsed.body.minimum_confidence !== undefined && (!Number.isFinite(parsed.body.minimum_confidence) || parsed.body.minimum_confidence < 0 || parsed.body.minimum_confidence > 1)) throw new UsageError('--confidence must be from 0 to 1.');
  if (parsed.body.segment_duration !== undefined && (!Number.isInteger(parsed.body.segment_duration) || parsed.body.segment_duration < 6 || parsed.body.segment_duration > 30)) throw new UsageError('--segment-duration must be an integer from 6 to 30.');
  if (parsed.body.output_format !== undefined && !['', 'srt', 'vtt', 'webvtt'].includes(parsed.body.output_format)) throw new UsageError('--format must be srt, vtt, or webvtt; omit it for JSON.');
  maxAtomic(parsed['max-usd']);
  if (parsed.file) parsed.body.input_type = 'upload';
  return parsed;
}

async function fingerprint(file) {
  const hash = createHash('sha256');
  for await (const chunk of createReadStream(file)) hash.update(chunk);
  return hash.digest('hex');
}

async function saveState(path, value) {
  const temporary = `${path}.${process.pid}.tmp`;
  let file;
  try {
    file = await open(temporary, 'wx', 0o600);
    await file.writeFile(JSON.stringify(value));
    await file.sync();
    await file.close();
    file = undefined;
    await rename(temporary, path);
    const directory = await open(dirname(path), 'r');
    try { await directory.sync(); } finally { await directory.close(); }
  } finally {
    await file?.close();
    await unlink(temporary).catch(error => { if (error.code !== 'ENOENT') throw error; });
  }
}

async function loadState(path) {
  const info = await lstat(path);
  if (!info.isFile() || (info.mode & 0o077)) throw new UsageError('Payment state must be a regular file readable only by its owner.');
  const state = JSON.parse(await readFile(path, 'utf8'));
  if (state.version !== 1 || typeof state.body !== 'string' || !state.endpoint) throw new UsageError('Invalid payment state file.');
  return state;
}

async function signerFrom(env) {
  if (!env.SIC_X402_WALLET_MODULE) throw new UsageError('Set SIC_X402_WALLET_MODULE to your configured wallet module exporting signer.');
  const { signer } = await import(pathToFileURL(resolve(env.SIC_X402_WALLET_MODULE)).href);
  if (!signer?.address || typeof signer.signTypedData !== 'function') throw new UsageError('The wallet module must export a standard EVM signer with address and signTypedData.');
  return signer;
}

async function request(fetchImpl, url, init) {
  return fetchImpl(url, { redirect: 'error', signal: AbortSignal.timeout(60_000), ...init });
}

function visible(value) {
  if (!value || typeof value !== 'object') return value;
  if (Array.isArray(value)) return value.map(visible);
  return Object.fromEntries(Object.entries(value).filter(([key]) => !['upload_token', 'payment_signature'].includes(key)).map(([key, item]) => [key, visible(item)]));
}

async function responseJson(response) {
  if (!response.ok) throw new UsageError(`Request returned HTTP ${response.status}. Keep the state file; do not buy again to resolve an uncertain payment.`);
  return response.json();
}

async function upload(state, path, fetchImpl) {
  const ready = state.response;
  if (ready?.status !== 'READY' || !ready.upload_token || !ready.upload_url) throw new UsageError('Upload continuation is unavailable. Keep the payment state.');
  const target = new URL(ready.upload_url);
  const local = target.protocol === 'http:' && ['localhost', '127.0.0.1'].includes(target.hostname);
  if (target.username || target.password || (target.protocol !== 'https:' && !local)) throw new UsageError('Upload continuation must use HTTPS.');
  // The one-use token can replay an accepted transfer with the same input.
  if (await fingerprint(state.file) !== state.fileHash) throw new UsageError('The input file changed. Resume must use the original file.');
  const form = new FormData();
  form.append('input_file', await openAsBlob(state.file), basename(state.file));
  const response = await request(fetchImpl, ready.upload_url, { method: 'POST', body: form,
    signal: AbortSignal.timeout(3_700_000),
    headers: { 'X-SiC-Upload-Token': ready.upload_token } });
  if (!response.ok) throw new UploadRejected(`Upload returned HTTP ${response.status}. Keep the state and resume the original purchase.`);
  let accepted;
  if (response.headers.get('content-type')?.includes('text/event-stream')) {
    let buffered = '';
    const decoder = new TextDecoder();
    for await (const chunk of response.body) {
      buffered += decoder.decode(chunk, { stream: true });
      let end;
      while ((end = buffered.indexOf('\n\n')) !== -1) {
        const event = buffered.slice(0, end).split('\n').filter(line => line.startsWith('data:')).map(line => line.slice(5).trimStart()).join('\n');
        buffered = buffered.slice(end + 2);
        if (!event) continue;
        const data = JSON.parse(event);
        if (data.id) accepted = data;
        if (data.error) throw new UploadRejected('Upload did not finish. Keep the state and resume the original purchase.');
      }
    }
    if (!accepted) throw new UploadRejected('Upload response ended without a job ID. Keep the state and resume.');
  } else accepted = await response.json();
  state.response = accepted;
  await saveState(path, state);
  return accepted;
}

async function replay(state, path, fetchImpl) {
  const response = await request(fetchImpl, state.endpoint, { method: 'POST', body: state.body,
    headers: { 'Content-Type': 'application/json', ...state.paymentHeaders } });
  // An expired or removed quote and an authorization that ended unsettled took no payment.
  if (response.status === 404 || response.status === 410) throw new UsageError(`HTTP ${response.status}: the quote or its payment authorization expired, so no payment was taken. Start a new purchase with a new --state path.`);
  if (response.status === 402 && response.headers.get('PAYMENT-REQUIRED')) {
    // A fresh challenge means the service rejected this proof without taking payment.
    const { error } = decodePaymentRequiredHeader(response.headers.get('PAYMENT-REQUIRED'));
    delete state.paymentHeaders;
    await saveState(path, state);
    throw new UsageError(`Payment was declined (${error || 'no reason given'}); no payment was taken. Fix the cause, then resume to sign a new quote.`);
  }
  if (response.status === 402 && response.headers.get('PAYMENT-RESPONSE')) {
    // The service never submits a declined authorization again.
    const { success, errorReason } = decodePaymentResponseHeader(response.headers.get('PAYMENT-RESPONSE'));
    if (success === false) {
      delete state.paymentHeaders;
      await saveState(path, state);
      throw new UsageError(`Settlement was declined (${errorReason || 'no reason given'}); no payment was taken. Fix the cause, then resume to sign a new quote.`);
    }
  }
  const result = await responseJson(response);
  // CLAIMED omits the one-use token, so keep the saved READY continuation.
  if (result.status !== 'CLAIMED') {
    state.response = result;
    await saveState(path, state);
  }
  return result;
}

const paymentPending = result => !result.id && result.status === 'PENDING';
const uploadable = result => !result.id && ['READY', 'CLAIMED'].includes(result.status);

async function purchase(state, path, env, fetchImpl, suppliedSigner, pause) {
  if (state.response?.id) return state.response;
  if (!state.paymentHeaders) {
    const response = await request(fetchImpl, state.endpoint, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: state.body });
    if (response.status !== 402) {
      const wait = response.status === 429 ? ` Quote requests are rate limited; retry after ${response.headers.get('Retry-After') || 60} seconds.` : '';
      throw new UsageError(`Unpaid request returned HTTP ${response.status}; no payment was signed.${wait}`);
    }
    const signer = suppliedSigner || await signerFrom(env);
    const client = new x402Client((version, choices) => {
      const selected = choices.find(choice => version === 2 && choice.scheme === 'exact' && choice.network === NETWORK && choice.asset.toLowerCase() === USDC.toLowerCase());
      if (!selected || !/^\d+$/.test(selected.amount) || BigInt(selected.amount) <= 0n || BigInt(selected.amount) > maxAtomic(state.maxUsd)) throw new UsageError('Payment challenge exceeds --max-usd or does not offer native USDC on Base with x402 v2 exact.');
      return selected;
    }).register(NETWORK, new ExactEvmScheme(signer));
    client.setSpendControls({ maxAmountPerPayment: `$${state.maxUsd}` });
    const http = new x402HTTPClient(client);
    const required = http.getPaymentRequiredResponse(name => response.headers.get(name));
    const choice = required.accepts.find(item => required.x402Version === 2 && item.scheme === 'exact'
      && item.network === NETWORK && item.asset.toLowerCase() === USDC.toLowerCase());
    if (!choice || !/^\d+$/.test(choice.amount) || BigInt(choice.amount) <= 0n || BigInt(choice.amount) > maxAtomic(state.maxUsd)) {
      throw new UsageError('Quote exceeds --max-usd or uses an unsupported token/network. No payment was signed.');
    }
    const resource = new URL(required.resource.url);
    const endpoint = new URL(state.endpoint);
    if (resource.origin !== endpoint.origin || resource.pathname !== endpoint.pathname || !resource.searchParams.get('purchase_id')) throw new UsageError('Payment challenge is not bound to this purchase endpoint.');
    state.paymentHeaders = http.encodePaymentSignatureHeader(await http.createPaymentPayload(required));
    state.purchaseId = resource.searchParams.get('purchase_id');
    // The authorization reaches disk before the paid request can reach the server.
    await saveState(path, state);
  }
  // Every run asks the service for the purchase's current state before any upload.
  let result = await replay(state, path, fetchImpl);
  for (let replays = 0; state.file && paymentPending(result) && replays < PENDING_UPLOAD_REPLAYS; replays++) {
    await pause(PENDING_UPLOAD_INTERVAL_MS);
    result = await replay(state, path, fetchImpl);
  }
  if (!state.file || !uploadable(result)) return result;
  try { return await upload(state, path, fetchImpl); }
  catch (error) {
    if (!(error instanceof UploadRejected)) throw error;
    // A failed transfer or a missed start window ends the purchase with a full refund.
    const outcome = await replay(state, path, fetchImpl);
    if (uploadable(outcome)) throw error;
    return outcome;
  }
}

// Cancellation has no payment state, so its failures need their own advice.
function cancelFailure(status) {
  const advice = { 401: 'The challenge expired or was already used; run cancel again to sign a new one.',
    403: 'Only the wallet that paid for this job can cancel it.', 404: 'No paid x402 job has this ID.' }[status];
  return new UsageError(`Cancellation returned HTTP ${status}. ${advice || 'Retry cancel later.'}`);
}

async function cancel(jobId, env, fetchImpl, suppliedSigner) {
  const url = `${apiBase(env)}/x402/jobs/${encodeURIComponent(jobId)}`;
  const response = await request(fetchImpl, url, { method: 'DELETE' });
  if (response.status !== 402) throw cancelFailure(response.status);
  const http = new x402HTTPClient(new x402Client());
  const required = http.getPaymentRequiredResponse(name => response.headers.get(name));
  const extension = required.extensions?.['sign-in-with-x'];
  const chain = extension?.supportedChains?.find(item => item.chainId === NETWORK && item.type === 'eip191');
  if (required.accepts.length || required.resource.url !== url || !chain || extension.info.uri !== url
    || extension.info.statement !== `Cancel Speech is Cheap transcription ${jobId}`
    || !extension.info.resources?.includes(`urn:speechischeap:cancel:${jobId}`)) throw new UsageError('Invalid auth-only challenge for this job cancellation.');
  const signer = suppliedSigner || await signerFrom(env);
  if (typeof signer.signMessage !== 'function') throw new UsageError('Cancellation needs a wallet signer with standard signMessage support.');
  const proof = await createSIWxPayload({ ...extension.info, ...chain }, signer, url);
  const result = await request(fetchImpl, url, { method: 'DELETE', headers: { 'SIGN-IN-WITH-X': encodeSIWxHeader(proof) } });
  if (result.status === 409) return result.json();
  if (!result.ok) throw cancelFailure(result.status);
  return result.json();
}

export async function run(args, { env = process.env, fetchImpl = fetch, signer, pause = delay } = {}) {
  const options = parseArgs(args);
  if (options.command === 'status') {
    const response = await request(fetchImpl, `${apiBase(env)}/jobs/${encodeURIComponent(options.jobId)}`, { method: 'GET' });
    if (!response.ok) throw new UsageError(`Status returned HTTP ${response.status}.`);
    return response.headers.get('content-type')?.includes('application/json') ? response.json() : response.text();
  }
  if (options.command === 'cancel') return visible(await cancel(options.jobId, env, fetchImpl, signer));
  const path = resolve(options.state);
  let lock;
  try { lock = await open(`${path}.lock`, 'wx', 0o600); }
  catch (error) {
    if (error.code === 'EEXIST') throw new UsageError('This state is already in use. After a crashed process, remove only its stale .lock file and resume.');
    throw error;
  }
  try {
    await lock.writeFile(`${process.pid}\n`);
    let state;
    if (options.command === 'resume') state = await loadState(path);
    else {
      if (options.file && !(await stat(options.file)).isFile()) throw new UsageError('--file must name a regular local file.');
      state = { version: 1, endpoint: `${apiBase(env)}/x402/jobs/`, body: JSON.stringify(options.body), maxUsd: options['max-usd'],
        ...(options.file ? { file: resolve(options.file), fileHash: await fingerprint(options.file) } : {}) };
      try { await writeFile(path, JSON.stringify(state), { flag: 'wx', mode: 0o600 }); }
      catch (error) { if (error.code === 'EEXIST') throw new UsageError('This state already exists. Use resume, or choose a new state path for a new purchase.'); throw error; }
    }
    return visible(await purchase(state, path, env, fetchImpl, signer, pause));
  } finally { await lock.close(); await unlink(`${path}.lock`); }
}

if (process.argv[1] && import.meta.url === pathToFileURL(resolve(process.argv[1])).href) {
  try {
    const result = await run(process.argv.slice(2));
    console.log(typeof result === 'string' ? result : JSON.stringify(result));
  } catch (error) {
    console.error(error instanceof UsageError ? error.message : 'x402 request did not finish. Keep the state file and resume the same purchase; do not pay again.');
    process.exitCode = 1;
  }
}
