#!/usr/bin/env node
/**
 * Calendar Crab - Google Calendar CLI
 * Zero dependencies. Just Node.js + Google OAuth.
 *
 * Usage:
 *   node calendar-crab.js list --days=3 --max=20
 *   node calendar-crab.js create --title="Lunch" --date=2026-03-20 --time=12:00
 *   node calendar-crab.js move --date=2026-03-01 --from=19:00 --to=16:00
 *   node calendar-crab.js move --id="EVENT_ID" --to="2026-03-01T16:00:00-07:00"
 *   node calendar-crab.js delete --id="EVENT_ID"
 *   node calendar-crab.js delete --date=2026-03-01 --time=19:00
 */

const fs = require('fs');
const path = require('path');
const https = require('https');

// Resolve secrets dir: CALENDAR_CRAB_SECRETS > ~/.openclaw/secrets
const SECRETS_DIR = process.env.CALENDAR_CRAB_SECRETS
  || path.join(process.env.HOME, '.openclaw', 'secrets');
const TOKEN_FILE = path.join(SECRETS_DIR, 'google-calendar-token.json');
const OAUTH_FILE = path.join(SECRETS_DIR, 'google-calendar-oauth.json');
const CALENDAR_ID = process.env.CALENDAR_CRAB_CALENDAR || 'primary';

function loadJson(filePath) {
  return JSON.parse(fs.readFileSync(filePath, 'utf8'));
}

function requestJson(options, body = null) {
  return new Promise((resolve, reject) => {
    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', (chunk) => (data += chunk));
      res.on('end', () => {
        try {
          const parsed = data ? JSON.parse(data) : {};
          if (res.statusCode >= 400 || parsed.error) {
            return reject(new Error(JSON.stringify(parsed.error || { code: res.statusCode, data })));
          }
          resolve(parsed);
        } catch (e) {
          reject(e);
        }
      });
    });
    req.on('error', reject);
    if (body) req.write(body);
    req.end();
  });
}

async function getAccessToken() {
  const tokens = loadJson(TOKEN_FILE);
  const oauth = loadJson(OAUTH_FILE);

  const obtainedAt = new Date(tokens.obtained_at || 0).getTime();
  const expiresAt = obtainedAt + (tokens.expires_in || 0) * 1000;
  const stillValid = Date.now() < expiresAt - 60_000;

  if (tokens.access_token && stillValid) {
    return tokens.access_token;
  }

  const postData = new URLSearchParams({
    refresh_token: tokens.refresh_token,
    client_id: oauth.client_id,
    client_secret: oauth.client_secret,
    grant_type: 'refresh_token'
  }).toString();

  const refreshed = await requestJson({
    hostname: 'oauth2.googleapis.com',
    path: '/token',
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
      'Content-Length': Buffer.byteLength(postData)
    }
  }, postData);

  const newTokens = {
    ...tokens,
    access_token: refreshed.access_token,
    expires_in: refreshed.expires_in,
    obtained_at: new Date().toISOString()
  };
  fs.writeFileSync(TOKEN_FILE, JSON.stringify(newTokens, null, 2));
  return refreshed.access_token;
}

async function gcal(apiPath, method = 'GET', body = null) {
  const accessToken = await getAccessToken();
  const payload = body ? JSON.stringify(body) : null;

  return requestJson({
    hostname: 'www.googleapis.com',
    path: `/calendar/v3${apiPath}`,
    method,
    headers: {
      Authorization: `Bearer ${accessToken}`,
      ...(payload ? { 'Content-Type': 'application/json', 'Content-Length': Buffer.byteLength(payload) } : {})
    }
  }, payload);
}

function parseArgs() {
  const [,, cmd, ...rawArgs] = process.argv;
  const args = { _: cmd || 'help' };
  for (const arg of rawArgs) {
    if (arg.startsWith('--')) {
      const eq = arg.indexOf('=');
      if (eq > -1) {
        args[arg.slice(2, eq)] = arg.slice(eq + 1);
      } else {
        args[arg.slice(2)] = 'true';
      }
    }
  }
  return args;
}

// Resolve timezone: --tz flag > CALENDAR_CRAB_TZ env > system local
function resolveTz(args) {
  return args.tz || process.env.CALENDAR_CRAB_TZ || Intl.DateTimeFormat().resolvedOptions().timeZone;
}

function isoAt(dateStr, hhmm, tz) {
  const [h, m] = hhmm.split(':').map(Number);
  const dt = new Date(`${dateStr}T${String(h).padStart(2, '0')}:${String(m).padStart(2, '0')}:00`);
  return dt.toISOString();
}

function eventStartToDate(event) {
  return new Date(event.start?.dateTime || event.start?.date);
}

function formatTime(dt) {
  return new Date(dt).toLocaleString();
}

// ── Commands ──

async function listCmd(args) {
  const days = Number(args.days || 7);
  const max = Number(args.max || 20);
  const now = new Date();
  const future = new Date(now);
  future.setDate(future.getDate() + days);

  const params = new URLSearchParams({
    timeMin: now.toISOString(),
    timeMax: future.toISOString(),
    maxResults: String(max),
    orderBy: 'startTime',
    singleEvents: 'true'
  });

  const data = await gcal(`/calendars/${encodeURIComponent(CALENDAR_ID)}/events?${params}`);
  const events = data.items || [];

  if (!events.length) {
    console.log('No upcoming events');
    return;
  }

  console.log(`Upcoming (${events.length})`);
  for (const e of events) {
    const s = formatTime(eventStartToDate(e));
    console.log(`- ${s} | ${e.summary || '(no title)'} | id=${e.id}`);
  }
}

async function createCmd(args) {
  if (!args.title || !args.date || !args.time) {
    throw new Error('create requires --title="..." --date=YYYY-MM-DD --time=HH:MM [--duration=60] [--location="..."] [--attendees="a@b.com,c@d.com"] [--description="..."] [--tz=America/Los_Angeles]');
  }

  const durationMin = Number(args.duration || 60);
  const tz = resolveTz(args);
  const [h, m] = args.time.split(':').map(Number);
  const startDate = new Date(`${args.date}T${String(h).padStart(2, '0')}:${String(m).padStart(2, '0')}:00`);
  const endDate = new Date(startDate.getTime() + durationMin * 60_000);

  const body = {
    summary: args.title,
    start: { dateTime: startDate.toISOString(), timeZone: tz },
    end: { dateTime: endDate.toISOString(), timeZone: tz },
    ...(args.location ? { location: args.location } : {}),
    ...(args.description ? { description: args.description } : {}),
    ...(args.attendees ? {
      attendees: args.attendees.split(',').map(email => ({ email: email.trim() }))
    } : {})
  };

  const created = await gcal(
    `/calendars/${encodeURIComponent(CALENDAR_ID)}/events?sendUpdates=all`,
    'POST',
    body
  );

  console.log('Event created');
  console.log(`- Title: ${created.summary}`);
  console.log(`- Time: ${formatTime(created.start.dateTime)} -> ${formatTime(created.end.dateTime)}`);
  console.log(`- Location: ${created.location || 'none'}`);
  console.log(`- Attendees: ${(created.attendees || []).map(a => a.email).join(', ') || 'none'}`);
  console.log(`- Link: ${created.htmlLink || 'none'}`);
}

async function findEventByTime(date, time) {
  const dayStart = `${date}T00:00:00`;
  const dayEnd = `${date}T23:59:59`;
  const params = new URLSearchParams({
    timeMin: new Date(dayStart).toISOString(),
    timeMax: new Date(dayEnd).toISOString(),
    singleEvents: 'true',
    orderBy: 'startTime',
    maxResults: '50'
  });
  const data = await gcal(`/calendars/${encodeURIComponent(CALENDAR_ID)}/events?${params}`);
  const items = data.items || [];

  const target = items.find((e) => {
    const d = eventStartToDate(e);
    const hh = String(d.getHours()).padStart(2, '0');
    const mm = String(d.getMinutes()).padStart(2, '0');
    return `${hh}:${mm}` === time;
  });

  if (!target) {
    throw new Error(`No event found on ${date} at ${time}`);
  }
  return target;
}

async function moveCmd(args) {
  const tz = resolveTz(args);
  let event;

  if (args.id) {
    event = await gcal(`/calendars/${encodeURIComponent(CALENDAR_ID)}/events/${encodeURIComponent(args.id)}`);
  } else {
    if (!args.date || !args.from || !args.to) {
      throw new Error('move by time requires --date=YYYY-MM-DD --from=HH:MM --to=HH:MM');
    }
    event = await findEventByTime(args.date, args.from);
  }

  const oldStart = new Date(event.start.dateTime);
  const oldEnd = new Date(event.end.dateTime);
  const durationMs = oldEnd.getTime() - oldStart.getTime();

  let newStart;
  if (args.to && /^\d{2}:\d{2}$/.test(args.to) && args.date) {
    newStart = new Date(isoAt(args.date, args.to, tz));
  } else if (args.to && args.to.includes('T')) {
    newStart = new Date(args.to);
  } else {
    throw new Error('move requires --to=HH:MM with --date, or --to=ISO_DATETIME');
  }

  const newEnd = new Date(newStart.getTime() + durationMs);

  const updated = await gcal(
    `/calendars/${encodeURIComponent(CALENDAR_ID)}/events/${encodeURIComponent(event.id)}?sendUpdates=all`,
    'PATCH',
    {
      start: { dateTime: newStart.toISOString(), timeZone: tz },
      end: { dateTime: newEnd.toISOString(), timeZone: tz }
    }
  );

  console.log('Event moved');
  console.log(`- Title: ${updated.summary}`);
  console.log(`- New time: ${formatTime(updated.start.dateTime)} -> ${formatTime(updated.end.dateTime)}`);
  console.log(`- Attendees: ${(updated.attendees || []).map(a => a.email).join(', ') || 'none'}`);
}

async function deleteCmd(args) {
  let event;

  if (args.id) {
    event = await gcal(`/calendars/${encodeURIComponent(CALENDAR_ID)}/events/${encodeURIComponent(args.id)}`);
  } else if (args.date && args.time) {
    event = await findEventByTime(args.date, args.time);
  } else {
    throw new Error('delete requires --id=EVENT_ID or --date=YYYY-MM-DD --time=HH:MM');
  }

  await gcal(
    `/calendars/${encodeURIComponent(CALENDAR_ID)}/events/${encodeURIComponent(event.id)}?sendUpdates=all`,
    'DELETE'
  );

  console.log('Event deleted');
  console.log(`- Title: ${event.summary}`);
  console.log(`- Was: ${formatTime(event.start.dateTime)} -> ${formatTime(event.end.dateTime)}`);
}

function help() {
  console.log(`Calendar Crab - Google Calendar CLI

Commands:
  list   --days=7 --max=20
  create --title="..." --date=YYYY-MM-DD --time=HH:MM [--duration=60] [--location="..."] [--attendees="a@b,c@d"] [--description="..."] [--tz=America/Los_Angeles]
  move   --date=YYYY-MM-DD --from=HH:MM --to=HH:MM [--tz=...]
  move   --id=EVENT_ID --to=2026-03-01T16:00:00-07:00
  delete --id=EVENT_ID
  delete --date=YYYY-MM-DD --time=HH:MM

Environment variables:
  CALENDAR_CRAB_SECRETS  Path to secrets dir (default: ~/.openclaw/secrets)
  CALENDAR_CRAB_TZ       Default timezone (default: system local)
  CALENDAR_CRAB_CALENDAR Calendar ID (default: primary)`);
}

async function main() {
  const args = parseArgs();
  switch (args._) {
    case 'list':   return listCmd(args);
    case 'create': return createCmd(args);
    case 'move':   return moveCmd(args);
    case 'delete': return deleteCmd(args);
    default:       return help();
  }
}

main().catch((e) => {
  console.error('Error:', e.message);
  process.exit(1);
});
