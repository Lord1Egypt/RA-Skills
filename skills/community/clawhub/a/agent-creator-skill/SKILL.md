---
name: create_agent
description: Automatically create a new OpenClaw agent, translate its name, and initialize its persona/system prompt based on user requests.
parameters:
  type: object
  properties:
    agent_name_en:
      type: string
      description: "The translated English short ID for the agent. Snake_case, lowercase only. Example: 'java_expert'."
    agent_display_name:
      type: string
      description: "The friendly display name for the agent, written in the same language as the user's request unless the user specifies another language. Example: 'Java高级专家' or 'Senior Java Expert'."
    identity_prompt:
      type: string
      description: "A highly detailed persona description and system prompt, written in the same language as the user's request unless the user specifies another language."
  required:
    - agent_name_en
    - agent_display_name
    - identity_prompt
---

# Agent Creator Skill

When a user asks you to create a new agent, assistant, or proxy (e.g., "创建一个Java高级开发的代理", "Help me build a product manager agent"), you MUST use this skill to accomplish the task.

## SOP (Standard Operating Procedure):

1. **Translation**: Translate the requested role into a short English snake_case string. This will be the `<agent_name_en>`.
2. **Language Matching**: Detect the primary language of the user's request. Use that language for both `<agent_display_name>` and `<identity_prompt>`, unless the user explicitly asks for another language.
3. **Persona Generation**: Generate a professional, highly detailed system prompt for this specific role. This will be the `<identity_prompt>`.
4. **Execution**: Choose the script that matches the user's operating system:
   - On Linux, macOS, WSL, or Git Bash:
   ```bash
   bash {baseDir}/create_agent.sh "<agent_name_en>" "<agent_display_name>" "<identity_prompt>"
   ```
   - On native Windows PowerShell:
   ```powershell
   powershell -ExecutionPolicy Bypass -File "{baseDir}/create_agent.ps1" -AgentId "<agent_name_en>" -DisplayName "<agent_display_name>" -IdentityPrompt "<identity_prompt>"
   ```
