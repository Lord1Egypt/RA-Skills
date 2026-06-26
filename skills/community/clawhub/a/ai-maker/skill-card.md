## Description: <br>
Ai Maker routes ecommerce creative briefs to Jimeng or LiblibAI image-generation workflows and records candidate results and generation parameters. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[duzhihai123](https://clawhub.ai/user/duzhihai123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and ecommerce creative teams can use this skill to turn Chinese-language creative briefs into structured image-generation requests, candidate output records, and reproducible parameter notes. It is best treated as a scaffold until provider calls and output-file verification are implemented. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can report successful image generation while returning placeholder paths instead of provider-created files. <br>
Mitigation: Confirm real Jimeng or LiblibAI provider calls are implemented and verify output files exist before relying on generated results. <br>
Risk: Prompt excerpts and generation details may be appended to local history. <br>
Mitigation: Avoid including sensitive product or campaign details in prompts unless local history storage is acceptable. <br>


## Reference(s): <br>
- [ClawHub Ai Maker release page](https://clawhub.ai/duzhihai123/ai-maker) <br>
- [Jimeng](https://jimeng.jianying.com/) <br>
- [LiblibAI](https://www.liblib.art/) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, configuration, guidance] <br>
**Output Format:** [JSON generation result records with image paths, tool names, model parameters, and status messages.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Configured for 1-4 candidate image records; video generation is reserved and disabled.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
