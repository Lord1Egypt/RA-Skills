## Description: <br>
Parses regular expressions and produces a visual structure plus a plain-English explanation of groups, quantifiers, anchors, and character classes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kofna3369](https://clawhub.ai/user/kofna3369) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to understand, document, or debug Python-style regular expressions by turning a pattern into tokens, a readable tree, and a concise explanation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Regex patterns entered as command-line arguments can appear in shell history or terminal output. <br>
Mitigation: Do not paste secrets, tokens, or sensitive production data into regex examples; use sanitized sample patterns. <br>
Risk: The visualizer supports Python re syntax and has documented limits around complex lookbehind, backreference visualization, and Unicode property visualization. <br>
Mitigation: Use it for explanation and documentation, and verify behavior separately with the target regex engine when using engine-specific features. <br>
Risk: The skill explains regex structure but is not intended to test whether a pattern matches a string. <br>
Mitigation: Use Python re.match or the relevant runtime matcher for match validation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kofna3369/axiom-regex-visualizer) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [README.md](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown with plain-text regex explanations, tree-style text output, Python snippets, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Pure Python standard-library helper; outputs are deterministic for the same regex input.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
