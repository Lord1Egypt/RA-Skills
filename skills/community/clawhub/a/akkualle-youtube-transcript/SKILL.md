---
name: youtube-transcript
description: "Extrahiert Transkripte von YouTube-Videos für Content-Erstellung. Nutze für Video-Analysen, Content-Ideen und Blog-Posts aus YouTube-Videos."
metadata: {"requires":{"env":["YOUTUBE_API_KEY"]},"emoji":"🎬","always":true}
user-invocable: true
---

# YouTube Transcript Skill

Extrahiert Transkripte von YouTube-Videos für SEO-Content.

## Setup

**API-Key erforderlich:**
1. Google Cloud Console öffnen
2. YouTube Data API v3 aktivieren
3. API-Key erstellen
4. In `.env` speichern: `YOUTUBE_API_KEY=your_key`

## Verwendung

**Via Shell Tool:**

```bash
/root/.openclaw/skills/youtube-transcript/youtube-transcript "VIDEO_ID"
```

**Beispiel:**

```bash
/root/.openclaw/skills/youtube-transcript/youtube-transcript "9nnsszlfE0w"
```

## Funktionen

1. **Transkript extrahieren** - Deutsches Transkript laden
2. **Video-Metadaten** - Titel, Beschreibung, Tags
3. **Content-Ideen generieren** - Aus Transkript
4. **Blog-Post erstellen** - Aus Video-Inhalt

## Alternative ohne API

Falls kein API-Key vorhanden, nutze:

```bash
# Mit yt-dlp
yt-dlp --write-auto-sub --sub-lang de --skip-download "VIDEO_URL"

# Mit youtube-transcript-api (Python)
pip install youtube-transcript-api
python -c "from youtube_transcript_api import YouTubeTranscriptApi; print(YouTubeTranscriptApi.get_transcript('VIDEO_ID', languages=['de']))"
```

## Use Cases

- **Video-to-Blog:** YouTube-Video in Blog-Post umwandeln
- **Content-Ideen:** Transkript für Keyword-Recherche nutzen
- **Zitate extrahieren:** Wichtige Aussagen finden
- **FAQ generieren:** Aus Video-Fragen

## Beispiel-Ausgabe

```
## Video: Claude Code 2.0 Neue Features

**Dauer:** 12:34
**Channel:** TechChannel

### Transkript (DE):

[00:00] Willkommen zurück zu einem neuen Video...
[00:15] Heute schauen wir uns Claude Code 2.0 an...
...

### Key Points:
1. Neue Skills-Funktion
2. Loops für wiederholte Aufgaben
3. Verbesserte Code-Analyse

### Content-Ideen:
- Blog: "Claude Code 2.0: Die 5 besten neuen Features"
- Vergleich: Claude Code vs GitHub Copilot
```

## Wann verwenden

Nutze dieses Skill wenn der User fragt:
- "Extrahiere das Transkript von diesem YouTube-Video"
- "Erstelle einen Blog-Post aus diesem Video"
- "Was sind die Key Points aus Video X?"
- "YouTube-Video analysieren"
