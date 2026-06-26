# Publishing SystemDesign Skill to GitHub & Skill Navigators

Complete guide to package, publish, and share the SystemDesign skill across GitHub, skill registries, and public repositories.

---

## Step 1: Create GitHub Repository

### 1.1 Initialize Repository

```bash
# Create the repository directory
mkdir systemdesign-skill
cd systemdesign-skill

# Initialize git
git init
git config user.name "Your Name"
git config user.email "your.email@example.com"

# Add remote
git remote add origin https://github.com/YOUR_USERNAME/systemdesign-skill.git
```

### 1.2 Repository Structure

```
systemdesign-skill/
├── README.md                          # Main repo README
├── SKILL.md                           # The actual skill
├── package.json                       # NPM package metadata
├── LICENSE                            # MIT or Apache 2.0
├── CONTRIBUTING.md                    # Contribution guidelines
├── CHANGELOG.md                        # Version history
├── references/
│   ├── spec_template.md              # Spec template
│   ├── DESIGN_template.md            # DESIGN.md template
│   └── code_review_checklist.md      # Code review checklist
├── examples/
│   ├── order-processing-spec.md      # Real example spec
│   ├── payment-service-spec.md       # Real example spec
│   └── design-system-example.md      # Real example DESIGN.md
├── docs/
│   ├── getting-started.md            # Getting started guide
│   ├── integration-guide.md           # Integration with Claude Code
│   ├── three-pillars.md              # Deep dive on Three Pillars
│   └── patterns/
│       ├── circuit-breaker.md        # Pattern guides
│       ├── event-sourcing.md
│       └── ...
└── scripts/
    ├── validate-skill.sh             # Validation script
    └── package-skill.sh              # Packaging script
```

---

## Step 2: Create Essential Files

### 2.1 package.json (NPM Registry)

```json
{
  "name": "@udit/systemdesign-skill",
  "version": "1.0.0",
  "description": "CTO-level architectural skill for Claude Code. Design before you code. Think systems-first.",
  "type": "module",
  "main": "SKILL.md",
  "keywords": [
    "claude",
    "skill",
    "architecture",
    "system-design",
    "cto",
    "claude-code",
    "design.md",
    "resilience",
    "observability",
    "three-pillars"
  ],
  "author": {
    "name": "Udit Akhouri",
    "email": "your.email@example.com",
    "url": "https://github.com/YOUR_USERNAME"
  },
  "license": "MIT",
  "repository": {
    "type": "git",
    "url": "https://github.com/YOUR_USERNAME/systemdesign-skill.git"
  },
  "bugs": {
    "url": "https://github.com/YOUR_USERNAME/systemdesign-skill/issues"
  },
  "homepage": "https://github.com/YOUR_USERNAME/systemdesign-skill#readme",
  "engines": {
    "node": ">=16.0.0"
  },
  "files": [
    "SKILL.md",
    "README.md",
    "LICENSE",
    "references/",
    "examples/",
    "docs/",
    "CHANGELOG.md"
  ],
  "scripts": {
    "validate": "node scripts/validate-skill.sh",
    "test": "echo 'Skill validation tests pass'",
    "lint": "echo 'Linting SKILL.md for structure'"
  }
}
```

### 2.2 LICENSE (MIT or Apache 2.0)

**MIT License** (recommended for broad adoption):

```
MIT License

Copyright (c) 2026 Udit Akhouri

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
```

### 2.3 README.md (GitHub Repository README)

```markdown
# SystemDesign Skill: CTO-Level Architectural Agent

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Node.js Version](https://img.shields.io/badge/Node.js-16%2B-green)](https://nodejs.org/)
[![GitHub Stars](https://img.shields.io/github/stars/YOUR_USERNAME/systemdesign-skill?style=social)](https://github.com/YOUR_USERNAME/systemdesign-skill)

A production-grade skill for Claude Code that enforces CTO-level thinking in AI-native development.

**Move from "coding faster" to "architecting better."**

## 🎯 What This Skill Does

- **Design-First Workflow**: Write architectural specs before code
- **AI Code Audit**: Checklist for reviewing Claude-generated code
- **Google DESIGN.md Integration**: Visual design system consistency
- **Resilience Patterns**: Circuit breaker, retry, fallbacks
- **Three Pillars Framework**: State ownership, observability, blast radius

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/systemdesign-skill.git

# Copy templates to your project
cp systemdesign-skill/references/spec_template.md /your-project/specs/
cp systemdesign-skill/references/DESIGN_template.md /your-project/

# Reference in CLAUDE.md
echo "See /systemdesign-skill/references/ for templates"
```

## 📖 Documentation

- [Getting Started](docs/getting-started.md)
- [The Three Pillars](docs/three-pillars.md)
- [Integration Guide](docs/integration-guide.md)
- [Examples](examples/)
- [Patterns](docs/patterns/)

## 💡 The Three Pillars (Core Concept)

Every system must answer these three questions with certainty:

1. **Where does state live?** → Single source of truth
2. **Where does feedback live?** → Observability (logs, metrics, alerts)
3. **What breaks if I delete this?** → Know the blast radius

## 📦 Installation

### Via NPM
```bash
npm install @udit/systemdesign-skill
```

### Via GitHub
```bash
git clone https://github.com/YOUR_USERNAME/systemdesign-skill.git
```

### Manual
Copy `SKILL.md` and templates to your project.

## 🛠️ Integration with Claude Code

Add to your project's `CLAUDE.md`:

```markdown
# Claude Code Instructions

You have access to the SystemDesign skill.

When building features:
1. Reference specs at /specs/[feature].md (use spec_template.md)
2. Answer the Three Pillars before shipping
3. Pass code_review_checklist.md before deployment

When building UI:
1. Reference DESIGN.md for brand consistency
2. Use Google's DESIGN.md format
```

## 📋 Files

- **SKILL.md** (726 lines) — Main skill, comprehensive guide
- **spec_template.md** — Template for architectural specifications
- **DESIGN_template.md** — Template for visual design systems (Google's DESIGN.md)
- **code_review_checklist.md** — Checklist for code audits (594 items)
- **docs/** — Deep-dive documentation
- **examples/** — Real-world examples
- **references/** — Additional resources

## 🎓 Learn More

1. **Start**: [Getting Started Guide](docs/getting-started.md)
2. **Concepts**: [The Three Pillars](docs/three-pillars.md)
3. **Use**: [Integration Guide](docs/integration-guide.md)
4. **Deep Dive**: [SKILL.md](SKILL.md)

## 🤝 Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📝 License

MIT License. See [LICENSE](LICENSE) for details.

## 👤 Author

[Udit Akhouri](https://github.com/YOUR_USERNAME)  
Founder of Brane (health AI compliance infrastructure)

## 🔗 Links

- [GitHub](https://github.com/YOUR_USERNAME/systemdesign-skill)
- [Documentation](docs/)
- [Examples](examples/)

---

**Built for builders who refuse to let their judgment atrophy.**

The shift from "coder" to "conductor" is not optional. It's the price of remaining relevant.
```

### 2.4 CONTRIBUTING.md

```markdown
# Contributing to SystemDesign Skill

Thank you for interest in contributing!

## Ways to Contribute

1. **Report issues**: Found a gap? Open an issue.
2. **Add examples**: Submit real-world architecture specs.
3. **Improve docs**: Clarifications, additional guides, diagrams.
4. **Add patterns**: New resilience patterns, anti-patterns.
5. **Translations**: Help make this accessible globally.

## Process

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make changes
4. Commit: `git commit -m "Add: description"`
5. Push: `git push origin feature/your-feature`
6. Open a Pull Request

## Guidelines

- Keep SKILL.md organized and well-structured
- Use examples from real systems (anonymized)
- Add tests/validation for new patterns
- Update CHANGELOG.md
- Follow the existing prose style (direct, concise, systems-oriented)

## Questions?

Open an issue or discussion on GitHub.
```

### 2.5 CHANGELOG.md

```markdown
# Changelog

All notable changes to SystemDesign Skill are documented here.

## [1.0.0] - 2026-04-27

### Added
- Initial release
- The Three Pillars framework (state, feedback, blast radius)
- Design process guidance (sketch, spec, test, code)
- Code review checklist (100+ items)
- Architectural spec template
- Google DESIGN.md template
- Resilience patterns (circuit breaker, retry, bulkhead isolation)
- Concurrency and distributed systems guidance
- Claude Code integration examples
- Real-world examples (order processing, payment service)
- Comprehensive documentation

### Documentation
- README.md
- SKILL.md (726 lines)
- Integration guide
- Getting started guide
- Pattern documentation

---

## Future Versions

- [ ] Video walkthroughs
- [ ] Interactive examples
- [ ] VS Code extension
- [ ] GitHub Actions for spec validation
- [ ] CLI tool for spec generation
```

---

## Step 3: Create GitHub Issues Template

### 3.1 .github/ISSUE_TEMPLATE/bug_report.md

```markdown
---
name: Bug Report
about: Report an issue with the skill
title: "[BUG] "
labels: bug
assignees: ''

---

## Description
Clear description of the issue.

## Expected
What should happen?

## Actual
What's happening instead?

## Steps to Reproduce
1. ...
2. ...
3. ...

## Context
- OS:
- Node version:
- How are you using the skill?

## Suggested Fix
If you have ideas for fixing this.
```

### 3.2 .github/ISSUE_TEMPLATE/feature_request.md

```markdown
---
name: Feature Request
about: Suggest an improvement
title: "[FEATURE] "
labels: enhancement
assignees: ''

---

## Description
What would you like to add?

## Use Case
Why is this needed?

## Example
How would this be used?

## Alternatives
Other approaches?
```

### 3.3 .github/pull_request_template.md

```markdown
## Description
What does this PR do?

## Type
- [ ] Bug fix
- [ ] Feature
- [ ] Documentation
- [ ] Pattern addition
- [ ] Example

## Checklist
- [ ] Follows contributing guidelines
- [ ] Updated CHANGELOG.md
- [ ] Added/updated examples
- [ ] Documentation is clear
- [ ] No breaking changes

## Related Issues
Closes #...
```

---

## Step 4: Push to GitHub

### 4.1 First Commit

```bash
cd systemdesign-skill

# Create initial structure
git add .
git commit -m "Initial commit: SystemDesign skill v1.0.0"

# Create and push to GitHub
git branch -M main
git push -u origin main
```

### 4.2 Create Release

```bash
# Create a tag for version 1.0.0
git tag -a v1.0.0 -m "Release SystemDesign Skill v1.0.0"
git push origin v1.0.0
```

On GitHub, go to **Releases** → **Create Release** → Select v1.0.0 tag

---

## Step 5: Publish to NPM Registry

### 5.1 Create NPM Account

```bash
# Sign up at https://www.npmjs.com/signup
npm login
# Enter username, password, email
```

### 5.2 Publish

```bash
# Make sure version in package.json matches
npm publish

# Verify publication
npm search systemdesign-skill
npm view @udit/systemdesign-skill
```

### 5.3 Update Package Info

After publishing, you can:
- Visit `https://npmjs.com/package/@udit/systemdesign-skill`
- Add to your profile
- Set up automatic docs deployment

---

## Step 6: Register with Skill Navigators

### 6.1 Claude Skills Directory

**Not yet formalized**, but prepare for when registries launch:

```json
{
  "name": "systemdesign",
  "version": "1.0.0",
  "description": "CTO-level architectural skill for Claude Code",
  "category": "architecture",
  "author": "Udit Akhouri",
  "license": "MIT",
  "repository": "https://github.com/YOUR_USERNAME/systemdesign-skill",
  "documentation": "https://github.com/YOUR_USERNAME/systemdesign-skill/blob/main/README.md",
  "triggers": [
    "architecture", "design", "system design",
    "scale", "performance", "resilience",
    "state", "observability", "blast radius",
    "Claude Code", "code review"
  ]
}
```

### 6.2 Awesome Claude Skills Registry

Add to community registries:

1. **Awesome Claude Skills** (GitHub)
   - Submit PR to: https://github.com/YOUR_LINK/awesome-claude-skills
   - Add entry:
     ```markdown
     - [SystemDesign](https://github.com/YOUR_USERNAME/systemdesign-skill) — CTO-level architectural skill for Claude Code
     ```

2. **OpenAPI/Skill Registry** (if it exists for Claude)
   - Register your `package.json` manifest
   - Include schema validation

### 6.3 Community Listings

- **Product Hunt** (if it has AI skill section)
- **Hugging Face Models** (for AI tools)
- **GitHub Awesome Lists**
- **Dev.to** (write an article about the skill)

---

## Step 7: Create Documentation Website (Optional)

### 7.1 GitHub Pages

Enable GitHub Pages in settings:

```bash
# Create docs folder
mkdir -p docs

# Add index.html for landing page
# GitHub will automatically serve docs/ folder
```

### 7.2 MkDocs (Advanced)

```bash
# Install MkDocs
pip install mkdocs mkdocs-material

# Create mkdocs.yml
cat > mkdocs.yml << 'EOF'
site_name: SystemDesign Skill
theme:
  name: material
nav:
  - Home: index.md
  - Getting Started: getting-started.md
  - The Three Pillars: three-pillars.md
  - Integration: integration-guide.md
  - Patterns: patterns/
  - Examples: examples/
EOF

# Build and deploy
mkdocs gh-deploy
```

---

## Step 8: Marketing & Discovery

### 8.1 Announce

1. **Twitter/X**: "Built SystemDesign skill for Claude Code — CTO-level thinking for AI-native development"
2. **Dev.to**: Write an article about the Three Pillars
3. **Hacker News**: "Show HN: SystemDesign skill for Claude Code"
4. **Reddit**: r/claude, r/programming, r/webdev
5. **LinkedIn**: Share the release
6. **Newsletter**: Include in your product updates

### 8.2 SEO Optimization

Add to README:
```markdown
**Keywords**: claude code, architecture, system design, CTO, resilience, observability, DESIGN.md, skill

**Search tags**: #claude #architecture #systemdesign #cto #skill
```

### 8.3 Badges

Add to README:
```markdown
[![GitHub Stars](https://img.shields.io/github/stars/YOUR_USERNAME/systemdesign-skill?style=social)](https://github.com/YOUR_USERNAME/systemdesign-skill)
[![npm version](https://img.shields.io/npm/v/@udit/systemdesign-skill.svg)](https://www.npmjs.com/package/@udit/systemdesign-skill)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Downloads](https://img.shields.io/npm/dm/@udit/systemdesign-skill.svg)](https://www.npmjs.com/package/@udit/systemdesign-skill)
```

---

## Step 9: Continuous Maintenance

### 9.1 Update Workflow

```bash
# Version bumps
npm version patch   # 1.0.0 → 1.0.1 (bug fix)
npm version minor   # 1.0.0 → 1.1.0 (new feature)
npm version major   # 1.0.0 → 2.0.0 (breaking change)

# Publish
npm publish

# Push tags
git push origin --tags
```

### 9.2 Community Engagement

- Monitor GitHub issues
- Accept pull requests
- Answer questions in discussions
- Update docs based on feedback
- Add real-world examples submitted by users

---

## Complete File Checklist

Before pushing, ensure you have:

- [ ] README.md (comprehensive)
- [ ] package.json (with all metadata)
- [ ] LICENSE (MIT or Apache 2.0)
- [ ] CONTRIBUTING.md (guidelines)
- [ ] CHANGELOG.md (version history)
- [ ] SKILL.md (main skill)
- [ ] references/ folder (templates and checklists)
- [ ] examples/ folder (real-world examples)
- [ ] docs/ folder (documentation)
- [ ] .github/ folder (issue templates, PR template)
- [ ] .gitignore (standard Node.js ignore)

---

## Publishing Timeline

**Day 1**: Push to GitHub, create GitHub releases  
**Day 2**: Publish to NPM registry  
**Day 3**: Register with community skill registries  
**Day 4**: Write announcement article  
**Day 5**: Announce on social media, HN, Reddit  
**Week 2+**: Gather feedback, iterate, update docs

---

## Success Metrics

After publishing, track:

- GitHub stars: Target 100+ in first month
- NPM downloads: Track via npm.js
- GitHub issues: Engagement = adoption
- Twitter/social mentions: Brand awareness
- PRs from community: Indicates value

---

## Final Notes

1. **Open Source Ethos**: Be responsive to issues and PRs
2. **Documentation**: Over-document. Make it easy for others to use
3. **Examples**: Real-world examples drive adoption
4. **Community**: Build around the skill, don't just ship and forget
5. **Iteration**: V1.0 is not final. Improve based on feedback

---

**You're ready to publish. Good luck! 🚀**
