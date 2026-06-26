# Cron Session Prompt Template

Nutze diese Vorlage fuer wiederkehrende Deskbird-Laeufe.
Wenn verfuegbar, nutze `DESKBIRD_FIREBASE_API_KEY` + `DESKBIRD_FIREBASE_REFRESH_TOKEN` fuer automatisches Token-Refresh.

## Minimalvorlage

```text
Du steuerst Deskbird vorsichtig ueber das lokale CLI im Projektordner <repo-root>.
Nutze fuer Reauth standardmaessig nur DevTools-Paste + `auth-import`.
Nutze fuer alle Aufrufe den Wrapper `./scripts/deskbird.sh`, damit immer die Skill-`.env` verwendet wird.

1) Auth-Pflichtcheck:
- Fuehre aus: ./scripts/deskbird.sh auth-check --format json --min-valid-minutes 90
- Wenn requires_reauth=true:
  - Falls `DESKBIRD_FIREBASE_API_KEY` + `DESKBIRD_FIREBASE_REFRESH_TOKEN` vorhanden:
    - zuerst automatischen Refresh versuchen:
      - `./scripts/deskbird.sh auth-refresh --format json --min-valid-minutes 90`
    - danach erneut auth-check.
    - nur wenn weiterhin reauth noetig: manuellen Flow starten.
  - Bitte den Nutzer um einen Header-/Token-Paste aus Chrome DevTools:
    - Deskbird im Browser oeffnen, normal per SSO einloggen.
    - DevTools > Network > Request auf `api.deskbird.com`.
    - `Authorization` und optional `Cookie`/`X-CSRF-Token`/`X-XSRF-Token` kopieren.
    - In Telegram an den Bot pasten.
  - Importiere den Paste intern:
    - `cat <<'EOF' | ./scripts/deskbird.sh auth-import --stdin --format json`
    - `<PASTED_HEADER_BLOCK_OR_TOKEN>`
    - `EOF`
  - Danach erneut auth-check ausfuehren.
  - Beende den Lauf ohne weitere API-Aktionen.

2) Bei naechstem Lauf:
- Erneut auth-check ausfuehren.
- Nur wenn auth-check OK: fahre mit Discovery/Buchung fort.
- Sonst erneut Header-/Token-Paste anfordern.

3) Discovery (Standardumfang):
- Fuehre aus: ./scripts/deskbird.sh discovery --date <DATE_YYYY_MM_DD> --start-local 00:00 --end-local 23:59 --format json
- Erstelle eine kompakte Zusammenfassung je Zone/Objekttyp (frei, belegt, buchbar, gesperrt).
- Nutze die `office_resolution` aus dem Discovery-Ergebnis fuer alle folgenden Schritte.

4) Optional Parkplatz-Logik:
- Bei Regel "nur monitoren": keine Buchung, nur Bericht.
- Bei Regel "auto-buchen":
  - Fuehre aus: ./scripts/deskbird.sh parking-status --date <DATE_YYYY_MM_DD> --start-local <START_HH_MM> --end-local <END_HH_MM> --format json
  - Wenn Bedingungen erfuellt sind, buche vorsichtig mit dry-run vorab:
    - ./scripts/deskbird.sh parking-book-first --date <DATE_YYYY_MM_DD> --start-local <START_HH_MM> --end-local <END_HH_MM> --dry-run
    - danach ohne --dry-run nur wenn alles plausibel ist.

5) Telegram-Ausgabe:
- Melde Auth-Status, Kernzahlen, auffaellige Sperrungen und ob gebucht wurde.
- Bei Fehlern klar sagen, was als naechster manueller Schritt noetig ist.
```

## Platzhalter

- `<ZONE_NAME>`: Name der Parking-Zone (tenant-spezifisch)
- `<DATE_YYYY_MM_DD>`: Zieltag des Laufes (bei Daily 00:30 standardmaessig das aktuelle lokale Datum in Europe/Berlin)
- `<START_HH_MM>/<END_HH_MM>`: Buchungsfenster (z. B. `08:30` bis `19:00`)

## Sicherheitsregeln

- Schonmodus immer aktiv lassen.
- Pro Lauf so wenig API-Calls wie moeglich.
- Keine harten Retry-Loops bei 429/5xx.
