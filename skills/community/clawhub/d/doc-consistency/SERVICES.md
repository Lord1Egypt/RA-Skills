# Long-Document Consistency Engineering — Services

**Contact: [HEFANGSHENG@gmail.com](mailto:HEFANGSHENG@gmail.com)** · open an [issue](https://github.com/dongsheng123132/doc-consistency/issues) · [u-king.org](https://u-king.org)

The tool in this repository is free and runs offline. This page is about the work
that a tool cannot do.

---

## What we actually do

We do not write documents. Anyone can write. We handle what comes after:
turning *"is this document consistent with itself?"* into something you can
**re-check at the push of a button**.

Every engagement delivers three things:

1. **A findings list** — location, type, why it is wrong, suggested fix. Exportable
   to CSV/Excel so you can assign items to people.
2. **The corrected file** — original formatting intact. Headers, footers,
   auto-numbering, styles, tracked-changes history preserved.
3. **A re-check you can run yourself** — the command, the expected exit code, and
   the acceptance threshold.

That third item is the difference. Not *"we checked it, it's fine"* — but
**"run it yourself: 137 findings down to 0."** That is an acceptance criterion a
machine can adjudicate, so it can go in the contract and there is nothing to argue about.

---

## 1. Proposal & bid compliance (GovCon, RFP/RFQ/ITT responses)

**Who buys:** proposal managers, capture teams, bid consultancies, systems
integrators, anyone responding to a public solicitation.

**Why it hurts:** compliance failure is a cliff, not a slope. Miss one "shall"
and you are non-responsive. The evaluator never sees your technical brilliance.
And proposals are always written under deadline, by several people, at night.

**What we deliver:**

- **Compliance matrix / requirements traceability matrix (RTM)** — every
  *shall / must / will* in Sections L and M (or the equivalent) decomposed into
  discrete requirements, mapped against your response, scored
  **responsive / non-responsive / partially responsive**, with the page and
  paragraph where each response lives.
- **Stale-content sweep** — last cycle's program name, agency, dates, dollar
  figures, and incumbent references, all surfaced. This one catches somebody every year.
- **Cross-document number reconciliation** — technical volume vs. cost volume vs.
  representations vs. past-performance attachments.
- **Attachment, exhibit, and page-numbering audit** against the TOC.
- **Template normalization** — heading levels, numbering styles, and fonts
  conformed to the solicitation's stated format requirements.

**We will not:** write your past performance, fabricate qualifications, or touch
anything resembling bid rigging or collusion. No exceptions.

**We will not take it on** if you are inside 24 hours of submission and the
document does not exist yet — we check finished drafts, we do not write them for you.

---

## 2. Academic & educational publishing

**Who buys:** publishers and editorial desks, textbook author teams, university
presses, corporate training and courseware departments.

**Why it hurts:** a textbook is written by several people and assembled by the
one with the least time. What kills the schedule is never the content:

- figure, table, and equation numbers collide or skip after the merge, and the
  body says "see Figure 3-12" pointing at a figure that no longer exists;
- every author used a different chapter skeleton — some have "Learning
  Objectives," some don't;
- three authors, three names for the same concept;
- artwork arrives at wildly different resolutions and half of it prints muddy.

**What we deliver:**

- **Cross-reference & numbering audit** across figures, tables, equations,
  appendices, and inter-chapter references — every finding located.
- **Chapter skeleton reconciliation** against your approved model chapter:
  which sections are missing, extra, or out of order.
- **Figure specification report** — actual pixel dimensions, color mode, and role
  of every image; which ones fall below print threshold; which need redrawing.
- **Terminology table** — every same-concept-different-name cluster in the book,
  for the editor-in-chief to rule on.
- **Multi-file merge** into one chapter or one book, with a diff report showing
  whose paragraphs did not make it in.
- Optional: **redrawing non-conforming schematics as vector art** (`.dxf` / `.svg`).

**We will not take it on** if there is a single author, a single draft, and no
approved model chapter — with no definition of "correct," there is nothing to check against.

---

## 3. Fiction, serial publishing & IP continuity

**Who buys:** publishers' fiction editors, IP licensors, adaptation studios
(screen, audio, comics), literary agencies, serial-fiction studios.

**Why it hurts:** the enemy of a long series is the author's own memory. By
chapter 200 nobody remembers what colour that minor character's eyes were in
chapter 40. **Readers remember. And they will list every instance in public.**

**What we deliver:**

- **A series bible extracted from the prose itself** — characters, places, items,
  rules, timeline. Not the one you maintain by hand and forget to update; one
  that grew out of the actual text.
- **Continuity findings** — "chapter X says A, chapter Y says B," with both quotes.
- **Pre-writing briefs** — before the next chapter is drafted, push the facts it
  will touch in front of the writer (human or AI), so the error never gets written.
- **Pre-adaptation audit** — surface the continuity holes before a screen, audio,
  or comics team hits them and bills you for the rework.

**We will not take it on** if there is only an outline and no prose — without
prose there are no facts to reconcile.

---

## 4. Technical documentation & translation QA

**Who buys:** documentation teams, localization vendors, standards bodies.

**What we deliver:**

- **Terminology governance** — enforce an approved glossary across a whole
  documentation set; report every violation with location.
- **Structural alignment** between source and translated documents: chapter,
  section, numbering, and figure/table correspondence — so you can catch a dropped
  paragraph or a mistranslated figure **without reading the target language**.
- **Release-to-release consistency** — what changed, what silently disappeared.

For localization vendors this doubles as a deliverable: the report is something
you can hand your client, and it is leverage in a rate negotiation.

---

## 5. Contract sets, policy manuals, compliance libraries

> ⚠️ **Boundary, stated up front: we do not give legal advice and we make no legal
> judgments.** Whether a clause is enforceable, how risk is allocated, whether an
> arrangement is compliant — that is work for a licensed attorney. We do the
> **formal** consistency layer only.

**What we deliver:** defined-term drift between master agreement and annexes,
dangling clause cross-references, numbering integrity across a template library,
and version-to-version diff reporting.

---

## How we engage

**Every engagement starts with a sample run** on one chapter or one file —
free or at nominal cost. You get the real findings list before you commit anything.
You then judge for yourself: are these real problems? How many would your own team
have caught?

**If it turns up nothing real, we will say so** — that job should not have cost you money.

Send a representative chapter or the previous version (redacted is fine) to
**[HEFANGSHENG@gmail.com](mailto:HEFANGSHENG@gmail.com)**. You get an answer within
24 hours on whether we can take it and roughly what it costs.

Working languages: **English and Chinese**. Time zone UTC+8, but deadline-driven
work is normal here — say when you need it.

---

## What we will never promise

- That your bid will win, or pass evaluation.
- That a document will clear any particular review, audit, or plagiarism check.
- That the content is *correct*. We verify that a document **agrees with itself**.
  Those are different claims and we will not blur them.
