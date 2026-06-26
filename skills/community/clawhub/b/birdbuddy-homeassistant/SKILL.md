---
name: birdbuddy-homeassistant
description: >
  Set up a Bird Buddy smart bird feeder integration with Home Assistant.
  Installs ha-birdbuddy custom component, configures automations for bird
  detection / rare species / battery / feeder state, creates a live camera
  entity with GraphQL watching API, builds an HA dashboard, and routes all
  notifications to a configurable Telegram topic. Trigger phrases: "Bird Buddy
  Home Assistant", "set up birdbuddy HA", "Bird Buddy feeder automation",
  "birdbuddy camera entity", "birdbuddy notifications".
version: "1.0.0"
author: myk
tags: [home-assistant, bird-buddy, camera, telegram, automation]
---

# Bird Buddy ↔ Home Assistant Skill

This skill walks you through a complete production-grade Bird Buddy integration
with Home Assistant: custom component, live camera entity, Telegram notifications,
and a purpose-built dashboard.

---

## Variable Reference

Substitute these placeholders wherever you see `{{VAR}}` in config snippets
and reference files.

| Variable | Description | Example |
|---|---|---|
| `{{HA_CONFIG_DIR}}` | HA config directory on disk | `/home/mike/homeassistant` (Docker) or `/config` (HA OS) |
| `{{FEEDER_ID}}` | Bird Buddy feeder UUID (from HA entity attributes) | `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx` |
| `{{TELEGRAM_BOT_TOKEN}}` | Telegram Bot API token | `123456789:AAF...` |
| `{{TELEGRAM_CHAT_ID}}` | Telegram chat/group ID (integer, negative for groups) | `-1001234567890` |
| `{{TELEGRAM_THREAD_ID}}` | Telegram message thread / topic ID | `42` |
| `{{HA_URL}}` | Home Assistant base URL | `http://homeassistant.local:8123` |
| `{{HA_TOKEN}}` | Long-lived HA access token | created in HA Profile → Security |

---

## Step 1 — Install ha-birdbuddy Custom Component

**Option A: HACS (recommended)**
1. Open HACS → Integrations → ⋮ menu → Custom repositories
2. Add `https://github.com/jhansche/ha-birdbuddy` as an Integration
3. Search "Bird Buddy" → Download (version 0.0.21 tested)
4. Restart Home Assistant

**Option B: Manual**
```bash
mkdir -p {{HA_CONFIG_DIR}}/custom_components/birdbuddy
# Clone or download release tarball from https://github.com/jhansche/ha-birdbuddy
cp -r ha-birdbuddy/custom_components/birdbuddy/* {{HA_CONFIG_DIR}}/custom_components/birdbuddy/
```

After installing, go to **Settings → Devices & Services → Add Integration** and
search "Bird Buddy". Enter your Bird Buddy account credentials.

> **Account note:** If using a member account (not the feeder owner), the owner
> must add you as a member in the Bird Buddy app AND explicitly grant postcards
> and livestream access.

---

## Step 2 — Add Camera Platform to Component

The v0.0.21 component does not include the `camera` platform by default.
You must:

1. Copy `references/camera.py` to `{{HA_CONFIG_DIR}}/custom_components/birdbuddy/camera.py`
2. Edit `{{HA_CONFIG_DIR}}/custom_components/birdbuddy/__init__.py` and add
   `Platform.CAMERA` to the `PLATFORMS` list:

```python
from homeassistant.const import Platform

PLATFORMS = [
    Platform.BINARY_SENSOR,
    Platform.SENSOR,
    Platform.CAMERA,           # ← add this line
]
```

3. Restart Home Assistant. A new entity `camera.bird_buddy_camera` will appear.

---

## Step 3 — Configure rest_command

Bird Buddy automations send Telegram messages via `rest_command`.

### 3a. Add include to configuration.yaml

```bash
# Docker: configuration.yaml may be root-owned — use the move trick
cd {{HA_CONFIG_DIR}}
mv configuration.yaml configuration.yaml.bak
cp configuration.yaml.bak configuration.yaml
# Now edit as your user
```

Add to `configuration.yaml`:
```yaml
rest_command: !include rest_commands.yaml
```

### 3b. Create rest_commands.yaml

Copy `references/rest_commands.yaml` to `{{HA_CONFIG_DIR}}/rest_commands.yaml`
and substitute your Telegram values.

The final file should look like:
```yaml
birdbuddy_telegram_notify:
  url: "https://api.telegram.org/bot{{TELEGRAM_BOT_TOKEN}}/sendMessage"
  method: POST
  content_type: "application/json"
  payload: >-
    {
      "chat_id": {{TELEGRAM_CHAT_ID}},
      "message_thread_id": {{TELEGRAM_THREAD_ID}},
      "text": "{{ message }}",
      "parse_mode": "Markdown"
    }
```

> ⚠️ **`chat_id` must be a bare integer**, not a quoted string.
> `"-1001234567890"` will be rejected by the Telegram API; use `-1001234567890`.

Restart HA after editing configuration.yaml.

---

## Step 4 — Create input_boolean Notification Toggles

Create these five helpers via **Settings → Helpers → Create Helper → Toggle**,
or via the HA WebSocket API:

| Entity ID | Name |
|---|---|
| `input_boolean.bird_buddy_new_bird_detected` | Bird Buddy - New Bird Detected |
| `input_boolean.bird_buddy_rare_species_alert` | Bird Buddy - Rare Species Alert |
| `input_boolean.bird_buddy_low_battery_alert` | Bird Buddy - Low Battery Alert |
| `input_boolean.bird_buddy_offline_alert` | Bird Buddy - Offline Alert |
| `input_boolean.bird_buddy_daily_summary` | Bird Buddy - Daily Summary |

Enable the toggles you want active.

---

## Step 5 — Import Automations

Copy `references/automations.yaml` contents into your
`{{HA_CONFIG_DIR}}/automations.yaml`.

> If `automations.yaml` doesn't exist yet, create it (empty list `[]` to start).
> HA includes it automatically if you have `automation: !include automations.yaml`
> in `configuration.yaml` (it's the default for new installs).

The six automations cover:

| ID | Trigger | Condition |
|---|---|---|
| `birdbuddy_new_bird_detected` | `birdbuddy_new_postcard_sighting` event | toggle enabled |
| `birdbuddy_rare_species_alert` | same event + `hasNewSpecies == true` | toggle enabled |
| `birdbuddy_low_battery_alert` | battery sensor < 20% | toggle enabled |
| `birdbuddy_feeder_offline` | feeder state → `offline` | toggle enabled |
| `birdbuddy_feeder_online` | feeder state from `offline` | toggle enabled |
| `birdbuddy_daily_summary` | time trigger 00:00 UTC (8 PM ET) | toggle enabled |

Each automation calls `rest_command.birdbuddy_telegram_notify`.

You must supply `token`, `chat_id`, and `thread_id` in the `data:` block of
each action — or inject them via `input_text` helpers / secrets.yaml for a
cleaner setup.

Reload automations: **Developer Tools → YAML → Automations** or restart HA.

---

## Step 6 — Create the Bird Buddy Dashboard

Use the HA WebSocket API (or the UI) to create a dashboard at path `bird-buddy`.

> ⚠️ The `url_path` **must contain a hyphen** — `birdbuddy` (no hyphen) is
> rejected by HA. Use `bird-buddy`.

### Via WebSocket (curl + websocat or HA REST)

```bash
# Long-lived token required
export HA_URL="{{HA_URL}}"
export HA_TOKEN="{{HA_TOKEN}}"

# 1. Create the dashboard shell
curl -s -X POST "$HA_URL/api/lovelace/dashboards" \
  -H "Authorization: Bearer $HA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "url_path": "bird-buddy",
    "title": "Bird Buddy",
    "icon": "mdi:bird",
    "show_in_sidebar": true
  }'

# 2. Save dashboard config (see assets/dashboard_config.json)
```

### Via UI
1. Settings → Dashboards → Add Dashboard
2. Title: "Bird Buddy", URL path: `bird-buddy`, Icon: `mdi:bird`
3. Open dashboard → Edit → Raw config editor
4. Paste contents of `assets/dashboard_config.json`

The dashboard includes:
- **Camera card** — live snapshot from `camera.bird_buddy_camera`
- **Glance card** — battery, temperature, food level, signal, feeder state
- **Entity card** — last recent visitor sensor
- **Entities card** — all five notification toggle switches

---

## Step 7 — Verify Everything Works

```bash
# Check the camera entity exists
curl -s "$HA_URL/api/states/camera.bird_buddy_camera" \
  -H "Authorization: Bearer $HA_TOKEN" | python3 -m json.tool

# Trigger a test notification (fill in your values)
curl -s -X POST "$HA_URL/api/services/rest_command/birdbuddy_telegram_notify" \
  -H "Authorization: Bearer $HA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "token": "{{TELEGRAM_BOT_TOKEN}}",
    "chat_id": {{TELEGRAM_CHAT_ID}},
    "thread_id": {{TELEGRAM_THREAD_ID}},
    "message": "🐦 Bird Buddy HA integration test!"
  }'
```

Watch HA logs for camera snapshot activity:
```bash
# Docker example
docker logs homeassistant 2>&1 | grep -i birdbuddy
```

---

## Gotchas & Known Issues

1. **Telegram `chat_id` must be integer** — pass `-1001234567890`, not
   `"-1001234567890"`. The Telegram API rejects string-formatted chat IDs
   in JSON payloads from `rest_command`.

2. **`configuration.yaml` may be root-owned in Docker HA** — `nano` or direct
   edits may fail with permission denied. Use the move trick:
   `mv configuration.yaml configuration.yaml.bak && cp configuration.yaml.bak configuration.yaml`
   to create a user-owned copy.

3. **`watchingActiveKeep` returns `RESOURCE_NOT_FOUND` when feeder is
   DEEP_SLEEP** — this is expected behavior. The watching/streaming API is only
   available when the feeder is awake. The camera entity returns the cached
   postcard thumbnail instead.

4. **`Platform.CAMERA` must be added to `PLATFORMS`** in `__init__.py` — the
   v0.0.21 release does not ship a `camera.py`. Without adding `Platform.CAMERA`
   to `PLATFORMS`, HA will never call `async_setup_entry` in `camera.py`.

5. **Lovelace dashboard `url_path` must contain a hyphen** — `birdbuddy` is
   rejected; `bird-buddy` works. This is an HA URL slug validation rule.

6. **Food level sensor always reports `low`** — this is a known bug in the
   ha-birdbuddy integration (or Bird Buddy API). It does not reflect actual
   hardware food level. Ignore this sensor value until the integration is fixed.

7. **`content_type: "application/json"` in rest_command** — do NOT use a
   `headers:` block with Content-Type. Use the top-level `content_type:` key
   instead, otherwise the payload may not be parsed correctly by HA.

8. **Member account needs explicit permission** — if you're authenticating with
   a Bird Buddy member account (not the feeder owner), the feeder owner must
   add you as a member AND separately grant postcards and livestream access
   inside the Bird Buddy mobile app.

9. **`me.feed` query for postcards access** — member accounts use `me.feed` for
   recent postcards. The field `FeederForMember.recentPostcards` does not exist
   in the API; attempting to query it returns a schema error.

10. **`WatchingStartV2` returns `REQUESTED` when feeder is DEEP_SLEEP** — the
    `streamUrl` field only populates after the feeder wakes and transitions to
    `STREAMING` or `READY_TO_STREAM`. The camera.py polls with
    `watchingActiveKeep` for up to 45 seconds before giving up and returning
    the cached image.

---

## Reference Files

| File | Purpose |
|---|---|
| `references/camera.py` | Complete HA camera entity with GraphQL watching API + postcard thumbnail caching |
| `references/automations.yaml` | All six automations with placeholder variables |
| `references/rest_commands.yaml` | Telegram `rest_command` template |
| `assets/dashboard_config.json` | Lovelace dashboard YAML/JSON config |

---

## Sensor Entity IDs (ha-birdbuddy v0.0.21)

These are the entity IDs created by the integration. Adjust if yours differ
(check Settings → Entities and filter by "Bird Buddy").

| Entity | Description |
|---|---|
| `sensor.birdbuddy_battery` | Battery % (0–100) |
| `sensor.birdbuddy_temperature` | Ambient temperature (°F or °C per HA settings) |
| `sensor.birdbuddy_food_level` | Food level (⚠️ always reports `low` — known bug) |
| `sensor.birdbuddy_signal_strength` | WiFi signal (attribute `level`) |
| `sensor.birdbuddy_feeder_state` | Feeder state: `online`, `offline`, `deep_sleep`, `taking_postcards`, etc. |
| `sensor.birdbuddy_recent_visitor` | Species name of last recorded visitor |
| `camera.bird_buddy_camera` | Live snapshot camera (added by this skill) |
