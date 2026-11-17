## Description:

Run a full equity research report on a stock by coordinating local price, fundamentals, and market-news scripts with uv run.

This skill is ready for commercial/non-commercial use.

## Publisher:

[youpele52](https://clawhub.ai/user/youpele52)

### License/Terms of Use:


## Use Case:

Investors, analysts, and agents use this skill to combine price, fundamentals, and market-context signals for a stock into a structured equity research report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill delegates its work to separate local stock-price, fundamentals, and market-news scripts plus uv-resolved Python dependencies outside the reviewed artifact.

Mitigation: Install only after reviewing those referenced skills, protecting their integrity, and ensuring ticker arguments are executed safely rather than interpolated into shell commands.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/youpele52/skills/equity-research)
- [Yahoo Finance](https://finance.yahoo.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown report with command-driven evidence synthesis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Depends on valid Yahoo Finance tickers, uv, and separately installed local price, fundamentals, and market-news skills.]

## Skill Version(s):

0.1.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
