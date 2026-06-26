## Description: <br>
Clawy helps agents generate stable mascot avatars and short image-driven adventure arcs using configured external image-edit providers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Ocean7322](https://clawhub.ai/user/Ocean7322) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents, developers, and external users use Clawy to create or refine a stable mascot identity, preserve that identity across themed scene images, and run short interactive story posts with captions and choices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected reference images and prompts are sent to the configured external image provider during generation. <br>
Mitigation: Use a trusted provider, prefer a dedicated API key, and avoid sensitive reference images or prompt content. <br>
Risk: Custom base URL overrides can redirect provider traffic to an unintended endpoint. <br>
Mitigation: Leave base URL overrides unset unless the endpoint is explicitly trusted and reviewed. <br>
Risk: If the bundled mother image is missing, the helper may download and write the fallback image locally. <br>
Mitigation: Review the fallback image source and local write behavior before running the helper in restricted environments. <br>


## Reference(s): <br>
- [Clawy Release Page](https://clawhub.ai/Ocean7322/clawy) <br>
- [Asset Rules](references/asset-rules.md) <br>
- [Image Edit Playbook](references/image-edit-playbook.md) <br>
- [Fallback Mother Image](https://www.8uddy.land/images/clawy.png) <br>


## Skill Output: <br>
**Output Type(s):** [Images, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Generated images with short Markdown captions, choice blocks, and optional shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires one supported image-edit provider credential when generation is invoked.] <br>

## Skill Version(s): <br>
0.2.9 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
