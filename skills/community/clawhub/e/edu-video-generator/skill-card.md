## Description:

Edu Video Generator helps agents generate educational and demo videos programmatically with Remotion, React layout components, TTS narration, subtitles, and visual composition guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linhongbijkm-dot](https://clawhub.ai/user/linhongbijkm-dot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content creators use this skill to create tutorial, explainer, and demo videos from scripted scene content, layout components, narration, subtitles, and rendering commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe code patterns or setup commands could affect the host project or local machine during use.

Mitigation: Review the skill before installation and run it only in an isolated project environment with pinned dependencies and lockfiles.

Risk: Browser security protections may be weakened by disableWebSecurity during rendering.

Mitigation: Remove disableWebSecurity unless there is a narrow, documented need for that render job.

Risk: Dynamic expression evaluation can execute more than intended.

Mitigation: Replace new Function usage with a strict arithmetic parser before using untrusted or user-supplied expressions.

Risk: Rendered SVG or troubleshooting commands can introduce content or operational risk.

Mitigation: Sanitize SVG before rendering and avoid broad kill or network commands unless the exact target has been verified.

## Reference(s):

- [Project initialization guide](artifact/references/setup.md)
- [Remotion component templates](artifact/references/templates.md)
- [Troubleshooting guide](artifact/references/troubleshooting.md)
- [Remotion documentation](https://www.remotion.dev/docs)
- [Lucide icon library](https://lucide.dev/icons)
- [edge-tts](https://github.com/rany2/edge-tts)
- [Noto fonts](https://fonts.google.com/noto)
- [KaTeX supported functions](https://katex.org/docs/supported.html)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline code blocks, JavaScript and TypeScript examples, shell commands, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide agents to produce Remotion video components, subtitle files, rendering scripts, and project configuration.]

## Skill Version(s):

4.7.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
