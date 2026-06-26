# Probe File

Use an extra probe file when the default detector is not enough.

The built-in detector already covers:

- Git
- Java
- `javac`
- Maven
- Gradle
- Node
- npm
- pnpm
- Yarn
- Python
- Go
- Rust (`rustc`, Cargo, Rustup)
- Clang, Clang++, GCC, G++, CMake, Make, Ninja
- Ruby, RubyGems, Bundler
- PHP, Composer
- .NET SDK
- Docker
- kubectl
- `JAVA_HOME`
- `MAVEN_HOME`
- `GRADLE_HOME`, `GOROOT`, `GOPATH`, `CARGO_HOME`, `RUSTUP_HOME`, `DOTNET_ROOT`, `CC`, `CXX`
- common runtime-manager env vars such as `NVM_DIR`, `PYENV_ROOT`, `RBENV_ROOT`, `SDKMAN_DIR`, `HOMEBREW_PREFIX`, and `VIRTUAL_ENV`
- important PATH entries on Windows, macOS, and Linux

For services, databases, startup scripts, or project-specific tools, create a JSON file and pass it through `--probe-file`.

## Supported Keys

```json
{
  "tools": [
    {
      "id": "docker",
      "label": "Docker",
      "commands": ["docker"],
      "version_command": ["{selected_executable}", "--version"],
      "version_regex": "Docker version\\s+([^,\\s]+)"
    }
  ],
  "env_vars": ["DOCKER_HOST", "GRADLE_HOME"],
  "important_path_contains": ["Docker", "Gradle"],
  "checks": [
    {
      "id": "postgres-service",
      "label": "PostgreSQL Service",
      "command": ["sc.exe", "query", "postgresql-x64-16"],
      "success_patterns": ["RUNNING"]
    }
  ]
}
```

## Tool Fields

- `id`
  - Stable tool id used in `--tools`.
- `label`
  - Human-readable display name for docs.
- `commands`
  - Lookup commands used to resolve PATH hits.
- `commands_windows` / `commands_posix` / `commands_macos` / `commands_linux`
  - Optional platform-specific overrides for command lookup.
- `version_command`
  - Command used to extract a version.
  - Use `{selected_executable}` to reuse the final chosen executable path.
- `version_regex`
  - Regex with one capture group for the version string.
- `env_var_hint`
  - Optional env var whose value points at the install root.
- `env_var_suffix_windows` / `env_var_suffix_posix`
  - Optional path segments appended to the env var value to form the executable path.

## Check Fields

- `id`
  - Stable identifier for the check.
- `label`
  - Human-readable name for docs.
- `command`
  - Command array executed exactly as provided.
- `capture`
  - Optional. One of `stdout`, `stderr`, or `combined`. Defaults to `combined`.
- `success_patterns`
  - Optional list of regex patterns that must all match for the check to pass.
- `timeout`
  - Optional timeout in seconds.
- `cwd`
  - Optional working directory for the check.

## Example: Windows Services and Ports

```json
{
  "checks": [
    {
      "id": "postgres-service",
      "label": "PostgreSQL Service",
      "command": ["sc.exe", "query", "postgresql-x64-16"],
      "success_patterns": ["RUNNING"]
    },
    {
      "id": "redis-port",
      "label": "Redis Port 6379",
      "command": [
        "powershell",
        "-NoProfile",
        "-Command",
        "Test-NetConnection -ComputerName 127.0.0.1 -Port 6379 | Format-List"
      ],
      "success_patterns": ["TcpTestSucceeded : True"]
    }
  ]
}
```

## Example: macOS and Linux Services

```json
{
  "tools": [
    {
      "id": "docker",
      "label": "Docker",
      "commands": ["docker"],
      "version_command": ["{selected_executable}", "--version"],
      "version_regex": "Docker version\\s+([^,\\s]+)"
    }
  ],
  "checks": [
    {
      "id": "systemd-docker",
      "label": "Docker systemd service",
      "command": ["systemctl", "is-active", "docker"],
      "success_patterns": ["active"]
    },
    {
      "id": "launchd-postgres",
      "label": "PostgreSQL launchd service",
      "command": ["launchctl", "print", "system/homebrew.mxcl.postgresql@16"],
      "success_patterns": ["state = running"]
    },
    {
      "id": "shell-startup",
      "label": "Shell startup file",
      "command": ["bash", "-lc", "test -f ~/.zshrc || test -f ~/.bashrc"],
      "success_patterns": []
    }
  ]
}
```

## Example: Gradle and MySQL

```json
{
  "tools": [
    {
      "id": "gradle",
      "label": "Gradle",
      "commands": ["gradle"],
      "version_command": ["{selected_executable}", "--version"],
      "version_regex": "Gradle\\s+([0-9.]+)"
    },
    {
      "id": "mysql",
      "label": "MySQL Client",
      "commands": ["mysql"],
      "version_command": ["{selected_executable}", "--version"],
      "version_regex": "Distrib\\s+([0-9.]+)"
    }
  ],
  "env_vars": ["GRADLE_HOME", "MYSQL_HOME"],
  "important_path_contains": ["Gradle", "MySQL"]
}
```

## Usage

Windows PowerShell:

```powershell
python scripts/detect_environment.py --probe-file .\extra-probes.json --output .\environment-baseline.json
```

macOS / Linux:

```bash
python3 scripts/detect_environment.py --probe-file ./extra-probes.json --output ./environment-baseline.json
```

Targeted refresh:

```bash
python3 scripts/detect_environment.py \
  --baseline ./environment-baseline.json \
  --probe-file ./extra-probes.json \
  --tools gradle,mysql \
  --output ./environment-baseline.json
```
