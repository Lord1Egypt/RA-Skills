# Clawmerge Publishing Checklist

ClawHub CLI v0.12.x does **not** support `clawhub skill publish --dry-run`.
Use this checklist before publishing.

## Preflight

```bash
cd ~/.openclaw/workspace

grep -E '^(name|version):' skills/clawmerge/SKILL.md
bash -n skills/clawmerge/scripts/*.sh
python3 -m py_compile skills/clawmerge/scripts/*.py
openclaw skills info clawmerge
```

## Safety smoke tests

```bash
# backup preview
bash skills/clawmerge/scripts/one-click-full-backup.sh /tmp/clawmerge-test.tar.gz --dry-run

# if you have a backup file, restore preview only
bash skills/clawmerge/scripts/one-click-full-restore.sh /path/to/backup.tar.gz --dry-run
```

## Publish

```bash
clawhub whoami
clawhub skill publish skills/clawmerge \
  --slug clawmerge \
  --name clawmerge \
  --version <version> \
  --changelog '<changelog>'
```

## Verify after publish

```bash
clawhub inspect clawmerge --json
clawhub search clawmerge --limit 5
```

## Policy

- Do not claim publish dry-run support unless the installed `clawhub` CLI actually supports it.
- Prefer a patch version bump for documentation/safety changes.
- Disaster restore defaults must remain safe; destructive live overwrite requires `--unsafe-overwrite`.
