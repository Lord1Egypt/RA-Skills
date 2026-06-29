# Marketplace Listing Copy

## Canonical Title

Cruit Recruiter

## SEO Title

Cruit Recruiter: search AI-native developers from your coding agent

## Short Description

Search Cruit for AI-native developers, review low-PII candidate cards, and explicitly
confirm any paid reveal or candidate message.

## Medium Description

Cruit Recruiter helps hiring teams search for AI-native developers from inside their
coding agent. The skill translates a hiring need into structured search filters, returns
ranked low-PII candidate cards, and requires explicit approval before any contact-credit
reveal or candidate message.

Use it for early sourcing when you care whether candidates actually build with coding
agents and recent modern stacks.

Website: https://cruit.dev

## Long Description

Cruit Recruiter is an agent skill for finding AI-native developers through Cruit.

Recruiters describe a hiring need in natural language, such as "Rust backend engineers
who shipped AI tooling recently" or "full-stack TypeScript product engineers with agent
experience." The skill turns that request into structured search filters, shows the
filters for review, searches Cruit, and presents low-PII candidate cards before any paid
action.

The workflow is intentionally explicit:

- browser device auth, no pasted tokens
- recruiter access and credits are checked first
- search filters are shown before searching
- candidate cards avoid contact info before reveal
- reveal and message actions each require explicit confirmation
- exact message text is shown before sending

Built by Cruit, the AI-native hiring marketplace inside coding agents.

Website: https://cruit.dev

## Category Options

- Recruiting
- Hiring
- Sourcing
- Developer tools
- AI coding
- Productivity

## Tags

cruit, recruiter, candidate-search, sourcing, ai-native-developers, developer-hiring,
coding-agents, claude-code, codex, cursor, technical-recruiting, startup-hiring

## Security Note

This is an API-backed skill. It contacts `https://cruit.dev`, uses browser device auth,
and stores credentials locally under `~/.cruit/`. It never reveals contact information,
spends credits, or sends candidate messages without explicit approval.

