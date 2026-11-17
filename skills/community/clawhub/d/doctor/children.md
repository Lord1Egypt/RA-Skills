# Children — Age-Banded Thresholds

Children compensate well and then decompensate suddenly, which is why paediatric triage runs on age bands and observable behaviour rather than on how bad the symptom sounds.

**Before answering**, read the dependent's health file if one exists — `~/Clawic/data/health/<child-name>.md`, indexed in `## Boxes` — for weight, conditions, allergies, medicines and vaccine status. **Weight is not optional here**: every paediatric dose is per kilogram, and the last recorded weight is the input.

## Fever By Age — The Hard Lines

| Age | Threshold | Action |
|---|---|---|
| Under 3 months | Any temperature ≥38.0 °C (100.4 °F) | Emergency assessment. No home observation, no antipyretic-and-wait — the examination is the point |
| 3-6 months | ≥39.0 °C (102.2 °F) | Same-day medical assessment |
| Over 6 months | The number alone does not decide | Assess by the traffic-light features below; behaviour outranks the thermometer |

Any age: fever with a non-blanching rash, neck stiffness, a bulging fontanelle, a seizure, a fever lasting more than 5 days, or a child who is immunosuppressed or has no spleen → emergency.

## Traffic-Light Features (NICE)

| Green — low risk | Amber — same-day review | Red — emergency now |
|---|---|---|
| Normal colour, responds normally, content, strong cry, moist mucous membranes, normal skin | Pallor, reduced response, less activity, dry mouth, poor feeding, reduced urine output, rigors, fever ≥5 days | Pale/mottled/ashen/blue, no response to social cues, unrousable, weak or high-pitched continuous cry, grunting, marked chest recession, reduced skin turgor, bulging fontanelle, non-blanching rash |

Breathing rate is the most useful and most ignored sign. Count it for a full minute with the chest exposed: over 60/min in an infant under 1, over 50 in a 1-5 year old, over 40 above 5 is abnormal. Grunting, nasal flaring, head bobbing and drawing-in below the ribs are work-of-breathing signs that matter more than the rate itself.

## Dehydration

- Count wet nappies or trips to the toilet: **fewer than 4 wet nappies in 24 hours** in an infant, or no urine for 8-12 hours in an older child, is the observable that decides.
- Other signs: dry mouth, no tears when crying, sunken eyes, sunken fontanelle, lethargy, cold mottled hands and feet, skin that stays tented.
- Treatment is oral rehydration solution in small frequent amounts — 5 ml every few minutes beats a glass that comes straight back. Sports drinks, fruit juice and fizzy drinks have the wrong osmolarity and can worsen diarrhoea.
- Vomiting everything for more than a few hours, blood in stool, bile-stained (green) vomit, or a distended abdomen → emergency.

## Dosing By Weight

| Drug | Paediatric dose | Ceiling |
|---|---|---|
| Paracetamol | 15 mg/kg every 4-6 h | Maximum 4 doses (60 mg/kg) in 24 h |
| Ibuprofen | 10 mg/kg every 6-8 h, with food | Maximum 30 mg/kg in 24 h; not under 3 months, not in dehydration or chickenpox |

Worked example: a 14 kg three-year-old takes 210 mg of paracetamol per dose (14 × 15), which is 8.4 ml of the 125 mg/5 ml suspension. Two concentrations exist on shelves — always read the strength on the bottle rather than reusing a remembered volume, and dose with the supplied syringe, never a kitchen spoon.

**Never give aspirin to under-16s** for fever or pain (Reye's syndrome). Codeine is contraindicated under 12 and after tonsillectomy. Honey is unsafe under 1 year (botulism); most over-the-counter cough remedies are ineffective under 6 and are not recommended.

## Rashes Worth Naming

- **Non-blanching** with fever → emergency, no exceptions. Test with a glass tumbler pressed against the skin.
- **Chickenpox**: crops of blisters at different stages; concern if lesions become hot, red and painful (bacterial superinfection) or the child is immunosuppressed or a newborn.
- **Hand, foot and mouth**: mouth ulcers plus spots on palms and soles; the risk is not drinking, not the rash.
- **Measles**: fever, cough, coryza, conjunctivitis, then a rash spreading from the face; check vaccination status and notify — it is not historical.
- **Slapped-cheek**: usually mild, but relevant exposure for pregnant contacts and for children with haemolytic anaemia.
- **Eczema flare** with weeping, honey-coloured crust → bacterial infection; with grouped punched-out lesions and a sick child → eczema herpeticum, an emergency.

## Breathing Illnesses

- **Croup**: barking cough, hoarse voice, worse at night, stridor when upset. Stridor at rest, drooling or exhaustion → emergency. Steam has no evidence; a single dose of oral steroid from a clinician is what works.
- **Bronchiolitis** (under 2): coughing, wheeze, poor feeding. The admission trigger is feeding under about half of normal, apnoea, marked recession, or oxygen saturation below 92%.
- **Asthma in children**: reliever needed more than every 4 hours, unable to complete a sentence, or no response to the usual rescue plan → emergency. Every child with asthma should have a written action plan (`chronic.md`).

## Head Injury In Children

Same-day assessment for: loss of consciousness, more than one vomit, abnormal drowsiness, a fall from over 1 metre or three times their height, a significant mechanism, seizure, any bulging fontanelle, or any child under 1 with a head injury. Under-1s are assessed more readily because the examination is less reliable and the mechanism is often unwitnessed.

## Development And Growth

Red flags that warrant review rather than watchful waiting: not smiling by 3 months · not sitting unsupported by 9 months · not walking by 18 months · no words by 18 months, no two-word phrases by 2 years · loss of any skill previously acquired, at any age · persistent toe-walking, or a strong hand preference before 18 months.

Growth is read as a trend on a centile chart: crossing two centile lines downward, or weight and height diverging, matters far more than being on a low centile consistently.

## Safe Sleep And Prevention

Infants sleep **on their back**, on a firm flat surface, in the parents' room for the first 6 months, with no pillows, bumpers or loose bedding, never on a sofa, and never bed-sharing after alcohol, sedating medicine, smoking, or with a preterm or low-birthweight baby. Room temperature 16-20 °C. Feverish children do not need to be cooled by fanning or tepid sponging; that has been out of guidance for years and causes shivering.

## Where This Goes

**Write in the same turn** (`memory-template.md`): a child's health record lives in the shared health box as its own file — `~/Clawic/data/health/<child-kebab-name>.md`, opening with `# Health — <Name>` and the same headings as `profile.md` (`## Conditions`, `## Allergies`, `## Medications`, `## Vaccines`, `## Measurements`, `## Screenings`) — because `nutrition`, `sleep` and others need the same allergy and weight facts. Its index line goes in `## Boxes` of `~/Clawic/data/doctor/memory.md` with the read condition "read before any question about <Name>", and the child's person row goes in the shared `~/Clawic/data/contacts/contacts.md` with `Role: dependent`. Weight and height go to `## Measurements` in that file with the date, since dosing depends on the most recent one. Episodes go to `~/Clawic/data/doctor/episodes/<year>.md` with the child's name in the row. Immunisation dates go to `## Vaccines`, and the next due one to `## Due`.
