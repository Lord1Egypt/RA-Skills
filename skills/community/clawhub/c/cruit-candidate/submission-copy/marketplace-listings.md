# Marketplace Listing Copy

## Canonical Title

Cruit Candidate

## SEO Title

Cruit Candidate: publish an AI-native developer profile from real project metadata

## Short Description

Create a privacy-respecting Cruit profile for AI-native developer discovery. Reviews only
approved project folders, drafts a recruiter-searchable profile, and publishes after user
approval.

## Medium Description

Cruit Candidate helps developers become discoverable to recruiters looking for
AI-native builders. The skill guides a coding agent through browser auth, approved
project-folder review, optional resume import, profile drafting, user approval, publish,
and weekly refresh setup.

It is built for developers who work inside coding agents and want a low-effort,
privacy-respecting way to show what they actually build. Cruit uploads metadata and
approved profile text, never source code or secrets.

Website: https://cruit.dev

## Long Description

Cruit Candidate is an agent skill for creating and maintaining a recruiter-searchable
profile for AI-native developers.

The skill runs inside a developer's coding agent and turns approved local project
metadata, optional resume facts, and user-provided role preferences into a Cruit profile.
It is designed for candidates who build with Claude Code, Codex, Cursor, and other
coding agents and want recruiters to find evidence of recent, real work.

The flow is consent-first:

- browser device auth, no pasted tokens
- user chooses which folders may be reviewed
- source code, secrets, `.env` files, private keys, phone numbers, personal email, and
  street address are not published
- profile draft is shown in chat before publishing
- weekly refresh is optional and user-approved

Built by Cruit, the AI-native hiring marketplace inside coding agents.

Website: https://cruit.dev

## Category Options

- Recruiting
- Hiring
- Developer tools
- AI coding
- Career
- Productivity

## Tags

cruit, ai-native-developers, developer-profile, recruiting, hiring, coding-agents,
claude-code, codex, cursor, developer-discovery, candidate-profile, career

## Security Note

This is an API-backed skill. It contacts `https://cruit.dev`, uses browser device auth,
and stores credentials locally under `~/.cruit/`. It must not ask users to paste tokens
or upload source code, secrets, `.env` files, private keys, or private contact details.

