## Description: <br>
平替旅行家 helps travelers break down the core experience of an aspirational destination and find closer or lower-cost substitute destinations that match the user's budget, time, distance, or visa constraints. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hello-ahang](https://clawhub.ai/user/hello-ahang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External travelers use this skill to turn a destination they consider too expensive, far away, time-consuming, or difficult to visit into feasible substitute trip options. The skill guides an agent through experience decomposition, FlyAI-backed destination search, flight and hotel checks, match scoring, budget comparison, and transparent difference notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can install or upgrade global CLI packages without pinning and may suggest sudo when permissions fail. <br>
Mitigation: Review installation commands before execution, prefer a pinned CLI version in an isolated Node environment, and avoid sudo or global installs unless explicitly approved. <br>
Risk: The workflow instructs agents to set NODE_TLS_REJECT_UNAUTHORIZED=0 for routine searches, disabling TLS certificate validation. <br>
Mitigation: Keep TLS validation enabled by default and only disable it for a clearly understood temporary troubleshooting case after user approval. <br>
Risk: The skill may persist travel profile details such as location, budget, family context, and special needs in memory or ~/.flyai/user-profile.md. <br>
Mitigation: Ask for consent before saving profile data, avoid persisting sensitive details unless necessary, and periodically review or delete stored profile entries. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hello-ahang/flyai-destination-substitute) <br>
- [Workflow](reference/workflow.md) <br>
- [Tools](reference/tools.md) <br>
- [Examples](reference/examples.md) <br>
- [User profile storage](reference/user-profile-storage.md) <br>
- [Self-learning](reference/self-learning.md) <br>
- [AI search](reference/ai-search.md) <br>
- [Keyword search](reference/keyword-search.md) <br>
- [Flight search](reference/search-flight.md) <br>
- [Hotel search](reference/search-hotel.md) <br>
- [POI search](reference/search-poi.md) <br>
- [Train search](reference/search-train.md) <br>
- [Marriott hotel search](reference/search-marriott-hotel.md) <br>
- [Marriott package search](reference/search-marriott-package.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown travel recommendations with comparison tables, command snippets, budget estimates, match scores, and caveat notes.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include user-profile read/write prompts and travel search command examples.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
