# QALB Spelling & Punctuation Reference

Extracted and condensed from the Qatar Arabic Language Bank (QALB) Guidelines v0.90
(Zaghouani, Habash, Mohit — CMU-Qatar / Columbia, 2013), Section 7.
Source: http://nlp.qatar.cmu.edu/qalb/QALB-guidelines_0.90.pdf

Use this when Section 5 of SKILL.md flags a hamza, punctuation, or number issue and you need
the specific rule rather than the quick heuristic.

## Hamza (الهمزة)

### Hamzat Wasl vs. Hamzat Qat' (word-initial)

Test: prefix the word with و or ف. If the hamza is pronounced in the resulting phrase, it's
qat' (write `أ` or `إ`). If it's silent, it's wasl (write bare `ا`).

**Hamzat Wasl (silent, written as bare alif) occurs in:**
- Imperative of triliteral verbs not starting with hamza: اعلم، اكتب
- Past tense, imperative, and masdar of form VII/VIII verbs: انتفع، انتفاع؛ اطّلع
- Past tense, imperative, and masdar of form X verbs: استغفر، استغفار
- A closed set of nouns: اسم، ابن، ابنة، امرؤ، امرأة (and duals: اسمان، ابنان، ابنتان، امرأتان)
- The definite article ال

**Hamzat Qat' (pronounced, written with hamza mark) occurs in:**
- Form IV verbs and their masdar: أكرم → إكرام؛ أجاد → إجادة
- All nouns except the wasl set above
- All letters/particles except ال

### Medial Hamza Seat

Governed by the stronger of the hamza's own vowel and the preceding vowel.
Strength order: kasra > damma > fatha > sukun.

- **On ya' seat (ئـ):** hamza is kasra (سُئل، تطمئن، أسئلة); or preceding letter is kasra (بئر);
  or preceded by a kasra-vowelled ya' (بيئة)
- **On waw seat:** damma+damma (شؤون، رؤوس); damma+fatha (رؤوف); damma+sukun (مرؤوس، مسؤول);
  fatha+damma (فؤاد، مؤرخ); sukun+damma (بؤس); damma after a madd-waw (وضوؤك)
- **On alif seat:** fatha+fatha (سأل، اطمأن); sukun+fatha (فأس، يأبى); fatha+sukun (مسألة، ملأى، توأم، ييأس)
- **On the line (no seat), bare hamza:** fatha after madd-alif (تساءل، قراءة، إجراءات) or madd-waw
  (مروءة، وضوءك)

### Word-Final Hamza

Seat matches the vowel of the preceding letter:
- Preceding letter kasra → ya' seat: قارئ، يخطئ
- Preceding letter damma → waw seat: امرؤ، يجرؤ
- Preceding letter fatha → alif seat: يقرأ، ملجأ
- Preceding letter sukun, or preceded by alif → on the line: شيء، ضوء / ماء، سماء، نداء

### Common Confusions (from QALB Table 1)

| Wrong | Right | Issue |
|---|---|---|
| اصبعه | إصبعه | missing hamza |
| او | أو | missing hamza |
| اقل | أقل | missing hamza |
| ايران | إيران | missing hamza |
| الان | الآن | missing alif madd |
| للامه | للأمة | taa marbuta + missing hamza |
| منذو | منذ | extra waw |
| سئال | سؤال | wrong medial hamza seat |

## Punctuation (علامات الترقيم)

Always convert Latin punctuation to Arabic equivalents in Arabic text: `,` → `،`, `;` → `؛`,
`?` → `؟`. Don't leave Latin punctuation mixed into Arabic sentences.

**Comma (،)** — use only in these four cases (remove elsewhere):
1. Separating coordinated/related clauses, usually joined by و or لكن or أو
2. Enumeration (list items), may combine with و before the last item
3. Introducing an explanation or definition of the preceding word/phrase
4. Separating clauses of a conditional sentence

**Semicolon (؛)** — "فاصلة منقوطة" (dotted comma), written inverted. Two uses:
1. Between two phrases where the first causes the second: لقد لعب كثيرًا؛ فاتسخت ملابسه
2. Between two phrases where the second explains the reason for the first: لم تحقق أختك درجات
   عالية؛ لأنها لم تدرس بإخلاص

**Colon (:)** — use only when:
1. Introducing reported speech (قال، حكى، سأل، أجاب...)
2. Introducing a thing's types/categories/parts
3. After phrases ending in "التالية" / "الآتية" / "ما يلي" or similar
4. Before a direct quotation

**Question mark (؟)** — only at the end of sentences that open with an interrogative
(من، متى، كيف، أين...). Repeat after each part of a multi-part question joined by أم/أو.

**Exclamation mark (!)** — only after: standard exclamatory forms (ما أفعل — ما أجمل الربيع),
recognized exclamatory expressions, or genuine emotional statements (awe, astonishment, praise,
blame).

**Quotation marks (" ")** — enclose verbatim quoted material (Quran, hadith, direct quotes) and
terms being highlighted.

**Parentheses ( )** — enclose parenthetical clauses, explanatory/clarifying detail, or inserted
sources/figures.

**Two dashes ( — — )** — set off a parenthetical clause that could be removed without changing
the sentence's meaning.

## Numbers (كتابة الأعداد)

- **1 and 2 (واحد، اثنان):** agree in gender with the counted noun — جاء رجل واحد / وصلت امرأة واحدة
- **3-9:** reverse agreement — feminine form with masculine counted noun and vice versa —
  أكلت ثلاث تفاحات (تفاحة is feminine → ثلاث, no ta marbuta)
- **Compound numbers (13-19):** first part reverse-agrees, second part (عشر) matches normally
- **10 alone:** agrees normally with the counted noun (عشرة رجال / عشر نساء)
- **Tens/hundreds/thousands (20, 30... 100, 1000):** invariant — no gender agreement — تسعون مجلدًا
  / عشرون صحيفةً
- Keep the numeral system (Eastern Arabic ١٢٣ vs. Western Arabic 123) consistent with what the
  source document uses — don't silently convert.
- Group large numbers with commas/spaces consistently: 1,000,000 — merge any space-broken numbers
  in source text into one properly grouped number.

## When Still Unsure

Per QALB's own annotator guidance: check spelling against Al Jazeera's archive
(aljazeera.net) for names/proper nouns, compare Google search frequency for competing spellings,
or check an online Arabic dictionary (e.g. arabicdictionary.kacst.edu.sa). If genuinely uncertain
after checking, flag it rather than guessing.
