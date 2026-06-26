# Recommended Prompt

```
Using the figma-pixel skill, build the layout from Figma <FigmaURL>. Run the full pipeline from the skill. If any problems come up, report them immediately — don't try to silently work around them.
```

Replace `<FigmaURL>` with the actual Figma link (including `node-id` parameter for a specific frame).

## Optional additions

| Need | Add to prompt |
|---|---|
| Reuse shared Figma data | `Reuse shared artifacts from figma-pixel-runs/ if available` |
| Cleanup preference | `Clean up working files in figma-pixel-runs/ when done` |
| Multiple iterations | `Iterate until mismatch is below X%` |
