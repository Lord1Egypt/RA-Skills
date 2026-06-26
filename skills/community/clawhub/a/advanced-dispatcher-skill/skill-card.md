## Description: <br>
Routes mid-session work to deterministic spawned-model plans for coding, architecture, math, algorithms, web development, brainstorming, research, long-context reading, quick scripts, formatting, tradeoff evaluation, and build pipelines. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[omaression](https://clawhub.ai/user/omaression) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to route in-progress agent work to selected spawned models while keeping the main session fixed. It supports standard task routing, multi-model tradeoff evaluation, and buildq/build/buildx delivery pipelines with test and review stages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Task content may be routed to different spawned model providers, and some OpenAI routes use long cache retention. <br>
Mitigation: Use explicit prompts for build or tradeoff workflows and avoid sending secrets unless the selected provider and retention behavior are acceptable. <br>
Risk: Build pipelines can produce code changes that may be incorrect or broader than intended. <br>
Mitigation: Review generated diffs before merging and require the skill's automated test and review stages to pass before treating work as ready. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/omaression/advanced-dispatcher-skill) <br>
- [Advanced Dispatcher README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and structured route-plan text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include selected model routes, cache-retention rationale, tradeoff judge guidance, or build pipeline steps depending on the prompt.] <br>

## Skill Version(s): <br>
1.0.1-alpha (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
