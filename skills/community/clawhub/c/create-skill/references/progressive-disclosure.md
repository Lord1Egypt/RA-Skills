# Progressive Disclosure

The 200-line rule is important—it's the difference between fast navigation and context confusion.

## Core Principle

Progressive disclosure is not optional. Every skill over 200 lines should be refactored. No exceptions. If you can't fit core instructions within 200 lines, you're putting too much at the entry point.

**Note**: While 200 lines is the strict target, skills up to 500 lines can still perform well. However, for optimal performance, always prefer splitting content into reference files.

## Reference Files are First-Class Citizens

### Structure

- **SKILL.md**: High-level overview, when to use, core principles (<200 lines)
- **references/**: Detailed documentation loaded on-demand
- Each reference file should also be <200 lines when possible

### Example

Instead of creating a 1000-line SKILL.md:
- SKILL.md: Core principles, architecture overview (150 lines)
- references/components.md: Component patterns (150 lines)
- references/routing.md: Routing patterns (100 lines)
- references/forms.md: Form handling (120 lines)
