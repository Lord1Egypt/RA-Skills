## Description: <br>
Cn Percent Calculator helps agents calculate percentages, percentage values, growth rates, discounts, and VAT with a local Python tool. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freedompixels](https://clawhub.ai/user/freedompixels) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to answer Chinese-language percentage questions and run local calculations for percentage shares, percentage values, growth rates, discounts, and VAT. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Security evidence flags sensitive-credential handling as a release capability. <br>
Mitigation: Install only in a trusted ClawHub or development environment and review any commands involving admin tokens or published proof artifacts before use. <br>
Risk: Percentage, discount, growth, and VAT outputs depend on the supplied numbers and assumptions. <br>
Mitigation: Review inputs, discount conventions, and tax-rate assumptions before using results for business or compliance decisions. <br>
Risk: Natural-language parsing supports a limited set of Chinese percentage patterns. <br>
Mitigation: Use explicit CLI arguments or verify the computed result when a request is ambiguous. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/freedompixels/cn-percent-calculator) <br>
- [Publisher profile](https://clawhub.ai/user/freedompixels) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, guidance] <br>
**Output Format:** [Plain text or JSON calculation output, with concise agent guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs locally with the Python standard library and accepts supported Chinese natural-language prompts or explicit CLI arguments.] <br>

## Skill Version(s): <br>
1.2.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
