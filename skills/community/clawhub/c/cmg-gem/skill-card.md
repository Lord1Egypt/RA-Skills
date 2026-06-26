## Description: <br>
This skill helps agents generate, debug, and refine CMG GEM reservoir or core-scale DAT simulation files with attention to runnable syntax and scale-appropriate well definitions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nv4dll-git](https://clawhub.ai/user/nv4dll-git) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Reservoir engineers and technical agents use this skill to draft CMG GEM DAT files, choose oil-reservoir or core-scale modeling patterns, run local simulation commands when requested, and diagnose simulator output errors for iterative correction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated DAT files or simulator runs may use an unintended working directory, executable path, file name, or parallelism setting. <br>
Mitigation: Review the DAT file, working directory, executable path, and parallelism setting before running a simulation, and use a controlled project directory to avoid overwriting important files. <br>
Risk: Reservoir simulation output can be incorrect when user-provided units, grid dimensions, component ordering, initialization data, or well definitions are incomplete or inconsistent. <br>
Mitigation: Validate units, array lengths, component mole fractions, scale-specific well definitions, and simulator logs before relying on generated results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nv4dll-git/cmg-gem) <br>
- [Publisher profile](https://clawhub.ai/user/nv4dll-git) <br>
- [Artifact skill instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with CMG GEM DAT snippets, diagnostic notes, and Windows CMD command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce simulation file content and local run commands for user review before execution.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
