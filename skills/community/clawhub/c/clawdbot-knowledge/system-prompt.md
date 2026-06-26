# System Prompt Reference

## Overview

OpenClaw creates custom system prompts for each agent run. This prompt is OpenClaw-specific and does not use the p-coding-agent's default prompt. The prompt is assembled by OpenClaw and inserted into every agent run.

## Prompt Structure

### Component Assembly
The system prompt is intentionally kept compact with fixed sections:

1. **Tooling**: Current tool list + short descriptions
2. **Security**: Brief guardrail as reminder to avoid power-seeking behavior or oversight evasion
3. **Capabilities**: Tells the model how skills instructions can be loaded when needed
4. **OpenClaw Self-Update**: How to execute config.apply and update.run
5. **Workspace**: Working directory (agents.defaults.workspace)
6. **Documentation**: Local path to OpenClaw documentation (repo or npm package) and when to read it
7. **Workspace Files (Injected)**: Shows that bootstrap files are included below
8. **Sandbox**: Shows runtime environment in sandbox, sandbox paths, elevated execution rights availability
9. **Current Date & Time**: User time, timezone, time format
10. **Reply Tags**: Optional syntax for reply tags in supported providers
11. **Heartbeats**: Heartbeat prompt and acknowledgment behavior
12. **Runtime**: Host, OS, node, model, repo root (if detected), thinking level (one line)
13. **Reasoning**: Current visibility level + /reasoning toggle hint

### Prompt Modes
OpenClaw can render smaller system queries for subagents. The runtime environment sets a promptMode for each run (no user configuration):

**full (default)**
- Includes all sections listed above
- Used for main agent execution
- Complete context and capabilities

**minimal**
- Used for subagents
- Excludes: Capabilities, Memory recall, OpenClaw self-update, model aliases, user identity, reply tags, messages, silent replies, heartbeats
- Keeps: Tools, security, workspace, sandbox, current date/time (if known), runtime environment, injected context
- Purpose: Reduce token usage for subagent tasks

**none**
- Returns only base identity line
- Used for very simple subagents
- Minimal context for basic tasks

### Additional Prompt for Subagent Context
If additional injected prompts are designated as "subagent context" rather than "group chat context", promptMode=minimal is used.

## Workspace Bootstrap Injection

### File Injection Process
Bootstrap files are truncated and appended under Project Context, so the model sees identity and profile context without requiring explicit reads:

**Standard Bootstrap Files:**
- AGENTS.md
- SOUL.md  
- TOOLS.md
- IDENTITY.md
- USER.md
- HEARTBEAT.md
- BOOTSTRAP.md (only in brand new workspaces)

### Injection Rules
- **Maximum File Size**: Limited by agents.defaults.bootstrapMaxChars (default 20000 bytes)
- **Large Files**: Truncated with truncation marker
- **Missing Files**: Short marker added indicating missing file
- **Internal Hooks**: agent:bootstrap hook can intercept this step to alter/replace injected bootstrap files (e.g., swap SOUL.md for alternative persona)

### Example Injection Format
```
## Project Context

### AGENTS.md
[Content of AGENTS.md file, truncated if necessary]

### SOUL.md  
[Content of SOUL.md file]

### TOOLS.md
[Content of TOOLS.md file, may be truncated]

[... other files ...]
```

### File Size Calculation
The system tracks both raw and injected sizes:
```python
{
    "filename": "TOOLS.md",
    "raw_size": 54210,
    "injected_size": 20962,
    "status": "TRUNCATED"
}
```

## Time Management

### Time Section
The system query includes a separate section for date and time if the user's timezone is known:
```
## Current Date & Time
**Date:** 2026-02-07
**Timezone:** UTC
**Time Format:** 24-hour
```

### Cache Stability
To ensure query cache stability, only the timezone is displayed (no dynamic time or dynamic time format).

### Configuration
Configure with:
- `agents.defaults.userTimezone`: User's timezone (e.g., "Europe/Berlin", "America/New_York")
- `agents.defaults.timeFormat`: Time format (auto | 12 | 24)

### Session Status for Current Time
If the agent needs the current time, use `session_status` - the status card includes a timestamp line.

## Capabilities Section

### Skills Integration
If appropriate skills are present, OpenClaw adds a compact list of available skills to the prompt using the SkillsForPrompt format for each skill.

### Skills Loading Logic
The prompt instructs the model to:
```
When you need to use a capability, read the SKILL.md file at the specified location (workspace, managed, or bundled).
```

### Skills Selection
The system reads skills from three locations (workspace wins on name conflicts):
1. **Bundled**: Shipped with installation
2. **Managed/Local**: ~/.openclaw/skills  
3. **Workspace**: <workspace>/skills

### Prompt Section Format
```
## Capabilities

The following skills are available:

- **frontend-design**: Create and design frontend web interfaces and components. Location: /home/deepall/.npm-global/lib/node_modules/clawdbot/skills/frontend-design
- **oracle**: Provide insights, predictions, and wisdom-based guidance. Location: /home/deepall/clawd/skills/oracle
- **gemini**: Gemini CLI for one-shot Q&A, summaries, and generation. Location: /home/deepall/.npm-global/lib/node_modules/clawdbot/skills/gemini

[... more skills ...]

When you need to use a capability, read the SKILL.md file at the specified location.
```

### Missing Skills Handling
If no appropriate skills are available, the "Capabilities" section is omitted entirely to save tokens.

## Documentation Section

### Documentation References
If available, the system query includes a documentation section that references:
- **Local OpenClaw Documentation**: docs/ directory in workspace repository OR in shipped npm package
- **Public Mirror**: https://docs.clawd.bot
- **Source Repository**: https://github.com/clawdbot/clawdbot
- **Community Discord**: https://discord.com/invite/clawd
- **ClawHub (Skills):** https://clawdhub.com

### Model Instructions
The query instructs the model to:
```
For OpenClaw behavior, commands, configuration, or architecture, consult local documentation first when possible. If you have access, run openclaw status yourself to check system state.
```

### Documentation Priority
1. **Local Documentation**: First choice for OpenClaw-specific information
2. **Direct Commands**: Run `openclaw status` when possible
3. **Public Resources**: Fall back to public mirror and community
4. **User Questions**: Only ask user if no access to local documentation

## Runtime Section

### Runtime Information
The prompt includes a single-line runtime information section:
```
## Runtime
**Host:** faton-ubuntu | **OS:** Linux 6.8.0-94-generic (x64) | **Node:** main | **Model:** openrouter/z-ai/glm-4.5 | **Default Model:** openrouter/z-ai/glm-4.5 | **Channel:** webchat | **Capabilities:** none | **Thinking:** low
```

### Information Fields
- **Host**: Hostname where Gateway is running
- **OS**: Operating system and architecture
- **Node**: Node type (main, agent, etc.)
- **Model**: Current model in use
- **Default Model**: Fallback model configuration
- **Channel**: Communication channel (webchat, telegram, discord, etc.)
- **Capabilities**: Available capabilities
- **Thinking**: Current reasoning level (off, low, medium, high)

### Repository Detection
If the workspace is a git repository, the repo root is detected and included in model references.

## Reasoning Section

### Reasoning Visibility
The prompt includes current reasoning visibility and toggle hint:
```
## Reasoning
**Visibility:** off | **Toggle:** /reasoning
```

### Visibility Levels
- **off**: Reasoning not visible to user
- **low**: Basic reasoning visible
- **medium**: Detailed reasoning visible  
- **high**: Comprehensive reasoning visible

### Toggle Command
Users can toggle reasoning visibility with `/reasoning` command during conversation.

## Security Section

### Security Guidelines
The security precautions shown in the system prompt window are recommendations. They control model behavior but do not enforce policies.

### Actual Enforcement
For strict enforcement, use:
- **Tool policies**: Control what tools can be called
- **Supervisor approvals**: Require human approval for sensitive operations
- **Sandboxing**: Restrict file system and network access
- **Channel allowlists**: Limit what channels can be used

### Security Wording
```
## Security
- Don't exfiltrate private data. Ever.
- Don't run destructive commands without asking.
- Use `trash` > `rm` (recoverable beats gone forever)
- When in doubt, ask.
```

## Tooling Section

### Tool List
The prompt includes a list of available tools with short descriptions:
```
## Tooling

**Available Tools:**
- **read**: Read file contents (text files and images)
- **edit**: Edit file by replacing exact text
- **write**: Write content to file
- **exec**: Execute shell commands
- **process**: Manage running exec sessions
```

### Tool Schema Cost
Tools affect context in two ways:
1. **Tool List Text**: Shown in prompt (what user sees as "tools")
2. **Tool Schemas (JSON)**: Sent to model so it can call tools, count toward context even if not visible

### Large Schema Handling
For tools with large schemas, use `/context detail` to see which tools dominate context usage.

## Heartbeats Section

### Heartbeat Instructions
The prompt includes heartbeat behavior instructions:
```
## Heartbeats
When you receive a heartbeat poll (message matches configured heartbeat prompt), don't just reply HEARTBEAT_OK every time. Use heartbeats productively.

Default heartbeat prompt:
"Read HEARTBEAT.md if it exists (workspace context). Follow it strictly. Do not infer or repeat old tasks from prior chats. If nothing needs attention, reply HEARTBEAT_OK."
```

### Productive Heartbeat Usage
The model is encouraged to:
- Check email, calendar, notifications
- Look for important events or issues
- Perform background work
- Review and update MEMORY.md
- Only reply HEARTBEAT_OK when nothing needs attention

### Heartbeat vs Cron
The prompt explains when to use heartbeats vs cron:
- **Heartbeat**: Multiple checks together, conversational context, timing can drift
- **Cron**: Exact timing, task isolation, different model/thinking level, one-shot reminders

## Reply Tags Section

### Reply Tag Support
For platforms that support reply tags, the prompt includes optional syntax:
```
## Reply Tags
Optional reply tag syntax for supported platforms:
- [[reply_to_current]] - replies to triggering message
- [[reply_to:<id>]] - replies to specific message id when you have it
```

### Tag Processing
Whitespace inside tags is allowed. Tags are stripped before sending. Support depends on current channel configuration.

## Prompt Optimization

### Token Management
The system prompt is designed to be concise while providing essential information:
- **Estimated Size**: ~38,412 characters (~9,603 tokens) for system prompt
- **Project Context**: ~23,901 characters (~5,976 tokens) for injected files
- **Total Context**: Varies by model, typically 32K-128K tokens

### Context Inspection
Use these commands to inspect context usage:
- `/status` - Quick view of context window usage
- `/context list` - What gets injected + sizes
- `/context detail` - Detailed breakdown by component
- `/usage tokens` - Add usage stats to responses

### Context Optimization
When context is full:
1. Use `/compact` to summarize older history
2. The system may trigger automatic compaction
3. Large files are automatically truncated
4. Skills are loaded on-demand, not all at once

## Prompt Customization

### Hooks
Use the `agent:bootstrap` hook to customize prompt assembly:
```python
def agent_bootstrap_hook(params):
    # Add custom sections to system prompt
    if should_add_custom_section():
        params["system_prompt"] += "\n\n## Custom Section\n..."
    
    # Replace standard sections
    if use_alternative_security():
        params["system_prompt"] = replace_security_section(params["system_prompt"])
    
    return params
```

### Dynamic Prompts
The prompt can be modified at runtime based on:
- **User preferences**: Customized instructions or tone
- **Task requirements**: Specialized prompts for specific tasks
- **Environment**: Different prompts for development vs production
- **Model capabilities**: Adjusted based on model context window

### Prompt Validation
The system validates prompts before sending to model:
- **Size Check**: Ensure within model context limits
- **Structure Check**: Verify required sections present
- **Content Check**: Ensure no harmful or inappropriate content
- **Format Check**: Verify proper markdown and structure

## Troubleshooting

### Common Issues

#### Prompt Too Large
- **Symptom**: Model refuses response or cuts off
- **Solution**: Use `/compact`, reduce injected files, increase model context limit
- **Check**: `/context detail` to see largest components

#### Missing Bootstrap Files
- **Symptom**: [MISSING: filename] markers in prompt
- **Solution**: Create missing files or use `openclaw setup` to generate defaults
- **Check**: Verify workspace directory and file permissions

#### Skills Not Loading
- **Symptom**: Skills section missing or incomplete
- **Solution**: Check skill locations, verify skill.md files exist
- **Check**: Use `/context detail` to see skill loading status

#### Timezone Issues
- **Symptom**: Wrong time displayed or missing
- **Solution**: Configure `agents.defaults.userTimezone` and verify timezone format
- **Check**: Use `session_status` to see current time information

### Debug Commands
```bash
# Check current prompt composition
openclaw context detail

# Test prompt generation
openclaw agent --dry-run --prompt-only

# Validate prompt structure
openclaw prompt validate

# Optimize prompt for model
openclaw prompt optimize --model <model-name>
```