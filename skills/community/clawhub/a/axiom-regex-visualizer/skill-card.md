## Description:

Regex visualizer that tokenizes Python-style regular expressions and produces a readable structure view with plain-English explanations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kofna3369](https://clawhub.ai/user/kofna3369)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical writers use this skill to inspect regular expressions, produce readable visual trees, and draft explanations for documentation or debugging. It is not a substitute for testing whether a pattern matches specific input.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Regex explanations may be incomplete for unsupported constructs, Perl/PCRE-only syntax, complex lookbehind, backreferences, or Unicode property visualization.

Mitigation: Use the output as documentation aid, and verify match behavior with the target regex engine and representative test cases.

Risk: Release evidence and artifact documentation contain inconsistent license and version-adjacent signals.

Mitigation: Confirm the authoritative release metadata before publication or redistribution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kofna3369/skills/axiom-regex-visualizer)
- [Skill instructions](artifact/SKILL.md)
- [README](artifact/README.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Plain text or Markdown with optional inline shell and Python snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces deterministic local regex tokenization, visual tree text, and plain-English explanations; no network use is indicated by the security evidence.]

## Skill Version(s):

0.1.2 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
