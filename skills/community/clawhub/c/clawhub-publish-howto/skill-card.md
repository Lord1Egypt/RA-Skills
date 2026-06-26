## Description: <br>
A ClawHub publishing guide that helps agents walk users through skill release, update, authentication, verification, and troubleshooting workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bbj375767338-arch](https://clawhub.ai/user/bbj375767338-arch) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill when publishing or updating OpenClaw skills on ClawHub, especially to configure authentication, run publish commands, verify releases, and troubleshoot common publish failures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The guide includes an example that permanently stores a GitHub token in ~/.bashrc. <br>
Mitigation: Prefer temporary environment variables, an OS credential manager, or a CI secret store; rotate any token that was stored in plaintext or shared accidentally. <br>
Risk: Publishing troubleshooting can involve authentication tokens and account metadata. <br>
Mitigation: Use narrowly scoped tokens, avoid pasting secrets into logs or skill text, and verify release state with ClawHub CLI or the release page after publishing. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/bbj375767338-arch/clawhub-publish-howto) <br>
- [Publisher profile](https://clawhub.ai/user/bbj375767338-arch) <br>
- [GitHub rate limit endpoint](https://api.github.com/rate_limit) <br>
- [GitHub authenticated user endpoint](https://api.github.com/user) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash code blocks and troubleshooting tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance includes ClawHub CLI commands, GitHub token checks, and post-publish verification steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
