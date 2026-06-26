# Identity Maker — Creator Instructions

These instructions guide the skill-creator in building the identity-maker skill.

## Purpose

The identity-maker creates and maintains IDENTITY.md — the document that defines who the agent is. This includes the agent's name, role, capabilities, boundaries, communication style, and any other attributes that define its identity.

## What makes a good identity-maker

The identity-maker should:

- Feel like a thoughtful conversation about who the assistant should be, not a form to fill out
- Adapt its questions based on the user's responses and the context from identity-creator-context.md
- Recognize that different users want very different things from their assistant's identity — some want a professional tool, others want a creative companion, others want something entirely unique
- In bootstrap mode, create a complete IDENTITY.md from scratch through interview
- In update mode, make surgical updates when the agent's role or self-concept genuinely evolves

## Key considerations for the skill-creator

When building this skill:

- The template structure comes from identity-creator-context.md — designed specifically for this user based on their meta interview
- The interview should be conversational and build naturally, not feel like a checklist
- The skill should handle users who have strong opinions about their agent's identity AND users who want guidance and suggestions
- In update mode, the bar for changes should be high — identity should be stable unless there's real reason to evolve
- The agent has no identity yet during this interview — it should be open and curious, not defaulting to a pre-baked persona
