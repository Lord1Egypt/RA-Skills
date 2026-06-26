# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.2.0] - 2026-03-01

### Added
- **Multi-source query**: Parallel search across AniList GraphQL + Jikan API + MediaWiki
- **Forced disambiguation**: Requires `--anime` hint for ambiguous names (prevents wrong character selection)
- **Semantic validation**: 9-check validation system (5 basic + 4 semantic checks)
- **Structured MERGE mode**: Multi-character SOUL.md generation with Character Selection Guide
- **Smart caching**: 24-hour SQLite cache with automatic retry logic
- **Interactive loading**: Three modes (REPLACE/MERGE/KEEP) for handling existing files
- **Confidence scoring**: Weighted scoring from multiple data sources (AniList 50% + Jikan 30% + Wiki 20%)
- **Backup system**: Automatic backup creation before file modifications

### Changed
- Refactored single-source query to multi-source architecture
- Improved error handling with graceful fallbacks between APIs
- Enhanced prompt engineering for more accurate character extraction

### Fixed
- Fixed ambiguous name resolution (e.g., "Sakura" now requires anime hint)
- Fixed validation false-positives with stricter semantic checks
- Fixed encoding issues with Japanese/Chinese character names

## [2.1.0] - 2026-02-28

### Added
- Basic AniList GraphQL integration
- Single character SOUL.md generation
- File existence detection with user prompts

## [2.0.0] - 2026-02-27

### Added
- Initial release with Jikan (MyAnimeList) API support
- Basic character data extraction
- Markdown SOUL format output

## Roadmap

### [2.3.0] - Planned
- [ ] Support for Chinese anime databases (Bilibili, Bangumi)
- [ ] Batch processing from character list file
- [ ] Web UI for non-technical users
- [ ] Export to other formats (JSON, YAML)

### [3.0.0] - Planned
- [ ] LLM-powered character synthesis from limited data
- [ ] Voice trait extraction from anime audio
- [ ] Relationship mapping between characters

---

[2.2.0]: https://github.com/colinchen4/anime-character-loader/releases/tag/v2.2.0
[2.1.0]: https://github.com/colinchen4/anime-character-loader/releases/tag/v2.1.0
[2.0.0]: https://github.com/colinchen4/anime-character-loader/releases/tag/v2.0.0
