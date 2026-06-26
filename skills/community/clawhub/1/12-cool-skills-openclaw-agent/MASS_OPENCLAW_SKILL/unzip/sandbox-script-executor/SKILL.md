---
name: sandbox-script-executor
description: Executes scripts in the sandbox environment and returns the output. Supports various languages (Python, Bash, Node.js) and handles dependency installation. Use this when a user provides a script to run or asks to execute code within the sandbox.
---

# Sandbox Script Executor

This skill allows the agent to execute user-provided scripts within the secure sandbox environment and return their output. It supports multiple programming languages and includes mechanisms for automatic dependency management.

## Workflow

When a user requests to execute a script or run code in the sandbox, follow these steps:

### 1. Obtain Script Details

- **Script Content**: Ask the user to provide the full content of the script they wish to execute.
- **Language**: Determine the programming language of the script (e.g., Python, Bash, Node.js). If not specified, ask the user.
- **Dependencies (Optional)**: Inquire about any specific libraries or packages required by the script. If a `requirements.txt` (Python) or `package.json` (Node.js) is provided, use it.

### 2. Prepare Environment and Install Dependencies

- **Save Script**: Save the user-provided script content to a file in the sandbox (e.g., `/home/ubuntu/script.py`, `/home/ubuntu/script.sh`, `/home/ubuntu/script.js`).
- **Install Dependencies**: Before execution, attempt to install any specified dependencies. Refer to `references/execution_guide.md` for common dependency management commands (e.g., `pip3 install`, `npm install`). If dependencies are not explicitly mentioned, try to infer them or ask the user.

### 3. Execute Script

- **Execute Command**: Use the appropriate command to execute the script based on its language. Refer to `references/execution_guide.md` for execution commands (e.g., `python3`, `bash`, `node`).
- **Capture Output**: Ensure that both standard output (stdout) and standard error (stderr) are captured during execution.

### 4. Report Results

- **Success**: If the script executes successfully, return the stdout to the user.
- **Failure**: If the script fails, report the stderr to the user, along with any relevant error messages. Attempt to diagnose common issues (e.g., missing dependencies, syntax errors) and suggest solutions.

## Supported Languages and Dependency Management

This skill supports:

- **Python**: Execution via `python3`, dependency management via `pip3`.
- **Bash**: Execution via `bash`, system package management via `apt-get` (requires `sudo`).
- **Node.js**: Execution via `node`, dependency management via `npm` or `pnpm`.

For detailed commands and examples, refer to `references/execution_guide.md`.

## Example Usage

**User Request:** "Run this Python script: `print('Hello, Sandbox!')`"

**Agent Action (Conceptual):**
1. Save script to `/home/ubuntu/temp_script.py`.
2. Execute `python3 /home/ubuntu/temp_script.py`.
3. Return output: "Hello, Sandbox!"

**User Request:** "Execute this Node.js script that uses `axios`: `const axios = require('axios'); axios.get('https://api.example.com').then(res => console.log(res.data));`"

**Agent Action (Conceptual):**
1. Save script to `/home/ubuntu/temp_script.js`.
2. Install `axios`: `npm install axios`.
3. Execute `node /home/ubuntu/temp_script.js`.
4. Return API response data.
