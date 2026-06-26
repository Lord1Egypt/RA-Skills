# ra-skills 🛡️

> Search **90,896** Hermes Agent skills offline — and download any skill's full folder on demand.

`ra-skills` is a lightweight, dependency-free CLI + library over the
[RA-Skills](https://github.com/Lord1Egypt/RA-Skills) registry. It bundles the
~45 MB metadata index so you can **search instantly offline**, then **download**
a skill's complete folder (`SKILL.md` + scripts, references, assets) straight
from GitHub when you need it.

## Install

```bash
pip install ra-skills
```

## CLI

```bash
ra-skills search github --limit 5      # search by keyword
ra-skills search "" --source ClawHub   # filter by source
ra-skills show apple-notes             # show one skill's metadata
ra-skills stats                        # registry totals by source
ra-skills list --source built-in       # list skills
ra-skills get aso-playbook             # download the FULL skill folder
ra-skills get apple-notes --md-only    # just SKILL.md to stdout
```

(`ra` is a shorthand alias for `ra-skills`.)

## Python API

```python
from ra_skills import search, stats, show, download, fetch_content

search("security", source="ClawHub", limit=5)   # -> list of skill dicts
stats()                                          # -> {total, by_source, ...}
show("github-pr-workflow")                       # -> one skill's metadata
download("aso-playbook", dest="./skills")        # -> full folder on disk
fetch_content("aso-playbook")                    # -> SKILL.md text
```

## Notes

- **Search/stats/show** work fully offline from the bundled registry.
- **Download** pulls live from the RA-Skills GitHub repo. Set `GITHUB_TOKEN` to
  raise GitHub's API rate limit (5,000/hr vs 60/hr).
- 88% of community skills exist as complete folders upstream; the rest are
  genuinely delisted/removed at their source.

MIT © Lord1Egypt
