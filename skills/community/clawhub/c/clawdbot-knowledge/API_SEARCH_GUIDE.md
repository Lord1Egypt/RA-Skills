# 🔍 API SUCHE - KOMPLETTE ANLEITUNG

**Version:** 1.0.0
**Tool:** `api_search.py`
**Datum:** 2026-02-05

---

## 🚀 Schnellstart

```bash
cd /home/deepall/clawd

# Basis Suche
python3 api_search.py search "authentication"

# Endpoint suchen
python3 api_search.py endpoint GET /agents

# Kategorie durchsuchen
python3 api_search.py category agents

# Quick Reference anzeigen
python3 api_search.py ref

# Alle Endpoints auflisten
python3 api_search.py list
```

---

## 📋 VERFÜGBARE BEFEHLE

### 1. `search <term>` - Freie Textsuche

Suche nach beliebigen Begriffen in der API-Dokumentation.

```bash
python3 api_search.py search "authentication"
python3 api_search.py search "webhook"
python3 api_search.py search "rate limit"
python3 api_search.py search "error handling"
python3 api_search.py search "POST /tasks"
```

**Ausgabe:** Zeigt alle Zeilen mit Zeilennummern, die den Suchbegriff enthalten.

### 2. `endpoint <METHOD> <PATH>` - Spezifischer Endpoint

Finde einen genauen API-Endpoint.

```bash
python3 api_search.py endpoint GET /agents
python3 api_search.py endpoint POST /tasks
python3 api_search.py endpoint DELETE /tasks/123
python3 api_search.py endpoint GET /queue/status
```

**Ausgabe:** Zeigt alle Zeilen für diesen spezifischen Endpoint.

### 3. `category <name>` - Endpunkte nach Kategorie

Finde alle Endpoints einer bestimmten Kategorie.

```bash
python3 api_search.py category agents      # Agent-Endpunkte
python3 api_search.py category tasks       # Task-Endpunkte
python3 api_search.py category webhooks    # Webhook-Endpunkte
python3 api_search.py category auth        # Authentifizierung
python3 api_search.py category errors      # Fehlerbehandlung
python3 api_search.py category examples    # Code-Beispiele
```

### 4. `ref` - Quick Reference

Zeigt alle Endpoints, Authentifizierung, Rate Limits und Fehler auf einen Blick.

```bash
python3 api_search.py ref
```

**Inhalt:**
- Agent Management Endpoints
- Task Management Endpoints
- Queue Management Endpoints
- Webhook Endpoints
- Authentication Info
- Rate Limiting Info
- Common Errors
- Resources

### 5. `list` - Alle Endpoints auflisten

Zeigt eine strukturierte Liste aller verfügbaren Endpoints mit Beschreibungen.

```bash
python3 api_search.py list
```

### 6. `examples` - Code Beispiele

Zeigt Python, JavaScript und cURL Beispiele.

```bash
python3 api_search.py examples
```

---

## 🎯 PRAKTISCHE SZENARIEN

### Szenario 1: Ich möchte Tasks erstellen

```bash
# 1. Task-Creation-Dokumentation finden
python3 api_search.py search "Create Task"

# 2. POST /tasks Endpoint anschauen
python3 api_search.py endpoint POST /tasks

# 3. Code-Beispiele anschauen
python3 api_search.py examples
```

### Szenario 2: Ich brauche Authentifizierungsinformationen

```bash
# 1. Authentifizierung suchen
python3 api_search.py search "authentication"

# 2. Auth-Kategorie durchsuchen
python3 api_search.py category auth

# 3. Quick Reference anschauen
python3 api_search.py ref
```

### Szenario 3: Ich suche Fehlerbehandlung

```bash
# 1. Fehler suchen
python3 api_search.py search "error"

# 2. Error-Kategorie durchsuchen
python3 api_search.py category errors

# 3. Spezifischen Error Code suchen
python3 api_search.py search "401"
python3 api_search.py search "429"
```

### Szenario 4: Ich will Webhooks konfigurieren

```bash
# 1. Webhooks suchen
python3 api_search.py search "webhook"

# 2. Webhook-Kategorie durchsuchen
python3 api_search.py category webhooks

# 3. Subscribe Endpoint anschauen
python3 api_search.py endpoint POST /webhooks/subscribe
```

### Szenario 5: Agents verwalten

```bash
# 1. Alle Agent-Endpoints sehen
python3 api_search.py category agents

# 2. Endpoint-Liste anschauen
python3 api_search.py list

# 3. Spezifischen Endpoint anschauen
python3 api_search.py endpoint GET /agents
python3 api_search.py endpoint GET /agents/{id}/status
```

---

## 📊 BEISPIEL-AUSGABEN

### Beispiel 1: Search Output

```
======================================================================
🔍 Suchergebnis für: 'authentication'
======================================================================
Treffer gefunden: 5

1. [Zeile 6]
   **Authentication:** Bearer Token (JWT)

2. [Zeile 23]
   ## 🔐 AUTHENTICATION

3. [Zeile 25]
   ### Getting an API Key

4. [Zeile 106]
   | 401 | Unauthorized - Missing or invalid authentication |

5. [Zeile 131]
   authentication_failed - Invalid API key

======================================================================
```

### Beispiel 2: Endpoint Output

```
======================================================================
🔍 Suchergebnis für: 'GET /agents'
======================================================================
Treffer gefunden: 3

1. [Zeile 149]
   **Endpoint:** `GET /agents`

2. [Zeile 176]
   **Endpoint:** `GET /agents/{agent_id}`

3. [Zeile 199]
   **Endpoint:** `GET /agents/{agent_id}/status`

======================================================================
```

---

## 🎯 HÄUFIGE SUCHEN

| Aufgabe | Befehl |
|---------|--------|
| API Key holen | `python3 api_search.py search "API Key"` |
| Rate Limits | `python3 api_search.py search "rate limit"` |
| Fehler 401 | `python3 api_search.py search "401"` |
| Tasks erstellen | `python3 api_search.py search "POST /tasks"` |
| Agenten auflisten | `python3 api_search.py search "GET /agents"` |
| Webhooks | `python3 api_search.py search "webhook"` |
| SDKs | `python3 api_search.py search "SDK"` |
| Python-Beispiel | `python3 api_search.py search "Python Example"` |
| JavaScript-Beispiel | `python3 api_search.py search "JavaScript Example"` |
| cURL-Beispiel | `python3 api_search.py search "cURL Example"` |

---

## 💡 TIPPS & TRICKS

### Mehrwort-Suchen
```bash
python3 api_search.py search "Bearer Token"
python3 api_search.py search "POST /webhooks"
python3 api_search.py search "Rate Limiting"
```

### Case-insensitive
```bash
python3 api_search.py search "AUTHENTICATION"  # Funktioniert auch!
python3 api_search.py search "authentication"  # Oder so
python3 api_search.py search "Authentication"  # Oder auch so
```

### Teilsuchbegriffe
```bash
python3 api_search.py search "auth"            # Findet alles mit 'auth'
python3 api_search.py search "task"            # Findet alles mit 'task'
python3 api_search.py search "GET"             # Findet alle GET-Requests
python3 api_search.py search "POST"            # Findet alle POST-Requests
```

### Wildcards & Patterns
```bash
python3 api_search.py search "/agents"         # Alle agents-URLs
python3 api_search.py search "/tasks"          # Alle tasks-URLs
python3 api_search.py search "{id}"            # Alle parametrisierten URLs
```

---

## 🔗 DIREKTE SUCHE MIT SKILL

Falls du nur die rohe Suche möchtest:

```bash
python3 clawd_docs_skill.py search api_docs "your_search_term"
```

**Output:** JSON mit allen Matches

```json
{
  "document": "api_docs",
  "search_term": "your_search_term",
  "matches": 5,
  "results": [
    {
      "line_number": 23,
      "content": "..."
    }
  ]
}
```

---

## 📚 RESSOURCEN

### Dateien
- **API Such-Tool:** `/home/deepall/clawd/api_search.py`
- **Komplette API Docs:** `/home/deepall/clawd/API_DOCUMENTATION.md`
- **Skill Guide:** `/home/deepall/clawd/CLAWD_DOCS_SKILL_GUIDE.md`

### Befehle
```bash
# Vollständige API-Dokumentation anschauen
python3 clawd_docs_skill.py show api_docs

# API-Zusammenfassung
python3 clawd_docs_skill.py summary api_docs

# Alle Dokumentationen
python3 clawd_docs_skill.py list
```

---

## ⚡ PERFORMANCE

- **Such-Zeit:** < 100ms
- **Speichernutzung:** Minimal
- **Treffer:** Auf erste 20 Ergebnisse begrenzt
- **Ausgabe:** Formatiert und lesbar

---

## 🔍 SUCHSTRATEGIE

### Für Anfänger
1. Starte mit `python3 api_search.py ref`
2. Sieh dir die verfügbaren Endpoints an
3. Nutze `search` für spezifische Informationen

### Für fortgeschrittene Nutzer
1. Nutze `endpoint` für genaue Endpoint-Details
2. Verwende `category` für thematische Übersicht
3. Kombiniere mehrere Suchen für tiefe Analyse

### Für Entwickler
1. Nutze `examples` für Code-Snippets
2. Suche nach spezifischen Methoden (GET, POST, etc.)
3. Kombiniere mit JSON-Processing für Automation

---

## 🎓 LERNPFAD

**Tag 1:** Grundlagen
```bash
python3 api_search.py ref
python3 api_search.py list
```

**Tag 2:** Spezifische Endpoints
```bash
python3 api_search.py category agents
python3 api_search.py category tasks
```

**Tag 3:** Suche & Automation
```bash
python3 api_search.py search "POST"
python3 api_search.py examples
```

---

## ✅ Checkliste

- [ ] Tool installiert (`api_search.py`)
- [ ] Basis-Befehle getestet
- [ ] Quick Reference angeschaut (`ref`)
- [ ] Spezifische Suchen durchgeführt
- [ ] Code-Beispiele angesehen
- [ ] Mit Integrations-Szenarien experimentiert

---

**Version:** 1.0.0
**Status:** ✅ Production Ready
**Last Updated:** 2026-02-05

Viel Spaß beim API-Erkunden! 🚀
