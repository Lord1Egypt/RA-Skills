## Description:

Analyzes Chinese A-share stocks with ChanLun technical-analysis methods, fetching K-line data and producing structured buy and sell signals with trading-reference guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hunkguo](https://clawhub.ai/user/hunkguo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to run ChanLun-style technical analysis for A-share stock codes and review structured signals, trend context, and informational trading suggestions. The output is for reference only and is not investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Trading guidance can be misunderstood as investment advice.

Mitigation: Treat all generated signals as informational technical-analysis output and preserve the skill's explicit investment-risk disclaimer.

Risk: The script performs disclosed network calls to public quote servers and depends on runtime Python packages.

Mitigation: Install and run it in an isolated Python environment without elevated privileges, with dependencies pinned by the publisher.

Risk: Local temporary caching and loose stock-code handling can create hygiene issues.

Mitigation: Validate stock codes as exactly six digits and harden or disable the temporary cache before operational use.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON analysis output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The CLI accepts a six-digit stock code plus optional period, count, and recent-window arguments.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
