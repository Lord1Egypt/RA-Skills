# Ahrefs Domain Rating Free Skill

Agent skill for checking Ahrefs Domain Rating (DR) with the free public Ahrefs API endpoint.

- Skill name: `ahrefs-domain-rating-free`
- Repo: `AIGC-Hackers/ahrefs-domain-rating-free-skill`
- API: `GET https://api.ahrefs.com/v3/public/domain-rating-free?target=<domain-or-url>`
- Auth: no API key required
- Docs: https://docs.ahrefs.com/en/api/reference/public/get-domain-rating-free

## What It Does

This skill gives agents a reliable wrapper around Ahrefs' free Domain Rating endpoint. It is meant for quick DR checks, website authority checks, and multi-domain comparisons without requiring an Ahrefs subscription or API token.

Domain Rating is Ahrefs' score for backlink profile strength on a 100-point logarithmic scale.

## Install with skills.sh

```bash
npx skills add AIGC-Hackers/ahrefs-domain-rating-free-skill --skill ahrefs-domain-rating-free
```

List available skills in this repo:

```bash
npx skills add AIGC-Hackers/ahrefs-domain-rating-free-skill --list
```

Use once without installing:

```bash
npx skills use AIGC-Hackers/ahrefs-domain-rating-free-skill@ahrefs-domain-rating-free
```

## Install with ClawHub

After marketplace publication:

```bash
clawhub install ahrefs-domain-rating-free
# or, depending on local CLI name
clawdhub install ahrefs-domain-rating-free
```

If installing directly from GitHub before marketplace indexing:

```bash
npx skills add AIGC-Hackers/ahrefs-domain-rating-free-skill --skill ahrefs-domain-rating-free
```

## Direct Wrapper Usage

```bash
python3 scripts/ahrefs-domain-rating-free.py ahrefs.com
python3 scripts/ahrefs-domain-rating-free.py ahrefs.com example.com github.com
python3 scripts/ahrefs-domain-rating-free.py https://example.com/page --json
python3 scripts/ahrefs-domain-rating-free.py ahrefs.com --raw
```

Example output:

```text
ahrefs.com  91.0
```

JSON output:

```json
[
  {
    "target": "ahrefs.com",
    "ok": true,
    "domain_rating": 91.0
  }
]
```

## Files

```text
SKILL.md                                      Agent skill instructions
scripts/ahrefs-domain-rating-free.py          Dependency-free Python wrapper
README.md                                     Install and usage docs
LICENSE                                       MIT-0 license
```

## Verification

```bash
python3 scripts/ahrefs-domain-rating-free.py ahrefs.com --json
python3 scripts/ahrefs-domain-rating-free.py 'not a url'
npx skills add AIGC-Hackers/ahrefs-domain-rating-free-skill --list
```

Invalid targets should return a 400-style error from Ahrefs and a non-zero wrapper exit code.

## Notes

- Correct endpoint path is `/v3/public/domain-rating-free`.
- Do not send `Authorization`; endpoint is public.
- This does not return backlinks, referring domains, organic keywords, or paid Ahrefs Site Explorer metrics.
