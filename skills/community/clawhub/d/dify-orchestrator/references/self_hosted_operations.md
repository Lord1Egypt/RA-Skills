# Self-Hosted Operations

Diese Referenz sammelt operative Grundregeln fuer self-hosted Dify.

## API- und Oberflaechen-Trennung

Im self-hosted Betrieb ist es wichtig, die Oberflaechen sauber zu trennen:

- `DIFY_MGMT_API_URL` fuer Management-nahe Operationen
- `DIFY_API_URL` fuer Runtime-/App-API-Pfade
- `DIFY_CONSOLE_API_URL` fuer Console-nahe API-Pfade

## Operative Grundregeln

1. Vor Schreiboperationen zuerst den Ist-Zustand lesen.
2. Vor Loeschoperationen den Impact benennen und explizite Bestaetigung einholen.
3. Nach jeder Schreib- oder Loeschoperation einen lesenden Check oder Smoke-Check planen.
4. Bei self-hosted Trigger-/OAuth-Faellen Domain, Callback und Admin-Rechte explizit mitdenken.
5. Secrets nie in Skilltexten, Beispielen, Logs oder Commit-Historie materialisieren.

## Prompt- und App-Aenderungen

- `update_dify_prompt(...)` nicht blind fuer jeden App-Typ als gleich sicher behandeln.
- Nach Prompt-Aenderungen App-Details oder UI-nahe Verifikation empfehlen.

## Dataset- und Retrieval-Aenderungen

- Nach Uploads oder Dataset-Linking Retrieval mit realistischen Queries pruefen.
- Bei mehreren Knowledge Bases nicht nur auf Linking schauen, sondern auch auf Retrieval-Settings.

## Loesch- und Rollback-Denke

- App- oder Dataset-Loeschungen nie als triviale Routine behandeln.
- Vor Loeschung klar machen, ob nachgelagerte Apps, Datasets oder Arbeitsablaeufe betroffen sind.
- Bei riskanteren Umstellungen oder Trigger-/OAuth-Aenderungen lieber einen Rueckbaupfad benennen, statt nur "wird schon" zu signalisieren.

## Self-Hosted Trigger-/OAuth-Betriebsrealitaet

- self-hosted braucht oft eigene OAuth-Client-Einrichtung.
- Trigger-Callbacks brauchen korrekte Domain-/`TRIGGER_URL`-Konfiguration.
- Cloud-Verhalten ist keine sichere Annahme fuer self-hosted.
