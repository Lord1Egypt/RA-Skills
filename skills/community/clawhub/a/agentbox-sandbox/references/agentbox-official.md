# AgentBox official docs summary

This reference condenses the official documentation at `https://agentbox.cloud/docs` for the most common support and how-to questions.

## 1. What AgentBox is

- AgentBox runs AI-generated code inside secure cloud sandboxes.
- The docs say the Python SDK is the main way to start and control sandboxes.
- Supported platforms include x86 and Android.

## 2. Quickstart

### CLI path

1. Install CLI:

```bash
npm install -g agentbox-cli
```

2. Authenticate:

```bash
agentbox auth login -u your_email -p your_password
```

3. Initialize and build a template:

```bash
agentbox template init
agentbox template build --platform linux_x86
```

4. Start a sandbox from the template id:

```bash
agentbox sandbox sp ${TEMPALTE_ID}
```

### Python SDK path

```bash
pip install agentbox-python-sdk
export AGENTBOX_DOMAIN=agentbox.cloud
export AGENTBOX_API_KEY=ab_******
```

Minimal example:

```python
from agentbox import Sandbox

sandbox = Sandbox(
    api_key="ab_xxxxxxxxxxxxxxxxxxxxxxxxx",
    template="<YOUR_TEMPLATE_ID>",
    timeout=120,
)
result = sandbox.commands.run("ls -l")
```

## 3. Lifecycle and timeout

- By default, a sandbox stays alive for 5 minutes.
- `timeout` is measured in seconds.
- You can inspect sandbox info with `get_info()`.
- You can reset the remaining lifetime while the sandbox is running with `set_timeout(seconds)`.

Example:

```python
from agentbox import Sandbox

sandbox = Sandbox(
    api_key="ab_xxxxxxxxxxxxxxxxxxxxxxxx",
    template="wemmodr8mb2uk3kn7exw",
    timeout=60,
)

info = sandbox.get_info()
print(info.started_at)
print(info.end_at)

sandbox.set_timeout(30)
```

## 4. Running commands

Use `sandbox.commands.run(command)`.

It returns a command result with stdout, stderr, and exit code.

```python
result = sandbox.commands.run("ls -l")
print(result.stdout)
print(result.stderr)
print(result.exit_code)
```

## 5. Filesystem read and write

### Read

```python
file_content = sandbox.files.read("/path/to/file")
```

### Write

```python
sandbox.files.write("/path/to/file", "file content")
```

Notes:
- `write()` overwrites the file if it already exists.
- The docs also describe writing multiple files with the same interface family.

## 6. Environment variables

There are three documented patterns.

### Global envs at sandbox creation

```python
sandbox = Sandbox(
    api_key="ab_xxxxxxxxxxxxxxxxxxxxxxxxx",
    template="wemmodr8mb2uk3kn7exw",
    timeout=60,
    envs={"MY_VAR": "my_value"},
)
```

### Scoped envs for `run_code`

Recommended for secrets that should apply only to one code execution.

```python
sandbox.run_code(
    'import os; print(os.environ.get("MY_VAR"))',
    envs={"MY_VAR": "my_value"},
)
```

### Scoped envs for `commands.run`

Recommended for secrets that should apply only to one shell command.

```python
sandbox.commands.run(
    "echo $MY_VAR",
    envs={"MY_VAR": "123"},
)
```

Notes:
- Scoped envs are not persisted globally inside the sandbox.
- Scoped envs override any global env with the same name only for that execution.

## 7. Custom sandbox templates

AgentBox uses `agentbox.Dockerfile` to define a custom template.

Flow:
1. Install CLI
2. Authenticate
3. Run `agentbox template init`
4. Edit `agentbox.Dockerfile`
5. Build with:

```bash
agentbox template build --platform linux_x86 -p YOUR_WORKPATH
```

6. Start sandbox with the returned template id:

```bash
agentbox sandbox sp ${YOUR_TEMPLATE_ID}
```

Notes:
- The docs say the Dockerfile follows standard Dockerfile syntax.
- Building a template can take a few minutes.

## 8. What not to claim from this skill

Do not claim support for undocumented features such as:
- hidden CLI flags
- unpublished REST endpoints
- unsupported auth flows
- SDK methods not shown in the official docs summary above
