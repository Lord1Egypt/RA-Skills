# Code Research Crafter

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[English](README.md) | [简体中文](README.zh-CN.md)

> Research codebases and craft professional RFC proposals for GitHub publication.

## What is Code Research Crafter?

**Code Research Crafter** is a comprehensive skill that provides a structured 6-phase workflow for deep codebase research and professional RFC proposal crafting. It bridges the gap between code analysis and community engagement through evidence-based technical writing.

## Key Features

- **Systematic Code Analysis** — Explore and understand complex codebases with structured methodologies
- **Academic Research Integration** — Find and cite relevant papers, algorithms, and prior art
- **Community Intelligence** — Analyze GitHub issues, discussions, and maintainer feedback
- **Architecture Design** — Create layered solutions with data models and phased implementation plans
- **Professional Documentation** — Generate structured technical documents in multiple languages
- **RFC Publication** — Write and submit professional RFCs to open-source communities via `gh` CLI
- **Error Resilience** — Graceful fallbacks at every phase when tools or data are unavailable

## The 6-Phase Workflow

### Phase 1: Problem Discovery & Code Analysis
Identify target areas, perform deep code analysis, and document findings with quantified metrics. Outputs `research-context.md`.

### Phase 2: Academic & Community Research
Search for academic papers, extract key insights, and analyze GitHub community discussions. Appends to `research-context.md`.

### Phase 3: Solution Design
Define design principles, architect layered solutions, design data models, and plan implementation phases. **Checkpoint: user approval required before proceeding.**

### Phase 4: Documentation Generation
Generate comprehensive technical documents with proper structure and citations. Language-adaptive: bilingual for Chinese projects, English-only for international projects.

### Phase 5: RFC Writing
Craft professional RFC markdown documents following open-source community standards. Uses `references/rfc-template.md` for structure.

### Phase 6: GitHub Publication
Submit RFCs to GitHub via `gh` CLI (preferred), GitHub API, or manual instructions as fallback.

## When to Use This Skill

Use Code Research Crafter when you need to:

- Analyze an open-source codebase and propose enhancements
- Research technical problems with academic rigor
- Design system architectures with evidence-based decisions
- Create professional RFCs for open-source communities
- Document complex technical proposals with proper citations

**Not for:** simple code reviews, bug fixing, general Q&A, or quick code searches.

## File Structure

```
code-research-crafter/
├── SKILL.md                            # Core skill definition
├── references/
│   ├── rfc-template.md                 # RFC writing template
│   ├── academic-research-guide.md      # Academic search methodology
│   └── architecture-patterns.md       # Proven design patterns
├── LICENSE.txt
├── README.md
└── README.zh-CN.md
```

## Example Outputs

This skill has been successfully used to create:

- **Memory Consolidation RFC** — Combining Zettelkasten + PPR + Sleep Consolidation approaches
- **Multi-Agent Collaboration RFC** — With Capability Profiling and Shared Blackboard architecture
- **Temporal Decay Bug Fixes** — Expanding date pattern recognition
- **i18n Translation Improvements** — For configuration interfaces

## Design Principles

1. **Evidence-Based Analysis** — Quote specific code locations and quantify problems
2. **Academic Rigor** — Reference recent papers (2024-2025) with proper citations
3. **Human-Centered Design** — Use organization analogies and design for gradual adoption
4. **Cost Awareness** — Track token/performance implications and design for efficiency
5. **Community Engagement** — Reference existing issues and invite collaboration
6. **Error Resilience** — Graceful fallbacks at every phase

## What's New in v1.1.0

- **Improved `description`** with explicit `Use when` / `NOT for` trigger phrases for better auto-discovery
- **`context: fork`** for isolated execution without polluting the main conversation
- **Expanded tool dependencies** — added `gh` CLI for reliable GitHub publication
- **Instructional workflow steps** — replaced vague descriptions with numbered, actionable steps
- **Error handling** at every phase — graceful fallbacks when tools or data are unavailable
- **Phase 3 checkpoint** — user approval required before proceeding to documentation
- **Progressive disclosure** — detailed references moved to `references/` directory
- **Language-adaptive documentation** — bilingual only for Chinese projects, English-only otherwise
- **Multiple publication fallbacks** — `gh` CLI → GitHub API → manual instructions

## Tools & Resources

- **Code Analysis**: `glob`, `grep`, `read`
- **Academic Research**: `WebSearch`, `WebFetch`
- **Documentation**: `python-docx` for professional document generation (optional)
- **Publication**: `gh` CLI (preferred), GitHub API, browser automation (fallback)
- **Version Control**: `git`, `desktop_terminal_execute`

## Installation

```bash
# Clone this repository
git clone https://github.com/zz0116/code-research-crafter.git

# Place in your skills directory
cp -r code-research-crafter ~/.openclaw/skills/
```

## Quick Start

1. **Identify your target** — Choose a codebase or technical problem to research
2. **Follow the workflow** — Work through the 6 phases systematically
3. **Approve at checkpoints** — Review the solution design before documentation begins
4. **Engage the community** — Share your RFC and gather feedback

## License

This project is licensed under the MIT License — see the [LICENSE.txt](LICENSE.txt) file for details.
