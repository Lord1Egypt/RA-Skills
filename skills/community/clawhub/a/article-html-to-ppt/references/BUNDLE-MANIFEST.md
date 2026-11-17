# PPT Smith Public Bundle Manifest

## Identity

- Display name: PPT Smith
- Installed route: `article-html-to-ppt`
- Public slug: `meowclaw-pptsmith`
- Version: `5.3.0`
- License: Apache-2.0

`VERSION` and `packaging/identity.json` define the release identity.

## Included material

GitHub, ClawHub and other public distributions contain material needed to
install, use, inspect and package the Skill:

- `SKILL.md`, README usage instructions and route references;
- runtime engine, native builders, rendering and delivery QA tools;
- dependency declarations and the pinned PptxGenJS runtime source;
- schemas, reusable styles, templates and valid authoring examples;
- branding and selected sample previews, editable PPTX files and concise object data;
- identity and distribution checks that keep the package self-contained.

The v5.0 20-slide research example, v5.1 six-slide policy example and two
four-slide template comparison examples retain separate counts and original
file hashes. A replaceable bitmap is not counted as an internally editable
native object.

The v5.2 addition is the unmodified 22-slide Xiaomi Q2/H1 2025 overview PNG.
It was rendered during development commit `af23320`, before the version file
was bumped from `5.1.1` to `5.2.0`. Only the preview and a concise scope summary
are included; its source inputs, full PPTX, logs and evidence package are not.

Version 5.2.1 adds the written two-round business report case, planning/review
guidance and read-only composition observations. The case's original 5.2.0 runs
are not relabelled as 5.2.1 tests; no additional customer source files or decks
are included.

## Version 5.3.0: native template workflow and current showcase

Original-page template tools now run inside the host agent's existing Python
workflow: clone source-bound pages, edit native objects, inherit source styles,
apply revision-checked patches, export, render and ingest hash-bound external
review. Existing component/Atlas tasks remain compatible. Deterministic source
retention/type-scale checks do not replace visual, factual or business review.
The new executor requires POSIX fcntl/O_NOFOLLOW; Windows is unsupported.

The user-provided 36-slide Xiaomi Q2/H1 2025 template-route result is displayed
through actual office-rendered previews. Only the overview, three selected page
images and concise public evidence are included. The original PPTX, full-size
render output, source material and logs remain local. Inspection of the supplied
file is not relabelled as a newly repeated end-to-end generation run.

## Local-only material

Development fixtures, CI, benchmark harnesses, development notes,
promotional articles, source PDFs, full review/edit logs, intermediate builds,
worktrees, caches, credentials and private customer/commercial materials are
excluded from the public source tree and registry bundle. Local files are
preserved for development. Exclusion does not rewrite earlier published history.

The public source tree intentionally includes focused composition and native-template
regression tests. All development tests remain excluded from registry/runtime archives.

`.gitignore` prevents normal staging of local-only files. `.clawhubignore`
filters registry packaging, `.gitattributes` filters source exports, and
`packaging/bundle-exclude.txt` makes their presence fail the archive audit.
Only intentionally selected usage examples belong in `assets/samples/`.

## Checks

```bash
python3 scripts/check_identity.py
python3 scripts/quick_validate_skill.py
python3 -m engine design capabilities
```

The public bundle builder audits the exact selected tree before creating the
ZIP. Its detailed audit reports and archive manifest stay beside the local
packaging output; the ZIP contains runtime and usage material. The package
version does not by itself mean any external platform has been updated.
