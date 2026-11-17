## Description: <br>
Ai Writing Style Cloner helps agents analyze writing samples, extract reusable style fingerprints, and generate new content in a similar style using structured writing formulas. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, marketing teams, and automation builders can use this skill to distill an author's style from permitted writing samples, save a structured style fingerprint, and draft new Chinese-language marketing copy, articles, titles, or product content in that style. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Author style profiles may be created or reused without clear consent, rights, or retention boundaries. <br>
Mitigation: Use only writing samples the user has the right to analyze, document the permitted purpose, and delete profiles when they are no longer needed. <br>
Risk: Saved style fingerprints may expose personal, proprietary, or brand-sensitive writing patterns. <br>
Mitigation: Keep style_fingerprints private, restrict access to authorized users, and avoid storing sensitive source material in reusable profiles. <br>
Risk: The skill requests broad command and file access to read, write, and reuse style profiles. <br>
Mitigation: Run it in a restricted environment or replace command execution with safer file APIs before operational use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/ai-writing-style-cloner) <br>
- [Skill source artifact](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Files, Guidance] <br>
**Output Format:** [Markdown and JSON responses, including style fingerprint JSON, generated drafts, and saved profile records.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May persist reusable style fingerprints per author_id when file access is available.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release; artifact frontmatter says 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
