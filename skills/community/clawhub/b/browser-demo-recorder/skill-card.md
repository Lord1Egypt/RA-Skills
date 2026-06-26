## Description: <br>
Records browser demo videos from a plain-language brief by planning the flow, driving the OpenClaw browser, encoding an MP4, and returning the media file. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smile618](https://clawhub.ai/user/smile618) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, product teams, and content creators use this skill to create browser walkthroughs, product demos, landing-page captures, and search or click-flow recordings from a short brief. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recording plans can control an active browser, including navigation, clicks, typing, scrolling, and page-side evaluation. <br>
Mitigation: Review generated plans before running them, use public or throwaway demo pages, and avoid evaluate steps unless the code is trusted. <br>
Risk: Recordings and debug files can save sensitive browsing details to disk. <br>
Mitigation: Do not type secrets during recordings, prefer a clean browser profile, keep the output directory under workspace media, and delete debug JSON files when finished. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/smile618/browser-demo-recorder) <br>
- [Plan Schema](references/plan-schema.md) <br>
- [Example Recording Plan](references/example-skills-video-plan.json) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, shell commands, files] <br>
**Output Format:** [Markdown status with a MEDIA line, plus generated MP4 and debug JSON files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes outputs to the workspace media directory unless the user requests a different safe location.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
