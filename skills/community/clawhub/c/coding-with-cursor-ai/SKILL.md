# coding-with-cursor-ai

## Description
Execute coding tasks using Cursor AI agent for advanced code generation, refactoring, and bug fixes. This skill is designed to handle complex logic changes, feature implementations, and code reviews within the `/home/ubuntu/workspace` projects.

## Usage
Use this skill whenever:
- Implementing new features
- Fixing bugs
- Refactoring code
- Writing unit tests
- Performing code reviews

## Inputs
- `project`: Path to the project root (e.g., `/home/ubuntu/workspace/zinner/repo/zinner-webapi`)
- `task`: Natural language description of the coding task
- `files`: Optional list of files to focus on

## Execution
The skill spawns a Cursor AI agent session with full access to the project repository. It uses Cursor's advanced reasoning and code editing capabilities to complete the task and commit changes.

## Constraints
- Always verify Cursor's edits before final commit
- Do not run Cursor on production branches without review
- Prefer `dev` or feature branches for automated coding

## Example
```yaml
project: /home/ubuntu/workspace/zinner/repo/zinner-webcms
task: Add Terms and Conditions page with dummy content
```
