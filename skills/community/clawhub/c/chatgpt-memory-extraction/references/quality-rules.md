# Quality Rules

These rules address specific pitfalls discovered through real-world use of this skill. They cover things an AI agent would NOT figure out on its own.

## ChatGPT Export-Specific Pitfalls

1. **Multi-day conversations**: A single ChatGPT conversation window may be reused over weeks or months. The title and start date only reflect the first message. Always look for date markers within the conversation and split events by actual dates.

2. **Misleading titles**: Titles are auto-generated from the first message. Never guess content from title — read the actual content.

3. **Emails are evidence**: When users draft or receive emails inside a conversation, these reveal real events (conflicts, decisions, relationships). Record the underlying event, not just "user wrote an email."

4. **Voice transcription**: Voice-to-text conversations are messy and jump topics rapidly. Read every message even when text seems garbled.

## AI Laziness Pitfalls

These are failure modes that consistently appear when processing large volumes of conversations:

5. **Message count filler**: Never write "XX messages about various topics." Describe what was actually discussed.

6. **Early stop**: The most important content is often in the middle or end. Do not summarize after reading only the first few messages.

7. **False completion claims**: Do not say "files updated" without actually opening and editing them. Verify.

8. **Knowledge shallowness**: Do not write "learned X." Record what the concept is, how the user understood it, what it was applied to, and why it mattered.

9. **People file skipping**: Every person mentioned by name in a quarter must have their file updated — not just the "main" person.

10. **Speed over quality**: Quality degrades when rushing large batches. Split into monthly batches if needed. Users should review each batch before proceeding.
