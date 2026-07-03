## Description: <br>
3-pass recursive prompting that critiques, refines, and finalizes an answer for a claim, diagnosis, plan, or analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[h-mascot](https://clawhub.ai/user/h-mascot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and other agent users use this skill to stress-test a claim, diagnosis, plan, or analysis through critique, evidence gathering, and a final evidence-backed answer. It is most useful before decisions where missing evidence, weak assumptions, or overconfidence would create risk. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may use broad conversation context and ask the agent to investigate with tools without clear limits on what should be analyzed or accessed. <br>
Mitigation: Invoke it with explicit target text where possible, and review or constrain any proposed command, file read, or web search before allowing it to proceed. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown sections for Pass 1 critique, Pass 2 refinement, and Pass 3 final answer.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include tool-backed evidence and recommended next steps; users should review any proposed command, file read, or web search before allowing it to proceed.] <br>

## Skill Version(s): <br>
1.0.1780516490 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
