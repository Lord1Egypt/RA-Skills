# Install

## Package Contents

- Binary: `assets/bin/skillscan`
- Skill document: `SKILL.md`
- Build metadata: `assets/build/build-info.json`
- SHA-256: `assets/build/skillscan.sha256`

## Install Steps

1. Unzip the release package.
2. Optionally verify the checksum:

```bash
shasum -a 256 assets/bin/skillscan
cat assets/build/skillscan.sha256
```

3. Run the binary directly:

```bash
./assets/bin/skillscan review /path/to/skill
./assets/bin/skillscan review /path/to/skills --output-dir /tmp/skillscan-out
```

4. If you want to use an external scanner bridge:

```bash
./assets/bin/skillscan review /path/to/skill --engine external
```

5. For batch review in enterprise environments:

```bash
./assets/bin/skillscan review /path/to/skills \
  --output-dir /tmp/skillscan-out \
  --upload-url https://scanner.example.com/api/report \
  --instance-id prod-a1
```

The upload payload contains embedded review details for each skill, including the full scan summary and findings.

## Common Commands

```bash
./assets/bin/skillscan inspect /path/to/skill
./assets/bin/skillscan scan /path/to/skill
./assets/bin/skillscan review /path/to/skill
./assets/bin/skillscan benchmark
./assets/bin/skillscan package-skill
```
