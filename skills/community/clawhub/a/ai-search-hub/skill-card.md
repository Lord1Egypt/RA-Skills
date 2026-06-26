## Description: <br>
Run the AI Search Hub browser automation scripts for Yuanbao, LongCat, Doubao, Qwen, Gemini, and Grok, including Chrome DevTools setup, login detection, prompt submission, and result capture. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[peanuts62](https://clawhub.ai/user/peanuts62) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation users use this skill to send prompts to supported AI search and chat services through a standardized browser-driven runner, then collect answer text for agents, workflows, research pipelines, or monitoring systems. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can copy and reuse logged-in browser profile data in a persistent debug profile. <br>
Mitigation: Use a dedicated browser profile and dedicated service accounts, avoid sensitive prompts, and delete the copied debug profile after use. <br>
Risk: The skill drives a local Chromium-family browser through a Chrome DevTools endpoint. <br>
Mitigation: Keep DevTools bound to local access, review the scripts before installation, and run only in an environment where local browser automation is acceptable. <br>
Risk: Prompts and responses may pass through third-party AI services that require logged-in sessions. <br>
Mitigation: Avoid confidential or regulated data unless the selected service account and provider terms permit that use. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/peanuts62/ai-search-hub) <br>
- [README.en.md](artifact/README.en.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text answers and Markdown guidance, with optional answer files written by the bundled scripts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May launch or attach to a local Chromium-family browser through Chrome DevTools and may wait for manual login before producing output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
