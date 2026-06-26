---
name: create-skill
description: Guide for creating and importing skills. Use when users need to create or import skills.
---


# Complete Workflow

## When Creating Skills
1. Follow the skill creation guide to accurately understand the skill and generate a skill folder that meets user requirements
2. Complete skill registration according to the Easyclaw Skill Registration Guide
3. Inform the user of completion status

## When Importing Skills
1. Read and review the skill package according to the Skill Import Guide
2. Complete skill registration according to the Easyclaw Skill Registration Guide
3. Inform the user of completion status


# Skill Creation Guide

A guide for creating effective skills that extend Agent capabilities through specialized knowledge, workflows, and tool integration.

## About Skills

Skills are modular, self-contained packages that extend Agent capabilities by providing specialized knowledge, workflows, and tools. Think of them as "onboarding guides" for specific domains or tasks.

### What Skills Provide

1. Specialized Workflows - Multi-step processes for specific domains
2. Tool Integration - Instructions for using specific file formats or APIs
3. Domain Expertise - Company-specific knowledge, patterns, business logic
4. Bundled Resources - Scripts, references, and assets for complex and repetitive tasks

## Understanding Skills Through Concrete Examples

To create effective skills, you should clearly understand how the skill will be used. This can come from direct examples provided by users or by generating examples and validating them with users.

For example, when building an image editing skill, relevant questions include:

- "What features should the image editing skill support? Editing, rotation, or others?"
- "Can you provide examples of how this skill would be used?"
- "I can imagine users might say 'remove red-eye from this image' or 'rotate the image 90 degrees'. Are there other trigger patterns?"
- "What kind of user requests should trigger this skill?"

To avoid overwhelming users, don't ask too many questions at once. Ask the most important questions first, then follow up as needed for better effectiveness.

## Progressive Disclosure Principle

**The 200-line rule is critical.** SKILL.md must be less than 200 lines. If more content is needed, split it into `references/` files.

### Three-Tier Loading System

1. **Metadata (name + description)** - Always in context (~100 words)
2. **SKILL.md Body** - When skill is triggered (<200 lines, ideally <500 lines for optimal performance)
3. **Bundled Resources** - As needed by Agent (unlimited)

### Why Progressive Disclosure Matters

- Initial context load reduced by 85%
- Activation time drops from 500ms+ to under 100ms
- Agent only loads what's needed when needed
- Skills remain maintainable and focused

## Skill Structure

```
skill-name/
├── SKILL.md (Required, <200 lines)
│   ├── YAML Frontmatter (Required)
│   │   ├── name: (Required)
│   │   └── description: (Required)
│   └── Markdown Instructions (Required)
└── Bundled Resources (Optional)
    ├── scripts/          - Executable code
    ├── references/       - Documentation loaded on-demand
    └── assets/           - Files used in output
```

## Core Principles

### Brevity is Key

Context window is a shared resource. Your skill shares it with everything else the Agent needs. Be concise and challenge every piece of information:
- Does the Agent really need this explanation?
- Can I assume the Agent knows this?
- Is this paragraph worth its token cost?

### Set Appropriate Degrees of Freedom

- **High Freedom**: Text-based instructions for tasks with multiple valid approaches
- **Medium Freedom**: Pseudocode or scripts with parameters
- **Low Freedom**: Specific scripts for fragile operations with few or no parameters

### Test with All Models

Skills complement models, so effectiveness depends on the underlying model. Test your skills with all models you plan to use.

## References

For detailed guidance, see:
- `references/progressive-disclosure.md` - 200-line rule and reference patterns
- `references/skill-structure.md` - SKILL.md format and frontmatter details
- `references/examples.md` - Good skill examples
- `references/best-practices.md` - Comprehensive best practices guide


# Skill Import Guide

## Step 1: Read Skill Content Based on User-Provided Skill Package Type
- If it's a SKILL.md file, read it directly
- If it's a folder, read all files inside
- If it's a zip file, extract it first then read all files (follow the Skill Package Extraction Guide for extraction method)

## Step 2: Security Review
- Check if skill content complies with security standards
- Check if skill content complies with ethical standards
- Check if skill content complies with legal standards
- Check if skill content contains malicious code or virus behavior

**If security review fails, inform the user immediately, end the skill import process, and terminate the task**


# Skill Package Extraction Guide (Strictly Follow)

Execute the `create-skill/scripts/easyclaw_unzip_skill.py` script to complete skill package extraction

Usage example:
```
python yuanqi_ai_bot_unzip_skill.py "zip_path"
```
Parameter explanation:
zip_path: Path to the zip file to be extracted

**Special emphasis**: For extracting skill packages, you must only follow this extraction guide and run this script. Under no circumstances should you generate other scripts to complete the extraction!



# Easyclaw Skill Registration Guide (Strictly Follow)

Execute the `create-skill/scripts/easyclaw_register_skill.py` script to complete skill registration

Usage example:
```
python easyclaw_register_skill.py <source_folder_path>
```

Parameter explanation:
source_folder_path: Path to the skill folder to be registered to Easyclaw


**Special emphasis**: For registering Easyclaw skills, you must only follow this registration guide and run this script. Under no circumstances should you generate other scripts to complete the registration!

