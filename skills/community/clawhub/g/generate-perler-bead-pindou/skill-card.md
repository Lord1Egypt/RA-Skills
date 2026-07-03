## Description: <br>
Generates 2D Perler Bead and Pindou pixel-art patterns from text prompts and reference image URLs, returning bead color codes and workspace links for pattern instructions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ai-hub-admin](https://clawhub.ai/user/ai-hub-admin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to call a hosted Craftsman Agent service that creates bead-board patterns from prompts or public image URLs for craft planning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, image URLs, and generated results are sent to a remote pattern-generation service. <br>
Mitigation: Use non-sensitive prompts and public image URLs only, and avoid submitting private designs or confidential source images. <br>
Risk: Generated share or workspace links may expose the result to anyone with the link. <br>
Mitigation: Treat returned links as shareable artifacts and review them before distributing or storing them in public logs. <br>
Risk: The helper scripts depend on API metadata and an access key to call the remote service. <br>
Mitigation: Provide DEEPNLP_ONEKEY_ROUTER_ACCESS only in trusted environments, rotate it if exposed, and verify the runtime endpoint before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ai-hub-admin/generate-perler-bead-pindou) <br>
- [Publisher profile](https://clawhub.ai/user/ai-hub-admin) <br>
- [Craftsman Perler Bead app](https://craftsman-agent.aiagenta2z.com/app/pindou_perler_bead) <br>
- [Craftsman gallery](https://craftsman-agent.aiagenta2z.com/gallery) <br>
- [DeepNLP Router access keys](https://www.deepnlp.org/workspace/keys) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON request and response examples plus JavaScript and Python command invocations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [API responses include palette data, grid cells, bead statistics, blueprint settings, and share or workspace URLs when returned by the remote service.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
