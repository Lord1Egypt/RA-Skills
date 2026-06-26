# SKILL: Add PI Events to Cloudflare D1

## Trigger
Use this skill when Alex says:
- "Add an event to the site"
- "Add this event to D1"
- "Update PI events"
- "Add [event name] on [date] to babenchuk.com"
- Sends a CSV or list of events to add

---

## Context
- **Database:** `mb-events` (Cloudflare D1)
- **Env vars:** load from `~/.env/.env` — use `$CF_API_TOKEN`, `$CF_ACCOUNT_ID`, `$CF_ZONE_BABENCHUK_COM`
- **Repo:** `/Users/viki/Projects/projects/marketing-bull/babenchuk-com/`
- **Live site:** https://babenchuk.com/#events

## Schema
```sql
CREATE TABLE events (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  address TEXT,
  date_start TEXT,        -- ISO format: "2026-06-06T08:00:00" or "2026-06-06"
  date_end TEXT,          -- ISO format or NULL
  location TEXT,          -- venue name/description
  rsvp_contact TEXT,      -- phone/email to RSVP
  rsvp_to TEXT,           -- person/org name to RSVP to
  register_url TEXT,      -- registration/info URL
  tags TEXT,              -- comma-separated: "PI,networking,Miller"
  created_at TEXT DEFAULT (datetime('now'))
);
```

---

## Steps

### 1. Load credentials
```bash
source ~/.env/.env
# Provides: $CF_API_TOKEN, $CF_ACCOUNT_ID
```

### 2. Build the INSERT SQL
Parse the event data Alex provides. Convert dates to ISO 8601:
- "March 14, 2026 6:00 PM (EDT)" → `2026-03-14T18:00:00`
- "June 6, 2026" → `2026-06-06`
- Date ranges: set `date_start` + `date_end`

Escape single quotes in text fields by doubling them: `O'Brien` → `O''Brien`

```sql
INSERT INTO events (name, address, date_start, date_end, location, rsvp_contact, rsvp_to, register_url, tags)
VALUES ('Event Name', NULL, '2026-06-06T08:00:00', '2026-06-06T18:00:00', 'Venue, City FL', 'contact@example.com', 'Organizer Name', 'https://register-url.com', 'PI,conference');
```

### 3. Execute against D1 (remote)
```bash
source ~/.env/.env
cd /Users/viki/Projects/projects/marketing-bull/babenchuk-com

CLOUDFLARE_API_TOKEN="$CF_API_TOKEN" \
CLOUDFLARE_ACCOUNT_ID="$CF_ACCOUNT_ID" \
npx wrangler d1 execute mb-events --remote \
  --command "INSERT INTO events (name, address, date_start, date_end, location, rsvp_contact, rsvp_to, register_url, tags) VALUES ('...', ...);"
```

For multiple events at once, use a SQL file:
```bash
CLOUDFLARE_API_TOKEN="$CF_API_TOKEN" \
CLOUDFLARE_ACCOUNT_ID="$CF_ACCOUNT_ID" \
npx wrangler d1 execute mb-events --remote --file=/tmp/new-events.sql
```

### 4. Verify insertion
```bash
CLOUDFLARE_API_TOKEN="$CF_API_TOKEN" \
CLOUDFLARE_ACCOUNT_ID="$CF_ACCOUNT_ID" \
npx wrangler d1 execute mb-events --remote \
  --command "SELECT id, name, date_start FROM events ORDER BY date_start DESC LIMIT 5;"
```

Or hit the live API:
```bash
curl -s "https://babenchuk-com.pages.dev/api/events?all=true" | jq '[.events[] | {id, name, date: .date}]'
```

### 5. No redeploy needed
D1 is a live database. Events appear on the site immediately — no wrangler deploy required.

---

## Useful Queries

**List all upcoming events:**
```bash
source ~/.env/.env
CLOUDFLARE_API_TOKEN="$CF_API_TOKEN" CLOUDFLARE_ACCOUNT_ID="$CF_ACCOUNT_ID" \
npx wrangler d1 execute mb-events --remote --command "SELECT id, name, date_start FROM events WHERE date_start >= date('now') ORDER BY date_start ASC;"
```

**Delete an event by ID:**
```bash
CLOUDFLARE_API_TOKEN="$CF_API_TOKEN" CLOUDFLARE_ACCOUNT_ID="$CF_ACCOUNT_ID" \
npx wrangler d1 execute mb-events --remote --command "DELETE FROM events WHERE id = 42;"
```

**Update an event:**
```bash
CLOUDFLARE_API_TOKEN="$CF_API_TOKEN" CLOUDFLARE_ACCOUNT_ID="$CF_ACCOUNT_ID" \
npx wrangler d1 execute mb-events --remote --command "UPDATE events SET register_url = 'https://new-url.com' WHERE id = 42;"
```

**Bulk insert from CSV:** Convert CSV to SQL INSERTs manually or ask Viki to parse and generate the SQL.

---

## Tag Conventions
Use consistent comma-separated tags (no spaces after commas):
- `PI` — general PI networking
- `Miller` — Andrew Miller events
- `PT Now` — PT Now events
- `conference` — multi-day summits
- `attorney` — attorney-focused
- `medical` — medical professional events
- `bar association` — FL bar events
- `networking` — general networking
- `MRI` — MRI/imaging provider events
- `CLE` — continuing legal education

---

## Notes
- `date_start` and `date_end` must be ISO 8601 strings — the frontend parses them with `new Date()`
- NULL is fine for optional fields (address, location, rsvp_contact, rsvp_to, register_url)
- Tags field is plain text — frontend splits on commas
- No redeploy needed after DB changes — site fetches live from D1 on every page load
