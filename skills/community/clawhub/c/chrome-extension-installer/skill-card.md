## Description: <br>
Install a Chrome extension by ID or Chrome Web Store URL on this Mac. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ryanpwelliver-oss](https://clawhub.ai/user/ryanpwelliver-oss) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to open Chrome Web Store installation pages, force-install trusted Chrome extensions through macOS Chrome policy, or load unpacked extensions for local development. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Chrome force-install policy can silently and persistently install extensions through managed policy. <br>
Mitigation: Prefer the Chrome Web Store method so Chrome shows extension details and permissions; use force-install only for trusted extension IDs and document how to remove the policy entry. <br>
Risk: Policy installation requires sudo and modifies the local Chrome managed preferences. <br>
Mitigation: Review the exact extension ID and command before execution, and apply it only on the intended macOS Chrome profile. <br>


## Reference(s): <br>
- [Chrome Web Store extension page template](https://chromewebstore.google.com/detail/<extension-id>) <br>
- [Chrome extension update service endpoint](https://clients2.google.com/service/update2/crx) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes macOS-specific Chrome policy commands that may require sudo and affect the user's Chrome profile.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
