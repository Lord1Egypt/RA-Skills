# Search Policy

## Search Scope

Use live search only for dynamic information that may change and is useful for the patient's next step:

- official hospital access pages for foreign or self-pay patients
- official department pages
- official hospital appointment or contact pages
- official mainland-China visa and entry-policy pages
- high-level transportation planning
- accommodation planning near the shortlisted city or hospital area

## Do Not Search

- Fudan rankings themselves
- hospital reputation claims that are already covered by the bundled ranking baseline
- exact pricing, waiting-time guarantees, treatment success rates, or admission promises
- informal doctor reviews or forum claims

## Source Priority

Prefer sources in this order:

1. official hospital websites
2. official university or affiliated medical center pages
3. official government or embassy pages
4. major public transport operators or airport sources for route sanity checks

Use lower-confidence sources only if the answer explicitly labels them as provisional. If you cannot verify a claim cleanly, do not smooth the wording.

## Visa-Specific Source Priority

For mainland-China visa questions, use this stricter order instead of the generic list above:

1. PRC State Council or official government policy pages
2. Ministry of Foreign Affairs visa-free or consular pages
3. National Immigration Administration transit or border-entry pages
4. visa-center or embassy/consulate pages only for application flow after eligibility is resolved

Do not use visa-center pages as the first source for deciding whether a user is already visa-free.

## Failure Handling

- If a hospital's international access path is unclear, write `Needs confirmation`.
- If visa eligibility cannot be confirmed across nationality, passport type, purpose, stay duration, and policy validity window, return `No sufficient official confirmation found`.
- If the question is transit-related and the onward itinerary, port, or region rule is unclear, return `No sufficient official confirmation found`.
- If a regular visa route is needed, then point the user to the visa-center or embassy/consulate page for category and materials.
- If the hospital website does not clearly support teleconsult or foreign-patient intake, do not imply that it does.
