# Emirati Arabic Skill | مهارة اللهجة الإماراتية

**By Binablan · v0.2.1-rc.1 · Experimental ClawHub distribution · MIT-0 (original project material)**

مهارة للمحادثة وفهم المقصود وكتابة النصوص ومراجعتها بالإماراتية، مع تخصص أبوظبي عند اختياره. تنجز الطلب بدل شرح تعبيرات المستخدم تلقائيًا؛ المعجم مرجع مساعد فقط. قواعدها محدودة وأمثلتها قابلة للمراجعة، وليست بديلًا عن مراجعة متحدثي اللهجة.

A small, source-grounded skill for conversation, contextual intent, writing, and revision in Emirati Arabic. It prioritizes task completion and meaning preservation, avoids mechanical word substitutions, and separates source evidence from original examples.

## Experimental candidate | مرشح الإصدار التجريبي

`0.2.1-rc.1` is a new prerelease version, separate from `0.2.0` on `main`. It carries the prior conversation-first behavior and all source/owner examples forward, with an additional clarity rule for actors, actions, and potentially ambiguous kinship/body-part references in spoken scripts. It does not ban regional spellings or include a private test answer as a template.

Publication of this experimental distribution is authorized by the maintainer. The ClawHub copy grants MIT-0 for original project material; the GitHub release remains MIT. Relative to reviewed GitHub commit `5aa437cd1366b4c4e0407a7d6121cdbec071a9d4`, only licensing and publication-status documentation differ: all behavioral instructions, examples, reference content, code and tests are preserved. Historical review-stage records below remain historical, not current publication restrictions. No main-branch merge or native-speaker certification is implied. Dialect quality remains provisional and open to human review. See [release notes](RELEASE_NOTES.md) and [distribution policy](DISTRIBUTION.md).

## Historical behavior review — intent-first-review-2

`intent-first-review-2` adds general guidance for speakable collocations, clearly self-directed humor, practical drafts without unsupported personal feelings/motives/excuses, temporary language changes, and locally scoped user corrections. It does not install known test answers as templates.

Historical r2 checks: 49 offline tests. The new ordinary-discovery comparison collected 44 actual replies: 12 new standalone cases, one six-turn resumed dialogue, and four known-input regressions in each of two conditions. Both conditions received identical user turns; the candidate used no `-s`, forced skill-reading request, or technical activation turn. Actual tool records showed the revised skill and Abu Dhabi guide loaded in all 17 candidate sessions; the baseline lacked the target skill. A separate post-hoc ambiguity probe collected two more replies and is not folded into the frozen comparison. The full unchanged outputs, assessments, limitations, and all attempts belong in the local evidence bundle, not the installed skill. These observations are not native-speaker certification or causal proof of improvement.

### Previous review — retained historical record

`intent-first-review-1` modifies the instructions in `SKILL.md` itself: answer ordinary conversation, write requested text, rewrite when asked, and explain meaning only when requested or necessary. It preserves general Emirati as the default, the opt-in Abu Dhabi profile, existing source rules, and owner-authorized quotations.

- [Behavior examples and boundaries](references/conversation-behavior.md)
- [Isolated loading and real conversation evaluation](references/conversation-evaluation.md)

The `main` URL below remains the previously published version, **not this candidate**. A working-tree edit is not proof that any running assistant loaded it. Use a separate test profile and verify the exact branch-copy hashes and actual `skill_view` results; do not replace another installed skill or change global settings implicitly.

Local verification for the previous review: 43 offline tests passed (the prior baseline was 40). A real, limited A/B run collected 34 replies: 14 cases / 17 user turns per condition, including a four-turn resumed conversation. Both conditions used `gpt-6-astra` via `openai-codex`, requested medium reasoning, and disabled persistent memory; temperature and seed were not explicitly set. The comparison condition had no Emirati skill; the treatment's persisted launch policy contained the exact modified `SKILL.md` text on every evaluated turn. An additional activation session returned that file and two references via real `skill_view` calls. Full inputs, raw replies, loading evidence, and judgments are kept in the separate local review bundle, not installed as teaching examples. This is not an independent native-speaker assessment or a statistical claim of improvement.

## v0.2.0 — تخصص أبوظبي وتصحيحات صاحب المهارة

الإماراتية العامة باقية افتراضياً؛ يُفعّل تخصص أبوظبي عند طلبه فقط. أُضيف معجم محدود مع إحالة لكل مدخل، وقواعد للنطق والسياق، ومحادثات وتحويلات مؤلفة، وضوابط تمنع التصنّع، وفحوص للمعنى السطحي والتوثيق.

- [دليل أبوظبي](references/abu-dhabi.md) · [المعجم المنظّم](references/abu-dhabi-lexicon.json)
- [المعجم المقروء والمحادثات والتحويلات](references/abu-dhabi-examples.md)
- [المصادر وحدودها](references/abu-dhabi-sources.md) · [التقييم](references/evaluation.md)
- [حالات التقييم](tests/fixtures/abu_dhabi_cases.json) · [أداة الفحص](scripts/check_conversions.py)

الموثّق في مصدر عن أبوظبي ليس بالضرورة حصرياً لها. شواهد Qafisheh تاريخية، وشواهد Habash et al. موسومة بأبوظبي في دراسة كتابة ونطق؛ لا يثبت أي منهما وحده طبيعية محادثة معاصرة عند كل المتحدثين. الأمثلة تطبيقات أصلية غير معتمدة محلياً.

**Historical v0.2.0 GitHub source update, not a registry publication or GitHub Release.** The `main` installation URL below installs that branch, not this candidate. The version number does not imply independent native-speaker certification.

### أمثلة صاحب المهارة المأذون بنشرها

[الأمثلة والسياقات والبدائل](references/owner-examples.md) · [النسخة المنظّمة](references/owner-examples.json) · [حالات تقييم المعنى والسياق](tests/fixtures/owner_context_cases.json).

نُقلت أمثلة Binablan بنفس كتابته وبإذنه، مع فصلها عن المصادر القديمة. تمثل اختياراته في السياقات المحددة، لا كل أهل أبوظبي. لا تُوحّد «مش» و«مب» آلياً، ولا تُخلط جهة الإخبار في «بخبرك» و«خبرنيه»، ولا «باجر» مع «عقب باجر» أو «ورا باجر». بدائل السؤال عن الوصول تختلف بحسب الموقف، و«من الصبح نترياك» قد تحمل عتاباً خفيفاً بحسب النبرة. الاختبارات تسمح ببدائل مؤلفة تحفظ القيود المحددة؛ ليست فرضاً لجملة واحدة أو حكماً دلالياً شاملاً.

## Install in Hermes | التثبيت

Prerequisite: an installed Hermes version supporting direct `SKILL.md` URL installation. Review the source before installing. Test in a **new isolated profile** so an existing personal skill is not overwritten:

```sh
hermes profile create emirati-community-review --no-skills --no-alias
hermes -p emirati-community-review skills install https://raw.githubusercontent.com/Binablan/emirati-arabic/work/v0.2.0-abu-dhabi/SKILL.md
hermes -p emirati-community-review skills list
hermes -p emirati-community-review
```

The branch name predates the candidate version. Check the installed `SKILL.md` says `version: 0.2.1-rc.1` and `behavior_revision: intent-first-rc-1`. This is a mutable review-branch URL, not a final-release tag. For a fixed snapshot, replace the branch segment with the full commit SHA shown on the PR. Installation is subject to Hermes' normal safety scan; do not bypass a blocked verdict with `--force`. Choose another fresh profile name if this one exists.

To deliberately install the older `main` source instead (not the candidate):

```sh
hermes skills install https://raw.githubusercontent.com/Binablan/emirati-arabic/main/SKILL.md
```

The public source ZIP includes offline tests and build tooling for contributors; URL installation loads the skill and its linked runtime references, not private evaluation logs.

For a compatible agent that supports `SKILL.md`, download the repository and follow that agent's skill-installation instructions. Compatibility with every agent has not been tested.

## Usage | الاستخدام

الإماراتية العامة هي الافتراض. لاختيار أبوظبي في المحادثة الحالية، قل «خل سوالفنا بالظبياني». يبقى الاختيار إلى أن تغيّره؛ طلب رسالة إنجليزية مؤقتة لا يلغي اختيار المحادثة. لا يُفرض الاختيار على جلسات أخرى أو نصوص مقتبسة أو طلب بلغة مختلفة.

For explicit verification in a fresh chat, ask the assistant to load `emirati-arabic` and read `references/abu-dhabi.md`; inspect the actual tool result and version, not only its claim of loading. A natural dialect request does not guarantee discovery in every model/session.

Ask your assistant, for example:

- «كلمني ظبياني؛ اليوم خلصت الشغل بدري.»
- «اكتب لي رسالة قصيرة أعتذر فيها عن الموعد، بدون ما تخترع سبب.»

- «استخدم مهارة emirati-arabic وراجع هالنص، بدون ما تغيّر معناه.»
- «حوّل النص إلى كلام إماراتي بسيط، بدون مبالغة أو حشو أمثال.»
- «اشرح القاعدة الموجودة في المهارة، واذكر مصدرها.»
- «استخدم تخصص أبوظبي وحوّل هالنص لمحادثة بسيطة؛ حافظ على الأسماء والوقت، ولا تضف نداءات.»

Original provisional example — not a source quotation:

> سوف أكتب لك الشرح. → بكتب لك الشرح.

The skill is guidance loaded by the assistant, not a new model, a voice, or an automatic guarantee of accent accuracy.

## Preserved v0.1.0 foundation

- Selected future, negation, and demonstrative constructions.
- A safeguard against indiscriminate ج → ي substitution.
- Meaning-preserving rewriting and restrained dialect markers.
- Source attribution, uncertainty, and private-versus-public correction handling.

## Reference and limitations

The initial reference is **«المتوصّف — أمثال وحكم من الإمارات»**, collected and researched by **عبدالله حمدان عبدالله أحمد بن دلموك**, published by **مركز حمدان بن محمد لإحياء التراث**, second edition, 2021 as stated in the examined copy.

The initial pronunciation/spelling rules were checked against images of printed pages **49 and 52**. This is not a claim that the whole book was reviewed. See [source notes](references/sources.md).

**The PDF, page images, bulk extracted text, private conversations, private calibration reference, historical review archives/logs, and local-machine files are not included.** Only the explicitly publication-authorized owner examples are added; other private preferences remain excluded. This project is independent and does not claim endorsement by the referenced authors, publishers, or Nous Research.

## Contribute | المساهمة

Corrections and additional well-supported examples are welcome. Explain the context and, where relevant, the regional variety. Separate a personal preference from a broader claim. Do not upload private conversations or copyrighted books. See [CONTRIBUTING.md](CONTRIBUTING.md).

## Tests

From the repository directory, with Python 3.10 or later:

```sh
python -B -m unittest discover -s tests -v
python -B scripts/verification_probes.py --project .
python -B scripts/build_distribution.py --output-dir ../emirati-release-files
```

The build uses an explicit file allowlist and emits a ZIP with a per-file SHA-256 manifest and `SHA256SUMS` outside the repository. Keep the original private review evidence separate; do not attach it to a public PR or release.

These tests check structure, source metadata, publication hygiene, and the conversion checker with positive/negative authored cases. They do not prove linguistic fluency, full semantic equivalence, or universal naturalness. To check actual model outputs, use the separate workflow in [evaluation.md](references/evaluation.md); do not present reference-fixture self-tests as model evaluation.

## License

Original instructions, documentation, code, and newly authored examples in this ClawHub distribution are provided under [MIT No Attribution (MIT-0)](LICENSE), copyright Binablan, with the rights holder's authorization. The GitHub source and the GitHub installation commands above remain under MIT. The referenced books and any third-party source material retain their own rights; this distribution does not license or redistribute those books. See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
