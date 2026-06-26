## Description: <br>
Monitor blogs and RSS/Atom feeds for updates using the blogwatcher CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and other CLI users use this skill to install and operate blogwatcher for tracking blogs and RSS/Atom feed updates while applying local-use safety guardrails. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Go install target is unpinned and depends on the upstream blogwatcher project. <br>
Mitigation: Install only when the upstream project is trusted; pin or review the module version in controlled deployments. <br>
Risk: Feed URLs from untrusted, shortened, or internal sources can expose local or internal network resources. <br>
Mitigation: Confirm discovered URLs with the user and refuse localhost, private IP ranges, link-local addresses, and .local or .internal domains. <br>
Risk: Blogwatcher output can include subscription data and article metadata. <br>
Mitigation: Keep output local and do not pipe or redirect it to network-transmitting commands or remote destinations. <br>
Risk: Bulk read or remove operations can affect more saved data than the user intended. <br>
Mitigation: Require clear confirmation when remove or read-all requests are ambiguous or broader than the user's stated intent. <br>


## Reference(s): <br>
- [Blogwatcher upstream repository](https://github.com/Hyaxia/blogwatcher) <br>
- [Blogwatcher Hardened ClawHub page](https://clawhub.ai/snazar-faberlens/blogwatcher-hardened) <br>
- [Faberlens blogwatcher safety evaluation](https://faberlens.ai/explore/blogwatcher) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local blogwatcher CLI commands and safety guidance; no network transmission of blogwatcher output should be proposed.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
