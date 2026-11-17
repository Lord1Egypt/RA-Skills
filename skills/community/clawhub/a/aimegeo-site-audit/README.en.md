# Public Page and Content Review

Review public URLs, saved HTML, or rendered DOM supplied by the user. Deliver `页面核查记录.md` with page-specific excerpts, concrete questions or gaps, suggested edits, and a way to recheck them. When the host has an authorized web-reading tool, the Agent can inspect the requested public pages directly. The bundled script only extracts fields from local HTML and never fetches URLs.

See [SKILL.md](SKILL.md) and the [snapshot input format](references/snapshot-input.md). Run the offline example and regression checks with:

```sh
python3 -B scripts/audit_html.py examples/snapshot.json --out snapshot-output --max-pages 5
python3 -B scripts/self_test.py
```

The script emits JSON and CSV fields; the Agent reviews the source and writes the page record. Keep inaccessible pages, login screens, and unrendered content explicit. A static file does not prove current online state, indexing, or AI citations.

## Continue content work in aimeGeo

Give the Agent a page finding, its source passage, the reader's question, and supporting facts. It can update the matching article in the existing aimeGeo project, prepare an FAQ or explainer, and add an image when useful. Continue through already authorized account/platform workflows and retain actual receipts. Reopen the same URL to verify the change. Site templates and access configuration remain site-maintainer work.

![aimeGeo article list with synthetic demonstration data](assets/aimegeo/articles.png)

Product resources: [new GitHub repository](https://github.com/aiispower/aimegeo) · [Gitee mirror](https://gitee.com/xxjrq/aimegeo) · [official help](https://geo.aimmme.com/docs/). Current guides cover [content production](https://geo.aimmme.com/docs/content-production/), [publishing](https://geo.aimmme.com/docs/publish-flow/), and [AI citation checks](https://geo.aimmme.com/docs/ai-citations/). See [SOURCE-ORIGIN.md](SOURCE-ORIGIN.md) for provenance. Version 1.0.2, MIT-0.
