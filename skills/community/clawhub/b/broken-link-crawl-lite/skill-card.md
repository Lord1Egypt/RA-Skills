## Description:

Extract all links from a saved HTML file and classify them — internal/external, anchors, mailto/tel, protocol-relative — plus flag obvious breakage signals (empty href, #, javascript:). Offline, no fetching. Use when the user wants to check links on a page they saved or built.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nenadzivotic](https://clawhub.ai/user/nenadzivotic)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and site authors use this skill to inspect links in a saved HTML page and identify structural issues such as empty destinations, unresolved in-page anchors, and javascript: links. It reports link categories and flags patterns without checking live server responses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan reported no findings, but only half of the components were fully inspected, so its overall confidence is medium.

Mitigation: Review the skill script and tests before relying on its results.

Risk: A structural link report could be mistaken for confirmation that external pages are reachable.

Mitigation: Treat the report as offline classification only; use a live crawler when HTTP status, redirects, or timeouts need checking.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/nenadzivotic/skills/broken-link-crawl-lite)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [JSON link report with a concise human-readable summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One report for one local HTML file; does not fetch URLs or verify live HTTP status.]

## Skill Version(s):

1.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
