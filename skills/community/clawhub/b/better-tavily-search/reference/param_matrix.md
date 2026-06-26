# Parameter Matrix

This reference lists the Tavily controls that matter most for an agent-facing search skill.
The left column uses the actual CLI surface exposed by `scripts/tavily.py`.

## Search Parameters

| CLI flag | Default | Use it for | Avoid / notes |
|---|---:|---|---|
| `--query` | required | The retrieval intent itself | Keep compact and focused |
| `--profile` | `general` | Express high-level planning intent before low-level tuning | `official` and `precision` are wrapper profiles, not Tavily topics |
| `--topic` | profile-dependent | `news` for recent events, `finance` for market/company info | Do not use `news` for timeless documentation |
| `--search-depth` | profile-dependent, usually `basic` | `ultra-fast` or `fast` for iteration, `advanced` for high precision | Do not jump to `advanced` by default |
| `--max-results` | `5` | Small evidence sets for agent inspection | Large result sets bloat context |
| `--time-range` | none | Relative recency filters like day/week/month/year | Use exact dates when the time window is known |
| `--start-date` / `--end-date` | none | Precise time-bounded searches | Prefer over vague date terms when exact windows matter |
| `--include-domains` | none | Official docs, standards bodies, primary sources, site-specific search | Over-filtering can hide useful corroboration |
| `--exclude-domains` | none | Excluding spammy or repetitive sources | Use sparingly |
| `--country` | none | Regionalized search intent for general search | The wrapper warns and omits it when `topic` is not `general` |
| `--exact-match` | `false` | Exact phrases, product flags, error strings, titles | Too strict for exploratory search |
| `--auto-parameters` | `false` | Recovery path when manual profile selection is uncertain or weak | Use after one failed manual attempt, not as default |
| `--chunks-per-source` | profile-dependent or none | More relevant chunks from the same URL during precise search | The wrapper only sends it for `advanced` search |
| `--include-answer [basic\|advanced]` | off | Optional short synthesis when that helps inspection | Do not let answer-first replace evidence review |
| `--include-raw-content [markdown\|text]` | off | Only when the first pass is not enough and extraction is unavailable or unsuitable | Prefer `extract` for targeted reading |
| `--include-favicon` | `false` | UI polish or domain-rich visual outputs | Usually unnecessary for machine use |
| `--safe-search` | `false` | Enterprise-safe filtering when available | Requires `basic` or `advanced`; not supported with `fast` or `ultra-fast` |
| `--include-usage` | on | Credit and cost awareness in agent workflows | Can be disabled in human-facing or compatibility flows |
| `--format` | `agent` | Choose the output contract | `brave` exists only for `search` |

## Extract Parameters

| CLI flag | Default | Use it for | Avoid / notes |
|---|---:|---|---|
| `--urls` | required | Read the best 1–3 URLs after search | Do not batch too many pages at once |
| `--query` | none | Rerank extracted chunks to the current intent | Add it whenever only parts of the page matter |
| `--chunks-per-source` | `3` when `--query` is present | Return a few relevant chunks per page | Only sent when `--query` is present |
| `--extract-depth` | `basic` | `advanced` when extraction quality matters more than speed | Start basic unless the first pass is weak |
| `--content-format` | `markdown` | Machine-readable and concise content for downstream reasoning | Use `text` only when markdown harms parsing |
| `--include-images` | `false` | Preserve image URLs from extracted pages | Usually unnecessary unless media matters |
| `--include-favicon` | `false` | UI polish or domain-rich rendering | Optional |
| `--request-timeout` | none | Tight control over slow or fragile pages | Must be between 1 and 60 seconds |
| `--include-usage` | on | Cost awareness | Optional in human-facing output |
| `--format` | `agent` | Choose machine or human output | No `brave` mode for extract |

## Map Parameters

| CLI flag | Default | Use it for | Avoid / notes |
|---|---:|---|---|
| `--url` | required | Discover structure of a docs site or knowledge base | Not needed for ordinary web search |
| `--instructions` | none | Bias map discovery toward a section or topic | Keep instructions short |
| `--max-depth` | `1` | Control traversal depth | Must be between 1 and 5 |
| `--max-breadth` | `20` | Control traversal breadth per level | Must be between 1 and 500 |
| `--limit` | `50` | Hard cap on total discovered URLs | Keep conservative |
| `--select-paths` | none | Include only matching path patterns | Regex-like filtering can exclude useful pages if too narrow |
| `--select-domains` | none | Include only matching domains | Useful for multi-domain doc trees |
| `--exclude-paths` | none | Exclude noisy sections | Use to avoid blog/news/changelog clutter |
| `--exclude-domains` | none | Exclude external or irrelevant domains | Useful when site nav leaks elsewhere |
| `--allow-external` | `false` | Permit off-site links in map results | Default is conservative: external links stay off unless explicitly requested |
| `--request-timeout` | none | Long-running site maps | Must be between 10 and 150 seconds |
| `--include-usage` | on | Cost awareness | Optional in human-facing output |
| `--format` | `agent` | Choose machine or human output | No `brave` mode for map |

## Stable Skill Defaults

The wrapper should set conservative defaults unless the model has a clear reason to override them.

Recommended defaults:
- `include_answer=false`
- `include_raw_content=false`
- `include_usage=true` for machine-facing outputs
- `include_favicon=false`
- `max_results=5`
- `search_depth=basic` except for the `precision` profile
- `extract_depth=basic`

## What the Model Should Usually Decide

The model should usually decide:
- the query
- the profile
- whether time matters
- whether domain filtering helps
- whether exact matching is appropriate
- whether a second search or extraction pass is necessary

The wrapper should usually decide:
- conservative defaults
- stable output shape
- payload-size safeguards
- validation and normalization
