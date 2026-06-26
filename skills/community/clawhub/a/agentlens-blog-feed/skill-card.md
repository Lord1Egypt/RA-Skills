## Description: <br>
Use this skill when a user, prompt, or another skill needs newly published AgentLens blogs that have not already been surfaced. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[archlab-space](https://clawhub.ai/user/archlab-space) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content workflow authors use this skill to ingest public AgentLens blog posts once, then pass the returned body and source link to a caller for summarization, drafting, translation, saving, or other downstream handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts the public AgentLens API and returns public blog content that another caller may consume, transform, or publish. <br>
Mitigation: Review any separate caller skill or prompt that summarizes, saves, translates, or publishes the returned content. <br>
Risk: The skill maintains a local deduplication file to remember processed blog IDs. <br>
Mitigation: Choose a MEMORY_PATH the user is comfortable with and commit entries only after the caller confirms successful consumption. <br>


## Reference(s): <br>
- [AgentLens Blog Feed on ClawHub](https://clawhub.ai/archlab-space/agentlens-blog-feed) <br>
- [AgentLens public blog API](https://agentlens-core.archlab.workers.dev) <br>
- [Open Skill Hub issues](https://github.com/archlab-space/open-skill-hub/issues) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown and structured blog fields returned to the caller, including id, title, summary, body_markdown, source_link, occurred_at, and generated_at.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a caller-selected MEMORY_PATH, defaulting to ~/agentlens-processed-blogs.json, to track consumed blog IDs after confirmation.] <br>

## Skill Version(s): <br>
0.8.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
