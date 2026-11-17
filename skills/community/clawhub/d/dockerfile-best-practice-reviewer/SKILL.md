---
name: dockerfile-best-practice-reviewer
description: >
  Review a Dockerfile for layer hygiene, least-privilege users, pin practices,
  and clearer build structure. Use when drafting or cleaning up container builds.
metadata: {"clawdbot":{"emoji":"🐳","requires":{"bins":[]}}}
---

# Dockerfile Best Practice Reviewer

## Purpose / Overview
Provide a structured review of a Dockerfile the user pastes: what is fine,
what to change, and a suggested patch sketch — without claiming to run a build
unless asked.

## When to Use
- New service containerization
- Image size or build-time complaints
- Security review of build instructions

## Usage / Instructions
1. Ask for the Dockerfile contents (and base image constraints if any).
2. Review in this order:
   a. Base image choice and tags (`:latest` risk)
   b. Package installs (cleanup, combined `RUN`, pinning)
   c. Multi-stage opportunities
   d. `COPY`/`ADD` scope and `.dockerignore` reminders
   e. Non-root `USER`
   f. `HEALTHCHECK`, `EXPOSE`, signal handling (`STOPSIGNAL` / tini notes)
   g. Secrets in build args/ENV (flag strongly)
3. For each issue: severity (high/med/low), why, and a concrete rewrite snippet.
4. Call out what already looks good so the review is balanced.
5. Prefer minimal diffs over full rewrites unless the file is short.
6. If multi-stage would clearly help, sketch builder vs runtime stages.
7. Do not invent registry names or private base images.
8. If the user asks to "make it production-ready," still keep changes explainable.
9. Remind that runtime orchestration (readiness probes) may belong outside Docker.
10. Offer a final checklist of 5 verification commands (`docker build`, run as
    non-root, etc.) without executing them unless requested.
11. Keep answers structured with short headings so the user can skim.
12. If information is missing, ask at most two clarifying questions before guessing.
13. Prefer concrete commands or checklists the user can copy.
14. Call out assumptions explicitly when the environment is unknown.
15. Refuse to invent tool output you did not see; ask for a fresh paste instead.
16. When offering optional follow-ups, keep them clearly optional.
17. Stay within this skill's scope; suggest a different task type if the request drifts.
18. End with a brief "done when" criterion so the user knows success.


## Examples
Single-stage Python image as root with `pip install` and no cleanup
→ suggest multi-stage, non-root user, and apt/pip cleanup patterns.

## Requirements / Dependencies
None for review. Docker CLI only if the user wants build commands run locally.

## Limitations / Caveats
Cannot validate that a private base image exists. Distro package names vary.

## Security / Permissions
Flag secrets in ENV/ARG. Do not ask for registry passwords. Text review only
by default.

## Description

Review a Dockerfile for layer hygiene, least-privilege users, pin practices, and clearer build structure.

## License or terms

Research

## Use case

For users and teams who want a concise assistant for: Review a Dockerfile for layer hygiene, least-privilege users, pin practices, and clearer build structure.

## Risks and mitigations

## References

- Dockerfile reference: https://docs.docker.com/reference/dockerfile/

## Ethical considerations

This skill may not be used illegally. Violations of domestic or international law are unacceptable; The publisher will not be accountable for such use. Do not use it to plan physical harm, terror-related activity, or other violent crime. Do not use it to generate instructions for committing crimes.
