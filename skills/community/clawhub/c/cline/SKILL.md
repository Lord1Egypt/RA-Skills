---
name: cline
description: >
  Run the local Cline CLI to plan/build/code and return the output.
requirements:
  - command: cline
    description: Cline CLI must be installed and on PATH
usage:
  - title: Run Cline headless
    command: cline -y "<TASK>"
    notes: |
      Use for coding, scaffolding, debugging, and multi-step plans.
      Keep prompts short and task-oriented.
examples:
  - 'cline -y "Create hello.sh that prints date and uname -a."'
  - 'cline -y "Refactor this repo: add README and scripts folder."'
safety:
  - Never paste secrets.
  - Ask before destructive commands.
