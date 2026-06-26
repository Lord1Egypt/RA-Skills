## Description: <br>
Capture, store, and retrieve errors, corrections, and best practices locally to continuously improve AI agent workflows and knowledge. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vedantsingh60](https://clawhub.ai/user/vedantsingh60) <br>

### License/Terms of Use: <br>
MIT License <br>


## Use Case: <br>
Developers and AI-agent users use this skill to record errors, corrections, successful patterns, and best practices locally, then search or summarize them before similar tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local memory files may persist project details, credentials, private customer data, or raw production logs if a user records them. <br>
Mitigation: Do not record secrets or sensitive data, and periodically review the local learning files for content that should be removed. <br>
Risk: Exported JSON may disclose recorded notes or be written to an unintended path. <br>
Mitigation: Choose export paths deliberately and review exported JSON before sharing it. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/vedantsingh60/adaptive-learning-agents) <br>
- [Skill documentation](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, JSON, Guidance] <br>
**Output Format:** [Python objects, local JSON files, and human-readable text or Markdown summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores user-provided learnings and errors locally by default and can export them as JSON.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata, manifest.yaml, SKILL.md changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
