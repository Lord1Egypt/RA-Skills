## Description: <br>
AudioBookLM helps agents run audiobook and podcast creation workflows through the audiobooklm_mcp remote tools, including chapter creation, voice assignment, synthesis, mixing, and optional album publishing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[audiobooklm](https://clawhub.ai/user/audiobooklm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators and developers use this skill to guide podcast, single-narrator audiobook, and multi-cast audiobook production through AudioBookLM/Ximalaya tools. It helps configure authentication, choose the appropriate workflow, confirm user inputs, bind voices, synthesize chapters, mix audio, and optionally publish to an album. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an AudioBookLM/Ximalaya token and may send user-provided content or files to the remote service. <br>
Mitigation: Install only if the user trusts AudioBookLM/Ximalaya with the token and content, and avoid sending private, copyrighted, or sensitive files unless authorized. <br>
Risk: The security summary notes a local-file upload path using a raw authenticated curl command outside the stated MCP workflow. <br>
Mitigation: Before approving any local-file upload, verify the exact file path, destination, and token handling; do not expose Authorization headers in user-visible output. <br>
Risk: The workflows can create or modify books, chapters, character voice bindings, synthesis jobs, mixed audio, and album uploads. <br>
Mitigation: Require user confirmation before write operations, use returned IDs and statuses only, and stop on tool errors or unverified results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/audiobooklm/audiobooklm) <br>
- [AudioBookLM homepage](https://aigc.ximalaya.com) <br>
- [AudioBookLM MCP endpoint](https://aigc.ximalaya.com/audiobooklm/mcp) <br>
- [AudioBookLM user center](https://aigc.ximalaya.com/user/center) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration, Shell commands, API calls] <br>
**Output Format:** [Markdown with MCP tool call guidance and inline configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns confirmed book, chapter, character, speaker, task, audio, edit, and album details; does not expose tokens.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
