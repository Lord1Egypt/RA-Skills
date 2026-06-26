# CAD Automation Skill Pack

Control AutoCAD, SolidWorks, Fusion 360, and FreeCAD via Claude Code skills.

## Why CADStack?

**The problem:** CAD tools require precise commands. Want a 10mm hole? You need to know the exact API call, parameter order, and coordinate system.

**The solution:** Describe what you want in natural language. CADStack generates the CAD script, validates it for safety, executes it, and verifies the output.

```
Traditional CAD:                    CADStack:
─────────────────────────────────    ─────────────────────────────────
1. Open CAD software                1. /cad "bracket with 4 holes"
2. Create sketch                      → Generated script
3. Draw rectangle                      → Safety validated
4. Add dimensions                      → Executed
5. Extrude                             → Dimensions verified
6. Create hole sketch                2. ✓ Done
7. Draw circle
8. Cut extrude
9. Repeat 3 more times
10. Export STEP
```

**What makes CADStack different:**
- **Safety-first**: Every script reviewed before execution
- **Multi-backend**: Same commands work across FreeCAD, AutoCAD, SolidWorks, Fusion 360
- **Verification built-in**: `/cad-qa` confirms dimensions match your intent
- **Headless mode**: FreeCAD works without opening a GUI

## Available Skills

| Skill | Description |
|-------|-------------|
| `/cad` | **Primary skill** — Execute CAD commands: create, modify, export parts |
| `/cad-plan` | Plan complex multi-step CAD operations before execution |
| `/cad-review` | Review generated CAD scripts for safety/correctness |
| `/cad-qa` | Verify exported files, check dimensions, validate geometry |
| `/cad-config` | Set up and configure CAD backend connections |

### Which Skill to Use?

```
┌─────────────────────────────────────────────────────────────┐
│                    CADSTACK DECISION TREE                    │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  START                                                       │
│    │                                                         │
│    ▼                                                         │
│  "Is this your first time?" ──YES──► /cad-config            │
│    │                                (detect & configure)    │
│    NO                                                        │
│    │                                                         │
│    ▼                                                         │
│  "Simple operation?" ──YES──► /cad                          │
│  (single part, 1-3 steps)       (create, modify, export)    │
│    │                                                         │
│    NO                                                        │
│    │                                                         │
│    ▼                                                         │
│  "Multi-step or assembly?" ──► /cad-plan ──► /cad           │
│                                 (plan first)   (execute)    │
│                                                              │
│  AFTER /cad:                                                 │
│    • Need to verify output? ──► /cad-qa                     │
│    • Review script safety?  ──► /cad-review                 │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Quick reference:**
- **Just want to make a part?** → `/cad`
- **Building something complex?** → `/cad-plan` then `/cad`
- **Not sure it worked?** → `/cad-qa`
- **Setting up for the first time?** → `/cad-config`

## Supported Platforms

- **FreeCAD** (Recommended) - Pure Python, headless mode, no license required
- **AutoCAD** - Requires AutoCAD running, uses COM automation
- **SolidWorks** - Requires SolidWorks running, uses COM automation
- **Fusion 360** - Requires Fusion 360 running with bridge add-in

## Quick Start

```bash
# Install cadstack
git clone https://github.com/user/cadstack.git ~/.claude/skills/cadstack
cd ~/.claude/skills/cadstack && ./setup
```

Then in Claude Code:
```
/cad "Create a 100x50x20mm box with 5mm filleted edges"
```

## First Run Experience

If this is your first time using cadstack, follow this sequence:

```
Step 1: Verify setup
┌─────────────────────────────────────────┐
│ /cad-config                             │
│                                         │
│ ✓ FreeCAD: available                    │
│ ✓ Output dir: ~/.claude/.../output      │
│ ✓ Default format: STEP                  │
└─────────────────────────────────────────┘

Step 2: Hello World (builds confidence)
┌─────────────────────────────────────────┐
│ /cad "create a 10mm cube"               │
│                                         │
│ ✓ Created: output/cube.step (2.1 KB)    │
│   Dimensions: 10 × 10 × 10 mm           │
└─────────────────────────────────────────┘

Step 3: Your first real part
┌─────────────────────────────────────────┐
│ /cad "create a 50×30×5mm plate with     │
│       four 5mm holes at corners"        │
└─────────────────────────────────────────┘
```

### User Journey Storyboard

| Step | User Action | User Feels | Skill Supports It |
|------|-------------|------------|-------------------|
| 1 | Install cadstack | Uncertain: "Will this work?" | `/cad-config` verifies setup |
| 2 | Create first cube | Relieved: "It works!" | Simple 10mm cube example |
| 3 | Create real part | Curious: "What else can I do?" | Examples in `/cad` skill |
| 4 | Complex operation | Confident but cautious | `/cad-plan` for structure |
| 5 | Verify output | Certain: "It's correct" | `/cad-qa` confirms dimensions |
| 6 | Error occurs | Frustrated | Minimal error → recovery command |
| 7 | Fix and retry | Satisfied | Clear path forward |

## Architecture

```
cadstack/
├── SKILL.md                 # This file
├── setup                    # Installation script
├── skills/                  # Skill definitions
│   ├── cad.md
│   ├── cad-plan.md
│   ├── cad-review.md
│   ├── cad-qa.md
│   └── cad-config.md
├── lib/                     # Core library
│   ├── cad_executor.py      # Script executor
│   ├── backends/            # Platform backends
│   └── utils/               # Helpers
└── templates/               # Script templates
```

## Configuration

Add to your project's `CLAUDE.md`:

```markdown
## cadstack
Available skills: /cad, /cad-plan, /cad-review, /cad-qa, /cad-config
Supported platforms: FreeCAD, AutoCAD, SolidWorks, Fusion 360
Default platform: freecad
```
