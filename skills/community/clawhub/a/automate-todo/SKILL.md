---
name: automate-todo
description: 'Complete TODO.md items nested under the level 2 header "Current", then update documentation, CHANGELOG.md, and manifest files according to the version update each item indicates. Use when asked to automate TODO items, work through the Current section of TODO.md, apply the next version update, maintain a current road map, or archive completed TODO items to a Complete section. Bundles scripts/todo.mjs for moving checked items.'
---

# Automate TODO

Complete all items listed under the level 2 header **Current** in the
`TODO.md` file at the root of the workspace or repository.

- If level 2 header **Current** does not exist:
  - Create level 2 header in `TODO.md`
  - Resolve to `Else if no TODO` condition of `CHANGELOG.md Updating` section
    of this skill

Once completed, update:

- Relevant documentation files
- The repository or workspace `CHANGELOG.md` according to the nested **From**
  list item of a **current** `TODO` item
- If **manifest** file exists (e.g., `package.json`, `tsconfig.json`, etc.), then:
  - Update **manifest** file according to:
    - Version update applied
    - Any newly introduced items from the update
- **Testing**: Write and test the updates, and:
  - If pass, then:
    - Resolve to `Closing` section of this skill as **applied**
  - Else:
    - While update and test attempts are less than 3, then:
      - Debug failing items from test, and resolve back to **Testing** parent
        list item (*recurse*)
    - Else if update and test attempts are 3 or more, then:
      - Undo failing updates, and add the corresponding `TODO` items back to
        the **Current** `TODO.md` section as incomplete, then:
        - Note completed `TODO` items and resolve to `CHANGELOG.md Updating`
          section of this skill
        - Resolve to `Closing` section of this skill as either:
          - Updates **partially applied**, and:
            - Revert relevant files according to failing and passing updates
          - Updates **not applied**, and:
            - Restore all relevant files, so essentially:
              - In the terminal run: `git restore .`

## Nested **From** List Items or Property

A **current** `TODO` item should have a nested **From** list item, which will
be followed by text that either fully or **partially** matches another level 2
header in the `TODO.md` file. In regards to the **matching level 2 header**:

### Applying Next Version Update

- The text of the level 2 header that matches the nested **From** list item
  of a `TODO` in the **Current** section will include instructions or
  specific text specifying the next version update to apply
- If the `TODO` item in the **Current** section does not have a corresponding
  nested list item starting with **From**, then apply the next version update
  accordingly

### `CHANGELOG.md` Updating

Resolve to the `Applying Next Version Update` section of this skill, then:

- If 1 list item is in the **Current** section of the `TODO`, then:
  - Resolve to `Constant CHANGELOG Conditions` section of this skill
- Else if multiple `TODO` items are in the **Current** section, then:
  - If nested **From** exists in all **Current** `TODO` items:
    - Resolve to the **Priority Version Updates** section of this skill
    - Resolve to `Constant CHANGELOG Conditions` section of this skill
  - Else if nested **From** does not exist in any **Current** `TODO` items:
    - Indicate the next version update accordingly for each
    - Resolve to the **Priority Version Updates** section of this skill
    - Resolve to `Constant CHANGELOG Conditions` section of this skill
  - Else if nested **From** exists in some of the **Current** `TODO` items:
    - Indicate the next version update accordingly for each list item missing
      the nested **From** property
    - Resolve to the **Priority Version Updates** section of this skill
    - Resolve to `Constant CHANGELOG Conditions` section of this skill
- Else if no `TODO` items are in the **Current** section, then:
  - Do not update the current workspace or repository
  - Instead:
    - Resolve to `Current Road Map Document` section of this skill with
      *no updates applied*

### Priority Version Updates

1. **Highest**: Major version update indicated
   - Example: `1.0.0` to `2.0.0`
2. **Moderate**: Minor version update indicated
   - Example: `1.1.0` to `1.2.0`
3. **Lowest**: Patch version update indicated
   - Example: `1.0.0` to `1.0.1`

### Constant `CHANGELOG` Conditions

- If `CHANGELOG.md` current version is using append text like `alpha`,
  `beta`, etc., then:
  - Continue to use the appended version text
- For each `TODO` list item in the **Current** section:
  - Resolve next version priority
  - Next version remains the same
- Once all **Current** `TODO` items have been completed, then:
  - Resolve to `Current Road Map Document` section of this skill with
    *updates applied*

## Current Road Map Document

1. Read the `CHANGELOG.md` at the latest version, then read the
   workspace or repository source code
2. Add a set of existing `TODO` items to the **Current** section of the
   `TODO` in regards to:
   - Relative to the current source code state, determine the best order of
     `TODO` items to apply in sequential order
     - If the file `current.roadmap.md` does not exist in the workspace or
       repository `.github` (*create if not exist*) folder, then:
       - Create `current.roadmap.md` in the workspace or repository `.github`
         folder (*create if not exist*)
       - Write the determined sequence of updates to `current.roadmap.md`
     - Else:
       - Update and write the determined sequence of updates to
         `current.roadmap.md`
   - If *updates applied*, then:
     - Resolve to top-level **Testing** list item
   - Add a sequence of `TODO` items to the **Current** section
     - Max Items: 5 (*initial last item value*)
     - **Evaluate compatibility**: use the next sequence of `TODO` items
       compatibility to each other, then:
       - If next 5 determined `TODO` items are not compatible, then:
         - From sequentially 1st item to sequentially last item, remove the
           sequentially last item
         - Re-evaluate compatibility: resolve back to
           **Evaluate compatibility** parent list item (*recurse*)

## Move Completed `TODO` items

Run the bundled maintenance script [scripts/todo.mjs](scripts/todo.mjs) from
the workspace or repository root:

```bash
node <path-to-this-skill>/scripts/todo.mjs
```

The script:

- Defaults to `TODO.md` in the current working directory; an explicit path
  may be passed as the first argument (`node scripts/todo.mjs path/to/TODO.md`)
- Moves every checked top-level item (`- [x] ...`, with its wrapped
  continuation lines and nested sub-items) out of its roadmap section and
  into a `## Complete` section, created on first use and always kept at the
  bottom of the file
- Stamps each archived item with a nested `- From: <section>` line recording
  the roadmap section it came from, unless the item already carries its own
  `- From:` note, which is preserved
- Is idempotent: items already under `## Complete` stay where they are, so
  running the script repeatedly is a no-op
- Leaves nested checked items under an unchecked parent in place; the parent
  keeps its context until it is checked off as a whole

## Closing

Before finishing, ensure that:

1. Changes have been tested and applied correctly
2. Based on the status of applied changes, ensure that:
   - **Relevant Files**:
     - [ ] Relevant documentation files have been updated
     - [ ] `CHANGELOG.md` has been updated
     - [ ] **Manifest** file has been updated
3. If closing was called after testing as:
   - **applied**: then resolve to `Move Completed TODO items` section of this
     skill
   - **partially applied**: then ensure:
     - Failing **Current** `TODO` items have been moved back, and are unchecked
     - Resolve to `Move Completed TODO items` section of this skill
   - **not applied**: then restore all changes, reverting workspace or
     repository back to its prior state
