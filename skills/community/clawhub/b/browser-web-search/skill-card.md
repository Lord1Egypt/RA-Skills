## Description:

Browser Web Search lets agents run unified web-search commands across 55 platforms and return structured JSON, including optional OpenClaw browser-session backed adapters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sipingme](https://clawhub.ai/user/sipingme)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to retrieve structured search results, trending content, repository data, videos, transcripts, and other public or authenticated site content through a common command interface.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can invoke a third-party npm package inside an OpenClaw browser profile, including contexts that may contain authenticated site data.

Mitigation: Install only when this access is acceptable, keep BWS_PUBLIC_ONLY=1 unless authenticated adapters are intentionally needed, use a dedicated browser profile, and close unrelated logged-in tabs.

Risk: Users may bypass the safer launcher path or safer install flow described by the security evidence.

Mitigation: Use the bws-skill scripts/run.js launcher path rather than direct bws site commands, install browser-web-search@0.4.3 with --ignore-scripts, and retain the pinned integrity checks.

Risk: Sensitive browser-session calls can expose private page content if authorized accidentally or without current review.

Mitigation: Use the sealed sensitive tier, per-call opt-in, platform consent ledger, transparency output, audit log, and --dry-run preflight before real sensitive calls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sipingme/skills/browser-web-search)
- [browser-web-search-skill repository](https://github.com/sipingme/browser-web-search-skill)
- [browser-web-search core library](https://github.com/sipingme/browser-web-search)
- [browser-web-search npm package](https://www.npmjs.com/package/browser-web-search)
- [Pinned browser-web-search source](https://github.com/sipingme/browser-web-search/blob/v0.4.3/src/index.ts)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Structured JSON results with command and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Adapters may support count, sort, jq filtering, id, limit, and page options; sensitive adapters require explicit runtime gates.]

## Skill Version(s):

0.4.11 (source: server release metadata; artifact frontmatter reports 0.4.10)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
