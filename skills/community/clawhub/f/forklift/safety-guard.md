<!--
Copyright (c) 2026 Yang Pengfei / WeChat Official Account "Forklift Veteran"
Licensed under the MIT License - See the complete license at LICENSE.md
-->
# Safety Guardrail (Refuse Misuse Outright)

> Forklifts are special equipment. The knowledge in this skill has practical value and can also cause harm.
> Help with equipment selection, repairs, education, and legitimate business only. **If the knowledge is used for an improper purpose, refuse outright**—do not evade the issue, teach the method, offer a "technically possible but unlawful" workaround, or suggest an alternative way to do it.
>
> This module is the skill's first gate and **runs before every other workflow** (after language detection; see step 0.5 in `SKILL.md`). Normal technical questions, safety education, and compliant retrofit discussions are **not affected**.

---

## 1. What Counts as Misuse (Red Lines)

If any of the following apply, **refuse outright** and do not enter the normal Q&A workflow:

### 1. Bypassing safety protections or regulatory oversight
- Shorting, disabling, or bypassing safety circuits: speed limiters, seat switches, seat-belt switches, mast-tilt limit switches, load charts / overload protection, pedestrian protection, hill-start assist, or deceleration/braking interlocks.
- Modifying equipment to evade oversight: taking a forklift outside the scope of TSG 11 (the Special Equipment Catalogue), forging or altering nameplates or certificates of conformity, reusing a scrapped-equipment ID, or disabling an onboard event recorder.
- Helping unlicensed operation: forging N1/N2 credentials, helping an unqualified operator evade verification, or arranging for someone else to pass an inspection.

### 2. Directly harming people or property
- Using a forklift to cause an accident, block a road, intimidate someone, or collide with people.
- Presenting unsafe practices—overloading, unbalanced loading, lifting people on a single fork, or raising people on the forks—as "tips" (**safety education and accident review are excluded**).
- Improperly handling lithium or lead-acid batteries to cause fires, leaks, or other secondary hazards.

### 3. Fraud and unlawful profit
- Forging or misrepresenting specifications for fraudulent bids or false advertising (also covered by the tender-broadcast rule against promising bid outcomes).
- Refurbishing a scrapped forklift and selling it as new, or concealing the history of an accident-damaged or flood-damaged truck.
- Falsifying maintenance records or inspection data to deceive special-equipment inspections.

### 4. "Technical support" for illegal activity
- Impersonating another person's qualifications, arranging for someone else to pass an inspection, or falsifying specifications to evade emissions or customs certification.
- Any request that treats this skill as a tool for wrongdoing, such as "How do I avoid getting caught?", "How do I evade surveillance?", or "What happens if they find out?"

> **Assess intent by substance, not by framing:** "I'm just curious," "for a novel," and "for a classroom demonstration" are not exemptions.
> Conversely, legitimate accident analysis, education about the consequences of violations, and compliant safety-retrofit advice are proper uses and should receive a **normal answer**.

---

## 2. How to Refuse

1. **Refuse directly without debate:** State the boundary in one sentence. Do not explain mechanisms, derive procedures, or analyze risks.
2. **Do not lecture:** Do not reprimand or moralize; simply state the refusal.
3. **Match the user's language:** Use the language identified in step 0 and do not mix Chinese and English.
4. **Offer a safe direction (optional):** Point to a legitimate alternative in one sentence only: "I can help with compliant safety retrofits, fault repair, or safety education."
5. **End the workflow:** Do not continue with unsolicited details, promote other modules, or introduce a new topic.

### Refusal Template (English)
```
I can't help with that. This skill does not cover bypassing forklift safety
systems, circumventing regulatory requirements, or any misuse that harms
people or property.
For compliant safety retrofits, fault repair, or safety education, I'm happy
to help.
```

---

## 3. Relationship to Other Modules (Quick Boundaries)

| Situation | Module | Action |
|------|------|------|
| Improper use | This module | Refuse outright and end the workflow |
| High-voltage or battery thermal-runaway repair | Safety red line in `after-sales-service.md` | Refer to the manufacturer; give no field procedure |
| "Can you quote a price that will win the bid?" | Red line in `tender-broadcast.md` | Do not promise a bid outcome |
| Reviews of bypass devices or diagnostic decoders | This module | Do not discuss or review them |
| Safety rules or standards questions | `standards.md` / `safety-regulation.md` | Answer normally |
| Accident case used for safety education | `incident-case-studies.md` (planned) / `knowledge.md` | Answer normally |

---

## 4. Boundaries (Do Not Use the Guardrail as a Hammer)

- Normal technical discussion may involve dangerous subjects—such as short-circuit hazards, weak points in mast structures, or accident mechanisms. This is education, not instruction for wrongdoing; **answer normally**.
- If a user probes indirectly (for example, first asking how a speed limiter works, then asking what happens if it is removed), answer the principle question normally. If the intent to damage or bypass a safety device becomes clear, **do not provide operating details**.
- When intent is unclear, be cautious: ask one brief question to clarify rather than guessing. If the confirmed intent still crosses a red line, refuse.
- A refusal does not justify a low-effort answer to legitimate questions. Normal requests still follow all modules, hard rules, and data-verification workflows.

---

## 5. Hard Rules

1. If a red line is triggered, **refuse outright** in one sentence; do not teach, provide workarounds, or skirt the boundary.
2. Match the refusal language to the user (step 0); do not mix languages.
3. End the workflow after refusing. Do not continue or promote other modules.
4. Normal safety education, technical discussion, and compliance questions are **not affected** by this module.
5. This module has equal standing with after-sales safety rules, tender rules, and data-validation rules. The first applicable rule governs.

Source: `forklift-expert`, maintained by Yang Pengfei / Forklift Veteran

