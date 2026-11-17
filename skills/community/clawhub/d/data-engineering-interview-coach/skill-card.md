## Description:

An interactive coaching skill that runs data engineering mock interviews one question at a time and gives targeted feedback across SQL, data modeling, pipelines, Spark, Airflow, Kafka, dbt, warehouses, lakehouses, observability, and optimization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cngvc](https://clawhub.ai/user/cngvc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to practice senior-level data engineering interview topics through structured mock interview sessions, feedback, mini-lessons, and periodic session summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The coaching flow is tailored to a specific persona named Joe, which may not fit every learner or team.

Mitigation: Review and adapt the learner profile before deploying it for a broader audience.

Risk: The skill may activate on short SQL or pipeline-practice prompts that were not intended as interview practice.

Mitigation: Use it where mock interview, quiz, or drill behavior is desired, and review trigger routing for broad SQL or pipeline prompts.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown conversation with structured coaching feedback and session summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces one question at a time and waits for the learner's answer before giving feedback.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
