# Quick examples

## Most common: install for all popular agents

```bash
npx -y create-opc-wiki@latest ~/wiki --yes \
  --agents=openclaw,claude,codex,cursor,hermes,vscode
```

## Minimal install (no MCP, no site, single agent)

```bash
npx -y create-opc-wiki@latest /tmp/quick-wiki --yes \
  --agents=claude --no-mcp --no-site --no-recipes --no-git
```

## Custom domains for a research vault

```bash
npx -y create-opc-wiki@latest ~/research --yes \
  --domains=ai,bio,papers,methodology --agents=claude
```

## Programmatic / CI use

```bash
npx -y create-opc-wiki@latest /tmp/wiki --yes --json --no-git \
  | jq '{ok, files, dirs, target}'
```

Output:
```json
{
  "ok": true,
  "target": "/tmp/wiki",
  "files": 28,
  "dirs": 17
}
```

## Then use the wiki

After scaffolding, `cd <vault>` and run your agent. From inside:

```
/wiki-ingest https://paulgraham.com/ds.html
/wiki-query "what's the relationship between Kelly criterion and position sizing?"
/wiki-lint
```

## Run the MCP server

```bash
cd ~/wiki/mcp
npm install
npm start
```

Then connect from Claude Desktop / Cursor / Codex. Three tools available: `wiki_query`, `wiki_list`, `wiki_read`.

## Publish your wiki

Tag pages with `privacy: public` in frontmatter, then:

```bash
cd ~/wiki/site
npm install
npm run build
# dist/ contains: index.html, sitemap.xml, llms.txt, robots.txt, feed.xml,
# per-page HTML with OpenGraph + JSON-LD
```

Drop `dist/` on GitHub Pages, Cloudflare Pages, Netlify, anywhere.
