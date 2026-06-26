# Drafting Style Template

Generate draft replies that are clear, concise, and action-oriented.

## Inputs

- Original message metadata and body
- User tone preferences (formal, friendly, concise)
- User intent (accept, decline, ask clarification, propose next step)

## Draft checklist

- Subject line matches thread intent (`Re: ...` when appropriate)
- Acknowledge sender request/context in first sentence
- Provide direct answer or next step
- Include concrete timing if relevant
- Keep short unless user asked for detailed response
- Avoid commitments the user did not approve

## Output format

```json
{
  "subject": "Re: ...",
  "text_body": "Hello ...",
  "to": ["..."],
  "cc": []
}
```
