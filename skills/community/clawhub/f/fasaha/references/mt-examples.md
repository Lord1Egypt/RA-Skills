# Worked Machine Translation Correction Examples

Real MT-output correction pairs from QALB Guidelines Section 6.1 (news and Wikipedia text,
Google MT output corrected by human annotators). Source:
http://nlp.qatar.cmu.edu/qalb/QALB-guidelines_0.90.pdf

Use this alongside SKILL.md Sections 2–4 — these examples show full-sentence fixes (word
order, missing articles, agreement, lexical choice) rather than isolated spelling rules, so
they're better calibrated to catching calque and terminology problems than the spelling
reference is.

## Word order restored to natural Arabic syntax

Source: "Brazil's Syrians divided over unrest."

- MT (calqued word order): السوريون منقسمون حول البرازيل الاضطرابات
- Corrected: سوريو البرازيل منقسمون حول الاضطرابات

The MT output kept the English possessive-then-topic order almost verbatim. The fix restructures
around the Arabic idafa (إضافة) construction — "Brazil's Syrians" becomes سوريو البرازيل as a
genitive unit, not two separate transplanted phrases.

## Missing definite articles (a systematic EN→AR gap)

Source: "Skin discolouration and pigmentation is just one of the many effects..."

- MT: تغير لون جلد وتصبغ هو مجرد واحد من الأثار الكثيرة
- Corrected: تغير لون الجلد والتصبغ هو مجرد واحد من الأثار الكثيرة

English doesn't require an article on generic nouns the way Arabic does. This is a systematic
gap, not a one-off mistake — check every generic/collective noun carried over from an English
noun phrase for a missing ال.

## Preposition and register mismatch from literal rendering

Source: "Japan has an extensive web of highways with thousands of tunnels."

- MT: اليابان لديها على شبكة الإنترنت واسعة من الطرق السريعة مع الآلاف من الأنفاق
- Corrected: اليابان لديها شبكة طرقات سريعة واسعة مع الآلاف من الأنفاق

Two things happened here: "web" was mistranslated as شبكة الإنترنت (internet network, a false
cognate reading of the wrong sense of "web"), and an extra على was inserted matching no Arabic
grammatical need. Word-sense ambiguity in the source is a common cause of this kind of error —
"web" as "network" vs. "web" as "the internet" needs disambiguating from context, not translated
by the more frequent sense.

## Passive/verb-choice mismatch

Source: "Engineers on Monday began inspections..."

- MT: بدأت المهندسين — wrong verb-subject gender/number agreement (بدأت is feminine singular,
  المهندسين is a plural masculine object-case noun used incorrectly as subject)
- Corrected: بدأ المهندسون — بدأ agrees correctly, المهندسون in the correct nominative plural form

Subject-verb agreement errors are common in MT output when the source sentence's subject is
morphologically ambiguous in English (no case marking) but Arabic requires the correct case
ending to signal grammatical role.

## Person/gender mismatch in biographical text

Source: "Daniela Hantuchová (born April 23, 1983 ... ) is a Slovak professional tennis player."

- MT: دانييلا هانتوشوفا (ولد 23 أبريل 1983...) هو لاعب التنس السلوفاكية المهنية
  — uses masculine ولد (born) and هو (he) and لاعب (male player) for a woman's biography
- Corrected: دانييلا هانتوشوفا (ولدت في 23 أبريل 1983...) هي لاعبة تنس سلوفاكية محترفة

MT frequently defaults to masculine forms regardless of the subject's actual gender, especially
in biographical/profile text translated from English (which doesn't mark gender on verbs).
Always verify gender agreement across the entire sentence when translating biographical content
— it's not just the pronoun, it's the verb, the profession noun, and any adjectives.

## Long-sentence restructuring (multi-clause example)

Source: "It developed from a persistent area of deep convection on September 12, and steadily
strengthened as it moved to the north-northwest."

- MT (clause-by-clause, follows English structure almost exactly):
  أنها وضعت من منطقة الحمل الحراري العميق استمرار في 12 سبتمبر، وعزز بشكل مطرد، حيث إنها انتقلت
  إلى الشمال والشمال الغربي
- Corrected (restructured, better verb choices, proper agreement):
  وقد تشكل من منطقة حمل حراري عميق متواصلة في 12 سبتمبر، واشتد بشكل مطرد حيث انتقل إلى الشمال
  والشمال الغربي

Note the corrected version changes وضعت (a weak/generic verb choice for "developed") to تشكل
(formed), a more precise verb — this is a Section 3 (word choice) fix layered on top of a
Section 2 (calque) fix in the same sentence. Real MT output often needs both fixes at once,
not one or the other.

## Lexical choice depends on context, not dictionary default

Source: "Traditional museums are run by the old people."

- MT: يتم تشغيل المتاحف التقليدية من قبل كبار السن (uses تشغيل, "to operate/run" in a mechanical/
  operational sense — appropriate for machinery, not institutions)
- Corrected: تدار المتاحف التقليدية من قبل كبار السن (uses تُدار, "to be administered/managed" —
  the institutional sense of "run")

English "run" covers both senses; MT picks whichever Arabic equivalent is more frequent in
training data, not whichever fits this context. Check whether a polysemous English word got the
contextually correct Arabic sense, not just a valid one — this is the same failure pattern as
"web" being mistranslated as "internet" earlier in this file.

## Headline restructuring (titles need different treatment than body text)

Source: "Japan orders tunnel checks after disaster."

- MT (word-for-word, produces a nonsensical noun pile in Arabic): أوامر اليابان بعد كارثة نفق
  الشيكات
- Corrected (restored as a verbal sentence, the natural Arabic headline structure):
  اليابان تأمر بالتدقيق في الأنفاق بعد الكارثة

English headlines often drop articles and use noun-stacking ("Japan orders tunnel checks") in a
way that has no natural Arabic equivalent. Don't translate a headline word-for-word — identify
the actual verb and rebuild it as a proper Arabic verbal sentence (VSO or SVO), not a string of
nouns.

## Technical/numeric text needs the same restructuring as prose

Source: "The amount of RAM greatly affects the performance of the PC. However, if power is
discontinued to the RAM, as when you shut off your PC, the contents of the RAM disappear."

- MT (calqued, and drops a required idafa construction — "كمية من" instead of "كمية"):
  كمية من ذاكرة الوصول العشوائي يؤثر بشكل كبير على أداء جهاز الكمبيوتر. ومع ذلك، إذا توقف السلطة
  إلى RAM، وعند إيقاف تشغيل الكمبيوتر الخاص بك، ومحتويات RAM تختفي
- Corrected: كمية ذاكرة الوصول العشوائي تؤثر بشكل كبير على أداء جهاز الكمبيوتر. ومع ذلك، إذا
  انقطع التيار عن ذاكرة الوصول العشوائي، مثل ما يحدث عند إيقاف تشغيل جهاز الكمبيوتر، تختفي
  محتويات ذاكرة الوصول العشوائي

Two separate fixes in one passage: (1) "كمية من ذاكرة" incorrectly inserts من into what should be
a direct idafa construction "كمية ذاكرة"; (2) "توقف السلطة" literally back-translates "power is
discontinued" using the wrong sense of "power" (السلطة means political authority, not
electricity — the correct word here is التيار, current). Technical/scientific text is just as
prone to calque and word-sense errors as narrative prose — don't assume it needs lighter review
because it's "just factual."
