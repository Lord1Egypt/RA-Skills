# Code Archaeology Skill

## Overview
This skill provides tools and workflows for analyzing legacy codebases and extracting actionable insights for modernization planning.

## Directory Structure
```
code-archaeology/
├── SKILL.md                    # Skill specification and documentation
├── license.txt                 # License file
├── README.md                   # This file
└── scripts/
    ├── code-archaeology-integrator.cjs    # Core integration logic
    ├── process-file-manager.cjs          # File location management
    └── convert-to-ai-plan-generator.cjs  # Conversion utility
```

## Usage

### Convert Code Archaeology Results to AI Plan Generator Format
```bash
cd /Users/admin/.npm-global/lib/node_modules/openclaw/skills/code-archaeology/scripts
node convert-to-ai-plan-generator.cjs \
  /path/to/project_code_archaeology \
  /output/context-documents \
  finance
```

### Integration with AI Plan Generator
The converted context documents can be used directly with AI Plan Generator:
```bash
# Analyze completeness of generated context documents
ai-plan-generator analyze-completeness /output/context-documents

# Create ClawTeam migration team
clawteam create --name "finance-migration" --description-file campaign.md
```

## Unified Directory Structure
Code Archaeology results should be organized in the standard unified structure:
```
project_code_archaeology/
├── results/        # Primary analysis outputs
├── process/        # Detailed analysis artifacts  
├── source/         # Original source code
└── project_archaeology_status.json  # Status tracking
```

## Requirements
- Node.js v14+
- Code Archaeology analysis results in unified directory format
- AI Plan Generator v2 for full integration

## License
See `license.txt` for licensing information.