---
name: deskbird-automator
description: Steuert Deskbird ueber Telegram mit sicherem Auth-Handling, Discovery und Parkplatz-Status/Reservierung. Verwende diesen Skill, wenn ein OpenClaw-Agent Deskbird-Aufgaben ausfuehren oder eine wiederkehrende Cron-Session dafuer anlegen/aktualisieren soll, inklusive Rueckfrage zum Rhythmus und Reauth bei abgelaufener Auth.
---

# Deskbird-Automator

Verwende diesen Skill, um Deskbird ueber das lokale CLI (`scripts/deskbird_tool.py`) sicher zu bedienen und optional als wiederkehrende Cron-Session laufen zu lassen.

## Voraussetzungen

- Arbeite im Projektordner `<repo-root>`.
- Nutze bevorzugt diese CLI-Kommandos:
  - `./scripts/deskbird.sh auth-check`
  - `./scripts/deskbird.sh auth-refresh --format json`
  - `./scripts/deskbird.sh auth-import --stdin --format json`
  - `./scripts/deskbird.sh discovery`
  - `./scripts/deskbird.sh parking-status`
  - `./scripts/deskbird.sh parking-book-first`
  - Setup bei frischem Upload:
    - `python3 -m venv .venv`
    - `source .venv/bin/activate`
    - `pip install -r requirements.txt`
    - `python -m playwright install chromium`
    - `chmod +x scripts/deskbird.sh`
- Halte den Schonmodus aktiv (`DESKBIRD_SAFE_MODE=true`) und sende keine Request-Stuerme.
- Fuer Telegram-Reauth standardmaessig **nur** DevTools-Paste + `auth-import` verwenden.
- `auth-pair-*` und `auth-capture` nicht als Standard im Chat vorschlagen.

## Deterministischer Env-Pfad

- Verwende fuer alle Skill-Aufrufe den Wrapper `./scripts/deskbird.sh`.
- Der Wrapper setzt automatisch `--env-file <skill-root>/.env` und verhindert damit CWD-bedingte Auth-Fehler.
- Nur bei gezieltem Debugging darfst du `--env-file` explizit auf eine andere Datei setzen.

## Empfohlene Dauer-Auth (Broker-Basis)

- Hinterlege nach einmaliger Ermittlung in der Skill-`.env`:
  - `DESKBIRD_FIREBASE_API_KEY`
  - `DESKBIRD_FIREBASE_REFRESH_TOKEN`
- Dann kann der Agent automatisch per `auth-refresh` einen neuen Bearer holen, ohne jeden Login-Flow.

## Pflichtdialog Vor Automatisierung

Wenn noch keine passende Cron-Session existiert, frage den Nutzer in genau dieser Reihenfolge:

1. `Soll ich eine wiederkehrende Cron-Session dafuer anlegen?`
2. Wenn ja: `Welcher Rhythmus? Default ist taeglich um 00:30 Uhr (Europe/Berlin), ein Lauf fuer den naechsten 24h-Blick.`
3. `Was soll die Session pro Lauf genau tun?`  
   Falls unklar, biete als Defaults an:
   - `Nur Uebersicht ueber alle buchbaren Objekte senden`
   - `Uebersicht + Parkplatz automatisch buchen, wenn Regel erfuellt ist`
   - `Nur monitoren, nie buchen`
4. Fasse Name, Rhythmus und Session-Aufgabe zusammen und hole eine letzte Bestaetigung ein.

Wenn der Nutzer keinen Rhythmus nennt, setze den Default: taeglich 00:30 (Europe/Berlin).

## Reauth-Protokoll (immer vor Deskbird-Calls)

Fuehre vor Discovery/Status/Buchung immer zuerst aus:

```bash
./scripts/deskbird.sh auth-check --format json --min-valid-minutes 90
```

Auswertung:

- Wenn `requires_reauth=false`: normal fortfahren.
- Wenn `requires_reauth=true`:
  - Wenn `DESKBIRD_FIREBASE_API_KEY` und `DESKBIRD_FIREBASE_REFRESH_TOKEN` vorhanden sind:
    - zuerst automatisch `./scripts/deskbird.sh auth-refresh --format json --min-valid-minutes 90` ausfuehren.
    - nur wenn das fehlschlaegt, Nutzer um manuelle Reauth bitten.
  - Ohne Firebase-Refresh-Creds: Nutzer aktiv fragen, ob Reauth jetzt gestartet werden soll.
- Manueller Reauth-Standard ist **Token/Header-Paste aus Chrome DevTools**.

## Office-Discovery Pflicht

- Vor jeder Detailabfrage (`parking-status`, `parking-check`, `parking-book-first`) zuerst `discovery` ausfuehren.
- `--office-id` ist optional: Das CLI loest das Office automatisch ueber `internalWorkspaces` auf.
- Nur wenn mehrere Offices vorhanden und der Default unklar ist:
  - zuerst `--office-name "<NAME_TEILSTRING>"` verwenden, oder
  - `DESKBIRD_DEFAULT_OFFICE_ID` in der Skill-`.env` setzen.
- Der Agent soll den Nutzer **nicht** standardmaessig nach einer Office-ID fragen.

## Reauth Via DevTools Paste

Wenn Reauth noetig ist, leite den Nutzer kurz an:

1. `app.deskbird.com` im Browser oeffnen und normal per SSO einloggen.
2. DevTools (`Network`) oeffnen.
3. Einen `api.deskbird.com` Request anklicken.
4. Request-Header (`Authorization`, optional `Cookie`, `X-CSRF-Token`, `X-XSRF-Token`) kopieren.
5. Header-Block in Telegram an den Bot senden.

Importiere den vom Nutzer gepasteten Block dann intern so:

```bash
cat <<'EOF' | ./scripts/deskbird.sh auth-import --stdin --format json
<PASTED_HEADER_BLOCK_OR_TOKEN>
EOF
```

Danach immer nochmals pruefen:

```bash
./scripts/deskbird.sh auth-check --format json --min-valid-minutes 90
```

Fallback:
- Nur wenn DevTools-Paste unmoeglich ist, manuelles `auth-capture` anbieten.

Wenn Auth danach weiterhin ungueltig ist:

- Keine Buchungen ausfuehren.
- Klar melden, dass ohne erfolgreiche Reauth abgebrochen wird.

## Verhalten In Cron-Laeufen

Cron-Laeufe muessen fehlertolerant und vorsichtig sein:

- Nie aggressive Retries oder enge Polling-Schleifen starten.
- Wenn Auth im Cron-Lauf nicht mehr gueltig ist, nicht blind weiterprobieren.
- Stattdessen eine Telegram-Nachricht senden mit klarer Handlungsaufforderung zur Reauth und den Lauf sauber beenden.

## Cron-Session Erstellen/Aktualisieren

Nutze OpenClaw-Cron-Funktionen. Wenn Tooling verfuegbar ist, bevorzuge `cron.add`/`cron.update`; alternativ CLI:

```bash
openclaw cron add --name "Deskbird Daily" --schedule "30 0 * * *" --prompt "<SESSION_PROMPT>" --announce
```

Regeln:

- Verwende lokale Zeit (Europe/Berlin) fuer den Standard.
- Lege pro Aufgabe genau eine Cron-Session an (keine Duplikate).
- Aktualisiere bestehende Sessions statt neue Kopien anzulegen.

## Session-Prompt Bauen

Beim Erstellen des Cron-Prompts nutze die Vorlage aus [references/cron-session-template.md](references/cron-session-template.md) und ersetze Platzhalter fuer Zone/Regeln.

## Ausgabeformat Gegenueber Dem Nutzer

Bei jedem Lauf (manuell oder Cron) liefere kompakt:

1. Auth-Status (`ok` oder `reauth_noetig`)
2. Was geprueft wurde (Datum/Zonen/Objekttypen)
3. Wichtige Treffer (frei/belegt/gesperrt, wer belegt)
4. Ob eine Buchung durchgefuehrt wurde oder warum nicht
