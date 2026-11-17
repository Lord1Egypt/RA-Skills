# Injuries — Who Needs Imaging, Who Needs Rest

Validated decision rules exist for the common injuries, and they are more accurate than intuition. Using them is how a person avoids both an unnecessary X-ray and a missed fracture.

**Before advising**, read `~/Clawic/data/health/profile.md` for anticoagulants, osteoporosis, diabetes and steroid use — each changes the threshold for imaging or review after an injury that would otherwise be trivial.

## Ankle And Midfoot — Ottawa Ankle Rules

X-ray is indicated if there is pain in the malleolar or midfoot zone **and any one** of:

- Bone tenderness at the posterior edge or tip of the lateral malleolus
- Bone tenderness at the posterior edge or tip of the medial malleolus
- Bone tenderness at the base of the fifth metatarsal (foot injuries)
- Bone tenderness at the navicular (foot injuries)
- Inability to bear weight for four steps both immediately after the injury and at assessment

Sensitivity for clinically significant fracture is close to 100% in adults, and applying the rule cuts ankle X-rays by roughly a third. Bruising, swelling and severe pain are *not* criteria — a badly sprained ankle out-swells many fractures.

## Knee — Ottawa Knee Rules

X-ray if any one of: age 55 or over · isolated tenderness of the patella · tenderness at the head of the fibula · inability to flex to 90° · inability to bear weight for four steps both immediately and at assessment.

Immediate large swelling within the first hour suggests blood in the joint (ligament rupture or fracture) rather than a simple sprain, and is worth review even if the rule is negative.

## Neck — Canadian C-Spine Rule

Immobilise and get assessed if any high-risk factor: age 65 or over · a dangerous mechanism (fall from over 1 metre or five stairs, axial load, high-speed collision, bicycle or motorised recreational vehicle) · paraesthesia in the limbs. Assessment is also needed if the person cannot rotate the neck 45° to each side. Sitting up, walking, delayed onset of pain and a simple rear-end collision are the low-risk features that allow safe range-of-motion testing.

## Head Injury — When A Scan Matters

Same-day emergency assessment after any head injury with: loss of consciousness, amnesia for events, vomiting more than once, a seizure, worsening headache, drowsiness, unequal pupils, clear fluid from nose or ear, focal weakness, a dangerous mechanism, age 65 or over, or **any anticoagulant or antiplatelet drug** — that last one alone is sufficient, because a bleed can be slow and silent.

**Concussion** needs no scan by itself but does need rules:

- Removed from play the same day, always. No return to sport that day, at any age.
- Relative rest 24-48 h, then graded return with about 24 hours at each stage, moving back a stage if symptoms return.
- No alcohol, and no second impact before symptoms have fully cleared — the second one, sustained while still symptomatic, is the dangerous one.
- Symptoms lasting beyond 4 weeks (2 weeks longer than the typical adult recovery) need specialist review, not more rest.

## Sprains And Strains

- POLICE replaced RICE: **P**rotection, **O**ptimal **L**oading, **I**ce, **C**ompression, **E**levation. The change is real — early controlled loading heals soft tissue faster than immobilisation.
- Ice: 15-20 minutes at a time, never directly on skin, and mainly for comfort in the first 48 h. It does not speed healing.
- Return-to-activity test: can they hop or walk normally on it without limping? A limp means it is not ready, whatever the pain score says.
- Persistent inability to bear weight at 48-72 h, or no improvement at all by one week, warrants imaging even when the initial rule was negative.

## Wounds

- Cleaning matters more than dressing choice: irrigate with clean running water under pressure until visibly clean.
- Wounds needing a clinician: gaping edges that will not stay together, deeper than the skin, on the face, over a joint, from a bite, from a crush, contaminated with soil or rust, or with anything embedded. Closure is most effective within about 12-24 hours (longer on the face), so "wait and see" costs the option.
- **Bites**: human and cat bites are high-risk for infection and usually need antibiotics; cat bites puncture deep and look trivial. Any bite over a joint or on a hand is a same-day review.
- Tetanus: boost if the last dose was over 10 years ago for a clean wound, or over 5 years for a dirty or puncture wound. Vaccine dates live in `~/Clawic/data/health/profile.md` under `## Vaccines`.
- Signs of infection at 24-72 h: spreading redness, increasing pain, pus, fever, or red streaking. Draw a line around the redness with a pen and note the time — it converts "does this look worse?" into an observable.

## Fractures And Suspected Fractures

- Deformity, inability to use the limb, point tenderness over bone, or a snap heard at the time — treat as fracture until imaged.
- Splint in the position found; do not attempt to straighten. Elevate, ice over the splint, and keep nil by mouth if surgery seems likely.
- **Compartment syndrome** is the emergency after a fracture or crush: pain out of all proportion, worse on passive stretch, tight swollen compartment, numbness. Pulses are present until very late, so a normal pulse means nothing.
- An older person with a hip injury who cannot weight-bear is a fracture until X-rayed, even after a trivial fall (`older-adults.md`).

## Back And Neck After A Fall

Apply the cauda equina red flags from `symptoms.md` first. In someone over 50, on steroids, or with osteoporosis, a new spinal pain after even minor trauma raises the question of a vertebral compression fracture — worth imaging rather than treating as a strain.

## Where This Goes

**Write it in the same turn** (`memory-template.md`): the injury as an episode row in `~/Clawic/data/doctor/episodes/<year>.md` — mechanism, decision rule applied and its result, imaging done, and the return-to-activity date. A rehabilitation or graded-return plan the user will follow over weeks is an artifact: `~/Clawic/data/doctor/artifacts/<kebab-name>.md` (for example a return-to-sport ladder), with its `## Boxes` line the same turn and, if it has stages with dates, a row in `## Due`. A tetanus booster given goes to `## Vaccines` in `~/Clawic/data/health/profile.md` with its date.
