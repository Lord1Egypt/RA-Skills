## Description:

Integrate Backboard.io for assistants, threads, memories, and document RAG via a local backend on http://localhost:5100.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrisk60331](https://clawhub.ai/user/chrisk60331)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to create and manage Backboard assistants, conversation threads, persistent memories, and document RAG workflows from an agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An unauthenticated local backend exposes assistant, thread, memory, and document operations if reachable on a network.

Mitigation: Run only on a trusted machine, bind to 127.0.0.1, avoid exposing port 5100, and add authentication before shared use.

Risk: Documents, messages, and memories may be processed by Backboard and configured model providers.

Mitigation: Do not upload sensitive documents or store sensitive memories unless the user accepts provider processing and retention.

Risk: Routine startup installs unpinned dependencies, which can change behavior over time.

Mitigation: Pin and review dependencies before routine or production-like use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/chrisk60331/skills/backboard)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown or JSON responses with backend setup and API operation details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BACKBOARD_API_KEY and a running local backend on port 5100.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
