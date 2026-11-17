# FAQ pages and FAQPage markup

Reference for the FAQ Schema Content Builder skill. Every limit and rule below is a US-facing constraint the workflow has to respect.

## How the markup has to line up

- The FAQPage JSON-LD holds a mainEntity array of Question objects.
- Each Question carries a name and an acceptedAnswer with a text field.
- The answer text in the markup has to match the visible answer, word for word.
- One FAQPage block per page; do not stack several markup blocks on one URL.

## What Google does with FAQ markup

- FAQ rich results are limited to well-known authoritative government and health sites.
- Google requires the marked-up content to be visible on the page.
- Google deprecated the HowTo rich result in September 2023.

## Getting the questions people actually ask

- Pull questions from support tickets, live chat transcripts and on-site search terms.
- Deduplicate near-identical questions before the page is written.
- Answer the question on the page before marking it up; markup never replaces an answer.
