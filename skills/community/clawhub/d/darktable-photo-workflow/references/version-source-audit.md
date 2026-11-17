# Version and source audit

## Scope and date

Audit completed on 2026-06-30 (Asia/Shanghai).

Primary materials used for the archived audit:

- a local PDF export of the Darktable development manual, inspected in the source workspace but not bundled with this portable skill;
- official HTML manual: <https://docs.darktable.org/usermanual/development/en/>;
- official 5.6.0 release notes: <https://www.darktable.org/2026/06/darktable-5.6.0-released/>.

## PDF coverage

- 384 pages.
- SHA-256: `aed4c76991b3f8d25483ad60974ec31fec6438b944217b46601a3c4376e43ceb`.
- 1,235,570 extracted characters and about 175,542 extracted words.
- Every page produced text; page 1 is the cover and page 384 is the short final page.
- The embedded outline contains 299 manual entries plus the table of contents.
- Key interface pages were visually inspected, including global layout, lighttable/darkroom layout, module headers, module groups, masks, AgX, color modules, AI preferences, neural restore, and AI runtime documentation.

## HTML coverage and comparison

- 300 English HTML URLs were enumerated from the official manual index, including the landing page and section indexes.
- All 300 pages were fetched successfully; no content URL remained in error.
- Extracted article/section text totals about 173,505 words.
- 249 in-article image references appear across 66 pages.
- No same-prefix content page linked by the manual was missing from the index.
- The 299 ordered HTML table-of-contents entries match the 299 PDF outline entries exactly after punctuation normalization; there are no order or title mismatches.
- Automated eight-word-window comparison produced a median page-level match of about 98.9% after per-page translation blocks were removed. Remaining mismatch is dominated by HTML-only section indexes, local page tables of contents, translations, PDF headers/footers, column layout, and line breaking. Manual inspection of lower-scoring editing pages did not reveal a different Darktable interface version.

The official documentation page explains that HTML, PDF, and EPUB are generated from the same `dtdocs` repository. The audited PDF and live HTML were therefore two renderings of substantially the same source, with HTML serving as the refreshable source. The PDF is audit evidence, not a runtime dependency of this skill.

## Current-version interpretation

Darktable 5.6.0 was released on 2026-06-21. Its release notes identify the optional AI subsystem, AI object masks, neural restore, color harmonizer, HEIF export, touchpad gestures, second-window pinning, condensed controls, 2-up scopes, and other 5.6 UI changes. These features are represented in the audited development manual.

The documentation versioning page states that after 4.6 only one current-development manual is maintained; version links after 4.6 redirect to it. Do not treat the development URL as a frozen 5.6 snapshot.

## Known documentation tensions

### Tone-mapper tutorial versus default

The introductory workflow still instructs readers to enable scene-referred filmic and teaches `filmic rgb`. The current Preferences > processing page lists `scene-referred (sigmoid)` as the default and offers `scene-referred (AgX)` and `scene-referred (filmic)` alternatives.

Rule: inspect the active tone mapper or the user's processing preference. Do not call filmic the current default.

### Lua installation pages versus 5.6 release notes

The development manual still contains a `lua scripts installer` utility page and older installation instructions. The 5.6.0 release notes state that Lua scripts are included in the release and `scripts_installer` was removed.

Rule: for Lua UI questions, verify the installed 5.6 build and current release notes before giving navigation instructions. This conflict does not affect ordinary photo editing.

### External raster mask wording

The module's technical information and 5.6 release notes support PFM/PNG, while one explanatory sentence still says `.pfm` only. The release notes also mention vectorizing the bitmap into a path mask.

Rule: state PFM/PNG for 5.6, then verify the control in the user's build if exact file support is critical.

## Refresh procedure

When accuracy depends on a changed interface:

1. Record the user's exact Darktable version, operating system, packaging source, and UI language.
2. Open the current official HTML page for the module or preference.
3. Check the installed version's official release notes for additions/removals.
4. Compare the user's screenshot with the current page.
5. Update this skill only after confirming a durable change; do not encode a one-off packaging bug as a general rule.
