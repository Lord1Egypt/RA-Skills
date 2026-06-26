## Description: <br>
Verifies factual claims from text or URLs, traces claims to original or official sources, and returns structured credibility reports with authoritative links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alondotsh](https://clawhub.ai/user/alondotsh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and analysts use this skill to verify factual claims from text or URLs, classify them as true, misleading, false, or unverified, and trace claims to authoritative source URLs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Private text or authenticated/internal URLs may be exposed if the host agent browses or searches them externally. <br>
Mitigation: Use the skill for public or non-sensitive fact-checking, and avoid submitting confidential material unless external browsing is acceptable. <br>
Risk: A claim may remain unresolved when sources are inaccessible, ambiguous, or only weak secondary mentions are found. <br>
Mitigation: Use the skill's unverified verdicts, trace confidence, and notes to preserve uncertainty instead of forcing a conclusion. <br>
Risk: High-stakes factual checks can be mistaken for personalized medical, legal, financial, or safety advice. <br>
Mitigation: Treat outputs as evidence summaries about claims, not personalized advice, and rely on qualified professionals for decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/alondotsh/alon-fact-check) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/alondotsh) <br>
- [Artifact README](artifact/README.md) <br>
- [Runtime skill instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown fact-check report or source trace with links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include source summaries, verdicts, credibility scores, source links, trace confidence, and notes on missing or ambiguous evidence.] <br>

## Skill Version(s): <br>
0.1.2 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
