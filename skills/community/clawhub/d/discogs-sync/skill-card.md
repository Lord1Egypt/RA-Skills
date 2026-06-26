## Description: <br>
Discogs Sync helps agents manage Discogs wantlists and collections by artist and album name, master ID, release ID, or bulk CSV/JSON input, and search marketplace pricing for vinyl, CD, and other formats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[khaney64](https://clawhub.ai/user/khaney64) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Discogs users and agents use this skill to authenticate with Discogs, add or remove releases from wantlists or collections, list saved items, sync batches from CSV/JSON files, and compare marketplace prices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make broad changes to a Discogs wantlist or collection. <br>
Mitigation: Review proposed commands before execution and run sync commands with --dry-run before allowing writes. <br>
Risk: The --remove-extras option can remove items that are not present in the input file. <br>
Mitigation: Use --remove-extras only after checking the dry-run output and confirming the input file is complete. <br>
Risk: Fuzzy artist and album matching can select an unintended release. <br>
Mitigation: Prefer exact Discogs release IDs for removals or high-impact updates. <br>
Risk: Discogs access tokens are stored locally in ~/.discogs-sync/config.json. <br>
Mitigation: Protect the credential file, delete it when no longer needed, and revoke tokens in Discogs if they may be exposed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/khaney64/discogs-sync) <br>
- [Publisher profile](https://clawhub.ai/user/khaney64) <br>
- [Discogs developer settings](https://www.discogs.com/settings/developers) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; the CLI can return terminal tables or JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local dependency, credential, and cache files when executed by an agent.] <br>

## Skill Version(s): <br>
0.1.10 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
