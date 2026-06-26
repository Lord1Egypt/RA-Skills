# GitHub Datasets and Repositories Useful for Advisor Finder

This file lists external repositories that can improve advisor discovery, department verification, and faculty activity checks.

These sources are helpers, not final authority. Always verify school affiliation and homepage details against official pages when possible.

## 1. CSrankings
- Repository: https://github.com/emeryberger/CSrankings
- Website: https://csrankings.org
- Why it matters:
  - tracks active computer science faculty across many institutions
  - includes institution mappings, homepages, DBLP identities, Google Scholar IDs, ORCID hints, and publication-based area signals
  - is much more useful than a generic university list for CS advisor finding
- What to use from it:
  - institution names and aliases
  - faculty names
  - homepage links
  - DBLP disambiguation info
  - Google Scholar / ORCID related fields when available
  - area-based research activity clues
- Important limitation:
  - not every university or department is complete
  - stronger for computer science than for all academic fields
  - not an official faculty directory

## 2. World universities CSV repos
Examples:
- https://github.com/endSly/world-universities-csv
- https://github.com/Geziwen/world-universities

Why they matter:
- useful for normalizing school names and domains
- useful when the user gives only a fuzzy English school name

Limitation:
- only school-level metadata
- not useful for finding faculty directly

## How Advisor Finder should use these sources

### Preferred order
1. official university / department / faculty page
2. official personal homepage
3. CSrankings or similar structured faculty dataset
4. scholar and paper sources
5. third-party pages

### Best use cases for CSrankings
- target field is computer science or adjacent AI fields
- official department site is weak or incomplete
- need to cross-check whether a faculty member is active in a subarea
- need homepage and identity disambiguation help

### Hard rule
Do not treat a GitHub dataset as stronger than an official faculty page.
Use it to recover from poor websites, fill candidate pools, or resolve name/affiliation ambiguity.
