# ⚡ PRIORITÄT 2 QUICK START
**Erstellt:** 2025-01-01  
**Geschätzte Zeit:** 15 Minuten

---

## 🚀 SCHNELLSTART (3 BEFEHLE)

### **1. Services starten** (1 Befehl)
```powershell
cd "C:\Download\speakmcp projekt\SpeakMCP\scripts"
.\start-p2-services.ps1
```

**Was passiert:**
- ✅ Startet Docling RAG Backend (Port 8001)
- ✅ Startet n8n (Port 5678)
- ✅ Prüft ob Services laufen

---

### **2. FATONI RAG importieren** (1 Befehl)
```powershell
cd "C:\Download\speakmcp projekt\SpeakMCP\scripts"
.\import-fatoni-to-rag.ps1
```

**Was passiert:**
- ✅ Lädt fatoni.md hoch
- ✅ Testet RAG-Suche
- ✅ Verifiziert Import

---

### **3. n8n registrieren** (3 Schritte)

#### **Schritt A: API Key holen**
1. Öffne: http://localhost:5678
2. Settings → API → Create API Key
3. Kopiere den Key

#### **Schritt B: .env aktualisieren**
```powershell
cd "C:\Download\speakmcp projekt\SpeakMCP\mcp-servers\n8n-mcp-bidirectional"
notepad .env
```

Ersetze:
```env
N8N_API_KEY=your_n8n_api_key_here
```

Mit deinem echten Key:
```env
N8N_API_KEY=n8n_api_abc123xyz...
```

#### **Schritt C: In SpeakMCP registrieren**
```powershell
cd "C:\Download\speakmcp projekt\SpeakMCP\mcp-servers\n8n-mcp-bidirectional"
.\register-in-speakmcp.ps1
```

---

## ✅ FERTIG!

### **Testen:**

#### **FATONI RAG:**
In SpeakMCP (Voice oder Chat):
> "Welche FATONI Tools gibt es?"

**Erwartete Antwort:**
```
FATONI MCP Bridge bietet 33 Tools in 11 Kategorien:
- Code Tools (4): generate, review, optimize, test
- DeepALL Tools (7): ask, generate, review, explain...
- Strategy Tools (3): insights, develop, decision_matrix
...
```

#### **n8n Voice:**
In SpeakMCP (Voice):
> "List my n8n workflows"

**Erwartete Antwort:**
```
Found X workflows:
- Workflow 1: [Name]
- Workflow 2: [Name]
...
```

---

## 📁 DATEIEN

### **Neu erstellt:**
- ✅ `P2_SETUP_GUIDE.md` - Vollständige Anleitung
- ✅ `P2_QUICK_START.md` - Diese Datei
- ✅ `scripts/start-p2-services.ps1` - Auto-Start
- ✅ `scripts/import-fatoni-to-rag.ps1` - FATONI Import
- ✅ `mcp-servers/n8n-mcp-bidirectional/register-in-speakmcp.ps1` - n8n Registration

### **Bereits vorhanden:**
- ✅ `mcp-servers/knowledge/fatoni.md` - FATONI Dokumentation
- ✅ `mcp-servers/n8n-mcp-bidirectional/.env` - n8n Config
- ✅ `mcp-servers/n8n-mcp-bidirectional/QUICK_START.md` - n8n Anleitung

---

## 🔍 TROUBLESHOOTING

### **Services starten nicht?**
```powershell
# Manuell starten:

# Docling RAG
cd "C:\Download\DOCLING_RAG\docling-Rag\backend"
python backend_new_api.py

# n8n
n8n start
# Oder: docker run -it --rm -p 5678:5678 n8nio/n8n
```

### **Import schlägt fehl?**
```powershell
# Prüfe Backend
Invoke-WebRequest -Uri "http://localhost:8001/health"

# Manuell via UI
# Öffne: http://localhost:8001
# Upload: mcp-servers/knowledge/fatoni.md
```

### **n8n API Key funktioniert nicht?**
```powershell
# Test API Key
$headers = @{ "X-N8N-API-KEY" = "your_key" }
Invoke-WebRequest -Uri "http://localhost:5678/api/v1/workflows" -Headers $headers
```

---

## 📊 CHECKLISTE

- [ ] Services gestartet (Docling RAG + n8n)
- [ ] fatoni.md importiert
- [ ] RAG-Suche getestet
- [ ] n8n API Key erstellt
- [ ] .env aktualisiert
- [ ] n8n in SpeakMCP registriert
- [ ] SpeakMCP neu gestartet
- [ ] Voice Commands getestet

---

## 🎯 ERFOLGS-KRITERIEN

### **FATONI RAG:**
- ✅ RAG findet FATONI Tools (Score > 0.8)
- ✅ Automatische Tool-Erkennung funktioniert

### **n8n Voice:**
- ✅ Voice Command listet Workflows
- ✅ Workflow-Erstellung via Voice möglich

---

## 📞 SUPPORT

**Vollständige Anleitung:** `P2_SETUP_GUIDE.md`  
**n8n Docs:** `mcp-servers/n8n-mcp-bidirectional/QUICK_START.md`  
**FATONI Docs:** `mcp-servers/knowledge/fatoni.md`

---

**🎉 VIEL ERFOLG MIT PRIORITÄT 2!** 🚀

