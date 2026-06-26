# User Maker — Creator Instructions

These instructions guide the skill-creator in building the user-maker skill.

## Purpose

The user-maker creates and maintains USER.md — the document that captures who the user is, how they work, what they care about, and how the assistant should relate to them.

## What makes a good user-maker

The user-maker should:

- Feel respectful and non-invasive — the user decides how much to share
- Already know the agent's identity (from IDENTITY.md) and ask questions informed by that context
- Focus on information that will actually help the assistant work better with the user, not generic profile data
- Recognize that what matters varies wildly — a developer might care about coding preferences, a writer about creative process, a manager about communication style
- In bootstrap mode, create USER.md through a thoughtful interview
- In update mode, capture durable new insights about the user as they emerge from working together

## Key considerations for the skill-creator

When building this skill:

- The template structure comes from user-creator-context.md — tailored to this specific user
- The agent already has an identity at this point — the user-maker should embody it
- The interview should never feel like surveillance — frame questions around "how can I be more helpful" not "tell me about yourself"
- In update mode, only update when the insight is genuinely durable and will improve future interactions
- Respect boundaries — if the user doesn't want to share something, that's fine
