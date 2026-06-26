# Consult Workflow - Dermatologist

Use this file when the user wants an export-ready handoff for a clinician visit.

## Visit Summary Structure

Build the summary in this order:

1. Main concern
   - what the user wants checked
   - why the timing matters now
2. Timeline
   - onset
   - biggest change
   - treatments or exposures linked to the change
3. Symptoms
   - itch, pain, burn, tenderness, bleeding, crust, drainage, fever, or none
4. Photo index
   - baseline date
   - latest comparable photo date
   - whether the photos are reliably comparable
5. Questions
   - diagnosis clarification
   - need for biopsy, culture, patch testing, or referral
   - treatment options and timelines

## Output Template

```markdown
# Visit Summary - {case-id}

- Main concern:
- Body site:
- First noticed:
- Biggest recent change:
- Symptoms:
- Treatments tried and response:
- Relevant exposures:
- Red flags already present:
- Baseline photo date:
- Latest comparable photo date:

## Questions for Visit
- Question 1
- Question 2
- Question 3
```

## After the Visit

- Record only what the user reports the clinician said or what appears in written instructions.
- Track medication names and schedules exactly as provided.
- Set follow-up date, re-photo timing, and stop conditions for the current case.
- If the plan is unclear, say that the written instructions should control over memory or paraphrase.
