## Description:

Generate vertical short videos of gardening and plant growth with WeryAI, including seed germination, blooms, fruiting plants, succulents, mushrooms, and time-lapse growth stories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zoucdr](https://clawhub.ai/user/zoucdr)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn short gardening or plant-growth briefs into confirmed WeryAI video generation requests and playable video URLs. It is suited for vertical social clips, time-lapse plant growth scenes, and image-to-video plant transformations when inputs use public HTTPS image URLs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Use of a paid WeryAI API key can spend credits when generation is confirmed and submitted.

Mitigation: Confirm model, duration, aspect ratio, prompt, and image inputs before running generation, and use dry-run/status checks where appropriate.

Risk: Environment URL overrides could route prompts, image URLs, and bearer tokens to an unintended endpoint if misconfigured.

Mitigation: Review WERYAI_BASE_URL and WERYAI_MODELS_BASE_URL before use and keep them unset unless an approved endpoint is required.

Risk: Image-to-video inputs do not accept local files and require public HTTPS URLs.

Mitigation: Provide only trusted public HTTPS image URLs and avoid local paths or private images that should not be sent to the service.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zoucdr/skills/garden-grow-video)
- [WeryAI API Endpoint](https://api.weryai.com)
- [WeryAI Models Endpoint](https://api-growth-agent.weryai.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, API calls]

**Output Format:** [Markdown guidance with JSON CLI parameters and returned video URL data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 18+, WERYAI_API_KEY, network access, and public HTTPS image URLs for image inputs. Successful wait runs may consume WeryAI credits.]

## Skill Version(s):

0.1.3 (source: server release evidence; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
