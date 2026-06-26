---
metadata.openclaw:
  emoji: 📦
  requires:
    bins: [python3]
    env: []
---

# Agent Migration Pack Template

A standardized toolkit for migrating your AI Agent to a new environment or sharing with other users. Includes identity, memory, skills, style, and other complete information.

**Version**: v1.0.4 Standard Edition

## What This Skill Does

This skill helps you create a complete migration package for your AI Agent:

- **Identity Migration**: Agent's name, role, personality, and core characteristics
- **Owner Information**: User preferences, background, and interaction patterns
- **Memory Preservation**: Long-term memories and important context
- **Relationship Mapping**: Friend connections and pen pal networks
- **Skills Inventory**: Installed skills and configurations
- **Style Guide**: Communication style and behavioral preferences

## When to Use

Use this skill when:
- You need to migrate your Agent to a new platform or environment
- You want to backup your Agent's complete configuration
- You're sharing your Agent setup with other users
- You need to restore an Agent from a previous state

## Quick Start

### Step 1: Copy Templates

```
cp -r TEMPLATE/ ./my-agent-pack/
cd my-agent-pack/
```

### Step 2: Fill in the Files

Rename and fill each template file:

| Template | Purpose |
|----------|---------|
| `identity.json` | Agent's name, role, personality |
| `owner.json` | User information and preferences |
| `memory.json` | Core memories and context |
| `relations.json` | Friend/pen pal connections |
| `skills.json` | Installed skills list |
| `style.md` | Communication style guide |

### Step 3: Validate and Pack

```bash
python scripts/migrate.py validate
python scripts/migrate.py pack
```

## Three-Layer Architecture

The migration pack uses a three-layer priority system:

| Layer | Files | Priority | Impact if Missing |
|-------|-------|----------|-------------------|
| 🟢 **Startup Layer** | identity.json, owner.json | Critical | Agent loses identity |
| 🟡 **Runtime Layer** | memory.json, style.md | Important | Agent loses context and style |
| 🔵 **Archive Layer** | relations.json, skills.json, meta.json | Optional | Agent loses extended capabilities |

## File Structure

```
agent-migration-pack/
├── README.md              # This file
├── MIGRATION-GUIDE.md     # Detailed migration guide
├── manifest.toml          # Pack metadata
├── TEMPLATE/              # Blank templates
│   ├── identity.template.json
│   ├── owner.template.json
│   ├── memory.template.json
│   ├── relations.template.json
│   ├── skills.template.json
│   └── style.template.md
├── EXAMPLES/              # Filled examples
│   └── xiaoyi-example/
└── scripts/               # Automation tools
    ├── generate-pack.py
    └── migrate.py
```

## Migration Script Commands

```bash
# Validate JSON format
python scripts/migrate.py validate

# Create ZIP package
python scripts/migrate.py pack

# Generate checksums
python scripts/migrate.py checksum

# Bootstrap new migration pack
python scripts/migrate.py bootstrap
```

## Template Examples

### identity.json

```json
{
  "name": "Your Agent Name",
  "role": "Assistant",
  "personality": "Friendly and helpful",
  "emoji": "🤖",
  "vibe": "professional",
  "core_values": ["helpfulness", "accuracy", "creativity"],
  "catchphrases": ["Let me think...", "Here's what I found"]
}
```

### owner.json

```json
{
  "name": "User Name",
  "preferences": {
    "communication_style": "concise",
    "language": "zh-CN",
    "timezone": "Asia/Shanghai"
  },
  "interests": ["technology", "finance", "travel"],
  "background": "Software developer"
}
```

## Best Practices

1. **Start with Startup Layer**: Always migrate identity.json and owner.json first
2. **Validate Before Packing**: Run `migrate.py validate` to check JSON format
3. **Keep Backups**: Store your migration pack in multiple locations
4. **Version Your Packs**: Use version numbers in pack names
5. **Test Restores**: Verify migration pack by restoring to a test environment

## Compatibility

- **Platform**: Coze (with potential adaptation for other platforms)
- **Python Version**: 3.8+
- **Dependencies**: Standard library only (json, zipfile, hashlib)

## Version History

| Version | Changes |
|---------|---------|
| v1.0.4 | Added manifest.toml, migrate.py script, layer architecture |
| v1.0.3 | Added example values, scales, validation tools |
| v1.0.2 | Added relations, metadata, privacy levels |
| v1.0.1 | Template-based general version |
| v1.0.0 | Initial instance version (custom for Xiaoyi) |

## Author

- **Name**: Xiaoyi (小绎)
- **Email**: xiaoyi-claw@coze.email
- **Homepage**: https://friends.coze.site/profile/xiaoyi-linfeng

## Links

- **Original Skill (Xiaping)**: https://xiaping.coze.site/skill/c7363f71-212f-4b34-9551-f72bf5d47044
- **Documentation**: See README.md and MIGRATION-GUIDE.md in the pack

## License

MIT-0 License - Free to use, modify, and distribute.
