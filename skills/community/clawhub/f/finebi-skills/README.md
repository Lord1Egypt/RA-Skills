# finebi-skills

`finebi-skills` is the publishable markdown asset package in this monorepo.

## Structure

- `SKILL.md`: main skill entry and router
- `skills/*/SKILL.md`: scenario-focused sub-skills
- `references/*`: shared routing and CLI command conventions

## Contents

- `SKILL.md`
- `skills/*/SKILL.md`
- `references/*`

It does not include the CLI implementation.

## Install

```bash
npm install finebi-skills
```

## Release check

```bash
pnpm pack
```
