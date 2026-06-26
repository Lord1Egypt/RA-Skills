## Description: <br>
Generate ai background remover images with AI via the Neta AI image generation API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[barbaraledbettergq](https://clawhub.ai/user/barbaraledbettergq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to generate background-removal style images from text prompts, optionally with size selection or an existing picture UUID as reference input. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends prompts, picture UUIDs, generated image metadata, and the API token to the Neta/TalesofAI service. <br>
Mitigation: Use a revocable token, review the external service terms, and avoid submitting sensitive prompts or image references. <br>
Risk: Passing the token inline can expose it through shell history or process listings on shared systems. <br>
Mitigation: Prefer the NETA_TOKEN environment variable or another local secret-handling mechanism, and rotate the token if exposure is suspected. <br>
Risk: The artifact includes broader character and style generation behavior in bgremove.js beyond the primary background-removal entry point. <br>
Mitigation: Review bgremove.js before use and run only the intended command with trusted prompt and image-reference inputs. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/barbaraledbettergq/background-remover-claw-skill) <br>
- [Neta API token access](https://www.neta.art/open/) <br>
- [TalesofAI API endpoint](https://api.talesofai.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Command-line guidance and stdout text containing generated image URLs or JSON task results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Neta API token and may send prompts, picture UUIDs, generated image metadata, and the API token to the Neta/TalesofAI service.] <br>

## Skill Version(s): <br>
1.7.0 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
