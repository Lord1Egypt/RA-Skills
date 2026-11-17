# Spec To Deck Visual Priority Gate

Use when a user provides a detailed PPT spec, coordinates, placeholder map, brand template, or page-by-page layout description.

A detailed spec is not a command to draw every object at full strength. Treat it as design intent plus candidate inventory.

## Required Plan

Before PPT implementation, create `spec_implementation_plan.json` with:

- slide intent
- primary visual anchor
- object roles
- visual priority levels
- keep/merge/weaken/move/delete decisions
- connector, icon, grid, and table budgets
- editable core
- material/raster layers
- delivery route for complex components

## Object Roles

- `message`: states the judgment
- `proof`: supports the judgment
- `structure`: organizes reading order
- `navigation`: section/page orientation
- `brand`: restrained identity cue
- `material`: mood/background layer
- `decoration`: optional texture

## Priority Levels

- `hero`: main anchor; never competes with another hero.
- `primary`: required for meaning; editable and high contrast.
- `secondary`: support; grouped and lower contrast.
- `tertiary`: context; may move to notes/footer.
- `delete`: noise or duplication.

## Hard Deletion Triggers

- decorative grid competes with content
- connector line does not clarify flow or dependency
- icon repeats label without meaning
- table cell forces body text below minimum size
- more than two callout systems compete
- multiple diagrams explain the same relationship
- background motif distracts from the primary anchor
