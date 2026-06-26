# Landing Pages and Sites

Use this file for creating and managing Bitrix24 sites and landing pages, adding blocks, editing content, and publishing.

Scope: `landing`

## Sites

- `landing.site.getList` — list sites (params: `select`, `filter`, `order`)
- `landing.site.add` — create a site (fields: `TITLE`, `CODE`, `DOMAIN_ID`)
- `landing.site.update` — update a site
- `landing.site.delete` — delete a site
- `landing.site.publication` — publish site and all its pages
- `landing.site.unpublic` — unpublish site and all its pages
- `landing.site.getPublicUrl` — get public URL of a site
- `landing.site.fullExport` — export site structure
- `landing.site.getFolders` — get site folders
- `landing.site.getRights` — get current user's rights to a site

## Pages

- `landing.landing.getList` — list pages (params: `select`, `filter`, `order`; filter by `SITE_ID`)
- `landing.landing.add` — add page (fields: `TITLE`, `CODE`, `SITE_ID`)
- `landing.landing.update` — update page
- `landing.landing.delete` — delete page
- `landing.landing.copy` — copy page
- `landing.landing.move` — move page to another site
- `landing.landing.publication` — publish a page
- `landing.landing.unpublic` — unpublish a page
- `landing.landing.getpublicurl` — get public URL of a page

Extra flags in `landing.landing.getList`: `get_preview=1`, `get_urls=1`, `check_area=1`.

## Blocks

Blocks are visual sections added to pages.

- `landing.block.getlist` — list blocks on a page
- `landing.block.getrepository` — list available block templates by section
- `landing.block.getContentFromRepository` — get block HTML before placing
- `landing.landing.addblock` — add block to page (fields: `CODE`, `AFTER_ID`, `ACTIVE`, `CONTENT`)
- `landing.block.updatenodes` — edit block content by node selectors
- `landing.block.updatecontent` — replace entire block HTML
- `landing.block.getcontent` — get block content (HTML, CSS, JS)
- `landing.block.getmanifest` — get block manifest (describes editable nodes)

Repository sections: `cover`, `about`, `text_image`, `columns`, `tiles`, `forms`, `team`, `gallery`, `menu`, `footer`, `social`, etc.

### Node types in `updatenodes`

- Text: `'.selector': 'New text with <b>html</b>'`
- Image: `'.selector': {src: '/path/image.png', alt: 'Alt text'}`
- Link: `'.selector': {text: 'Link text', href: 'https://...', target: '_blank'}`
- Embed: `'.selector': {src: '//youtube.com/embed/...', source: 'https://youtube.com/watch?v=...'}`

## Common Use Cases

### List all sites

```bash
python3 scripts/bitrix24_call.py landing.site.getList \
  --param 'params[select][]=ID' \
  --param 'params[select][]=TITLE' \
  --param 'params[select][]=DOMAIN.DOMAIN' \
  --json
```

### Create a site

```bash
python3 scripts/bitrix24_call.py landing.site.add \
  --param 'fields[TITLE]=My Site' \
  --param 'fields[CODE]=mysite' \
  --json
```

### Add a page to a site

```bash
python3 scripts/bitrix24_call.py landing.landing.add \
  --param 'fields[TITLE]=About Us' \
  --param 'fields[CODE]=about' \
  --param 'fields[SITE_ID]=292' \
  --json
```

### List available block templates

```bash
python3 scripts/bitrix24_call.py landing.block.getrepository \
  --param 'section=cover' \
  --json
```

### Add a block to a page

```bash
python3 scripts/bitrix24_call.py landing.landing.addblock \
  --param 'lid=351' \
  --param 'fields[CODE]=04.1.one_col_fix_with_title' \
  --json
```

### Edit block text content

```bash
python3 scripts/bitrix24_call.py landing.block.updatenodes \
  --param 'lid=351' \
  --param 'block=6058' \
  --param 'data[.landing-block-node-title]=Welcome to our site' \
  --param 'data[.landing-block-node-text]=We provide great services.' \
  --json
```

### Replace entire block HTML

```bash
python3 scripts/bitrix24_call.py landing.block.updatecontent \
  --param 'lid=351' \
  --param 'block=6058' \
  --param 'content=<section class="landing-block"><h1>Hello World</h1></section>' \
  --json
```

### Publish a site

```bash
python3 scripts/bitrix24_call.py landing.site.publication \
  --param 'id=292' \
  --json
```

### Get site public URL

```bash
python3 scripts/bitrix24_call.py landing.site.getPublicUrl \
  --param 'id[]=292' \
  --json
```

## Building a Site from Scratch

1. Create site: `landing.site.add`
2. Add pages: `landing.landing.add` with `SITE_ID`
3. Browse block templates: `landing.block.getrepository` by section
4. Add blocks to pages: `landing.landing.addblock` with block `CODE`
5. Edit block content: `landing.block.updatenodes` or `landing.block.updatecontent`
6. Publish: `landing.site.publication`
7. Get URL: `landing.site.getPublicUrl`

## Working Rules

- Landing methods use nested `params` for `select`/`filter`/`order` (not top-level).
- Block `CODE` comes from `landing.block.getrepository`.
- `landing.block.updatenodes` uses CSS selectors to target editable nodes.
- Get the block manifest first (`landing.block.getmanifest`) to see which nodes are editable.
- `landing.block.updatecontent` replaces the entire block HTML — use with care.
- Filter uses `%` for LIKE: `filter[TITLE]=%keyword%`.

## Good MCP Queries

- `landing site add getList publication`
- `landing landing add getList page`
- `landing block addblock getrepository updatenodes`
- `landing block updatecontent getcontent`
