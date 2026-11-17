# Prevention — Screening, Vaccines, Travel

Screening is a test offered to people with no symptoms, which makes it the one area of medicine where the harms fall on healthy people. Every recommendation here comes with its body, because the bodies disagree and the disagreement is honest.

**Before answering**, read `## Screenings` and `## Vaccines` in `~/Clawic/data/health/profile.md` and the `## Due` table in `~/Clawic/data/doctor/memory.md` — half of prevention work is knowing what was already done and when. State anything overdue in one line. Ages and intervals below follow `guideline_body`; while it is unset, give the body's name with each number.

## Adult Screening

| Screen | Who and when | Body |
|---|---|---|
| Blood pressure | Every adult, at least every 3-5 years; annually from 40 or if previously high | USPSTF, NICE |
| Colorectal cancer | From 45 to 75 (stool test every 1-2 years, or colonoscopy every 10 years); several national programmes start at 50 | USPSTF 2021 vs national programmes |
| Breast cancer | Mammography every 2 years, 40-74 per USPSTF 2024; many European programmes run 50-69/74 | USPSTF vs national programmes |
| Cervical cancer | HPV testing every 5 years from 30 to 65; cytology every 3 years from 21-29 where HPV testing is not used | USPSTF, WHO |
| Lung cancer | Annual low-dose CT, 50-80, with a 20 pack-year history and still smoking or quit within 15 years | USPSTF 2021 |
| Abdominal aortic aneurysm | One-time ultrasound, men 65-75 who ever smoked | USPSTF |
| Lipids and cardiovascular risk | From 40, every 5 years, sooner with risk factors — the output is a 10-year risk score, not a cholesterol number | Most bodies |
| Type 2 diabetes | From 35-40, or at any age with overweight plus a risk factor; every 3 years if normal | USPSTF, ADA |
| Osteoporosis | Women from 65; earlier with fracture history, steroids, or early menopause | USPSTF |
| Hepatitis C | Once in adulthood for everyone 18-79 | USPSTF |
| Depression and anxiety | All adults, at routine contacts, using a scored screen (`mental-health.md`) | USPSTF |
| Prostate (PSA) | A shared decision, 55-69, not a routine test; against over 70 | USPSTF grade C |
| Vision, hearing, falls | From 65, annually — hearing loss and falls have larger downstream effects than most screened cancers | Multiple |

**Pack-year formula**, because the lung-cancer criterion depends on it: packs per day × years smoked. Ten cigarettes a day for 40 years = 0.5 × 40 = 20 pack-years, which qualifies.

## The Harms Side, Which Is Rarely Stated

- **False positives** are the common outcome of any screening programme run over years, and each one costs anxiety, further tests and sometimes a biopsy.
- **Overdiagnosis** is finding disease that would never have caused symptoms in that person's lifetime; it is treated anyway, because nobody can tell which ones. It is the main harm in prostate, thyroid and some breast screening.
- The number worth asking for is the **number needed to screen** to prevent one death over a decade, alongside the false-positive rate for the same period. When a programme cannot state both, that is information too.
- None of this argues against screening. It argues for choosing which ones apply to *this* person, and for the person knowing what a positive result starts.

## Vaccines

| Vaccine | Adult schedule |
|---|---|
| Tetanus/diphtheria/pertussis | Booster every 10 years; every pregnancy for pertussis; 5-year rule for dirty wounds (`injuries.md`) |
| Influenza | Annually, before the season; strain composition changes each year, which is why last year's does not carry over |
| COVID-19 | Boosters per current national schedule and risk group |
| Pneumococcal | From 65, or earlier with chronic lung, heart, liver or kidney disease, diabetes, immunosuppression, or no spleen |
| Shingles | From 50-65 depending on programme; two doses of the recombinant vaccine |
| HPV | Routine in adolescence; catch-up into adulthood in several programmes |
| MMR | Two documented doses, or evidence of immunity — a gap matters for anyone born after routine vaccination began and never completed |
| Hepatitis B | Health workers, household and sexual contacts, chronic liver or kidney disease, travel |
| RSV | Older adults and pregnancy in programmes that now offer it |

Asplenia, immunosuppression and pregnancy each carry their own additional schedule; note the status in the profile so it is applied every time rather than remembered.

## Travel Health

- Start 6-8 weeks before departure: several vaccines need a course, and rabies pre-exposure is three doses.
- **Malaria** prophylaxis is chosen by destination, season and resistance pattern, and started before arrival — bite avoidance (repellent, nets, covered evenings) is not optional alongside it. Fever after return from an endemic area within a year is an urgent malaria test, not a wait.
- **Traveller's diarrhoea**: oral rehydration is the treatment; antibiotics are for severe or dysenteric illness only. Blood in stool or high fever means being seen.
- **Flights and clots**: risk rises with flights over about 4 hours, and multiplies with recent surgery, pregnancy, oestrogen, cancer or a previous clot. Move hourly, hydrate; compression stockings for higher risk; aspirin is not prophylaxis.
- **Altitude**: ascend gradually above 2,500 m, and treat headache with nausea and unsteadiness as altitude illness — descend rather than push on.
- Carry medicines in labelled original packaging with a prescription list, check destination rules for controlled drugs, and take enough for the trip plus a week.

## The Levers That Beat Every Test

Named honestly, because they are unglamorous and they dominate: not smoking, blood pressure control, physical activity, alcohol below hazardous levels, sleep, weight, and vaccination. Effect sizes here are larger than any single screening programme's, and unlike screening they carry no false positives. Where the user wants depth on one of these, the specialist skills go further (`nutrition`, `fitness`, `sleep`).

## Where This Goes

**Write in the same turn** (`memory-template.md`): every screening done — test, date, result, and the interval to the next one — goes to `## Screenings` in `~/Clawic/data/health/profile.md`; every vaccine to `## Vaccines` with date and, where it has one, validity. Both create or refresh a row in `## Due` of `~/Clawic/data/doctor/memory.md` when `screening_reminders` is true, so the next one is a date rather than a memory. A travel plan with its vaccine course and prophylaxis dates is an artifact — `~/Clawic/data/doctor/artifacts/travel-<destination>.md` — with its `## Boxes` line the same turn, and the trip itself belongs in the shared `~/Clawic/data/bookings/<year>.md` rather than here.
