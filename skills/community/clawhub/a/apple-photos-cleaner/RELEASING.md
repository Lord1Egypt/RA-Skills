# Releasing

Releases ship to [ClawHub](https://www.clawhub.ai/skills/apple-photos-cleaner) as `@and3rn3t/apple-photos-cleaner`.
Merging a version bump to `main` publishes it automatically
([clawhub-publish.yml](.github/workflows/clawhub-publish.yml)), so the PR is the
release. Everything below happens before that merge.

## Versioning

[Semantic Versioning](https://semver.org/), applied to the JSON output as the API:

| Change | Bump |
| --- | --- |
| Bug fix, docs, internal refactor | patch |
| New command, flag or JSON field | minor |
| Removed/renamed flag or JSON field, or a changed field shape | major, and bump `SCHEMA_VERSION` in `scripts/_common.py` |
| Removing behavior that let a mutation run without informed approval | any; see the safety exception in [CONTRIBUTING.md](CONTRIBUTING.md#deprecation-policy) |

Raising the Python floor is called out in the CHANGELOG even when it's a patch.

## Checklist

1. **Branch.** Use `release/vX.Y.Z` off `main`, or bump on the branch carrying the release's last change.
2. **Bump the version in both places.** `tests/test_skill_manifest.py` fails if they disagree:
   - `version:` in the `SKILL.md` frontmatter (the source of truth ClawHub reads)
   - `version` in `pyproject.toml`
3. **CHANGELOG.md.** Move entries under `## [X.Y.Z] - YYYY-MM-DD` (the merge date),
   grouped as Added / Changed / Fixed / Security / Removed. Mention roadmap IDs. Add
   the compare link at the bottom. CI enforces both: `tests/test_skill_manifest.py`
   fails while the SKILL.md version has no dated entry, so the PR stays red until
   it's done. If the merge slips a day, update the date.
4. **ROADMAP.md.** Mark the shipped items done and update the status line.
5. **Run the checks CI runs:**

   ```bash
   ruff check . && ruff format --check . && mypy && pytest --cov=scripts
   ```

   If the release touches date math, AppleScript or a mutating command, also run
   the affected command against a real library (`--human`) and compare with Photos.app.
6. **Dry-run the publish (optional).** Actions → *Publish to ClawHub* → Run workflow
   with `dry_run: true`. It validates the bundle without publishing.
7. **Open the PR** with the CHANGELOG section as its description, then merge once CI is green.
8. **After merge:**
   - Confirm the *Publish to ClawHub* run succeeded and shows the new version.
     ClawHub may first accept it as **pending** while its security scan runs (1.1.0's took
     about an hour); the run summary says so, and `latestVersion` updates once it clears.
     A push that doesn't change the version is a no-op, so a green run with
     "Version unchanged" means the bump didn't land.
   - Check `clawhub inspect apple-photos-cleaner` (or the listing page) shows `X.Y.Z`.
   - Tag the merge commit and push the tag:

     ```bash
     git checkout main && git pull
     git tag -a vX.Y.Z -m "vX.Y.Z" && git push origin vX.Y.Z
     ```

   - Release Drafter keeps a draft named "Next release (draft)" up to date. It has no tag (it doesn't
     guess versions), so publish it by **ID** through the API, with the CHANGELOG section as its notes:

     ```bash
     id=$(gh api repos/and3rn3t/apple-photos-cleaner/releases --jq '[.[] | select(.draft)][0].id')
     gh api -X PATCH "repos/and3rn3t/apple-photos-cleaner/releases/$id" \
       -f tag_name=vX.Y.Z -f name="vX.Y.Z — <theme>" -F body=@notes.md \
       -F draft=false -f make_latest=true
     ```

     (`gh release edit` takes a tag name, not an ID, so it can't address an untagged draft.)

## If a publish goes wrong

ClawHub won't accept the same version twice. Fix forward with a new patch
release rather than trying to overwrite one.
