<p align="center">
  <img src="assets/claw3d-logo.png" alt="claw3d" width="300">
</p>

# claw3d — Unified 3D Skill for OpenClaw

Single skill for the full 3D workflow: create models (AI), search (Thingiverse), slice, and print. Modular at install time—enable only what you need.

---

## Structure

```
claw3d-skill/
├── SKILL.md              # Generated output (do not edit directly)
├── manifest.json         # Module registry
├── src/
│   ├── 00-frontmatter.md # Skill metadata template
│   ├── 01-core.md        # Setup flow, intent resolution (always included)
│   ├── 02-ai-forger.md   # AI model creation (FAL)
│   ├── 03-directory.md   # Search Thingiverse
│   ├── 04-slicing.md     # Slice to G-code
│   └── 05-printing.md    # Printer control
├── scripts/
│   └── build-skill.sh    # Merge modules → SKILL.md
├── backends/             # Community: printer backends (Moonraker, PrusaLink, OctoPrint…)
├── providers/            # Community: AI providers (FAL, Replicate, local…)
└── directories/          # Community: search providers (Thingiverse, Printables…)
```

## Build

```bash
cd claw3d-skill
./scripts/build-skill.sh --modules ai-forger,directory,slicing,printing
```

Or with env:

```bash
CLAW3D_MODULES=ai-forger,printing ./scripts/build-skill.sh
```

## Adding Modules (Community)

1. **New printer backend** — Add `backends/moonraker.md` (or similar) with backend-specific notes. Document in the main printing module that `claw3d configure backends` lists options. The CLI (`claw3d`) handles backend logic; the skill documents usage.

2. **New AI provider** — Add `providers/replicate.md`. Update `manifest.json` if the provider becomes a first-class module. The skill references `claw3d configure` for provider selection.

3. **New directory** — Add `directories/printables.md`. Update `03-directory.md` or create `03-directory-printables.md` and extend the manifest. Run `build-skill.sh` to merge.

4. **New module** — Add `src/06-your-module.md`, register in `manifest.json` under `modules`, then run build with `--modules` including your module.

## Install-Time Selection

The setup script (`claw3d/scripts/setup-openclaw-docker.sh`) prompts for capabilities and builds the skill with only the selected modules. This keeps the installed skill focused and avoids unused API key requirements.

## Related projects

| Repo | Description |
|------|-------------|
| [clarvis-ai](https://github.com/makermate/clarvis-ai) | One-command distro — bundles everything into a single Docker Compose stack |
| [claw3d](https://github.com/makermate/claw3d) | Python CLI that this skill orchestrates — AI generation, slicing, printer control |
| [curaengine-slicer-api](https://github.com/makermate/curaengine-slicer-api) | CuraEngine REST API for slicing and mesh conversion |

## License

MIT

---

<p align="center">
  <a href="https://clarv.is">
    <img src="assets/clarvis_logo.png" alt="Clarvis" width="140">
  </a>
</p>

<p align="center">
  For a ready-to-use, anything-to-3D-print experience, check out <a href="https://clarv.is">clarv.is</a>
</p>
