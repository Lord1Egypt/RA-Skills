# Teams Runtime Troubleshooting

## Purpose

Use this guide when the Teams page source code looks correct, but live behavior still drops fields like `parentId` during save.

This is specifically for cases where:
- the UI shows a Parent Team selector
- the editor appears to save
- after save, the team reverts to `No parent team`
- `updatedAt` changes, but `parentId` never persists

## Symptom pattern

Typical symptom chain:
1. User selects a parent team in the editor
2. Clicks **Save**
3. UI refreshes
4. Parent selection is gone
5. Registry file on disk shows no `parentId`

If this happens, the live runtime is probably still serving an older teams handler or registry normalizer.

## Root cause pattern

The most important lesson:

**Do not trust source files alone.**

In this failure mode, source files already support `parentId`, but the compiled runtime bundle still uses the old logic. The old runtime path rewrites the saved team without `parentId`, effectively stripping the field on every save.

A common smoking gun is a compiled `normalizeTeamRecord()` that still returns:
- `id`
- `name`
- `description`
- `agentIds`
- `createdAt`
- `updatedAt`

but not `parentId`.

## Fast diagnosis

### 1. Check the registry file

Inspect:

```text
~/.openclaw/workspace/teams/teams.json
```

If save truly worked, the edited team should contain:

```json
{
  "parentId": "marketing-team"
}
```

If `updatedAt` changes but `parentId` is missing, the save path is stripping it.

### 2. Verify source and runtime separately

Check both:
- source handler files
- compiled runtime bundle actually serving gateway RPCs

Do not stop after confirming source code is correct.

### 3. Inspect compiled bundle contents

Search the built gateway/runtime artifacts for:
- `teams.create`
- `teams.update`
- `function normalizeTeamRecord`
- `parentId`

If the compiled bundle lacks `parentId` support, the live service will keep deleting it on save.

## Fix workflow

### Preferred fix

1. update source files
2. rebuild the correct runtime artifact
3. restart the gateway
4. save again
5. verify `parentId` persists in `teams.json`

### If rebuild output is not taking effect

If the correct source exists but the deployed runtime still serves stale code:
1. locate the exact runtime bundle used by the gateway
2. patch the active bundle if necessary
3. restart the gateway
4. verify by saving again and re-reading the registry file

## Verification checklist

A fix is not complete until all of these are true:
- Parent Team dropdown still appears
- selecting a parent and saving keeps the selection in the UI
- `teams.json` contains `parentId`
- reloading the page still shows the parent relationship
- child team appears nested under its parent in the left tree

## Regression guard

When changing Teams save logic in future, always test this exact scenario:

1. create a parent team
2. create a child team nested under it
3. save
4. re-open child team
5. verify parent selector still shows the parent
6. verify `teams.json` still contains `parentId`
7. reload the UI and verify nesting still renders

If any one of those fails, the implementation is not done.
