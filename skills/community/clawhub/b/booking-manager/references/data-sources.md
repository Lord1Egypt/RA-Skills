# Data Source Connection Patterns

**Important:** All credentials (tokens, passwords, API keys) must be stored as
environment variables in `openclaw.json` under `env`, not in plaintext in workspace
files.

## Turso (LibSQL / SQLite Cloud)

Query via the Turso HTTP API (`/v2/pipeline` endpoint). Authenticate with a Bearer
token from the `BOOKING_DB_TOKEN` environment variable. Send POST requests with JSON
payloads containing SQL statements.

**Always use parameterized queries** to prevent SQL injection:

```json
{
  "requests": [
    {
      "type": "execute",
      "stmt": {
        "sql": "SELECT * FROM bookings WHERE id = ?",
        "args": [{"type": "integer", "value": "1"}]
      }
    },
    {"type": "close"}
  ]
}
```

Text args: `{"type": "text", "value": "email@example.com"}`

### Schema setup (if creating from scratch)

```sql
CREATE TABLE IF NOT EXISTS bookings (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  email TEXT NOT NULL,
  phone TEXT,
  service TEXT NOT NULL,
  appointment_datetime_local TEXT NOT NULL,
  appointment_datetime_utc TEXT NOT NULL,
  created_at TEXT
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_bookings_email_utc
  ON bookings(email, appointment_datetime_utc);

CREATE TABLE IF NOT EXISTS booking_locks (
  email TEXT PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS booking_reminders (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  booking_id INTEGER NOT NULL,
  sent_at TEXT NOT NULL DEFAULT (datetime('now')),
  UNIQUE(booking_id)
);
```

### Reminder queries

Check for bookings needing reminders (appointments 23–25h from now, not yet reminded):

```sql
SELECT b.*
FROM bookings b
LEFT JOIN booking_reminders r ON b.id = r.booking_id
WHERE b.status = 'confirmed'
  AND b.appointment_datetime_utc > datetime('now', '+23 hours')
  AND b.appointment_datetime_utc <= datetime('now', '+25 hours')
  AND r.booking_id IS NULL;
```

Record a sent reminder:

```sql
INSERT INTO booking_reminders (booking_id) VALUES (?);
```

Clean up old reminder records (optional, run periodically):

```sql
DELETE FROM booking_reminders
WHERE sent_at < datetime('now', '-7 days');
```

Delete a reminder record when rescheduling (so a new reminder sends for the new time):

```sql
DELETE FROM booking_reminders WHERE booking_id = ?;
```

## PostgreSQL

Connect using standard PostgreSQL client tools or libraries. Credentials should be
provided via environment variables (`BOOKING_DB_HOST`, `BOOKING_DB_PORT`,
`BOOKING_DB_USER`, `BOOKING_DB_PASSWORD`, `BOOKING_DB_NAME`). Always use SSL.

Schema is identical to Turso but use `SERIAL PRIMARY KEY` instead of
`INTEGER PRIMARY KEY AUTOINCREMENT`, and `NOW()` instead of `datetime('now')`.

### Reminder queries (PostgreSQL)

```sql
-- Bookings needing reminders
SELECT b.*
FROM bookings b
LEFT JOIN booking_reminders r ON b.id = r.booking_id
WHERE b.status = 'confirmed'
  AND b.appointment_datetime_utc > (NOW() + INTERVAL '23 hours')
  AND b.appointment_datetime_utc <= (NOW() + INTERVAL '25 hours')
  AND r.booking_id IS NULL;

-- Record sent reminder
INSERT INTO booking_reminders (booking_id) VALUES ($1);

-- Delete reminder on reschedule
DELETE FROM booking_reminders WHERE booking_id = $1;
```

## Google Sheets

Use the Google Sheets API v4. Requires a service account JSON key. Store the access
token as an environment variable (`GOOGLE_SHEETS_TOKEN`).

**Reading rows:** GET request to the Sheets API values endpoint for your spreadsheet
ID and range, authenticated with the Bearer token.

**Appending rows:** POST request to the Sheets API append endpoint with a JSON body
containing the row values.

Expected columns: Name | Email | Phone | Service | Date | Time | Status | Created

### Reminder tracking (Google Sheets)

Add a `Reminder Sent` column (column I) to the bookings sheet. The agent checks this
column when polling — if empty and the appointment is 23–25h away, send the reminder
and update the cell to the current timestamp.

Alternatively, use a separate `Reminders` sheet with columns: Booking Row | Sent At.

## REST APIs (Calendly, Square, Fresha)

Each platform has its own API. General pattern:

1. Authenticate (OAuth2 or API key via environment variables)
2. Poll for new events: `GET /bookings?created_after=[timestamp]`
3. Update status: `PATCH /bookings/[id]` or `POST /bookings/[id]/confirm`
4. Extract customer details from response for email sending

Consult the specific platform's API docs for endpoints and auth.
