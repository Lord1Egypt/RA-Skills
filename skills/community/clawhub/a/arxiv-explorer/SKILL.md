---
name: arxiv-explorer
description: Search, download, and explore arXiv academic papers. Use when the user needs to find research papers, download PDFs, get recent publications in a field, or summarize academic content from arXiv. Supports searching by keywords, categories, authors, and downloading papers for offline reading.
---

# arXiv Explorer

Search and download academic papers from arXiv.

## Commands

### Search Papers
```bash
arxiv-explorer search "query" [-n NUM] [-s SORT] [--json]
```

Examples:
```bash
arxiv-explorer search "machine learning"
arxiv-explorer search "transformer architecture" -n 20 -s date
arxiv-explorer search "quantum computing" --json
```

### Download PDF
```bash
arxiv-explorer download ARXIV_ID [-o OUTPUT]
```

Examples:
```bash
arxiv-explorer download 2401.12345
arxiv-explorer download 2306.04338v1 -o paper.pdf
```

### Recent Papers by Category
```bash
arxiv-explorer recent CATEGORY [-n NUM]
```

Common categories:
- `cs.AI` - Artificial Intelligence
- `cs.CL` - Computation and Language (NLP)
- `cs.CV` - Computer Vision
- `cs.LG` - Machine Learning
- `physics` - Physics
- `math` - Mathematics

Examples:
```bash
arxiv-explorer recent cs.AI -n 5
arxiv-explorer recent cs.CL
```

## Output Format

Default output shows:
- Title
- Authors (first 3, with ... if more)
- Publication date
- arXiv ID
- PDF URL
- Summary (truncated to 200 chars)

Use `--json` for machine-readable output.

## Notes

- arXiv API has rate limits; be respectful with large queries
- PDF downloads are direct from arxiv.org
- No API key required

---

## Support

If this skill helps your research, consider supporting the developer:

**微信赞赏** - 扫码支持持续开发更多实用 Skill

![赞赏码](https://raw.githubusercontent.com/xunuowu/openclaw-skills/main/assets/reward-qrcode.png)
