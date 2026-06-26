# Delivery Notifier

Fetches delivery notifications from Gmail and sends formatted WhatsApp alerts for personal deliveries.

## How It Works

- **Scans** your Gmail inbox for delivery-related emails
- **Identifies** couriers (AliExpress, DHL, FAN Courier, KROM, Temu, etc.)
- **Extracts** tracking numbers when available
- **Filters** out marketing emails from AliExpress, Temu, etc.
- **Sends** WhatsApp notifications for personal deliveries
- **Tracks** sent notifications to avoid duplicates

## Configuration

Edit `/home/o0o/.openclaw/skills/delivery-notifier/scripts/delivery_notifier.py` to customize:

- **EMAIL settings:** Your Gmail credentials
- **WHATSAPP target:** `+40746085791` (Stefan)
- **EXCLUDED_SENDERS:** Marketing couriers to filter (AliExpress, Temu, etc.)

## Usage

Run manually:
```bash
python3 /home/o0o/.openclaw/skills/delivery-notifier/scripts/delivery_notifier.py
```

Or set up as a cron job:
```bash
# Every 15 minutes
*/15 * * * * /usr/bin/python3 /home/o0o/.openclaw/skills/delivery-notifier/scripts/delivery_notifier.py
```

## Output Format

```
📦 LIVRARE NOUĂ

🏢 Curier: FAN Courier
📋 Trimitere: #PO-167
📄 Mesaj: FAN Courier - Comanda dumneavoastră a fost expediată

---
Generat automat de OpenClaw Delivery Notifier
```

## State Management

- Notifications are stored in `/home/o0o/.openclaw/skills/delivery-notifier/scripts/state.json`
- Keeps track of sent notifications to avoid duplicates
- Old notifications expire automatically (keeps last 100)