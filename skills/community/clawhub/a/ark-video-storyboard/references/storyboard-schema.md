# Storyboard Schema

Use this schema for the full 60-second plan and for each 15-second segment.

## Full Output

```json
{
  "title": "string",
  "theme": "string",
  "total_duration_seconds": 60,
  "character_rule": "All human characters are East Asian unless explicitly specified otherwise.",
  "style_summary": "string",
  "overall_story": "string",
  "segments": []
}
```

## Segment Schema

Each segment must be 15 seconds by default.

```json
{
  "segment_index": 1,
  "start_second": 0,
  "end_second": 15,
  "duration_seconds": 15,
  "story_function": "establish | deepen | peak | resolve",
  "visual_description": "中文，描述画面、主体、动作、环境、构图",
  "lighting_state": "中文，描述亮度、主光、轮廓光、氛围",
  "continuity_notes": "中文，说明与上一段和下一段的衔接",
  "camera_language": "中文，可选，说明镜头视角、运动、节奏",
  "voiceover_or_caption": "中文，可选",
  "ai_prompt": "English prompt for generation",
  "negative_prompt": "optional English negative prompt"
}
```

## Required Fields

Every segment must include:

- `segment_index`
- `duration_seconds`
- `visual_description`
- `lighting_state`
- `continuity_notes`
- `ai_prompt`

## Continuity Checklist

Before finalizing the 4 segments, verify:

- Same person remains visually consistent
- Same scene logic remains believable
- Props do not randomly appear/disappear
- Lighting changes are intentional
- Segment 4 feels like an ending, not a random cut

## Output Style

- Keep Chinese planning fields concrete and visual.
- Keep English prompts cinematic and executable.
- Avoid vague words like “nice”, “beautiful”, “good vibe” without visual anchors.
