## Description: <br>
Fetch any URL and convert it to Markdown using Chrome CDP, saving rendered HTML snapshots, extracting page metadata, supporting wait mode for login-required pages, and falling back through Defuddle, legacy conversion, or the hosted defuddle.md API when needed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nengnengZ](https://clawhub.ai/user/nengnengZ) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and agents use this skill to capture web pages as Markdown files for notes, archives, research workflows, or downstream content processing. It is especially useful when JavaScript rendering, login-assisted capture, media localization, or YouTube transcript extraction is needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send a target URL to the hosted defuddle.md fallback when local browser capture fails. <br>
Mitigation: Use it only on URLs appropriate for third-party processing, or configure and monitor usage so sensitive private, internal, or token-bearing URLs are not sent to the fallback service. <br>
Risk: Rendered HTML snapshots, Markdown output, a dedicated Chrome profile, and downloaded media can persist private page content locally. <br>
Mitigation: Avoid capturing highly sensitive pages, keep media downloads on ask or never for untrusted pages, and periodically review or clear the output directory and Chrome profile. <br>


## Reference(s): <br>
- [Baoyu URL to Markdown homepage](https://github.com/JimLiu/baoyu-skills#baoyu-url-to-markdown) <br>
- [First-time setup reference](references/config/first-time-setup.md) <br>
- [ClawHub skill page](https://clawhub.ai/nengnengZ/baoyu-url-to-markdown-2) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands, Configuration] <br>
**Output Format:** [Markdown files with YAML front matter, optional sibling HTML snapshots, optional localized media files, and console status output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include captured page HTML, downloaded image and video directories, conversion method logs, and fallback status.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
