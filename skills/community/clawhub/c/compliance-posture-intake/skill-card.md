## Description: <br>
Comprehensive HIPAA compliance posture assessment for agent and API contexts that guides a structured intake, analyzes provided compliance documents, and produces a posture snapshot with maturity stage, enterprise blocker flags, prioritized gaps, and a 30/60/90 day roadmap. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dangsllc](https://clawhub.ai/user/dangsllc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Compliance, security, and healthcare operations teams use this skill to conduct a conversational HIPAA posture intake, review supplied policies or agreements, and turn the results into a practical remediation roadmap. It is intended for agent contexts that can ask structured questions, read user-provided documents, and optionally use web search for state-law considerations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may read compliance documents supplied by the user. <br>
Mitigation: Provide only documents and details appropriate for the agent context, and avoid organization names, customer names, PHI, secrets, or other sensitive specifics unless the user is comfortable sharing them. <br>
Risk: Optional state-law research may send user-provided state and generalized business context to web search. <br>
Mitigation: Use generalized business descriptions for searches, omit sensitive identifiers, or ask the agent to skip web research when a local-only review is required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dangsllc/compliance-posture-intake) <br>
- [Rote Compliance](https://rotecompliance.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, files] <br>
**Output Format:** [Conversational intake followed by a structured compliance posture report, with optional Word document output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include maturity stage, enterprise blocker flags, gap prioritization, document-analysis findings, state-law considerations, and a 30/60/90 day roadmap.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
