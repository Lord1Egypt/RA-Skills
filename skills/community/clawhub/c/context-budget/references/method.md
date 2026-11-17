# Method and measurements

The examples below came from one local BPE-tokenizer measurement. Exact token
counts are model-specific; repeat the test with the production model before
making a cost claim. The observed direction is useful as a hypothesis, not a
universal tokenizer guarantee.

## Abbreviation did not save tokens in this sample

| long | tokens | short | tokens | result |
|---|---|---|---|---|
| configuration | 1 | config | 1 | no saving |
| infrastructure | 1 | infra | 1 | no saving |
| documentation | 1 | docs | 1 | no saving |
| verification | 1 | verify | 1 | no saving |
| repository | 1 | repo | 1 | no saving |
| environment | 1 | env | 1 | no saving |
| because | 1 | `b/c` | 3 | worse |
| without | 1 | `w/o` | 3 | worse |
| with | 1 | `w/` | 2 | worse |

Zero of the nine shown pairs saved a token; three cost more. Frequent English
words may be single vocabulary entries while unusual abbreviations are assembled
from fragments. Measure the target tokenizer rather than assuming abbreviations
reduce cost.

## Techniques measured in one workspace

| Technique | chars | tokens |
|---|---|---|
| repeated-path list → table, prefix stated once | −37% | −29% |
| merge sections answering one question, cut filler | −34% | −26% |
| move task-specific sections to verified on-demand loading | −26% | −31% |

Relocation can change instruction availability and precedence. Apply it only
after classifying the rule and verifying its loader and trigger.

## Worked result

One workspace with six always-loaded files changed from 47,173 to 27,804
characters and from 10,681 to 6,493 tokens. A 68-marker checklist reported no
missing text, but marker presence alone does not prove semantic or precedence
equivalence; prompt-assurance regressions are also required.

## Failure patterns worth checking

- **Pointer plus paraphrase.** A section names its canonical file and then
  restates it.
- **Silent truncation.** A file over the per-file limit loses its tail without
  a task-level error.
- **Merged files nobody re-read.** Folding one bootstrap file into another can
  push the combined file past its limit.
- **Three-way overlap.** Communication style can be repeated in operating,
  temperament, and audience files.
- **Stale pointers after a move.** Verify every moved filename and trigger.
- **Precedence regression.** A rule moved on demand may no longer be loaded when
  an adversarial or safety-sensitive request arrives.
