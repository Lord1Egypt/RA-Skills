# feeds-digest

Multi-Source-RSS-Digest für technische Updates (YouTube, Microsoft-Blogs, GitHub Releases).
Sammelt, filtert, formatiert. Optional mit LLM-Summary.

## Setup

```bash
bash scripts/install.sh
```

Oder manuell:

```bash
mkdir -p ~/.config/feeds-digest
cp config/config.example.yaml ~/.config/feeds-digest/config.yaml
pip3 install --user -r requirements.txt
```

## Schnellstart

```bash
# Standard-Digest (alle Feeds, letzte 7 Tage)
feeds-digest

# Mit Zeitfenster
feeds-digest --since 3d
feeds-digest --since 1w

# Topic-Filter
feeds-digest --topics bc,fabric

# In Datei schreiben
feeds-digest --since 7d --output /home/HolBot/reports/digest-$(date +%Y-%m-%d).md

# LLM-Summary anhängen (Perplexity)
feeds-digest --llm
PERPLEXITY_API_KEY=sk-... feeds-digest --llm

# JSON für Piping
feeds-digest --json | jq '.items[].title'
```

## Verfügbare Optionen

| Flag | Beschreibung |
|---|---|
| `--since`, `-s` | Zeitfenster (`3d`, `1w`, `2w`, `1m`) |
| `--topics`, `-t` | Komma-getrennte Themen (z.B. `bc,fabric`) |
| `--config`, `-c` | Pfad zur Config-YAML |
| `--output`, `-o` | Output-Datei (sonst stdout) |
| `--llm` | LLM-Summary anhängen |
| `--json` | JSON statt Markdown |
| `--quiet`, `-q` | Nur Errors ausgeben (für Cron) |
| `--test` | Nur Feed-Erreichbarkeit testen |
| `--list-feeds` | Aktive Feeds aus Config anzeigen |
| `--history` | Cache-Verlauf anzeigen |

## Datenquellen

| Typ | URL-Pattern | Status 2026-06-07 |
|---|---|---|
| YouTube | `feeds/videos.xml?channel_id=UC...` | ✅ (IDs selbst finden) |
| MS Tech Community | `page_news_rss?category=...` | ❌ RSS abgeschaltet 2025 |
| Microsoft-Blogs | `https://*.microsoft.com/.../feed/` | ✅ (D365, Power BI) |
| blog.fabric.microsoft.com | `/feed`, `/rss`, etc. | ❌ Kein RSS |
| GitHub Releases | `releases.atom` | ✅ |
| Generische RSS | beliebig | ✅ |

Siehe `references/data-sources-2026.md` für Details und Alternativen.

## Cron-Integration

Default-Setup: **Sonntag, Mittwoch, Freitag um 21:00 Uhr lokal** (CET/CEST mit automatischer Sommerzeit).

```cron
# feeds-digest: 3x pro Woche (So, Mi, Fr) um 21:00 Uhr lokal
0 21 * * 0,3,5 TZ=CET /home/HolBot/skills/feeds-digest/scripts/feeds-digest.py \
  --since 7d --topics bc,fabric,openclaw \
  --output /home/HolBot/reports/digest-$(date +\%Y-\%m-\%d).md --quiet
```

Installation via User-Crontab:

```bash
crontab -e
# Obige Zeile einfügen, speichern, fertig.
```

Oder system-weit (`/etc/cron.d/`):

```bash
sudo tee /etc/cron.d/feeds-digest <<'EOF'
SHELL=/bin/bash
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
0 21 * * 0,3,5 root cd /home/HolBot && TZ=CET /home/HolBot/skills/feeds-digest/scripts/feeds-digest.py --since 7d --topics bc,fabric,openclaw --output /home/HolBot/reports/digest-$(date +\%Y-\%m-\%d).md --quiet >> /var/log/feeds-digest.log 2>&1
EOF
```

Mit LLM (Perplexity-Key aus `~/.config/openclaw/secrets/.env.gpg`):

```cron
0 21 * * 0,3,5 TZ=CET \
  PERPLEXITY_API_KEY="$(gpg --quiet --decrypt ~/.config/openclaw/secrets/.env.gpg 2>/dev/null | grep ^PERPLEXITY_API_KEY= | cut -d= -f2)" \
  /home/HolBot/skills/feeds-digest/scripts/feeds-digest.py --llm --output /home/HolBot/reports/digest-$(date +\%Y-\%m-\%d).md --quiet
```

Hinweise:
- `TZ=CET` = lokale Zeit mit DST (MESZ im Sommer automatisch)
- `\%` in Crontab = Escaped `%` (Crontab-Syntax)
- Cache-Dedup verhindert Dopplungen trotz überlappendem 7d-Fenster
- Beim ersten Lauf werden alle Items der letzten 7 Tage gezeigt, danach nur neue

## Konfiguration

Siehe `config/config.example.yaml`. Wichtige Felder:

```yaml
feeds:
  github_releases:
    - name: "OpenClaw"
      repo: "openclaw/openclaw"    # GitHub-Repo
      enabled: true
      topics: [openclaw]

  generic_rss:
    - name: "Power BI Blog"
      url: "https://powerbi.microsoft.com/en-us/blog/feed/"
      enabled: true
      topics: [powerbi]

defaults:
  since: "7d"                        # Default-Zeitfenster
  topics: []                         # Default-Topics
  max_per_source: 10                 # Items pro Quelle

llm:
  provider: "perplexity"             # perplexity | openai | ollama
  model: "sonar-pro"
```

## Eigene YouTube-Channel hinzufügen

Siehe `references/youtube-channel-discovery.md`. Kurzfassung:
1. Öffne `youtube.com/@<handle>`
2. Quelltext anzeigen (`Ctrl+U`)
3. Suche nach `"externalId":"UC..."`
4. ID in `config.yaml` eintragen, `enabled: true` setzen

## Eigene Feeds hinzufügen

```yaml
feeds:
  generic_rss:
    - name: "Mein Blog"
      url: "https://example.com/feed/"
      enabled: true
      topics: [mein-thema]
```

## Architektur

```
scripts/
├── feeds-digest.py           # Click-CLI Entry-Point
└── lib/
    ├── config.py             # YAML-Loader
    ├── models.py             # Dataclasses
    ├── filter.py             # Datum/Topic-Filter + Dedup
    ├── formatter.py          # Markdown/JSON-Output
    ├── llm.py                # Perplexity/OpenAI/Ollama
    ├── cache.py              # last-seen-guid
    └── sources/
        ├── base.py           # FeedSource-ABC
        ├── youtube.py
        ├── ms_techcommunity.py
        ├── github_releases.py
        └── generic_rss.py
```

## Troubleshooting

### "Config nicht gefunden"
```bash
mkdir -p ~/.config/feeds-digest
cp config/config.example.yaml ~/.config/feeds-digest/config.yaml
```

### Feed liefert 404
Manche RSS-URLs ändern sich. Test mit `curl -sI <url>`. Falls tot: in `references/data-sources-2026.md` nach Alternativen suchen.

### LLM-Summary leer
- `PERPLEXITY_API_KEY` (oder `OPENAI_API_KEY`) muss in der Umgebung sein
- `feeds-digest --llm` zeigt Fehler-Details in stderr

### Doppelte Items
Cache prüfen: `feeds-digest --history`. Falls veraltet: `rm ~/.cache/feeds-digest/history/*.jsonl`

## LLM-Kosten

Perplexity `sonar-pro`: ca. $0.001 pro Digest (sehr günstig).
Für lokale/kostenlose Variante: Ollama mit `qwen2.5:7b` — `ollama` als Provider in Config setzen.

## Lizenz

MIT (siehe Haupt-Repo)
