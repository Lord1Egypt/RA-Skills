## Description: <br>
Reviews Chinese contract files, identifies legal risks, suggests revisions, and generates Markdown review reports with original text, suggested changes, and reasons. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lingmoon96-dev](https://clawhub.ai/user/lingmoon96-dev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, legal operations teams, and contract reviewers use this skill to extract text from Chinese PDF, Word, or TXT contracts, send the contract text to a configured AI provider, and produce a structured review report. The report highlights legal risks, revision suggestions, and a three-column comparison table for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Contract text may contain confidential terms, personal data, pricing, or trade secrets that are processed by the configured AI provider. <br>
Mitigation: Redact sensitive content before use, choose an approved provider and model, and avoid broad auto-trigger use for sensitive files. <br>
Risk: The configuration file stores an API key for the selected provider. <br>
Mitigation: Keep config.json out of shared locations and version control, restrict file permissions, and rotate exposed keys. <br>
Risk: The reviewed artifact references dependencies that were not included in the artifact set. <br>
Mitigation: Verify and install dependencies from trusted package sources before running the skill. <br>
Risk: AI-generated legal-risk findings can be incomplete or inaccurate. <br>
Mitigation: Use the report as drafting and review assistance, and have qualified humans verify important contract decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lingmoon96-dev/contract-review-cn) <br>
- [Publisher profile](https://clawhub.ai/user/lingmoon96-dev) <br>
- [README.md](artifact/README.md) <br>
- [QUICKSTART.md](artifact/QUICKSTART.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [config.example.json](artifact/config.example.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown review report, command-line output, Python API result, and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports may be saved as a contract-specific _review.md file or printed with --show-only; generated content should be treated as review assistance, not final legal advice.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
