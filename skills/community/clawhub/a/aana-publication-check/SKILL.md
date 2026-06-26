# AANA Publication Check Skill

Use this skill when an OpenClaw-style agent may publish, update, send, post, release, or prepare public-facing content such as posts, blogs, reports, documentation, changelogs, press copy, website updates, newsletters, social posts, papers, or public repository pages.

This is an instruction-only skill. It does not install packages, run commands, write files, call services, persist memory, or execute a checker on its own.

## Core Principle

Before publishing, the agent should check that the content is authorized, accurate, sourced, privacy-safe, scoped to the intended audience, and ready for public or external visibility.

The agent should separate:

- drafts that can be revised privately,
- content ready for review,
- content that needs citations or evidence,
- content that needs privacy redaction,
- content that needs permission or owner approval,
- content that needs legal, compliance, brand, or domain review,
- content that should not be published.

## When To Use

Use this skill before:

- publishing or updating posts, blogs, reports, docs, websites, readmes, release notes, public issue comments, or social content,
- sending newsletters, public announcements, support articles, or external documentation,
- claiming benchmark results, safety results, compliance, guarantees, model behavior, product features, timelines, prices, or policies,
- including citations, quotes, screenshots, charts, images, videos, datasets, logs, customer examples, or private records,
- changing public website pages, docs pages, repo About text, marketplace listings, or download pages.

## Publication Categories

Classify the proposed publication:

- `draft`: private work-in-progress.
- `internal_review`: not public; needs team or owner review.
- `ready_public`: approved, accurate, sourced, scoped, and privacy-safe.
- `needs_evidence`: factual claims need sources, citations, tests, or records.
- `needs_redaction`: private, sensitive, or unrelated data must be removed.
- `needs_permission`: publication, asset, quote, claim, or external-send approval is missing.
- `needs_review`: legal, compliance, medical, financial, safety, brand, or domain review is needed.
- `block_publish`: unsafe, unauthorized, deceptive, or materially unsupported.

## AANA Publication Gate Loop

1. Identify the publication target and audience.
2. Identify what will become public or externally visible.
3. Check authority: user approval, owner approval, publishing rights, and target scope.
4. Check evidence: factual claims, citations, links, test results, quotes, screenshots, charts, and uncertainty.
5. Check privacy: personal data, customer data, account data, secrets, logs, private messages, internal URLs, and metadata.
6. Check permissions: images, videos, datasets, quotes, trademarks, third-party material, and confidential information.
7. Check impact: legal, medical, financial, safety, compliance, reputation, market, or public-risk consequences.
8. Check quality: broken links, wrong downloads, stale copy, missing alt text, inconsistent claims, and unclear calls to action.
9. Choose action: publish, revise, retrieve, ask, request approval, route to review, or block.

## Required Pre-Publish Checks

Before publishing, verify:

- publication target,
- intended audience,
- content summary,
- publication scope,
- approval status,
- evidence status,
- privacy status,
- asset permission status,
- link/download status,
- risk level,
- recommended action.

## Evidence Rules

Do not publish unsupported claims about:

- benchmark results,
- safety or alignment guarantees,
- medical, legal, financial, tax, or compliance advice,
- product features, availability, pricing, timelines, or policies,
- customer outcomes,
- citations, quotes, or source interpretations,
- security, privacy, or reliability claims.

Use visible caveats for early research, examples, internal experiments, estimates, or claims that are not independently verified.

## Privacy And Redaction Rules

Do not publish:

- secrets, credentials, keys, tokens, cookies, auth headers, or private URLs,
- payment data, bank details, tax IDs, government IDs, health/legal/financial records,
- private messages, full logs, account records, customer records, employee records, student records, or support tickets,
- non-public names, emails, phone numbers, addresses, screenshots, or metadata unless clearly approved,
- internal-only decisions, vulnerabilities, contracts, confidential plans, or proprietary datasets.

Prefer redacted examples, synthetic examples, aggregate results, and public-safe summaries.

## Permission Rules

Require approval before publishing:

- content externally or publicly,
- third-party quotes, screenshots, images, video, datasets, or logos,
- customer stories, support examples, or account facts,
- legal, medical, financial, safety, compliance, or security-sensitive claims,
- releases, tags, public docs, website updates, or marketplace listings.

Do not treat draft approval as publish approval unless the user explicitly approved publication.

## Quality Rules

Before publication, check:

- links and downloads point to the intended files,
- screenshots, thumbnails, images, videos, and PDFs match their labels,
- claims are consistent across README, site, docs, release notes, and marketplace copy,
- dates, versions, filenames, and URLs are current,
- alt text and accessible labels are present where relevant,
- public copy avoids overclaiming and clearly marks limitations.

## Review Payload

When using a configured AANA checker, send only a minimal redacted review payload:

- `publication_target`
- `audience`
- `content_summary`
- `publication_status`
- `approval_status`
- `evidence_status`
- `privacy_status`
- `asset_permission_status`
- `quality_status`
- `risk_level`
- `recommended_action`

Do not include raw secrets, credentials, full private records, full logs, full transcripts, full account records, unpublished customer data, or unrelated private data when a redacted summary is enough.

## Decision Rule

- If content is approved, accurate, sourced, privacy-safe, permissioned, scoped, and low-risk, publish.
- If claims need evidence, retrieve or revise.
- If private data appears, redact before review or publication.
- If publication approval is missing, request approval.
- If legal, medical, financial, compliance, safety, security, brand, or customer impact is plausible, route to review.
- If content is unsafe, unauthorized, deceptive, materially unsupported, or privacy-violating, block publication.
- If a checker is unavailable or untrusted, use manual publication review.

## Output Pattern

For publication-sensitive work, prefer:

```text
AANA publication check:
- Target: ...
- Audience: ...
- Content: ...
- Approval: approved / required / unclear / denied
- Evidence: sufficient / partial / missing / stale / conflicting
- Privacy: clear / needs_redaction / sensitive / unknown
- Assets: permissioned / needs_permission / third_party / unknown / not_applicable
- Quality: ready / revise_links / revise_copy / check_downloads / unknown
- Risk: low / moderate / high / professional / legal / financial / safety / reputation / unknown
- Decision: publish / revise / retrieve / ask / request_approval / route_to_review / block
```

Do not include this check in the user-facing answer unless review, approval, revision, or a publication blocker needs to be explained.
