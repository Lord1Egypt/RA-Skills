# 🚀 NÄCHSTE SCHRITTE - MANUELLE AKTIONEN ERFORDERLICH

## ✅ Was bereits erledigt ist:

1. ✅ Dependencies installiert (npm install)
2. ✅ .env Datei konfiguriert mit allen Credentials
3. ✅ Setup-Anleitungen erstellt

---

## ⚠️ Was DU jetzt machen musst:

### 1️⃣ Pinecone Index erstellen (3 Minuten)

**Warum?**
Der existierende Index "deepall-unified-kb" hat **1024 Dimensionen**.
Der Self-Memory Server benötigt **1536 Dimensionen** (für OpenAI text-embedding-3-small).

**Schritte:**
1. Gehe zu: https://www.pinecone.io
2. Log in (du hast bereits einen Account)
3. Dashboard → **Create Index**
4. Fill in:
   - **Name**: `deepallspeak-skills` (exakt so!)
   - **Dimensions**: `1536` (wichtig!)
   - **Metric**: `cosine`
   - **Pod Type**: `serverless` (empfohlen) oder `p1.x1` (free tier)
   - **Region**: `us-east-1` (oder deine Region)
5. Click **"Create Index"**
6. Warte ~1 Minute bis Status = "Ready"

**Detaillierte Anleitung**: `PINECONE_SETUP_INSTRUCTIONS.md`

---

### 2️⃣ Supabase SQL Schema ausführen (2 Minuten)

**Warum?**
Das Self-Memory System benötigt 3 Tabellen in Supabase:
- `skills` - Skill-Definitionen
- `skill_executions` - Ausführungs-Historie
- `skill_feedback` - User Feedback

**Schritte:**
1. Gehe zu: https://supabase.com/dashboard
2. Wähle Projekt: `vufkhfuphdsezilzclwv` (deepall)
3. Dashboard → **SQL Editor** → **New query**
4. Kopiere den **KOMPLETTEN** Inhalt von:
   ```
   C:\Download\speakmcp projekt\SpeakMCP\.claude\skills\deepallspeak\scripts\supabase\schema.sql
   ```
5. Paste in SQL Editor
6. Click **"Run"** (oder Ctrl+Enter)
7. Erwartete Ausgabe:
   ```
   ✅ DeepAllSpeak Self-Memory System schema created successfully!
   Tables created: skills, skill_executions, skill_feedback
   ```

**Verifizieren:**
```sql
SELECT * FROM active_skills;
```
Du solltest 1 Sample Skill sehen: `analyze-sales-report`

**Detaillierte Anleitung**: `SUPABASE_SETUP_INSTRUCTIONS.md`

---

## 3️⃣ Nach den manuellen Schritten:

### Verifizierung (Augment macht das für dich)
```bash
# Pinecone Index prüfen
node -e "const { Pinecone } = require('@pinecone-database/pinecone'); const pc = new Pinecone({ apiKey: process.env.PINECONE_API_KEY }); pc.describeIndex('deepallspeak-skills').then(console.log);"

# Supabase Verbindung prüfen
node -e "const { createClient } = require('@supabase/supabase-js'); const sb = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_KEY); sb.from('skills').select('count').then(console.log);"
```

### MCP Server starten
```bash
cd "C:\Download\speakmcp projekt\SpeakMCP\.claude\skills\deepallspeak\scripts"
node skill-memory-server.js
```

### Test-Suite ausführen
```bash
node test-skill-memory.js
```

---

## 📋 Checkliste

Bevor du zu Phase 6 gehst, stelle sicher:

- [ ] Pinecone Index "deepallspeak-skills" erstellt (1536 dims, cosine)
- [ ] Pinecone Index Status = "Ready"
- [ ] Supabase SQL Schema ausgeführt
- [ ] Supabase Tabellen existieren (skills, skill_executions, skill_feedback)
- [ ] Sample Skill "analyze-sales-report" sichtbar in Supabase

---

## 🆘 Troubleshooting

### Pinecone: "Index name already exists"
**Lösung**: Wähle einen anderen Namen ODER lösche den existierenden Index.

### Supabase: "Permission denied"
**Lösung**: Stelle sicher, dass du als **Owner** des Projekts eingeloggt bist.

### Supabase: "Table already exists"
**Lösung**: Das ist OK! Das Schema verwendet `CREATE TABLE IF NOT EXISTS`.

---

## ✅ Bereit für Phase 6?

Sobald du die 2 manuellen Schritte erledigt hast, sage:

**"Phase 6"** oder **"Weiter"**

Dann führe ich die automatischen Tests aus! 🚀

