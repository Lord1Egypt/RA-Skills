## Description: <br>
Use @ainative/svelte-sdk to add reactive AINative chat state and configuration to Svelte or SvelteKit apps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[urbantech](https://clawhub.ai/user/urbantech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill when adding AINative chat completions to Svelte or SvelteKit applications, including installation, store setup, message rendering, loading state, error state, and server-side API routing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may install and rely on a third-party npm package and the AINative service without validating that they trust those providers. <br>
Mitigation: Confirm trust in @ainative/svelte-sdk and AINative before installing or sending application traffic through the service. <br>
Risk: Secret API keys could be exposed if production credentials are placed in browser-bundled client code. <br>
Mitigation: Keep real secret keys server-side and use only scoped public keys in browser code. <br>
Risk: Chat messages may be sent to AINative as part of normal external API use. <br>
Mitigation: Make users aware that chat content may be sent to AINative and route sensitive production traffic through a controlled server-side endpoint. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/urbantech/ainative-svelte-sdk) <br>
- [AINative API base URL](https://api.ainative.studio) <br>
- [AINative chat completions endpoint](https://api.ainative.studio/v1/public/chat/completions) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration] <br>
**Output Format:** [Markdown with bash, TypeScript, and Svelte code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes client-side setup, Svelte store usage, server route guidance, exported types, and API key handling notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
