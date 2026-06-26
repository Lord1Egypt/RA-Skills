## Description: <br>
Display amount of free and used memory in the system. Use for monitoring memory usage and diagnosing performance issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dinghaibin](https://clawhub.ai/user/dinghaibin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and system operators use this skill to inspect Linux memory and swap totals while monitoring memory usage or diagnosing performance issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The utility depends on Linux-style /proc/meminfo, so it may not work on systems without that interface. <br>
Mitigation: Use it on Linux-like systems and verify memory values against platform-native tools when running elsewhere. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dinghaibin/free-tool) <br>
- [Publisher profile](https://clawhub.ai/user/dinghaibin) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text memory statistics and Markdown usage examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads Linux /proc/meminfo and reports selected memory and swap fields.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
