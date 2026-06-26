## Description: <br>
Personalized GitHub digest - tracks activity from people you follow, GitHub Trending, and hot new projects. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[miraclemin](https://clawhub.ai/user/miraclemin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and GitHub users use this skill to configure and receive personalized daily or weekly digests covering followed users, GitHub Trending repositories, and fast-growing new projects. It can deliver digests in chat, stdout, Telegram, or email depending on the user's setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores GitHub, Telegram, or Resend credentials under ~/.follow-github when the user enables those integrations. <br>
Mitigation: Use narrowly scoped read-only GitHub permissions, protect the .env file, and avoid Telegram or email delivery when stdout or on-demand use is sufficient. <br>
Risk: Recurring digest jobs can run automatically if the user enables scheduled delivery. <br>
Mitigation: Review cron entries after setup and choose on-demand/stdout delivery when background execution is not desired. <br>
Risk: A configured remote prompt URL could change summarization behavior outside the bundled artifact. <br>
Mitigation: Leave prompts.remoteUrl unset unless the user controls and trusts the remote prompt source. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/miraclemin/follow-github) <br>
- [GitHub fine-grained personal access tokens](https://github.com/settings/personal-access-tokens/new) <br>
- [GitHub classic personal access tokens](https://github.com/settings/tokens/new) <br>
- [Resend](https://resend.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown digest text, JSON from helper scripts, and inline shell commands for setup or delivery] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Digest content depends on live GitHub data, local user configuration, selected delivery channel, and optional language translation settings.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
