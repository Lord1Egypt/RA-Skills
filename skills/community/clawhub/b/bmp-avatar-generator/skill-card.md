## Description: <br>
Generates deterministic pixel-art avatar SVG files from seed strings using the pinned @bitmappunks/avatar-generator@0.0.5 npm package through npx. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tt-u](https://clawhub.ai/user/tt-u) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to generate reproducible 24x24 pixel-art SVG avatars from names, IDs, or other seed strings and save them to chosen paths. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill invokes a pinned npm package through npx, which may download package code from the npm registry on first use. <br>
Mitigation: Use the documented @bitmappunks/avatar-generator@0.0.5 pin and install only in workspaces where npm package execution is acceptable. <br>
Risk: The skill writes SVG files to disk and can overwrite an existing path if the agent is directed to that path. <br>
Mitigation: Prefer an explicit output path and confirm before overwriting files in sensitive workspaces. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tt-u/bmp-avatar-generator) <br>
- [Project homepage](https://github.com/bitmappunks-com/avatar-generator-skill) <br>
- [@bitmappunks/avatar-generator npm package](https://www.npmjs.com/package/@bitmappunks/avatar-generator) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Guidance] <br>
**Output Format:** [SVG file with concise text confirmation and optional terminal ANSI preview] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Deterministic by seed; produces one SVG per invocation; terminal preview renders the generated SVG as ANSI truecolor blocks.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
