## Description: <br>
Free, local, deterministic knowledge base for AI agents. 443 verified facts, instant cache (122x speedup), no hallucinations. MIT license. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[certainlogicai](https://clawhub.ai/user/certainlogicai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to install and operate a local knowledge base for deterministic, cache-backed answers grounded in stored company facts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installation runs unpinned external code that is not fully represented in the reviewed package. <br>
Mitigation: Review install.sh and the upstream source before installing, and prefer a pinned release or manual dependency setup before using it with private company facts. <br>
Risk: The installer can execute user-level code from bun.sh, GitHub, and pip. <br>
Mitigation: Install in a controlled environment and proceed only if those external sources are acceptable for the intended workspace. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/certainlogicai/company-brain-os) <br>
- [CertainLogic Company Brain](https://certainlogic.ai/brain) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes local installation and health-check guidance for a cache-backed knowledge base.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
