---
name: auto-design
description: Auto-select and apply design systems from awesome-design-md based on project type and task context
version: 1.0.0

metadata:
  openclaw:
    requires:
      bins:
        - node
        - curl
    primaryEnv: null
    emoji: "🎯"
    homepage: https://github.com/moyubox/auto-design
    always: true  # This skill is always active
    
    # AI Cross-Platform Compatibility
    aiCompatibility:
      claudeCode:
        format: "markdown-headers"
        location: ".claude/skills/auto-design/skill.md"
        conversionSteps:
          - "Read YAML frontmatter for metadata"
          - "Copy all content after frontmatter to new file"
          - "Insert '## Name\nauto-design' after title"
          - "Insert '## Description' from metadata.description"
          - "Convert '## Trigger Conditions' to Claude format"
          - "Save to .claude/skills/auto-design/skill.md"
        autoConvertible: true
        oneLineConvert: |
          mkdir -p .claude/skills/auto-design && 
          echo "# Auto Design\n\n## Name\nauto-design\n\n## Description\nAuto-select and apply design systems from awesome-design-md based on project type and task context\n" > .claude/skills/auto-design/skill.md && 
          tail -n +35 SKILL.md >> .claude/skills/auto-design/skill.md

---

# Auto Design

Intelligent design system selector that automatically picks the best style from awesome-design-md for your project.

## Philosophy

Stop asking "what design should I use?" — let the AI figure it out based on:
- Project type (tool, dashboard, marketing, docs)
- Target audience (developers, designers, consumers)
- Technology stack (Vue, React, vanilla)
- Task context (creating, optimizing, refactoring)

## Trigger Conditions

This skill activates automatically when:

### Explicit Requests
- "Create a new page/component"
- "Design a [something]"
- "Make it look like [brand]"
- "What style should I use?"

### Implicit Context
- User creates Vue/React component files
- User mentions "design", "style", "UI", "UX"
- User requests optimization of existing UI
- Any task involving CSS/styling decisions

### Keywords That Trigger
```
design, style, theme, UI, UX, layout, component
page, screen, interface, visual, look, appearance
optimize, improve, refactor, enhance, polish
```

## Smart Selection Logic

### Decision Matrix

```yaml
Project Type Mapping:
  developer-tool:
    primary: vercel
    alternatives: [linear, cursor, raycast]
    reason: "Clean, professional, code-centric"
    
  ai-ml-product:
    primary: claude
    alternatives: [cohere, voltagent]
    reason: "Warm, human-centered, modern"
    
  documentation:
    primary: mintlify
    alternatives: [notion]
    reason: "Reading-optimized, clear hierarchy"
    
  marketing-site:
    primary: stripe
    alternatives: [apple, framer]
    reason: "Elegant gradients, premium feel"
    
  data-dashboard:
    primary: linear
    alternatives: [supabase, sentry]
    reason: "Data-dense, precise, dark-friendly"
```

### Context Detection

The skill analyzes:
1. **File paths**: `frontend/src/views/` → Vue project
2. **Package.json**: React? Vue? Dependencies?
3. **CLAUDE.md**: Project description and goals
4. **User's words**: "tool", "dashboard", "landing page"
5. **Existing code**: Current color schemes, component patterns

## Usage Examples

### Example 1: Tool Page
```
User: "Create a password generator"
AI: Detects "tool" → Selects Vercel
Result: Clean black/white UI with blue accents
```

### Example 2: Documentation
```
User: "Build an API docs page"
AI: Detects "docs" → Selects Mintlify
Result: Green-accented, reading-optimized layout
```

### Example 3: Override
```
User: "Make it like Linear"
AI: User specified → Uses Linear regardless
Result: Purple-accented, minimal data-dense UI
```

## Execution Flow

### Step 1: Analyze Context (Automatic)
```javascript
context = {
  projectType: analyzeProject(),     // "toolbox", "saas", "docs"
  techStack: detectFramework(),      // "Vue 3", "React", "vanilla"
  userIntent: parseUserRequest(),    // "create", "optimize", "refactor"
  existingDesign: scanCurrentStyles() // Current colors, fonts
}
```

### Step 2: Select Design System
```javascript
selection = {
  brand: selectBrand(context),       // "vercel", "linear", etc.
  confidence: calculateConfidence(), // 0.0 - 1.0
  reason: generateReason(),          // Why this choice
  alternatives: getAlternatives()    // Backup options
}
```

### Step 3: Download & Apply
```bash
# Auto-download from awesome-design-md
curl https://raw.githubusercontent.com/VoltAgent/awesome-design-md/main/design-md/{brand}/DESIGN.md

# Save to project
mkdir -p Docs/Design
cp downloaded.md Docs/Design/{brand}-DESIGN.md
```

### Step 4: Generate Local Reference
creates `DESIGN.md` with:
- Selected brand info
- Core design tokens (colors, fonts, spacing)
- Usage instructions
- Generated timestamp

### Step 5: Apply to Implementation
When creating UI:
- Uses selected brand's color palette
- Follows typography hierarchy
- Applies spacing system
- Uses component patterns

## Brand Library

### Available Brands (58 total)

**Developer Tools:**
- Vercel (default) - Black/white, Geist font, precise
- Linear - Purple, minimal, data-dense
- Cursor - Dark IDE, gradient accents
- Raycast - Dark chrome, vibrant colors
- Supabase - Emerald, code-first

**AI/ML:**
- Claude - Warm terracotta, editorial
- Cohere - Vibrant gradients, dashboard
- Mistral - Purple, French minimalism

**Documentation:**
- Mintlify - Green, reading-optimized
- Notion - Warm, serif headings

**Marketing:**
- Stripe - Purple gradients, weight-300
- Apple - Premium whitespace, SF Pro
- Framer - Bold black/blue, motion

## Configuration

### Environment Variables
```bash
# Override default brand
AUTO_DESIGN_DEFAULT=linear

# Disable auto-selection
AUTO_DESIGN_AUTO=false

# Specify user preference
AUTO_DESIGN_PREFERENCE=claude
```

### Per-Project Config
Add to `CLAUDE.md` or `.clauderc`:
```yaml
design:
  default: vercel
  allowed: [vercel, linear, mintlify]
  disabled: [stripe]  # Exclude if not relevant
```

## Cross-Platform Conversion

### For Claude Code Users

If you have this ClawHub skill and need to use it with Claude Code:

**Option 1: Automatic Conversion (Recommended)**
```bash
# Run this command in the skill directory
mkdir -p .claude/skills/auto-design && \
echo "# Auto Design\n\n## Name\nauto-design\n\n## Description\nAuto-select and apply design systems from awesome-design-md" \
  > .claude/skills/auto-design/skill.md && \
tail -n +35 SKILL.md >> .claude/skills/auto-design/skill.md
```

**Option 2: AI-Assisted Conversion**
Tell Claude:
```
"Convert this ClawHub skill to Claude Code format. 
 The file is at .claude/skills/auto-design-clawhub/SKILL.md"
```

**Option 3: Manual Steps**
1. Copy `SKILL.md` content (skip YAML frontmatter)
2. Create `.claude/skills/auto-design/skill.md`
3. Add:
   ```markdown
   ## Name
   auto-design
   
   ## Description
   [from metadata]
   ```
4. Keep all trigger conditions and execution steps

### Conversion Checklist for AI Agents

- [ ] Extract `metadata.description` as "## Description"
- [ ] Extract `name` as "## Name"
- [ ] Preserve all markdown content after frontmatter
- [ ] Ensure trigger conditions are clear
- [ ] Maintain execution steps order
- [ ] Test conversion output works in Claude Code

## Technical Implementation

### Auto-Selection Algorithm

```javascript
function selectBrand(context) {
  // User override takes priority
  if (context.userPreference) {
    return brands[context.userPreference];
  }
  
  // Match by keywords in request
  for (const [keyword, brand] of keywordMappings) {
    if (context.request.includes(keyword)) {
      return brand;
    }
  }
  
  // Match by project type
  const typeMap = {
    'tool': 'vercel',
    'dashboard': 'linear',
    'docs': 'mintlify',
    'landing': 'stripe'
  };
  
  return typeMap[context.projectType] || 'vercel';
}
```

### Confidence Scoring

```javascript
confidence = {
  keywordMatch: 0.9,      // User said "like Linear"
  projectTypeMatch: 0.8,  // Tool project → Vercel
  default: 0.7            // Fallback
}
```

## Integration with Design Extractor

These two skills work together:

```
Design Extractor (analyze existing)
    ↓
Extracts current design tokens
    ↓
Auto Design (suggests improvements)
    ↓
Recommends closest awesome-design-md match
    ↓
Applies selected design system
```

## Output Files

| File | Purpose |
|------|---------|
| `DESIGN.md` | Quick reference for current project |
| `Docs/Design/{brand}-DESIGN.md` | Full design system spec |
| `Docs/DevLog/YYYY-MM-DD_design.md` | Decision log |

## AI Compatibility Notes

**For AI agents reading this file:**

This skill is designed to be **auto-convertible** between platforms:

1. **ClawHub** (native): Uses YAML frontmatter
2. **Claude Code**: Uses markdown headers
3. **Future platforms**: Parse this file's structure

**Key sections to extract:**
- `metadata.description` → Always use as description
- `## Trigger Conditions` → Activation rules
- `## Execution Steps` → Implementation guide
- Brand mappings → Core logic

**Never remove** the `aiCompatibility` section when porting.

## License

MIT-0 (Public Domain)

## See Also

- [awesome-design-md](https://github.com/VoltAgent/awesome-design-md) - Design system collection
- [Design Extractor](./design-extractor) - Complementary skill
- [ClawHub](https://clawhub.ai) - Skill registry
- [Claude Code](https://claude.ai/code) - AI coding assistant

---

**AI Conversion Note**: This SKILL.md is self-documenting for cross-platform use. 
To convert to Claude Code, an AI should:
1. Parse YAML frontmatter for metadata
2. Create new file with "## Name" and "## Description" headers
3. Copy all content after frontmatter
4. Save to .claude/skills/auto-design/skill.md
