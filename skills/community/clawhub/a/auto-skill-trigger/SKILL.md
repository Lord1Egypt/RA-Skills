---
name: auto-skill-trigger
description: Auto Skill Trigger - Match skills to tasks using keyword scoring
---

# Auto Skill Trigger - Automatic Skill Matching

## Overview

Automatically match relevant skills to the current task using keyword/pattern scoring. Pre-filters the `<available_skills>` list before the LLM decides which to load.

## How It Works

1. When a message arrives, score each skill's description against the message
2. Only include high-scoring skills in the prompt
3. The LLM makes the final decision from a relevant subset

## Scoring Algorithm

Simple TF-IDF-like keyword overlap:

```javascript
api.registerHook("before_prompt_build", async ({ event, ctx }) => {
  const msg = event.messages?.[0]?.content || "";
  const keywords = extractKeywords(msg);
  
  // Get all skills and their descriptions
  const skills = await getAllSkills();
  const scored = skills.map(skill => ({
    skill,
    score: keywordOverlap(keywords, skill.description)
  })).filter(s => s.score > 0.3); // threshold
  
  // Sort by score and take top 5
  scored.sort((a, b) => b.score - a.score);
  const topSkills = scored.slice(0, 5);
  
  // Return instruction to prioritize matched skills
  if (topSkills.length > 0) {
    return {
      prompt: `\n\n## Skill Hint\nFocus on: ${topSkills.map(s => s.skill.name).join(", ")}\n`
    };
  }
  return {};
});
```

## Keyword Extraction

```javascript
function extractKeywords(text) {
  // Extract meaningful words/n-grams
  const words = text.toLowerCase()
    .split(/\W+/)
    .filter(w => w.length > 2)
    .filter(w => !STOP_WORDS.has(w));
  return new Set(words);
}

function keywordOverlap(keywords, description) {
  const descWords = extractKeywords(description);
  let matches = 0;
  for (const kw of keywords) {
    if (descWords.has(kw)) matches++;
  }
  return matches / keywords.size;
}
```

## Configuration

```json5
{
  "agents": {
    "defaults": {
      "autoSkillTrigger": {
        "enabled": true,
        "maxSkills": 5,
        "threshold": 0.3,
        "stopWords": ["the", "a", "an", "is", "are", "and"]
      }
    }
  }
}
```

## Patterns That Match

| Message Pattern | Matched Skills |
|----------------|---------------|
| "帮我查 GitHub issue" | github |
| "天气怎么样" | weather |
| "写个 Python 脚本" | coding |
| "搜一下最近的新闻" | search |

## Limitations

- Pattern-based matching is imperfect
- Complex tasks may need multiple skills
- LLM still has final say via SKILL.md scanning
- Update threshold based on results
