# Plan Schema

Use `scripts/run-recording.mjs <plan.json>`.

## Shape

```json
{
  "meta": {
    "title": "Short label for the recording",
    "outputBasename": "optional-output-name",
    "outputDir": "/path/to/workspace/media",
    "browserURL": "http://127.0.0.1:18800",
    "viewport": {
      "width": 1600,
      "height": 1200,
      "deviceScaleFactor": 1
    }
  },
  "steps": []
}
```

## Step Types

- `goto`: open a URL; supports `url`, `waitUntil`, `timeoutMs`, `holdMs`
- `hold`: wait on the current page; supports `ms`
- `move`: move cursor through `points` or a single `target`
- `click`: click a target; supports `waitForNavigation`, `switchToNewPage`, `waitForUrlIncludes`, `holdMs`
- `scroll`: wheel-based smooth scroll to `targetY` or a matched `target`; also supports `stepY`, `stepWaitMs`, `moveSteps`, `anchorX`, and `anchorY`
- `type`: click into a target and type text; supports `text`, `delay`, `clear`, `submit`, `holdMs`
- `press`: press a keyboard key; supports `key`, `holdMs`
- `evaluate`: run small page-side JS; supports `code`, `args`, `holdMs`

## Target Matching

A target can be either coordinates:

```json
{ "x": 800, "y": 450 }
```

Or DOM-based matching:

```json
{
  "selector": "a,button,input",
  "tag": "A",
  "text": "Explore Video Skills - Free"
}
```

Useful target fields:

- `selector`: CSS selector pool to search within
- `tag`: expected tag name
- `text`: exact visible text
- `textIncludes`: partial visible text
- `href`: exact link URL
- `index`: choose the Nth match when there are duplicates
- `offsetX` / `offsetY`: click offset from the center

## Notes

- Homepage forms that open a new tab can be converted to same-tab via an `evaluate` step before clicking submit.
- Output video and debug JSON are written to the `outputDir`, which should usually be `workspace/media`.
