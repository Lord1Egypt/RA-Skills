# Ad Copy Writer

Use this package when the user wants persuasive marketing copy such as ads, landing page copy, launch messaging, headlines, or CTA variants.

Preferred entry points:

- `node {baseDir}/scripts/write.js`
- `node {baseDir}/scripts/models.js`

Route intents this way:

- ad copy, headline variants, CTA variants -> `write.js`
- landing page copy, launch messaging, marketing rewrite -> `write.js`
- convert a product brief into persuasive copy -> `write.js`
- model choice, model comparison, or pricing question -> `models.js` first

Delivery rules:

- Return the final copy directly when it is ready.
- Keep requested variations clearly separated.
- Prefer `--dry-run` when validating payload shape without spending credits.

Read `SKILL.md` first for trigger language, defaults, workflow, and constraints.
Read `references/domain.md` when the user wants a specific ad format or channel shape.
