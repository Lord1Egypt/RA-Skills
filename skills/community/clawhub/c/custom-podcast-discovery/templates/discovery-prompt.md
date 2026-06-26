# Topic Ranking Prompt

You are helping rank potential podcast topics based on user interests.

## User Interests
{interests}

## Candidate Topics
{topics_json}

## Your Task

Rank these topics by relevance to the user's interests. Consider:
1. Direct keyword matches with interests
2. Topical relevance (even if keywords don't match exactly)
3. Newsworthiness and timeliness
4. Depth potential (can this support 15-20 min of content?)
5. Audience engagement potential

Output JSON format:
```json
[
  {
    "title": "Topic title",
    "url": "source url",
    "relevance_score": 0-10,
    "reasoning": "Why this matches interests",
    "category": "Best matching interest category"
  }
]
```

Sort by relevance_score descending.
