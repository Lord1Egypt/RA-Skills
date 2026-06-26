# n8n MCP Server - Direct Tool Test

## Problem
SpeakMCP sagt: "The n8n skill is not listed among the available skills"

## Ursache
- Der `n8n-mcp` Server läuft ✅
- Alle 14 Tools sind aktiv ✅
- ABER: SpeakMCP erkennt die Tools nicht als "Skill"

## Warum?
In SpeakMCP sind "Skills" != "MCP Tools"

- **MCP Tools** = Einzelne Funktionen (list_workflows, create_workflow, etc.)
- **Skills** = Komplexe Workflows die mehrere Tools kombinieren

## Lösung: Direkte Tool-Nutzung

Statt zu sagen:
> "List my n8n workflows" (sucht nach Skill)

Sage:
> "Use the list_workflows tool from n8n-mcp server"

Oder noch besser:
> "Call list_workflows"

## Alternative: Skill-Wrapper erstellen

Wir können einen Skill-Wrapper erstellen der die n8n-Tools nutzt.

**Datei:** `.claude/skills/n8n-automation/skill-wrapper.json`
```json
{
  "name": "n8n-automation",
  "description": "Manage n8n workflows via voice",
  "triggers": [
    "list my n8n workflows",
    "show n8n workflows",
    "create n8n workflow",
    "run workflow"
  ],
  "tools": [
    "n8n-mcp:list_workflows",
    "n8n-mcp:get_workflow",
    "n8n-mcp:create_workflow",
    "n8n-mcp:execute_workflow",
    "n8n-mcp:activate_workflow",
    "n8n-mcp:delete_workflow"
  ],
  "prompt_template": "You are an n8n workflow automation assistant. Use the available n8n tools to help the user manage their workflows."
}
```

## Test Commands

### 1. Direct Tool Call
```
"Call list_workflows"
"Execute list_workflows tool"
"Use list_workflows from n8n-mcp"
```

### 2. Natural Language (wenn Skill-System aktiv)
```
"Show me all my n8n workflows"
"What workflows do I have in n8n?"
"List workflows"
```

### 3. Explicit MCP Tool Reference
```
"Use the n8n-mcp server to list workflows"
"Call the list_workflows tool"
```

## Nächste Schritte

1. **Teste direkte Tool-Calls** (siehe oben)
2. **Wenn das funktioniert:** n8n-Tools sind verfügbar, nur die Skill-Erkennung fehlt
3. **Wenn das nicht funktioniert:** Server-Verbindung prüfen

## Expected Behavior

**Wenn Tools funktionieren:**
```
User: "Call list_workflows"
Assistant: "Found 0 workflows in your n8n instance"
```

**Wenn Skill-System funktioniert:**
```
User: "List my n8n workflows"
Assistant: (verwendet automatisch list_workflows tool)
```

## Debugging

**Check 1: Sind Tools verfügbar?**
- Settings → MCP Tools → n8n-mcp → sollte 14 Tools zeigen

**Check 2: Kann SpeakMCP Tools aufrufen?**
- Teste: "Call list_workflows"

**Check 3: Funktioniert Skill-Matching?**
- Teste: "List my n8n workflows"
- Wenn Fehler: Skill-System erkennt n8n nicht

## Workaround (JETZT TESTEN)

Sage einfach:
> **"Call list_workflows"**

Oder:
> **"Use list_workflows tool"**

Das sollte direkt funktionieren ohne Skill-System!

