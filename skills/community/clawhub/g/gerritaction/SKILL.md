# Gerrit Action Skill

Use the `gerritaction` worker to query Gerrit resources and apply actions to matching changes through the Gerrit API.

## When to use

Use this skill when the user wants to:

- query Gerrit accounts
- query Gerrit changes
- query Gerrit groups
- query Gerrit projects
- add or delete reviewers on matching changes
- add or remove attention set members on matching changes
- approve, submit, or delete matching changes

## Worker configuration

The worker is configured by `skill/config.yml`:

```yaml
apiVersion: v1
kind: worker
metadata:
	name: gerritaction
spec:
	gerrit:
		host: http://127.0.0.1/
		port: 8080
		user: user
		pass: pass
```

Required fields:

- `apiVersion`: `v1`
- `kind`: `worker`
- `metadata.name`: `gerritaction`
- `spec.gerrit.host`: Gerrit base URL including scheme
- `spec.gerrit.port`: Gerrit port
- `spec.gerrit.user`: Gerrit username
- `spec.gerrit.pass`: Gerrit password

## Invocation rules

- Install the package with `pip install gerritaction` before running commands.
- Invoke the CLI as `gerritaction` instead of `python action.py`.
- Always provide `--config-file` with a `.yml` or `.yaml` file.
- Provide exactly one query selector: `--account-query`, `--change-query`, `--group-query`, or `--project-query`.
- Only use `--change-action` together with `--change-query` in the same invocation.
- Use `--output-file` only for a new `.json` file path. The command rejects an existing file.
- If `--output-file` is omitted, query results are printed to standard output as JSON.

## Supported queries

### Account query

Use `--account-query` to search accounts.

Example:

```bash
pip install gerritaction
gerritaction --config-file="skill/config.yml" --account-query="name:john email:example.com"
```

### Change query

Use `--change-query` to search changes.

Example:

```bash
pip install gerritaction
gerritaction --config-file="skill/config.yml" --change-query="status:open since:2024-01-01 until:2024-01-02"
```

### Group query

Use `--group-query` to search groups.

Example:

```bash
pip install gerritaction
gerritaction --config-file="skill/config.yml" --group-query="name:admin member:john"
```

### Project query

Use `--project-query` to search projects. Project results are enriched with project config, branches, and tags.

Example:

```bash
pip install gerritaction
gerritaction --config-file="skill/config.yml" --project-query="name:test state:active"
```

## Supported change actions

The worker supports these change actions:

- `add-reviewer:account-id[,account-id...]`
- `delete-reviewer:account-id[,account-id...]`
- `add-attention:account-id[,account-id...]`
- `remove-attention:account-id[,account-id...]`
- `approve-change:Label=Value[,Label=Value...]`
- `delete-change`
- `submit-change`

Multiple actions can be chained in one `--change-action` value, separated by spaces.

Example:

```bash
pip install gerritaction
gerritaction \
	--config-file="skill/config.yml" \
	--change-query="status:open project:test" \
	--change-action="add-reviewer:1001,1002 approve-change:Code-Review=+2"
```

## Output handling

- Use `--output-file` when the caller needs a persistent JSON artifact.
- Account, change, group, and project queries return JSON.
- Change actions operate on the changes returned by `--change-query`.

Example:

```bash
pip install gerritaction
gerritaction \
	--config-file="skill/config.yml" \
	--project-query="name:test state:active" \
	--output-file="/tmp/projects.json"
```

## Safety guidance

- Prefer a query-only run before destructive or state-changing actions.
- Before `delete-change` or `submit-change`, make sure the change query is narrow and explicit.
- If the user request is ambiguous, ask for the exact Gerrit query or target account IDs before generating the final command.

## Recommended behavior for the agent

- Generate commands that match the repository CLI exactly.
- Keep queries and actions explicit rather than inferred.
- When performing change actions, include both `--change-query` and `--change-action` in the same command.
- When the user asks for structured output, add `--output-file` with a new `.json` path.
- Surface invalid combinations early, especially a `--change-action` without `--change-query`.
