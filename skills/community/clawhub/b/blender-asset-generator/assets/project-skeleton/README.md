## Project Skeleton (Runnable)

This folder is a template for a runnable Blender 4.2+ project (including 5.x).

### What you do

1. Copy the entire folder as your working project.
2. Edit `spec.json` (or generate it via the Skill).
3. Run the appropriate script:
   - Cloud Windows: `run_cloud_windows.ps1`
   - Local Windows: `run_local_windows.ps1`
   - Local macOS: `run_local_macos.sh`

### Donut Demo

Use the included donut demo scripts to verify your Blender setup quickly:
- macOS: `run_donut_macos.sh`
- Windows: `run_donut_windows.ps1`

### What you get

- `scene.blend`
- `exports/<asset>.glb` (required)
- `exports/<asset>.fbx` (optional)
- `renders/front.png`, `renders/three_quarter.png`
- `run-log.txt`
