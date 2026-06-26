# Filesystem Blueprint

Use this to create the Duolingo Learning OS scaffold.

## 1. Create Global Structure

```bash
mkdir -p ~/duolingo/{router,topics,archive}
```

Create baseline files:
- `~/duolingo/memory.md`
- `~/duolingo/router/topics.md`
- `~/duolingo/router/agentsmd-snippet.md`

## 2. Create Topic Namespace

For each active topic slug:

```bash
mkdir -p ~/duolingo/topics/<topic-slug>
```

Create required files from `topic-template.md`:
- `profile.md`
- `curriculum.md`
- `queue.md`
- `sessions.md`
- `checkpoints.md`

## 3. Seed Router Topics File

Add one section per topic:
- slug
- trigger phrases
- default difficulty lane
- weekly target loops

`router/topics.md` is the source of truth for activation matching.

## 4. Seed First Queue

Each topic starts with:
- placement block
- first 3 lessons
- first review item after initial completion

Do not leave queue empty after setup.

## 5. Verify Ready State

A topic is runnable only if all are true:
- namespace files exist
- at least one queue item exists
- routing trigger exists
- first checkpoint is scheduled
