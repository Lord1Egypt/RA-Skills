# Supabase Setup - Manuelle Schritte

## 1. Supabase Account & Projekt

Gehe zu: **https://supabase.com**

### Schritte:
1. **Sign up / Log in**
2. Click **"New Project"**
3. Fill in:
   - **Name**: `deepallspeak-memory`
   - **Database Password**: `[GENERIERE STARKES PASSWORD - SPEICHERE ES SICHER!]`
   - **Region**: Wähle nächstgelegene Region (z.B. `eu-central-1` für Europa)
4. Click **"Create new project"**
5. Warte ~2 Minuten (Projekt wird initialisiert)

### Empfohlenes Password:
```
Generiere ein starkes Password mit mindestens:
- 16 Zeichen
- Groß- und Kleinbuchstaben
- Zahlen
- Sonderzeichen

Beispiel-Generator (PowerShell):
-1..16 | ForEach-Object { [char](Get-Random -Minimum 33 -Maximum 126) } | Join-String

WICHTIG: Speichere das Password in einem Password Manager!
```

---

## 2. Credentials holen

### Dashboard → Settings → API

Kopiere folgende Werte:

1. **Project URL**:
   ```
   https://xxxxx.supabase.co
   ```
   (Ersetze xxxxx mit deiner Project ID)

2. **Service Role Key** (FÜR SERVER-SIDE!):
   ```
   eyJ... (sehr langer String)
   ```
   ⚠️ **WICHTIG**: Verwende den **service_role** Key, NICHT den anon/public Key!
   
   Der service_role Key hat volle Rechte und sollte nur server-side verwendet werden.

---

## 3. SQL Schema ausführen

### Dashboard → SQL Editor → New query

1. Click **"New query"** (oder **"+"** Button)
2. Kopiere den **KOMPLETTEN** Inhalt von:
   ```
   C:\Download\speakmcp projekt\SpeakMCP\.claude\skills\deepallspeak\scripts\supabase\schema.sql
   ```
3. Paste in SQL Editor
4. Click **"Run"** (oder Ctrl+Enter)

### Erwartete Ausgabe:
```
✅ DeepAllSpeak Self-Memory System schema created successfully!

Tables created:
  - skills (with 9 indexes)
  - skill_executions (with 5 indexes)
  - skill_feedback (with 4 indexes)

Views created:
  - active_skills
  - recent_executions

Triggers created:
  - Auto-update timestamps
  - Auto-update skill statistics

Next steps:
  1. Configure Supabase connection in .env
  2. Create Pinecone index (see pinecone.md)
  3. Start skill-memory-server.js
  4. Test with skill_create tool
```

---

## 4. Verifizieren

### In SQL Editor, run:
```sql
SELECT * FROM active_skills;
```

### Erwartetes Ergebnis:
Du solltest **1 Sample Skill** sehen:
- **Name**: `analyze-sales-report`
- **Category**: `business_intelligence`
- **Tags**: `['sales', 'analytics', 'business', 'quarterly']`

Wenn du diesen Skill siehst, ist das Schema korrekt installiert! ✅

---

## 5. Credentials in .env eintragen

**Augment wird dies für dich tun!**

Die Datei ist: `C:\Download\speakmcp projekt\SpeakMCP\mcp-servers\.env`

Folgende Werte werden eingetragen:
```bash
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=eyJ...[DEIN SERVICE ROLE KEY]
```

---

## 6. Troubleshooting

### Problem: "Permission denied" beim Schema ausführen
**Lösung**: Stelle sicher, dass du als **Owner** des Projekts eingeloggt bist.

### Problem: "Table already exists"
**Lösung**: Das ist OK! Das Schema verwendet `CREATE TABLE IF NOT EXISTS`.

### Problem: "Function already exists"
**Lösung**: Das Schema verwendet `CREATE OR REPLACE FUNCTION`.

---

## 7. Nächste Schritte

Nach erfolgreichem Setup:
1. ✅ Supabase Projekt erstellt
2. ✅ SQL Schema ausgeführt
3. ✅ Credentials kopiert
4. ⏭️ **Weiter zu**: `PINECONE_SETUP_INSTRUCTIONS.md`

---

**Bereit für Pinecone Setup!** 🚀

