# agent-browser — Command Reference

Dies ist eine Referenz der häufigsten Befehle. Für die vollständige Liste: `agent-browser --help`

Version: 0.25.5 | Globale Flags: `--json`, `--debug`, `--annotate`, `-p browserbase`, `--session <name>`

---

## Navigation

| Befehl | Beschreibung |
|:---|:---|
| `open <url>` | URL öffnen |
| `back` | Zurück |
| `forward` | Vorwärts |
| `reload` | Seite neu laden |
| `close [--all]` | Browser/Session schließen (`--all` = alle Sessions) |

## Snapshots

| Befehl | Beschreibung |
|:---|:---|
| `snapshot` | Accessibility Tree der Seite |
| `snapshot -i` | Nur interaktive Elemente (empfohlen) |
| `snapshot -i -c` | Kompakt (leere Strukturen entfernt) |
| `snapshot -d 3` | Tiefe begrenzen |
| `snapshot -s "#main"` | Auf CSS-Selektor beschränken |
| `diff snapshot` | Vergleich zum letzten Snapshot |

## Interaktion

| Befehl | Beschreibung |
|:---|:---|
| `click @ref` | Element klicken |
| `dblclick @ref` | Doppelklick |
| `fill @ref "text"` | Eingabefeld leeren + füllen (bevorzugt!) |
| `type @ref "text"` | Text tippen (simuliert Tastendrücke) |
| `keyboard type "text"` | Tippen ohne Selektor |
| `press Enter` | Taste drücken (Enter, Tab, Escape, Control+a) |
| `hover @ref` | Maus über Element |
| `focus @ref` | Element fokussieren |
| `check @ref` | Checkbox anhaken |
| `uncheck @ref` | Checkbox abhaken |
| `select @ref "value"` | Dropdown-Option wählen |
| `drag @src @dst` | Drag & Drop |
| `upload @ref file1 file2` | Dateien hochladen |
| `download @ref /tmp/file` | Datei per Klick herunterladen |

## Scrollen

| Befehl | Beschreibung |
|:---|:---|
| `scroll <dir> [px]` | Scrollen (up/down/left/right, optional Pixel) |
| `scroll down 500` | 500px nach unten |
| `scrollintoview @ref` | Element in den Viewport scrollen |

## Informationen extrahieren

| Befehl | Beschreibung |
|:---|:---|
| `get text @ref` | Text eines Elements |
| `get html @ref` | HTML eines Elements |
| `get value @ref` | Wert eines Inputs |
| `get attr href @ref` | Attribut eines Elements |
| `get title` | Seitentitel |
| `get url` | Aktuelle URL |
| `get count ".item"` | Anzahl passender Elemente |
| `get cdp-url` | CDP WebSocket URL |
| `screenshot [path]` | Screenshot (optional: Pfad) |
| `screenshot --annotate` | Screenshot mit nummerierten Labels |
| `screenshot --full` | Volle Seite (scrollbar) |
| `pdf <path>` | Seite als PDF |

## Status prüfen

| Befehl | Beschreibung |
|:---|:---|
| `is visible @ref` | Ist Element sichtbar? |
| `is enabled @ref` | Ist Element aktiv? |
| `is checked @ref` | Ist Checkbox angehakt? |

## Elemente finden

| Befehl | Beschreibung |
|:---|:---|
| `find role button click` | Button per Rolle finden + klicken |
| `find text "Submit" click` | Element per Text finden + klicken |
| `find label "Email" fill "test@test.com"` | Per Label finden + füllen |
| `find placeholder "Search" fill "query"` | Per Placeholder |

## Warten

| Befehl | Beschreibung |
|:---|:---|
| `wait @ref` | Warten bis Element erscheint |
| `wait 2000` | 2 Sekunden warten |
| `wait --text "Success"` | Warten auf bestimmten Text |
| `wait --load networkidle` | Warten bis Netzwerk ruhig |

## Sessions & Auth

| Befehl | Beschreibung |
|:---|:---|
| `--session <name>` | Isolierte Browser-Session |
| `--session-name <name>` | Auto-Save/Restore (Cookies + Storage) |
| `--state <path>` | State aus JSON laden |
| `--profile <name>` | Chrome-Profil wiederverwenden |
| `auth save <name>` | Auth-Profil speichern |
| `auth login <name>` | Mit gespeichertem Profil einloggen |
| `auth list` | Gespeicherte Profile anzeigen |

## Remote / CDP

| Befehl | Beschreibung |
|:---|:---|
| `connect <port>` | Per CDP verbinden (empfohlen) |
| `connect <ws-url>` | Per WebSocket-URL verbinden |
| `--cdp <port>` | Legacy CDP-Verbindung |
| `--auto-connect` | Laufenden Chrome automatisch finden |

## Maus (Low-Level)

| Befehl | Beschreibung |
|:---|:---|
| `mouse move <x> <y>` | Maus bewegen |
| `mouse down` | Maustaste drücken |
| `mouse up` | Maustaste loslassen |
| `mouse wheel <dy>` | Mausrad scrollen |

## Netzwerk

| Befehl | Beschreibung |
|:---|:---|
| `network requests` | Netzwerk-Requests anzeigen |
| `network route <url> --abort` | Request blockieren |
| `network har <start\|stop> [path]` | HAR-Aufzeichnung starten/stoppen |

## Debug

| Befehl | Beschreibung |
|:---|:---|
| `console` | Konsolen-Logs anzeigen |
| `errors` | Seiten-Fehler anzeigen |
| `highlight @ref` | Element hervorheben |
| `trace start` | Chrome DevTools Trace aufzeichnen |
| `record start /tmp/video.webm` | Video aufzeichnen |
| `eval "document.title"` | JavaScript ausführen |
| `--debug` | Debug-Output aktivieren (globales Flag, z.B. `agent-browser --debug open <url>`) |

## Tabs

| Befehl | Beschreibung |
|:---|:---|
| `tab list` | Offene Tabs anzeigen |
| `tab new` | Neuen Tab öffnen |
| `tab close` | Tab schließen |
| `tab <n>` | Zu Tab n wechseln |

## Batch

```bash
agent-browser batch "open https://example.com" "snapshot -i" "click @e1"
# --bail: Bei erstem Fehler abbrechen
agent-browser batch --bail "open https://a.com" "click @e1"
```

## Clipboard

| Befehl | Beschreibung |
|:---|:---|
| `clipboard read` | Zwischenablage lesen |
| `clipboard write "text"` | In Zwischenablage schreiben |
| `clipboard copy` | Markierung kopieren |
| `clipboard paste` | Einfügen |

## AI Chat & Dashboard

| Befehl | Beschreibung |
|:---|:---|
| `chat "click the login button"` | KI-gesteuerte Aktion (Single-Shot) |
| `chat` | Interaktiver KI-Chat (REPL) |
| `dashboard start [--port 4848]` | Observability-Dashboard starten |
| `dashboard stop` | Dashboard stoppen |
| `skills list` | Verfügbare Skills anzeigen |
| `skills get <name>` | Skill-Inhalt abrufen |

## Streaming

| Befehl | Beschreibung |
|:---|:---|
| `stream enable [--port <n>]` | WebSocket-Streaming starten |
| `stream disable` | Streaming stoppen |
| `stream status` | Streaming-Status anzeigen |

## Browser-Einstellungen

| Befehl | Beschreibung |
|:---|:---|
| `set viewport 1920 1080` | Viewport-Größe |
| `set device "iPhone 15 Pro"` | Device emulieren |
| `set geo 51.47 6.86` | Geolocation setzen |
| `set offline on` | Offline-Modus |
| `set media dark` | Dark Mode |
| `cookies get` | Cookies anzeigen |
| `cookies clear` | Cookies löschen |
| `storage local` | LocalStorage anzeigen |
