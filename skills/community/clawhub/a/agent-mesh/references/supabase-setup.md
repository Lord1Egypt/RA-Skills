# Supabase Table Setup

Use a **dedicated Supabase project** for the mesh. Do not reuse a project that contains sensitive data.

## 1. Create the table

Run in Supabase Dashboard → SQL Editor → New query:

```sql
CREATE TABLE IF NOT EXISTS agent_messages (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  from_agent TEXT NOT NULL,
  to_agent TEXT NOT NULL,
  message TEXT NOT NULL,
  priority TEXT DEFAULT 'normal' CHECK (priority IN ('low', 'normal', 'high', 'urgent')),
  metadata JSONB DEFAULT '{}',
  created_at TIMESTAMPTZ DEFAULT now()
);

-- Fast polling index (main query path: filter by recipient + time window)
CREATE INDEX IF NOT EXISTS idx_agent_messages_poll
  ON agent_messages (to_agent, created_at DESC);

-- Agent activity index
CREATE INDEX IF NOT EXISTS idx_agent_messages_from
  ON agent_messages (from_agent, created_at DESC);
```

## 2. Enable Row Level Security

RLS scopes the anon key to INSERT and SELECT only. No UPDATE or DELETE is permitted via the anon key.

```sql
ALTER TABLE agent_messages ENABLE ROW LEVEL SECURITY;

-- Agents can read messages
CREATE POLICY "agents_select" ON agent_messages
  FOR SELECT USING (true);

-- Agents can insert new messages
CREATE POLICY "agents_insert" ON agent_messages
  FOR INSERT WITH CHECK (true);

-- No UPDATE or DELETE policies — the anon key cannot modify or remove rows.
-- Maintenance (cleanup/archival) is done by the project owner via the
-- Supabase Dashboard SQL Editor using the service_role key.
```

## 3. Get credentials

1. Supabase Dashboard → Settings → API
2. **Project URL** → append `/rest/v1` → this is `MESH_SUPABASE_URL`
3. **anon public key** → this is `MESH_SUPABASE_KEY`

## Maintenance

Run these queries in the Supabase Dashboard SQL Editor (uses the service_role key, not the anon key):

Archive old messages (monthly):
```sql
DELETE FROM agent_messages
WHERE created_at < now() - INTERVAL '30 days';
```

Check table size:
```sql
SELECT count(*) as total,
  pg_size_pretty(pg_total_relation_size('agent_messages')) as size
FROM agent_messages;
```
