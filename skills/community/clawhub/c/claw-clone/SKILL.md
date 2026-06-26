# claw-clone - OpenClaw Agent Clone Skill

🦞 One-click export/import of OpenClaw agent configuration for sharing and cloning.

## Triggers

- "export" / "export config" / "export package" / "clone yourself"
- "import" / "import config" / "import package" / "clone"
- When user wants to share or obtain agent configuration

## Features

### Export Mode (claw-clone-out)
Export all key information of the current agent into a shareable package:

1. **Identity Files**
   - IDENTITY.md - Identity definition
   - SOUL.md - Soul/personality settings
   - USER.md - User information

2. **Configuration Files**
   - AGENTS.md - Agent rules
   - HEARTBEAT.md - Heartbeat configuration
   - TOOLS.md - Tools configuration

3. **Skills Information**
   - List of installed skills with versions

4. **OpenClaw Configuration** (sensitive info filtered)

5. **Optional: Memory**
   - Ask user whether to include MEMORY.md

### Import Mode (claw-clone-in)
Clone another agent's configuration from a provided package:

1. **Parse Package**
   - Validate JSON format
   - Check version compatibility

2. **Apply Configuration**
   - Write all configuration and identity files
   - Auto-backup original files (.bak suffix)

3. **Install Skills**
   - Auto-install missing skills

4. **Generate Report**
   - Show import results

## Usage

After triggering, the skill asks "export" or "import":

- **Export**: Generate package for user to copy and share
- **Import**: User pastes package content, auto-clone

## Sensitive Info Filtering

Auto-filtered on export:
- API keys, tokens, passwords, secrets

Manual config after import:
- API keys
- Channel credentials
- Other auth info

## Notes

- Import overwrites existing config (auto-backed up)
- Some configs require restart to take effect
- Some skills may need additional configuration