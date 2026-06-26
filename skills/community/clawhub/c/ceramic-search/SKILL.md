---
name: ceramic-search
description: Web search for AI agents using Ceramic. Use for accurate current information — news, prices, recent events, documentation, general fact checking. Trigger this skill for keywords like "latest", "recent", "look up", "search for", "find online", "what's happening".
metadata: { "openclaw": { "homepage": "https://ceramic.ai", "primaryEnv": "CERAMIC_API_KEY", "requires": {"env": ["CERAMIC_API_KEY"] } } }    
---

# Ceramic Search

Lexical (keyword-based) search engine built for AI agents.

# Usage

1. **Rewrite the natural language query**

   Ceramic matches exact keywords — it does not interpret natural language or synonyms automatically. Convert the user's natural language query into a keyword query of **2–8 words**.

   Rules:
   - Extract specific entities, topics, locations, and dates
   - Replace conversational phrasing with concrete keywords
   - Do not include uninformative words such as articles (the, a, an). Avoid prepositions (on, about, in, for, of, at, by, with) unless they are within established phrases or names (United States of America, Into the Wild).
   - Include relevant synonyms explicitly when terminology is ambiguous
   - Keep word order meaningful (`house cat` and `cat house` return different results)
   - Good keyword query examples:
     - "2026 Super Bowl halftime performer"
     - "climate change effects global warming impact"
     - "beginner investing strategies stocks bonds basics"

2. **Call the Ceramic Search API**

   ```bash
   curl https://api.ceramic.ai/search \
     -H "Authorization: Bearer $CERAMIC_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{"query": "keyword query", "maxDescriptionLength": 3000}'
   ```
   For `maxDescriptionLength`, use the default of 3000 unless the user needs more detail (max 8000).

3. **Retrieve the top sources from the response**

   The response is structured json with a `results` array containing up to 10 search results. The search results in the array are ordered by relevance, with the first result being the strongest match. Each result includes the fields `description`, `title`, and `url`.

   ```json
   {
     "requestId": "request id",
     "result": {
       "results": [
         {
           "description": "search result description",
           "title": "search result title",
           "url": "search result url",
         },
         ...
       ],
       ...
     }
   }
   ```

4. **Summarize with citations**

   Write a concise answer drawing from the search result descriptions, and then list sources as numbered references:

   **Sources**
   1. [Title](url)
   2. [Title](url)

   Only cite sources whose descriptions contributed to the answer. If the search returns no useful results, refine the query with more specific keywords and try again before giving up.