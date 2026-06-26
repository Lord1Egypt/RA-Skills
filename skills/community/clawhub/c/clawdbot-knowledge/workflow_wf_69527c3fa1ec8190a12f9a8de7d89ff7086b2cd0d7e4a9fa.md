# OpenAI Agent Builder - SpeakMCP Workflow

## Workflow ID
```
wf_69527c3fa1ec8190a12f9a8de7d89ff7086b2cd0d7e4a9fa
```

## Agent: DeepallSpeak

**Modell:** gpt-4o  
**Temperature:** 1  
**Max Tokens:** 2048  
**Parallel Tool Calls:** ✓  

---

## Tools

### 1. callTool
Ruft ein MCP-Tool direkt auf (calls an MCP tool directly)

**Parameters:**
- `tool_name` (string): Name des Tools
- `arguments` (object): Tool-Argumente

### 2. speakmcpCallTool  
Ruft FATONI-Agenten oder Computer-Control Tools auf.

**Parameters:**
- `tool_name` (string): Name des Tools
- `arguments` (object): Tool-Argumente

---

## FATONI Agenten-Referenz (16 Agents, 33 Tools)

| Agent | Tools |
|-------|-------|
| code_agent | `fatoni_code_generate`, `fatoni_code_review`, `fatoni_code_optimize`, `fatoni_code_test` |
| strategy_agent | `fatoni_strategy_insights`, `fatoni_strategy_develop` |
| analytics_agent | `fatoni_analytics_analyze`, `fatoni_analytics_dashboard` |
| designer_agent | `fatoni_design_component` |
| orchestration_agent | `fatoni_orchestrate_task` |
| advanced_analytics_agent | `fatoni_advanced_analytics` |
| automation_agent | `fatoni_automation_create`, `fatoni_automation_execute` |
| collaboration_agent | `fatoni_collaboration_coordinate`, `fatoni_collaboration_status` |
| improvement_agent | `fatoni_improvement_analyze`, `fatoni_improvement_implement` |
| decision_agent | `fatoni_decision_analyze`, `fatoni_decision_matrix` |
| integration_agent | `fatoni_integration_connect`, `fatoni_integration_sync` |
| monitoring_agent | `fatoni_monitoring_status`, `fatoni_monitoring_alerts`, `fatoni_monitoring_logs` |
| optimization_agent | `fatoni_optimization_analyze`, `fatoni_optimization_apply` |
| security_agent | `fatoni_security_scan`, `fatoni_security_audit` |
| system_agent | `fatoni_system_health`, `fatoni_system_configure` |
| web_agent | `fatoni_web_scrape`, `fatoni_web_search`, `fatoni_web_api_call` |

---

## Computer Vision & Control Tools

| Tool | Beschreibung |
|------|--------------|
| `take_screenshot` | Erfasst den Bildschirm |
| `click_screen` | Mausklick an Koordinaten |
| `type_text` | Tastatureingabe |
| `move_mouse` | Maus bewegen |
| `drag_drop` | Drag-and-Drop |

---

## Remote Server Konfiguration

```env
SPEAKMCP_BASE_URL=http://127.0.0.1:3210
SPEAKMCP_API_KEY=c4c8f44dd96d720793721cc736777341c1a36a999adc7f01c5fd9fbf81e2e518
```

## Startup Checklist

- [x] SpeakMCP Remote URL konfiguriert ✓
- [x] API-Key in Secrets hinterlegt ✓
- [ ] Health-Check erfolgreich
- [ ] Mindestens 1 MCP-Server aktiv
- [ ] Tool-Liste gecached

---

## Quick Commands

| Command | Aktion |
|---------|--------|
| `FAST` | Nur Antwort |
| `DEBUG` | Volle Timeline |
| `TOOLS` | Liste Tools |
| `HEALTH` | Status prüfen |

---

*Version: 1.0 | Created: 2025-12-29*

