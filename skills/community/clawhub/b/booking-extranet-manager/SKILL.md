---
name: Booking.com Extranet Manager
description: Manage Booking.com properties — download reservations, list/reply to guest messages, update rates. Wraps a Python CLI that automates the Booking.com extranet via real Chrome.
version: 1.1.0
tags:
  - booking
  - hospitality
  - reservations
  - property-management
  - automation
author: matsei-ruka
source: https://github.com/matsei-ruka/booking-extranet-bot
credentials:
  - name: BOOKING_USERNAME
    description: Booking.com partner extranet login name
    required: true
  - name: BOOKING_PASSWORD
    description: Booking.com partner extranet password
    required: true
  - name: PULSE_TOTP_SECRET
    description: Optional TOTP secret for automated 2FA (if not using SMS)
    required: false
env:
  - name: BOT_DIR
    description: Absolute path to the booking-extranet-bot directory
    required: true
  - name: BOOKING_HOTEL_ID
    description: Default property hotel ID (optional, used when --hotel-id is omitted)
    required: false
scope:
  - browser_automation: Uses Google Chrome via remote debugging (CDP on localhost:9222)
  - local_storage: Persists browser session in .chrome-data/ directory to avoid repeated login/2FA
  - network: Connects only to admin.booking.com and account.booking.com
  - filesystem: Reads .env for credentials, writes Excel files to ./downloads/
---

# Booking.com Extranet Manager

Automate Booking.com property management through a Python CLI tool. Uses your locally installed Google Chrome (not a headless browser) to interact with the Booking.com partner extranet, avoiding bot detection.

## Security Notes

- **Credentials** are stored locally in a `.env` file in the bot directory — never transmitted elsewhere.
- **Browser session** is persisted in `.chrome-data/` so login + SMS 2FA only happens once. Delete this directory to clear the session.
- **Chrome remote debugging** runs on `localhost:9222` only — not exposed to the network.
- The bot connects exclusively to `admin.booking.com` and `account.booking.com`.

## Prerequisites

The CLI tool must be installed and configured on the host machine:

```bash
git clone https://github.com/matsei-ruka/booking-extranet-bot.git
cd booking-extranet-bot
python3 -m venv venv
source venv/bin/activate   # Linux/macOS
pip install -r requirements.txt
```

Then create a `.env` file with your credentials:

```
BOOKING_USERNAME=your_login_name
BOOKING_PASSWORD=your_password
BOOKING_HOTEL_ID=your_default_hotel_id  # optional
```

Google Chrome must be installed on the host machine.

## Environment

- `BOT_DIR`: Absolute path to the booking-extranet-bot directory
- Python venv at `$BOT_DIR/venv/bin/python3`
- CLI entry point: `$BOT_DIR/cli.py`

All commands output JSON to stdout. Logs go to stderr.

## Available Commands

### List Properties

Get all properties with hotel IDs and unread message counts.

```bash
cd $BOT_DIR && source venv/bin/activate && python3 cli.py list-properties
```

Returns:
```json
{
  "status": "success",
  "action": "list-properties",
  "count": 3,
  "properties": [
    {"hotel_id": "10353912", "name": "Property Name", "unread_messages": 4}
  ]
}
```

### Download Reservations

Download reservations for a date range. Use `--json` to get data directly, or omit it to save an Excel file.

```bash
# As JSON (for processing)
cd $BOT_DIR && source venv/bin/activate && python3 cli.py download-reservations --start 2026-03-01 --end 2026-09-30 --json

# As Excel file
cd $BOT_DIR && source venv/bin/activate && python3 cli.py download-reservations --start 2026-03-01 --end 2026-09-30
```

Options:
- `--start YYYY-MM-DD` (required): Start date
- `--end YYYY-MM-DD` (required): End date
- `--date-type`: `arrival` (default), `departure`, or `booking`
- `--json`: Return data as JSON instead of Excel
- `--output-dir`: Directory for Excel file (default: `./downloads`)

### List Messages

List guest messages for a property. Defaults to unanswered.

```bash
cd $BOT_DIR && source venv/bin/activate && python3 cli.py list-messages --hotel-id 10353912
```

Options:
- `--hotel-id` (required): Property hotel ID from list-properties
- `--filter`: `unanswered` (default), `sent`, or `all`

### Read Message

Open and read a specific conversation with reservation details.

```bash
cd $BOT_DIR && source venv/bin/activate && python3 cli.py read-message --hotel-id 10353912 --index 0
```

Options:
- `--hotel-id` (required): Property hotel ID
- `--index` (required): Message index from list-messages (0-based)

### Send Message

Reply to a guest conversation. Always use list-messages first to get the correct index.

```bash
cd $BOT_DIR && source venv/bin/activate && python3 cli.py send-message --hotel-id 10353912 --index 0 --message "Thank you for your message"
```

Options:
- `--hotel-id` (required): Property hotel ID
- `--index` (required): Message index from list-messages (0-based)
- `--message` (required): Reply text

### Update Rates

Update room rates from the CSV pricing file.

```bash
cd $BOT_DIR && source venv/bin/activate && python3 cli.py update-rates
cd $BOT_DIR && source venv/bin/activate && python3 cli.py update-rates --hotel-id 13616005
```

## Typical Workflow

1. **List properties** to get hotel IDs and see which have unread messages
2. **List messages** for properties with unread messages
3. **Read** each conversation to understand the guest's request
4. **Send replies** as appropriate
5. **Download reservations** periodically to track bookings

## First Run

On first run, Chrome opens and you must complete the login (including SMS 2FA). Subsequent runs reuse the session — no login needed until the session expires.
