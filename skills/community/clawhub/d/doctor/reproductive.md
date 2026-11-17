# Reproductive And Sexual Health — Windows That Decide The Option

More of this domain is governed by clock windows than any other: contraception, emergency contraception, post-exposure prophylaxis, test window periods, pregnancy dating. Get the window right first, then the option.

**Before answering**, read `## Conditions`, `## Medications` and `## Allergies` in `~/Clawic/data/health/profile.md`, plus the restrictions preference area in `config.yaml` — migraine with aura, clotting history, smoking over 35, breast cancer history and current pregnancy or breastfeeding each remove options from the list before it is offered. Day-to-day cycle tracking is `period`; pregnancy tracking is `pregnancy`.

## Contraception

| Method | Typical-use failure per year | Notes that decide it |
|---|---|---|
| Implant | <1% | Most effective reversible method; irregular bleeding is the common reason for removal |
| IUD (copper or hormonal) | <1% | Copper is hormone-free and heavier bleeding; hormonal is lighter or absent periods |
| Injection | ~4% | Delayed return of fertility, up to a year |
| Combined pill | ~7% | Contraindicated with migraine with aura, BMI and clot risk factors, smoking over 35 |
| Progestogen-only pill | ~7% | Narrow window for some formulations — 3 or 12 hours depending on type |
| Condoms | ~13% | The only method that also reduces STI transmission |
| Fertility awareness | 2-23% depending on method and rigour | Requires daily measurement and abstinence discipline |

Typical-use failure is the honest number: it includes the missed pills and the late injections that real life produces. Perfect-use figures are much lower and describe almost nobody.

**Missed pills**: for a combined pill, one missed dose is taken as soon as remembered even if that means two in a day. Two or more missed in the first week, with unprotected sex, needs emergency contraception plus seven days of additional protection. Vomiting within 2-3 hours, severe diarrhoea, and CYP3A4-inducing drugs (St John's wort, some antiepileptics, rifampicin) all reduce absorption or level — treat as missed pills.

## Emergency Contraception — The Clock

| Option | Window | Effectiveness note |
|---|---|---|
| Copper IUD | Up to 120 h after intercourse, or up to 5 days after the earliest estimated ovulation | The most effective by a wide margin, and it continues as contraception |
| Ulipristal acetate | Up to 120 h | More effective than levonorgestrel closer to ovulation; delays restarting hormonal contraception by 5 days |
| Levonorgestrel | Up to 72 h, sooner is better | Reduced effectiveness at higher body weight; a doubled dose is sometimes advised |

None of them terminates an established pregnancy, and none is a substitute for ongoing contraception. Ask about the timing of the last period, because it changes which is preferred.

## Pregnancy

- **Preconception**: folic acid 400 µg daily from before conception to 12 weeks, and 5 mg daily where there is diabetes, BMI ≥30, epilepsy medication, coeliac disease, or a previous neural tube defect. Review every medicine for pregnancy safety before, not after.
- **Early red flags — same-day**: bleeding with pain, one-sided pelvic pain with shoulder-tip pain or fainting (ectopic pregnancy, which is a surgical emergency), severe persistent vomiting with no fluids kept down.
- **After 20 weeks — same-day maternity assessment**: severe headache with visual change, upper-abdominal pain, sudden swelling of face or hands, blood pressure ≥140/90 (pre-eclampsia), any bleeding, reduced or changed fetal movements, fluid loss, contractions before 37 weeks.
- Reduced fetal movements are never "wait until morning". There is no safe home test, including cold drinks and lying down.
- **Postpartum red flags**: heavy bleeding soaking a pad an hour, fever, a hot painful calf, breathlessness or chest pain, severe headache, and mood symptoms that do not lift after two weeks (postnatal depression is common, treatable, and screened with the same instruments as `mental-health.md`).

## Menopause

- Diagnosis is clinical over 45: irregular then absent periods for 12 months, with vasomotor symptoms. Blood tests are unreliable in that age band and are used mainly under 45.
- Perimenopause can run for years before periods stop, and mood, sleep and cognitive symptoms often precede the hot flushes — they are frequently treated as primary anxiety or depression instead.
- HRT: the absolute risks that dominated headlines are small for most women starting under 60 or within 10 years of the last period, and the benefit on vasomotor symptoms and bone is real. Route of delivery matters — transdermal oestrogen does not carry the oral clot risk. Personal history of breast cancer, clot or stroke changes the calculus entirely, so the decision belongs with a clinician who has the full history.
- Vaginal oestrogen for genitourinary symptoms is a separate, low-systemic-exposure treatment and is usually appropriate even for those who cannot take systemic HRT.
- Contraception is still needed: 2 years after the last period under 50, 1 year over 50.

## Sexual Health

| Test or action | Window |
|---|---|
| HIV post-exposure prophylaxis | Start within 72 h, ideally within 24 h — this is an emergency-department or sexual-health-clinic call today |
| HIV 4th-generation test | Conclusive at 45 days after exposure |
| Chlamydia and gonorrhoea NAAT | 2 weeks after exposure |
| Syphilis | Up to 12 weeks for a conclusive result |
| Hepatitis B and C | 12 weeks |

- Symptoms that need same-week testing: discharge, ulcers, painful urination, pelvic pain, rash, testicular pain (torsion first if acute and severe — `symptoms.md`).
- Partner notification is part of treatment, not a courtesy; clinics can do it anonymously.
- PrEP exists and is a clinic conversation for anyone with ongoing risk.

## Men's Health, Because It Gets Skipped

- **Testicular self-examination** monthly after a warm shower: any hard painless lump is a same-week referral. Testicular cancer is the commonest solid cancer in men aged 15-40 and is highly curable when caught early.
- **Erectile dysfunction is a vascular symptom** before it is anything else: it precedes cardiac events by an average of a few years and warrants a cardiovascular risk assessment, not just a prescription.
- Lower urinary tract symptoms over 50 warrant assessment, and a discussion about PSA as a decision rather than a routine test (`prevention.md`).

## Where This Goes

**Write in the same turn** (`memory-template.md`): the contraceptive method with its start date → `## Medications` in `~/Clawic/data/health/profile.md`, updated in place; pregnancy or breastfeeding status → `## Conditions` with its date, because it gates every drug answer until it changes; the last menstrual period when it is relevant to a current question → `## Measurements`; screening dates (cervical, STI) → `## Screenings` with the next due date mirrored into `## Due`. A contraception or HRT decision with its reasoning and what was ruled out is an artifact: `~/Clawic/data/doctor/artifacts/<kebab-name>.md`, with its `## Boxes` line the same turn. An implant or IUD expiry date is a `## Due` row — it is the one that is otherwise remembered five years late.
