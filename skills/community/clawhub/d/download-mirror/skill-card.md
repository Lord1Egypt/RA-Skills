## Description: <br>
Helps agents diagnose slow or failed HuggingFace and GitHub downloads, then propose mirror-based download commands, helper scripts, and verification steps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yazuibi](https://clawhub.ai/user/yazuibi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill when model, dataset, or repository downloads from HuggingFace or GitHub are slow, timing out, or inaccessible. It guides connectivity checks, mirror selection, mirrored download commands, and post-download validation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Downloads and possible HuggingFace tokens may be routed through third-party mirrors. <br>
Mitigation: Use third-party mirrors only for public artifacts, avoid sending private tokens through mirrored endpoints, and prefer direct sources for private or gated content. <br>
Risk: The helper can install Python packages at runtime. <br>
Mitigation: Run the helper in an isolated environment and review package installation commands before execution. <br>
Risk: Mirrored artifacts can differ from the original source or be incomplete. <br>
Mitigation: Verify checksums or signatures when available and perform the bundled post-download validation checks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yazuibi/download-mirror) <br>
- [ModelScope ID mapping reference](references/modelscope_id_map.md) <br>
- [ModelScope model search](https://modelscope.cn/models) <br>
- [hf-mirror endpoint](https://hf-mirror.com) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May recommend third-party mirror endpoints, Python package installation, environment variables, and local download verification steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
