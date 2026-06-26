## Description: <br>
Scan meme coins for scam signals, rug-pull risk, and on-chain audit flags. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[loutai0307-prog](https://clawhub.ai/user/loutai0307-prog) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to inspect meme token addresses, review new or trending token listings, and generate safety checklists before doing manual verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The package includes an unrelated, undocumented local security utility that stores command history locally. <br>
Mitigation: Use the documented scripts/meme.sh for meme-coin scanning. Avoid scripts/script.sh unless intentionally using that separate utility. <br>
Risk: Token addresses scanned by scripts/meme.sh are sent to DexScreener public endpoints. <br>
Mitigation: Do not scan sensitive investigation targets unless sharing those token addresses with DexScreener is acceptable. <br>
Risk: Command arguments passed to scripts/script.sh can be saved on disk. <br>
Mitigation: Do not pass secrets, seed phrases, API tokens, or sensitive investigation details to scripts/script.sh. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/loutai0307-prog/bytesagain-meme-coin-scanner) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Terminal text with command examples, risk flags, external-check links, and checklist output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No structured JSON output is documented; scanner results depend on public DexScreener responses.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence; artifact frontmatter reports 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
