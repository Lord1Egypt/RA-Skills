## Description: <br>
AI-powered visual frontend editing in your browser. Click any element in your running app, describe changes in plain English, and get real source file edits with instant hot reload. Works with Next.js, Astro, and Vite. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bluehotdog](https://clawhub.ai/user/bluehotdog) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, designers, and product managers use this skill to set up and operate Frontman for browser-based edits to running Next.js, Astro, or Vite frontend apps. It supports click-to-target UI changes, source-file edits, and hot reload during development. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install Frontman packages and change project source files. <br>
Mitigation: Use it only in a version-controlled development project and review package, configuration, and source diffs before keeping changes. <br>
Risk: The workflow may involve OpenAI, Anthropic, or OpenRouter API keys. <br>
Mitigation: Store keys in environment variables or a secret manager, and avoid placing them in chat, source files, screenshots, or logs. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/bluehotdog/frontman-dev) <br>
- [Frontman GitHub repository](https://github.com/frontman-ai/frontman) <br>
- [Frontman documentation](https://frontman.sh/docs/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide installation of framework plugins and use browser tooling to apply source-file edits in a local development app.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
