## Description: <br>
AI Fact Checker helps agents extract factual claims from text, search the web for corroborating evidence, score confidence, and produce a correction-oriented fact-check report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rudagebil11-jpg](https://clawhub.ai/user/rudagebil11-jpg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to check AI-generated or user-provided text for factual claims, compare those claims against web search results, and receive a concise confidence-scored Markdown report with suggested corrections. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Text submitted for checking is sent to web search, which can expose secrets, private documents, personal data, or proprietary content. <br>
Mitigation: Use the skill only on content that is acceptable to share with search providers, and add explicit user notice and consent before running checks on sensitive text. <br>
Risk: The current implementation invokes a shell command using user-provided claim text, which creates command-injection risk for crafted input. <br>
Mitigation: Replace shell-string execution with a structured API call or execFile-style invocation before running the skill on untrusted text. <br>
Risk: Fact-check scores are based on keyword overlap against search snippets and can miss nuance, stale sources, or contradictory evidence. <br>
Mitigation: Treat the Markdown report as review guidance and manually verify high-impact claims against authoritative sources. <br>


## Reference(s): <br>
- [Ai Fact Checker ClawHub release](https://clawhub.ai/rudagebil11-jpg/ai-fact-checker) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown fact-check report with confidence scores, verdicts, source links, and suggested corrections.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses web search results as evidence and returns concise claim-level and overall assessments.] <br>

## Skill Version(s): <br>
1.1.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
