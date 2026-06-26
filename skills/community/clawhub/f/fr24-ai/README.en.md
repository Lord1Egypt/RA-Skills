# FR24-AI · Flightroutes24 International Flights Agent Skill

[中文](README.md)

**Agent Skill** (`fr24-ai`) for Flightroutes24 international air tickets. Python scripts call the export gateway for natural-language parsing, demo/procurement shopping, verify, and booking—intended for Cursor, Claude Code, and similar agents.

| Item | Value |
|------|-------|
| Project | FR24-AI |
| Skill ID | `fr24-ai` |
| Author | FR24 |
| Python | 3.10+ |

---

## Features

| Mode | Prerequisites | Capabilities |
|------|---------------|--------------|
| Demo shopping | No procurement keys | `POST /ai/shopping` + `X-Skill-Client-Key`; daily quota per clientKey (default 10) |
| Procurement shopping | `FR_NEWAPI_APPKEY` + sign secret | Same endpoint with `appkey` and `authentication`; no demo daily quota |
| Booking | AES secret additionally | `POST /api/new/pricing` (verify), `POST /api/new/booking` (order) |

- **One-way / round-trip** only (max 2 legs); open-jaw not supported
- NL parsing for cities, dates, pax count, cabin; **refine** for airline / departure window then re-search
- Summary: **lowest direct** + **lowest connecting** (refund/change & baggage hints)
- JSON stdout: `userView` (user-facing) and `agentOnly` (agent-internal only)

---

## Quick start

### 1. Environment

```bash
cd /path/to/skill
pip install -r requirements.txt   # required for booking; shopping-only may skip
```

### 2. Install for Agent

Copy this folder into the agent skills path. Directory name must be **`fr24-ai`** (matches `name` in `SKILL.md`):

| Product | Example path |
|---------|----------------|
| Cursor | `~/.cursor/skills/fr24-ai/` |
| Claude Code | `~/.claude/skills/fr24-ai/` |

See [INSTALL.md](./INSTALL.md) for details.

### 3. Gateway

Edit **`config.py`** (do not use `skill.local.env`):

```python
EXPORT_BASE_URL = "https://flight.flightroutes24.com"
```

Shopping URL: `{EXPORT_BASE_URL}/ai/shopping`.

### 4. Smoke test

```bash
python scripts/skill_search_client.py ensure-key
python scripts/nl_to_search.py parse --text "Shenzhen to Bangkok Jun 1, 1 adult"
python scripts/skill_search_client.py search --payload-file .cache/pending_search.json
```

---

## Configuration

| Setting | Location | Description |
|---------|----------|-------------|
| `EXPORT_BASE_URL` | `config.py` | Export gateway base URL |
| `GRAY_HEADER` | `config.py` | Gray-routing header (e.g. `ww`) |
| `FR_NEWAPI_APPKEY` | OS user env | Procurement APPKEY |
| `FR_NEWAPI_SIGN_SECRET` | OS user env | SHA512 signing secret |
| `FR_NEWAPI_AES_SECRET` | OS user env | 16-byte AES for passenger encryption |

Check procurement setup:

```bash
python -c "import config; print('configured:', config.is_newapi_configured()); print('booking_ready:', config.is_booking_ready())"
```

- End-user key setup: [references/user-appkey-config.md](./references/user-appkey-config.md)
- Maintainer / dev: [references/setup-maintainer.md](./references/setup-maintainer.md)

---

## Project layout

```
fr24-ai/
├── README.md                 # Chinese (this file’s counterpart)
├── README.en.md              # English
├── SKILL.md                  # Agent workflow & triggers
├── INSTALL.md                # Installation
├── config.py                 # Gateway constants & env-based keys
├── requirements.txt
├── scripts/
│   ├── nl_to_search.py       # parse / refine
│   ├── skill_search_client.py
│   ├── skill_booking_client.py
│   ├── newapi_client.py
│   └── ...
├── references/
└── .cache/                   # local state (gitignored)
```

---

## CLI reference

Run from the skill root:

| Command | Purpose | Uses demo quota |
|---------|---------|-----------------|
| `python scripts/nl_to_search.py parse --text "..."` | Parse itinerary | No |
| `python scripts/nl_to_search.py refine --text "..."` | Merge airline/time filters | No |
| `python scripts/skill_search_client.py search --payload-file .cache/pending_search.json` | Search | Yes (demo) |
| `python scripts/skill_search_client.py search ... --selection direct\|transfer` | Search + pick direct/connecting | Yes |
| `python scripts/skill_booking_client.py parse-passengers --text "..."` | Parse passengers | — |
| `python scripts/skill_booking_client.py verify --passenger-confirmed` | Verify offer | — |
| `python scripts/skill_booking_client.py order --user-confirmed` | Place order | — |

Agents must confirm the trip with the user before `search`, and require two explicit confirmations for booking. See [SKILL.md](./SKILL.md).

---

## Documentation

| Doc | Purpose |
|-----|---------|
| [SKILL.md](./SKILL.md) | Agent instructions, search/booking flow |
| [INSTALL.md](./INSTALL.md) | Installation |
| [references/booking.md](./references/booking.md) | Booking steps |
| [references/search_params.md](./references/search_params.md) | Search request fields |
| [references/output-rules.md](./references/output-rules.md) | User-visible output rules |
| [references/user-appkey-config.md](./references/user-appkey-config.md) | Procurement key setup (users) |
| [references/setup-maintainer.md](./references/setup-maintainer.md) | Maintainer notes (not for end users) |

---

## Security & notes

- Do not commit `.cache/`, `skill_client.json`, or procurement secrets; never paste secrets in chat
- Only expose **`userView`** / **`message`** to users; keep `agentOnly` (e.g. `traceId`, `offerId`) internal
- Orders are real—call `order` only after explicit user confirmation
- Demo quota exceeded (`307901`): guide users to enable procurement keys

---

## Links

- Flightroutes24: https://www.flightroutes24.com/
