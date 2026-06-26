## Description: <br>
Runs VPS performance and network tests covering system information, CPU, memory, disk, streaming access, IP quality, routing, latency, and speed checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[spiritLHLS](https://clawhub.ai/user/spiritLHLS) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, VPS operators, and infrastructure evaluators use this skill to benchmark a target server and collect network, performance, routing, streaming-access, and IP-quality results for comparison or diagnosis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill downloads and runs an upstream binary at runtime. <br>
Mitigation: Install only when comfortable with runtime binary download and prefer running on a disposable or test VPS as a non-root user. <br>
Risk: The default test flow can upload detailed server and network results publicly. <br>
Mitigation: Pass -upload=false unless public result sharing is intentional. <br>
Risk: Broad external network tests may disclose infrastructure characteristics or trigger monitoring on the target network. <br>
Mitigation: Run only on systems and networks where benchmarking and outbound network testing are authorized. <br>
Risk: Using --call-ai can share raw infrastructure results with the configured AI backend. <br>
Mitigation: Review result contents before AI analysis and avoid --call-ai when the results contain sensitive infrastructure details. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/spiritLHLS/clawchimera) <br>
- [Clawdis homepage](https://github.com/oneclickvirt/ClawChimera) <br>
- [Upstream ECS project](https://github.com/oneclickvirt/ecs) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Plain text benchmark results, terminal output, and Markdown analysis prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes goecs.txt when tests complete; analyze.sh can summarize or compare result files and can optionally call a local AI tool.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
