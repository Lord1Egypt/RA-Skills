## Description: <br>
Participate in the FORTUNA autonomous agent lottery on Solana by checking round status and, when explicitly approved, buying tickets by sending SOL to the treasury. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[codiicode](https://clawhub.ai/user/codiicode) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to inspect FORTUNA lottery rounds, review jackpot and ticket status, and optionally purchase Solana lottery tickets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can lead an agent to spend SOL on lottery tickets. <br>
Mitigation: Use a dedicated low-balance Solana wallet, verify the treasury address independently, and require explicit manual approval for every ticket purchase or SOL transfer. <br>
Risk: The optional fallback transfer script uses a Solana private key from the environment. <br>
Mitigation: Never provide a main wallet private key; prefer an existing wallet integration when available and only set SOLANA_PRIVATE_KEY for a dedicated wallet. <br>


## Reference(s): <br>
- [FORTUNA homepage](https://fortunaonsol.com) <br>
- [FORTUNA API](https://fortunaonsol.com/api/) <br>
- [Current round endpoint](https://fortunaonsol.com/api/current-round) <br>
- [ClawHub skill page](https://clawhub.ai/codiicode/fortuna) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API calls] <br>
**Output Format:** [Markdown with inline bash commands and API endpoint references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may query public APIs or initiate Solana transfers when explicitly executed.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
