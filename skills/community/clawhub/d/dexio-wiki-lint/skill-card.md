## Description:

Checks Markdown wikis for broken links, possible secrets, missing metadata, stale or hard-to-find pages, oversized pages, and duplicate titles, then guides deliberate repairs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dexio](https://clawhub.ai/user/dexio)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents maintaining Markdown wikis use this skill to identify broken links, possible credential leaks, and pages needing review before commits, after refactors, or during scheduled maintenance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Lint output can reveal the location and type of possible credentials in wiki pages.

Mitigation: Run only on intended wiki folders, limit access to reports, and review affected pages; rotate confirmed exposed credentials.

Risk: Automated edits based on stale-page or link findings can remove useful content or create misleading fixes.

Mitigation: Review suggested changes and underlying pages before committing or scheduling repairs; rerun the linter after edits.

## Reference(s):

- [Wiki Lint (Dexio) release](https://clawhub.ai/dexio/skills/dexio-wiki-lint)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Plain-text or JSON wiki health report with agent-authored repair guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can produce a page catalog, incoming-link list, or verification queue; reports possible secrets without revealing their values.]

## Skill Version(s):

1.2.0 (source: release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
