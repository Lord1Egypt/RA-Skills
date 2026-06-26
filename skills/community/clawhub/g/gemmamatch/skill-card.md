## Description: <br>
Auto-detect hardware and recommend the best Gemma 4 model for local deployment on PC, Mac, or mobile. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[walex8925](https://clawhub.ai/user/walex8925) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and local AI users use this skill to choose a Gemma 4 model tier for their device and obtain setup guidance or run commands for local deployment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated terminal commands may not match the user's intended local setup. <br>
Mitigation: Review every generated command before running it and adjust model, runtime, and platform options as needed. <br>
Risk: Browser hardware detection uses WebGPU/WebGL APIs on an external website. <br>
Mitigation: Use manual hardware entry if browser GPU detection is not appropriate for the user's privacy or environment requirements. <br>


## Reference(s): <br>
- [GemmaMatch website](https://www.gemmamatch.com) <br>
- [GemmaMatch ClawHub page](https://clawhub.ai/walex8925/gemmamatch) <br>
- [GemmaMatch source link](https://github.com/walex8925/Gemma4local) <br>
- [GemmaMatch Product Hunt page](https://www.producthunt.com/products/gemma-4-local-hardware-matcher) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with links and copy-paste command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Recommendations depend on browser hardware detection or manually entered hardware details.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
