---
name: daily-english-vocab
description: |
  Daily English vocabulary and conversation practice via scheduled cron delivery.
  Sends a daily lesson with two parts: (1) a real-life Small Talk phrase with context,
  variations, and natural responses, and (2) 3-5 themed vocabulary words with
  pronunciation, example sentences, and tips. Vocabulary rotates through 12 life
  categories every 2-3 days for comprehensive coverage.
  Use when: setting up daily English learning, vocabulary practice, creating an
  English lesson cron job, language learning schedule, or "teach me English daily".
  Also triggers on: 每日英语, 学英语, English lesson, vocab of the day, word of the day.
---

# Daily English Vocab

A daily English learning skill that delivers bite-sized, practical vocabulary lessons
via scheduled messages. Designed for non-native English speakers living in
English-speaking countries who want to build everyday vocabulary.

## Setup

Create a cron job to deliver daily lessons. Adjust time, timezone, and channel as needed:

```bash
openclaw cron add \
  --name "daily-english" \
  --description "Daily English: Small Talk + Themed Vocabulary" \
  --cron "0 8 * * *" \
  --tz "America/Los_Angeles" \
  --session isolated \
  --announce \
  --channel telegram \
  --to <CHAT_ID> \
  --timeout-seconds 60 \
  --message "Generate today's English lesson following the daily-english-vocab skill instructions."
```

Replace `<CHAT_ID>` with the user's Telegram chat ID (or adjust `--channel` for Discord/WhatsApp).

## Lesson Format

Each daily lesson has two parts:

### Part 1: Daily Small Talk 🗣️

One natural American English conversational phrase:
- **Scene**: Where/when you'd use it (e.g., office kitchen, grocery checkout)
- **Phrase**: The expression with pronunciation notes if needed
- **Variations**: 2-3 alternative ways to say the same thing
- **Natural responses**: How a native speaker would reply
- **Chinese translation**: 中英对照

### Part 2: Themed Vocabulary 📚

3-5 words from the current rotating category:
- **Word** + phonetic transcription (IPA)
- **Meaning** in Chinese
- **Example sentence** (中英对照) — use realistic, everyday contexts
- **💡 Tip**: Easily confused words, cultural notes, or fun facts

## Category Rotation

Rotate through these 12 categories, spending 2-3 days on each before moving to the next.
One full cycle takes about a month.

1. 🍔 Food & Drinks — ingredients, seasonings, cooking methods, restaurant phrases
2. 🏥 Body & Health — body parts, secretions, symptoms, doctor visit phrases
3. 🏠 Home & Living — furniture, appliances, cleaning, repairs
4. 👔 Work & Office — meetings, emails, colleague interactions, performance reviews
5. 🏋️ Fitness & Sports — equipment, exercises, muscle groups, gym phrases
6. 🛒 Grocery Shopping — produce, meat, household items, checkout phrases
7. 🚗 Transportation — driving, gas stations, car repairs, road signs
8. 🐱 Pets & Animals — breeds, behaviors, vet visits, pet supplies
9. 🧹 Daily Chores — laundry, cooking, cleaning, trash sorting
10. 🎮 Entertainment — gaming, movies, music, social activities
11. 💰 Finance — stocks, banking, taxes, insurance
12. 🌤️ Weather & Nature — weather phenomena, disasters, terrain, plants

### Tracking State

Store rotation state in `memory/english-vocab-state.json`:

```json
{
  "currentCategory": 1,
  "daysOnCategory": 1,
  "lastRun": "2026-03-15",
  "wordsUsed": ["booger", "saliva", "sweat"]
}
```

- Read this file at the start of each lesson
- If `daysOnCategory >= 3` or file doesn't exist, advance to the next category
- Track `wordsUsed` per category to avoid repeats within the same cycle
- Reset `wordsUsed` when cycling back to a category

## Style Guidelines

- Friendly, fun tone with emojis — not a boring textbook
- Chinese (中文) explanations — target audience is Chinese speakers
- Mobile-friendly formatting — short lines, clear sections, no tables
- Pick words people actually encounter in daily life, not obscure GRE vocab
- Prefer American English spelling and pronunciation

## Example Output

```
🗣️ 【每日口语】

场景：同事周一早上在茶水间打招呼
💬 "How was your weekend? Do anything fun?"

变体：
• "Good weekend?"
• "What'd you get up to this weekend?"

地道回法：
• "Not bad! Just took it easy." (还行，就休息了)
• "Yeah! Went hiking at Rancho." (去 Rancho 爬山了)

📚 【今日词汇】🏥 身体与健康

1️⃣ **booger** /ˈbʊɡ.ɚ/
   鼻屎
   🗨️ "Your kid has a booger hanging out of his nose."
   (你家娃鼻子上挂着鼻屎。)
   💡 口语常用，不算粗俗。"Pick your nose" = 挖鼻孔

2️⃣ **drool** /druːl/
   口水（流出来的）
   🗨️ "The baby drooled all over my shirt."
   (宝宝把口水流了我一身。)
   💡 drool vs saliva: saliva 是医学用语，drool 更口语

3️⃣ **sweat** /swɛt/
   汗
   🗨️ "I'm drenched in sweat after that workout."
   (锻炼完浑身是汗。)
   💡 "Break a sweat" = 出汗/费力，"No sweat!" = 没问题！
```

## Customization

Users can customize by editing the cron message:
- Change number of words (e.g., "give me 5 words" instead of 3)
- Focus on specific categories (e.g., "only food and fitness categories")
- Add Part 3 for idioms, slang, or phrasal verbs
- Switch explanation language from Chinese to another language
