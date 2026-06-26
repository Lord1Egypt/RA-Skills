## Description: <br>
无所不能 — Universal prompt compression protocol that translates natural language into compressed I-Lang syntax for token-saving, text-to-text prompt compression without file, URL, command, credential, or external-resource access. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adsorgcn](https://clawhub.ai/user/adsorgcn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to convert natural-language prompts into compact I-Lang instructions for use in AI assistants while preserving the requested meaning and response shape. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may rely on compressed prompts without reviewing whether meaning and constraints were preserved. <br>
Mitigation: Review the generated I-Lang instruction and its explanation before reusing it in another AI assistant. <br>
Risk: The skill is intended for prompt-compression workflows only and may be misapplied to unrelated tasks. <br>
Mitigation: Use it only for natural-language-to-I-Lang text translation, consistent with the artifact behavior and security guidance. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/adsorgcn/everything-is-ok) <br>
- [I-Lang website](https://ilang.ai) <br>
- [I-Lang dictionary](https://github.com/ilang-ai/ilang-dict) <br>
- [I-Lang research](https://research.ilang.ai) <br>
- [AI See](https://i.ilang.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown text with compressed I-Lang syntax followed by a brief explanation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Text-to-text translator only; does not access files, fetch URLs, execute commands, or perform external actions.] <br>

## Skill Version(s): <br>
1.0.4 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
