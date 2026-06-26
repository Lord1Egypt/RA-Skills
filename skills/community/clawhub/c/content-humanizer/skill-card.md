## Description: <br>
Content Humanizer helps agents audit AI-sounding marketing copy, rewrite it with more natural rhythm and specificity, and adapt it to a brand voice. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[paudyyin](https://clawhub.ai/user/paudyyin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing and content teams use this skill to turn robotic or generic drafts into more credible human-facing copy. It supports AI-pattern audits, full rewrites, voice injection, before-and-after comparisons, and heuristic humanity scoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The humanity score is a heuristic and should not be treated as definitive authorship detection. <br>
Mitigation: Use the score as an editing signal only, and rely on human review before making authorship, quality, or publication decisions. <br>
Risk: Brand voice context or pasted drafts may contain sensitive marketing details. <br>
Mitigation: Provide only the context needed for the edit and review rewritten or annotated output before sharing it outside the intended audience. <br>
Risk: Humanizing a draft can change factual claims, tone, or useful original passages. <br>
Mitigation: Review the final copy against source material, preserve strong original sections when flagged, and provide evidence for specific claims rather than inventing proof. <br>


## Reference(s): <br>
- [Content Humanizer on ClawHub](https://clawhub.ai/paudyyin/content-humanizer) <br>
- [AI Tells Checklist](references/ai-tells-checklist.md) <br>
- [Voice Techniques Reference](references/voice-techniques.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with rewritten copy, annotated findings, comparisons, and optional local scoring output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May ask for brand voice context or read marketing-context.md when present; the local scorer reports a 0-100 heuristic humanity score with signal breakdowns.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, package.json, and SKILL.md metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
