---
name: bambuddy
description: >
  Full integration with a self-hosted Bambuddy instance — the print archive and
  management system for Bambu Lab 3D printers. Covers printers, real-time status,
  print archives, print queue, filament/spool tracking, AMS, camera snapshots,
  k-profiles, projects, notifications, Spoolman sync, smart plugs, settings,
  system info, and more. Requires a running Bambuddy server and an API key.
metadata:
  openclaw:
    requires:
      env:
        - BAMBUDDY_URL
        - BAMBUDDY_API_KEY
      bins:
        - curl
        - jq
    primaryEnv: BAMBUDDY_API_KEY
    config:
      requiredEnv:
        - BAMBUDDY_URL
        - BAMBUDDY_API_KEY
      example: |
        skills.entries.bambuddy = {
          enabled = true;
          env = {
            BAMBUDDY_URL = "http://localhost:8000";
            BAMBUDDY_API_KEY = "bb_your_key_here";
          };
        };
---

# Bambuddy Skill

You have full access to the Bambuddy REST API. Use `curl` to make all requests.
Never invent endpoint paths — use exactly the routes documented below.

## Authentication & Base URL

Every request must include the API key header. The base URL comes from the
`BAMBUDDY_URL` environment variable (no trailing slash).

```bash
# Convenience alias — reuse this pattern for every call
BB_URL="${BAMBUDDY_URL}/api/v1"
BB_AUTH="X-API-Key: ${BAMBUDDY_API_KEY}"

# GET example
curl -s -H "$BB_AUTH" "$BB_URL/system/info" | jq .

# POST example
curl -s -X POST -H "$BB_AUTH" -H "Content-Type: application/json" \
  -d '{"key":"value"}' "$BB_URL/some/endpoint" | jq .

# PATCH example
curl -s -X PATCH -H "$BB_AUTH" -H "Content-Type: application/json" \
  -d '{"key":"value"}' "$BB_URL/some/endpoint" | jq .

# DELETE example
curl -s -X DELETE -H "$BB_AUTH" "$BB_URL/some/endpoint"
```

Always pipe JSON responses through `jq .` for readability unless you need raw output.
For binary responses (camera snapshots, thumbnails), omit `jq` and save to a file.

---

## API Categories & Endpoints

### 1. System

```bash
# System info (version, paths, database stats)
curl -s -H "$BB_AUTH" "$BB_URL/system/info" | jq .
```

---

### 2. Auth / Users / Groups

```bash
# Current user info
curl -s -H "$BB_AUTH" "$BB_URL/auth/me" | jq .

# Auth status (whether auth is enabled)
curl -s -H "$BB_AUTH" "$BB_URL/auth/status" | jq .

# List users
curl -s -H "$BB_AUTH" "$BB_URL/users" | jq .

# Get a specific user
curl -s -H "$BB_AUTH" "$BB_URL/users/{user_id}" | jq .

# User item count
curl -s -H "$BB_AUTH" "$BB_URL/users/{user_id}/items-count" | jq .

# List groups
curl -s -H "$BB_AUTH" "$BB_URL/groups" | jq .

# Available permissions
curl -s -H "$BB_AUTH" "$BB_URL/groups/permissions" | jq .

# Get a specific group
curl -s -H "$BB_AUTH" "$BB_URL/groups/{group_id}" | jq .
```

---

### 3. API Keys

```bash
# List all API keys
curl -s -H "$BB_AUTH" "$BB_URL/api-keys/" | jq .

# Create a new API key
curl -s -X POST -H "$BB_AUTH" -H "Content-Type: application/json" \
  -d '{
    "name": "my-key",
    "can_queue": true,
    "can_control_printer": true,
    "can_read_status": true,
    "printer_ids": null,
    "expires_at": null
  }' "$BB_URL/api-keys/" | jq .

# Get a specific API key
curl -s -H "$BB_AUTH" "$BB_URL/api-keys/{key_id}" | jq .

# Update an API key
curl -s -X PATCH -H "$BB_AUTH" -H "Content-Type: application/json" \
  -d '{"name": "updated-name", "enabled": false}' \
  "$BB_URL/api-keys/{key_id}" | jq .

# Delete an API key
curl -s -X DELETE -H "$BB_AUTH" "$BB_URL/api-keys/{key_id}"
```

---

### 4. Printers

```bash
# List all printers
curl -s -H "$BB_AUTH" "$BB_URL/printers/" | jq .

# Get a specific printer
curl -s -H "$BB_AUTH" "$BB_URL/printers/{printer_id}" | jq .

# Real-time status (temps, progress, stage, AMS, speeds, etc.)
curl -s -H "$BB_AUTH" "$BB_URL/printers/{printer_id}/status" | jq .

# Current print user
curl -s -H "$BB_AUTH" "$BB_URL/printers/{printer_id}/current-print-user" | jq .

# Printer cover image (binary PNG — save to file)
curl -s -H "$BB_AUTH" "$BB_URL/printers/{printer_id}/cover" -o cover.png

# Files on printer SD/storage
curl -s -H "$BB_AUTH" "$BB_URL/printers/{printer_id}/files" | jq .

# Printer storage info
curl -s -H "$BB_AUTH" "$BB_URL/printers/{printer_id}/storage" | jq .

# MQTT debug logging
curl -s -H "$BB_AUTH" "$BB_URL/printers/{printer_id}/logging" | jq .

# AMS slot presets
curl -s -H "$BB_AUTH" "$BB_URL/printers/{printer_id}/slot-presets" | jq .

# Specific slot preset
curl -s -H "$BB_AUTH" \
  "$BB_URL/printers/{printer_id}/slot-presets/{ams_id}/{slot_id}" | jq .

# Print objects (current job plate objects)
curl -s -H "$BB_AUTH" "$BB_URL/printers/{printer_id}/print/objects" | jq .

# Runtime debug info
curl -s -H "$BB_AUTH" "$BB_URL/printers/{printer_id}/runtime-debug" | jq .

# Camera status
curl -s -H "$BB_AUTH" "$BB_URL/printers/{printer_id}/camera/status" | jq .

# USB cameras
curl -s -H "$BB_AUTH" "$BB_URL/printers/usb-cameras" | jq .

# Update printer (name, IP, access code, etc.)
curl -s -X PATCH -H "$BB_AUTH" -H "Content-Type: application/json" \
  -d '{"name": "New Name"}' "$BB_URL/printers/{printer_id}" | jq .

# Add a printer
curl -s -X POST -H "$BB_AUTH" -H "Content-Type: application/json" \
  -d '{
    "name": "My X1C",
    "ip": "192.168.1.100",
    "access_code": "12345678",
    "serial": "01S00A000000000"
  }' "$BB_URL/printers/" | jq .

# Delete a printer
curl -s -X DELETE -H "$BB_AUTH" "$BB_URL/printers/{printer_id}"

# Printer control (pause, resume, stop)
curl -s -X POST -H "$BB_AUTH" -H "Content-Type: application/json" \
  -d '{"command": "pause"}' "$BB_URL/printers/{printer_id}/control"
# command options: "pause" | "resume" | "stop"
```

---

### 5. Archives

```bash
# List archives (supports filtering/pagination)
curl -s -H "$BB_AUTH" "$BB_URL/archives/" | jq .

# With filters
curl -s -H "$BB_AUTH" \
  "$BB_URL/archives/?page=1&page_size=20&search=benchy&printer_id=1" | jq .

# Get a specific archive
curl -s -H "$BB_AUTH" "$BB_URL/archives/{archive_id}" | jq .

# Archive stats summary
curl -s -H "$BB_AUTH" "$BB_URL/archives/stats" | jq .

# Update archive metadata
curl -s -X PATCH -H "$BB_AUTH" -H "Content-Type: application/json" \
  -d '{"name": "Updated Name", "rating": 5, "notes": "Great print"}' \
  "$BB_URL/archives/{archive_id}" | jq .

# Delete an archive
curl -s -X DELETE -H "$BB_AUTH" "$BB_URL/archives/{archive_id}"

# Reprint an archive
curl -s -X POST -H "$BB_AUTH" -H "Content-Type: application/json" \
  -d '{"printer_id": 1, "ams_mapping": []}' \
  "$BB_URL/archives/{archive_id}/reprint" | jq .

# Download archive 3MF file
curl -s -H "$BB_AUTH" "$BB_URL/archives/{archive_id}/download" \
  -o archive.3mf

# Export archives as CSV/JSON
curl -s -H "$BB_AUTH" "$BB_URL/archives/export" -o archives_export.csv
```

---

### 6. Print Queue

```bash
# List queue items
curl -s -H "$BB_AUTH" "$BB_URL/print-queue/" | jq .

# Add to queue
curl -s -X POST -H "$BB_AUTH" -H "Content-Type: application/json" \
  -d '{
    "archive_id": 42,
    "printer_id": 1,
    "priority": 0,
    "ams_mapping": []
  }' "$BB_URL/print-queue/" | jq .

# Get a queue item
curl -s -H "$BB_AUTH" "$BB_URL/print-queue/{item_id}" | jq .

# Update a queue item (priority, printer, etc.)
curl -s -X PATCH -H "$BB_AUTH" -H "Content-Type: application/json" \
  -d '{"priority": 10}' "$BB_URL/print-queue/{item_id}" | jq .

# Remove from queue
curl -s -X DELETE -H "$BB_AUTH" "$BB_URL/print-queue/{item_id}"

# Start / process next queue item
curl -s -X POST -H "$BB_AUTH" "$BB_URL/print-queue/{item_id}/start" | jq .
```

---

### 7. Projects

```bash
# List projects
curl -s -H "$BB_AUTH" "$BB_URL/projects/" | jq .

# Get a project
curl -s -H "$BB_AUTH" "$BB_URL/projects/{project_id}" | jq .

# Create a project
curl -s -X POST -H "$BB_AUTH" -H "Content-Type: application/json" \
  -d '{"name": "My Project", "description": ""}' \
  "$BB_URL/projects/" | jq .

# Update a project
curl -s -X PATCH -H "$BB_AUTH" -H "Content-Type: application/json" \
  -d '{"name": "Renamed Project"}' "$BB_URL/projects/{project_id}" | jq .

# Delete a project
curl -s -X DELETE -H "$BB_AUTH" "$BB_URL/projects/{project_id}"

# Add an archive to a project
curl -s -X POST -H "$BB_AUTH" -H "Content-Type: application/json" \
  -d '{"archive_id": 42}' "$BB_URL/projects/{project_id}/archives" | jq .
```

---

### 8. Filaments / AMS

```bash
# List all filament profiles
curl -s -H "$BB_AUTH" "$BB_URL/filaments/" | jq .

# Get a specific filament
curl -s -H "$BB_AUTH" "$BB_URL/filaments/{filament_id}" | jq .

# Create a filament profile
curl -s -X POST -H "$BB_AUTH" -H "Content-Type: application/json" \
  -d '{
    "name": "PolyTerra PLA Teal",
    "type": "PLA",
    "color": "#00BCD4",
    "brand": "Polymaker",
    "nozzle_temp_min": 190,
    "nozzle_temp_max": 230,
    "bed_temp": 35
  }' "$BB_URL/filaments/" | jq .

# Update a filament profile
curl -s -X PATCH -H "$BB_AUTH" -H "Content-Type: application/json" \
  -d '{"color": "#FF5722"}' "$BB_URL/filaments/{filament_id}" | jq .

# Delete a filament profile
curl -s -X DELETE -H "$BB_AUTH" "$BB_URL/filaments/{filament_id}"

# AMS history (which spools have been used)
curl -s -H "$BB_AUTH" "$BB_URL/ams-history/" | jq .
```

---

### 9. K-Profiles (Pressure Advance)

```bash
# List k-profiles
curl -s -H "$BB_AUTH" "$BB_URL/kprofiles/" | jq .

# Get a specific k-profile
curl -s -H "$BB_AUTH" "$BB_URL/kprofiles/{profile_id}" | jq .

# Create a k-profile
curl -s -X POST -H "$BB_AUTH" -H "Content-Type: application/json" \
  -d '{
    "name": "PLA 0.4mm",
    "k_value": 0.018,
    "filament_type": "PLA",
    "nozzle_diameter": 0.4
  }' "$BB_URL/kprofiles/" | jq .

# Update a k-profile
curl -s -X PATCH -H "$BB_AUTH" -H "Content-Type: application/json" \
  -d '{"k_value": 0.022}' "$BB_URL/kprofiles/{profile_id}" | jq .

# Delete a k-profile
curl -s -X DELETE -H "$BB_AUTH" "$BB_URL/kprofiles/{profile_id}"
```

---

### 10. Camera

```bash
# Camera status for a printer
curl -s -H "$BB_AUTH" "$BB_URL/printers/{printer_id}/camera/status" | jq .

# Snapshot (binary JPEG — save to file)
curl -s -H "$BB_AUTH" \
  "$BB_URL/printers/{printer_id}/camera/snapshot" -o snapshot.jpg

# Stream URL (for RTSP/MJPEG clients)
curl -s -H "$BB_AUTH" "$BB_URL/camera/" | jq .
```

---

### 11. Settings

```bash
# Get all settings
curl -s -H "$BB_AUTH" "$BB_URL/settings/" | jq .

# Update settings (PATCH supported)
curl -s -X PATCH -H "$BB_AUTH" -H "Content-Type: application/json" \
  -d '{"archive_dir": "/data/archive", "auto_archive": true}' \
  "$BB_URL/settings/" | jq .

# Check if ffmpeg is available
curl -s -H "$BB_AUTH" "$BB_URL/settings/check-ffmpeg" | jq .

# Spoolman connection settings
curl -s -H "$BB_AUTH" "$BB_URL/settings/spoolman" | jq .

# Backup settings
curl -s -H "$BB_AUTH" "$BB_URL/settings/backup" | jq .

# MQTT status
curl -s -H "$BB_AUTH" "$BB_URL/settings/mqtt/status" | jq .

# Virtual printer models list
curl -s -H "$BB_AUTH" "$BB_URL/settings/virtual-printer/models" | jq .

# Virtual printer configuration
curl -s -H "$BB_AUTH" "$BB_URL/settings/virtual-printer" | jq .
```

---

### 12. Notifications

```bash
# List notification channels
curl -s -H "$BB_AUTH" "$BB_URL/notifications/" | jq .

# Get a specific notification channel
curl -s -H "$BB_AUTH" "$BB_URL/notifications/{notification_id}" | jq .

# Create a notification channel (Discord, Telegram, Email, etc.)
curl -s -X POST -H "$BB_AUTH" -H "Content-Type: application/json" \
  -d '{
    "type": "discord",
    "name": "Discord Webhook",
    "enabled": true,
    "config": {"webhook_url": "https://discord.com/api/webhooks/..."},
    "events": ["print_done", "print_failed", "print_started"]
  }' "$BB_URL/notifications/" | jq .

# Update a notification channel
curl -s -X PATCH -H "$BB_AUTH" -H "Content-Type: application/json" \
  -d '{"enabled": false}' "$BB_URL/notifications/{notification_id}" | jq .

# Delete a notification channel
curl -s -X DELETE -H "$BB_AUTH" "$BB_URL/notifications/{notification_id}"

# Test a notification channel
curl -s -X POST -H "$BB_AUTH" "$BB_URL/notifications/{notification_id}/test" | jq .

# List notification templates
curl -s -H "$BB_AUTH" "$BB_URL/notification-templates/" | jq .

# Get a specific template
curl -s -H "$BB_AUTH" "$BB_URL/notification-templates/{template_id}" | jq .

# Update a notification template
curl -s -X PATCH -H "$BB_AUTH" -H "Content-Type: application/json" \
  -d '{"body": "Print {{archive.name}} finished!"}' \
  "$BB_URL/notification-templates/{template_id}" | jq .
```

---

### 13. Smart Plugs

```bash
# List configured smart plugs
curl -s -H "$BB_AUTH" "$BB_URL/smart-plugs/" | jq .

# Get a specific smart plug
curl -s -H "$BB_AUTH" "$BB_URL/smart-plugs/{plug_id}" | jq .

# Create a smart plug
curl -s -X POST -H "$BB_AUTH" -H "Content-Type: application/json" \
  -d '{
    "name": "X1C Plug",
    "type": "tasmota",
    "ip": "192.168.1.50",
    "printer_id": 1
  }' "$BB_URL/smart-plugs/" | jq .

# Toggle smart plug (on/off)
curl -s -X POST -H "$BB_AUTH" -H "Content-Type: application/json" \
  -d '{"state": "on"}' "$BB_URL/smart-plugs/{plug_id}/toggle" | jq .
# state options: "on" | "off"

# Delete a smart plug
curl -s -X DELETE -H "$BB_AUTH" "$BB_URL/smart-plugs/{plug_id}"
```

---

### 14. Spoolman Integration

```bash
# Spoolman connection status/config
curl -s -H "$BB_AUTH" "$BB_URL/spoolman/" | jq .

# Sync filaments from Spoolman
curl -s -X POST -H "$BB_AUTH" "$BB_URL/spoolman/sync" | jq .

# Spoolman spool list (from Bambuddy's perspective)
curl -s -H "$BB_AUTH" "$BB_URL/spoolman/spools" | jq .
```

---

### 15. Firmware

```bash
# Check available firmware for printers
curl -s -H "$BB_AUTH" "$BB_URL/firmware/" | jq .

# Get firmware info for a specific printer
curl -s -H "$BB_AUTH" "$BB_URL/firmware/{printer_id}" | jq .
```

---

### 16. Discovery

```bash
# Auto-discover printers on the local network
curl -s -H "$BB_AUTH" "$BB_URL/discovery/" | jq .
```

---

### 17. External Links

```bash
# List external links
curl -s -H "$BB_AUTH" "$BB_URL/external-links/" | jq .

# Create an external link
curl -s -X POST -H "$BB_AUTH" -H "Content-Type: application/json" \
  -d '{"name": "OrcaSlicer", "url": "orcaslicer://...", "icon": ""}' \
  "$BB_URL/external-links/" | jq .

# Update an external link
curl -s -X PATCH -H "$BB_AUTH" -H "Content-Type: application/json" \
  -d '{"name": "Updated Link"}' "$BB_URL/external-links/{link_id}" | jq .

# Delete an external link
curl -s -X DELETE -H "$BB_AUTH" "$BB_URL/external-links/{link_id}"
```

---

### 18. Maintenance

```bash
# List maintenance records
curl -s -H "$BB_AUTH" "$BB_URL/maintenance/" | jq .

# Get a specific maintenance record
curl -s -H "$BB_AUTH" "$BB_URL/maintenance/{record_id}" | jq .

# Create a maintenance record
curl -s -X POST -H "$BB_AUTH" -H "Content-Type: application/json" \
  -d '{
    "printer_id": 1,
    "type": "nozzle_change",
    "notes": "Replaced 0.4mm nozzle",
    "date": "2026-03-29T10:00:00"
  }' "$BB_URL/maintenance/" | jq .

# Update a maintenance record
curl -s -X PATCH -H "$BB_AUTH" -H "Content-Type: application/json" \
  -d '{"notes": "Updated notes"}' "$BB_URL/maintenance/{record_id}" | jq .

# Delete a maintenance record
curl -s -X DELETE -H "$BB_AUTH" "$BB_URL/maintenance/{record_id}"
```

---

### 19. Pending Uploads

```bash
# List pending (in-progress / unprocessed) uploads
curl -s -H "$BB_AUTH" "$BB_URL/pending-uploads/" | jq .

# Get a specific pending upload
curl -s -H "$BB_AUTH" "$BB_URL/pending-uploads/{upload_id}" | jq .

# Delete / discard a pending upload
curl -s -X DELETE -H "$BB_AUTH" "$BB_URL/pending-uploads/{upload_id}"
```

---

### 20. Updates

```bash
# Check for Bambuddy updates
curl -s -H "$BB_AUTH" "$BB_URL/updates/" | jq .
```

---

### 21. Cloud (Bambu Cloud)

```bash
# Cloud connection status
curl -s -H "$BB_AUTH" "$BB_URL/cloud/" | jq .

# Bambu Cloud profiles (filament/print profiles from cloud)
curl -s -H "$BB_AUTH" "$BB_URL/cloud/profiles" | jq .

# Sync cloud profiles
curl -s -X POST -H "$BB_AUTH" "$BB_URL/cloud/sync" | jq .
```

---

### 22. Support Bundle

```bash
# Download support bundle (ZIP archive for bug reports)
curl -s -H "$BB_AUTH" "$BB_URL/support/bundle" -o support_bundle.zip
```

---

### 23. Statistics

```bash
# Overall print statistics
curl -s -H "$BB_AUTH" "$BB_URL/archives/stats" | jq .

# Per-printer stats (use printer_id filter on archives)
curl -s -H "$BB_AUTH" "$BB_URL/archives/?printer_id=1" | jq \
  '[.[] | {name, duration_seconds, filament_used_g, cost}]'
```

---

## Common Workflows

### Check what's printing right now
```bash
BB_URL="${BAMBUDDY_URL}/api/v1"
BB_AUTH="X-API-Key: ${BAMBUDDY_API_KEY}"

curl -s -H "$BB_AUTH" "$BB_URL/printers/" | jq '.[].id' | while read id; do
  echo "=== Printer $id ==="
  curl -s -H "$BB_AUTH" "$BB_URL/printers/$id/status" | \
    jq '{stage, progress, layer_num, total_layer_num, mc_remaining_time, nozzle_temp, bed_temp}'
done
```

### Queue a reprint of the most recent archive
```bash
BB_URL="${BAMBUDDY_URL}/api/v1"
BB_AUTH="X-API-Key: ${BAMBUDDY_API_KEY}"

ARCHIVE_ID=$(curl -s -H "$BB_AUTH" "$BB_URL/archives/?page_size=1" | jq '.[0].id')
PRINTER_ID=$(curl -s -H "$BB_AUTH" "$BB_URL/printers/" | jq '.[0].id')

curl -s -X POST -H "$BB_AUTH" -H "Content-Type: application/json" \
  -d "{\"archive_id\": $ARCHIVE_ID, \"printer_id\": $PRINTER_ID}" \
  "$BB_URL/print-queue/" | jq .
```

### Get filament usage stats for this week
```bash
BB_URL="${BAMBUDDY_URL}/api/v1"
BB_AUTH="X-API-Key: ${BAMBUDDY_API_KEY}"

SINCE=$(date -u -d '7 days ago' +%Y-%m-%dT%H:%M:%S 2>/dev/null || \
        date -u -v-7d +%Y-%m-%dT%H:%M:%S)

curl -s -H "$BB_AUTH" "$BB_URL/archives/?since=$SINCE" | \
  jq '{
    total_prints: length,
    total_filament_g: [.[].filament_used_g // 0] | add,
    total_cost: [.[].cost // 0] | add
  }'
```

---

## Error Handling

Always check for non-2xx responses:

```bash
RESPONSE=$(curl -s -w "\n%{http_code}" -H "$BB_AUTH" "$BB_URL/printers/")
HTTP_CODE=$(echo "$RESPONSE" | tail -1)
BODY=$(echo "$RESPONSE" | head -n -1)

if [ "$HTTP_CODE" -ge 200 ] && [ "$HTTP_CODE" -lt 300 ]; then
  echo "$BODY" | jq .
else
  echo "Error $HTTP_CODE: $BODY"
fi
```

Common errors:
- **401 Unauthorized** — API key missing or invalid. Check `BAMBUDDY_API_KEY`.
- **403 Forbidden** — Key exists but lacks permission for this action (check key permissions: `can_queue`, `can_control_printer`, `can_read_status`).
- **404 Not Found** — Resource doesn't exist. Verify IDs.
- **422 Unprocessable Entity** — Invalid request body. Check JSON field names/types.
- **503 Service Unavailable** — Bambuddy or the printer is unreachable.

---

## Setup Instructions for User

To use this skill:

1. **Generate an API key** in Bambuddy: go to `Settings → API Keys → Create Key`.
   Grant the permissions you need (`can_read_status`, `can_queue`, `can_control_printer`).
   The key will look like `bb_xxxxxxxxxxxxxxxx`.

2. **Add to your OpenClaw config** (`~/.openclaw/openclaw.json`):
   ```json
   {
     "skills": {
       "entries": {
         "bambuddy": {
           "enabled": true,
           "env": {
             "BAMBUDDY_URL": "http://192.168.1.x:8000",
             "BAMBUDDY_API_KEY": "bb_your_key_here"
           }
         }
       }
     }
   }
   ```

3. Start a new OpenClaw session — the skill will be active.

> **Tip:** If Bambuddy is on a remote server, use its external URL or
> set up a Tailscale/WireGuard VPN. Ensure `curl` and `jq` are installed
> (`brew install curl jq` on macOS, `apt install curl jq` on Debian/Ubuntu).
