# Research Procedure

Scout for competitions, events, publications, and precedents relevant to the user's active projects.

## Steps

1. **Load projects** — Read `workspace/projects/README.md` for active projects. If none, reply HEARTBEAT_OK.
2. **Load sources** — Read `workspace/config/sources.md`, focusing on Competitions, Materials & Technology, and Research & Theory sections.
3. **Per project** — For each active project:
   - Read its project file to get Research Topics, Type, and Phase.
   - Search in both English and the user's preferred language for:
     - **Competition deadlines** — open competitions matching the project type or research topics.
     - **Events** — exhibitions, lectures, conferences relevant to the project.
     - **Publications** — new papers, books, articles on the research topics.
     - **Precedents** — built projects similar in type, scale, or approach.
4. **Log findings** — For each finding, append to the project's `Findings Log` section:

```markdown
### YYYY-MM-DD
- [{title}]({url}) — {one-line summary and why it's relevant}
```

5. **Notify selectively** — Only message the user if something is noteworthy (upcoming deadline, highly relevant precedent). Otherwise, log silently.

## Guidelines

- Findings log is always written in **English**. Preserve original-language terms in parentheses.
- Avoid duplicating findings already in the Findings Log.
- Competition deadlines are highest priority — always flag these.
- Prefer depth on 1–2 projects over shallow coverage of all.
- If a finding spans multiple projects, log in the most relevant one and cross-reference.
