## Description: <br>
Predicts which ad hook, email subject, or social post is likely to perform best for a target ICP, including confidence intervals, rewrite suggestions, cross-ICP scoring, and quality gates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[drivenautoplex1](https://clawhub.ai/user/drivenautoplex1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External marketers, copywriters, sales teams, and content operators use this skill to rank campaign hooks, diagnose weak variants, and generate targeted rewrite guidance before spending budget on live tests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically execute a neighboring content_resonance_scorer/content_resonance_scorer.py file when that file exists. <br>
Mitigation: Review that neighboring file before installation or run the skill in an isolated directory where only reviewed dependencies are present. <br>
Risk: The scoring output is predictive marketing guidance and may not match real campaign performance. <br>
Mitigation: Use the output for pre-test triage and confirm important decisions with live A/B testing, especially when the winner margin is small. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/drivenautoplex1/ab-predictor) <br>
- [OpenClaw Metadata Homepage](https://github.com/drivenautoplex1/openclaw-skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, guidance] <br>
**Output Format:** [CLI text or JSON with ranked scores, confidence intervals, coaching flags, cross-ICP scores, quality gate status, and rewrite suggestions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3; can score direct text input or a JSON file of labeled variants.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
