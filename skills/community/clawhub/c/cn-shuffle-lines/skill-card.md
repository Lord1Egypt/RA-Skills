## Description: <br>
Randomly shuffles the order of lines in text or a local file using Python standard library scripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freedompixels](https://clawhub.ai/user/freedompixels) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content operators use this skill to randomize newline-separated text, including pasted text, lists, prompts, samples, or local text files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The file mode reads the full supplied local file and prints shuffled content to standard output. <br>
Mitigation: Only provide files that the user intends the local script to read and display. <br>
Risk: Line order is randomized and may not be reproducible across runs. <br>
Mitigation: Use the output immediately or modify the script to set a fixed random seed when repeatability is required. <br>
Risk: External marketing links in the artifact are not required for the utility's function. <br>
Mitigation: Treat those links as optional website references and review them separately before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/freedompixels/cn-shuffle-lines) <br>
- [Publisher profile](https://clawhub.ai/user/freedompixels) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text and Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces shuffled line order on standard output; randomness is non-deterministic unless the script is modified to set a seed.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
