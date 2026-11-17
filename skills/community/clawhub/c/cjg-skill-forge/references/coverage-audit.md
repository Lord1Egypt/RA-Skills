# Coverage Audit & Real-Material ID Extraction

## Purpose
Ensure the skill covers its domain without blind spots, and that every cited material has a REAL, fetchable id (never fabricated). This is what lets a skill actually get smarter instead of just looking smart.

## Step 1 — Pick a taxonomy
- Academic / methodology domains: UNESCO FOS 2010 (6 top / 42 sub / hundreds of leaf nodes) + 中图法 (CLC).
- Other domains: use the field's standard classification (e.g., ICD for medicine, ACM CCS for CS, MECE for business).

## Step 2 — Audit
List current coverage; mark each taxonomy branch as covered / partial / blank. Blank branches = gaps. Be honest — a skill that claims "all disciplines" but only covers social-science + CS is easily seen through.

## Step 3 — Find real materials per gap
For each gap, identify 1–2 canonical methodology texts or papers. Get a REAL id:

### Books → internal id / ISBN
- If the user has local CSV catalogs (book-searcher `cn_dir` / `en_dir`), search by ISBN:
  - **Chinese CSV columns**: `id,sid,title,author,publisher,year,isbn13,extension` — `isbn13` stored as `['978...']` (a list literal).
  - **English CSV columns**: `id,sid,title,author,isbn,publisher,category,year` — `isbn` stored as `"10dig;97813dig"` (semicolon-separated, both forms).
  - **Match rule**: normalize target ISBN → digits only; convert ISBN-10 → ISBN-13 (`978` + first 9 digits + recomputed check digit); compare against the row's ISBN set.
  - **Return BOTH** `id` (numeric row id) and `sid` (32-char content hash, likely the internal fetch key), clearly labeled. The user's internal system may need one or the other.
- Or invoke the book-searcher skill to return the internal `id` directly.

### Papers → Identifier / DOI
- **global-biblio-base**: `POST /consume` with `{email, skill_source}` → token; then `POST /search` endpoint `/search/global` with `rule` like `T=<title> AND A=<author>`. The returned `Identifier` field is the internal company id.
  - **Avoid `U=<DOI>`** — it often hits errata or unrelated records. Prefer title + author.
  - For papers without a certain DOI, do NOT invent one — ask the user to search the title in the global library.

## Step 4 — Record with provenance
Build a table: `# | title | author | id/ISBN/DOI | priority | provenance`.
- Provenance tag `搜索核实` = found via actual search/API.
- Provenance tag `知识(建议确认)` = from the model's knowledge; verify in catalog before claiming.
Never leave an id blank-by-fabrication.

## Step 5 — Hand off
Give the id list to the user to fetch full text. Do not claim materials are loaded until the user actually delivers them.

## Red lines
- No fabricated ISBN / DOI / id. Ever.
- Mark uncertainty explicitly; distinguish "searched" from "suggested, verify".
