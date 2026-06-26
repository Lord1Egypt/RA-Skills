#!/usr/bin/env python3
"""Create a scaffold Expert Mode dossier markdown file.

Usage:
  python3 scripts/make_expert_dossier.py --title "Software Architect" --slug software-architect --out experts/dossiers/software-architect.md --project "Example Project"
"""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path


def render(title: str, slug: str, project: str) -> str:
    today = date.today().isoformat()
    return f"""# Expert Dossier: {title}

Version: 0.2.0
Status: candidate
Created: {today}
Updated: {today}
Project: {project}
Slug: {slug}

## Scope

TODO: Define this expert archetype and what project decisions it should influence.

## Archetype buckets

- Primary bucket: TODO
- Secondary buckets: TODO
- Why this is not just a job title: TODO

## Load when

- TODO: Add precise retrieval conditions.

## Do not load when

- TODO: Add conditions that prevent context bloat.

## Client relationship stance

- How this expert builds trust: TODO
- How this expert explains complexity: TODO
- How this expert challenges the client: TODO
- How this expert handles uncertainty: TODO
- How this expert preserves client agency: TODO
- How this expert repairs mistakes: TODO

## Expert operating loop

1. TODO: How this expert understands the goal.
2. TODO: How this expert diagnoses the real problem.
3. TODO: How this expert recommends or intervenes.
4. TODO: How this expert explains tradeoffs.
5. TODO: How this expert names risks and next steps.

## Judgement standards

- Optimizes for: TODO
- Refuses to compromise on: TODO
- Trusts this evidence: TODO
- Changes mind when: TODO
- Good enough means: TODO
- Dangerous means: TODO

## Behaviour clues

TODO: Up to 1000 words. Describe what this expert inspects, values, worries about, asks, and considers evidence.

## How this expert talks

TODO: Up to 1000 words. Describe register, directness, explanation style, uncertainty language, and critique style.

## Common jargon

TODO: Up to 1000 words. List terms, meanings, and common misuses.

## Common phrases

TODO: Up to 500 words. Add natural phrases this expert might use.

## Common metaphors

TODO: Up to 500 words. Add industry metaphors that help explain concepts.

## Explaining expertise to non-experts

TODO: Up to 500 words. Describe how this expert translates specialist concerns into everyday language.

## Definitive information sources

TODO: List authoritative sources: official docs, standards, laws, specifications, primary sources, maintainer docs, etc.

## Heuristic information sources

TODO: List practical sources: incident reports, practitioner blogs, forums, talks, benchmarks, case studies, internal history.

## Useful questions this expert asks

- TODO

## Red flags this expert notices

- TODO

## Collaboration notes

TODO: Note which other expert types this one pairs well with.

## Compression notes

TODO: Mark what to preserve when this dossier is consolidated later.
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--title", required=True)
    parser.add_argument("--slug", required=True)
    parser.add_argument("--project", default="Unnamed project")
    parser.add_argument("--out", required=True)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    out = Path(args.out)
    if out.exists() and not args.force:
        raise SystemExit(f"Refusing to overwrite existing file: {out} (use --force)")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render(args.title, args.slug, args.project), encoding="utf-8")
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
