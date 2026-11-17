---
name: custom-ui-spec
version: "0.1.0"
license: Apache-2.0
description: "A highly customizable UI design specification system based on headless component libraries (shadcn/ui, Radix UI), integrating Apple HIG, Microsoft Fluent, and Google Material Design. Unlike using off-the-shelf frameworks (Ant Design, Element Plus), this skill is for scenarios requiring full control over component styles and DOM structure, emphasizing design freedom and brand customization. Use when: generating custom UI code, reviewing custom UI designs, or needing to follow platform-specific design guidelines. Supports HIG / Fluent / Material / All specification modes. Keywords: shadcn/ui, Radix UI, headless, custom components, HIG, Fluent, Material Design."
metadata:
  openclaw:
    emoji: 📐
    requires:
      bins:
        - python3
---

# Custom UI Spec

## Overview

This skill provides strict definitions for the three major design specifications — Apple HIG, Microsoft Fluent, and Google Material Design — to guide highly customizable UI implementations based on headless component libraries like shadcn/ui and Radix UI.

Unlike scenarios using off-the-shelf UI frameworks (e.g., TDesign), this skill is for projects that require full control over component anatomy and styling, emphasizing design freedom, brand customization, and cross-platform design consistency.

## Specification Selection Decision Tree

**Dimension A: Target Platform (default recommendation)**

| Platform | Recommended Spec | Rationale |
|---|---|---|
| iOS / iPadOS / macOS / watchOS / tvOS | HIG | Native Apple ecosystem experience |
| Windows / Xbox | Fluent | Native Microsoft ecosystem experience |
| Android / Web / Flutter | Material | Native Google ecosystem experience |
| Cross-platform / Unsure | Ask about design tone preference | See Dimension B |

**Dimension B: Design Tone Preference (when platform is unclear)**

| Design Tone | Recommended Spec | Typical Scenarios |
|---|---|---|
| Refined, native, restrained, layered | HIG | Utility apps, productivity software, Apple ecosystem products |
| Productive, professional, deep, luminous | Fluent | Enterprise software, office suites, Windows ecosystem products |
| Bold, graphical, tactile, dynamic | Material | Consumer apps, creative products, Google ecosystem products |

**Decision Flow:**

```
User specified a spec explicitly?
├── Yes → Use the specified spec directly
└── No → User specified a target platform?
    ├── Yes → Recommend per Dimension A
    └── No → Ask about design tone preference (Dimension B)
        └── User chooses "All" → Comprehensive cross-check (flag cross-spec conflicts)
```

## Usage Modes

### Generation Mode

Before generating UI code:
1. Determine the target spec using the decision tree
2. Read the corresponding `references/<spec>.md` for the complete specification
3. Implement compliant styles using headless components like shadcn/ui
4. Run `scripts/validate_ui.py` for automated validation
5. Self-check against `references/checklist.md` item by item
6. Output the validation report

### Review Mode

When reviewing existing UI code/design:
1. Determine the target spec based on code characteristics or user input
2. Run `scripts/validate_ui.py` for automated static analysis
3. Cross-check against `references/checklist.md` item by item
4. Output the validation report (Pass / Warning / Error)

## Validation Flow

Three-step validation:

1. **Automated check**: Run `scripts/validate_ui.py --spec <hig|fluent|material> --file <path>` or `--text <code>`
2. **Manual self-check**: Agent cross-checks against `references/checklist.md` item by item
3. **Report output**: Combine automated results and manual review into a structured validation report

Color checks are skipped by default. Add `--check-color` to enable them.

## Component Mapping Quick Reference

| Unified Name | HIG | Fluent | Material |
|---|---|---|---|
| Button | Button | Button | Button |
| TextField | Text Field | Input | Text Field |
| Checkbox | Checkbox | Checkbox | Checkbox |
| RadioButton | Radio Button | Radio | Radio Button |
| Switch | Toggle | Switch | Switch |
| Slider | Slider | Slider | Slider |
| ProgressIndicator | Progress View | Progress Bar | Progress Indicator |
| Menu | Menu | Menu | Menu |
| Dialog | Alert / Sheet | Dialog | Dialog |
| Card | — | Card | Card |
| List | List | List | List |
| NavigationBar | Navigation Bar | Navigation | App Bar / Bottom App Bar |
| TabBar | Tab Bar | Tab | Tabs |
| SegmentedControl | Segmented Control | — | — |
| Tooltip | Tooltip | Tooltip | Tooltip |
| Badge | Badge | Badge | Badge |
| Chip | — | Tag | Chip |
| DatePicker | Date Picker | Date Picker | Date Picker |
| Table | Table | Data Grid | Data Table |
| Breadcrumb | — | Breadcrumb | — |
| Select | Pop-up Button | Dropdown | Exposed Dropdown Menu |
| Autocomplete | — (inferred) | Combobox | — (inferred) |
| Textarea | Multiline Text Field | Textarea | Text Field (multiline) |
| NumberInput | Stepper + Field | SpinButton | — (inferred) |
| Upload | — (inferred) | — (inferred) | — (inferred) |
| Toast | — (inferred) | Toast | Snackbar |
| Notification | — (inferred) | — (inferred) | — (inferred) |
| Alert·Banner | — (inferred) | MessageBar | Banner |
| Skeleton | — (inferred) | Skeleton | — (inferred) |
| Drawer·Sidebar | Sidebar | NavigationView | Navigation Drawer |
| Pagination | — (inferred) | — (inferred) | — (inferred) |
| Stepper | — (inferred) | — (inferred) | Stepper |
| Sheet·ActionSheet | Action Sheet | — (inferred) | Bottom Sheet |
| Avatar | — (inferred) | Avatar / Persona | Avatar |
| Accordion | Disclosure | Accordion | — (inferred) |
| Carousel | Page Control | Carousel | Carousel |
| Timeline | — (inferred) | — (inferred) | — (inferred) |
| Tree | Outline View | TreeView | — (inferred) |
| Divider | Separator | Divider | Divider |
| Grid·Layout | — (inferred) | — (inferred) | Grid |
| Space·Stack | — (inferred) | Stack | — (inferred) |
| AspectRatio | — (inferred) | — (inferred) | — (inferred) |
| Popover | Popover | Popover | — (inferred) |
| Modal | Modal Sheet | Modal Dialog | Full-screen Dialog |
| FAB | — (inferred) | — (inferred) | FAB |
| SearchBar | Search Field | SearchBox | Search Bar |
| Rating | — (inferred) | Rating | — (inferred) |
| ColorPicker | Color Well | ColorPicker | — (inferred) |
| Calendar | Calendar View | Calendar | Date Calendar |

See `references/component-specs.md` for detailed definitions.

## Resource Reference

| File | When to Read |
|---|---|
| `references/apple-hig.md` | When HIG spec is selected |
| `references/microsoft-fluent.md` | When Fluent spec is selected |
| `references/google-material.md` | When Material spec is selected |
| `references/component-specs.md` | When detailed component definitions or cross-spec comparison is needed |
| `references/interaction-guidelines.md` | When user interaction behavior specs (navigation/gestures/feedback/confirmation/undo) are needed |
| `references/checklist.md` | When performing manual self-checks |
| `scripts/validate_ui.py` | When running automated validation |
