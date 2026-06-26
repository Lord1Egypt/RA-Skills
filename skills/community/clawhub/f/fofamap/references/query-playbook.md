# Query Playbook

## Mode selection

- `search`: concrete asset list
- `search-next`: continuous paging for larger result harvests without page-number drift
- `host`: one IP or one domain, deeper profile
- `stats`: rankings, distributions, and aggregates
- `icon-hash`: derive an `icon_hash` query from a website
- `monitor-run`: recurring inventory watch with baseline, drift comparison, and alert-friendly reports

When the task is exploratory, hunt-style, or under-specified, also consult:

- `references/syntax-arsenal.md`
- `references/syntax-corpus.tsv`
- `references/redteam-hunt-playbook.md` when the goal is attack infrastructure, takeover, deception, or cloud/API leak hunting
- `references/report-templates.md` when the user wants a persuasive report or a specific analyst lens
- `references/evolution-playbook.md` when the task is recurring or the skill should learn from prior runs

## Permission-first planning

When the user asks for advanced fields or for `host` or `stats`, call `login` first and inspect `permission_profile`.

- `vip_level 0`: no `host`, no `stats`
- `vip_level 1` and `11`: `host` yes, `stats` no
- `vip_level 2`, `12`, `13`, `5`: `host` yes, `stats` yes
- `vip_level 13` and `5`: deep search fields such as `product.version` and `cert.is_valid`
- `vip_level 5`: adds `icon`, `fid`, and `structinfo`

Also read:

- `documented_search_export_field_count`
- `data_limit`
- `search_field_presets`

If the user intent is fuzzy, search `references/syntax-corpus.tsv` by:

- product name
- Chinese or English rule name
- exposure tags such as `unauth`, `db`, `jenkins`, `redis`, `jboss`, `log4j2`
- distinctive strings that may appear in `title`, `body`, `header`, `banner`, or `icon_hash`

## Safe baseline fields

Use these first unless the user explicitly needs something richer:

`host,ip,port,protocol,title,domain,country_name,server`

This skill's helper script falls back to that set when FOFA rejects a higher-tier field request.

## Advanced field reminders

Field availability depends on FOFA plan level. Practical guidance:

- broadly safe: `host`, `ip`, `port`, `protocol`, `title`, `domain`, `server`, `country_name`, `asn`, `org`, `status_code`
- personal-tier add-ons: `header_hash`, `banner_hash`, `banner_fid`
- professional-tier add-ons: `product`, `product_category`, `cname`, `lastupdatetime`
- business-tier add-ons: `body`, `icon_hash`, `product.version`, `cert.is_valid`, `cname_domain`, `cert.is_match`, `cert.is_equal`
- enterprise-only add-ons: `icon`, `fid`, `structinfo`

If FOFA rejects a query because of field permissions:

1. rerun with the safe baseline
2. preserve the original query
3. explain that the field set, not necessarily the query logic, caused the downgrade

The helper now also drops known over-tier fields before the request and reports them in `field_resolution.dropped_fields`.

## Divergent query planning

Do not force every task into one exact query. Use controlled branching.

Prefer building:

1. one precise query
2. one supporting query from a different signal family
3. one broader fallback query

Typical branch directions:

- from `app=` to `title=` or `body=`
- from a product to an exposure class such as `unauth`
- from a web panel artifact to a service family such as `protocol=redis`
- from a product name to a dashboard title or static response string
- from a domain or org to certificate, ASN, or geography pivots
- from one weak clue to a fingerprint family such as `icon_hash=`, `header=`, or `server=`

Label these clearly when reporting them so the user knows which query is exact and which is exploratory.

The syntax corpus is a seed library, not a straightjacket. If the workbook has no exact rule, invent a nearby query that preserves the same operational goal.

## Report framing

When the user wants a delivery artifact, do not default to one generic summary voice. Pick the lens that matches the mission:

- `standard`: general asset handoff
- `attack-infrastructure`: suspicious infra clustering, tooling, and campaign-style patterns
- `abnormal-exposure`: admin surface, middleware exposure, leaks, and odd service reachability
- `takeover-risk`: dangling domains, placeholder pages, and abandoned platform indicators

The helper supports `--report-profile` for `search`, `search-next`, `project-run`, `monitor-run`, `host`, and `stats`.

## Learning loop

The helper now records local memory after the main FOFA modes run. Use that to make the next task better instead of starting from zero every time.

- default memory directory: `results/fofamap_memory`
- latest reflection: `latest_reflection.md`
- aggregated memory: `semantic-patterns.json`
- explicit review command: `python3 scripts/fofa_recon.py learn-review`

If the same target class, org, or hunt family appears again, read the latest reflection first and reuse the strongest recurring lessons.

## Query construction patterns

### Asset list

- `app="HIKVISION-Video Surveillance"`
- `app="ThinkPHP" && country="CN"`
- `(app="seeyon" || app="yonyou") && region="Beijing"`
- `protocol="mysql" && country="US"`

### Login and panel hunting

- `title="login"`
- `body="admin"`
- `(title="login" || body="signin") && protocol="http"`

### Certificate and organization pivots

- `cert="google"`
- `cert.subject.org="Google"`
- `org="Cloudflare"`

### Fingerprint and infrastructure pivots

- `icon_hash="-1231872293"`
- `icon_hash="1578525679"`
- `asn="45102" && app="COBALTSTRIKE-beacon"`
- `asn="16509" && app="RAPID7-Metasploit"`

### Geography and scoping pivots

- `city="Hangzhou" && domain="edu.cn"`
- `city="Shenzhen" && app="HIKVISION"`
- `city="Chengdu" && port="3389"`
- `country="CN" && city!="Hong Kong"`

### API and anomaly pivots

- `domain="example.com" && body="ListBucketResult"`
- `body="/api/v1" && domain="example.com"`
- `body="algolia_api_key" && domain="example.com"`
- `body="hacked by"`

### Icon-based pivots

1. compute the favicon hash with the helper script
2. use the returned `fofa_query`

## Continuous paging

Use `search-next` when the user wants more than one ordinary page and data ordering matters.

- Endpoint: `/api/v1/search/next`
- Required parameter: `qbase64`
- Common parameters: `fields`, `size`, `next`, `full`
- Resume token: FOFA returns `next` in each response; pass that token into the next request

Practical rules for this skill:

- For the first request, prefer omitting `next`
- The public FOFA example still shows `next=id`, so the helper accepts `id` as a compatibility sentinel and internally treats it as a first-page bootstrap
- Do not rely on `page` for control flow; real responses may return `null`
- Use `next_cursor_to_resume` from the helper output if the run should continue later

Important size caps from the FOFA docs:

- if the query contains `body`, cap `size` at `500`
- if the query contains `cert` or `banner`, cap `size` at `2000`
- otherwise FOFA allows up to `10000` rows per request

The helper reports:

- `requested_size`
- `effective_size`
- `size_limited`
- `size_limit_reasons`
- `cursor_trace`

This makes it clear when the requested size was larger than FOFA would allow.

## Corpus-driven seeding

The syntax corpus from the team workbook is best used as a seed library, not as a blind copy source.

Good uses:

- find a known query for a named product
- look up how a panel or unauth exposure is commonly expressed
- pivot from product hunt to artifact hunt
- borrow a body or title signal when `app=` is too narrow

Use `rg` when needed:

```bash
rg -n 'redis|mongodb|jenkins|jboss|weblogic' references/syntax-corpus.tsv
rg -n 'unauth|dashboard|login|admin|db' references/syntax-corpus.tsv
rg -n 'log4j2|phish|honeypot|proxy|社工库' references/syntax-corpus.tsv
```

## Operator creativity

Good FOFA hunting is not only about choosing the field. It is also about choosing the operator.

- prefer `==` when an exact token improves precision and the grammar supports it
- use `!=` to remove recurring garbage, supplier pages, or obvious false positives
- use `()` to force grouping when mixing `&&` and `||`
- use wildcard or regex thinking when title variants or login strings are the real signal

Examples of useful intent:

- `title!="供应商大全网" && body!="赌博"`
- `(title="login" || body="signin") && protocol="http"`
- `title=/(login|admin)/i`

If an exotic operator is uncertain, translate it into a safer nearby query instead of dropping the idea.

## Zero-result retry heuristics

When a search fails, do not only repeat it. Broaden it intentionally:

1. remove the narrowest geographic or version filter
2. replace exact host assumptions with broader content or product fingerprints
3. reduce a multi-clause query to the most distinctive signal
4. if a guessed domain suffix fails, try a broader keyword-based query instead

Example progression:

- strict: `app="Redis" && country="US" && city="Seattle"`
- broader: `app="Redis" && country="US"`
- broader: `protocol="redis" && country="US"`
- fallback: `title="Redis"`

If the first product-led query fails, try a different signal family from the corpus before abandoning the hunt.

## Host profiling cues

Use `host` mode when the user provides one IP or domain and wants:

- open ports
- ASN and organization
- country or geography
- ISP, country code, domains, and protocol mix
- component rules or per-port rule hints when FOFA returns them
- product hints on discovered services

Prefer `host` mode over `search` when the target is singular.

## Stats guidance

Use `stats` when the user asks for:

- country distribution
- port distribution
- top titles
- ASN or organization rankings

Good fields:

- `country`
- `port`
- `title`
- `org`
- `asn`
- `server`

FOFA's stats response can also carry:

- `consumed_fpoint`
- `required_fpoints`
- `lastupdatetime`

Keep those when the user cares about API cost or data freshness.

## Monitoring and drift analysis

Use `monitor-run` when the user wants daily, weekly, or monthly asset watch.

- Keep `--state-dir` stable across runs so the command can compare against `latest_snapshot.json`
- Prefer `--use-search-next` for larger inventories or when the user explicitly wants the continuous paging API
- The first run creates a baseline and should not be treated as an alert
- Later runs produce `latest_diff.json`, `latest_report.md`, and timestamped snapshot archives
- Add `--fail-on-change` when the surrounding scheduler or automation should raise an alert on drift

Good monitoring patterns:

- `monitor-run --query 'org=\"Example Corp\"' --state-dir results/monitor_example`
- `monitor-run --query-file queries.txt --use-search-next --max-pages 3 --state-dir results/monitor_monthly`
- `monitor-run --query 'app=\"nginx\" && country=\"US\"' --alive-check --split-exports --suggest-nuclei`

## Follow-up triage suggestions

After reviewing the FOFA data, you can suggest next steps. Keep passive findings and active checks separate.

Examples:

- Spring or Java patterns: suggest `nuclei` tags such as `spring`, `java`, or targeted CVE templates
- WebLogic or JBoss patterns: suggest `weblogic` or `jboss`
- ThinkPHP patterns: suggest `thinkphp`
- Exchange or OA patterns: suggest `exchange` or `oa`

Only recommend active validation when the user has asked for it or agreed to it.
