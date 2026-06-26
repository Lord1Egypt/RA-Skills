# ⚠️ MANUAL SUPABASE SETUP REQUIRED

## Problem
Die Tabellen `skills`, `skill_executions`, `skill_feedback` existieren **NICHT** in Supabase.

Fehler: `PGRST205 - Could not find the table 'public.skills' in the schema cache`

---

## ✅ LÖSUNG: SQL Schema manuell ausführen

### Schritt 1: Supabase Dashboard öffnen

1. Gehe zu: https://supabase.com/dashboard
2. Wähle dein Projekt: **vufkhfuphdsezilzclwv**
3. Klicke auf **SQL Editor** (linke Sidebar)

---

### Schritt 2: SQL Schema ausführen

1. Klicke auf **New query**
2. Öffne die Datei:
   ```
   C:\Download\speakmcp projekt\SpeakMCP\.claude\skills\deepallspeak\scripts\supabase\schema.sql
   ```
3. Kopiere den **gesamten Inhalt** (14.830 Zeichen)
4. Füge ihn in den SQL Editor ein
5. Klicke auf **Run** (oder drücke `Ctrl+Enter`)

---

### Schritt 3: Verifizieren

Nach der Ausführung solltest du sehen:

```
✅ 3 Tables created:
   - skills
   - skill_executions
   - skill_feedback

✅ 18 Indexes created
✅ 2 Views created:
   - active_skills
   - recent_executions

✅ 2 Triggers created:
   - update_skills_updated_at
   - update_skill_stats_on_execution
```

---

### Schritt 4: Test

Führe aus:
```bash
cd "C:\Download\speakmcp projekt\SpeakMCP\.claude\skills\deepallspeak\scripts"
node check-tables.js
```

Erwartete Ausgabe:
```
✅ skills table exists
✅ skill_executions table exists
✅ skill_feedback table exists
```

---

## Alternative: Supabase CLI

Wenn du die Supabase CLI installiert hast:

```bash
supabase login
supabase link --project-ref vufkhfuphdsezilzclwv
supabase db push --file "C:\Download\speakmcp projekt\SpeakMCP\.claude\skills\deepallspeak\scripts\supabase\schema.sql"
```

---

## Nach dem Setup

Sobald die Tabellen existieren, kannst du:

1. **Ersten Skill erstellen**:
   ```bash
   node test-create-skill.js
   ```

2. **MCP Server testen**:
   ```bash
   node test-skill-memory.js
   ```

3. **In SpeakMCP verwenden**:
   - Server ist bereits registriert
   - Starte SpeakMCP neu
   - Verwende Tools wie `skill_create`, `skill_search`, etc.

---

## ⚠️ WICHTIG

**OHNE** die manuellen Schritte 1-3 wird **NICHTS** funktionieren!

Die Tabellen **MÜSSEN** in Supabase existieren, bevor der MCP Server funktioniert.

---

**Soll ich dir helfen, das SQL Schema zu kopieren?** ✅

