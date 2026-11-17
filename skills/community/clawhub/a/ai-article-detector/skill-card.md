## Description:

AI Article Detector analyzes article links and scores AI writing probability from 0 to 100.

This skill is ready for commercial/non-commercial use.

## Publisher:

[evan-y25](https://clawhub.ai/user/evan-y25)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, editors, and content reviewers use this skill to fetch a web article and estimate whether it appears AI-generated using an eight-dimension statistical scoring report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fetch arbitrary user-supplied URLs, which may expose internal network resources or exhaust local resources.

Mitigation: Run it in a sandbox without internal network access and avoid untrusted links until URL allowlisting, private-IP blocking, redirect validation, request timeouts, response-size limits, and pinned dependencies are added.

Risk: The AI-writing score is a heuristic and may be unreliable, especially outside Chinese-language content.

Mitigation: Use the score as a review signal rather than a final decision, and pair it with human review for moderation, originality, or quality workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/evan-y25/skills/ai-article-detector)
- [Publisher profile](https://clawhub.ai/user/evan-y25)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [CLI text report and JavaScript result object with AI probability, per-dimension scores, weights, and interpretation.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The score is a heuristic estimate optimized for Chinese-language content and should be paired with human review.]

## Skill Version(s):

1.0.0 (source: package.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
