# Workspace Management Reference

## Overview

The workspace is the agent's working directory - the sole directory used for file tools and workspace context. Protect it and treat it like memory. This is separate from ~/.openclaw/, which stores configurations, credentials, and sessions.

## Important Notes
- **Default Working Directory**: Not a strict sandbox
- **Tool Behavior**: Tools resolve relative paths in workspace, but absolute paths can still access other host areas if sandbox is not enabled
- **Isolation**: Use `agents.defaults.sandbox` for isolation (and/or agent-specific sandbox configuration)
- **Sandbox Behavior**: When sandbox enabled and `workspaceAccess` not set to "rw", tools work in sandbox workspace under `~/.openclaw/sandboxes` current host working directory, not host workspace

## Standard Location

### Default Paths
- **Default**: `~/.openclaw/workspace`
- **With Profile**: `~/.openclaw/workspace-<profile>` (if OPENCLAW_PROFILE set and not "default")
- **Configuration Override**: Set in `~/.openclaw/openclaw.json`:
  ```json
  {
    "agent": {
      "workspace": "~/.openclaw/workspace"
    }
  }
  ```

### Workspace Initialization
- **Command**: `openclaw onboard`, `openclaw configure`, or `openclaw setup` creates workspace and injects bootstrap files if missing
- **Skip Bootstrap**: Disable bootstrap file creation with:
  ```json
  { "agent": { "skipBootstrap": true } }
  ```

## Additional Workspace Folders

### Multiple Workspaces Issue
- **Problem**: Older installations may have `~/openclaw`
- **Risk**: Multiple workspace directories can cause confusing authentication or status deviations - only one workspace is active
- **Solution**: Use only one active workspace
- **Cleanup**: Archive or move (e.g., `trash ~/openclaw`) if not needed
- **Verification**: `openclaw doctor` warns when additional workspace directories detected

### Workspace Configuration
- **Active Workspace**: Ensure `agents.defaults.workspace` points to active workspace
- **Profile Management**: Different profiles can use different workspaces

## Workspace Files Overview (Meaning of Individual Files)

### Required Bootstrap Files
OpenClaw expects these user-editable files inside `agents.defaults.workspace`:

#### AGENTS.md
- **Purpose**: Agent instructions and memory usage
- **Loading**: Loaded at beginning of every session
- **Content**: Good place for rules, priorities, behavior details
- **Importance**: Core agent personality and operational guidelines

#### SOUL.md  
- **Purpose**: Personality, tone, and boundaries
- **Loading**: Loaded every session
- **Content**: How the agent should behave, interact, respond
- **Importance**: Defines agent's character and interaction style

#### USER.md
- **Purpose**: Who is the user and how to address them
- **Loading**: Loaded every session  
- **Content**: User profile, preferences, communication style
- **Importance**: Personalizes agent for specific user

#### IDENTITY.md
- **Purpose**: Agent name, vibe, and emoji
- **Creation/Update**: Created/updated during bootstrap ritual
- **Loading**: Loaded every session
- **Content**: Agent's self-identification and signature
- **Importance**: Establishes agent identity and branding

#### TOOLS.md
- **Purpose**: User's local tool notes and conventions
- **Loading**: Loaded every session
- **Content**: Notes about local tools, preferences, setup details
- **Guarantee**: Does not ensure tool availability - just policy guidance
- **Importance**: Helps agent understand local environment and tools

#### HEARTBEAT.md
- **Purpose**: Optional small checklist for heartbeat runs
- **Loading**: Loaded every session
- **Content**: Short list of periodic check tasks
- **Optimization**: Keep short to limit token burn
- **Importance**: Enables proactive agent behavior

#### BOOTSTRAP.md
- **Purpose**: One-time ritual for first performance
- **Scope**: Exclusively for brand new workspace
- **Lifecycle**: Delete after completion (won't be restored on later restarts)
- **Creation**: Only created for completely new workspace without other bootstrap files
- **Importance**: Initial agent setup and configuration

### Memory Files

#### memory/YYYY-MM-DD.md
- **Purpose**: Daily memory logs (one file per day)
- **Recommendation**: Read today + yesterday at session start
- **Creation**: Create `memory/` directory if needed
- **Content**: Raw logs of what happened, decisions made
- **Importance**: Short-term memory and session continuity

#### MEMORY.md (Optional)
- **Purpose**: Curated long-term memory
- **Loading**: ONLY in main session (direct chats with human)
- **Security**: DO NOT load in shared contexts (Discord, group chats) - contains personal context
- **Content**: Significant events, thoughts, decisions, opinions, lessons learned
- **Importance**: Long-term knowledge retention and agent development

### Skill and Asset Directories

#### skills/ (Optional)
- **Purpose**: Workspace-specific skills
- **Override Behavior**: Overrides managed/bundled skills on name conflicts
- **Loading**: Skills loaded from three locations (workspace wins)
- **Importance**: Custom agent capabilities and workflows

#### canvas/ (Optional)  
- **Purpose**: Canvas UI files for node displays
- **Example**: `canvas/index.html`
- **Usage**: Node interface templates and layouts
- **Importance**: Visual interface for agent interactions

## Missing File Handling

### Automatic Markers
If a bootstrap file is missing, OpenClaw adds corresponding marker in session and continues:
```
[MISSING: AGENTS.md]
[MISSING: SOUL.md]
[etc.]
```

### File Restoration
- **Command**: `openclaw setup` can restore missing defaults without overwriting existing files
- **Behavior**: Creates missing files with safe default content
- **Safety**: Preserves existing file content

### Large File Truncation
- **Limit**: Large bootstrap files are truncated when injected
- **Configuration**: Limit adjustable via `agents.defaults.bootstrapMaxChars` (default: 20000)
- **Behavior**: Files truncated with truncation marker when exceeding limit
- **Visibility**: `/context list` shows both raw and injected sizes per file

## What Should NOT Be in Workspace

### Separate Repository Files
These files belong in `~/.openclaw/` workspace repository and should NOT be checked into workspace:

#### ~/.openclaw/openclaw.json (Configuration)
- **Content**: Gateway and agent configuration
- **Location**: Configuration directory, not workspace
- **Reason**: Separation of code from configuration

#### ~/.openclaw/credentials/ (OAuth Tokens, API Keys)
- **Content**: Authentication tokens and API keys
- **Location**: Credentials directory, not workspace  
- **Reason**: Security - secrets should not be in workspace

#### ~/.openclaw/agents/<agentId>/sessions/ (Session Logs + Metadata)
- **Content**: Session history and metadata
- **Location**: Agent session directory, not workspace
- **Reason**: Session data is runtime information, not workspace content

#### ~/.openclaw/skills/ (Managed Skills)
- **Content**: Skills managed by OpenClaw
- **Location**: Managed skills directory, not workspace
- **Reason**: Workspace skills override these, but managed skills are separate

### Migration Considerations
- **Session Migration**: Copy sessions separately from old machine
- **Configuration Migration**: Copy configuration separately
- **Keep Separate**: Never mix workspace content with configuration/credentials

## Git Backup (Recommended, Private)

### Treat Workspace as Private Memory
Store workspace in a private Git repository for backup and recovery. Run these commands on the machine where Gateway runs (where workspace is located).

### 1) Repository Initialization
Git is automatically initialized for new workspaces if Git is installed. If this workspace is not yet a repository:

```bash
cd ~/.openclaw/workspace
git init
git add AGENTS.md SOUL.md TOOLS.md IDENTITY.md USER.md HEARTBEAT.md memory/
git commit -m "Add agent workspace"
```

### 2) Add Private Remote (Beginner-Friendly Options)

#### Option A: GitHub Web Interface
1. Create new private repository on GitHub
2. **Important**: Do NOT initialize with README (avoids merge conflicts)
3. Copy HTTPS remote URL
4. Add remote and push:
```bash
git branch -M main
git remote add origin <https-url>
git push -u origin main
```

#### Option B: GitHub CLI (gh)
```bash
gh auth login
gh repo create openclaw-workspace --private --source . --remote origin --push
```

#### Option C: GitLab Web Interface  
1. Create new private repository on GitLab
2. **Important**: Do NOT initialize with README (avoids merge conflicts)
3. Copy HTTPS remote URL
4. Add remote and push:
```bash
git branch -M main  
git remote add origin <https-url>
git push -u origin origin
```

### 3) Ongoing Updates
```bash
git status
git add .
git commit -m "Update memory"
git push
```

### Security: Don't Expose Secrets
Even in a private repository, do NOT store secrets in workspace:
- **No API Keys**: OAuth tokens, API keys should stay in ~/.openclaw/
- **No Passwords**: User credentials should not be in workspace
- **No Private Credentials**: Private access data should not be in workspace
- **No Raw Chat History**: Unprocessed chat histories should not be in workspace
- **No Sensitive Attachments**: Private or sensitive files should not be in workspace

If you must store sensitive references, use placeholders and keep actual secrets elsewhere (password manager, environment variables, or ~/.openclaw/).

### Suggested .gitignore Entry
```
.DS_Store
.env
**/*.key
**/*.pem
**/secrets*
```

## Moving Workspace to New Machine

### Migration Process
1. **Clone Repository** to desired path (default `~/.openclaw/workspace`)
2. **Set Workspace Path** in `~/.openclaw/openclaw.json`:
   ```json
   {
     "agent": {
       "workspace": "~/.openclaw/workspace"
     }
   }
   ```
3. **Run Setup Command**: `openclaw setup --workspace <path>` to supplement missing files
4. **Copy Sessions**: Copy `~/.openclaw/agents/<agentId>/sessions/` separately from old machine

### Important Notes
- **Configuration Transfer**: Configuration and credentials must be copied separately
- **Session Transfer**: Sessions are not part of workspace and must be copied separately  
- **Skill Transfer**: Managed skills are in separate location and may need reconfiguration
- **Testing**: Verify all functionality after migration

## Advanced Notes

### Multiagent Routing
- **Different Workspaces**: Multiagent routing can use different workspaces for each agent
- **Configuration**: See routing configuration for details
- **Isolation**: Each agent can have its own workspace and configuration

### Sandbox Workspace Behavior
- **When Enabled**: If `agents.defaults.sandbox` is enabled, non-main sessions can use session-specific sandbox workspaces under `agents.defaults.sandbox.workspaceRoot`
- **Isolation**: Provides workspace isolation for different sessions or agents
- **Configuration**: Configure sandbox root and access permissions in agent configuration

## Troubleshooting

### Common Issues

#### Multiple Active Workspaces
- **Symptom**: Confusing behavior, inconsistent state
- **Solution**: Archive extra workspaces, ensure only one active
- **Check**: `openclaw doctor` to detect multiple workspaces

#### Missing Bootstrap Files
- **Symptom**: [MISSING] markers in session context
- **Solution**: Run `openclaw setup` to create missing files
- **Check**: Verify workspace directory exists and is writable

#### Large Context Usage
- **Symptom**: Model context window full
- **Solution**: Use `/compact`, reduce file sizes, increase model context limit
- **Check**: `/context detail` to see largest files

#### Permission Issues
- **Symptom**: Cannot read/write workspace files
- **Solution**: Check file permissions, workspace ownership
- **Check**: `ls -la ~/.openclaw/workspace` to verify permissions

### Debug Commands
```bash
# Check workspace status
openclaw workspace status

# Verify workspace files
openclaw workspace verify

# Fix workspace issues  
openclaw workspace repair

# Show workspace path
openclaw config get agents.defaults.workspace

# Set workspace path
openclaw config set agents.defaults.workspace "/path/to/workspace"
```