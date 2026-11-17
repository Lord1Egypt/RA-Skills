# The operations map

OPERATIONS.md is where agents do the most damage when it's missing: they redeploy the wrong thing, restart a service the wrong way, or read a secret to find out what a setting does. Give every row that applies to the project a line, and point at the guide that holds the procedure.

| Task | What the row must say |
|---|---|
| Local setup | The guide, the services it needs (such as a database), and which env template to copy |
| Checks before a PR | The exact typecheck, test and build commands for each package, and which tests need live services |
| CI | Which workflows exist, **what triggers them** (a manual-only CI means opening a PR runs nothing), and how to run them by hand |
| Preview or staging deploy | How to put a branch there and which gate it passes |
| Production deploy | **What actually ships** (a merge to `main`, a tag, a manual script), who or what pulls it, and the break-glass path |
| Release | Where the version lives, where the changelog lives, the release checklist, and any announcement |
| Rollback | How to go back: a redeploy, a snapshot, or roll forward |
| Health and verification | The health URL from outside and inside, and how to confirm new code is live (a version field, a bundle hash) |
| Logs and restarts | Where logs are and the right way to restart. Link the gotchas guide rather than repeating it. |
| Configuration | The env-var guide and the tracked template. **Names only, never values.** |
| Secrets | The CI secret *names* and what each is for. Never values, and never where to find them. |
| External services | Workers, runners or other boxes deployed separately, and their guides |
| Data | Where the schema lives, how migrations apply, and where runtime data sits outside Git |

When moving server-side operations material out of an entry point:

- **Put box layout, process manager, web-server routing and known gotchas in the deployment guide**, verbatim. Hostnames and paths that already live in tracked files can move with them. Do not copy them into a router.
- **Put the CI walkthrough and its secret names in a CI guide.** Put the env-var table in a configuration guide.
- **Keep the rule itself in the entry point**: for example, "merging into `main` deploys", "never deploy without the security check", "never push to `main` without approval". The procedure moves; the rule stays.
- **Then search scripts, workflows and skills** for "see CLAUDE.md" and repoint each one to the procedure's new home.
