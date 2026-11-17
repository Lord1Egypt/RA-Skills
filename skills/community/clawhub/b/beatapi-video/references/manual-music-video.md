# Manual Music Video workflow

Use this flow only when the user wants shot-level review, selection, ordering,
or edits.

## 1. Create the storyboard task

Copy `../assets/music-video.manual.json`, fill valid public media URLs, and
create the task:

```bash
beatapi music-video create --file /tmp/beatapi-music-manual.json
beatapi tasks wait TASK_ID --interval 7000 --attempts 120
```

The wait command intentionally stops at `storyboard_ready` or
`requires_action`.

## 2. Inspect the storyboard

Read `storyboard.shots[]`. Preserve each BeatAPI `shot_id`; do not substitute
the numeric index.

When the user did not already specify a selection, present a compact table with:

- shot ID and index;
- status;
- duration;
- prompt or lyric text;
- existing media URL when present.

Ask for selection/order only at this decision point.

## 3. Edit optional shots

Shot edits consume credits based on selected quality/resolution and duration.
An explicit edit request authorizes that edit; otherwise confirm before adding
it.

```bash
beatapi music-video shots edit TASK_ID SHOT_ID \
  --prompt "Night city chorus with brighter face lighting."
```

For quality, resolution, or duration controls, copy the full edit object to a
temporary JSON file and use `--file`.

After an edit is accepted, wait until the task returns to an actionable
storyboard state. Retrieve the shot media when the user needs to review it:

```bash
beatapi music-video shots media TASK_ID SHOT_ID
```

Do not call shot media retrieval for every shot without a reason; storyboard
shot videos are materialized on demand or after editing.

## 4. Compose

Pass selected shot IDs in the exact desired order. Composition consumes one
additional BeatAPI credit.

```bash
beatapi music-video compose TASK_ID \
  --shot SHOT_1 \
  --shot SHOT_2
```

Then wait for `succeeded` or `failed`:

```bash
beatapi tasks wait TASK_ID --interval 7000 --attempts 120
```

Report the final hosted output only after `output.media[]` is present.
