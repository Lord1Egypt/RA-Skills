# Evidence Evaluation

Use this reference to decide what to trust first, what to treat cautiously, and what questions to ask before turning evidence into action.

## Source Priority

Match the source ladder to the task instead of using a single rigid rule.

For clinical or biomedical decision support, prefer this order when applicable:

1. Current practice guidelines or consensus statements from credible bodies.
2. Systematic reviews and meta-analyses.
3. Large, well-designed randomized or otherwise high-quality prospective studies.
4. Strong observational studies, registries, or comparative effectiveness work.
5. Methods papers, benchmark studies, or validated reference implementations.
6. Preprints, conference abstracts, narrative reviews, and expert commentary.
7. Blog posts, social media threads, or model-generated summaries.

For method selection or scientific tooling, sometimes prioritize these instead:

1. Seminal methods papers and strong benchmark studies.
2. Official tool or library documentation.
3. Widely adopted reference implementations.
4. Comparative evaluations, ablations, and reproducibility studies.
5. Informal tutorials or community discussion.

## Medical Appraisal Prompts

Ask these questions before trusting a claim:

- Does the study population match the target population in age, disease severity, comorbidities, and care setting?
- Does the intervention, exposure, or diagnostic approach match the real question being answered?
- Is the comparator appropriate and current?
- Are the outcomes clinically meaningful, or only surrogate markers?
- Is the sample size large enough to support the claimed conclusion?
- Are the follow-up period and endpoint timing appropriate?
- Are major biases, confounders, or missing data likely to change the result?
- Does the paper report absolute effects, harms, uncertainty, and limitations clearly?
- Does the study reflect current standard of care, or has practice changed since publication?

## Biomedical Red Flags

Slow down when any of these appear:

- Only an abstract or press release is available.
- The claim jumps from cell or animal data to human efficacy.
- The result depends on a surrogate endpoint with unclear patient benefit.
- The data come from a single center, very small cohort, or highly selected population.
- The study is retrospective and the confounding risk is substantial.
- The evidence is preprint-only for a high-stakes conclusion.
- The paper makes subgroup claims without adequate power or multiplicity control.
- The analysis mixes association with causation.
- The recommendation ignores harms, contraindications, or competing risks.

## Reporting Standards to Keep in Mind

Use reporting standards as search targets and quality signals when relevant:

- PRISMA for systematic reviews.
- CONSORT for randomized trials.
- STROBE for observational studies.
- STARD for diagnostic accuracy studies.
- TRIPOD for prediction models.
- CARE for case reports.
- ARRIVE for animal studies.

## Safe Output Discipline

When summarizing evidence:

- State what is well supported.
- State what is plausible but uncertain.
- State what would change the conclusion.
- Separate source-backed findings from your inference.
- Avoid turning a literature summary into personalized medical advice.

When recommending a path forward:

- Prefer the strongest applicable standard.
- Name the main uncertainty explicitly.
- Suggest what additional evidence, dataset, or validation step would most reduce risk.
