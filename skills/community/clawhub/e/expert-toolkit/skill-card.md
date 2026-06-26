## Description: <br>
Expert Toolkit helps Chinese-speaking users browse, search, match, and invoke local expert role prompts across 178+ specialist roles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[catkid010520](https://clawhub.ai/user/catkid010520) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Chinese-speaking developers and operators use this skill to find suitable expert roles, load role prompts, and get specialized guidance for product, engineering, marketing, finance, testing, and related tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local role markdown can influence model responses if the role pack is untrusted or the roles directory is set too broadly. <br>
Mitigation: Keep the roles directory limited to trusted role packs, avoid broad EXPERT_TOOLKIT_ROLES_ROOT values, and review third-party role files before relying on the output. <br>
Risk: Missing or damaged local role and mapping files can produce incomplete expert matches or fallback behavior. <br>
Mitigation: Verify the role pack and configuration JSON before deployment, then test category listing, search, direct invocation, and automatic matching in the target environment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/catkid010520/expert-toolkit) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown text with expert search/list results and loaded role prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns prompt content for selected or matched expert roles.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
