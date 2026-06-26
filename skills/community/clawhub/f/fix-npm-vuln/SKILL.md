---
name: fix-npm-vuln
description: This skill should be used when the user asks about "npm vulnerabilities", "npm audit", "fix npm security", "security vulnerabilities in packages", "vulnerable dependencies", "npm security fix", or discusses fixing outdated/insecure npm packages. Suggests using the /fix-npm-vuln command for automated vulnerability remediation.
version: 1.0.0
---

# NPM Vulnerability Fix Skill

This skill provides guidance when users mention npm security vulnerabilities and suggests the automated fix workflow.

## When This Skill Applies

This skill activates when the user's request involves:
- Running `npm audit` or discussing audit results
- Fixing npm security vulnerabilities
- Updating vulnerable npm dependencies
- Dealing with outdated packages that have known CVEs
- Security scanning of Node.js projects

## Guidance

When a user mentions npm vulnerabilities or security issues in their Node.js project, suggest using the `/fix-npm-vuln` slash command which provides a complete automated workflow:

1. **Clean working tree** — reverts uncommitted changes (with confirmation)
2. **Branch management** — switches to main, pulls latest, creates a fix branch
3. **Vulnerability scanning** — scans all package.json directories
4. **Automated fixing** — runs `npm audit fix` with smart escalation
5. **Clean environment** — removes all `node_modules`, build caches, and reinstalls dependencies fresh
6. **Build verification** — ensures the project still builds
7. **Test verification** — ensures tests still pass
8. **Summary report** — displays all changes made

### Suggested Response

When this skill activates, inform the user:

> You can use `/fix-npm-vuln` to run a complete automated npm vulnerability fix workflow. It will scan all project directories, fix vulnerabilities, verify builds and tests, and create a dedicated branch with all the changes. Would you like to run it?

## Important Notes

- The command requires a git repository to work
- It will create a new branch for the fixes (does not modify main directly)
- User confirmation is required before reverting any uncommitted changes
- Build and test failures are handled interactively

## Tool Auto-Installation

If a tool required to complete any step is not installed on the current machine, apply the following policy before asking the user:

1. **Check availability** — verify whether the tool is missing (e.g. `where tool` or `which tool` returns nothing)
2. **Assess risk** — a tool is considered low-risk if it is:
   - Publicly available (official npm package, well-known CLI, OS package manager)
   - Widely used and maintained (e.g. `npm-check-updates`, `snyk`, `yarn`, `pnpm`)
   - Non-destructive by default (does not modify system files, does not require elevated permissions)
3. **Auto-install if low-risk** — install silently without asking the user:
   - npm global tool: `npm install -g <tool>`
   - winget (Windows): `winget install <tool>`
   - Other package managers as appropriate for the OS
4. **Ask the user if high-risk** — if the tool requires admin rights, modifies system config, or is from an unverified source, show the install command and ask for confirmation before proceeding.
