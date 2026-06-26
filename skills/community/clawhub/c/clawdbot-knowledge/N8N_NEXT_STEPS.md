# 🔍 n8n MCP Server - Nächste Schritte

## ⚠️ AKTUELLES PROBLEM

**Symptom:** SpeakMCP sagt "Tool fehlt" wenn du nach n8n Workflows fragst

**Bedeutung:** Der n8n MCP Server ist NICHT verbunden

---

## 🎯 SOFORT AUSFÜHREN

### **Schritt 1: Diagnose-Skript ausführen**

```powershell
cd "C:\Download\speakmcp projekt\SpeakMCP"
.\diagnose-n8n-mcp.ps1
```

**Dann:** Sende mir die KOMPLETTE Ausgabe!

---

## 🔧 MÖGLICHE PROBLEME & LÖSUNGEN

### **Problem 1: Server ist disabled**
**Symptom:** Diagnose zeigt "disabled = true"

**Lösung:**
```powershell
$config = Get-Content "$env:APPDATA\app.speakmcp\config.json" | ConvertFrom-Json
$config.mcpServers.'n8n-automation'.disabled = $false
$config | ConvertTo-Json -Depth 10 | Set-Content "$env:APPDATA\app.speakmcp\config.json"

# Restart SpeakMCP
Get-Process -Name "electron*" | Stop-Process -Force
cd "C:\Download\speakmcp projekt\SpeakMCP\apps\desktop"
pnpm run dev
```

---

### **Problem 2: cwd Feld fehlt**
**Symptom:** Diagnose zeigt "cwd field MISSING"

**Lösung:**
```powershell
$config = Get-Content "$env:APPDATA\app.speakmcp\config.json" | ConvertFrom-Json
$config.mcpServers.'n8n-automation' | Add-Member -NotePropertyName 'cwd' -NotePropertyValue 'C:\Download\speakmcp projekt\SpeakMCP\mcp-servers\n8n-mcp-bidirectional' -Force
$config | ConvertTo-Json -Depth 10 | Set-Content "$env:APPDATA\app.speakmcp\config.json"

# Restart SpeakMCP
Get-Process -Name "electron*" | Stop-Process -Force
cd "C:\Download\speakmcp projekt\SpeakMCP\apps\desktop"
pnpm run dev
```

---

### **Problem 3: Server nicht registriert**
**Symptom:** Diagnose zeigt "n8n-automation NOT FOUND"

**Lösung:**
```powershell
cd "C:\Download\speakmcp projekt\SpeakMCP\mcp-servers\n8n-mcp-bidirectional"
.\register-in-speakmcp.ps1

# Restart SpeakMCP
Get-Process -Name "electron*" | Stop-Process -Force
cd "C:\Download\speakmcp projekt\SpeakMCP\apps\desktop"
pnpm run dev
```

---

### **Problem 4: Python-Fehler**
**Symptom:** Diagnose zeigt Fehler beim Server-Start

**Lösung:**
```powershell
# Prüfe ob mcp package installiert ist
pip list | findstr mcp

# Wenn nicht:
pip install mcp

# Teste Server manuell
cd "C:\Download\speakmcp projekt\SpeakMCP\mcp-servers\n8n-mcp-bidirectional"
python -m n8n_mcp_server
```

---

## 📋 CHECKLISTE

Nach jeder Lösung:

- [ ] SpeakMCP neugestartet
- [ ] 30 Sekunden gewartet
- [ ] Settings → MCP Tools geöffnet
- [ ] Nach "n8n-automation" gesucht
- [ ] Status geprüft (grün/rot/fehlt)

---

## 🎤 WENN ALLES FUNKTIONIERT

**Test Voice Command:**
1. Press `Ctrl`
2. Say: "List my n8n workflows"

**Erwartete Antwort:**
```
Found 0 workflows
```
(Weil deine n8n Instanz leer ist)

---

## 📞 WENN NICHTS HILFT

**Sende mir:**
1. Komplette Ausgabe von `diagnose-n8n-mcp.ps1`
2. Screenshot von Settings → MCP Tools
3. Fehlermeldung wenn du "List my n8n workflows" sagst

**Dann kann ich:**
- Das genaue Problem identifizieren
- Eine spezifische Lösung geben
- Eventuell einen alternativen Ansatz versuchen

---

## 🔄 NUCLEAR OPTION (Letzter Ausweg)

**Wenn GAR NICHTS funktioniert:**

```powershell
# 1. Backup
Copy-Item "$env:APPDATA\app.speakmcp\config.json" "$env:APPDATA\app.speakmcp\config.backup_manual.json"

# 2. Komplett neu registrieren
$config = Get-Content "$env:APPDATA\app.speakmcp\config.json" | ConvertFrom-Json

# Entferne alte Einträge
if ($config.mcpServers.'n8n-automation') {
    $config.mcpServers.PSObject.Properties.Remove('n8n-automation')
}

# Füge komplett neu hinzu
$n8nServer = @{
    command = "python"
    args = @("-m", "n8n_mcp_server")
    cwd = "C:\Download\speakmcp projekt\SpeakMCP\mcp-servers\n8n-mcp-bidirectional"
    disabled = $false
}

$config.mcpServers | Add-Member -NotePropertyName 'n8n-automation' -NotePropertyValue $n8nServer -Force

# Speichern
$config | ConvertTo-Json -Depth 10 | Set-Content "$env:APPDATA\app.speakmcp\config.json"

# Komplett neu starten
Get-Process -Name "electron*" | Stop-Process -Force
Start-Sleep -Seconds 5
cd "C:\Download\speakmcp projekt\SpeakMCP\apps\desktop"
pnpm run dev
```

**Dann 30 Sekunden warten und prüfen!**

---

## ✅ ERFOLGS-KRITERIEN

Du weißt dass es funktioniert wenn:

1. ✅ Settings → MCP Tools zeigt "n8n-automation" (grün)
2. ✅ Voice Command "List my n8n workflows" antwortet
3. ✅ Keine Fehlermeldung "Tool fehlt"

---

**🎯 JETZT: Führe `diagnose-n8n-mcp.ps1` aus und sende mir die Ausgabe!**

