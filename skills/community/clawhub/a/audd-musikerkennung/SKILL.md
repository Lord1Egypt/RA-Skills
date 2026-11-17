---
name: "audd-musikerkennung"
description: "Musikerkennung und AudD-Kontoverwaltung über den offiziellen AudD-MCP-Server (https://mcp.audd.io) und/oder die direkte HTTP-API. Ein eigener api_token ist optional — funktioniert per OAuth-MCP ganz ohne Token, mit Trial-Plan und mit bezahltem Plan, ebenso mit dauerhaft hinterlegtem Token. Nutze diesen Skill bei Songerkennung — \"welcher Song ist das?\", Audio-Clip oder Datei identifizieren, Shazam-artig, Radio-/Twitch-/YouTube-Streams überwachen, DJ-Sets, Podcasts oder Videos nach Tracks durchsuchen, Tracklists, Airplay-Monitoring, Copyright-Check — und bei allem rund um das AudD-Konto: api_token eintragen, hinterlegen, aus der Zwischenablage in den Secret-Vault übernehmen, in .env setzen, rotieren; Request-Kontingent, Verbrauch, Trial-Restlaufzeit, Plan-Upgrade, Rechnungen. Auch anwenden, wenn AudD nicht namentlich genannt wird, aber ein Audio-/Video-Link oder eine lokale Audiodatei identifiziert werden soll."
---

# AudD Musikerkennung

Zwei Zugänge, die sich ergänzen:

- **MCP-Server** (`https://mcp.audd.io`) — OAuth-authentifiziert, kennt das Konto. Braucht **keinen** api_token.
- **HTTP-API** (`https://api.audd.io/`, `https://enterprise.audd.io/`) — braucht einen `api_token`, dafür kann sie Binärdateien hochladen und große Dateien verarbeiten.

## Betriebsmodi — der Token ist optional

Der Skill muss in jedem dieser Zustände arbeiten. Stelle **zuerst** fest, welcher vorliegt, und arbeite dann in dessen Grenzen, statt einen Token zu verlangen, den es vielleicht gar nicht braucht.

| Modus | Vorhanden | Was geht |
|---|---|---|
| **A — nur MCP** | OAuth-Verbindung, kein Token hinterlegt | Erkennung per URL, Konto, Verbrauch, Streams. Kein Datei-Upload |
| **B — MCP + Token** | beides | Alles. Der bequemste Zustand |
| **C — nur Token** | `api_token`, kein MCP | Erkennung per URL **und** Datei, Enterprise, Streams. Keine Konto-/Verbrauchsdaten |
| **D — nichts** | weder noch | `api_token=test` für einen Probeaufruf mit stark begrenztem Kontingent |

In Modus A ist ein Datei-Upload nicht möglich, weil `make_api_request` nur URLs annimmt. Dann nicht abbrechen: entweder die Datei irgendwo als URL bereitstellen, oder — wenn es öfter vorkommt — den Token beschaffen. Erkläre den Grund, statt nur „geht nicht" zu sagen.

In Modus C sind Fragen nach Kontingent oder Plan nicht beantwortbar; die Verbrauchsdaten liegen nur hinter OAuth. Sag das offen und verweise auf [dashboard.audd.io](https://dashboard.audd.io).

**Frage nie unaufgefordert nach einem Token, wenn die Aufgabe im vorliegenden Modus lösbar ist.** Ein Token ist Komfort, keine Voraussetzung.

## Entscheidungsregel

| Situation | Weg |
|---|---|
| Einmalige Frage, Audio liegt als URL vor | MCP `make_api_request`, sonst HTTP mit Token |
| Lokale Datei (bis 10 MB) | HTTP-API, multipart `file=` — Token nötig |
| Datei > 10 MB, Mix, Podcast, Video, DJ-Set | `https://enterprise.audd.io/` — Token nötig |
| Viele Dateien / Skript / Integration | einmal Token beschaffen, dann direkt HTTP |
| Streams anlegen, ändern, löschen | beides möglich |
| Kontingent, Verbrauch, Plan, Rechnung | nur MCP |

Faustregel: **Sobald mehr als ein, zwei Calls anfallen, nimm den Token und ruf die API direkt** — schneller und zuverlässiger, als jede Anfrage durch den MCP-Server zu leiten. AudD empfiehlt das selbst.

---

## Teil 1 — Pläne: Trial und bezahlt

Der Skill darf keinen bezahlten Plan voraussetzen.

**Trial:** kostenlos, zeitlich befristet (das Dashboard zeigt „The trial is active till …"), mit kleinem Request-Kontingent. Der Standard-Endpunkt läuft damit normal. Enterprise-Uploads und Streams sind zwar technisch erreichbar, fressen aber schnell das gesamte Kontingent — der Enterprise-Endpunkt rechnet **1 Request pro 12 Sekunden Audio**, ein einstündiger Mix also 300 Requests. AudD vergibt für Bildungs-, Non-Profit- und gemeinnützige Projekte auf formlose Anfrage an hello@audd.io mehr Requests.

**Bezahlt:** Ab etwa 2 $ pro 1.000 Requests, mit as-you-go über das enthaltene Kontingent hinaus. Streams kosten separat 45 $ pro Stream und Monat (25 $ mit eigenem Katalog).

Praktische Konsequenz: **Bevor du etwas anstößt, das nennenswert Kontingent kostet** — eine lange Enterprise-Datei, eine Batch-Verarbeitung, ein neuer Stream —, rechne den Verbrauch vor und nenne die Zahl. Ist der MCP verbunden, lohnt vorher ein Blick mit `get_usage_stats` und `get_account_status`; steht dort ein Trial oder wenig Rest, sag das, bevor du loslegst, nicht danach.

Läuft ein Aufruf in **#901** (Limit erreicht), ist das kein technischer Fehler, sondern eine Kontingentfrage — dann Verbrauch zeigen und die Optionen nennen (warten bis zum nächsten Zyklus, Bonus-Requests, Planwechsel), statt es erneut zu versuchen.

---

## Teil 2 — Der Token (optional)

Der `api_token` wird bei jedem HTTP-Request als Feld `api_token` mitgeschickt — als Query-Parameter oder POST-Feld. Er steht im Dashboard neben „Your api_token" mit den Schaltflächen *Show*, *Revoke* und *Copy*.

### Reihenfolge beim Suchen

1. `AUDD_API_TOKEN` in der Umgebung.
2. Secret-Vault: `python vault.py get <vault> "AudD" api_token`. Der Vault ist AES-256-GCM-verschlüsselt und braucht **einmalig die Passphrase des Nutzers** — danach im selben Auftrag nicht erneut fragen.
3. MCP: `get_api_token` (Scope `token:read`).
4. Nutzer fragen — aber nur, wenn die Aufgabe ohne Token wirklich nicht geht (siehe Betriebsmodi).

### Vorhandenen Token dauerhaft hinterlegen

Der übliche Fall: Der Nutzer hat den Token schon, meist frisch über *Copy* in der Zwischenablage. Es gibt keinen Grund, ihn durch den Chat zu schicken.

**Windows 11, PowerShell, Zwischenablage direkt in den Vault:**

```powershell
cd "<Pfad zum secret-vault-Ordner>"
python vault.py add "<Pfad zur .vault-Datei>" "AudD" api_token=$(Get-Clipboard).Trim()
```

`vault.py` fragt die Passphrase interaktiv ab; der Token erscheint weder in der Ausgabe noch in der Chat-Historie. `add` legt den Anbieter „AudD" an, falls er fehlt, und ersetzt sonst nur das genannte Feld.

Prüfen, ohne den Wert anzuzeigen:

```powershell
python vault.py get "<Pfad zur .vault-Datei>" "AudD" | ForEach-Object { $_.Length }
```

**Als dauerhafte Umgebungsvariable**, wenn Skripte den Token brauchen:

```powershell
setx AUDD_API_TOKEN "$((Get-Clipboard).Trim())"
```

Wirkt erst in neu geöffneten Terminals. `setx` schreibt unverschlüsselt in die Benutzer-Registry — bequem, aber der Vault ist die sicherere Ablage.

**Linux/macOS:** `python vault.py add <vault> "AudD" api_token="$(pbpaste)"` bzw. `"$(wl-paste)"` / `"$(xclip -o)"`.

**Wenn der Nutzer den Token in den Chat schreibt:** entgegennehmen, verwenden, aber **nicht wiederholen** — nicht in der Antwort, nicht in einer Zusammenfassung, nicht in einem Skript, das ins Repo geht. Danach anbieten, ihn im Vault abzulegen. Und darauf hinweisen, dass ein im Chat geteilter Token als kompromittiert gelten sollte, sobald die Konversation geteilt oder exportiert wird — im Dashboard gibt es *Revoke*.

**Zwischenablage agentenseitig auslesen** (`read_clipboard` via computer-use) funktioniert, ist aber die schlechteste Variante: Der Klartext landet dann im Modellkontext. Nur auf ausdrücklichen Wunsch.

### Wo der Vault liegt — eine Falle

Der Skill-Ordner unter `…\local-agent-mode-sessions\skills-plugin\…\skills\secret-vault\` ist ein **schreibgeschützter Cache**. Eine dort abgelegte Änderung an `projekt-secrets.vault` kann beim nächsten Abgleich verloren gehen.

Deshalb: Vault-Datei an einen stabilen Ort außerhalb des Caches legen, etwa `%USERPROFILE%\.secrets\projekt-secrets.vault`. `vault.py` nimmt den Pfad als Argument und funktioniert von überall.

### Rotieren

Über *Revoke* im Dashboard oder `rotate_api_token` im MCP. In beiden Fällen stirbt der alte Token **sofort** — laufende Streams, Deployments und CI fangen in derselben Sekunde an zu scheitern. Vorher fragen, wo der Token überall liegt (Vault, `.env`, `setx`, Server), und die Ablagen danach in einem Rutsch aktualisieren:

```powershell
python vault.py rotate "<Pfad zur .vault-Datei>" "AudD" api_token=$(Get-Clipboard).Trim()
```

Beim Setzen in eine `.env` prüfen, ob die Datei in `.gitignore` steht.

---

## Teil 3 — Der MCP-Server

### Verbinden

Sind keine AudD-Tools verfügbar, ist der Server nicht verbunden:

```bash
claude mcp add --transport http audd https://mcp.audd.io/
```

Danach `/mcp` aufrufen und im Browser anmelden. In der Claude-Desktop-App stattdessen: Einstellungen → Connectors → **Custom Connector hinzufügen** → `https://mcp.audd.io`.

Streamable HTTP mit OAuth 2.0 (Authorization Code + PKCE), Dynamic Client Registration — nichts vorzuregistrieren.

**In einer nicht-interaktiven Sitzung lässt sich der OAuth-Flow nicht ausführen.** Fehlt die Anmeldung, sag das und weiche auf Modus C oder D aus, statt zu warten.

### Scopes

Der Server zeigt nur Tools, deren Scope gewährt wurde — eng gewähren. Ein Agent, der nur den Verbrauch überwacht, braucht `usage:read` und sonst nichts.

| Scope | Erlaubt |
|---|---|
| `profile:read` | E-Mail, verknüpfte Anmeldemethoden |
| `account:read` | Plan, Abo-Status, bezahlt-bis, Bonus-Requests |
| `usage:read` | Tagesgenaue Request-Zahlen und Kontingent |
| `billing:read` | Zahlungshistorie, offener Betrag, verfügbare Pläne |
| `billing:pay` | Stripe-Zahlungslinks erzeugen (bucht nie selbst ab) |
| `api:request` | AudD-API auf Kontingent des Kontos aufrufen |
| `token:read` | `api_token` lesen — sensibel |
| `token:write` | `api_token` rotieren — alter Token stirbt sofort |

Dynamisch registrierte Clients bekommen standardmäßig **kein** `token:write`.

### Tools

| Bereich | Tool | Zweck |
|---|---|---|
| API | `make_api_request` | AudD-API als Konto aufrufen — Erkennung, Lyrics, Stream-Verwaltung. **Audio nur per URL.** Verbraucht Kontingent wie ein Direktaufruf |
| | `get_api_docs` | Offizielle Doku als Markdown: `api`, `streams`, `enterprise`, `file-upload` |
| Konto | `get_profile` | E-Mail und Anmeldemethoden |
| | `get_account_status` | Plan, Abo-Status, bezahlt-bis, Bonus-Requests, Auto-Renew |
| Verbrauch | `get_usage_stats` | Aktueller Zyklus: gesamt, Kontingent, Rest, pro Tag |
| Token | `get_api_token` | Liefert den `api_token` |
| | `rotate_api_token` | Ersetzt ihn; der alte funktioniert **sofort** nicht mehr |
| Billing | `list_plans` | Pläne mit Preis und enthaltenen Requests |
| | `get_billing_history` | Letzte Zahlungen |
| | `get_amount_owed` | Überschreitung im laufenden Zyklus und deren Kosten |
| Zahlung | `subscribe_to_plan` | Zahlungslink für Abo oder Planwechsel |
| | `create_renewal_payment` | Zahlungslink für Verlängerung inkl. offener Extras |
| | `buy_bonus_requests` | Zahlungslink für N Extra-Requests (Vielfache von 1.000) |

Die drei Zahlungs-Tools erzeugen ausschließlich einen Stripe-Link, den der Kontoinhaber im Browser öffnen und bestätigen muss. **Es wird nie automatisch abgebucht** — sag das dazu, wenn du einen Link lieferst.

Verbrauchsdaten sind nur aggregierte Tageswerte; einzelne Requests legt der Server nicht offen.

### Was im Gespräch erwähnenswert ist

- **`make_api_request` kostet echtes Kontingent** und kann Zustand ändern: `setCallbackUrl` und `addStream` verändern die Stream-Konfiguration des Kontos. Bei autonomen Agenten Bestätigung anlassen.
- **Prompt Injection:** Vorsicht, wenn im selben Kontext Tools laufen, die ungeprüfte Inhalte einspeisen (Webseiten, Uploads). Ein präparierter Text könnte sonst `rotate_api_token` oder ein Zahlungs-Tool auslösen.

---

## Teil 4 — Erkennung über die HTTP-API

### Standard-Endpunkt: kurze Clips bis 10 MB

`https://api.audd.io/` — Antwortzeit etwa 0,1 bis 1,5 Sekunden.

Parameter: `api_token` (Pflicht), dazu genau eine Audioquelle — `url` (HTTP-URL, von AudD serverseitig geladen), `file` (multipart/form-data) oder `audio` (base64, von AudD ausdrücklich nicht empfohlen). Optional: `return` als kommaseparierte Liste aus `apple_music`, `spotify`, `deezer`, `musicbrainz`, und `market` als Ländercode (Standard `us`).

```bash
# per URL
curl https://api.audd.io/ \
  -F url='https://audd.tech/example.mp3' \
  -F return='apple_music,spotify' \
  -F api_token="$AUDD_API_TOKEN"

# lokale Datei
curl https://api.audd.io/ \
  -F file=@/pfad/zum/clip.mp3 \
  -F api_token="$AUDD_API_TOKEN"
```

Immer `https://` verwenden. Bei `http://` folgt ein Redirect, und die Formdaten gehen dabei verloren — häufigste Ursache für Fehler #700.

Ohne eigenen Token funktioniert `api_token=test` für einen einzelnen Probeaufruf.

### Enterprise-Endpunkt: lange Dateien

`https://enterprise.audd.io/` — für stundenlange Mixe, Podcasts, Videos, ganze Mitschnitte. Der Server zerlegt die Datei serverseitig in 12-Sekunden-Blöcke und erkennt jeden Track.

**Abrechnung: 1 Request pro 12 Sekunden Audio.** Mit `skip` und `every` lässt sich das drastisch senken: `every` ist die Zahl der Blöcke, die am Stück erkannt werden, `skip` die Zahl der danach übersprungenen. `every=1&skip=4` erkennt 12 s, überspringt 48 s — ein Fünftel der Kosten. Für Tracklists von DJ-Sets meist ein guter Startpunkt, weil Tracks dort mehrere Minuten laufen. Bei dicht geschnittenem Material (Werbeblöcke, Trailer) engmaschiger.

Auf einem Trial ist das der Unterschied zwischen „geht" und „Kontingent weg" — vorher rechnen und die Zahl nennen.

Weitere Parameter: `limit` (Obergrenze der erkannten Blöcke), `accurate_offsets='true'` (genaue Start-/Endzeiten), `skip_first_seconds`, `use_timecode='true'` (nutzt `t`/`start` aus der URL als Startzeit — nicht zusammen mit `skip_first_seconds`).

ISRCs und UPCs in der Antwort setzen einen Enterprise-Account voraus (api@audd.io).

### Antwort lesen

Jede Antwort hat `status` mit `"success"` oder `"error"`. Bei Erfolg steht das Ergebnis in `result`; ohne Treffer ist `result` `null` oder leer — das ist **kein** Fehler, sondern heißt: kein Match. Sag das auch so.

Ein Treffer enthält immer `artist`, `title`, `album`, `release_date`, `label`, `timecode`, `song_link`.

Die drei Zeitangaben werden leicht verwechselt:

- `timecode` — die Stelle **im erkannten Song**, an der das eingesendete Fragment spielt (z. B. 02:32 von „Warriors").
- `offset` (nur Enterprise) — die Stelle **in der eingesendeten Datei**, an der der 12-Sekunden-Block beginnt. Das ist der Wert für eine Tracklist.
- `start_offset` / `end_offset` (nur Enterprise, Millisekunden) — die Grenzen des gematchten Bereichs **innerhalb des 12-Sekunden-Blocks**.

`score` (0–100) gibt die Match-Sicherheit an. Bei mehreren Kandidaten pro Block steht der beste zuerst; Werte unter etwa 60 als unsicher kennzeichnen, nicht als Fakt präsentieren.

### Fehlercodes

| Code | Bedeutung und Abhilfe |
|---|---|
| #901 | Kein Token und Limit erreicht — Kontingentfrage, siehe Teil 1 |
| #900 | Ungültiger Token — Wert prüfen, ggf. rotiert oder revoked worden? |
| #600 | Audio-URL nicht erreichbar oder falsch |
| #700 | Keine Datei angekommen — Content-Type `multipart/form-data`? `https://` statt `http://`? |
| #500 | Ungültige Audiodatei |
| #400 | Datei zu groß (>10 MB) — auf den Enterprise-Endpunkt wechseln |
| #300 | Fingerprinting-Fehler, meist zu kurzes Audio |
| #51 | Warnung: `napster` im `return` — Plattform existiert nicht mehr, Parameter entfernen |

---

## Teil 5 — Streams (Radio, Twitch, YouTube)

Für laufende Überwachung von Radios und Live-Streams. **45 $ pro Stream und Monat** (25 $ mit eigenem Katalog), setzt ein im Dashboard gesetztes Stream-Limit voraus. Auf einem Trial ist das nicht enthalten — nenne das, bevor jemand Streams anlegt. Zum kostenlosen Testen verweist AudD auf api@audd.io.

Alle Methoden nehmen `api_token` und liegen unter `https://api.audd.io/`:

| Methode | Parameter | Zweck |
|---|---|---|
| `setCallbackUrl/` | `url` | Ziel für die Ergebnis-Callbacks |
| `getCallbackUrl/` | — | Aktuelle Callback-URL |
| `addStream/` | `url`, `radio_id`, optional `callbacks` | Stream hinzufügen |
| `getStreams/` | — | Alle Streams inkl. `stream_running` und `longpoll_category` |
| `setStreamUrl/` | `url`, `radio_id` | URL eines Streams ändern |
| `deleteStream/` | `radio_id` | Stream entfernen |

`radio_id` ist eine frei wählbare Ganzzahl, mit der der Nutzer den Stream identifiziert.

Als Stream-URL funktionieren direkte Streams (Icecast, HLS, DASH, m3u/m3u8) sowie die Kurzformen `twitch:kanalname`, `youtube:videoid` und `youtube-ch:channelid`.

Standardmäßig kommt der Callback, **nachdem** ein Song zu Ende gespielt hat, inklusive gespielter Gesamtdauer. Mit `callbacks=before` kommt er beim Start — dann ohne Spieldauer. Für „Now Playing"-Anzeigen ist `before` richtig, für Airplay-Reports das Standardverhalten.

Callbacks kommen als JSON per POST. Neben Ergebnissen gibt es Benachrichtigungen mit `notification_code`: `0` alles in Ordnung, `650` Stream nicht erreichbar, `651` nur Rauschen, keine Musik. Antwortet der Zielserver nicht mit 200 OK, sammelt AudD die Callbacks und liefert sie später nach.

**Ohne eigenen Server:** Callback-URL auf `https://audd.tech/empty/` setzen — Voraussetzung dafür, dass LongPolling funktioniert. Danach `https://api.audd.io/longpoll/?category=<longpoll_category>&timeout=50&since_time=<ts>` abfragen und den zurückgegebenen `timestamp` als nächstes `since_time` verwenden. Die `longpoll_category` steht in der Antwort von `getStreams/`; sie darf an Clients weitergegeben werden, der `api_token` niemals.

Fertige Anzeige: `https://widget.audd.tech/?ch=-<category>&background&history&shadow` (Minuszeichen vor der Kategorie beachten).

---

## Arbeitsweise

Wenn jemand einen Link schickt und fragt, was da läuft, ist die knappe Antwort die richtige: Interpret, Titel, ggf. Album und ein Streaming-Link. Die vollständige JSON-Antwort ist selten das Gewünschte — auf Nachfrage nachreichbar.

Bei Tracklists aus langen Dateien fasse aufeinanderfolgende identische Treffer zusammen: Der Enterprise-Endpunkt meldet denselben Song für jeden 12-Sekunden-Block erneut, und eine rohe Ausgabe wiederholt „Keyboard Killer" fünfmal hintereinander. Sinnvoll ist eine Tabelle mit Startzeit (aus `offset`), Interpret und Titel — ein Eintrag pro tatsächlichem Track.

Bevor du etwas anstößt, das Geld oder Kontingent kostet, nenne die Größenordnung vorher. Und bevor du rotierst, frage nach; das ist eine Einbahnstraße.

## Quellen

- API-Referenz: https://docs.audd.io/ (Markdown: https://docs.audd.io/.md)
- Streams: https://docs.audd.io/streams
- Enterprise: https://docs.audd.io/enterprise
- MCP-Server: https://docs.audd.io/mcp
- SDKs für 11 Sprachen: https://docs.audd.io/sdks
- Dashboard: https://dashboard.audd.io

