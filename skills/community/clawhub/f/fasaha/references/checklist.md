# Fasaha Checklist — Runnable Quality Gate

The concrete pass to run on any Arabic output after drafting. Run every check, then
report which sections caught problems. Do not skip to "polished" output without running
this.

## Run order

**1. Latin leakage (Section 1)**
- [ ] Every English word outside proper nouns / product names / API identifiers is translated
- [ ] Every list/table row individually checked (a lone untranslated item is a common miss)

**2. Calque / structure (Section 2)**
- [ ] Read Arabic alone: does it read as composed by a native writer, not mirroring English?
- [ ] Sentences that share a subject or cause-effect merged with connectives (فـ، إذ، حيث، مما...)
- [ ] Arabic aggregates don't fall exactly where English paragraph breaks fell

**3. Word choice / terminology (Section 3)**
- [ ] Domain-standard term used, not a generic dictionary rendering (`تُدار` not `يتم تشغيله` for institutions)
- [ ] `terminology.md` consulted for known terms

**4. Morphology & agreement (Section 4)**
- [ ] Gender agreement verified (noun + verb + adjective + pronoun)
- [ ] Broken plurals correct
- [ ] Obligatory prepositions present (`تخرج من الجامعة`)
- [ ] Definite articles carried over from English's lack of them
- [ ] Every pronoun has a surviving antecedent

**5. Punctuation / hamza / numbers (Section 5)**
- [ ] Arabic punctuation (، ؛ ؟) not Latin ( , ; ?)
- [ ] Hamza wasl vs qat' and medial seat correct (see qalb-spelling-rules.md if unsure)
- [ ] Number numeral system + grouping consistent

**6. Dialect leakage (Section 6)**
- [ ] No dialectal words in MSA target
- [ ] If passage >~⅓ dialectal, FLAG it — do not partial-fix

**7. LLM-specific gaps (Section 7)**
- [ ] Not over-relying on QALB's 2013 spelling-heavy error weights; Sections 1-3 weighted highest
- [ ] `llm-failure-log.md` checked for matching known pattern

**R. Register (voice-profile.md)**
- [ ] Matching register profile applied (MSA vs Darija, formality, tone, terminology)
- [ ] If no profile fits, ask which register to use

## Output

Report in this shape:
- sections that flagged problems (list)
- key corrections made (source → bad → good)
- any new pattern added to `llm-failure-log.md` or new term to `terminology.md`
