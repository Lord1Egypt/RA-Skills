# Output Modes

## 1. Supported delivery forms

The skill should support:

- markdown summary
- HTML landing page
- Vercel web deployment
- PDF export
- both web and PDF when requested

---

## 2. Delivery rule

At the final delivery stage, ask the user which output they want:

- Vercel web page
- PDF
- both

Do not auto-deploy to Vercel without asking first at the delivery step.

---

## 3. Progress feedback rule

At each major workflow step, report:

- what step is currently running
- what step just completed
- what step is next

For long runs, include intermediate updates when helpful.

---

## 4. Report generation rule

When rebuilding a report:

- rewrite the landing page to match the latest benchmark snapshot
- do not append patch fragments to stale HTML
- keep estimated values visibly marked
- keep the default report section order consistent:
  1. ranking table
  2. cost table
  3. executive summary
  4. overall assessment
  5. recommended model selection
  6. detailed answers

## 5. Report language rule

- Default the report language to the user's current conversation language.
- Only switch to another language when the user explicitly asks for it.
- "Multilingual support" means the renderer/output pipeline can display multiple languages correctly; it does not mean the skill should randomly change report language.

## 6. PDF multilingual rendering rule

- PDF outputs should use Unicode-capable fonts.
- Vietnamese, Chinese, and mixed-language text should render correctly without mojibake or missing glyphs.
