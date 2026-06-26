# FuelWatch Backend Plan (Phase 2)

## Stack
- **Database + API:** Supabase (free tier — 500MB, unlimited reads)
- **Hosting:** Vercel (free tier, auto-deploy from git)
- **Domain:** fuelwatch.co.za (register when validated)

## Supabase schema

```sql
create table reports (
  id uuid default gen_random_uuid() primary key,
  station_name text not null,
  suburb text not null,
  fuel_type text not null,  -- 'Diesel 500ppm' | 'Diesel 50ppm' | 'Petrol 95' | 'Petrol 93'
  price numeric(6,2),       -- null if not reported
  availability text not null, -- 'has' | 'low' | 'out'
  created_at timestamptz default now(),
  -- future: upvotes int default 0, reporter_ip text
);

create index on reports (suburb);
create index on reports (created_at desc);
```

## Migration from localStorage

Replace in app.js:
```js
// OLD: localStorage
function loadReports() { return JSON.parse(localStorage.getItem(STORAGE_KEY)) || []; }
function saveReports(r) { localStorage.setItem(STORAGE_KEY, JSON.stringify(r)); }

// NEW: Supabase
const { createClient } = supabase;
const db = createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

async function loadReports() {
  const { data } = await db.from('reports').select('*').order('created_at', { ascending: false }).limit(200);
  return data || [];
}

async function saveReport(report) {
  await db.from('reports').insert([report]);
}
```

Add to index.html `<head>`:
```html
<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
```

## Phase 2 features
- Real-time updates (Supabase subscriptions)
- Upvote/confirm reports
- Alert me when station near me gets restocked
- Station owner verified updates
- Trucker route view (available diesel along N1/N3)
