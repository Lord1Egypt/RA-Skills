# Formal Adoption Status Protocol

Use this protocol for policy, standard, regulation, exam, certification, governance, and official-program research.

Official-looking sources do not all have the same force. Separate legal / institutional status before making a current-state claim.

## Status Ladder

| Status | Meaning | Typical source | How to phrase |
| --- | --- | --- | --- |
| `final-in-force` | final rule / law / standard exists and has entered into force | official journal, enacted law, published standard | "is in force" |
| `applicable-obligation` | an obligation is currently applicable to covered parties | article application date, official enforcement timeline | "applies from / is currently applicable" |
| `adopted-not-yet-applicable` | final text exists but duties start later | law text, official timeline | "has been adopted, applies from..." |
| `delegated-or-implementing-act` | secondary official act under a law / standard | regulator act, implementing decision | "supplements / implements..." |
| `official-guidance-final` | final non-legislative guidance | regulator guideline, FAQ, code guidance | "guidance says..." |
| `official-guidance-draft` | draft guidance or consultation text | consultation page, draft PDF | "draft guidance proposes..." |
| `political-agreement` | institutions agreed politically but final text may still need formal adoption | press release, trilogue / council / commission statement | "political agreement indicates..." |
| `pilot-or-trial` | official trial, pilot, beta, or transitional test | exam owner notice, regulator sandbox notice | "trial / pilot stage..." |
| `institution-policy` | one school, employer, platform, or local body applies its own rule | institution page | "applies for this institution only..." |
| `voluntary-code` | voluntary code, pledge, or industry commitment | code of practice, pledge registry | "voluntary unless incorporated elsewhere..." |
| `third-party-interpretation` | media, vendor, training provider, consultant summary | article, blog, course page | "interprets / summarizes..." |

## Required Fields

For each current-status claim, record:

- `status_label`
- `source_tier`
- `evidence_ids`
- `jurisdiction_or_institution`
- `effective_date`
- `application_date`
- `formal_adoption_step_remaining`
- `confidence`

If the status cannot be established, mark it as `status-unclear` and turn the conclusion into a recheck task.

## Phrase Discipline

- Do not say "is law" when the evidence only shows a political agreement.
- Do not say "applies now" when the evidence only shows an adopted future obligation.
- Do not treat draft guidance as final guidance.
- Do not generalize one institution's acceptance rule to all institutions.
- Do not treat a training-provider page as authority for official status.

## Monitoring

For volatile official-status topics, monitor:

- final text publication.
- entry-into-force date.
- application / enforcement dates by article or stakeholder.
- guidance finalization.
- delegated / implementing acts.
- institution-specific acceptance or implementation notices.
