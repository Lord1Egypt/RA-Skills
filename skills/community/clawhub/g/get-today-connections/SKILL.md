---
name: get-today-connections
description: Fetch today's NYT Connections puzzle answers and hints. Trigger this skill when the user asks for "today's Connections answers", "today's connections hints", "NYT Connections today", or similar questions.
---

# Get Today's NYT Connections Answers

## Purpose

Quickly retrieve the full answers and hints for today's NYT Connections puzzle without opening a browser.

## Steps

1. Use the WebFetch tool to request the following URL:

   ```
   https://connections-answers.com/api/today
   ```

   Prompt: "Extract the full JSON response as-is"

2. Parse the returned JSON, which has the following structure:

   ```json
   {
     "puzzleDate": "YYYY-MM-DD",
     "title": "Connections April 9 2026 Answers",
     "url": "https://connections-answers.com/blog/connections-april-9-2026-answers",
     "categories": [
       {
         "color": "yellow",
         "order": 0,
         "name": "Category Name",
         "hint": "A one-line hint",
         "words": ["WORD1", "WORD2", "WORD3", "WORD4"]
       }
     ],
     "hintContent": "...",
     "answerContent": "..."
   }
   ```

3. Display the results to the user in the following format:

   **Today's NYT Connections — {puzzleDate}**

   | Color | Category | Hint | Answers |
   | ----- | -------- | ---- | ------- |
   | 🟨 Yellow | {name} | {hint} | WORD1, WORD2, WORD3, WORD4 |
   | 🟩 Green  | {name} | {hint} | WORD1, WORD2, WORD3, WORD4 |
   | 🟦 Blue   | {name} | {hint} | WORD1, WORD2, WORD3, WORD4 |
   | 🟪 Purple | {name} | {hint} | WORD1, WORD2, WORD3, WORD4 |

   Full breakdown: {url}

## Notes

- If the user only wants hints and not answers, show only the `hint` column and hide the `words` column
- `order: 0` (yellow) = easiest, `order: 3` (purple) = hardest
- `hintContent` / `answerContent` are full Markdown articles; output them directly if the user wants a detailed breakdown
- For past puzzles, direct the user to <https://connections-answers.com/blog> to browse the archive
