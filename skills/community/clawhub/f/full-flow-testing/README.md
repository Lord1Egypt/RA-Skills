# End-to-End API Testing Expert Skill

An enterprise API testing assistant that supports six testing modes.

## Features

- **Developer Self-Test Mode**: fast smoke testing + basic validation
- **Single API Deep Test**: complete test cases, exception testing, and boundary testing
- **Business Flow Test**: end-to-end integration testing
- **Security Audit Mode**: privilege escalation, unauthorized access, and sensitive data exposure checks
- **Defect Diagnosis Mode**: root cause analysis when bugs occur
- **Report Generation Mode**: output a full consolidated report

## Quick Start

1. Trigger command: `!test` or "testing assistant"
2. Provide a username to create an isolated workspace
3. Select a testing mode to start

## Directory Structure

```
test-engineer/
├── SKILL.md          # Core Skill definition and usage specification
├── README.md         # This file
└── examples/         # Example code
    └── simple_api_test_example.py  # Simple API test example
```

## Configuration

The following variables can be configured in the Skill:

- `GLOBAL_KB_PATH`: global knowledge base root directory (default: `./company_api_knowledge`)
- `USER_WORKSPACE_BASE`: user workspace base directory (default: `./test_assistant_users`)

## Usage Example

```
User: !test
Assistant: Please provide your username or employee ID...

User: zhangsan
Assistant: [Workspace created] Please choose a mode: 1. Developer Self-Test 2. Single API Deep Test...

User: !test mode 1
Assistant: [Report self-test plan and wait for confirmation]
```

## More Information

See [SKILL.md](./SKILL.md) for the complete usage specification.
