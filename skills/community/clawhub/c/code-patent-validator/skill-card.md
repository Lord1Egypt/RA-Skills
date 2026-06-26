## Description: <br>
Turn your code scan findings into search queries so users can research existing implementations before consulting an attorney. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leegitw](https://clawhub.ai/user/leegitw) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering teams use this skill to convert code patent scanner findings into structured search strategies, evidence maps, and differentiation questions for self-directed research. It supports preparation for attorney review but does not provide legal conclusions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may mistake generated research strategies for legal advice or patentability conclusions. <br>
Mitigation: Present outputs as search planning guidance only and direct users to consult a qualified patent attorney for legal conclusions or filing decisions. <br>
Risk: Users may include confidential invention details in the agent context while asking for search planning. <br>
Mitigation: Avoid sharing sensitive invention details unless the user is comfortable placing them in the agent context. <br>
Risk: Generated search queries and evidence checklists may be incomplete or misleading if used without review. <br>
Mitigation: Review generated strategies before use, run searches manually across the recommended sources, and document findings systematically. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/leegitw/code-patent-validator) <br>
- [Skill homepage](https://github.com/Obviously-Not/patent-skills/tree/main/code-patent-validator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, guidance] <br>
**Output Format:** [Markdown guidance and structured JSON search strategy examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces search queries, source-priority guidance, analysis questions, evidence checklists, and required disclaimers; it does not perform searches or assess patentability.] <br>

## Skill Version(s): <br>
1.4.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
