## Description: <br>
Automatically selects the best model based on task type and requirements for coding, analysis, multimodal, writing, research, long-context, and cost-performance-sensitive tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mrcuo](https://clawhub.ai/user/mrcuo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to route tasks to available provider models based on task type, context length, multimodal needs, reasoning complexity, and cost-performance tradeoffs. It supports manual model overrides when a user specifies a preferred model. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic routing may send prompts to configured provider models and create routing metrics logs. <br>
Mitigation: For sensitive, regulated, or cost-sensitive work, specify the model/provider explicitly and avoid including sensitive details that could be captured in routing metrics. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mrcuo/auto-model-switcher) <br>
- [Project Homepage](https://github.com/mrcuo/auto-model-switcher) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration instructions] <br>
**Output Format:** [Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Recommends provider model selections and fallback behavior; does not produce standalone files or executable code.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
