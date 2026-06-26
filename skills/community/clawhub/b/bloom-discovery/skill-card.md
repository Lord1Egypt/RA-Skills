## Description: <br>
Bloom Discovery analyzes local OpenClaw context to generate a MentalOS profile, match use cases and skills, verify configuration, and support SBT claims with opt-in usage metrics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bloomprotocol](https://clawhub.ai/user/bloomprotocol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and developers use this skill to turn local conversation history, USER.md context, and installed-skill information into a builder profile, personalized use case matches, configuration checks, and proof-claiming guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads recent OpenClaw session history and USER.md, which can include sensitive personal or work context. <br>
Mitigation: Install only when this local access is acceptable, review the bundled session reader and wrapper behavior, and run it in a workspace whose session history is appropriate for profiling. <br>
Risk: The skill sends derived profile and recommendation data to Bloom's API after local analysis. <br>
Mitigation: Review the security guidance and privacy wording before use, and confirm that opt-in controls and transmitted fields match the user's expectations. <br>
Risk: The scanner summary calls out under-disclosed or broad network, install, and credential-adjacent behavior. <br>
Mitigation: Review the npm install path, wrapper, token/admin/test scripts, and prefer a pinned bundled release before deployment. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/bloomprotocol/bloom-discovery) <br>
- [Bloom Protocol publisher profile](https://clawhub.ai/user/bloomprotocol) <br>
- [Bloom Protocol homepage](https://bloomprotocol.ai) <br>
- [Architecture Diagram: Conversation-Driven Recommendations](docs/ARCHITECTURE-DIAGRAM.md) <br>
- [Skills Pipeline - Agent Instructions](docs/agent-skills-pipeline-instructions.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown or text response with profile details, use case matches, verification status, recommendations, and a dashboard URL.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May also write local discovery or identity state files when invoked by the skill runtime.] <br>

## Skill Version(s): <br>
4.0.2 (source: server release metadata; artifact frontmatter and package.json report 4.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
