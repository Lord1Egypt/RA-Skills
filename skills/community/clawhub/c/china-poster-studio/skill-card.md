## Description: <br>
China Poster Studio helps an agent turn pasted Chinese text, short prompts, or optional URLs into social-media poster content and local PNG generation guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tobewin](https://clawhub.ai/user/tobewin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, operators, creators, and social-media publishers use this skill to convert articles, notes, recommendations, and short ideas into poster-ready layouts for WeChat Moments, Xiaohongshu, Douyin, and similar channels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional URL fetching can expose private, intranet, authenticated, or token-bearing URLs. <br>
Mitigation: Paste article text directly when privacy matters and avoid providing private or credential-bearing URLs. <br>
Risk: Local poster generation depends on user-installed Pillow and fonts. <br>
Mitigation: Install Pillow and fonts only from trusted sources and review any generated local-generation steps before execution. <br>
Risk: Automatic title, key-point, and quote extraction can produce inaccurate or misleading poster text. <br>
Mitigation: Review the generated poster copy before publishing or sharing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tobewin/china-poster-studio) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with optional Python/Pillow implementation guidance for PNG poster generation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can include generated poster copy, layout choices, source attribution text, platform dimensions, and local font or Pillow setup guidance.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata, created 2026-04-29; artifact frontmatter reports 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
