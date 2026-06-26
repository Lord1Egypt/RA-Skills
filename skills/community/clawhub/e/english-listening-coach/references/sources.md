# English Listening Coach — Source Library

This file is the reference for all content sources used by the english-listening-coach skill. Read the relevant section when selecting or fetching content.

---

## Table of Contents
1. Listen A Minute — Full Topic List
2. Breaking News English
3. Daily Dictation
4. English Club
5. ESL Fast
6. Source Selection Guide

---

## 1. Listen A Minute

**Base URL:** `https://listenaminute.com`
**URL pattern:** `https://listenaminute.com/[letter]/[topic_slug].html`
**Difficulty:** A2–B2
**Content:** 60-second monologues (~120–160 words), first-person, everyday English
**Best for:** Beginners to upper-intermediate, conversational vocabulary, relatable topics

**Fetching tip:** The page body contains a `### READ` section with the article text in a table. Extract only that paragraph — ignore worksheets, gap-fill activities, and nav.

### Full Topic List (480 topics — alphabetical by slug)

#### A
accidents, actors, advertising, advice, airplanes, airports, alcohol, aliens, animals, anti-aging_creams, apartments, art, autumn, avatars

#### B
babysitting, bad_habits, banks, baths, beauty, being_afraid, being_married, being_single, birthdays, blood, books, bullying, business, busy

#### C
calories, carbon_footprint, careers, cars, cats, chickens, children, chocolate, christmas, climate_change, clothes, coffee, computers, cosmetic_surgery, cosmetics, credit_cards, crime, culture, current_events, cyber-bullying, cyber_crime

#### D
dancing, danger, death, dentists, diamonds, digital_cameras, directions, disability, discrimination, diseases, divorce, doctors, dogs, dreams, driving, drugs

#### E
e-mail, eating, education, eggs, electricity, emergencies, energy, english, evolution, exercise

#### F
factories, family, famine, fashion, fast_food, fear, feet, first_impressions, fish, fishing, flowers, flying, food, food_safety, football, formula_one, four_seasons, freedom, french_fries, friends, frustration, fun, funerals, furniture

#### G
gambling, gangs, gangsters, gardening, gardens, genetic_engineering, genocide, getting_married, global_warming, globalization, god, gold, guns

#### H
hacking, hair, haircuts, halloween, hands, hangovers, happiness, harry_potter, hate_crimes, health, heroes, history, hobbies, holidays, homework, hospitals, hotels, housework, human_rights, hunger

#### I
i_love_you, identity_cards, immigration, inflation, information, insects, intelligence, internet, investments

#### J
jealousy, junk_food

#### K
kindness, knowledge

#### L
languages, laughter, laziness, learning, libraries, lies, loneliness, love, luck

#### M
manners, marriage, media, medicine, memory, men, mobile_phones, money, movies, music, mystery

#### N
nature, news, nightlife, noise, nutrition

#### O
obesity, oceans, old_age, opinion, organic_food

#### P
pain, parents, peace, pets, philosophy, phobias, photography, plastic_surgery, politics, pollution, poverty, power, prejudice, privacy, procrastination

#### Q
quality_of_life, questions

#### R
racism, reading, recycling, relationships, religion, retirement, revenge, rich_and_poor, rights, risk, robots, romance, running

#### S
safety, science, self-confidence, shopping, sleep, smoking, social_media, space, sports, stress, success, superstitions, sustainability

#### T
tattoos, taxes, technology, teenagers, television, terrorism, time, tourism, transport, travel, trust, truth

#### U
unemployment, universe

#### V
vegetables, violence, volunteering

#### W
war, water, wealth, weather, weight, wildlife, wisdom, women, work, world_cup

#### Y–Z
yoga, youth, zoos

---

## 2. Breaking News English

**Base URL:** `https://breakingnewsenglish.com`
**Dictation page:** `https://breakingnewsenglish.com/dictation.html`
**Difficulty:** B1–C1
**Content:** Real news articles adapted for ESL learners, with gap-fill dictation activities built in
**Best for:** Upper-intermediate to advanced learners, current events, news vocabulary

**Fetching tip:** The dictation page shows individual sentences from news articles. Each article page (e.g., `https://breakingnewsenglish.com/2501/250101-topic.html`) contains a full article. Use the dictation page for sentence-level practice or individual article pages for paragraph-level practice.

**URL pattern for articles:** `https://breakingnewsenglish.com/[YYMM]/[YYMMDD]-[topic_slug].html`

**How to use:**
- Fetch `https://breakingnewsenglish.com/dictation.html` to get the current day's dictation sentences
- For a specific topic, search the site or construct a URL from their archive
- Articles are ~300–500 words at two difficulty levels (easier / harder)

---

## 3. Daily Dictation

**Base URL:** `https://dailydictation.com`
**Difficulty:** A2–C1
**Content:** Sentence-level and paragraph dictation exercises, organized by topic and difficulty
**Best for:** Focused sentence dictation, pronunciation patterns, TOEFL/TOEIC prep

**Topics:** Conversations, names, numbers, expressions, idioms, news, TOEFL, TOEIC

**Fetching tip:** Individual exercise pages contain an audio player and transcript. The transcript is usually in a `<p>` or `<div class="transcript">` element. Extract only the dictation text.

**How to use:**
- Browse by topic: `https://dailydictation.com/[topic]`
- For beginner-friendly content: conversation exercises
- For advanced: TOEFL or news exercises

---

## 4. English Club

**Base URL:** `https://www.englishclub.com`
**Dictation page:** `https://www.englishclub.com/listening/dictation.php`
**Difficulty:** A1–C1 (three distinct levels)
**Content:** Structured dictation exercises at elementary, intermediate, and advanced levels

**Level breakdown:**
- **Elementary (A1–A2):** Single sentences — simple commands, greetings, common phrases
- **Intermediate (B1–B2):** Multi-sentence — directions, common quotes, everyday situations
- **Advanced (C1):** Full paragraphs — literary passages, speeches, formal language

**Fetching tip:** Each exercise page has a recorded passage and a written transcript below. Extract the transcript text from the page body. Two recordings are provided: normal speed and slowed — note this to the learner.

**Recommended for:** Learners who want structured level progression and shorter, focused exercises.

---

## 5. ESL Fast

**Base URL:** `https://www.eslfast.com`
**Difficulty:** A1–B1
**Content:** Short graded readings with vocabulary support, very beginner-friendly
**Best for:** A1–A2 learners or complete beginners who need shorter, simpler passages

**URL pattern:** `https://www.eslfast.com/robot/[topic]/[topic]001.htm` (numbered stories)

**Topics include:** Daily life, simple conversations, routines, family, school

**Fetching tip:** Pages contain a short story (50–100 words) and a vocabulary list. Extract only the story paragraph.

---

## 6. Source Selection Guide

Use this table to select the right source based on learner level and preference:

| Learner level | Prefers | Best source |
|---|---|---|
| A1–A2 | Simple, everyday topics | ESL Fast or English Club (elementary) |
| A2–B1 | Relatable, conversational | Listen A Minute |
| B1–B2 | Current events, longer text | Breaking News English (easier version) |
| B2–C1 | News, real-world English | Breaking News English (harder version) |
| C1–C2 | Challenging, authentic | Breaking News English + English Club (advanced) |
| Any | Sentence-level focus | Daily Dictation |
| Any | Pronunciation focus | English Club (has slow + normal speed) |
| Any | Broad topic choice | Listen A Minute (480 topics) |

### Fallback Priority
If a source fails to load, try in this order:
1. Listen A Minute (most reliable, static pages)
2. English Club
3. ESL Fast
4. Generate an original passage at the correct level
