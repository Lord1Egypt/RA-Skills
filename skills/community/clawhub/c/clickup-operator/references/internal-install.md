# ClickUp Operator Internal Install

Use this when the goal is to make the package actually usable inside a real internal workspace, not just conceptually correct.

## Internal install target

The package needs four things to become usable:

1. a live ClickUp auth path
2. resolved workspace, list, and member IDs
3. a filled config file
4. a smoke test against real prompts

## Install sequence

### 1. Confirm ClickUp access

- verify the ClickUp MCP/auth route is already working
- do not ask the user for a new token until the known local auth path has been checked

### 2. Resolve the live defaults

Collect:

- workspace ID and workspace name
- default space name
- general to-do list ID and name
- ideas list ID and name
- default assignee ID and name
- active status vocabulary actually used in that workspace

### 3. Create a real config from the template

- copy `templates/config.template.yaml`
- fill in the live values
- keep the skill body generic; put the account-specific details only in config

### 4. Run the smoke test

Use `examples/internal-smoke-test.md`.

Minimum pass criteria:

- a general to-do routes correctly
- an idea routes correctly
- a project-contained task does not auto-assign or auto-date
- today's-list read only returns today's assigned active items

## Internal-release bar

Before calling the internal version ready:

- no hardcoded Sam-specific IDs remain in the skill body
- the config template is sufficient to onboard another internal workspace
- at least one real live workspace has been validated end to end
- any MCP quirks discovered during testing are documented
