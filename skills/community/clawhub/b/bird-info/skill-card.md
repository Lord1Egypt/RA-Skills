## Description: <br>
Query bird information from dongniao.net using web_fetch. Automatically search and extract detailed information about any bird species. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Leogaga](https://clawhub.ai/user/Leogaga) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agent operators use this skill to look up bird species by Chinese, English, or scientific name and receive concise taxonomy, habitat, distribution, and conservation information from Dongniao. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bird-name queries are sent to dongniao.net. <br>
Mitigation: Avoid including personal or sensitive information in bird-name queries and deploy only where access to dongniao.net is acceptable. <br>
Risk: Species results depend on the Dongniao database and exact matching behavior. <br>
Mitigation: Cross-check critical research or conservation decisions with primary sources or expert references. <br>
Risk: The artifact describes web_fetch behavior, while the executable implementation performs HTTP requests from Python. <br>
Mitigation: Review the packaged script and runtime dependencies before deployment so operators understand the actual network behavior. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Leogaga/bird-info) <br>
- [Dongniao](https://dongniao.net) <br>
- [Dongniao taxonomy page](https://dongniao.net/taxonomy.html) <br>
- [IOC World Bird List](https://www.worldbirdnames.org/) <br>
- [BirdWatch China](https://www.birdwatch.cn/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Plain text or Markdown-style structured sections with command-line status messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns bird details and source attribution; exits nonzero with a user-facing error when no exact species match is found.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
