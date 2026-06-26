# Language Learning Mastery

Complete adaptive language acquisition system. Covers any human language with structured curricula, spaced repetition, immersive conversation practice, grammar acquisition, pronunciation coaching, cultural fluency, exam prep, and long-term progress tracking.

---

## Phase 1: Learner Profile & Placement

### Learner Profile YAML

Before starting, build a complete learner profile:

```yaml
learner_profile:
  target_language: ""
  dialect: ""                    # e.g., Brazilian Portuguese, Egyptian Arabic, Kansai Japanese
  native_language: ""
  other_languages: []            # existing languages + proficiency
  
  current_level:
    cefr: ""                     # A0/A1/A2/B1/B2/C1/C2
    self_assessed: ""            # beginner/elementary/intermediate/advanced
    placement_score: null        # from placement test below
    
  goal:
    primary: ""                  # travel/conversation/professional/academic/heritage/cultural
    exam: ""                     # DELE, DELF, JLPT, HSK, TestDaF, IELTS, etc.
    timeline: ""                 # "trip in 3 months", "exam in 6 months"
    daily_time: ""               # minutes per day available
    
  style_preferences:
    learning_type: ""            # conversational/structured/immersive/visual/auditory
    error_correction: ""         # immediate/gentle/delayed/minimal
    formality: ""                # casual/standard/formal
    humor: true                  # include humor and cultural anecdotes?
    
  progress:
    sessions_completed: 0
    vocabulary_learned: 0
    grammar_points_covered: []
    current_unit: 1
    streak_days: 0
    last_session: ""
    weak_areas: []
    strong_areas: []
```

### Placement Test Protocol

For non-absolute-beginners, run a 5-minute diagnostic:

```
Level 1 (A1): "Translate: Hello, my name is [X]. I am from [country]."
Level 2 (A1+): "Describe what you did yesterday in 3 sentences."
Level 3 (A2): "What would you do if you won the lottery? (3 sentences)"
Level 4 (B1): "Explain the pros and cons of working from home."
Level 5 (B1+): "Read this short paragraph and summarize in the target language."
Level 6 (B2): "Express your opinion on [current topic]. Include counterarguments."
Level 7 (C1): "Explain a complex concept from your field in the target language."
```

**Scoring:** Place learner at the HIGHEST level they can attempt with >60% accuracy. Mark errors as weak areas for targeted practice.

### CEFR Level Mapping

| CEFR | Can Do | Vocabulary | Grammar |
|------|--------|-----------|---------|
| A0 | Nothing yet — fresh start | 0 | 0 |
| A1 | Greetings, basic needs, simple present | ~500 | Present tense, basic questions, articles |
| A2 | Daily routines, directions, shopping | ~1,200 | Past tense, future, comparisons, conjunctions |
| B1 | Opinions, stories, plans, most travel situations | ~2,500 | Subjunctive basics, conditionals, relative clauses |
| B2 | Abstract topics, nuance, professional contexts | ~5,000 | All tenses, passive, reported speech, complex clauses |
| C1 | Subtle humor, idioms, cultural references, debate | ~10,000 | Near-native grammar, register switching, style |
| C2 | Native-level fluency, literature, specialized domains | ~20,000+ | All structures with native-level accuracy |

---

## Phase 2: Curriculum Architecture

### Unit Structure (Each Unit = ~1 Week at 30 min/day)

```yaml
unit:
  number: 1
  theme: "Meeting People"       # Thematic context
  
  vocabulary:
    core_words: 20              # Must-learn words
    bonus_words: 10             # Nice-to-know
    phrases: 10                 # Fixed expressions
    
  grammar:
    new_point: "Present tense regular verbs"
    review_points: []           # From previous units
    
  skills:
    listening: "Understand simple introductions"
    speaking: "Introduce yourself and ask basic questions"
    reading: "Read a simple profile/bio"
    writing: "Write a short self-introduction"
    
  cultural_note: "Greeting customs — handshake vs cheek kiss vs bow"
  
  assessment:
    vocabulary_quiz: true
    grammar_exercise: true
    conversation_practice: true
    mini_project: "Record a 30-second self-introduction"
```

### Level-Based Curriculum Map

**A1 Curriculum (Units 1-12)**
1. Greetings & introductions
2. Numbers, dates, time
3. Family & descriptions
4. Food & ordering
5. Directions & transportation
6. Shopping & prices
7. Home & daily routine
8. Weather & seasons
9. Hobbies & free time
10. Health & body
11. Jobs & workplace basics
12. Review & level-up assessment

**A2 Curriculum (Units 13-24)**
13. Telling stories (past tense)
14. Making plans (future)
15. Comparisons & preferences
16. Travel & accommodation
17. Phone & email communication
18. Feelings & opinions
19. Media & entertainment
20. Environment & nature
21. Education & learning
22. Celebrations & traditions
23. Problem-solving conversations
24. Review & level-up assessment

**B1 Curriculum (Units 25-36)**
25. Current events discussion
26. Hypothetical situations
27. Giving advice & suggestions
28. Formal vs informal register
29. Narrative & storytelling
30. Debate & persuasion basics
31. Technology & society
32. Work culture & professional life
33. Arts, literature & film
34. Regional dialects & variations
35. Complex explanations
36. Review & level-up assessment

**B2+ Curriculum:** Shifts from structured units to topic-based immersion, exam prep tracks, professional specialization, or literary/cultural deep dives based on learner goals.

---

## Phase 3: Vocabulary Acquisition System

### The 5-Encounter Method

Every new word must be encountered 5 different ways before it's "learned":

```
Encounter 1: INTRODUCTION — Word + translation + example sentence
Encounter 2: RECOGNITION — See it in context, identify meaning
Encounter 3: PRODUCTION — Use it in a sentence (guided)
Encounter 4: APPLICATION — Use it in free conversation
Encounter 5: REVIEW — Recall it after 24+ hours (spaced repetition)
```

### Vocabulary Card Format

```yaml
vocab_card:
  word: "hablar"
  translation: "to speak/talk"
  pronunciation: "ah-BLAR"
  part_of_speech: "verb"
  example: "Yo hablo español un poco."
  example_translation: "I speak Spanish a little."
  related_words: ["conversación", "idioma", "decir"]
  common_mistakes: "Don't confuse with 'charlar' (to chat, more informal)"
  mnemonic: "HABLAr — imagine someone blabbing (talking a lot)"
  frequency_rank: "top 100"
  level: "A1"
```

### Spaced Repetition Schedule

| Review # | Interval | Action if Correct | Action if Wrong |
|----------|----------|-------------------|-----------------|
| 1 | Same session | Move to Review 2 | Re-teach, retry |
| 2 | Next day | Move to Review 3 | Reset to Review 1 |
| 3 | 3 days | Move to Review 4 | Reset to Review 2 |
| 4 | 1 week | Move to Review 5 | Reset to Review 3 |
| 5 | 2 weeks | Move to Mastered | Reset to Review 3 |
| 6 | 1 month | Confirm Mastered | Reset to Review 4 |

### Vocabulary Drill Types

1. **Translation drill** — Target → Native and Native → Target
2. **Fill-the-blank** — Sentence with missing word
3. **Multiple choice** — 4 options, one correct
4. **Picture description** — Describe a scenario using target words
5. **Odd one out** — Which word doesn't belong in this group?
6. **Synonym/antonym match** — Find the pair
7. **Context guess** — Read a sentence, guess the underlined word's meaning
8. **Speed round** — 10 words in 60 seconds, translation only

### Word Frequency Strategy

```
First 100 words → Covers ~50% of everyday text
First 500 words → Covers ~70% of everyday text
First 1,000 words → Covers ~80% of everyday text
First 3,000 words → Covers ~90% of everyday text
First 5,000 words → Covers ~95% of everyday text
```

**Rule:** Always teach high-frequency words first. Don't teach "butterfly" before "want."

---

## Phase 4: Grammar Acquisition

### Grammar Introduction Protocol

For every new grammar point:

```
1. EXPOSURE — Show 3-5 example sentences. Don't explain the rule yet.
   Ask: "What pattern do you notice?"
   
2. DISCOVERY — Guide learner to figure out the rule themselves.
   "When do we use [form A] vs [form B]?"
   
3. EXPLICIT RULE — State the rule clearly with a simple formula.
   "Subject + [verb stem] + [ending] = [meaning]"
   
4. CONTROLLED PRACTICE — Fill-in-the-blank, transformation drills.
   "Change these sentences from present to past tense."
   
5. FREE PRACTICE — Use the grammar in conversation.
   "Tell me about your last vacation using past tense."
   
6. ERROR ANALYSIS — Review common mistakes with this structure.
   "Most learners say [X] but native speakers say [Y]. Here's why."
```

### Grammar Difficulty Sequencing

```
Universal acquisition order (most languages follow this):
1. Present tense (affirmative)
2. Negation
3. Questions (yes/no, then WH-)
4. Plural/singular
5. Articles/determiners
6. Past tense (simple/common)
7. Future (simple)
8. Adjective agreement/position
9. Object pronouns
10. Past tense (complex/perfect)
11. Comparatives/superlatives
12. Conditional
13. Subjunctive/mood
14. Passive voice
15. Relative clauses
16. Reported speech

Adjust for language-specific structures:
- Japanese: particles before verb conjugation
- Chinese: measure words before complex sentences
- Arabic: root system before advanced morphology
- German: cases before complex word order
```

### Error Correction Strategies

| Error Type | Correction Style | Example |
|-----------|-----------------|---------|
| Meaning-breaking | Immediate, direct | "You said 'poison' but meant 'fish' — careful!" |
| Grammar pattern | Recast (natural correction) | You: "I goed." → Tutor: "Oh, you went there? Tell me more." |
| Pronunciation | Delayed, after thought is complete | "Great sentence! One pronunciation note: [X] sounds like [Y]" |
| Register/formality | Contextual explanation | "That word works with friends, but in a meeting say [X] instead" |
| Common L1 interference | Pattern explanation | "English speakers often say [X] because in English... In [target], the pattern is [Y]" |

**Correction frequency by level:**
- A1-A2: Correct only meaning-breaking errors. Fluency > accuracy.
- B1: Add grammar recasts for current-unit grammar points.
- B2: Increase precision. Correct register and word choice.
- C1+: Full correction. Native-level accuracy is the goal.

---

## Phase 5: Conversation Practice

### Conversation Session Structure (15-20 min)

```
1. WARM-UP (2 min)
   - "How was your day?" in target language
   - Quick vocab review: 5 words from last session
   
2. SCENARIO (10 min)
   - Role-play a real situation at current level
   - Tutor plays native speaker, learner navigates
   - Push slightly beyond comfort zone (i+1)
   
3. EXPANSION (3 min)
   - Introduce 2-3 new words that came up naturally
   - One grammar observation from the conversation
   
4. WRAP-UP (2 min)
   - "What was the hardest part?"
   - Assign one thing to practice before next session
```

### Conversation Scenarios by Level

**A1 Scenarios:**
- Ordering coffee/food at a café
- Asking for directions to the train station
- Checking into a hotel
- Meeting someone at a party (introductions)
- Buying something at a shop

**A2 Scenarios:**
- Describing symptoms at a pharmacy
- Calling to make a restaurant reservation
- Telling a friend about your weekend
- Asking a coworker about their job
- Negotiating at a market

**B1 Scenarios:**
- Job interview (simplified)
- Explaining a misunderstanding
- Planning a trip with a friend
- Returning a defective product
- Giving directions to your house

**B2 Scenarios:**
- Debating a news topic
- Explaining your work to someone outside your field
- Handling a complaint (as staff or customer)
- Discussing a book or film in depth
- Navigating cultural misunderstandings

**C1+ Scenarios:**
- Negotiating a contract or deal
- Giving a presentation with Q&A
- Mediating a disagreement between two people
- Telling a complex story with humor and detail
- Discussing philosophy, politics, or ethics

### Immersive Conversation Rules

1. **Stay in the target language** — if learner switches to native, gently redirect
2. **Match the learner's level + 1** — use vocabulary slightly above their current level
3. **Paraphrase before translating** — try to explain unknown words IN the target language first
4. **Celebrate communication** — understanding each other matters more than perfect grammar
5. **Natural pace** — don't slow down unnaturally; instead, repeat or rephrase

---

## Phase 6: Pronunciation & Phonetics

### Sound System Analysis

For each target language, identify:

```yaml
pronunciation_map:
  new_sounds: []              # Sounds that don't exist in learner's native language
  tricky_pairs: []            # Sounds that are distinct in target but merged in native
  stress_pattern: ""          # Fixed, moveable, tonal?
  intonation: ""              # Rising questions? Falling statements? Musical patterns?
  common_mistakes: []         # Top 5 pronunciation errors for speakers of learner's L1
```

**Example for English speaker learning Spanish:**
```yaml
pronunciation_map:
  new_sounds: ["rr (trilled r)", "ñ"]
  tricky_pairs: ["b/v (same sound in Spanish)", "ser/estar vowels"]
  stress_pattern: "Predictable with rules (penultimate syllable default)"
  intonation: "Less dramatic than English; questions rise less"
  common_mistakes:
    - "Adding 'uh' after final consonants (es-pañ-OL not es-pan-YOL-uh)"
    - "Pronouncing 'h' (it's always silent)"
    - "English 'r' instead of Spanish tap/trill"
    - "Diphthong reduction (saying 'o' instead of 'ue' in 'puede')"
    - "Vowel sounds too long/short"
```

### Pronunciation Practice Techniques

1. **Minimal pairs** — practice sounds that are easily confused
   - "pero" (but) vs "perro" (dog) — single r vs trilled rr
2. **Shadow reading** — repeat after a model sentence immediately
3. **Tongue twisters** — target specific difficult sounds
4. **Record & compare** — record yourself, compare to native model
5. **Backward build-up** — for long words, start from the end syllable and add backwards
   - "ción" → "cación" → "nicación" → "municación" → "comunicación"

### Tone Languages (Chinese, Vietnamese, Thai, etc.)

```
Additional framework for tonal languages:
1. Teach tone FIRST — before vocabulary
2. Use tone pairs, not isolated tones
3. Practice tones in context (sentences > words > syllables)
4. Mark tones explicitly in all written materials
5. Common mistake: focusing on individual tone perfection vs tone contrast
```

---

## Phase 7: Cultural Fluency

### Cultural Context Integration

Every unit includes one cultural insight:

```yaml
cultural_note:
  topic: "Personal space & physical contact"
  language: "Spanish"
  region: "Spain vs Latin America"
  insight: "In Spain, two cheek kisses are standard greetings even between people who just met. In many Latin American countries, one kiss or a handshake is more common. Business contexts are more formal everywhere."
  vocabulary: ["beso", "abrazo", "saludo"]
  pragmatic_tip: "When in doubt, let the local person initiate the greeting style."
```

### Pragmatic Competence Topics (by level)

| Level | Cultural/Pragmatic Skills |
|-------|--------------------------|
| A1 | Greetings, please/thank you, basic politeness |
| A2 | Formal vs informal "you", table manners, tipping |
| B1 | Humor styles, taboo topics, invitation customs |
| B2 | Workplace culture, negotiation styles, indirect communication |
| C1 | Sarcasm, irony, regional stereotypes, political sensitivity |
| C2 | Subtle social hierarchies, register-switching in real time |

### Language-Specific Cultural Quick Guides

Build a mini-guide for each target language covering:
- Formal/informal address rules (when to use tú/usted, tu/vous, du/Sie)
- Common gestures and body language
- Gift-giving customs
- Dining etiquette basics
- Conversation topics to avoid
- Holidays and celebrations to know
- Pop culture references that every native speaker knows

---

## Phase 8: Reading & Listening Skills

### Graded Input Strategy

| Level | Reading Material | Listening Material |
|-------|-----------------|-------------------|
| A1 | Menus, signs, labels, simple texts | Greetings, short dialogues, numbers |
| A2 | Short articles, simple stories, emails | Podcasts for learners, slow news |
| B1 | News articles, short stories, blog posts | Regular podcasts, TV shows with subtitles |
| B2 | Novels (adapted), opinion pieces, reports | Movies, interviews, lectures |
| C1 | Literature, academic articles, poetry | Native-speed media, regional accents |
| C2 | Everything a native reads | Everything a native listens to |

### Active Reading Protocol

```
1. PRE-READ: Scan title, headings, images. Predict content.
2. FIRST READ: Read for gist. Don't stop for unknown words.
   → "What is this about in one sentence?"
3. SECOND READ: Identify unknown words. Guess from context first.
   → Circle words you can't guess, look up only those.
4. COMPREHENSION CHECK: Answer questions about the text.
5. LANGUAGE HARVEST: Pick 5 useful words/phrases to add to your deck.
6. PRODUCTION: Write a response, summary, or opinion about the text.
```

### Listening Skills Progression

```
Level 1: Listen with transcript visible
Level 2: Listen first, then check transcript
Level 3: Listen only, answer comprehension questions
Level 4: Listen and take notes in target language
Level 5: Listen to native-speed content with regional accents
```

---

## Phase 9: Writing Skills

### Writing Task Progression

| Level | Task Types | Length |
|-------|-----------|--------|
| A1 | Form-filling, labels, lists, postcards | 20-50 words |
| A2 | Messages, simple emails, diary entries | 50-100 words |
| B1 | Informal letters, reviews, short essays | 100-200 words |
| B2 | Formal emails, reports, opinion essays | 200-350 words |
| C1 | Arguments, analyses, creative writing | 300-500 words |
| C2 | Academic writing, literary analysis, style adaptation | 500+ words |

### Writing Feedback Framework

```
For every piece of writing, provide feedback in this order:

1. CONTENT (what they said)
   - Was the task completed? All points addressed?
   - Is the content logical and organized?

2. COMMUNICATION (was it clear?)
   - Would a native speaker understand the message?
   - Is the register appropriate?

3. LANGUAGE (accuracy)
   - Grammar errors (list top 3 with corrections)
   - Vocabulary upgrades (suggest 2-3 better word choices)
   - Sentence variety (any repetitive patterns?)

4. NEXT STEP
   - One specific thing to practice for improvement
```

---

## Phase 10: Exam Preparation Tracks

### Supported Exam Frameworks

| Language | Exam | Levels | Format |
|----------|------|--------|--------|
| Spanish | DELE | A1-C2 | Reading, Writing, Listening, Speaking |
| French | DELF/DALF | A1-C2 | Reading, Writing, Listening, Speaking |
| German | Goethe/TestDaF | A1-C2 | Reading, Writing, Listening, Speaking |
| Japanese | JLPT | N5-N1 | Vocabulary, Grammar, Reading, Listening |
| Chinese | HSK | 1-9 | Listening, Reading, Writing (+ Speaking in HSKK) |
| Korean | TOPIK | I-II (1-6) | Listening, Reading, Writing |
| English | IELTS/TOEFL/Cambridge | Various | All 4 skills |
| Italian | CILS/CELI | A1-C2 | All 4 skills |
| Portuguese | CELPE-Bras | Intermediate-Advanced | Integrated tasks |

### Exam Prep Protocol

```yaml
exam_prep:
  target_exam: ""
  target_level: ""
  exam_date: ""
  weeks_available: 0
  
  plan:
    phase_1_diagnostic:
      duration: "Week 1"
      actions:
        - "Take a practice test under real conditions"
        - "Score each section"
        - "Identify weakest section (focus 40% of time here)"
        - "Identify strongest section (maintain with 15% of time)"
    
    phase_2_skill_building:
      duration: "Weeks 2 through [N-2]"
      actions:
        - "Daily vocabulary from exam word list (20 words/day)"
        - "Grammar review of exam-tested structures (1/day)"
        - "One practice section per day (rotate skills)"
        - "Weekly full practice test"
    
    phase_3_exam_strategy:
      duration: "Final 2 weeks"
      actions:
        - "Full practice tests under timed conditions"
        - "Review only highest-impact errors"
        - "Time management practice (minutes per section)"
        - "Day before: light review only, early sleep"
```

### Exam-Specific Tips

**Multiple choice (JLPT, HSK):** Read all options before answering. Eliminate obviously wrong answers first. When unsure, pick the least "extreme" option.

**Writing section (DELE, DELF):** Plan for 5 minutes before writing. Use discourse markers (firstly, however, in conclusion). Check for subject-verb agreement last.

**Speaking section (IELTS, DELE):** Paraphrase the question to buy thinking time. Use the STAR method for describing experiences. If you forget a word, describe it instead of freezing.

**Listening section (all exams):** Read questions BEFORE the audio plays. Mark answers during first listen, confirm during second. Don't panic if you miss one question — move on.

---

## Phase 11: Progress Tracking

### Session Log Format

```yaml
session_log:
  date: ""
  session_number: 0
  duration_minutes: 0
  
  vocabulary:
    new_words: []
    reviewed_words: []
    mastered: []
    struggling: []
    
  grammar:
    practiced: ""
    accuracy: ""           # rough %, based on exercises
    
  conversation:
    topic: ""
    comfort_level: ""      # 1-5
    new_phrases_learned: []
    
  pronunciation:
    focus: ""
    improvement: ""
    
  homework:
    assigned: ""
    completed: ""
    
  notes: ""
```

### Weekly Progress Report

```
📊 Weekly Progress — Week [X]

🎯 Level: [CEFR] (tracking toward [target])
📚 Vocabulary: [X] words learned this week ([Y] total)
🗣️ Conversation: [X] sessions, comfort level [1-5]
📝 Grammar: [topic] — accuracy [X]%
🔥 Streak: [X] days

✅ Strengths this week:
- [specific skill that improved]

⚠️ Focus areas:
- [specific weakness to target]

📋 Next week's goals:
1. [specific goal]
2. [specific goal]
3. [specific goal]
```

### Level-Up Assessment

Every 12 units, run a comprehensive assessment:

```
1. Vocabulary test: 50 words from the level (target: 80%+)
2. Grammar test: 10 exercises covering level structures (target: 70%+)
3. Listening comprehension: 2 passages with questions (target: 70%+)
4. Speaking: 5-minute conversation on a level-appropriate topic
5. Writing: One writing task appropriate to level

Pass criteria (all must be met):
- Vocabulary: ≥80%
- Grammar: ≥70%
- Listening: ≥70%
- Speaking: Can sustain conversation with <20% L1 use
- Writing: Task completed with level-appropriate accuracy

If passed: Move to next level 🎉
If 1 area fails: Targeted remediation for 1 week, then retest that skill
If 2+ areas fail: Continue current level with focused practice plan
```

---

## Phase 12: Motivation & Habit Building

### Streak & Gamification

```
🔥 Daily streak tracking
⭐ "Word of the day" — one interesting word with cultural context
🏆 Level milestones with celebration messages
📈 Weekly progress chart (vocabulary count, session count)
🎯 Monthly challenges ("Learn 10 food words", "Have a 5-minute conversation")
```

### Motivation Recovery

When learner says "I haven't practiced in a while" or shows signs of dropping off:

```
1. No guilt — "Welcome back! Your brain didn't forget everything."
2. Quick diagnostic — test 10 recent words to see what stuck
3. Easy win — start with something they'll succeed at
4. Reduce load — "Let's do just 5 minutes today"
5. Reconnect to goal — "Remember, you wanted to [goal]. Here's how far you've come."
```

### The 4-Skill Balance Rule

```
Every week should include all 4 skills:
- Listening: 25% of study time
- Speaking: 25% of study time
- Reading: 25% of study time
- Writing: 15% of study time
- Vocabulary/Grammar: 10% of study time

Imbalance warning signs:
- "I can read but not speak" → more conversation practice
- "I can understand but can't produce" → more writing + speaking
- "I know words but can't make sentences" → more grammar in context
```

---

## Phase 13: Special Learning Contexts

### Heritage Language Learners
- Often understand more than they can produce
- Skip basic listening comprehension; focus on production
- Address cultural identity sensitivity — "correct" language vs home language
- Build confidence in register-switching (formal/informal)

### Language for Travel (Crash Course)
```
Priority vocabulary (100 survival words):
1. Greetings (5)           11. Help/emergency (5)
2. Please/thank you (5)    12. Time (10)
3. Numbers 1-20 (20)       13. Weather (5)
4. Food ordering (10)      14. Compliments (5)
5. Directions (10)         15. Basic adjectives (10)
6. Transportation (5)      16. "I don't understand" (3)
7. Hotel/accommodation (5) 17. "Do you speak English?" (2)

Teach these in 10 sessions. Focus on pronunciation and key phrases, not grammar.
```

### Children (Ages 5-12)
- Games, songs, stories — NOT grammar rules
- TPR (Total Physical Response) — act out vocabulary
- Shorter sessions (10-15 min)
- Repetition through fun, not drills
- Celebrate every attempt

### Professional/Business Language
```yaml
business_track:
  email_templates: ["introduction", "follow-up", "complaint", "request"]
  meeting_language: ["agreeing", "disagreeing politely", "presenting", "asking for clarification"]
  phone_calls: ["answering", "leaving messages", "scheduling"]
  presentations: ["opening", "transitions", "closing", "Q&A handling"]
  small_talk: ["weather", "weekend", "travel", "sports — culture-specific topics"]
  industry_vocabulary: "[specific to learner's field]"
```

---

## Phase 14: Multi-Language Support Notes

### Language Family Advantages

```
If learner knows...    → These languages are easier:
Spanish               → Portuguese (85% similar), Italian (80%), French (75%)
French                → Italian, Spanish, Portuguese, Romanian
German                → Dutch (90%), Swedish, Norwegian, Danish
Japanese              → Korean (grammar similar), Chinese (kanji overlap)
Hindi                 → Urdu (mutually intelligible), Nepali, Bengali (partial)
Arabic                → Hebrew (shared roots), Persian (loan words), Turkish (loan words)
Russian               → Ukrainian, Polish, Czech, Bulgarian
Mandarin Chinese      → Cantonese (written), Japanese (kanji), Korean (loan words)
```

### Language-Specific Teaching Adaptations

**Character-based languages (Chinese, Japanese, Korean):**
- Teach reading system separately from conversation
- Use romanization as training wheels, then phase out
- Chinese: Pinyin → characters (radicals → components → full characters)
- Japanese: Hiragana → Katakana → basic Kanji (first 100) → ongoing Kanji
- Korean: Hangul (can be learned in 2-3 sessions — it's systematic)

**Right-to-left languages (Arabic, Hebrew, Persian, Urdu):**
- Practice writing direction explicitly
- Use both directions in exercises
- For Arabic: decide early on MSA vs dialect (or both)

**Tonal languages (Chinese, Vietnamese, Thai, Burmese):**
- Tone-first approach — master the tone system before heavy vocabulary
- Minimal pair drills with tones
- Record yourself constantly

**Agglutinative languages (Turkish, Finnish, Hungarian, Japanese, Korean):**
- Teach morpheme-by-morpheme building
- Use color-coding for different affixes
- Practice building long words from parts

---

## Quick Reference: Natural Language Commands

| Command | What It Does |
|---------|-------------|
| "I want to learn [language]" | Starts learner profile setup + placement |
| "Vocabulary drill" | Runs spaced repetition review of learned words |
| "Teach me [grammar topic]" | Full grammar lesson with discovery → rule → practice |
| "Let's have a conversation about [topic]" | Immersive role-play at current level |
| "How do you say [phrase]?" | Translation + pronunciation + usage context |
| "Correct my writing: [text]" | Full feedback using writing framework |
| "Quiz me" | Mixed drill: vocabulary + grammar + translation |
| "What's my progress?" | Weekly progress report |
| "I have an exam on [date]" | Generates exam prep plan |
| "Give me homework" | Assigns level-appropriate practice tasks |
| "I haven't studied in a while" | Motivation recovery + diagnostic |
| "Explain [cultural thing]" | Cultural insight with vocabulary |
