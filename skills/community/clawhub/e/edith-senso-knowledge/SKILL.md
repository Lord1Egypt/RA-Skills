---
name: edith-senso-knowledge
description: Search your Senso.ai knowledge base hands-free through Edith smart glasses. Triggers on knowledge/document queries.
user-invocable: true
---

# Senso Knowledge Search

Search your knowledge base through Senso.ai when users ask document or knowledge questions via Edith smart glasses.

## When to use

Activate this skill when the user asks questions that imply searching documents, policies, knowledge bases, or stored information. Examples:

- "What does the policy say about..."
- "Search my docs for..."
- "Find information about..."
- "What's in my knowledge base about..."
- "Look up..." (when referring to documents, not web search)
- "What did that document say about..."
- "Summarize the section on..."

Do NOT use this skill for general knowledge questions, web searches, weather, math, or anything that doesn't involve the user's own ingested documents.

## Setup

The user must have a Senso.ai API key. If they haven't configured one yet, tell them:

1. Sign up at https://senso.ai and create a project
2. Go to Settings > API Keys and generate a new key
3. Tell OpenClaw: "My Senso API key is sk-..." and store it for future use

The API key should be stored in OpenClaw's memory/config as `SENSO_API_KEY`.

## How to search

Use the `exec` tool to call the Senso.ai search endpoint:

```bash
curl -s -X POST "https://sdk.senso.ai/api/v1/search" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: ${SENSO_API_KEY}" \
  -d '{"query": "<user's question>", "top_k": 5}'
```

The response is JSON with an array of results, each containing relevant text passages and metadata.

## Formatting results for Edith voice output

Edith speaks responses through smart glasses speakers. Follow these rules strictly:

1. **Be concise.** Glasses users cannot read long text. Summarize the top 1-2 results into 1-3 short sentences.
2. **Lead with the answer.** Start with the most relevant finding, not "I found 5 results..."
3. **No markdown, no bullet points, no URLs.** The response is spoken aloud.
4. **Use natural speech patterns.** Say "According to your documents..." or "Your policy states that..." rather than listing metadata.
5. **If no results match**, say "I didn't find anything about that in your documents." Don't speculate or hallucinate content.
6. **If the API call fails**, say "I couldn't reach your knowledge base right now. Please check your Senso API key."

### Example

User: "Hey Edith, what does the return policy say about electronics?"

Good response: "Your return policy says electronics can be returned within 30 days with the original receipt. After 30 days, only store credit is offered."

Bad response: "I found 3 results in your knowledge base. Result 1: Section 4.2 of return-policy.pdf states that electronic items purchased from authorized retailers may be returned within a period of thirty calendar days from the date of purchase, provided that..."

## Generating answers from search results

If the search results contain relevant passages but need synthesis, you can optionally use the generate endpoint to produce a grounded answer:

```bash
curl -s -X POST "https://sdk.senso.ai/api/v1/generate" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: ${SENSO_API_KEY}" \
  -d '{"query": "<user question>", "context": "<concatenated search result passages>"}'
```

Only use this when search results need summarization across multiple passages. For simple lookups where a single passage answers the question, just summarize the passage directly.

## Error handling

- **Missing API key**: "You haven't set up your Senso knowledge base yet. You'll need a Senso API key. Visit senso.ai to get one, then tell me the key."
- **401 Unauthorized**: "Your Senso API key seems invalid. Please check it and try again."
- **Empty results**: "I didn't find anything about that in your documents."
- **Network/timeout error**: "I couldn't reach your knowledge base right now. Try again in a moment."
