## Description: <br>
The video search layer for AI agents; it helps agents search video by meaning across speech, visuals, and on-screen text when users need video evidence, citations, or timestamped answers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jessytsui](https://clawhub.ai/user/jessytsui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agents use this skill to answer questions about videos, talks, podcasts, interviews, and presentations with cited video URLs and timestamps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks agents to persist the user's Cerul API key in a local credentials file, which can expose the key if the file is printed, copied, or reused. <br>
Mitigation: Use a limited or revocable API key, keep the credentials file private, avoid displaying it in agent output, and prefer an environment variable or managed secret store when compatible. <br>
Risk: The skill installs and runs an external CLI before performing video searches. <br>
Mitigation: Review the CLI source and install command before use, install only from trusted Cerul sources, and run the skill in an environment where CLI access is appropriate. <br>


## Reference(s): <br>
- [Cerul homepage](https://github.com/cerul-ai/cerul) <br>
- [Cerul CLI repository](https://github.com/cerul-ai/cerul-cli) <br>
- [Cerul documentation](https://cerul.ai/docs) <br>
- [Cerul Python SDK](https://pypi.org/project/cerul/) <br>
- [Cerul TypeScript SDK](https://www.npmjs.com/package/cerul) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with video URLs, timestamps, transcript-based citations, and optional shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the cerul CLI and a Cerul API key; search output should use the agent-oriented CLI format.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
