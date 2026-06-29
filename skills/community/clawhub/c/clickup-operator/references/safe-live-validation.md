# ClickUp Operator Safe Live Validation

Use this when ClickUp is already live and working and the goal is to validate the packaged skill without disturbing the existing setup.

## Core principle

Do not rebuild ClickUp.
Do not replace the current setup.
Do not rewrite the live config.

The validation target is narrower:

- prove the packaged skill reproduces the existing operator behavior
- using the current live workspace
- with the smallest possible number of harmless test actions

## Best validation shape

The safest path is:

1. derive a temporary config snapshot from the existing live setup
2. keep that snapshot separate from any long-term or production config
3. run a tiny smoke test using clearly labeled test items
4. verify behavior
5. optionally clean up the test items after

## Recommended config strategy

Best practice:

- do **not** rewrite the main live config
- do **not** ask Sam to reconfigure ClickUp from scratch
- do **not** replace working defaults

Instead:

- create a temporary validation config file
- fill it with values already known from the live setup
- treat it as a disposable test artifact

Good example:

- `tmp/clickup-operator-validation.config.yaml`

This keeps the validation isolated from the real operating setup.

## Lowest-risk smoke test scope

The smallest meaningful live validation is:

1. one general to-do test item
2. one general idea test item
3. one read test for today's list

Optional fourth step:

4. one project-contained test item

## Labeling rule

Every created test item should be obviously disposable.

Prefix all test items with:

- `TEST - `

This makes cleanup simple and prevents confusion with real work.

## What not to test first

Avoid these in the first smoke test:

- creating brand-new project lists
- moving real production tasks around
- changing real due dates on existing tasks
- reassigning real active work
- any broad bulk operations

Those can come later if needed. They are not required for the first proof.

## Pass criteria

The safe live validation passes if:

- the general to-do goes to the correct live general list
- the to-do gets the expected default assignee
- the to-do gets the expected default due date
- the idea goes to the correct live ideas list
- the idea does not get auto-assigned
- the read query for today's list behaves correctly

Optional project-item pass criteria:

- the project-contained test item lands in the named project list
- it does not get auto-assigned
- it does not get auto-dated

## Cleanup policy

After validation:

- either leave the clearly labeled test items briefly for inspection
- or manually clean up/archive them once behavior is confirmed

Because delete behavior may be restricted by tool surface, cleanup may mean:

- manual removal in ClickUp UI
- status change
- moving to a test/archive area

## Important framing

This is **behavior validation**, not infrastructure validation.

ClickUp already works.
The question is whether the packaged skill reproduces the same decisions Nate already makes in the live environment.
