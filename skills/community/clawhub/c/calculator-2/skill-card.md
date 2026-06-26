## Description: <br>
Provides basic arithmetic calculation support for addition, subtraction, multiplication, division, chained expressions, and step-by-step result explanations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CexFree](https://clawhub.ai/user/CexFree) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill when they need an agent to parse ordinary arithmetic requests, show the calculation process, and return a clear result. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Arithmetic output may be wrong or insufficient for high-stakes decisions because the skill is an agent instruction prompt, not a certified calculator. <br>
Mitigation: Use it for ordinary arithmetic help and independently verify any high-stakes calculations. <br>
Risk: Division by zero or complex chained expressions can produce misleading results if the agent skips validation or omits intermediate steps. <br>
Mitigation: Check for division by zero, follow standard order of operations, and show the calculation process before returning the result. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/CexFree/calculator-2) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance] <br>
**Output Format:** [Plain text or Markdown with arithmetic steps and a final result] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No code execution, credential use, file access, network access, or persistence indicated by security evidence.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
