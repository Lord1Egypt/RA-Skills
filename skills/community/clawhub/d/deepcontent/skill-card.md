## Description: <br>
DeepContent provides recipe lookup, content generation, and asset management for branded social media content such as event posters, speaker cards, partnership posts, and templates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thierrypdamiba](https://clawhub.ai/user/thierrypdamiba) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing and content teams use this skill to list DeepContent recipes and generate branded social posts, event posters, speaker announcements, and partnership announcement copy from provided or discovered assets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Public web searches for logos, headshots, and templates can return inaccurate, untrusted, or rights-restricted assets. <br>
Mitigation: Prefer authorized image and logo URLs, and review identity accuracy, source trust, and reuse rights before publishing generated content. <br>
Risk: Image recipes rely on publicly accessible asset URLs and may take several minutes or time out. <br>
Mitigation: Warn users before image generation, retry once on timeout, and offer caption-only output or a different template URL if generation continues to fail. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Image URLs, Guidance] <br>
**Output Format:** [Markdown containing generated text, captions, and inline image links from DeepContent tool responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Image recipes may take 2-3 minutes and return recipe_id, status, generation_id, and content blocks.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
