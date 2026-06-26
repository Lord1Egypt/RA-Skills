---
name: edith-senso-ingest
description: Ingest documents into your Senso.ai knowledge base through Edith smart glasses. Triggers when user wants to add content to their knowledge base.
user-invocable: true
---

# Senso Content Ingestion

Ingest documents and content into the user's Senso.ai knowledge base so it becomes searchable through Edith smart glasses.

## When to use

Activate this skill when the user wants to add, upload, or ingest content into their knowledge base. Examples:

- "Add this to my knowledge base..."
- "Ingest this document..."
- "Store this information..."
- "Remember this for later..." (when referring to document-scale content, not short notes)
- "Upload this to Senso..."
- "Index this content..."

Do NOT use this skill for simple note-taking or reminders. This is for ingesting substantial content that should be searchable later.

## Setup

The user must have a Senso.ai API key configured. If not, tell them:

1. Sign up at https://senso.ai and create a project
2. Go to Settings > API Keys and generate a new key
3. Tell OpenClaw: "My Senso API key is sk-..." and store it for future use

The API key should be stored in OpenClaw's memory/config as `SENSO_API_KEY`.

## How to ingest content

Use the `exec` tool to call the Senso.ai content ingestion endpoint:

```bash
curl -s -X POST "https://sdk.senso.ai/api/v1/content/raw" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: ${SENSO_API_KEY}" \
  -d '{"content": "<text content to ingest>", "metadata": {"title": "<optional title>", "source": "<optional source>"}}'
```

### Ingesting from a file

If the user provides a file path, read it first and then send the content:

```bash
curl -s -X POST "https://sdk.senso.ai/api/v1/content/raw" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: ${SENSO_API_KEY}" \
  -d @- <<'BODY'
{
  "content": "<file contents>",
  "metadata": {
    "title": "<filename>",
    "source": "file"
  }
}
BODY
```

For large files, consider chunking the content into logical sections before ingesting.

## Formatting responses for Edith voice output

Edith speaks responses through smart glasses speakers. Keep confirmations brief:

1. **Confirm success simply.** Say "Done, I've added that to your knowledge base" or "Got it, that's been indexed."
2. **Mention what was ingested.** Say "I've added the return policy document to your knowledge base" so the user knows what happened.
3. **No technical details.** Don't mention API responses, document IDs, chunk counts, or byte sizes.
4. **If it fails, be clear.** Say what went wrong in plain language.

### Example

User: "Hey Edith, add this meeting summary to my knowledge base: We decided to launch the new product line in Q3 and increase the marketing budget by 20 percent."

Good response: "Done, I've added your meeting summary to your knowledge base."

Bad response: "I have successfully ingested 1 document containing 147 characters into your Senso.ai knowledge base. The document ID is doc_abc123 and it was chunked into 1 segment."

## Error handling

- **Missing API key**: "You haven't set up your Senso knowledge base yet. You'll need a Senso API key. Visit senso.ai to get one, then tell me the key."
- **401 Unauthorized**: "Your Senso API key seems invalid. Please check it and try again."
- **Content too large**: Split the content into smaller pieces and ingest each separately. Confirm with "I've added your document in multiple parts to your knowledge base."
- **Network/timeout error**: "I couldn't reach your knowledge base right now. Try again in a moment."
- **Empty content**: "There's no content to add. Tell me what you'd like to store in your knowledge base."
