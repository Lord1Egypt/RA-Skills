# OpenAlex API Key · Application and Integration Guide

> Scope: ct-literature has supported an OpenAlex API key since v0.3.3; **since v0.3.4 it auto-loads the skill-directory `.env`**, enabling "drop the key in and it just works, zero extra flags".

---

## 1. Why a key is needed

- OpenAlex has **required an API key since 2026-02-13**.
- No key: only **100 credits/day** (officially flagged *not suitable for production*).
- Free key: **~$1/day ≈ 100k credits/day** — enough for scale (≈1000 list/filter, 100 search calls).
- Billing (charged only above the free allowance; usually zero cost):

| Operation | Cost / 1k | Notes |
|---|---|---|
| Single-entity query (by ID / DOI) | Free | Fetching a single work is always free |
| List + Filter | $0.10 | Routine list / filter |
| Search (full-text) | $1.00 | Keyword full-text search |
| PDF / XML full text | $10.00 | `content` API full-text download |

> Routine literature search almost only uses List+Filter ($0.10/1k); the free $1/day budget is very generous.

---

## 2. Application steps (~30s, free)

1. Open **https://openalex.org** and register a free account (email required).
2. After login, visit **https://openalex.org/settings/api**.
3. Copy the **API key** (a string bound to your account).
4. Do not leak it; do not commit it to git.

---

## 3. Three configuration methods (most-recommended first)

### Method A: skill `.env` (recommended, zero-friction, no per-call flag)

```bash
cd ~/.workbuddy/skills/ct-literature
cp .env.example .env
# edit .env -> set OPENALEX_API_KEY=your_openalex_api_key_here
```

Then just run, no `--openalex-key` needed:

```bash
python scripts/ct_literature.py --topic "osimertinib" --safety --run --out-dir ./out
```

`http_utils.load_openalex_key()` resolves the key at startup in this order:
1. Env var `OPENALEX_API_KEY` (if `export`ed);
2. Skill-root `.env`;
3. `scripts/.env`.

On a hit it writes back to `os.environ` for later calls to reuse. **The key value is never printed to logs.**

### Method B: environment variable (for CI / shell sessions)

```bash
export OPENALEX_API_KEY="your_free_key"
python scripts/ct_literature.py --topic "osimertinib" --safety --run --out-dir ./out
```

### Method C: command line (one-off, avoids writing to disk)

```bash
python scripts/ct_literature.py --topic "osimertinib" --safety --run \
    --out-dir ./out --openalex-key "$OPENALEX_API_KEY"
```

---

## 4. Code integration points (ready, no further change)

| Module | Entry | Notes |
|---|---|---|
| `scripts/http_utils.py` | `load_openalex_key()` / `build_openalex_headers(api_key, mailto)` | Resolves key (env → .env); builds `Authorization: Bearer <key>` + polite-pool `mailto` UA |
| `scripts/fetch_openalex.py` | `fetch(..., api_key=None)` + `main --openalex-key` (default `load_openalex_key()`) | Injects Bearer into the primary request; **standalone run also picks up `.env`** |
| `scripts/ct_literature.py` | `run(..., openalex_key=None)` + `main --openalex-key` (default `load_openalex_key()`) | Orchestrator passes the key through |

---

## 5. Verify the key is active

- Validate the load logic without network:

  ```bash
  python -c "import sys; sys.path.insert(0,'scripts'); import http_utils; \
  print('LOADED' if http_utils.load_openalex_key() else 'NO KEY')"
  ```

  Prints only whether it loaded, **never the key value**.

- Real run: with the key, OpenAlex paging no longer hits the 100/day limit; if 429 still appears, the key is likely unloaded or the quota is exhausted.

---

## 6. Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Still only ~100/day | Key unloaded (wrong path / `OPENALEX_API_KEY` unset) | Use the §5 command to confirm `LOADED`; check `.env` is in the skill root |
| HTTP 401 | Invalid / malformed key | Re-copy the key from settings/api |
| Persistent HTTP 429 | Daily free quota exhausted (>100k) | Wait until next day / upgrade plan; or reduce search-type calls |
| Key committed to git | `.env` not ignored | `.gitignore` already ignores `.env`; if already committed, revoke and regenerate immediately |

---

## 7. Security notes

- `.env` is in the skill's `.gitignore` and **is never pushed to any remote**.
- The key never appears in plaintext in logs / reports / stdout (only whether it loaded is printed).
- Do not paste a real key into README / SKILL.md / chat.
- If leakage is suspected: revoke and regenerate at https://openalex.org/settings/api.
