#!/usr/bin/env node
// Free Image to Video (https://freeimagetovideo.ai) from the command line, for agents. Node 18+, no dependencies.
//
//   node fitv.mjs credits
//   node fitv.mjs submit "<prompt>" [--image <https url>] [--duration 4|5|6|8|10|15] [--resolution 480p|768p] [--aspect 16:9|9:16|1:1]
//   node fitv.mjs status <run id>
//   node fitv.mjs wait <run id> [--timeout <minutes, default 30>]
//
// Reads FREEIMAGETOVIDEO_API_KEY. Prints one JSON object on stdout; exits 1 on any refusal,
// with {"error": kind, "message": ...} where kind is auth | plan | quota | busy | rejected | generation | timeout | api.
const BASE = (process.env.FREEIMAGETOVIDEO_BASE_URL || 'https://freeimagetovideo.ai').replace(/\/$/, '');
const KEYS = 'https://freeimagetovideo.ai/settings/apikeys';

const out = (o) => console.log(JSON.stringify(o, null, 2));
function fail(kind, message, extra = {}) {
  out({ error: kind, message, ...extra });
  process.exit(1);
}

function kindOf(status, env) {
  const msg = env?.message || '';
  const reason = env?.data?.reason;
  if (status === 401) return 'auth';
  if (env?.code === -2 || env?.code === -3) return 'rejected';
  if (reason === 'insufficient_credits') return 'quota';
  if (reason === 'plan_required') return 'plan';
  if (reason === 'concurrency') return 'busy';
  if (/no auth/i.test(msg)) return 'auth';
  return 'api';
}

async function post(path, body) {
  const key = process.env.FREEIMAGETOVIDEO_API_KEY?.trim();
  if (!key) fail('auth', `FREEIMAGETOVIDEO_API_KEY is not set. Create a key at ${KEYS}`);
  let res;
  try {
    res = await fetch(BASE + path, {
      method: 'POST',
      headers: { 'content-type': 'application/json', authorization: `Bearer ${key}`, 'user-agent': 'freeimagetovideo-skill/0.1.0' },
      body: JSON.stringify(body ?? {}),
    });
  } catch (e) {
    fail('api', `could not reach freeimagetovideo.ai: ${e.message}`);
  }
  let env = {};
  try {
    env = JSON.parse((await res.text()) || '{}');
  } catch {
    fail(res.status === 401 ? 'auth' : 'api', `non-JSON response (HTTP ${res.status})`);
  }
  // Success is HTTP < 400 AND code 0: refusals often come back as HTTP 200 with a non-zero code.
  if (res.status < 400 && env.code === 0) return env.data;
  fail(kindOf(res.status, env), env.message || `request failed (HTTP ${res.status})`, { http: res.status, reason: env.data?.reason });
}

function flags(argv) {
  const f = { _: [] };
  for (let i = 0; i < argv.length; i++) {
    if (argv[i].startsWith('--')) f[argv[i].slice(2)] = argv[++i];
    else f._.push(argv[i]);
  }
  return f;
}

const [cmd, ...rest] = process.argv.slice(2);
const f = flags(rest);

if (cmd === 'credits') {
  const d = await post('/api/user/get-user-credits');
  out({ remainingCredits: d?.remainingCredits ?? 0 });
} else if (cmd === 'submit') {
  const prompt = f._.join(' ').trim();
  if (!prompt) fail('api', 'a prompt is required');
  const options = { sound: true };
  if (f.duration) options.duration = Number(f.duration);
  if (f.resolution) options.resolution = f.resolution;
  if (f.aspect) options.aspect_ratio = f.aspect;
  if (f.image) options.image_input = [f.image];
  const d = await post('/api/ai/generate', {
    provider: 'auto', mediaType: 'video', model: 'minimax-h3',
    scene: f.image ? 'image-to-video' : 'text-to-video', prompt, options,
  });
  if (!d?.id) fail('api', 'accepted but no run id returned');
  out({ id: String(d.id), status: d.status ?? 'pending' });
} else if (cmd === 'status' || cmd === 'wait') {
  const id = f._[0];
  if (!id) fail('api', 'a run id is required');
  const deadline = Date.now() + Number(f.timeout || 30) * 60_000;
  for (;;) {
    const t = await post('/api/ai/query', { taskId: id });
    const done = ['success', 'failed', 'canceled'].includes(t?.status);
    if (cmd === 'status' || done) {
      if (t?.status === 'failed' || t?.status === 'canceled') {
        fail('generation', t.errorMessage || `run ${t.status}`, { id, status: t.status, failureKind: t.failureKind });
      }
      out({ id, status: t?.status, video: t?.videos?.[0] ?? null, queued: t?.queued ?? false, queueEta: t?.queueEta ?? null });
      break;
    }
    if (Date.now() + 10_000 > deadline) fail('timeout', `run ${id} is still generating; check it later with: status ${id}`, { id });
    await new Promise((r) => setTimeout(r, 10_000));
  }
} else {
  console.error('usage: fitv.mjs credits | submit "<prompt>" [--image url] [--duration n] [--resolution 480p|768p] [--aspect 16:9|9:16|1:1] | status <id> | wait <id>');
  process.exit(2);
}
