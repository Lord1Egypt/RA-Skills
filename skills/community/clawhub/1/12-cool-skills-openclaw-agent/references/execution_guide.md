# Sandbox Script Execution Guide

This guide provides instructions for executing scripts and managing dependencies within the sandbox environment.

## Supported Languages and Commands

| Language | Execution Command | Dependency Manager |
| :--- | :--- | :--- |
| **Python** | `python3 <script.py>` | `pip3 install <package>` |
| **Bash** | `bash <script.sh>` | `apt-get install <package>` (requires sudo) |
| **Node.js** | `node <script.js>` | `npm install <package>` or `pnpm add <package>` |

## Automatic Dependency Management

Before executing a script, identify its dependencies and install them if they are missing.

### Python
```bash
# Check for dependencies in the script and install them
pip3 install -r requirements.txt
# Or individual packages
pip3 install <package_name>
```

### Node.js
```bash
# Install dependencies from package.json
npm install
# Or individual packages
npm install <package_name>
```

## Error Handling and Result Capture

- Always capture the standard output (stdout) and standard error (stderr) of the execution.
- If an execution fails, analyze the stderr to identify the cause (e.g., missing dependency, syntax error).
- Report the final output or error message clearly to the user.
