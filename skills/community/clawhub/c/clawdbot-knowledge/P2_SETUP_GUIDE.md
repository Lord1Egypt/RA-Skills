# 📋 PRIORITÄT 2 SETUP GUIDE
**Erstellt:** 2025-01-01  
**Status:** Ready to Execute

---

## 🎯 ÜBERSICHT

Priorität 2 umfasst zwei Hauptaufgaben:
1. **FATONI RAG Integration** (10 Min) - fatoni.md in Docling RAG importieren
2. **n8n Voice Automation** (5 Min) - API Key + SpeakMCP Config

**Gesamtzeit:** ~15 Minuten

---

## 📚 TASK 1: FATONI RAG INTEGRATION

### **Ziel:**
fatoni.md in Docling RAG Backend importieren für automatische FATONI-Tool-Erkennung

### **Voraussetzungen:**
- ✅ fatoni.md existiert: `mcp-servers/knowledge/fatoni.md`
- ⚠️ Docling RAG Backend muss laufen (Port 8001)

### **Schritt 1: Docling RAG Backend starten**

#### **Option A: PowerShell (Empfohlen)**
```powershell
# Terminal 1 öffnen
cd "C:\Download\DOCLING_RAG\docling-Rag\backend"
python backend_new_api.py
```

**Erwartete Ausgabe:**
```
INFO:     Uvicorn running on http://0.0.0.0:8001
INFO:     Application startup complete
```

#### **Option B: Autostart-Script**
```powershell
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd 'C:\Download\DOCLING_RAG\docling-Rag\backend'; python backend_new_api.py"
```

### **Schritt 2: Backend Health Check**
```powershell
# In neuem Terminal
Invoke-WebRequest -Uri "http://localhost:8001/health" -UseBasicParsing
```

**Erwartete Antwort:**
```json
{"status": "healthy"}
```

### **Schritt 3: fatoni.md importieren**

#### **Option A: Via API (Empfohlen)**
```powershell
$fatonPath = "C:\Download\speakmcp projekt\SpeakMCP\mcp-servers\knowledge\fatoni.md"
$content = Get-Content $fatonPath -Raw

# Upload via API
Invoke-WebRequest -Uri "http://localhost:8001/api/documents/upload" `
  -Method POST `
  -ContentType "application/json" `
  -Body (@{
    filename = "fatoni.md"
    content = $content
    namespace = "knowledge"
  } | ConvertTo-Json)
```

#### **Option B: Via UI**
1. Öffne: http://localhost:8001
2. Gehe zu "Documents" → "Upload"
3. Wähle: `mcp-servers/knowledge/fatoni.md`
4. Namespace: `knowledge`
5. Klicke "Upload"

### **Schritt 4: Verifizieren**
```powershell
# Suche nach FATONI Tools
Invoke-WebRequest -Uri "http://localhost:8001/api/search" `
  -Method POST `
  -ContentType "application/json" `
  -Body (@{
    query = "Welche FATONI Tools gibt es?"
    namespace = "knowledge"
    top_k = 5
  } | ConvertTo-Json)
```

**Erwartetes Ergebnis:**
```json
{
  "results": [
    {
      "content": "FATONI MCP Bridge bietet 33 Tools...",
      "score": 0.89,
      "metadata": {
        "source": "fatoni.md",
        "namespace": "knowledge"
      }
    }
  ]
}
```

---

## 🤖 TASK 2: N8N VOICE AUTOMATION

### **Ziel:**
n8n MCP Server in SpeakMCP registrieren für Voice-gesteuerte Workflow-Automation

### **Voraussetzungen:**
- ✅ Setup komplett (Dependencies, Config, Docs)
- ⚠️ n8n muss laufen (Port 5678)
- ⚠️ API Key benötigt

### **Schritt 1: n8n starten**

#### **Prüfen ob n8n installiert ist:**
```powershell
n8n --version
```

#### **n8n starten:**
```powershell
# Option A: Standard
n8n start

# Option B: Mit Custom Port
n8n start --port 5678

# Option C: Docker
docker run -it --rm --name n8n -p 5678:5678 n8nio/n8n
```

**Erwartete Ausgabe:**
```
n8n ready on http://localhost:5678
```

### **Schritt 2: API Key erstellen**

1. **Öffne n8n:** http://localhost:5678
2. **Login/Registrieren** (falls noch nicht geschehen)
3. **Navigiere zu:** Settings (⚙️) → API
4. **Klicke:** "Create API Key"
5. **Kopiere den Key** (z.B. `n8n_api_abc123xyz...`)

### **Schritt 3: .env aktualisieren**
```powershell
cd "C:\Download\speakmcp projekt\SpeakMCP\mcp-servers\n8n-mcp-bidirectional"

# .env bearbeiten
notepad .env
```

**Ersetze:**
```env
N8N_API_KEY=your_n8n_api_key_here
```

**Mit:**
```env
N8N_API_KEY=n8n_api_abc123xyz...
```

### **Schritt 4: SpeakMCP Config aktualisieren**

#### **Option A: Auto-Script (Empfohlen)**
```powershell
cd "C:\Download\speakmcp projekt\SpeakMCP\mcp-servers\n8n-mcp-bidirectional"

# Erstelle Register-Script
@"
`$configPath = "`$env:APPDATA\app.speakmcp\config.json"
`$config = Get-Content `$configPath | ConvertFrom-Json

if (-not `$config.mcpServers) {
    `$config | Add-Member -MemberType NoteProperty -Name "mcpServers" -Value @{}
}

`$config.mcpServers | Add-Member -MemberType NoteProperty -Name "n8n-automation" -Value @{
    command = "python"
    args = @("-m", "n8n_mcp_server")
    cwd = "C:\Download\speakmcp projekt\SpeakMCP\mcp-servers\n8n-mcp-bidirectional"
    disabled = `$false
} -Force

`$config | ConvertTo-Json -Depth 10 | Set-Content `$configPath
Write-Host "✅ n8n-automation registered!"
"@ | Out-File register-n8n.ps1

# Ausführen
.\register-n8n.ps1
```

#### **Option B: Manuell**
1. Öffne: `%APPDATA%\app.speakmcp\config.json`
2. Füge hinzu:
```json
{
  "mcpServers": {
    "n8n-automation": {
      "command": "python",
      "args": ["-m", "n8n_mcp_server"],
      "cwd": "C:\\Download\\speakmcp projekt\\SpeakMCP\\mcp-servers\\n8n-mcp-bidirectional",
      "disabled": false
    }
  }
}
```

### **Schritt 5: SpeakMCP neu starten**
```powershell
# Stoppe SpeakMCP
Get-Process -Name "electron*" | Stop-Process -Force

# Starte neu
cd "C:\Download\speakmcp projekt\SpeakMCP\apps\desktop"
pnpm run dev
```

### **Schritt 6: Testen**

1. **Öffne SpeakMCP**
2. **Prüfe MCP Tools:** Settings → MCP Tools → "n8n-automation" (sollte ✅ connected sein)
3. **Voice Test:**
   - Drücke `Ctrl` (Voice Mode)
   - Sage: **"List my n8n workflows"**

**Erwartetes Ergebnis:**
```
Found X workflows:
- Workflow 1: [Name]
- Workflow 2: [Name]
...
```

---

## 🔍 TROUBLESHOOTING

### **Docling RAG Backend startet nicht**
```powershell
# Prüfe Python
python --version  # Sollte 3.8+

# Prüfe Dependencies
cd "C:\Download\DOCLING_RAG\docling-Rag\backend"
pip install -r requirements.txt

# Prüfe .env
Get-Content .env | Select-String "PINECONE|OPENAI"

# Logs prüfen
python backend_new_api.py
```

### **n8n startet nicht**
```powershell
# Installiere n8n (falls nicht vorhanden)
npm install -g n8n

# Oder via Docker
docker pull n8nio/n8n
docker run -it --rm -p 5678:5678 n8nio/n8n
```

### **API Key funktioniert nicht**
```powershell
# Test API Key
$headers = @{
    "X-N8N-API-KEY" = "your_api_key_here"
}
Invoke-WebRequest -Uri "http://localhost:5678/api/v1/workflows" -Headers $headers
```

---

## ✅ ERFOLGS-KRITERIEN

### **FATONI RAG:**
- [x] Docling RAG Backend läuft (Port 8001)
- [x] fatoni.md importiert
- [x] RAG-Suche findet FATONI Tools
- [x] Score > 0.8 für "FATONI Tools"

### **n8n Voice:**
- [x] n8n läuft (Port 5678)
- [x] API Key erstellt
- [x] .env aktualisiert
- [x] SpeakMCP Config aktualisiert
- [x] Voice Command funktioniert

---

## 📊 FINALE CHECKLISTE

- [ ] Docling RAG Backend gestartet
- [ ] fatoni.md importiert
- [ ] RAG-Suche getestet
- [ ] n8n gestartet
- [ ] n8n API Key erstellt
- [ ] .env aktualisiert
- [ ] SpeakMCP Config aktualisiert
- [ ] SpeakMCP neu gestartet
- [ ] Voice Commands getestet

---

**🎯 NÄCHSTER SCHRITT: Starte Docling RAG Backend!**

```powershell
cd "C:\Download\DOCLING_RAG\docling-Rag\backend"
python backend_new_api.py
```

