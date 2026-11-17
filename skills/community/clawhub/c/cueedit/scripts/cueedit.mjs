#!/usr/bin/env node
// CueEdit CLI for agents. Zero dependencies, Node 18+.
// Auth: CUEEDIT_API_KEY=ce_live_… (create at https://www.cueedit.io/dashboard/settings → API keys).
// Every write is real: the agent must show the user the exact text and get a yes BEFORE calling it.

const BASE = (process.env.CUEEDIT_API_URL || 'https://www.cueedit.io/api/v1').replace(/\/$/, '');
const KEY = process.env.CUEEDIT_API_KEY;

const HELP = `cueedit <command> [args] [--flags]

Instagram
  accounts                                   connected accounts, plan, can_send
  posts [--limit 10] [--cursor C]            recent posts and reels
  comments <media_id> [--unhandled] [--keyword LINK] [--all-pages] [--limit 50]
  reply <comment_id> --text "…"              public reply (Pro)
  dm <comment_id> --text "…" [--force]       private reply DM to the commenter (Pro)
  scheduled [--status scheduled]             reels scheduled earlier (scheduling new reels is not supported yet)
  cancel <scheduled_post_id>                 cancel a scheduled reel
  rules                                      Auto DM rules
  rule-create --dm "…" [--keywords LINK,guide] [--any-comment] [--exact]
              [--media id1,id2] [--reply "Sent!|Check DMs"] [--require-follow]
  rule-status <rule_id> active|paused

Facebook Pages
  fb-pages
  fb-posts [--limit 10]
  fb-comments <post_id> [--unhandled] [--keyword LINK] [--all-pages]
  fb-reply <comment_id> --text "…"
  fb-dm <comment_id> --text "…" [--force]

Global: --account <id> (Instagram, needed when several are connected), --page <id> (Facebook)
Output is JSON. Exit code 1 on any API error.`;

function parse(argv) {
  const pos = [];
  const flags = {};
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a.startsWith('--')) {
      const k = a.slice(2);
      const next = argv[i + 1];
      if (next === undefined || next.startsWith('--')) flags[k] = true;
      else { flags[k] = next; i++; }
    } else pos.push(a);
  }
  return { pos, flags };
}

async function api(method, path, { query, body } = {}) {
  if (!KEY) {
    out({ error: 'missing_api_key', message: 'Set CUEEDIT_API_KEY (create one at https://www.cueedit.io/dashboard/settings → API keys). No account? https://www.cueedit.io/signup?ref=skill' });
    process.exit(1);
  }
  const url = new URL(BASE + path);
  for (const [k, v] of Object.entries(query || {})) if (v !== undefined && v !== '' && v !== false) url.searchParams.set(k, String(v));
  const res = await fetch(url, {
    method,
    headers: { authorization: `Bearer ${KEY}`, 'content-type': 'application/json', 'user-agent': 'cueedit-agent-skill/1.0' },
    body: body === undefined ? undefined : JSON.stringify(body),
  });
  const data = await res.json().catch(() => ({ error: 'bad_response', status: res.status }));
  return { ok: res.ok, status: res.status, data };
}

function out(x) { process.stdout.write(JSON.stringify(x, null, 2) + '\n'); }
function need(v, name) { if (!v || v === true) { out({ error: 'missing_argument', argument: name }); process.exit(1); } return v; }
const list = (v) => (typeof v === 'string' ? v.split(',').map((s) => s.trim()).filter(Boolean) : undefined);

async function allComments(path, query, keyword, allPages) {
  const comments = [];
  let cursor;
  let first;
  do {
    const r = await api('GET', path, { query: { ...query, cursor } });
    if (!r.ok) return r;
    first ??= r.data;
    comments.push(...(r.data.comments || []));
    cursor = r.data.next_cursor;
  } while (allPages && cursor);
  const kw = typeof keyword === 'string' ? keyword.toLowerCase() : null;
  const filtered = kw ? comments.filter((c) => (c.text || '').toLowerCase().includes(kw)) : comments;
  return {
    ok: true,
    status: 200,
    data: {
      ...(first || {}),
      comments: filtered,
      next_cursor: allPages ? null : first?.next_cursor ?? null,
      matched: filtered.length,
      dm_eligible: filtered.filter((c) => c.dm_eligible).length,
    },
  };
}

async function main() {
  const { pos, flags } = parse(process.argv.slice(2));
  const [cmd, a1, a2] = pos;
  const account_id = typeof flags.account === 'string' ? flags.account : undefined;
  const page_id = typeof flags.page === 'string' ? flags.page : undefined;
  let r;
  switch (cmd) {
    case 'accounts': r = await api('GET', '/accounts'); break;
    case 'posts': r = await api('GET', '/media', { query: { account_id, limit: flags.limit, cursor: flags.cursor } }); break;
    case 'comments':
      r = await allComments(`/media/${need(a1, 'media_id')}/comments`, { account_id, limit: flags.limit, unhandled: flags.unhandled ? 1 : undefined }, flags.keyword, flags['all-pages']);
      break;
    case 'reply': r = await api('POST', `/comments/${need(a1, 'comment_id')}/reply`, { body: { text: need(flags.text, '--text'), account_id } }); break;
    case 'dm': r = await api('POST', `/comments/${need(a1, 'comment_id')}/dm`, { body: { text: need(flags.text, '--text'), account_id, force: flags.force ? true : undefined } }); break;
    case 'schedule':
      // The API accepts schedules, but publishing fails until CueEdit's Meta app has instagram_business_content_publish again.
      r = { ok: false, status: 501, data: { error: 'not_supported', message: 'Scheduling reels from the agent is not supported yet: scheduled reels cannot publish until a Meta publishing permission is approved. Post the reel in Instagram instead.' } };
      break;
    case 'scheduled': r = await api('GET', '/scheduled-posts', { query: { account_id, status: flags.status, from: flags.from, to: flags.to } }); break;
    case 'cancel': r = await api('DELETE', `/scheduled-posts/${need(a1, 'scheduled_post_id')}`); break;
    case 'rules': r = await api('GET', '/autodm/rules', { query: { account_id } }); break;
    case 'rule-create':
      r = await api('POST', '/autodm/rules', {
        body: {
          dm_message: need(flags.dm, '--dm'),
          keywords: list(flags.keywords),
          trigger_mode: flags['any-comment'] ? 'any' : 'keyword',
          match_mode: flags.exact ? 'exact' : 'any',
          media_ids: list(flags.media) || [],
          auto_reply_enabled: typeof flags.reply === 'string' ? true : undefined,
          comment_replies: typeof flags.reply === 'string' ? flags.reply.split('|').map((s) => s.trim()).filter(Boolean).slice(0, 3) : undefined,
          require_follow: flags['require-follow'] ? true : undefined,
          account_id,
        },
      });
      break;
    case 'rule-status': {
      const status = need(a2, 'active|paused');
      if (!['active', 'paused'].includes(status)) { out({ error: 'bad_status', allowed: ['active', 'paused'] }); process.exit(1); }
      r = await api('PATCH', `/autodm/rules/${need(a1, 'rule_id')}`, { body: { status } });
      break;
    }
    case 'fb-pages': r = await api('GET', '/fb/pages'); break;
    case 'fb-posts': r = await api('GET', '/fb/posts', { query: { page_id, limit: flags.limit, cursor: flags.cursor } }); break;
    case 'fb-comments':
      r = await allComments(`/fb/posts/${need(a1, 'post_id')}/comments`, { page_id, limit: flags.limit, unhandled: flags.unhandled ? 1 : undefined }, flags.keyword, flags['all-pages']);
      break;
    case 'fb-reply': r = await api('POST', `/fb/comments/${need(a1, 'comment_id')}/reply`, { body: { text: need(flags.text, '--text'), page_id } }); break;
    case 'fb-dm': r = await api('POST', `/fb/comments/${need(a1, 'comment_id')}/dm`, { body: { text: need(flags.text, '--text'), page_id, force: flags.force ? true : undefined } }); break;
    case undefined: case 'help': case '--help': case '-h': process.stdout.write(HELP + '\n'); return;
    default: out({ error: 'unknown_command', command: cmd }); process.stdout.write(HELP + '\n'); process.exit(1);
  }
  out(r.ok ? r.data : { status: r.status, ...r.data });
  if (!r.ok) process.exit(1);
}

main().catch((e) => { out({ error: 'network_error', message: String(e?.message || e) }); process.exit(1); });
