## Description: <br>
Caches and manages frequently used context fragments to avoid redundant processing by saving, listing, clearing, and preloading cached data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shaoxiang616](https://clawhub.ai/user/shaoxiang616) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to cache reusable context fragments, list saved fragments, clear the cache, and optionally preload saved context at session startup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent local cache entries may contain secrets, credentials, private data, or stale instructions. <br>
Mitigation: Do not memoize sensitive or untrusted content, and review cached fragments periodically before reuse or session startup preload. <br>
Risk: The clear-cache example deletes the entire ~/.openclaw/context-cache directory. <br>
Mitigation: Confirm the path and intent before running the clear-cache command. <br>


## Reference(s): <br>
- [Context Memoize on ClawHub](https://clawhub.ai/shaoxiang616/context-memoize) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May append, list, delete, or preload local cache files under ~/.openclaw/context-cache when the agent follows the documented examples.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
