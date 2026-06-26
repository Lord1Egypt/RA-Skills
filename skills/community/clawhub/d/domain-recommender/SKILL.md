---
name: domain-recommender
description: Recommend SEO-friendly, brandable domain names for an AI product idea, then verify current availability before returning candidates. Use when the user provides a product direction, keyword, or one-sentence concept and wants usable domains.
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - python3
        - dig
    homepage: https://github.com/hilaraklesantosw-art/skills
---

# Domain Recommender

Use this skill when the user gives:

- an AI application direction
- a keyword
- a short product sentence

and wants domain recommendations that are:

- SEO-friendly
- brandable
- realistically usable
- checked for current availability before you answer

## Outcome

Return a short list of domain names that are both:

- semantically strong for the product
- verified as currently available or very likely available based on live checks

Do not stop at brainstorming names. The final answer must include an availability check.

## Workflow

### 1. Understand the product and derive naming roots

Extract:

- the core problem
- the target audience
- the strongest search intent words
- the most natural noun/verb roots

Then expand into:

- singular/plural forms
- shortened roots
- phonetic or spelling variants when natural
- useful suffixes and prefixes

Example:

- `calculator` can expand to `calc`, `calcu`, `calculator`, `calcurator`
- `writer` can expand to `write`, `writer`, `scribe`, `draft`
- `meeting notes` can expand to `note`, `memo`, `meet`, `recap`, `brief`

Read [seo-brand-patterns.md](./references/seo-brand-patterns.md) for naming patterns and scoring heuristics.

### 2. Generate candidate names locally first

Use the bundled script to generate candidate domains quickly:

```bash
python3 scripts/generate_candidates.py "AI meeting notes app"
```

Optional:

```bash
python3 scripts/generate_candidates.py "AI tax calculator" --tlds com ai io app
```

The script is only a generator. It does not prove registration availability.

### 3. Rank candidates before checking availability

Prefer names that are:

- easy to spell
- short enough to remember
- semantically close to the user intent
- likely to help search relevance through the root word
- not awkward or obviously spammy

Avoid names that are:

- trademark-heavy or clearly derived from famous brands
- too long
- full of random hyphens or digits
- semantically vague
- awkward to pronounce

### 4. Verify availability with live checks

Availability is time-sensitive. You must verify it live before returning results.

Recommended order:

1. Use live web checks on registrar or marketplace pages for the exact domain.
2. Use DNS checks as a quick filter, not as the final proof.
3. If you cannot confirm registrar availability, explicitly say it is only a likely-available fallback and explain why.

At minimum:

- check the exact domain live
- include the exact TLD
- prefer confirmed availability over speculation

Use `dig` only as a helper:

```bash
dig +short example.com
dig +short NS example.com
```

Important:

- no DNS record does not guarantee the domain is unregistered
- parked domains and for-sale domains may still resolve
- the final answer should prioritize registrar-confirmed availability

### 5. Return only the best shortlist

Default to 5 results unless the user asks for more.

For each result, include:

- domain
- why it fits the product
- naming logic
- current availability status

If nothing strong is available:

- say that directly
- offer the next-best alternatives
- widen the TLD set only after `.com` and the most relevant TLDs are checked

## Output Format

Use a concise structure:

- product interpretation
- shortlisted available domains
- optional backup domains

For each domain, prefer a compact line such as:

- `calcurator.ai` — calculator root with a memorable spelling variant; confirmed available

If availability is not fully confirmed, label it clearly:

- `calcpilot.io` — strong fit, DNS-clear, but registrar confirmation not obtained

## TLD Preference

Default priority:

1. `.com`
2. `.ai`
3. `.io`
4. `.app`
5. `.co`

Adjust only when the product makes another TLD more natural.

## Scope Boundaries

This skill is for domain recommendation and availability checking.

It is not for:

- trademark clearance
- legal opinion
- full brand identity work

You may mention obvious trademark risk heuristics, but do not present that as legal clearance.
