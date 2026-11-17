## Description:

Uses workflows already configured in the JMCAI Comfypet desktop app to discover options, submit runs, and check results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[allen-jmc](https://clawhub.ai/user/allen-jmc)

### License/Terms of Use:

MIT-0

## Use Case:

External users of JMCAI Comfypet Desktop use this skill to discover and run configured ComfyUI workflows for image, video, audio, or file-based tasks, then retrieve generated outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A remote bridge may save files outside its download folder and contact unrelated network services.

Mitigation: Prefer the default local desktop connection. If remote access is essential, use a trusted endpoint, restrict filesystem and network permissions, and ensure downloads are confined to a private folder with URLs and redirects limited to that bridge.

Risk: Remote mode uploads selected input files and automatically saves results.

Mitigation: Use remote mode only with a trusted bridge and provide only intended input assets; limit filesystem and network permissions.

## Reference(s):

- [Publisher profile](https://clawhub.ai/user/allen-jmc)
- [JMCAI Comfypet skill release](https://clawhub.ai/allen-jmc/skills/comfypet-jmcai-skill)
- [JMCAI Comfypet skill pack](https://github.com/allen-Jmc/comfypet-jmcai-skill-pack)
- [JMCAI Comfypet desktop app](https://github.com/allen-Jmc/comfypet-jmcai-Dist)
- [Workflow usage examples](references/usage.md)
- [Workflow Bridge reference](references/bridge.md)

## Skill Output:

**Output Type(s):** [Files, JSON, Guidance]

**Output Format:** [Workflow status data and local paths to generated image, video, audio, or other files, with concise text guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated files and available modalities depend on the selected desktop workflow.]

## Skill Version(s):

1.2.6 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
