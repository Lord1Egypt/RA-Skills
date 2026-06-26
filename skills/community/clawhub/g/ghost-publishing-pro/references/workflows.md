# Ghost Publishing Workflows

Proven workflows from real production use on a Ghost Pro site.

---

## Credentials Setup

**Credentials file:** `~/.openclaw/credentials/ghost-admin.json`
```json
{
  "url": "https://your-site.ghost.io",
  "key": "id:secret"
}
```

**Get your key:** Ghost Admin > Settings > Integrations > Add custom integration > Admin API Key.

This single integration token covers the full publishing workflow: post creation, updates, image uploads, newsletter sends, batch operations, analytics reads.

---

## Workflow 1: Write and Publish a New Article

1. Generate JWT token (see api.md)
2. POST to `/posts/?source=html` with:
   - `status: "draft"` to start
   - Full HTML content (see HTML Content Guidelines below)
   - Tags, excerpt, feature_image if ready
3. Review in Ghost admin browser if needed
4. Update post: PUT with `status: "published"` and `email_segment: "all"` to publish + send newsletter simultaneously

**Critical:** Ghost publish + newsletter send is ONE action. Don't publish first then try to send separately — you'll need to use Ghost admin to resend, which is clunky.

---

## Workflow 2: Migrate from Squarespace (Proven — full blog migrated in one afternoon)

**What you'll need:**
- Squarespace XML export (Settings → Advanced → Import/Export)
- Node.js script to parse and batch import

**The migration script pattern (Node.js):**

This workflow requires one third-party npm package. Install it before running:

```bash
npm install fast-xml-parser@5.7.2
```

```js
const { XMLParser } = require('fast-xml-parser');
// Parse items from channel.item array
// For each post: clean HTML, generate slug, set published_at from pubDate
// POST to Ghost API with 500ms delay between calls
```

**Key cleanup steps:**
1. Strip Squarespace wrapper divs and widget markup
2. Convert Squarespace image URLs → either re-upload to Ghost or keep external
3. Clean slugs (remove date prefixes like `/2015/10/25/`, normalize to hyphen-case)
4. Set `published_at` from original post date to preserve chronology
5. Map categories → Ghost tags

**WordPress migration:** Same pattern, different XML schema. WordPress uses `<wp:post_name>` for slugs, `<content:encoded>` for HTML body.

**Substack migration:** Export CSV + HTML files from Substack dashboard. Parse CSV for metadata, read HTML files for content. Same batch POST pattern.

---

## Workflow 3: Batch Update Existing Posts

Use case: Update feature images, fix formatting across many posts, add tags, change slugs.

```js
// 1. Fetch all posts with pagination
GET /posts/?limit=15&page=1&fields=id,title,slug,status,updated_at,feature_image

// 2. Loop through pages until meta.pagination.next is null

// 3. For each post that needs updating:
PUT /posts/{id}/ with updated_at from fetched post
// 500ms delay between calls
```

**Always include `updated_at`** from the fetched post — Ghost uses optimistic locking and will 409 without it.

---

## Workflow 4: Upload Image and Set as Feature Image

```bash
# 1. Upload image
curl -X POST "{url}/ghost/api/admin/images/upload/" \
  -H "Authorization: Ghost {token}" \
  -F "file=@/path/to/image.jpg" \
  -F "purpose=image"
# Returns image URL

# 2. Set on post
curl -X PUT "{url}/ghost/api/admin/posts/{id}/?source=html" \
  -H "Authorization: Ghost {token}" \
  -H "Content-Type: application/json" \
  -d '{"posts":[{"feature_image":"https://returned-url","updated_at":"..."}]}'
```

---

## HTML Content Guidelines

Ghost accepts raw HTML via `?source=html`. Inject a full HTML string as the `html` field.

**Standard structure:**
```html
<p>Opening paragraph.</p>

<h2>Section heading</h2>

<p>Body paragraph.</p>

<hr>

<p>Closing paragraph.</p>
```

**Book-style typography** (for literary/fiction content):
```html
<div style="font-family: Georgia, serif; text-align: justify; hyphens: auto; -webkit-hyphens: auto; lang='en'">
  <p style="text-indent: 2em; margin-bottom: 0; margin-top: 0;">First paragraph of story.</p>
  <p style="text-indent: 2em; margin-bottom: 0; margin-top: 0;">Second paragraph — no gap between paragraphs, indent only.</p>
</div>
```

Key book-style rules:
- `text-align: justify` + `hyphens: auto` — justified text with hyphenation
- `text-indent: 2em` on paragraphs — indent instead of gap
- `margin-bottom: 0; margin-top: 0` — no paragraph spacing
- Wrap in `lang="en"` for hyphenation to work
- `font-family: Georgia, serif` for book feel

**YouTube embed (responsive):**
```html
<figure class="kg-card kg-embed-card">
  <iframe width="560" height="315"
    src="https://www.youtube-nocookie.com/embed/{VIDEO_ID}"
    frameborder="0"
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
    allowfullscreen>
  </iframe>
</figure>
```

**Email newsletter rules (critical):**
- JS is stripped in Ghost email delivery — no interactive elements
- Subscribe widgets are web-only — stripped from email
- Ghost wraps articles in its own email template — don't add email headers/footers in HTML
- Keep email-safe: no `<script>`, no `position: fixed`, no complex CSS
- Ghost email send is one-shot — publish + `email_segment` in the same API call

**Footer template (standard newsletter CTA):**
```html
<hr>
<p><em>If you're reading this on the web, you can get articles straight to your inbox — 
no spam, unsubscribe anytime.</em></p>
```

---

## Workflow 5: DOCX Fiction/Essay Collection Batch Import

Use case: Import a collection of stories or essays from a DOCX as individual Ghost posts with book-style formatting.

**Source:** DOCX converted to HTML, then parsed piece by piece.

**Story detection:** Each piece starts with an `<h2>` tag (title). Split the full HTML on `<h2>` boundaries.

**Per-post structure:**
```html
<!-- Inline title -->
<h1 style="font-family: Georgia, serif; text-align: center;">{TITLE}</h1>
<h3 style="text-align: center; color: #666;">{AUTHOR NAME}</h3>
<hr>

<!-- Book-style body -->
<div style="font-family: Georgia, serif; text-align: justify; hyphens: auto; -webkit-hyphens: auto;" lang="en">
  {PARAGRAPHS with text-indent styling}
</div>

<!-- YouTube embed if applicable -->
{EMBED}

<!-- Footer -->
<hr>
<p><em>Footer text here.</em></p>
```

**Tags:** Match your collection name and content type (e.g., `["Fiction", "Short Stories"]`)

**Slug pattern:** `story-title` or `story-title-author-name`

**Status:** `draft` initially — review before publishing.

---

## Common Pitfalls

- **409 on PUT** — Always re-fetch post to get current `updated_at` before updating
- **Email not sending** — `email_segment` only fires on first publish. If post was already published, use Ghost admin to send manually
- **HTML rendering wrong** — Always use `?source=html` parameter on POST/PUT
- **Token expired mid-batch** — Regenerate token every 50 posts in long batch operations
- **Rate limiting** — Add 500ms delay between API calls in batch scripts; Ghost will 429 without it
- **Image upload fails** — Check file size (under 10MB), format (JPG/PNG/GIF/WebP), and that purpose field is set

---

## Workflow 6: YouTube Video Post (Thumbnail + Embed)

Use case: Publish a post built around a YouTube video — custom thumbnail as feature image, embedded player, structured content around it.

**Step 1: Upload your custom thumbnail as the feature image**
```bash
curl -s -X POST "{url}/ghost/api/admin/images/upload/" \
  -H "Authorization: Ghost {token}" \
  -F "file=@/path/to/thumbnail-1280x720.jpg" \
  -F "purpose=image"
# Copy the returned URL
```

**Step 2: Create the post with embed + feature image**
```json
{
  "posts": [{
    "title": "Video Title",
    "html": "<p>Intro paragraph setting up the video.</p>\n\n<figure class=\"kg-card kg-embed-card\"><iframe width=\"560\" height=\"315\" src=\"https://www.youtube-nocookie.com/embed/{VIDEO_ID}\" frameborder=\"0\" allow=\"accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture\" allowfullscreen></iframe></figure>\n\n<p>Description or transcript excerpt below the video.</p>",
    "feature_image": "https://your-ghost-site.com/content/images/returned-thumbnail-url.jpg",
    "status": "published",
    "email_segment": "all",
    "tags": [{"name": "Video"}]
  }]
}
```

**YouTube embed rules:**
- Use `youtube-nocookie.com` not `youtube.com` — avoids cookie consent banners
- `kg-card kg-embed-card` classes tell Ghost to render it as an embed card (proper responsive sizing)
- Thumbnail dimensions: 1280×720 (16:9) — Ghost crops to this for feature image display
- The embed renders in email but autoplay is blocked — acceptable behavior

---

## Workflow 7: Content Formatting Recipes

Copy-paste HTML patterns for common Ghost content needs.

**Pull quote:**
```html
<blockquote style="border-left: 4px solid #c8a84b; padding-left: 1em; font-style: italic; color: #555;">
  The sentence you want to emphasize.
</blockquote>
```

**Callout box:**
```html
<div style="background: #f9f5e7; border: 1px solid #e8d5a3; border-radius: 4px; padding: 1em 1.25em; margin: 1.5em 0;">
  <strong>Note:</strong> Your callout text here.
</div>
```

**Section separator (thematic break):**
```html
<hr style="border: none; border-top: 1px solid #e0e0e0; margin: 2em 0;">
```

**Image with caption:**
```html
<figure>
  <img src="https://image-url.jpg" alt="Description">
  <figcaption style="text-align: center; font-size: 0.85em; color: #888; margin-top: 0.5em;">Caption text here.</figcaption>
</figure>
```

**Footnote-style aside:**
```html
<p style="font-size: 0.85em; color: #777; border-top: 1px solid #eee; padding-top: 0.75em; margin-top: 2em;">
  ¹ Footnote or clarification text here.
</p>
```

**Two-column layout (web-only — stripped in email):**
```html
<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.5em;">
  <div><p>Left column content.</p></div>
  <div><p>Right column content.</p></div>
</div>
```

---

## Workflow 8: Newsletter Strategy Patterns

Hard-won Ghost email lessons from production use.

**The one-shot rule:**
`email_segment` only fires on the FIRST time a post is published. If you publish without it and then try to add it — Ghost won't send. You must use Ghost admin to manually trigger a resend, and even then it's unreliable. Always include `email_segment` in the same call that sets `status: "published"`.

**Email-safe content:**
Ghost sends HTML email through its own template wrapper. What gets stripped:
- All `<script>` tags
- `position: fixed` and `position: sticky`
- Subscribe portal widgets (`##subscribe##`)
- Custom fonts loaded via `@font-face`
- External CSS files

What works in email:
- Inline styles
- Standard HTML (p, h2, h3, ul, ol, blockquote, hr, img)
- YouTube embeds (renders as linked thumbnail in most clients)
- Web fonts from Google Fonts loaded inline

**Subscriber segments:**
- `"email_segment": "all"` — free + paid subscribers
- `"email_segment": "free"` — free tier only
- `"email_segment": "paid"` — paid subscribers only
- Omit `email_segment` entirely — no email sent (web publish only)

**Member-only content:**
Set `"visibility": "members"` on a post to restrict it to logged-in members. `"visibility": "paid"` restricts to paying subscribers. Default is `"public"`.

**Scheduling for time zones:**
Ghost stores and sends in UTC. If your audience is US-based and you want delivery at 9AM Eastern, set `published_at` to `T14:00:00.000Z` (EST) or `T13:00:00.000Z` (EDT).

**Subject line:**
Ghost uses the post title as the email subject. Keep titles under 60 characters for mobile preview. Avoid ALL CAPS and excessive punctuation — triggers spam filters.

---

## Workflow 9: Ghost + OpenClaw Integration Patterns

How to wire Ghost into agent workflows so publishing becomes automatic.

**Cron-based publishing schedule:**
Create a cron job in OpenClaw that checks a drafts queue and publishes on a schedule:
```
# Check for scheduled posts every morning
openclaw cron add "ghost-publish-check" "0 9 * * *" "Check Ghost drafts queue and publish any posts due today"
```

In the cron prompt, instruct the agent to:
1. Fetch posts filtered by `status:scheduled` and `published_at` in today's range
2. Verify content looks correct
3. Update status to `published` with `email_segment` if newsletter delivery is intended

**Memory file for publishing cadence:**
Keep a `memory/publishing.md` file that tracks:
```markdown
## Publishing Log
- Last published: 2026-03-16 — "Post Title"
- Next scheduled: 2026-03-23
- Subscriber count: 847 (as of 2026-03-16)
- Total posts: 12
```

Update this after every publish. Use it to avoid gaps and track cadence.

**Ghost as a CMS for other content:**
Ghost pages (not posts) work well as persistent content stores — about pages, landing pages, link-in-bio pages. Create/update via API the same way as posts. Pages don't appear in the feed and don't trigger emails.

**Batch operations from a working file:**
Keep a `memory/ghost-queue.md` with pending posts in structured format:
```markdown
## Queue
- [ ] Title: "Post Title" | Tags: Bitcoin, Essay | Status: draft | Notes: needs intro
- [x] Title: "Published Post" | Published: 2026-03-10
```

Agent reads the queue, drafts or publishes each item, marks done.

---

## Workflow 10: Analytics & Insights

**What the Admin API gives you:**
```bash
# Subscriber count
GET /members/?limit=1
# → meta.pagination.total = total member count

# Active subscribers only
GET /members/?limit=1&filter=subscribed:true

# Post engagement (basic)
GET /posts/{id}/?fields=id,title,email_recipient_filter,email,published_at
# → email.opened_count, email.clicked_count (if email was sent)

# Recent posts with metadata
GET /posts/?limit=10&fields=id,title,published_at,slug,feature_image,tags
```

**What the Admin API does NOT give you:**
- Page views and unique visitors
- Traffic sources / referrers
- Post-level view counts (these are in Ghost's native analytics dashboard only)
- Conversion rates (free → paid)

Ghost's traffic analytics are dashboard-only and not exposed via any API.

**Recommended alternative:**
Use a third-party analytics tool (Plausible, Fathom, or Google Analytics) alongside Ghost. These provide real traffic data via their own APIs and are more reliable long-term. Ghost supports adding custom tracking scripts via Settings → Code injection in Ghost Admin.

**Subscriber growth tracking:**
Poll `/members/?limit=1` on a schedule and log the total to a memory file. Simple, reliable, tells you the most important metric.
```bash
# Run weekly, append to memory/ghost-analytics.md

---

## Workflow 11: Ghost Webhooks + Automation (Zapier / Make / n8n)

Ghost fires outbound webhooks on key events. Wire these to automation platforms to trigger downstream workflows automatically.

**Set up a webhook in Ghost:**
Ghost Admin → Settings → Integrations → Add custom integration → Webhooks tab → Add webhook

**Available webhook events:**
- `post.published` — fires when a post goes live
- `post.unpublished` — fires when a post is taken down
- `member.added` — new subscriber joined
- `member.deleted` — subscriber unsubscribed
- `member.edited` — subscriber updated (tier change, email change)
- `page.published` — page published

**Webhook payload (post.published example):**
```json
{
  "post": {
    "current": {
      "id": "...",
      "title": "Post Title",
      "url": "https://your-site.ghost.io/post-slug/",
      "published_at": "2026-03-16T18:00:00.000Z",
      "tags": [...],
      "feature_image": "https://..."
    }
  }
}
```

**Common automation patterns:**

**n8n — auto-post to Twitter/X when published:**
- Trigger: Webhook node (receives Ghost post.published)
- Action: Twitter node → compose tweet from title + URL
- Add delay node (5 min) to let Ghost CDN cache the post first

**Zapier — notify Slack when new subscriber joins:**
- Trigger: Webhooks by Zapier (catches member.added)
- Action: Slack message to #subscribers channel with member email

**Make — cross-post to LinkedIn:**
- Trigger: Webhooks module (post.published)
- Action: HTTP module → LinkedIn API → create post with excerpt + link

**OpenClaw cron as webhook receiver:**
You can point Ghost webhooks at your OpenClaw gateway (if externally accessible) to trigger agent actions directly on publish events.

---

## Workflow 12: SEO & Metadata Control

Ghost exposes full SEO metadata via the Admin API. Control everything programmatically.

**Fields available on posts/pages:**
```json
{
  "posts": [{
    "title": "Post Title",
    "slug": "custom-url-slug",
    "custom_excerpt": "This appears in feed cards and social previews (150 chars max)",
    "meta_title": "SEO Title (overrides post title in <title> tag)",
    "meta_description": "SEO meta description (150-160 chars, appears in search results)",
    "og_title": "Open Graph title (Facebook, LinkedIn share preview)",
    "og_description": "Open Graph description",
    "og_image": "https://url-to-og-image-1200x630.jpg",
    "twitter_title": "Twitter card title",
    "twitter_description": "Twitter card description",
    "twitter_image": "https://url-to-twitter-image.jpg",
    "canonical_url": "https://original-source-if-syndicated.com/post"
  }]
}
```

**Slug rules:**
- Ghost auto-generates slugs from titles — override with `slug` field
- Lowercase, hyphens only, no special characters
- Ghost appends `-2`, `-3` etc. on duplicates
- Changing a slug breaks existing links — set it right the first time or add redirects

**Feature image vs OG image:**
- `feature_image` — shown in the post and feed cards
- `og_image` — used for social sharing previews (defaults to feature_image if not set)
- Recommended: set both explicitly. OG image optimal size: 1200×630px

**Canonical URL:**
Use when syndicating content from another platform. Tells search engines the original source. Prevents duplicate content penalties.
```json
{ "canonical_url": "https://medium.com/original-post-url" }
```

**Batch SEO audit + fix:**
```js
// Fetch all posts missing meta descriptions
const posts = await fetch('/posts/?limit=all&filter=meta_description:null&fields=id,title,slug,custom_excerpt');
// For each: generate meta_description from custom_excerpt or title
// PUT update with meta_description filled
```

---

## Workflow 13: Multi-Site Management

Running more than one Ghost site? Structure credentials and agent workflows to handle both cleanly.

**Multi-site credentials file:**
```json
{
  "sites": {
    "primary": {
      "url": "https://site-one.ghost.io",
      "key": "id:secret"
    },
    "secondary": {
      "url": "https://site-two.ghost.io",
      "key": "id:secret"
    }
  }
}
```

Store at `~/.openclaw/credentials/ghost-sites.json`

**Token generation per site:**
```bash
node -e "
const crypto=require('crypto');
const sites=JSON.parse(require('fs').readFileSync(process.env.HOME+'/.openclaw/credentials/ghost-sites.json','utf8'));
const site=sites.sites['primary']; // change to 'secondary' as needed
const [id,secret]=site.key.split(':');
const h=Buffer.from(JSON.stringify({alg:'HS256',typ:'JWT',kid:id})).toString('base64url');
const n=Math.floor(Date.now()/1000);
const p=Buffer.from(JSON.stringify({iat:n,exp:n+300,aud:'/admin/'})).toString('base64url');
const s=crypto.createHmac('sha256',Buffer.from(secret,'hex')).update(h+'.'+p).digest('base64url');
console.log(JSON.stringify({token:h+'.'+p+'.'+s,url:site.url}));
"
```

**Cross-post the same content to multiple sites:**
```js
const sites = ['primary', 'secondary'];
for (const siteName of sites) {
  const site = config.sites[siteName];
  const token = generateToken(site.key);
  await fetch(`${site.url}/ghost/api/admin/posts/?source=html`, {
    method: 'POST',
    headers: { 'Authorization': `Ghost ${token}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({ posts: [postData] })
  });
  await new Promise(r => setTimeout(r, 1000)); // 1s between sites
}
```

**Per-site memory tracking:**
Keep separate publishing logs per site in memory:
```markdown
## Site: Primary (site-one.ghost.io)
- Subscribers: 847
- Last published: 2026-03-16

## Site: Secondary (site-two.ghost.io)
- Subscribers: 234
- Last published: 2026-03-10
```

---

## Workflow 14: Site Audit — Find and Fix Content Debt

Use case: You've been publishing for a while and your archive has gaps — missing feature images, empty excerpts, orphaned tags, posts with broken internal links. This workflow pulls your full post list and produces an actionable audit report.

Run this periodically (monthly or before major site pushes). It requires no npm packages — pure Node.js built-ins.

### Step 1: Generate a JWT token

```bash
TOKEN=$(node -e "
const crypto=require('crypto');
const creds=JSON.parse(require('fs').readFileSync(process.env.HOME+'/.openclaw/credentials/ghost-admin.json','utf8'));
const [id,secret]=creds.key.split(':');
const h=Buffer.from(JSON.stringify({alg:'HS256',typ:'JWT',kid:id})).toString('base64url');
const n=Math.floor(Date.now()/1000);
const p=Buffer.from(JSON.stringify({iat:n,exp:n+300,aud:'/admin/'})).toString('base64url');
const s=crypto.createHmac('sha256',Buffer.from(secret,'hex')).update(h+'.'+p).digest('base64url');
process.stdout.write(h+'.'+p+'.'+s);
")
URL=$(node -e "const c=JSON.parse(require('fs').readFileSync(process.env.HOME+'/.openclaw/credentials/ghost-admin.json','utf8'));process.stdout.write(c.url);")
```

### Step 2: Fetch all published posts

```bash
node -e "
const https=require('https');
const crypto=require('crypto');
const fs=require('fs');

const creds=JSON.parse(fs.readFileSync(process.env.HOME+'/.openclaw/credentials/ghost-admin.json','utf8'));
const [id,secret]=creds.key.split(':');

function makeToken(){
  const h=Buffer.from(JSON.stringify({alg:'HS256',typ:'JWT',kid:id})).toString('base64url');
  const n=Math.floor(Date.now()/1000);
  const p=Buffer.from(JSON.stringify({iat:n,exp:n+300,aud:'/admin/'})).toString('base64url');
  const s=crypto.createHmac('sha256',Buffer.from(secret,'hex')).update(h+'.'+p).digest('base64url');
  return h+'.'+p+'.'+s;
}

async function fetchPage(page){
  return new Promise((resolve,reject)=>{
    const url=new URL(creds.url);
    const path='/ghost/api/admin/posts/?limit=15&page='+page+'&status=published&fields=id,title,slug,published_at,updated_at,feature_image,custom_excerpt,tags,meta_description&include=tags';
    const options={hostname:url.hostname,path,method:'GET',headers:{'Authorization':'Ghost '+makeToken()}};
    const req=https.request(options,res=>{
      let data='';
      res.on('data',d=>data+=d);
      res.on('end',()=>resolve(JSON.parse(data)));
    });
    req.on('error',reject);
    req.end();
  });
}

(async()=>{
  let page=1, allPosts=[];
  while(true){
    const data=await fetchPage(page);
    if(!data.posts||data.posts.length===0) break;
    allPosts=allPosts.concat(data.posts);
    if(!data.meta?.pagination?.next) break;
    page++;
    await new Promise(r=>setTimeout(r,300));
  }

  const now=Date.now();
  const ninetyDaysAgo=now-(90*24*60*60*1000);

  const issues={
    noFeatureImage: [],
    noExcerpt: [],
    noMetaDescription: [],
    noTags: [],
    notUpdatedIn90Days: [],
    slugWarnings: [],
  };

  for(const p of allPosts){
    if(!p.feature_image) issues.noFeatureImage.push({id:p.id,title:p.title,slug:p.slug});
    if(!p.custom_excerpt) issues.noExcerpt.push({id:p.id,title:p.title,slug:p.slug});
    if(!p.meta_description) issues.noMetaDescription.push({id:p.id,title:p.title,slug:p.slug});
    if(!p.tags||p.tags.length===0) issues.noTags.push({id:p.id,title:p.title,slug:p.slug});
    if(new Date(p.updated_at).getTime()<ninetyDaysAgo) issues.notUpdatedIn90Days.push({id:p.id,title:p.title,slug:p.slug,updated_at:p.updated_at});
    // Slug warnings: numeric-only, very short, or contains underscores
    if(/^\d+$/.test(p.slug)||p.slug.length<4||p.slug.includes('_'))
      issues.slugWarnings.push({id:p.id,title:p.title,slug:p.slug});
  }

  console.log('=== GHOST SITE AUDIT ===');
  console.log('Total published posts:', allPosts.length);
  console.log('Run at:', new Date().toISOString());
  console.log('');
  console.log('--- MISSING FEATURE IMAGES ('+issues.noFeatureImage.length+') ---');
  issues.noFeatureImage.forEach(p=>console.log(' •',p.title,'→',p.slug));
  console.log('');
  console.log('--- MISSING EXCERPTS ('+issues.noExcerpt.length+') ---');
  issues.noExcerpt.forEach(p=>console.log(' •',p.title,'→',p.slug));
  console.log('');
  console.log('--- MISSING META DESCRIPTIONS ('+issues.noMetaDescription.length+') ---');
  issues.noMetaDescription.forEach(p=>console.log(' •',p.title,'→',p.slug));
  console.log('');
  console.log('--- NO TAGS ('+issues.noTags.length+') ---');
  issues.noTags.forEach(p=>console.log(' •',p.title,'→',p.slug));
  console.log('');
  console.log('--- NOT UPDATED IN 90+ DAYS ('+issues.notUpdatedIn90Days.length+') ---');
  issues.notUpdatedIn90Days.forEach(p=>console.log(' •',p.title,'| last updated:',p.updated_at));
  console.log('');
  console.log('--- SLUG WARNINGS ('+issues.slugWarnings.length+') ---');
  issues.slugWarnings.forEach(p=>console.log(' •',p.title,'→',p.slug));
  console.log('');
  console.log('=== END AUDIT ===');
})();
" 2>&1
```

### What the audit checks

| Check | What it flags | Why it matters |
|---|---|---|
| Missing feature image | Posts with no `feature_image` | Feature images are required for social sharing previews and feed cards. Posts without them look broken on Twitter/LinkedIn shares. |
| Missing excerpt | Posts with no `custom_excerpt` | Excerpts drive Ghost's client-side search and appear in feed cards. Missing excerpts = invisible in search, weak social previews. |
| Missing meta description | Posts with no `meta_description` | Google uses this in search results. Empty = Google writes its own, usually badly. |
| No tags | Posts with zero tags | Tags are Ghost's primary navigation and filtering mechanism. Untagged posts are orphaned — readers can't find them via tag pages. |
| Not updated in 90+ days | Posts with a stale `updated_at` | Useful for identifying candidates for a content refresh pass. Not always an issue — but flags the oldest untouched content. |
| Slug warnings | Very short slugs, numeric-only, underscores | Short or auto-generated slugs hurt SEO. Numeric-only (`/123/`) are meaningless to search engines. Underscores break URL parsing in some clients. |

### Step 3: Fix issues via batch update

After reviewing the audit output, use Workflow 3 (Batch Update) to fix the flagged posts. Priority order:

1. **Missing feature images** — highest impact on social sharing and feed aesthetics
2. **Missing excerpts** — fixes search visibility immediately
3. **Missing meta descriptions** — SEO fix, worth doing in bulk
4. **No tags** — assign at least one primary tag per post
5. **Slug warnings** — fix carefully; changing slugs breaks existing links (add redirects first via Ghost Admin → Labs)

### Pitfalls

- The audit script regenerates a JWT before each paginated page fetch — tokens expire in 5 minutes and large sites (100+ posts) take time to fetch.
- `not updated in 90 days` does NOT mean the content is bad — a timeless essay published two years ago that still ranks well doesn't need touching. Use judgment.
- Slug fixes require adding a redirect in Ghost Admin → Settings → Labs → Redirects (upload a JSON file) before changing the slug, or you'll create dead links.

---

## Workflow 15: Content Performance Intelligence

Use case: You've been publishing for months. You want to know what's actually working — which posts drive email engagement, which content never reached your subscribers, and where your pages have health gaps.

Ghost's Admin API exposes email engagement data (opens, clicks) per post, member counts by tier, post and page metadata. This workflow assembles all of it into a three-section report.

**What this covers:**
- Audience snapshot: active subscribers, free vs paid split
- Section 1 — Email performance: open rate, click rate, CTO, divergence analysis
- Section 2 — Web-only posts: content published but never emailed (amplification candidates + health snapshot)
- Section 3 — Pages: evergreen content health (AI consultant, about, landing pages etc.)

**What Ghost's API cannot give you** (the ceiling):
- Per-post or per-page view counts — dashboard-only, backed by Tinybird, no API access
- Traffic sources / referrers — not exposed
- Free → paid conversion per post — not exposed
- Time-on-page — not exposed

For per-post view counts, wire a third-party analytics tool alongside Ghost:
- **Plausible** (`plausible.io/api/v1/stats/breakdown?property=event:page`) — simple, privacy-first, clean REST API
- **Fathom** (`usefathom.com/api`) — similar to Plausible
- **GA4** (`analyticsdata.googleapis.com`) — more complex OAuth but most widely used

All three return per-URL view counts you can join to Ghost post slugs.

### The script

Save as `ghost-performance.js` and run with `node ghost-performance.js`.

```js
const https = require('https');
const crypto = require('crypto');
const fs = require('fs');

const creds = JSON.parse(fs.readFileSync(process.env.HOME + '/.openclaw/credentials/ghost-admin.json', 'utf8'));
const [id, secret] = creds.key.split(':');

function makeToken() {
  const h = Buffer.from(JSON.stringify({ alg: 'HS256', typ: 'JWT', kid: id })).toString('base64url');
  const n = Math.floor(Date.now() / 1000);
  const p = Buffer.from(JSON.stringify({ iat: n, exp: n + 300, aud: '/admin/' })).toString('base64url');
  const s = crypto.createHmac('sha256', Buffer.from(secret, 'hex')).update(h + '.' + p).digest('base64url');
  return h + '.' + p + '.' + s;
}

function apiGet(path) {
  return new Promise((resolve, reject) => {
    const url = new URL(creds.url);
    const options = {
      hostname: url.hostname,
      path,
      method: 'GET',
      headers: { 'Authorization': 'Ghost ' + makeToken(), 'Accept-Version': 'v5.0' }
    };
    const req = https.request(options, res => {
      let data = '';
      res.on('data', d => data += d);
      res.on('end', () => resolve(JSON.parse(data)));
    });
    req.on('error', reject);
    req.end();
  });
}

async function fetchAll(endpoint, include = '') {
  let page = 1, all = [];
  const type = endpoint.includes('/pages/') ? 'pages' : 'posts';
  while (true) {
    const inc = include ? '&include=' + include : '';
    const data = await apiGet(`/ghost/api/admin/${endpoint}?limit=15&page=${page}&status=published${inc}`);
    if (!data[type] || data[type].length === 0) break;
    all = all.concat(data[type]);
    if (!data.meta?.pagination?.next) break;
    page++;
    await new Promise(r => setTimeout(r, 300));
  }
  return all;
}

function healthFlags(item) {
  const flags = [];
  if (!item.feature_image) flags.push('no feature image');
  if (!item.custom_excerpt) flags.push('no excerpt');
  if (!item.meta_description) flags.push('no meta description');
  if (!item.tags || item.tags.length === 0) flags.push('no tags');
  return flags;
}

(async () => {
  // --- Audience snapshot ---
  const allMembers = await apiGet('/ghost/api/admin/members/?limit=1');
  const activeMembers = await apiGet('/ghost/api/admin/members/?limit=1&filter=subscribed:true');
  const freeMembers = await apiGet('/ghost/api/admin/members/?limit=1&filter=subscribed:true,status:free');
  const paidMembers = await apiGet('/ghost/api/admin/members/?limit=1&filter=subscribed:true,status:paid');
  const totalSubs = activeMembers?.meta?.pagination?.total ?? '?';
  const freeSubs = freeMembers?.meta?.pagination?.total ?? '?';
  const paidSubs = paidMembers?.meta?.pagination?.total ?? '?';

  // --- Posts ---
  const allPosts = await fetchAll('posts/', 'email,tags');
  const emailed = allPosts.filter(p => p.email && p.email.email_count > 0);
  const webOnly = allPosts.filter(p => !p.email || p.email.email_count === 0);

  // --- Pages ---
  const allPages = await fetchAll('pages/', 'tags');

  // --- Email performance ---
  const withRates = emailed.map(p => {
    const sent = p.email.email_count || 0;
    const opened = p.email.opened_count || 0;
    const clicked = p.email.clicked_count || 0;
    const openRate = sent > 0 ? ((opened / sent) * 100).toFixed(1) : null;
    const clickRate = sent > 0 ? ((clicked / sent) * 100).toFixed(1) : null;
    const cto = opened > 0 ? ((clicked / opened) * 100).toFixed(1) : null;
    return { ...p, sent, opened, clicked, openRate, clickRate, cto };
  }).filter(p => p.openRate !== null);

  const byOpen = [...withRates].sort((a, b) => parseFloat(b.openRate) - parseFloat(a.openRate));
  const byClick = [...withRates].sort((a, b) => parseFloat(b.clickRate) - parseFloat(a.clickRate));
  const divergent = withRates
    .filter(p => parseFloat(p.openRate) > 40 && parseFloat(p.clickRate) < 3)
    .sort((a, b) => parseFloat(b.openRate) - parseFloat(a.openRate));

  const fmtEmail = p =>
    `  • ${p.title}\n    Sent: ${p.sent} | Open: ${p.openRate}% | Click: ${p.clickRate}% | CTO: ${p.cto}% | Segment: ${p.email_recipient_filter || 'all'}`;

  // --- Output ---
  console.log('=== GHOST CONTENT PERFORMANCE REPORT ===');
  console.log('Run at:', new Date().toISOString());
  console.log('');
  console.log('AUDIENCE');
  console.log(`  Active subscribers: ${totalSubs} (free: ${freeSubs} / paid: ${paidSubs})`);
  console.log(`  Total published posts: ${allPosts.length} | Emailed: ${emailed.length} | Web-only: ${webOnly.length}`);
  console.log(`  Total published pages: ${allPages.length}`);
  console.log('');

  console.log('--- SECTION 1: EMAIL PERFORMANCE ---');
  console.log('');
  console.log('Top 5 by open rate:');
  byOpen.slice(0, 5).forEach(p => console.log(fmtEmail(p)));
  console.log('');
  console.log('Top 5 by click rate:');
  byClick.slice(0, 5).forEach(p => console.log(fmtEmail(p)));
  console.log('');
  console.log('High open / low click — weak CTA candidates (opens >40%, clicks <3%):');
  if (divergent.length === 0) console.log('  None — CTAs are converting well.');
  divergent.slice(0, 5).forEach(p => console.log(fmtEmail(p)));
  console.log('');

  console.log('--- SECTION 2: WEB-ONLY POSTS (never emailed) ---');
  console.log('Note: per-post view counts require a third-party analytics tool (Plausible, Fathom, GA4).');
  console.log('');
  if (webOnly.length === 0) {
    console.log('  All published posts have been emailed.');
  } else {
    webOnly.forEach(p => {
      const flags = healthFlags(p);
      const flagStr = flags.length > 0 ? ' ⚠ ' + flags.join(', ') : ' ✓';
      console.log(`  • ${p.title}`);
      console.log(`    Published: ${p.published_at?.slice(0, 10)} | Slug: /${p.slug}/${flagStr}`);
    });
  }
  console.log('');

  console.log('--- SECTION 3: PAGES ---');
  console.log('Note: page view counts require a third-party analytics tool (Plausible, Fathom, GA4).');
  console.log('');
  if (allPages.length === 0) {
    console.log('  No published pages found.');
  } else {
    allPages.forEach(p => {
      const flags = healthFlags(p);
      const flagStr = flags.length > 0 ? ' ⚠ ' + flags.join(', ') : ' ✓';
      console.log(`  • ${p.title}`);
      console.log(`    Updated: ${p.updated_at?.slice(0, 10)} | Slug: /${p.slug}/${flagStr}`);
    });
  }
  console.log('');
  console.log('=== END REPORT ===');
})();
```

### Reading the report

**Open rate benchmarks:**
| Rate | Signal |
|---|---|
| Under 20% | Below average — subject line or sender reputation issue |
| 20–40% | Solid — typical for engaged lists |
| 40–60% | Strong — highly engaged audience |
| 60%+ | Exceptional — or MPP inflation (see pitfalls) |

**Click rate benchmarks:**
| Rate | Signal |
|---|---|
| Under 1% | Low — CTA buried or missing |
| 1–3% | Average |
| 3–5% | Strong |
| 5%+ | Exceptional |

**Click-to-open (CTO)** — the most honest signal. Of everyone who opened, how many clicked? High CTO means the content delivered on the subject line's promise. Low CTO means a curiosity open, not a real read.

**High open / low click (divergent posts):** Hidden wins. The subject line worked — people opened. But nothing inside drove a click. Add a CTA, a relevant link, or a "continue reading" anchor. A small edit can unlock latent engagement from an already-warm audience.

**Web-only posts:** Invisible to your subscriber list. Ghost doesn't allow retroactive API email sends — duplicate the post and publish fresh, or use Ghost Admin to manually resend if that option is available.

**Pages:** Evergreen content (about, landing pages, tools). Health flags catch SEO gaps — missing meta descriptions and excerpts on pages hurt search visibility just as much as on posts.

### Saving the report

```bash
node ghost-performance.js > ghost-performance-$(date +%Y-%m-%d).md
```

Run monthly. Compare rates over time to spot list fatigue, content drift, or CTA decay.

### Pitfalls

- `email.opened_count` and `email.clicked_count` only return data with `&include=email` — omitting it returns null even for emailed posts.
- **Apple Mail Privacy Protection (MPP)** pre-loads email pixels on iOS/macOS, inflating open rates. Open rates above 70% on small lists are often MPP artifacts. Click rate and CTO are more reliable signals.
- The `email_recipient_filter` field shows segment (`all`, `free`, `paid`) — compare like-for-like when benchmarking rates across posts.
- Token expires in 5 minutes — the script regenerates before every paginated fetch so long archives won't expire mid-run.
- Pages use the `/pages/` endpoint, not `/posts/` — they won't appear in post queries even though they share most fields.

---

## Workflow 16: Batch Custom Excerpt Push

Use case: Your Workflow 14 audit returned a long list of posts with no custom excerpt. This workflow writes excerpts to all of them in a single batch operation — no browser, no copy-paste, no per-post editing.

Proven in production: 65 posts updated in one run on josephvoelbel.com. Required no npm packages — pure Node.js built-ins and Python.

### Why excerpts matter

Ghost's `custom_excerpt` field controls three surfaces simultaneously:
- **Feed cards** — the preview text below the post title on your homepage and tag pages
- **Social sharing previews** — og:description when the post is shared on Twitter/LinkedIn/iMessage
- **Client-side search** — Ghost's search indexes `custom_excerpt`, not the full post body. If a keyword only lives in the body, the post won't surface in search. The excerpt is the search surface.

Empty excerpts mean weak social previews and invisible posts in your own site search.

### Hard limit: 300 characters

Ghost's `custom_excerpt` field has a hard cap of **300 characters**. The API will silently accept longer strings in some versions but the field is truncated on save. Any excerpt over 300 characters will fail with a validation error or be cut off mid-sentence.

Build your excerpts to fit. Target 200–280 characters for clean previews across all surfaces.

### Step 1: Build your excerpt map

Prepare a JSON file mapping post slugs to excerpts. Slugs are the source of truth — not titles, not IDs. If a slug doesn't match exactly, the update silently skips it.

```json
[
  { "slug": "your-post-slug", "excerpt": "Your excerpt text here — under 300 characters." },
  { "slug": "another-post-slug", "excerpt": "Another excerpt." }
]
```

Save as `excerpts.json`. Run a character count check before proceeding:

```python
import json

with open('excerpts.json') as f:
    entries = json.load(f)

over_limit = [(e['slug'], len(e['excerpt'])) for e in entries if len(e['excerpt']) > 300]
if over_limit:
    print(f"{len(over_limit)} entries over 300 chars:")
    for slug, length in over_limit:
        print(f"  {slug}: {length} chars")
else:
    print("All excerpts within 300-char limit.")
```

Fix any over-limit entries before running the push. Truncating mid-sentence is better than a failed API call — end at a clause boundary.

### Step 2: Fetch post IDs by slug

Ghost's PUT endpoint requires the post ID, not the slug. Fetch the full post list first and build a slug → ID map.

```python
import json, time, urllib.request
from pathlib import Path

creds = json.loads(Path.home().joinpath('.openclaw/credentials/ghost-admin.json').read_text())
BASE = creds['url'].rstrip('/')

import hmac, hashlib, base64, struct
from datetime import datetime, timezone

def make_token(key):
    key_id, secret = key.split(':')
    header = base64.urlsafe_b64encode(json.dumps({'alg':'HS256','typ':'JWT','kid':key_id}).encode()).rstrip(b'=').decode()
    now = int(datetime.now(timezone.utc).timestamp())
    payload = base64.urlsafe_b64encode(json.dumps({'iat':now,'exp':now+300,'aud':'/admin/'}).encode()).rstrip(b'=').decode()
    sig_input = f'{header}.{payload}'.encode()
    sig = base64.urlsafe_b64encode(hmac.new(bytes.fromhex(secret), sig_input, hashlib.sha256).digest()).rstrip(b'=').decode()
    return f'{header}.{payload}.{sig}'

def api_get(path):
    req = urllib.request.Request(f'{BASE}{path}', headers={'Authorization': f'Ghost {make_token(creds["key"])}'})
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())

# Fetch all published posts — paginate until done
slug_to_post = {}
page = 1
while True:
    data = api_get(f'/ghost/api/admin/posts/?limit=15&page={page}&status=published&fields=id,slug,updated_at')
    for post in data.get('posts', []):
        slug_to_post[post['slug']] = post
    if not data.get('meta', {}).get('pagination', {}).get('next'):
        break
    page += 1
    time.sleep(0.3)

print(f'Fetched {len(slug_to_post)} published posts.')
```

### Step 3: Push excerpts

```python
import urllib.error

excerpts = json.loads(Path('excerpts.json').read_text())

updated = 0
skipped = 0
failed = []

for entry in excerpts:
    slug = entry['slug']
    excerpt = entry['excerpt']

    if slug not in slug_to_post:
        print(f'  SKIP (not found): {slug}')
        skipped += 1
        continue

    post = slug_to_post[slug]
    post_id = post['id']
    updated_at = post['updated_at']

    payload = json.dumps({'posts': [{'custom_excerpt': excerpt, 'updated_at': updated_at}]}).encode()
    req = urllib.request.Request(
        f'{BASE}/ghost/api/admin/posts/{post_id}/',
        data=payload,
        method='PUT',
        headers={
            'Authorization': f'Ghost {make_token(creds["key"])}',
            'Content-Type': 'application/json'
        }
    )
    try:
        with urllib.request.urlopen(req) as r:
            r.read()
        print(f'  OK: {slug}')
        updated += 1
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f'  FAIL ({e.code}): {slug} — {body[:120]}')
        failed.append(slug)

    time.sleep(0.5)  # 500ms between calls — stay under rate limit

print(f'\nDone. Updated: {updated} | Skipped (slug not found): {skipped} | Failed: {len(failed)}')
if failed:
    print('Failed slugs:', failed)
```

### Reading the output

- **OK** — excerpt written successfully
- **SKIP (not found)** — the slug in your JSON doesn't match any published post. Common causes: post is a draft, post was deleted, slug changed since your audit. These are safe to ignore or investigate separately.
- **FAIL (422)** — usually a character count violation. Check the excerpt length for that slug.
- **FAIL (409)** — `updated_at` conflict. Another process touched the post between your fetch and your PUT. Re-fetch and retry.

### Pitfalls

- **300-character hard cap** — validate before you run. A batch of 79 where 19 fail on character count wastes the run and leaves your site in a half-updated state. Run the character count check in Step 1. Fix everything first, then push.
- **Slug mismatches are silent** — the script reports them as SKIP, not ERROR. Skipped slugs need a manual slug lookup — fetch the post by title search or browse Ghost Admin to confirm the real slug.
- **Don't use post IDs from a cached fetch** — if there's any gap between when you fetched post metadata and when you run the push, some `updated_at` values may be stale. For large batches (50+ posts), re-fetch immediately before the PUT loop or regenerate `updated_at` per post inline.
- **500ms delay is not optional** — Ghost will 429 on rapid successive PUTs. The delay keeps you under the rate limit on Ghost Pro hosting.
- **Custom excerpts drive client-side search** — if you're writing excerpts to fix search gaps, include the keywords you want to rank for. Ghost's search indexes this field verbatim. An excerpt that doesn't contain the keyword still won't surface the post in search for that term.

---

## Workflow 17: GSC → Ghost Indexing & SEO Repair Loop

Use case: Google Search Console is showing coverage gaps — pages discovered but not indexed, crawled but skipped, or redirect errors from a platform migration. This workflow walks the triage and repair process specifically for Ghost sites.

Proven in production: ran this loop on josephvoelbel.com after a Squarespace migration left 18+ URLs unindexed. Traffic increased measurably in the weeks following.

This workflow assumes you have GSC access already configured for your domain. It does not cover GSC authentication setup.

---

### Step 1: Pull the coverage report

In Google Search Console: **Index → Pages** (or Coverage in older GSC UI).

Four buckets matter:

| Bucket | What it means | Priority |
|---|---|---|
| **Valid** | Indexed and serving | Baseline — protect these |
| **Discovered — currently not indexed** | Google knows the URL exists but hasn't crawled it yet | Low urgency — internal links accelerate this |
| **Crawled — currently not indexed** | Google visited and actively decided to skip | High priority — Google made a judgment call |
| **Excluded** | Intentionally or structurally excluded | Triage: is it intentional? |

Export the **Crawled — currently not indexed** list first. That's where the leverage is.

---

### Step 2: Classify the URL list

Not every unindexed URL is a problem. Classify before acting.

**Category A — System/feed URLs (ignore):**
- `/rss/`, `/rss.xml`, `?format=rss` — feed URLs, shouldn't be indexed
- `/favicon.ico`, `/sitemap.xml` — binaries/feeds, not pages
- `/ghost/` — admin path, correctly blocked by robots.txt

**Category B — Migration ghosts (let die):**
If you migrated from Squarespace or WordPress, you'll likely see old platform URLs:
- `/blog/tag/SomeTag` — Squarespace tag pages redirected to Ghost tag pages that may not exist
- `/blog/category/Philosophy` — WordPress category pages
- Dated paths like `/2015/11/11/slug` that redirect into the void

Google will drop these naturally as it follows redirects and hits 404s. No action needed unless you want to explicitly 410 them.

**Category C — Actual posts (fix these):**
Real content Google visited and chose not to index. Common causes:
- Post is too short or thin
- No internal links pointing to it
- Duplicate content (canonical issue)
- `?format=amp` URL variant that your redirect rule doesn't handle cleanly

For each Category C URL, verify the post exists and is published on Ghost:

```bash
# Quick check: fetch post by slug from Ghost API
TOKEN=... # generate JWT
SLUG="your-post-slug"
curl -s "{url}/ghost/api/admin/posts/slug/${SLUG}/?fields=id,title,slug,status" \
  -H "Authorization: Ghost ${TOKEN}" | python3 -c "import json,sys; p=json.load(sys.stdin)['posts'][0]; print(p['status'], p['title'])"
```

---

### Step 3: Ghost-specific redirect issues

Migrations leave redirect chains. Ghost's redirect system has two hard constraints:

**The API blocks redirect writes.** `POST /ghost/api/admin/redirects/upload/` returns `403` for integration tokens. Redirect rules must be uploaded manually:

> Ghost Admin → Settings → Labs → Redirects → upload a JSON file

Redirects file format:
```json
[
  {"from": "/blog/old-slug", "to": "/new-slug", "permanent": true},
  {"from": "/blog/tag/(.*)", "to": "/tag/$1", "permanent": true}
]
```

**AMP URLs survive redirect rules.** A redirect from `/blog/slug` → `/slug` will not strip `?format=amp`. If GSC shows `?format=amp` variants as unindexed, add an explicit rule:
```json
{"from": "/blog/(.*)\\?format=amp", "to": "/$1", "permanent": true}
```

**Redirect chains break indexing.** If A→B→C, Google may stop following at B. Audit your redirects file for chains — every rule should point directly to the final destination.

---

### Step 4: Fix Ghost tag page indexing

Ghost includes tag pages in its sitemap by default. Tag pages are thin, low-signal content — they compete with your real posts for indexing budget and rarely rank.

**Add noindex to tag pages via your theme:**

In your `tag.hbs` template:
```handlebars
{{! In the <head> section }}
<meta name="robots" content="noindex, follow">
```

This tells Google to ignore the tag page but still follow links from it to your real posts. Real posts keep getting discovered. Tag pages stop competing.

**Remove tag pages from your sitemap** via `routes.yaml` (Ghost Admin → Labs → Routes upload):
```yaml
routes:
collections:
  /:
    permalink: /{slug}/
    template: index
taxonomies:
  # comment out or leave blank to exclude tag/author pages from sitemap
```

---

### Step 5: Submit real posts for indexing

For every Category C URL that represents a real post you want indexed:

1. Open GSC → **URL Inspection**
2. Paste the URL
3. Click **Request Indexing**

GSC will queue it for a Googlebot crawl, typically within days. You can submit one URL at a time — no batch submit exists in the UI.

**What makes a URL worth submitting:**
- It's a real published post with substantive content
- It has at least one internal link pointing to it from another indexed page
- It has a custom excerpt and meta description (Workflow 12)
- It's not thin content (under ~300 words with no unique angle)

Don't submit system URLs, tag pages, or thin placeholder posts — they'll be skipped again.

---

### Step 6: Accelerate indexing with internal links

The fastest lever for "Discovered but not indexed" pages is internal links from pages Google already trusts.

Identify your highest-traffic posts via Workflow 10 or Ghost Admin analytics. Add a "Related reading" or "Continue reading" section to those posts linking to your newer, unindexed content.

The Ghost API approach (see Workflow 16 pattern):
```python
# Fetch your top posts by view count
# For each: append a read-next block (see SKILL.md — Read-Next Pattern)
# The block links to 2-3 newer posts you want indexed
# PUT the updated post back
```

Even 2–3 internal links from high-authority pages to an unindexed post can move it from "Discovered" to "Indexed" within Google's next crawl cycle.

---

### Step 7: Triage "Crawled — currently not indexed" (the hard cases)

These are posts Google visited and actively chose not to index. That's a content judgment, not a crawl issue. Fix at the source:

| Cause | Fix |
|---|---|
| Thin content (under 400 words, low signal) | Expand the post or redirect it to a stronger related post |
| No unique angle | Differentiate the content — what does this post say that no other page says? |
| Duplicate content | Set canonical URL (Workflow 12) pointing to the definitive version |
| Orphaned (no inbound links) | Add internal links from indexed pages (Step 6) |
| Old placeholder from migration | 301 redirect to the closest live post, or leave it to drop naturally |

For posts you care about ranking: improve them, add internal links, then Request Indexing again (Step 5).

For posts that are genuinely low-value: either delete and redirect, or accept they won't rank and stop spending indexing budget on them.

---

### GSC → Ghost repair: the recurring loop

This isn't a one-time fix. Run it quarterly:

1. Pull coverage report — check for new Crawled-not-indexed entries
2. Triage new entries by category
3. Submit real posts for indexing after any content improvement
4. Check redirect file for chains (anything pointing to a URL that also redirects)
5. Confirm tag pages are still noindexed after any theme updates

### Pitfalls

- **Redirect uploads overwrite the entire file** — Ghost's Labs upload replaces, not appends. Always download the existing redirects JSON first, edit it, then re-upload the full file.
- **AMP variants survive simple redirect rules** — add explicit rules for `?format=amp` and `?format=json` if GSC shows them.
- **"Discovered but not indexed" is a waiting game** — submitting these via URL Inspection rarely helps. Internal links are faster. Don't burn GSC's submission quota on pages that just need to be crawled naturally.
- **GSC data lags 2–3 days** — a redirect fix you deployed today won't show as resolved until Google re-crawls and GSC processes it. Check back in a week before deciding a fix didn't work.
- **Tag page noindex requires a theme change** — this means re-uploading your Ghost theme via Admin → Design → Upload. If you're on a paid Ghost theme, test on a staging site first.

