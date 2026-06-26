# 🧠 MEMORY.md - Langzeit-Erinnerungen (Molty's Kernwissen)

## 🎬 **Trakt.tv** (seit 13.02.2026)
- **Keys:** `~/.trakt.yaml` (client-id/secret/access-token ✅ ready)
- CLI: `trakt-cli history`

## 💾 **Git-Backup** (seit 13.02.2026)
- **Repo:** https://github.com/WegoW/Openclaw.git
- **Hourly Cron:** MEMORY.md + memory/ auto commit/push (`scripts/backup.sh`)
- **Security:** NIE API-Keys in memory/*.md oder MEMORY.md speichern - immer .env + .gitignore + git-filter-repo für History-Cleanup bei Leaks

## 🎵 **Musik-Präferenz** (seit 02.02.2026)
- **Tool:** `mcporter call unified-hifi-control.hifi_zones`, `.hifi_now_playing zone_id=...`, `.hifi_play(...)` für Roon
- **Default Zone:** Schlafzimmer (`roon:1601dcef8115529daf4cd6807753971fae3e`)
- Wohnzimmer: `roon:160124b4c2dcc52aa8478e05110f7ed25120`

- **Artist-Only Regel**: Bei nur Interpret (kein Album/Song): `hifi_play zone_id=... query="Artist name" action="radio"`
- **Album‑Play‑Regel**: Beim Abspielen eines Albums immer den Artist ans Ende der Query anhängen (z.B. `query="Off the coast of me Kid Creole and the Coconuts"`).

## 🎮 **World of Tanks Console** (seit 05.02.2026)
- **Xbox ID:** 6062761 (wALTERwEGO [BOING])
- **WoTStars:** https://www.wotstars.com/xbox/6062761
- **Scraping:** agent-browser

## 🎥 **IMDb Ratings** (seit 08.02.2026)
- **CSV:** `/root/clawd/docs/imdb_ratings.csv` (3.962 Einträge: Filme/Serien + Ratings/Datum/Genre)
- **Queries:** `awk` oder Python-Scripts
- **Robust Search**: `awk -F',' 'NR>1 {line=tolower($0); if (line ~ /millers/ || line ~ /suchbegriff/) print $0}' /root/clawd/docs/imdb_ratings.csv | head -10` - sucht in ALLEN Feldern case-insensitive (inkl. Quotes/Apostrophe).

## 🏠 **Home Assistant** (seit 04.02.2026)
- ✅ **Nur MCP-Server:** `ha-mcp` via mcporter
- ❌ **Kein Web‑Zugriff:** No curl/browser/web_fetch für `ha.home:8123`
- 📌 **Best‑Practice:** Beim Zugriff immer das Skill **home-assistant-best-practices** verwenden.

 ## 🌐 **Browser Tools** (seit 15.02.2026)
 - **Primär:** agent-browser CLI (via exec) - für Web-Automatisierung/Scraping
- **agent-browser 'find'**: Nur Actions wie click/hover/fill (kein snapshot!). Snapshot separat nach find oder direkt.
 - **Fallback:** native browser tool (nur bei Fehlern)
 - bei browser tool fehler: `exec \"openclaw browser open <url>\"` statt Gateway-Restart

## 📰 **Nachrichten-Quellen** (seit 12.02.2026)
- **Primär RSS:** Tagesschau "Alle Meldungen": https://www.tagesschau.de/infoservices/alle-meldungen-100~rss2.xml

## 🔍 **Web-Suche** (seit 19.02.2026)
- **Primär:** `web_search` Tool (Brave Search API)
- **Fallback:** SearXNG-Server `http://192.168.1.247:8888`
- **Query:** `curl "http://192.168.1.247:8888/search?q=QUERY&format=json"`
- **Verwendung:** Bei Brave Rate-Limit oder anderen Fehlern → SearXNG via exec/curl nutzen

🎵 **Last.fm** (seit 13.02.2026)
- **Keys:** `/root/.openclaw/openclaw.json` → skills.entries.lastfm.env (LASTFM_USER=WegoW / LASTFM_API_KEY)
- API ready ✅

## 📄 **PDF-Generierung** (seit 14.02.2026)
- **ReportLab** (Fallback wenn Pandoc fehlt): `python3 -m pip install reportlab --break-system-packages --no-cache-dir`
- **Skript-Beispiel**: ReportLab Canvas für Text/PDF
- **Upload**: `gog drive upload &lt;file.pdf&gt; --account hupfhugo@gmail.com`
- **Telegram-Send**: Base64-Buffer für Local-Path-Bypass

## 🛠️ **Memory Search** (updated 2026-02-15)
- **Provider:** OpenAI text-embedding-3-small
- **Behavior:** Mandatory first step for prior work/dates/people/etc. Fallback to direct read/memory_get if results: [] (common for low-match queries).

## 🛠️ **Edit Tool** (neu 15.02.2026)
- **Regel:** oldText MUSS EXAKT matchen (Whitespace, Newlines inkl.!)
- **Routine:** 1. `read path` → oldText 1:1 kopieren → `edit`
- **Fallback:** Bei Error: `read` full → `write` updated file (oder kleinere Chunks)

## 🛠️ **Tool Exec Best Practices** (neu 16.02.2026)
- **Keine parallelen Calls bei Dependencies**: Sequence exec (zuerst open/snapshot → dann act). Errors überschreiben nicht gute Outputs.
- **Error Handling**: Bei Fehlern → retry sequentiell, nicht parallel. Nutze `get text` oder `eval` für sichere Scraping.
  - **Grep mit Apostrophen/Sonderzeichen** (neu 2026-02-25): Verwende `tolower($0) ~ /suchbegriff/i` in awk ODER `grep -iP "(?i).*suchbegriff.*|die millers|we.re the millers"` (PCRE für flexible Matches, . statt '). Vermeide komplexe Regex in single-quotes mit Escaping; teste mit `echo "we're the millers" | grep ...`.

## 🛠️ **Empfehlungen Filme/Serien** (neu 2026-02-17)
- **Prozess**: Bei \"was soll ich gucken/sehen\" FRAGEN IMMER:
  * 1. Trakt: `trakt-cli history --limit 50` (recent)
  * 2. IMDb: `awk` auf `/root/clawd/docs/imdb_ratings.csv` filtern (Title/Genre/Apple TV+ etc.)
  * Exclude: Schon bewertete/gesehene → Top-IMDb-Alternativen vorschlagen
  - **"Gesehen?" Queries** (neu 2026-02-25): IMMER:
    * IMDb-CSV: `awk -F',' 'NR>1 && tolower($0) ~ /suchbegriff/i {print $0}' /root/clawd/docs/imdb_ratings.csv | head -5` (sucht in ALLEN Feldern case-insensitive)
    * Trakt: `trakt-cli history --limit 200 | grep -i suchbegriff || true`
    * **Prozess**: IMMER zuerst IMDb-CSV durchsuchen (alle Felder case-insensitive), falls KEIN Treffer → dann Trakt (recent history).
- **Beispiel Query**: `awk -F',' 'NR>1 && /Apple TV/ {print}' /root/clawd/docs/imdb_ratings.csv

## 🔊 **TTS Voices** (seit 20.02.2026)
- **Primär:** ElevenLabs voiceId: "vl67BWhZHh0QyG35TvXt" (Config in openclaw.json ✅)
- **Fallback:** Edge-TTS de-DE-KillianNeural (nur bei Problemen mit ElevenLabs)
**Source:** User-Anweisung Walter Wego (20.02.2026)

## 🔊 **ElevenLabs Credits** (seit 20.02.2026)
- **Abruf:** `exec` mit `curl -X GET 'https://api.elevenlabs.io/v1/user' -H 'xi-api-key: [SECURE_STORAGE]' -H 'accept: application/json'`
- **Parse:** `subscription.character_limit - subscription.character_count` = verbleibend
- **Anzeige:** Nur "**Verbleibend:** X / Y Zeichen (Free Tier, monatlich). 🤓"

## 💰 **OpenClaw Cost-Tracker** (seit 21.02.2026)
- **Skill:** `~/openclaw/skills/openclaw-cost-tracker` (python3 scripts/cost_tracker.py)
- **Verwendung:** Bei allen Kostenfragen (Kosten/costs/token spend) diesen Skill priorisieren - parsed JSONL für USD/Tokens pro Model/Tag.
**Source:** User-Anweisung Walter Wego (21.02.2026)
**Source:** User-Anweisung Walter Wego (20.02.2026)
