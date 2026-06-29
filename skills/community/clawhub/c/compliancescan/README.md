# OpenClaw-Skill: `compliancescan`

Dieser Skill bindet die öffentliche API von **compliancescan.eu** in [OpenClaw](https://openclaw.ai)
ein. Damit können Sie direkt aus Ihrem Agenten heraus eine DSGVO-/Compliance-Prüfung einer
Website starten, den 0–100-Score samt wichtigster Befunde abrufen, Ihr Guthaben prüfen und
frühere Scans einsehen.

Der Skill besteht aus genau einer Datei – [`SKILL.md`](./SKILL.md). Diese enthält die Anweisungen
für den Agenten (curl-Aufrufe gegen `/api/v1`). Bitte lesen Sie sie vor der Installation einmal
durch – behandeln Sie fremde Skills grundsätzlich wie Code-Review.

## Voraussetzungen

- **OpenClaw** ist installiert und lauffähig.
- Die Kommandozeilen-Tools **`curl`** und **`jq`** sind im `PATH` verfügbar (der Skill prüft das
  über `requires.bins` und wird sonst nicht aktiv).
- Ein **API-Key** von compliancescan.eu. API-Zugriff erfordert einen **Business-** oder
  **Enterprise-**Tarif.

## 1. API-Key erstellen

1. Melden Sie sich unter `https://compliancescan.eu/dashboard` an.
2. Öffnen Sie **Einstellungen → API-Keys**.
3. Klicken Sie auf **Neuer Key**, vergeben Sie einen Namen (z. B. „OpenClaw").
4. Belassen Sie die Scopes auf der Vorgabe (`scan:read` + `scan:write`) – `scan:write` wird zum
   Starten eines Scans benötigt.
5. Kopieren Sie den angezeigten Schlüssel (`csk_live_…`). **Er wird nur einmal angezeigt** und
   kann später nicht erneut abgerufen werden.

## 2. Skill installieren

Kopieren Sie den Ordner `compliancescan/` (mit der `SKILL.md`) in eines Ihrer OpenClaw-Skill-
Verzeichnisse, z. B.:

```bash
mkdir -p ~/.openclaw/skills
cp -r compliancescan ~/.openclaw/skills/compliancescan
```

Alternativ können Sie ihn unter `<workspace>/skills/` ablegen, wenn der Skill nur für ein
bestimmtes Projekt gelten soll.

## 3. API-Key konfigurieren (nicht in den Chat eingeben)

Der Schlüssel wird **niemals** in den Chat eingegeben, sondern als Umgebungsvariable
`COMPLIANCESCAN_API_KEY` bereitgestellt. Empfohlen: Variable in Ihrem Shell-Profil setzen und in
`openclaw.json` referenzieren – so liegt der Wert nirgendwo in der Konfigurationsdatei.

Setzen Sie die Variable (z. B. in `~/.bashrc` / `~/.zshrc`):

```bash
export COMPLIANCESCAN_API_KEY="csk_live_…"
```

Und verweisen Sie in Ihrer `openclaw.json` darauf:

```json5
{
  skills: {
    entries: {
      "compliancescan": {
        enabled: true,
        apiKey: { source: "env", provider: "default", id: "COMPLIANCESCAN_API_KEY" }
      }
    }
  }
}
```

OpenClaw injiziert den Schlüssel nur für die Laufzeit des Agenten in den Host-Prozess und stellt
die ursprüngliche Umgebung danach wieder her. Der Wert erscheint dadurch weder im Prompt noch im
Chat-Verlauf.

> **Zwei Stolperfallen:**
> 1. **Sandbox:** Die Injektion gilt nur für den **Host-Prozess**, nicht innerhalb einer Sandbox.
>    Wird der Agent sandboxed ausgeführt, müssen `COMPLIANCESCAN_API_KEY` (sowie `curl`/`jq`)
>    zusätzlich in der Sandbox verfügbar gemacht werden, sonst schlägt der Skill mit
>    „apiKey not configured" fehl.
> 2. **Gating:** `requires.env` blendet den Skill aus, solange die Variable nicht gesetzt ist –
>    er taucht dann gar nicht erst als „eligible" auf.

## 4. Aktivierung prüfen

```bash
openclaw skills list --eligible      # Skill muss als „eligible" erscheinen (curl, jq, Key vorhanden)
openclaw skills info compliancescan  # zeigt das geparste Frontmatter
openclaw skills check                # validiert die Skill-Definition
```

Erscheint der Skill nicht als „eligible", fehlt meist `curl`/`jq` im `PATH` oder die
Umgebungsvariable `COMPLIANCESCAN_API_KEY`.

## 5. Verwendung

In einer OpenClaw-Sitzung:

```bash
openclaw agent --message "Scanne https://example.com auf Compliance"
```

oder als Slash-Command: `/compliancescan`. Beispiele für Anfragen:

- „Scanne https://example.com auf Compliance" → startet einen Full-Scan und meldet Score + Befunde.
- „Wie viele Scan-Credits habe ich noch?" → liest `GET /account`.
- „Zeig mir meine letzten Scans" / „Details zu Scan 1042" → listet bzw. ruft einen Scan ab.

## Wichtig zu wissen

- Die API führt **ausschließlich Full-Scans** aus (`type: "full"`). Quick-Scans gibt es nur in der
  Web-Oberfläche.
- `POST /api/v1/scans` arbeitet **synchron**: Der Aufruf wartet, bis der Scan fertig ist
  (typischerweise einige Sekunden bis Minuten), und liefert das vollständige Ergebnis zurück. Ein
  Polling ist nicht nötig; der Skill nutzt deshalb ein großzügiges Timeout (`--max-time 600`).
- **Jeder Full-Scan kostet 1 Credit** bzw. einen Scan aus dem monatlichen Tarif-Kontingent
  (Business 150/Monat, Enterprise 500/Monat). Bei einem Scan-Fehler wird ein abgebuchtes Credit
  automatisch zurückerstattet.
- Rate-Limits (Business 30 Anfragen/Min, 500/Tag; Enterprise 120/Min, 5000/Tag) liefern bei
  Überschreitung HTTP 429 mit `Retry-After`.

## Sicherheit

- Der API-Key wird nie im Chat, im Prompt oder in Logs ausgegeben.
- Der Skill startet pro Aufruf genau **einen** Scan und wiederholt fehlgeschlagene Aufrufe nicht
  automatisch (kein versehentlicher Credit-Verbrauch).
- Außer dem Scan-Start (`POST`) sind alle Aktionen nur lesend.
- Die Scan-`url` wird per `jq -n` als JSON-Wert übergeben (keine Shell-Interpolation
  ungeprüfter Eingaben).

## Für Maintainer: Veröffentlichung auf ClawHub

ClawHub ist die öffentliche Skill-Registry von OpenClaw. So wird dieser Skill dort publiziert:

1. **CLI installieren & anmelden** (GitHub-OAuth):
   ```bash
   npm i -g clawhub
   clawhub login          # bzw. `clawhub login --device` headless
   clawhub whoami
   ```
2. **Pflichtfelder im Frontmatter:** `name`, `description`, `version` (semver – ist gesetzt:
   `1.0.0`). `metadata.openclaw.requires` + `primaryEnv` müssen exakt das abbilden, was der Body
   nutzt (`curl`, `jq`, `COMPLIANCESCAN_API_KEY`) – sonst meldet die Sicherheitsanalyse einen
   „metadata mismatch". **Keine `license` eintragen:** ClawHub erzwingt MIT-0 und lehnt eigene
   Lizenz-/Preis-Angaben ab. Externe Kosten (Business/Enterprise-Tarif) gehören in den Body/die
   README, nicht in die Metadaten.
3. **Veröffentlichen:**
   ```bash
   clawhub skill publish ./skills/compliancescan --version 1.0.0 --dry-run   # Vorschau
   clawhub skill publish ./skills/compliancescan --version 1.0.0
   ```
4. **Sicherheitsprüfung (ClawScan):** läuft nach dem Upload automatisch und prüft u. a., ob die
   deklarierten `requires` (bins/env) zum tatsächlichen Verhalten passen. Blockierte Versionen
   bleiben für euch im Dashboard sichtbar, erscheinen aber nicht im öffentlichen Katalog.
5. **Updates:** `version` erhöhen und erneut `clawhub skill publish` ausführen; Tags wie `latest`
   zeigen auf eine Version.
6. **Endnutzer installieren** dann mit:
   ```bash
   clawhub inspect compliancescan     # vor der Installation prüfen (Code-Review-Hygiene)
   clawhub install compliancescan     # landet unter <workspace>/skills/compliancescan
   ```
   und konfigurieren den Key wie oben in Abschnitt 3.

> Quellen variieren je nach OpenClaw-/ClawHub-Version – prüft die genauen Flags mit
> `clawhub skill publish --help`, falls sich die CLI geändert hat.
