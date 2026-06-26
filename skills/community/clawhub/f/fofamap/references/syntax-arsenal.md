# Syntax Arsenal

This reference is distilled from the team's workbook and normalized into:

- `references/syntax-corpus.tsv`

The corpus has `116` rule rows with these columns:

- `id`
- `slug`
- `rule_name_zh`
- `rule_name_en`
- `description`
- `tags`
- `fofa_query`

## Why this matters

This corpus is not just a list of saved FOFA syntax. It captures operator habits:

- think from the exposure class, not only from the product name
- combine multiple weak signals into one stronger query
- keep a broad fallback when exact product matching fails
- pivot by tags like `unauth`, `db`, `phish`, `jenkins`, `redis`, `jboss`, or `log4j2`
- treat interesting internet noise as huntable patterns, not only as CVE lookups

That means the model should use it as a brainstorming and query-design library, not as a copy-only cheatsheet.

## Creativity contract

The `116` rows are reference material, not a fence.

The model should treat the workbook as:

- a seed library for operator intuition
- a memory of what has worked before
- a map of signal families and exposure classes

The model should not treat it as:

- the only valid FOFA grammar
- a fixed menu that blocks new pivots
- a reason to stop thinking once one saved rule is found

The right mindset is:

1. borrow a good seed
2. infer adjacent signals
3. build a tighter query
4. build a broader fallback
5. keep inventing nearby pivots that preserve the same hunting goal

When a user gives a novel objective, the model should generate new FOFA combinations even if the exact syntax is not already in the workbook.

## Corpus shape

Observed signal families in the extracted rules:

- `app=` dominates the corpus and is the cleanest first choice when the product is known
- `body=` is the next most common fallback and is useful for niche panels, error pages, or hardcoded artifacts
- `title=` is common for dashboards, login panels, and Chinese-language systems
- `protocol=` appears in service or database hunts such as `redis` or `MongoDB`
- `header=` and `server=` help when application identification is weak but the web stack leaks clues
- `banner=` and `icon_hash=` appear less often but are high-value pivots when present

This tells the model how to expand:

1. Start with `app=` if the intent names a known product.
2. Add `title=` or `body=` when the product is fuzzy or panel-oriented.
3. Fall back to `protocol=`, `header=`, `server=`, or `banner=` when the service leaks more than the application.
4. Use `icon_hash=` when the UI is distinctive and reused across deployments.

## Creative pivot families

The workbook should inspire new combinations from these families.

### UI and fingerprint pivots

- `icon_hash=` when the panel UI is reused across tenants
- `title=` when a dashboard or admin panel has a stable caption
- `body=` when a framework, script, or page artifact is more durable than the product fingerprint
- `header=` or `server=` when stack leakage is stronger than app identification

Examples:

- `icon_hash="-1231872293"` for Ruoyi-like admin panels
- `icon_hash="1578525679"` for 泛微 OA style pivots
- `body="indeterminate" && body="MainController" && header="X-Powered-By: Express"`
- `body="s1v13.htm"`

### Certificate pivots

Think beyond the domain name.

- `cert.subject.org=` for holder organization pivots
- `cert.issuer.org=` for CA-based pivots
- `cert=` for broader certificate-text pivots
- `cert.subject.cn=` and `cert.issuer.cn=` for naming variants

If the user wants certificate recency or certificate lifecycle thinking, try nearby stable pivots such as:

- `cert.not_before`
- `cert.not_after`
- `after=`

Use certificate pivots to find:

- infrastructure issued by the same organization
- newly deployed HTTPS exposure
- mismatched branding across asset groups

### ASN and cloud pivots

When the real intent is "which cloud or hosting cluster is carrying this exposure", pivot by ASN.

Examples:

- `asn="45102" && app="COBALTSTRIKE-beacon"`
- `asn="16509" && app="RAPID7-Metasploit"`
- `asn="45102" && body="login"`

Treat ASN as a way to move from one asset to an infrastructure family, especially for cloud-hosted offensive tooling, SaaS assets, or burst deployments.

### Geography plus stack pivots

The strongest real-world searches often combine place and technology.

Examples:

- `city="Hangzhou" && domain="edu.cn"`
- `city="Shenzhen" && app="HIKVISION"`
- `city="Chengdu" && port="3389"`
- `city="Beijing" && cert="baidu"`
- `country="CN" && city!="Hong Kong"`

Use this when the user is really asking for:

- a local exposure map
- a provincial or city-wide campaign scan
- region-scoped asset review

### Exposure and anomaly pivots

Do not only hunt named products. Hunt behaviors and oddities.

Examples:

- `body="get all proxy from proxy pool"`
- `body="miner start"`
- `body="hacked by"`
- `title="Site not found · GitHub Pages" && server=="cloudflare"`
- `(header="uc-httpd 1.0.0" && server="JBoss-5.0") || server="Apache,Tomcat,Jboss,weblogic,phpstudy,struts"`

These are useful for:

- free proxy pools
- exposed miners
- hacked sites
- domain takeover candidates
- honeypot suspicion

### API and content pivots

Look for application logic exposure, not just login pages.

Examples:

- `body="/api/v1" && domain="example.com"`
- `body="/admin" && domain="example.com"`
- `body="config.txt" && domain="example.com"`
- `body="algolia_api_key" && domain="example.com"`
- `domain="example.com" && body="ListBucketResult"`

These are useful for:

- API surface discovery
- leaked files
- accidental key exposure
- cloud bucket enumeration

## How to use the corpus

### 1. Search by meaning, not only by exact product

When the user asks for something like:

- unauthenticated dashboards
- Redis exposure
- OA systems
- Flash phishing pages
- interesting internet oddities

Search the corpus by:

- product name
- Chinese and English rule names
- tags
- descriptive phrases

Use `rg` on `references/syntax-corpus.tsv` when you need concrete seeds.

Example searches:

```bash
rg -n 'redis|mongodb|jenkins|jboss|weblogic' references/syntax-corpus.tsv
rg -n 'unauth|dashboard|login|admin|db' references/syntax-corpus.tsv
rg -n 'log4j2|phish|honeypot|proxy|社工库' references/syntax-corpus.tsv
```

### 2. Build a three-layer query plan

Do not stop at one query when the task is important.

For a serious hunt, prefer three layers:

- primary query: the most precise rule from the corpus
- supporting query: combine another signal family such as `title=` plus `body=`
- broad query: a looser fallback that preserves the same intent

Example pattern:

- primary: `app="JENKINS"`
- supporting: `app="JENKINS" && title="Dashboard [Jenkins]"`
- broad: `title="Jenkins" || body="jenkins"`

The goal is not random expansion. The goal is controlled widening that stays semantically close to the user's intent.

### 3. Think in exposure classes

The workbook strongly reflects hunt classes. Reuse that mindset:

- `unauth`: default dashboards, admin panels, notebooks, databases
- `db`: exposed data services and unauthenticated databases
- `fun`: odd, dangerous, or operationally interesting internet artifacts
- `log4j2`: campaign or vulnerability-driven hunting

If the user gives a vague goal, translate it into one or more exposure classes first, then search the corpus for seeds.

### 4. Think in signal families

Use the corpus to switch between these families:

- product fingerprint: `app=`
- UI fingerprint: `title=`, `icon_hash=`
- page artifact: `body=`
- transport/service fingerprint: `protocol=`
- stack leakage: `header=`, `server=`, `banner=`

A strong operator does not get stuck in one family.

If `app=` fails:

- try the dashboard title
- try a static body string
- try a stack header
- try the protocol family

### 5. Think in operators, not only in fields

Creativity also comes from operator choice.

- use `==` when the exact token matters and the grammar supports it
- use `!=` to remove common garbage or supplier noise
- use `()` to force logical grouping
- use wildcard-style thinking for panel families and naming variants
- use regex-style thinking when the grammar supports it and case variation matters

Examples of intent, not rigid canon:

- `title!="供应商大全网" && body!="赌博"`
- `title="管理*系统"`
- `title=/(login|admin)/i`

If a more exotic operator is uncertain, translate the idea into a safer nearby query instead of abandoning the intent.

## Divergent thinking rules

When the user's wording is sparse, the model should branch in several controlled ways.

### Product branch

Ask implicitly:

- what is the named product
- what nearby products or forks exist
- what admin or dashboard surfaces usually ship with it

### Exposure branch

Ask implicitly:

- is the real intent unauthenticated access
- leaked panel exposure
- known vulnerable service
- phishing or malicious content
- odd internet telemetry

### Artifact branch

Ask implicitly:

- what unique strings would exist in body, title, header, banner, or icon

### Protocol branch

Ask implicitly:

- is this better expressed as `protocol=redis`, `protocol="MongoDB"`, `protocol=mysql`, and so on

### Campaign branch

If the target is vulnerability-driven, search for rule seeds by campaign or attack family, not only product name.

This is especially important for rows tagged around `log4j2` or large-scale hunts.

## Zero-result expansion using the corpus

When a precise query fails:

1. keep the same hunt objective
2. switch to a different signal family from the corpus
3. remove the most brittle clause
4. widen from exact product to exposure class

Example:

- exact product panel
- same panel plus body artifact
- same exposure class plus title keyword
- same service family plus protocol

This is the right kind of divergence: same mission, broader evidence.

## Translation rules for novel ideas

When a creative idea is not obviously represented in the corpus, translate it through the closest stable family.

Examples:

- "new certificates" -> `cert.subject.org=`, `cert.issuer.org=`, `cert.not_before`, `after=`
- "same UI across many tenants" -> `icon_hash=`, `title=`, `body=`
- "same cloud cluster" -> `asn=`, `org=`, `country=`
- "same backend stack" -> `server=`, `header=`, `banner=`, `product=`
- "same protocol family" -> `protocol=`, `base_protocol=`, `port=`

The goal is to keep inventing adjacent pivots even when the exact saved rule does not exist.

## Precision rules

Do not blindly copy every workbook rule into production use.

- Some rules are campaign- or era-specific.
- Some version strings may age.
- Some interesting-rule rows are exploratory and should be labeled as hunt seeds, not guaranteed matches.

When you borrow a rule from the corpus:

- explain it as a seed query if confidence is moderate
- prefer combining it with a second signal for higher precision
- separate precise queries from exploratory queries in the output

## Recommended agent behavior

When the user asks for a fuzzy or hunt-style FOFA task:

1. inspect `references/syntax-arsenal.md`
2. grep `references/syntax-corpus.tsv` for tags, names, or artifacts
3. propose or run one primary query plus one or two fallback queries
4. label each query as `precise`, `supporting`, or `broad`
5. if results are empty, pivot by signal family before giving up

This preserves the workbook's real value: not memorizing syntax, but learning how experienced operators think with FOFA.
