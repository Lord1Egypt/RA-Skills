# Geeklink Home 0.1.0 Publish Notes

This directory is the ClawHub publish candidate for `geeklink-home` version `0.1.0`.

Before publishing:

1. Confirm `ownerId` in `_meta.json` is `lintertion`.
2. Keep `slug` as `geeklink-home`.
3. Keep `version` as `0.1.0` for this release.
4. Verify the bundled runtime file exists:
   - `vendor/geeklink-lan-cli.js`
5. Verify the package contains:
   - `SKILL.md`
   - `_meta.json`
   - `.clawhub/origin.json`
   - `scripts/geeklink-home.js`
   - `scripts/geeklink-home.sh`
   - `references/gateway_template.md`

Validated in this release:

- Device catalog listing
- Scene catalog listing
- Local device control
- State snapshot
- Single-instance watcher and recent event tracking in persistent runtime

Known release boundary:

- Some device classes may still need further runtime state enrichment depending on gateway firmware version.
