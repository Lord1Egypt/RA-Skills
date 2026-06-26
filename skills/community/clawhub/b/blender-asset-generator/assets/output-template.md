## Output Template (MVP)

### Project Package

```text
<project-root>/
  spec.json
  reference_images/        (optional)
  scripts/
    build.py
    render.py
    export.py
  renders/
    front.png
    three_quarter.png
  exports/
    <asset>.glb
    <asset>.fbx           (optional)
    <asset>.usdc          (optional)
  run-log.txt
  scene.blend
```

### Run Instructions

Cloud PC (Windows):
- Use `run_cloud_windows.ps1`

Local (Windows):
- Use `run_local_windows.ps1`

Local (macOS):
- Use `run_local_macos.sh`

### QA + Evaluation

- Checklist: `references/qa-checklist.md`
- Verdict: Achieved | Partially Achieved | Not Achieved
- Top fixes:
