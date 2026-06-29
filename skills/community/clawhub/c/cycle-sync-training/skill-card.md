## Description: <br>
Cycle Sync Training helps an agent plan women-focused workouts around menstrual-cycle phases, symptoms, energy, and training goals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kritsanan1](https://clawhub.ai/user/kritsanan1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and fitness agents use this skill to record cycle phase context, generate phase-aware workout plans, adjust intensity from symptoms and energy, and predict higher-energy windows for training goals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles menstrual-cycle, symptom, mood, energy, and fitness data with persistent storage expectations, but the evidence does not show clear consent, retention, access, or deletion controls. <br>
Mitigation: Use only when users intentionally want cycle-based fitness guidance, avoid logging sensitive health data until storage and deletion controls are understood, and add explicit consent plus retention and sharing documentation. <br>
Risk: The artifact asks agents to trigger on women-focused fitness planning even when a user does not explicitly mention cycle tracking. <br>
Mitigation: Narrow activation to explicit cycle-related requests and avoid collecting cycle or symptom details during general fitness conversations. <br>


## Reference(s): <br>
- [Server-resolved source repository](https://github.com/kritsanan1/cycle-sync-training) <br>
- [ClawHub skill page](https://clawhub.ai/kritsanan1/skills/cycle-sync-training) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, JSON, Configuration] <br>
**Output Format:** [Markdown documentation with JSON request and response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes MCP tool descriptions for logging cycle phase, generating workouts, adjusting intensity, and predicting energy windows.] <br>

## Skill Version(s): <br>
0.1.2 (source: server-resolved release) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
