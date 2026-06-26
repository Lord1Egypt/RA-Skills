# Skill Best Practices Checklist

Condensed best practices for Claude skills, derived from Anthropic's official guide.

---

## SKILL.md Structure

- [ ] Frontmatter includes `name` and `description`
- [ ] Description answers WHAT the skill does and WHEN to trigger it
- [ ] SKILL.md is under 500 lines (ideally under 300)
- [ ] Uses progressive disclosure — SKILL.md routes to external files for details
- [ ] Instructions are imperative and specific ("Run X", "Read Y", not "You might want to...")
- [ ] Workflow steps are numbered and sequential

## Trigger Design

- [ ] Description includes natural language trigger phrases users would actually say
- [ ] Trigger phrases cover common variations (e.g., "audit a skill", "review a skill", "check a skill")
- [ ] Not so broad that it triggers on unrelated requests
- [ ] Not so narrow that users must use exact phrasing

## File Organization

- [ ] Directory uses kebab-case naming
- [ ] SKILL.md at the root (exact case: `SKILL.md`)
- [ ] `scripts/` for executable code (bash, python)
- [ ] `references/` for context and criteria documents
- [ ] `assets/` for templates and static resources
- [ ] No unnecessary files that bloat token usage

## Token Efficiency

- [ ] SKILL.md acts as a router, not a monolith
- [ ] Large reference content lives in separate files
- [ ] Uses conditional loading ("If user needs X, read references/X.md")
- [ ] Scripts do heavy computation outside the context window
- [ ] Total skill footprint estimated and reasonable (<5,000 tokens ideal)

## Script Design

- [ ] Scripts have clear usage instructions and help text
- [ ] Exit codes are defined and meaningful
- [ ] Output goes to stdout (for Claude to parse); logging to stderr
- [ ] Scripts validate their inputs
- [ ] Scripts are self-contained (no unusual dependencies)

## Error Handling

- [ ] Common failure modes are anticipated
- [ ] Recovery steps are provided for each failure mode
- [ ] User is informed of errors with actionable messages
- [ ] Skill doesn't silently fail or produce misleading output

## Safety & Permissions

- [ ] Only requests tool access that is actually needed
- [ ] File operations scoped to specific directories
- [ ] Network access justified and scoped
- [ ] User input is validated before use in shell commands
- [ ] No access to secrets, credentials, or sensitive system files
- [ ] Destructive operations (delete, overwrite) have safeguards

## User Experience

- [ ] Skill provides progress feedback during long operations
- [ ] Asks for user input only when genuinely needed
- [ ] Output is well-formatted and scannable
- [ ] Suggests logical next steps after completion
- [ ] Works well on first use without prior configuration

## Documentation

- [ ] Purpose is clear to both Claude and human readers
- [ ] Complex logic is commented in scripts
- [ ] Reference files explain their own context and usage
- [ ] Template files include placeholder guidance
