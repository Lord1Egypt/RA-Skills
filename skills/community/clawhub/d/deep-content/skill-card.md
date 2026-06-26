## Description: <br>
DeepContent provides recipe lookup, branded content generation, and asset management for social media posts, event posters, speaker cards, partnership posts, and reusable content templates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scale-intelligence](https://clawhub.ai/user/scale-intelligence) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content teams and external users use this skill to discover DeepContent recipes, generate branded social media assets, run user-created recipes, and manage recipe remixes through the DeepContent MCP server. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: DeepContent may receive and persistently store images uploaded for generation. <br>
Mitigation: Avoid sending private or sensitive images unless DeepContent retention and deletion controls are understood and acceptable. <br>
Risk: Recipe remixing or copying can save cloned recipe objects. <br>
Mitigation: Confirm the user intends to create a saved recipe clone before using remix or copy workflows. <br>
Risk: The security evidence flags under-scoped persistent uploads and a confusing recipe creation/remix mutation path. <br>
Mitigation: Review generated actions before deployment and keep recipe creation routed through the DeepContent UI as instructed by the artifact. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/scale-intelligence/deep-content) <br>
- [DeepContent Recipes UI](https://deepcontent-pair.vercel.app/recipes) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown responses with generated captions, image links, generation page URLs, and concise operating guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include generated image URLs, recipe IDs, generation IDs, and site URLs returned by DeepContent tools.] <br>

## Skill Version(s): <br>
1.3.6 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
