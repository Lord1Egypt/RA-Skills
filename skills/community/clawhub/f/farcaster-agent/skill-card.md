## Description: <br>
Create Farcaster accounts and post casts autonomously. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rishavmukherji](https://clawhub.ai/user/rishavmukherji) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to create a Farcaster identity, configure a profile, and post casts through guided Node.js commands and JavaScript examples. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks the agent to run unbundled Node.js code while handling wallet private keys. <br>
Mitigation: Verify the external source and publisher claim, inspect the Node.js scripts before execution, and provide keys only through a fresh, low-balance wallet. <br>
Risk: The skill can move funds and post publicly to a Farcaster account. <br>
Mitigation: Require explicit operator approval for funding, transaction, and cast-posting actions before running the commands. <br>
Risk: Account-control credentials may be saved to plaintext local files by default. <br>
Mitigation: Prefer the documented no-save mode or a proper secret manager, and treat any saved credential file as sensitive account-control material. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/rishavmukherji/farcaster-agent) <br>
- [Farcaster Agent Source Referenced by Skill](https://github.com/rishavmukherji/farcaster-agent) <br>
- [Neynar Hub API](https://hub-api.neynar.com) <br>
- [Neynar REST API](https://api.neynar.com) <br>
- [Farcaster Fname Registry](https://fnames.farcaster.xyz) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration] <br>
**Output Format:** [Markdown with bash and JavaScript code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and npm; workflows may use wallet private keys, saved credentials, funds, and external Farcaster and Neynar APIs.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
