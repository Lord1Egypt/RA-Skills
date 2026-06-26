# Redteam Hunt Playbook

This reference captures creative FOFA use cases that matter for red-team style reconnaissance, adversary infrastructure tracking, deception review, takeover hunting, and cloud leak discovery.

Use it when the user is not only asking "what assets exist," but "what unusual, risky, or operationally interesting assets should we care about first."

## How to think

Do not reduce a hunt to one product name.

Translate the user goal into one or more of these hunt families:

- attack infrastructure
- exposed administration or unauthenticated control planes
- honeypot or deception suspicion
- domain takeover or abandoned platform exposure
- cloud bucket or API surface leakage
- mass-impact estimation for a technology or campaign

Then build:

1. one precise query
2. one supporting query from a different signal family
3. one broader fallback query

## Attack infrastructure tracking

Use FOFA to find hosted offensive tooling, staging panels, and suspicious service clusters.

Good pivots:

- `asn=` for cloud clusters
- `app=` for known framework or beacon families
- `title=` and `body=` for panel and kit artifacts
- `header=` and `server=` for brittle but sometimes unique stack leakage

Examples:

- `asn="45102" && app="COBALTSTRIKE-beacon"`
- `asn="16509" && app="RAPID7-Metasploit"`
- `body="miner start"`
- `body="get all proxy from proxy pool"`

Good follow-up questions for the agent:

- is this the same cloud family as other suspicious assets
- is the stack concentrated in one ASN or spread across multiple clouds
- does the title or body suggest a staging panel, a kit, or a management console

## Honeypot and deception review

Honeypots and decoys often leak contradictory or theatrical signals.

Look for:

- impossible or strange stack combinations
- old or generic servers mixed with enterprise middleware names
- repeated fake banners or headers across many unrelated hosts
- titles or bodies that look more like bait than operations

Examples:

- `(header="uc-httpd 1.0.0" && server="JBoss-5.0") || server="Apache,Tomcat,Jboss,weblogic,phpstudy,struts"`
- a weak product clue in `header=` combined with an implausible `server=` string
- the same `icon_hash=` or static title reused across too many clouds or geographies

Reporting rule:

- label these as deception suspicion, not confirmed honeypots
- explain which combinations feel inconsistent
- recommend careful live validation only if the user is authorized

## Domain takeover and abandoned platform hunting

This family is about finding dangling assets and forgotten application bindings.

High-value pivots:

- SaaS and hosting error pages
- cloud front-end or CDN combinations
- title strings that imply an unbound site
- organization or domain scoping

Examples:

- `title="Site not found · GitHub Pages" && server=="cloudflare"`
- `domain="example.com" && title="Site not found"`
- `domain="example.com" && body="There isn't a GitHub Pages site here."`

Good logic:

- start with one precise provider error page
- add a broader title or body fallback
- keep the organization's domain scope when possible

## Cloud bucket and file leak hunting

Bucket leaks and static hosting mistakes usually show up as content clues before they show up as product fingerprints.

Examples:

- `domain="example.com" && body="ListBucketResult"`
- `body="config.txt" && domain="example.com"`
- `body="algolia_api_key" && domain="example.com"`

Useful nearby pivots:

- `body="/api/v1"`
- `body="/admin"`
- `body="swagger"`

Reporting rule:

- separate "interesting content pattern" from "confirmed secret exposure"
- call out when the evidence is suggestive but not yet sensitive by itself

## API and application surface discovery

When the user wants hidden application surfaces, do not stop at the main login page.

Look for:

- REST path fragments
- admin path fragments
- documentation or API key strings
- framework-specific markers

Examples:

- `body="/api/v1" && domain="example.com"`
- `body="/admin" && domain="example.com"`
- `body="algolia_api_key" && domain="example.com"`

Good supporting pivots:

- `title="login"`
- `body="swagger-ui"`
- `body="openapi"`

## Defacement and abnormal content tracking

This hunt family is useful for incident response, public exposure review, and odd internet artifacts.

Examples:

- `body="hacked by"`
- `body="defaced"`
- a known brand domain combined with obvious attacker slogans or mirror-page artifacts

Good summary framing:

- what branding or organization scope was used
- whether the result looks like defacement, abuse, or simply noisy bait
- whether multiple assets share the same content marker

## Geography and organization scoped sweeps

Use place plus technology when the user wants city-level or organization-level exposure review.

Examples:

- `city="Hangzhou" && domain="edu.cn"`
- `city="Shenzhen" && app="HIKVISION"`
- `city="Chengdu" && port="3389"`
- `city="Beijing" && cert="baidu"`
- `country="CN" && city!="Hong Kong"`

This is especially useful for:

- regional attack-surface review
- sector-wide scans
- public incident scoping

## Fingerprint-first platform hunting

When products reuse the same UI or static assets, fingerprints can outperform names.

Examples:

- `icon_hash="-1231872293"`
- `icon_hash="1578525679"`
- `title="管理*系统"`

Also consider:

- `server=`
- `header=`
- `banner=`

If the product is hard to identify by name, find the most stable visual or textual artifact instead.

## Operator moves that increase precision

Use operators creatively, not mechanically.

- `==` when exact tokens are available and reduce noise
- `!=` to remove suppliers, aggregators, gambling pages, or repeated junk
- `()` when mixing `&&` and `||`
- wildcard or regex thinking when titles have many close variants

Examples:

- `title!="供应商大全网" && body!="赌博"`
- `(title="login" || body="signin") && protocol="http"`
- `title=/(login|admin)/i`

If a specific exotic operator is uncertain, keep the idea and translate it into a safer equivalent query.

## How to turn this into a strong report

A persuasive red-team style report should answer:

- why this hunt family matters
- which query is precise and which is exploratory
- what evidence supports the finding
- what makes the asset operationally interesting
- what still needs live validation

Good ordering:

1. executive judgment
2. most interesting new or risky assets
3. supporting evidence
4. scope and caveats
5. optional next-step validation path

## Caution

FOFA gives indexed evidence, not proof of compromise or proof of exploitability.

Keep these lines clear:

- passive observation versus active confirmation
- suspicious infrastructure versus confirmed malicious infrastructure
- possible takeover candidate versus confirmed takeover
- content clue versus confirmed secret leak
