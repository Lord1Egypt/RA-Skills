## Description:

AI-powered Reddit seeding agent for founders that analyzes a product spec, maps relevant subreddits, finds matching Reddit threads, drafts personalized replies and DMs, and posts only approved outreach through Reddit API or browser automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xconal](https://clawhub.ai/user/0xconal)

### License/Terms of Use:


## Use Case:

External founders and growth operators use this skill to find Reddit conversations where potential users are already expressing relevant needs, then prepare human-reviewed replies and DMs for early user acquisition.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires Reddit credentials and can post replies or send DMs from a real Reddit account after approval.

Mitigation: Use the least-privileged Reddit OAuth or token setup available, store credentials outside the skill content, and manually review every message before sending.

Risk: Outreach may violate subreddit norms, Reddit rules, or user expectations if targeting and message review are weak.

Mitigation: Confirm subreddit rules before outreach, keep the built-in approval gate and rate limits, and stop activity after removals, warnings, or negative responses.

Risk: Drafts, sent-message logs, contacted-user records, and metrics may be retained without a clear policy.

Mitigation: Define retention windows before use and periodically delete stale drafts, logs, contacted-user records, and engagement metrics.

Risk: The browser automation dependency may change behavior across versions.

Mitigation: Pin the Playwright MCP package version and review updates before allowing the skill to use browser automation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/0xconal/skills/acquire-first-1000-users-on-reddit)
- [Publisher profile](https://clawhub.ai/user/0xconal)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with structured research, ranked thread queues, draft messages, approval prompts, and action or monitoring logs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Reddit credentials and explicit human approval before any outreach is sent.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter version 3.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
