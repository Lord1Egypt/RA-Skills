# garmin-sync-cn-to-global

Sync activities from **Garmin China** (garmin.cn) to **Garmin Global/International** (garmin.com).

## Usage

```bash
# Install dependencies
pip install garth

# Set credentials (once, stored in ~/.config/garmin-sync/credentials.json)
garmin-sync set-credentials --email your_email --password your_password

# Sync new activities from CN to Global
garmin-sync sync --new-only
```

## Options

- `--new-only` - Only sync records newer than last sync time (recommended for cron jobs)

## Behavior

- **Silent when no new activities**: If there are no activities to sync (and no failed retries), the script exits silently with no output. This is useful for cron jobs where you only want to be notified when there's actual work to do.
- **English output**: All output is in English for consistency.

## Requirements

- Python 3.x
- garth library (`pip install garth`)

## Notes

- One-way sync: CN → Global (not bidirectional)
- Uses startTimeLocal + distance to detect duplicates (activity IDs differ between servers)
- Skips conflicts automatically
- Same email/password works for both Garmin CN and Garmin Global accounts

## Security Considerations

- Credentials are stored in plaintext at `~/.config/garmin-sync/credentials.json`
- Set restrictive file permissions after first run: `chmod 600 ~/.config/garmin-sync/credentials.json`
- Consider using a dedicated/sandbox account for testing
- Review the code before running with your primary credentials
