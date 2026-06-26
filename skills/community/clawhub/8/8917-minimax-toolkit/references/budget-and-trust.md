# Budget and Trust Notes

## Read this file when
- You need Token Plan request-cost guidance
- You need to explain privacy / upload behavior to the user
- You need to decide whether to rely on local estimates or official remains data

## Token Plan key rules
This skill is designed for **MiniMax Token Plan API keys**.

Lookup priority:
1. `MINIMAX_API_KEY`
2. `~/.openclaw/openclaw.json`

Do not assume Token Plan keys and pay-as-you-go API keys are interchangeable.

## Execution-time disclosures
Before execution, disclose at least:
- target model
- estimated request usage
- whether the model follows **5-hour rolling window** or **daily quota**
- high-cost warning for expensive tasks, especially video

## Quota rules (latest verified FAQ)
- **Text models**: 5-hour rolling window
- **Non-text models** (image / speech / video / music / voice): daily quota reset

## Important caution about remains API
The skill can query official remains data via:
```bash
python3 scripts/mm.py remains
```

However, until we manually validate the field semantics against the official Token Plan web console, remains output should be treated as **raw reference data**, not a fully trusted “balance dashboard”.

## Media handling and privacy
This skill may send user-provided media to MiniMax APIs in these cases:
- image generation / image-to-image
- video generation / video template workflows
- speech synthesis / long-text TTS
- voice cloning / voice design
- music generation

For sensitive image, audio, or video tasks, confirm the user accepts third-party API processing before execution.

## Voice-specific trust notes
### Voice clone
- Current official flow: `files/upload` → optional prompt upload → `voice_clone`
- Cloned voices may be deleted if not formally used within 7 days
- Official docs mention possible permission error `2038`

### Voice design
- Current official endpoint: `voice_design`
- `preview_text` is required
- Returned `voice_id` should be treated as a generated asset that needs later actual use/verification

## Output behavior
Output root priority:
1. `--output-dir`
2. `MINIMAX_OUTPUT_DIR`
3. `workspace/03-Resources/minimax-output/`
4. `./outputs/minimax/`

Always report:
- media type
- saved path
- suggestion to organize into a project directory when needed

## Typical request estimates
See also `references/costs.json`, `references/api_info.md`, and `references/quota_mapping.json`.

Examples from local estimates:
- Text: ~1 unit / call
- Image: ~75 units / image
- Video (`MiniMax-Hailuo-02`): ~4500 units / 6s video
- Speech HD: ~600 units / 1000 characters
- Music (`music-2.5+`): ~3000 units / 5 min song
