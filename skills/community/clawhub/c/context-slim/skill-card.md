## Description: <br>
See exactly what's eating your context window. Analyzes prompts, conversations, and system instructions to show where every token goes. Actionable compression suggestions. All local. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TheShadowRose](https://clawhub.ai/user/TheShadowRose) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, prompt engineers, and agent builders use Context Slim to profile token usage in prompts, conversations, and system instructions, identify truncation risk, and review compression opportunities before deployment or reuse. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated HTML reports can render untrusted conversation labels as HTML or script. <br>
Mitigation: Use trusted input files for HTML report generation, treat generated reports as sensitive local files, and prefer text or JSON output for untrusted conversation exports until report labels are escaped. <br>
Risk: Token counts are heuristic estimates and may be inaccurate for exact billing, hard context-limit enforcement, non-English text, code-heavy content, or multimodal inputs. <br>
Mitigation: Use Context Slim for profiling and planning, then validate critical counts with the target provider's tokenizer and keep a buffer for context-limit decisions. <br>


## Reference(s): <br>
- [Context Slim ClawHub listing](https://clawhub.ai/TheShadowRose/context-slim) <br>
- [TheShadowRose ClawHub profile](https://clawhub.ai/user/TheShadowRose) <br>
- [README](artifact/README.md) <br>
- [Limitations](artifact/LIMITATIONS.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and text guidance with inline shell commands, Python examples, JSON snippets, and optional local HTML or JSON report files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs locally with Python standard library only; token counts are estimates and should be validated with provider tokenizers for exact billing or hard limit decisions.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
