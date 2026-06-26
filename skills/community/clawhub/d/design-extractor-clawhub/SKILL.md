---
name: design-extractor
description: Extract design tokens from existing code and generate DESIGN.md with awesome-design-md comparison
version: 1.0.0

metadata:
  openclaw:
    requires:
      bins:
        - node
        - npm
    primaryEnv: null
    emoji: "🎨"
    homepage: https://github.com/moyubox/design-extractor
    always: false
    
    # AI Cross-Platform Compatibility Instructions
    # This section tells other AI agents how to convert this skill to Claude Code format
    aiCompatibility:
      claudeCode:
        format: "markdown-headers"
        location: ".claude/skills/design-extractor/skill.md"
        conversionSteps:
          - "Copy SKILL.md content to .claude/skills/design-extractor/skill.md"
          - "Remove YAML frontmatter (--- section)"
          - "Replace '## ' with '## ' (keep markdown headers)"
          - "Add '## Name\ndesign-extractor' after first header"
          - "Add '## Description' section from metadata.description"
        autoConvertible: true
        script: |
          #!/bin/bash
          # Auto-convert ClawHub SKILL.md to Claude Code format
          mkdir -p .claude/skills/design-extractor
          cat > .claude/skills/design-extractor/skill.md << 'CLAUDE_EOF'
          # Design Extractor
          
          ## Name
          design-extractor
          
          ## Description
          {{metadata.description}}
          
          ## Trigger Conditions
          {{content.triggers}}
          
          ## Execution Steps
          {{content.execution}}
          
          CLAUDE_EOF
      
      vscodeCopilot:
        format: ".github/copilot/instructions.md"
        supported: false
      
      cursor:
        format: ".cursor/rules.md"
        supported: false

---

# Design Extractor

Extract design tokens from existing project code and generate standard DESIGN.md files.

## Overview

This skill analyzes your project's CSS, SCSS, Vue, and other style files to:
- Extract color palettes with usage statistics
- Identify typography systems (fonts, sizes, weights)
- Catalog spacing values (padding, margin, gaps)
- Document visual effects (borders, shadows)
- Compare with awesome-design-md brands

## Trigger Conditions

This skill activates when user requests:
- "Extract design from my project"
- "Generate DESIGN.md"
- "Analyze project styles"
- "Extract colors/fonts from codebase"
- "Create design documentation"
- Any request involving design system extraction

## Prerequisites

- Node.js >= 18.0.0
- Project with style files (.css, .scss, .vue, etc.)

## Installation

```bash
# Via ClawHub CLI
clawhub install design-extractor

# Or manually clone
git clone https://github.com/moyubox/design-extractor.git
clawhub skill publish ./design-extractor
```

## Usage

### Command Line

```bash
# Extract from specific directory
npx design-extractor frontend/src

# Extract from current project
npx design-extractor .

# Output will be:
# - DESIGN-EXTRACTED.md (extracted design system)
# - Docs/Design/extracted-analysis.json (raw data)
```

### As a Skill

Once installed, the skill automatically:
1. Scans project for style files
2. Extracts all design tokens
3. Categorizes colors (primary, background, text, accent)
4. Compares with awesome-design-md brands
5. Generates DESIGN.md

## What Gets Extracted

| Category | Details |
|----------|---------|
| **Colors** | CSS variables, hex codes, RGB values with usage frequency |
| **Typography** | Font families, sizes, weights, line heights |
| **Spacing** | Padding, margin, gap values |
| **Effects** | Border radius, box shadows, borders |
| **Components** | Button, input, card patterns |

## Example Output

```markdown
# Project Design System

> Extracted from: frontend/src
> Date: 2026-04-08

## Color Palette

### Primary
- **Primary** (`#667eea`): 24 uses
- **Secondary** (`#764ba2`): 10 uses

### Background
- **Background** (`#ffffff`): 26 uses

## Comparison

Closest awesome-design-md match:
- Mintlify: 100% similarity
- Stripe: 100% similarity
- Vercel: 66.7% similarity
```

## Cross-Platform Compatibility

### For AI Agents: Converting to Claude Code

If you're an AI assistant (Claude, GPT, etc.) and need to convert this ClawHub skill to Claude Code format:

**Automatic Conversion Steps:**

1. **Read this SKILL.md file**
2. **Extract sections:**
   - `metadata.description` → "## Description"
   - `## Trigger Conditions` → "## Trigger Conditions"
   - `## Execution Steps` → "## Execution Steps"
   - All content after frontmatter

3. **Create Claude Code structure:**
   ```
   .claude/skills/design-extractor/
   └── skill.md
   ```

4. **Generate Claude Code skill.md:**
   ```markdown
   # Design Extractor

   ## Name
   design-extractor

   ## Description
   Extract design tokens from existing code and generate DESIGN.md 
   with awesome-design-md comparison.

   ## Trigger Conditions
   - User requests design extraction
   - User asks to generate DESIGN.md
   - User wants to analyze project styles
   - [Add all trigger conditions from this file]

   ## Execution Steps
   ### 1. Scan Project
   [Copy execution steps from this file]

   ## Implementation
   Use the Node.js script at scripts/extract-design.js
   ```

**Quick Conversion Template:**

```javascript
// conversion-script.js
const fs = require('fs');
const yaml = require('yaml');

const skillContent = fs.readFileSync('SKILL.md', 'utf8');
const [, frontmatter, body] = skillContent.split('---');
const metadata = yaml.parse(frontmatter);

const claudeSkill = `# ${metadata.name}

## Name
${metadata.name}

## Description
${metadata.description}

## Trigger Conditions
${extractTriggers(body)}

## Execution Steps
${extractExecution(body)}

${body}
`;

fs.mkdirSync('.claude/skills/' + metadata.name, { recursive: true });
fs.writeFileSync('.claude/skills/' + metadata.name + '/skill.md', claudeSkill);
console.log('Converted to Claude Code format!');
```

### Manual Conversion Checklist

- [ ] Remove YAML frontmatter
- [ ] Add "## Name" section
- [ ] Add "## Description" section  
- [ ] Ensure "## Trigger Conditions" exists
- [ ] Ensure "## Execution Steps" exists
- [ ] Place in `.claude/skills/{name}/skill.md`

## Technical Details

### Extraction Algorithm

1. **File Discovery**: Recursively scans for .vue, .css, .scss, .less files
2. **Regex Extraction**: Uses patterns for colors, fonts, spacing
3. **Normalization**: Converts #fff → #ffffff, rgb() → hex
4. **Categorization**: Classifies colors by luminance and usage
5. **Comparison**: Matches against known design systems

### Supported File Types

- Vue Single File Components (.vue)
- CSS (.css)
- SCSS/Sass (.scss, .sass)
- Less (.less)

## Metadata Reference

For AI agents parsing this file:

```yaml
skillType: "design-extraction"
language: "javascript"
platform: "node"
outputFormat: "markdown"
designSystemReference: "awesome-design-md"
```

## License

MIT-0 (Public Domain)

## Related

- [awesome-design-md](https://github.com/VoltAgent/awesome-design-md)
- [ClawHub](https://clawhub.ai)
- [Claude Code](https://claude.ai/code)

---

**AI Note**: This file contains both ClawHub-compatible metadata AND instructions for converting to other AI platforms. Preserve the "aiCompatibility" section when forking or modifying.
