## Description: <br>
Screens and evaluates Instagram, TikTok, and YouTube creators using configurable quality frameworks, Memories.ai video metadata and MAI analysis, and report-ready scoring criteria. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shawnshenopeninterx](https://clawhub.ai/user/shawnshenopeninterx) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Marketing, partnership, and creator operations teams use this skill to vet social media creators for brand fit, production quality, delivery, and engagement signals. Agents can run the helper scripts to fetch creator metadata, analyze videos, score creators, and produce screening reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The CAC Crusher framework can unfairly affect creator approval decisions through rural/class-coded and subjective appearance-based rejection rules. <br>
Mitigation: Revise the rubric to remove those criteria before real creator selection, and require human review for borderline or rejected creators. <br>
Risk: Using the skill sends creator URLs, usernames, and related public social-media metadata to Memories.ai and possibly Apify through the user's API keys. <br>
Mitigation: Use only authorized public data, keep API keys in environment variables, and confirm that external API processing is allowed for the intended workflow. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/shawnshenopeninterx/creator-screening) <br>
- [CAC Crusher Creator Screening Framework](references/frameworks/cac-crusher.md) <br>
- [Default Creator Screening Framework](references/frameworks/default.md) <br>
- [Custom Framework Template](references/frameworks/template.md) <br>
- [Memories.ai API Tools](https://api-tools.memories.ai) <br>
- [Memories.ai V2 API Base](https://mavi-backend.memories.ai/serve/api/v2) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown screening cards, JSON scoring output, and shell command guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports include profile stats, per-section PASS/FAIL/FLAG scores, transcript excerpts, visual quality notes, and APPROVED, REJECTED, or CONDITIONAL verdicts.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
