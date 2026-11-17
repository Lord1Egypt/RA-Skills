## Token Usage & Workflow Recommendation

> ⚠️ This workflow involves generating multiple high-resolution images, animation frames, sprite sheets, previews, and validation assets. Image generation tasks may consume a significant amount of tokens, especially when creating multiple actions and maintaining character consistency.

Because the workflow requires:

- Character master generation
- Multiple animation action generations
- Frame-by-frame sprite extraction
- Alignment previews
- GIF previews
- Iterative refinement

the total token usage can increase quickly depending on:

- Number of animation actions
- Frame count per action
- Image resolution
- Number of generation iterations
- Character refinement requirements

## Recommended Usage

For the best results, use this workflow together with **Brainstorming mode** before starting the actual generation process.

Recommended workflow:

1. **Brainstorm the character design**
   - Define character identity
   - Decide style direction
   - Select color palette
   - Confirm personality and animation behavior
2. **Plan animation requirements**
   - Decide required actions
   - Define frame counts
   - Determine looping behavior
   - Prioritize important animations
3. **Generate the final assets**
   - Create the character master
   - Generate animation sprites
   - Build the sprite package
   - Run alignment and validation

Using brainstorming first helps reduce unnecessary regeneration, avoid design changes during production, and improve token efficiency while maintaining higher-quality results.

For large projects, it is recommended to generate assets incrementally:

- Phase 1: Character master and style approval
- Phase 2: Core animations (idle, walk, interact)
- Phase 3: Additional expressions and special actions
- Phase 4: Packaging, validation, and web integration

This approach minimizes wasted generation attempts and provides better control over production quality.