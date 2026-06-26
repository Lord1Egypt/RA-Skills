## Description: <br>
AI Article Detector analyzes article links and scores the probability that the writing is AI-generated on a 0-100 scale. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Evan-y25](https://clawhub.ai/user/Evan-y25) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, content reviewers, and editors can use this skill to fetch a public article URL and receive a local heuristic estimate of AI-written style. It is best used for triage, content review, or originality checks alongside human judgment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The AI-writing probability score is a rough heuristic and can be wrong, especially for advanced AI-generated text or content outside the optimized language profile. <br>
Mitigation: Use the score as an advisory signal only, pair it with human review, and avoid treating it as proof for legal, disciplinary, or automated enforcement decisions. <br>
Risk: The tool fetches user-provided article URLs and depends on npm packages to parse remote pages. <br>
Mitigation: Install dependencies only from trusted registries, evaluate public URLs you intend to fetch, and run the tool in an environment appropriate for outbound web requests. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Evan-y25/ai-article-detector) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, code, guidance] <br>
**Output Format:** [Command-line text report and JavaScript object output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports a 0-100 AI-writing probability with per-feature scores for eight statistical dimensions.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
