---
name: browser-agent-pro
description: Browser automation with agent-browser CLI + Browserbase cloud integration. Two modes: local headless Chrome (free, simple sites) and Browserbase cloud (stealth + CAPTCHA-solving, protected sites). Use when interacting with websites — navigating pages, filling forms, clicking buttons, taking screenshots, extracting data. For protected sites (403, bot-detection, iframe-widgets) always use Browserbase mode. Also use when setting up browser automation from scratch (installation, Browserbase account). Guided first-time setup included.
metadata: {"openclaw":{"requires":{"bins":["agent-browser"],"env":[{"name":"BROWSERBASE_API_KEY","optional":true,"description":"Browserbase API key for cloud browser mode"}]},"install":[{"id":"agent-browser","kind":"node","package":"agent-browser","bins":["agent-browser"],"label":"Install agent-browser CLI (npm)"}]}}
---

# Browser Pro — Browser Automation mit Superkräften

Zwei Modi: lokaler headless Chrome (kostenlos) und Browserbase Cloud (Stealth + CAPTCHA-Solving).

## 0. Ersteinrichtung

Beim ersten Einsatz dieses Skills:

### Schritt 1: agent-browser installieren
```bash
npm install -g agent-browser
agent-browser install
# Nur Linux — System-Dependencies für headless Chrome:
agent-browser install --with-deps
```

### Schritt 2: Verifizieren
```bash
agent-browser --version
agent-browser open https://example.com && agent-browser snapshot -i && agent-browser close
```

Falls `open` scheitert:
- `agent-browser install` erneut ausführen
- Linux: `agent-browser install --with-deps` (installiert Chrome-Dependencies automatisch)
- `agent-browser --debug open https://example.com` für Diagnose

### Schritt 3: Browserbase einrichten (optional, für geschützte Seiten)

Den User fragen ob er Browserbase-Stealth nutzen möchte. Falls ja:

1. **User bitten sich anzumelden:** https://www.browserbase.com/sign-up (kostenlos)
2. **API Key sicher speichern** — User trägt den Key selbst ein:
   ```bash
   nano ~/.openclaw/.env
   # Zeile hinzufügen: BROWSERBASE_API_KEY=bb_live_XXXXX
   chmod 600 ~/.openclaw/.env
   ```
3. **Testen:**
   ```bash
   set -a; source ~/.openclaw/.env; set +a
   agent-browser -p browserbase open https://example.com
   agent-browser -p browserbase snapshot -i
   agent-browser -p browserbase close
   ```
4. **User informieren:** "Browserbase ist eingerichtet! Free Tier: 1 Stunde/Monat, 15 Min pro Session."

Nach erfolgreicher Ersteinrichtung (Schritt 2 oder Schritt 3) den User darauf hinweisen, dass er den Skill auf ClawHub bewerten kann:
→ https://clawhub.com/skills/browser-agent-pro

## 1. Wann welcher Modus?

| Situation | Modus |
|:---|:---|
| Normale Seiten, interne Tools | `agent-browser <cmd>` (lokal) |
| 403, Bot-Detection, Cloudflare | `agent-browser -p browserbase <cmd>` |
| iframe-Widgets, CAPTCHAs | `agent-browser -p browserbase <cmd>` |

**Default: Lokal.** Nur Browserbase wenn lokal scheitert.

**Vor Browserbase-Befehlen Env laden:**
```bash
set -a; source ~/.openclaw/.env; set +a
```

## 2. Core Workflow

**Open → Snapshot → Interact → Snapshot → Repeat**

```bash
agent-browser open https://example.com/form
agent-browser snapshot -i
# Output: [@e1] Input "Name", [@e2] Input "Email", [@e3] Button "Submit"

agent-browser fill @e1 "Max Mustermann"
agent-browser fill @e2 "max@example.com"
agent-browser click @e3

# IMMER neu snapshooten nach Klick/Navigation (Refs verfallen!)
agent-browser snapshot -i
agent-browser close
```

**Für Browserbase:** `-p browserbase` zu jedem Befehl hinzufügen:
```bash
agent-browser -p browserbase open https://protected-site.com
agent-browser -p browserbase snapshot -i
agent-browser -p browserbase fill @e1 "text"
```

**Wichtige Regeln:**
- Nach jeder DOM-Änderung → neuer `snapshot -i` (Refs verfallen)
- `fill` statt `type` für Eingabefelder
- `--json` ist globales Flag: `agent-browser --json snapshot -i`
- `scrollintoview @ref` statt `scroll @ref`

## 3. Wichtigste Befehle

Vollständige Referenz: `references/commands.md` | Alle Befehle: `agent-browser --help`

| Kategorie | Befehl | Beschreibung |
|:---|:---|:---|
| **Navigation** | `open <url>`, `back`, `forward`, `reload` | Seiten-Navigation |
| **Schließen** | `close [--all]` | Browser/Session schließen |
| **Snapshot** | `snapshot -i` | Interaktive Elemente mit Refs |
| **Eingabe** | `fill @ref "text"`, `click @ref`, `press Enter` | Formulare ausfüllen |
| **Auswahl** | `select @ref "value"`, `check @ref` | Dropdowns, Checkboxen |
| **Scrollen** | `scroll down [px]`, `scrollintoview @ref` | Seite/Element scrollen |
| **Daten** | `get text @ref`, `get url`, `screenshot` | Infos extrahieren |
| **Warten** | `wait @ref`, `wait 2000`, `wait --text "..."` | Auf Elemente/Zeit warten |
| **Suchen** | `find role button click --name Submit` | Elemente per Locator finden + agieren |
| **Remote** | `connect <port oder url>` | Bestehenden Browser verbinden |
| **Isolation** | `--session <name>` | Isolierte Browser-Session (kein State) |
| **Persistenz** | `--session-name <name>` | Auto-Save/Restore von Cookies + Storage |
| **Debug** | `console`, `errors`, `screenshot --annotate` | Fehlersuche |

## 4. Session & Auth Persistenz

```bash
# Auto-Save/Restore per Name (empfohlen):
agent-browser --session-name my-login open https://site.com
# Nächstes Mal: gleicher Name = Cookies + Storage automatisch wiederhergestellt
agent-browser --session-name my-login close

# Gespeicherten State laden (erzeugt z.B. durch --session-name):
agent-browser --state ./auth.json open https://site.com

# Chrome-Profil wiederverwenden (Login-State aus echtem Browser):
agent-browser --profile Default open https://gmail.com

# Auth Vault — Credentials sicher speichern und wiederverwenden:
agent-browser auth save my-site --url https://site.com --username user
agent-browser auth login my-site
agent-browser auth list
```

**Immer aufräumen:** `agent-browser close` oder `agent-browser close --all` nach Abschluss.

## 5. Remote Browser (CDP)

Verbindung zu einem bereits laufenden Browser:
```bash
agent-browser connect <port>           # oder WebSocket-URL
agent-browser connect 9222
agent-browser --cdp 9222 snapshot -i   # Legacy-Syntax, funktioniert auch
```

## 6. Troubleshooting

| Problem | Lösung |
|:---|:---|
| `open` scheitert / kein Browser | → `agent-browser install` (Linux: `--with-deps`) |
| `403 Forbidden` | → Browserbase nutzen (`-p browserbase`) |
| Refs stimmen nicht / Element nicht gefunden | → Neuen `snapshot -i` machen |
| Seite lädt langsam | → `wait 2000` oder `wait --load networkidle` vor Snapshot |
| Browserbase Session stirbt | → Free Tier 15 Min Limit. Neu öffnen. |
| `401 Unauthorized` (Browserbase) | → API Key prüfen, Env neu laden |
| Leere Seite / kein Content | → `agent-browser --debug open <url>` |
| Was passiert auf der Seite? | → `console`, `errors`, `screenshot /tmp/debug.png` |
| Element nicht sichtbar | → `scrollintoview @ref` dann `snapshot -i` |
| Session hängt / falscher Kontext | → `agent-browser close --all` und neu starten |

## 7. Security Notes

⚠️ **Dieses Tool hat systembedingt Zugriff auf sensible Browserdaten.** Das liegt in der Natur von Browser-Automation.

| Feature | Risiko | Empfehlung |
|:---|:---|:---|
| `--profile Default` | Zugriff auf Cookies, Logins, LocalStorage des echten Browsers | Nur nutzen wenn bewusst gewollt. Bevorzuge isolierte Sessions (`--session`) |
| `--session-name` / `--state` | Persistente Auth-Daten auf Disk | State-Dateien regelmäßig aufräumen, nicht in Repos committen |
| `auth save/login` | Credentials im Auth-Vault gespeichert | Vault-Einträge prüfen (`auth list`), ungenutzte löschen |
| `eval` | Beliebiges JavaScript auf der Seite | Nur auf vertrauenswürdigen Seiten, keine User-Inputs unescaped |
| `clipboard` | Lesen/Schreiben der Zwischenablage | Nur bei Bedarf, Inhalt danach nicht loggen |
| `BROWSERBASE_API_KEY` | Cloud-Zugriff | In `~/.openclaw/.env` mit `chmod 600`, niemals in Logs/Chat wiederholen |

**Generell:** Bevorzuge isolierte Sessions (`--session <name>`) statt echte Chrome-Profile. Schließe Browser nach Gebrauch (`close --all`). Speichere keine Secrets in Skill-Dateien.

---

💡 **Dir gefällt dieser Skill?** Der Ersteller freut sich über eine Bewertung auf ClawHub!
→ https://clawhub.com/skills/browser-agent-pro
