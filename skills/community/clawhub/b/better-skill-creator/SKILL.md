---
name: better-skill-creator
description: Enhanced skill creation and management tool with built-in end-to-end version control capabilities. Supports skill creation, editing, packaging, automatic version backup, intelligent diff comparison, risk assessment, requirement plan confirmation, interactive rollback, semantic version management. Applicable to: (1) Create new skills; (2) Optimize/modify existing skills; (3) Skill version management and rollback; (4) Standardize skill modification processes to ensure version stability.
---

# Better Skill Creator - Enhanced Skill Creation and Management Tool

## Core Features
### 🎯 100% Compatible with native skill-creator
All native functions are fully retained with zero switching of usage habits:
- Skill initialization template generation (`init_skill.py`)
- Skill directory structure specification verification
- Skill packaging and export (`package_skill.py`)
- Skill design best practice guidance
- Full compatibility with all original parameters and commands

### 🛡️ Built-in end-to-end version control (New capabilities)
No additional version management tools required, ready to use out of the box:
1. **Automatic Backup**: Automatically triggers version backup before creating/modifying skills, no manual operation required
2. **Intelligent Diff Comparison**: Compare content differences of any versions, automatically identify change types and assess risk levels (High/Medium/Low)
3. **Interactive Rollback**: Automatically list version records, roll back by selection, support difference preview
4. **Requirement Plan Control**: Built-in optimization plan generation + approval process, enforce "confirm the plan before modification"
5. **Semantic Version Number**: Automatically manage version numbers, with complete and traceable version records
6. **Automatic CHANGELOG Generation**: Automatically generate version change records for each modification

### ✨ New Enhanced Capabilities
- 📊 Automatic assessment of the impact scope of skill modifications
- 🧪 Built-in automatic test case execution, automatic function verification after modification
- 🔒 Stable version marking function, marked versions are permanently retained and will not be automatically cleaned up
- 📝 Automatic generation of version change reports, clearly recording every modification

## Installation Instructions
### Automatic Conflict Detection
Automatically detect the following old versions during installation, support intelligent migration:
- Native skill-creator built into the system
- Installed old versions of skill-creator
- Installed skill-version-control
- Automatically migrate all historical backups, version records, and optimization plan data

### Installation Command
python scripts/install.py

## Core Usage Process
### 1. Create a New Skill
python scripts/init_skill.py <skill-name> --path <output-directory>

> Automatically create version records, initial version number v1.0.0

### 2. Optimize Existing Skills
graph TD
A[User submits optimization requirements] --> B[Generate optimization plan]
B --> C[User confirms the plan]
C --> D[Automatically back up the current version]
D --> E[Modify skills according to the plan]
E --> F[Automatic diff comparison + risk assessment]
F --> G[Automatically run test cases]
G --> H[Generate new version records + CHANGELOG]

### 3. View Version List
python scripts/list.py <skill-name>

### 4. Roll Back to Historical Versions
# Interactive rollback (Recommended)
python scripts/interactive-rollback.py <skill-name>

# Direct rollback
python scripts/rollback.py <skill-name> <version-ID>

### 5. Compare Version Differences
python scripts/diff.py <skill-name> <version-ID1> [version-ID2]

### 6. Generate Optimization Plan
# Generate plan
python scripts/proposal.py generate <skill-name> "Requirement description" --version v1.1.0

# View all plans
python scripts/proposal.py list

### 7. Package Skills
python scripts/package_skill.py <skill-path>

## Script Descriptions
### Native Function Scripts
- `init_skill.py`: Initialize new skill templates
- `package_skill.py`: Package skills into .skill files
### Version Management Scripts
- `backup.py`: Version backup
- `list.py`: Version list query
- `diff.py`: Intelligent diff comparison + risk assessment
- `rollback.py`: Version rollback
- `interactive-rollback.py`: Interactive version rollback
- `proposal.py`: Optimization plan generation and management
- `install.py`: Installation script + conflict detection
- `migrate.py`: Historical data migration script
## Configuration Instructions
Refer to `references/config.md`, support custom backup directories, number of retained versions, etc.
