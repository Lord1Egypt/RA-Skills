## Description:

Free keyword research using Google PAA, Autocomplete, Reddit discussions, and Bing. No paid API needed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lal24886695](https://clawhub.ai/user/lal24886695)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, SEO practitioners, and content strategists use this skill to run no-cost keyword research from public Google, Reddit, and Bing sources for content planning, keyword clustering, topic ideation, and competitive content gap analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reddit mode can return unexpected adult or sensitive content because the scanned release searches sexual and relationship subreddits by default.

Mitigation: Use non-Reddit sources when that content is inappropriate, review outputs before sharing them, and run the tool only in workspaces approved for this type of content.

Risk: The skill makes outbound requests to public Google, Reddit, and Bing endpoints and may encounter rate limits, blocks, or unavailable results.

Mitigation: Run it in a low-privilege environment, expect partial results, and avoid high-volume use without confirming the relevant service terms and limits.

Risk: The command writes a local JSON file to the path provided by the caller.

Mitigation: Choose an output path that will not overwrite important files and review the generated JSON before using it in downstream workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lal24886695/skills/free-keyword-miner)
- [Artifact README](artifact/README.md)
- [Artifact skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with shell commands and a JSON results file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes keyword results to a caller-selected local JSON path; network results depend on public Google, Reddit, and Bing availability and rate limits.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
