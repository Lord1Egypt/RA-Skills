Use the business blueprint skill to produce a finance architecture blueprint and its downstream projection for other skills.

Output requirements:
- Save all generated artifacts under {artifact_dir}.
- Create `solution.blueprint.json`.
- Run validation on the blueprint.
- Create `solution.projection.json` for downstream report/slide skills.
- Do not create the downstream report or slide deck yourself.

Source notes:
- Loan origination captures applications and sends risk signals to the decision engine.
- Risk control consumes credit bureau, fraud model, and customer profile data.
- Compliance reviews high-risk cases before contract generation.
- Core banking books approved loans and triggers repayment schedules.
- Key actors: applicant, loan officer, risk analyst, compliance reviewer.
