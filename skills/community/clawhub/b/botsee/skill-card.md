## Description: <br>
Monitor your brand's AI visibility via BotSee API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[grahac](https://clawhub.ai/user/grahac) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use BotSee to connect an agent to a BotSee account, create sites, run AI visibility analyses, review competitors, keywords, sources, and responses, and generate content from analysis results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access BotSee account data and saves the BotSee API key in local configuration. <br>
Mitigation: Install only for trusted BotSee accounts, use the signup-status flow or deliberate local CLI invocation for API keys, and protect the local BotSee config file. <br>
Risk: USDC signup and top-up flows can involve real payments. <br>
Mitigation: Confirm payment amounts, wallet details, payment proofs, and the returned payment requirements before submitting a payment. <br>
Risk: Archive and delete commands can change or remove BotSee resources. <br>
Mitigation: Confirm UUID targets and intended archive or delete actions before running mutating commands. <br>
Risk: Changing BOTSEE_BASE_URL can redirect requests to a non-default BotSee endpoint. <br>
Mitigation: Keep BOTSEE_BASE_URL unset unless testing against a trusted BotSee endpoint. <br>


## Reference(s): <br>
- [BotSee ClawHub page](https://clawhub.ai/grahac/botsee) <br>
- [BotSee homepage](https://botsee.io) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Guidance] <br>
**Output Format:** [Markdown and human-readable text, with JSON responses and local configuration files for some commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can save account and site configuration locally, run polling analysis workflows, and create timestamped markdown content files.] <br>

## Skill Version(s): <br>
0.2.5 (source: server release metadata, skill frontmatter, changelog dated 2026-02-24) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
