## Description: <br>
Routes face and character swap requests for still images and video through the RunComfy CLI, selecting among RunComfy model endpoints based on the user's intent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kalvinrv](https://clawhub.ai/user/kalvinrv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and creative operators use this skill to choose and invoke a RunComfy face-swap or character-swap route for still images, batch image edits, motion-preserving video, or audio-driven video. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Face-swap outputs can be harmful when used without consent or disclosure. <br>
Mitigation: Use only identities and media the operator has rights to use, refuse harmful real-person swaps, and confirm disclosure obligations before generation. <br>
Risk: RunComfy authentication tokens can grant access to the user's account. <br>
Mitigation: Install only the official RunComfy CLI, protect RUNCOMFY_TOKEN and ~/.config/runcomfy, and avoid exposing tokens in prompts, logs, or shared output. <br>
Risk: A model run may use the wrong inputs, route, or output directory for sensitive media. <br>
Mitigation: Confirm the selected route, input URLs, JSON body, and output directory before invoking runcomfy. <br>
Risk: Third-party reference media URLs are untrusted and may produce unexpected identity, motion, or content behavior. <br>
Mitigation: Use only user-provided URLs for the requested swap and inspect unexpected results before reuse or publication. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/kalvinrv/face-swap-runcomfy) <br>
- [RunComfy](https://www.runcomfy.com) <br>
- [RunComfy CLI documentation](https://docs.runcomfy.com/cli/introduction?utm_source=clawhub&utm_medium=skill&utm_campaign=face-swap-runcomfy) <br>
- [RunComfy character-swap feature](https://www.runcomfy.com/models/feature/character-swap?utm_source=clawhub&utm_medium=skill&utm_campaign=face-swap-runcomfy) <br>
- [Wan 2-2 Animate endpoint](https://www.runcomfy.com/models/community/wan-2-2-animate/api?utm_source=clawhub&utm_medium=skill&utm_campaign=face-swap-runcomfy) <br>
- [Kling motion-control endpoint](https://www.runcomfy.com/models/kling/kling-2-6/motion-control-pro?utm_source=clawhub&utm_medium=skill&utm_campaign=face-swap-runcomfy) <br>
- [GPT Image 2 Edit endpoint](https://www.runcomfy.com/models/openai/gpt-image-2/edit?utm_source=clawhub&utm_medium=skill&utm_campaign=face-swap-runcomfy) <br>
- [Nano Banana 2 Edit endpoint](https://www.runcomfy.com/models/google/nano-banana-2/edit?utm_source=clawhub&utm_medium=skill&utm_campaign=face-swap-runcomfy) <br>
- [FLUX Kontext collection](https://www.runcomfy.com/models/collections/flux-kontext?utm_source=clawhub&utm_medium=skill&utm_campaign=face-swap-runcomfy) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code] <br>
**Output Format:** [Markdown with inline bash and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the runcomfy CLI, a RUNCOMFY_TOKEN or authenticated RunComfy config, and user-provided media URLs.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
