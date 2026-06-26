# Blog Schema — Supabase Setup

For blog auto-publishing to work, your Supabase project needs a `blog_articles` table and your Netlify site needs to query it at build time.

## Supabase Table: blog_articles

```sql
create table blog_articles (
  id uuid default gen_random_uuid() primary key,
  created_at timestamptz default now(),
  title text not null,
  slug text not null unique,
  excerpt text,
  content text not null,
  published_at date,
  og_image text,
  status text default 'published'
);

-- Enable RLS
alter table blog_articles enable row level security;

-- Public can read published posts
create policy "Public read"
  on blog_articles for select
  using (status = 'published');

-- Service role can insert/update
create policy "Service role write"
  on blog_articles for all
  using (auth.role() = 'service_role');
```

## Environment Variables Required

Add these to `~/.openclaw/.env`:

```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_KEY=your-service-role-key
NETLIFY_DEPLOY_HOOK=https://api.netlify.com/build_hooks/your-hook-id
```

- **SUPABASE_URL**: Project Settings → API → Project URL
- **SUPABASE_SERVICE_KEY**: Project Settings → API → service_role (secret)
- **NETLIFY_DEPLOY_HOOK**: Netlify → Site → Settings → Build & deploy → Build hooks → Add build hook

## How Blog Publishing Works

1. Evo writes a blog post in markdown format
2. Calls `publish-blog-post.js` with the markdown file
3. Script inserts a row into `blog_articles` via Supabase API
4. Script POSTs to the Netlify deploy hook → triggers a site rebuild
5. Your Netlify site fetches blog posts from Supabase at build time and renders them as static HTML

## Site Integration

Your Netlify site needs to query `blog_articles` at build time. If you're using the Xero site template, this is already wired. For a custom site, fetch from:

```
GET {SUPABASE_URL}/rest/v1/blog_articles?status=eq.published&order=published_at.desc
Headers:
  apikey: your-anon-key
  Authorization: Bearer your-anon-key
```

## Blog Post Markdown Format

Posts must follow this format for `publish-blog-post.js` to parse them:

```markdown
# Post Title Here
**Slug:** my-post-slug
**Date:** 2026-04-18
**Excerpt:** One sentence that describes the post.
---
Full post content in markdown starts here...
```

## Optional: Skip Blog Publishing

If you don't have Supabase/Netlify set up, the blog cron will simply be skipped. All other pipeline channels (TikTok, Twitter, newsletter, briefings) work independently. You can add blog publishing later without re-running the full setup.
