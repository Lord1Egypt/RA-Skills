## Description: <br>
Crazyrouter Video Gen generates text-to-video outputs through the Crazyrouter API, with support for Sora 2, Kling V2, Veo 3, Seedance, Pika, MiniMax Hailuo, and Runway models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xujfcn](https://clawhub.ai/user/xujfcn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agents use this skill to create short videos from text prompts by calling Crazyrouter-backed video generation models and saving returned video files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and any included context are sent to Crazyrouter and potentially to downstream model providers. <br>
Mitigation: Avoid sending secrets or private data unless Crazyrouter's terms and the user's data-handling requirements allow it. <br>
Risk: Video generation can incur third-party API usage costs. <br>
Mitigation: Confirm the API key, account, model choice, and expected usage before running generation. <br>
Risk: Generated video content is downloaded from a returned URL and written to a user-specified output path. <br>
Mitigation: Use an intended output path and review generated media before sharing or relying on it. <br>


## Reference(s): <br>
- [Crazyrouter](https://crazyrouter.com) <br>
- [Crazyrouter API base URL](https://crazyrouter.com/v1) <br>
- [ClawHub skill page](https://clawhub.ai/xujfcn/crazyrouter-video-gen) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Text, Shell commands, Configuration guidance] <br>
**Output Format:** [Video files with CLI status text and setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CRAZYROUTER_API_KEY; sends prompts to Crazyrouter and may incur API usage costs.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
