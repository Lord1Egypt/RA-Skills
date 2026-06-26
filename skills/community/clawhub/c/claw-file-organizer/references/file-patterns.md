# File Type Patterns Reference

## Built-in Categories

### Images
- **JPG/JPEG** — Standard photo format
- **PNG** — Lossless compression, transparency support
- **GIF** — Animated or static graphics
- **SVG** — Scalable vector graphics
- **WEBP** — Modern web format
- **BMP** — Bitmap images
- **TIFF/TIF** — High-quality archival format
- **ICO** — Icons

### Documents
- **PDF** — Portable document format
- **DOC/DOCX** — Microsoft Word
- **TXT** — Plain text
- **RTF** — Rich text format
- **ODT** — OpenDocument text
- **PPT/PPTX** — Microsoft PowerPoint
- **XLS/XLSX** — Microsoft Excel
- **ODP** — OpenDocument presentation
- **ODG** — OpenDocument graphics
- **TEX/TEXX** — LaTeX source
- **EPUB** — E-book format

### Audio
- **MP3** — Standard compressed audio
- **WAV** — Uncompressed audio
- **FLAC** — Lossless compressed
- **OGG** — Ogg Vorbis
- **AAC** — Advanced Audio Coding
- **M4A** — Apple AAC
- **WMA** — Windows Media Audio
- **AIFF** — Apple Audio Interchange

### Video
- **MP4** — Standard video format
- **MKV** — Matroska (supports subtitles)
- **AVI** — Video for Windows
- **MOV** — QuickTime format
- **WEBM** — Web-oriented video
- **FLV** — Flash Video
- **WMV** — Windows Media Video
- **M4V** — Apple video format
- **3GP** — Mobile video format

### Archives
- **ZIP** — Standard archive
- **TAR** — Unix tape archive
- **GZ** — Gzip compressed
- **7Z** — 7-Zip format
- **RAR** — WinRAR archive
- **BZ2** — Bzip2 compressed
- **XZ** — Lempel-Ziv compressed
- **TGZ** — Gzip-compressed tar
- **ZST** — Zstandard archive

### Code
- **Python** — py
- **JavaScript** — js, jsx
- **TypeScript** — ts, tsx
- **HTML/CSS** — html, css, scss
- **Markdown** — md
- **Data** — json, yaml, yml
- **Shell** — sh, bash
- **Batch** — bat, ps1
- **Ruby** — rb
- **Go** — go
- **Rust** — rs
- **Java** — java
- **C/C++** — c, cpp, h
- **Swift** — swift
- **Kotlin** — kt
- **PHP** — php
- **SQL** — sql

### Data
- **CSV** — Comma-separated values
- **XML** — Extensible Markup Language
- **DB/SQLITE** — SQLite database
- **DAT** — Generic data file
- **LOG** — Log files

### Installers
- **Windows** — exe, msi
- **macOS** — dmg, app, pkg
- **Linux** — deb, rpm
- **Android** — apk
- **Disk** — iso, img

### Fonts
- **TTF** — TrueType Font
- **OTF** — OpenType Font
- **WOFF/WOFF2** — Web fonts
- **FON** — Windows font
- **EOT** — Embedded OpenType

## Custom Categories

Add custom mappings in config.yaml:

```yaml
custom_types:
  - name: "Design Assets"
    folders: "design/"
    extensions: [AI, PSD, SKETCH, FIG, INDD]
  - name: "Development Tools"
    folders: "dev-tools/"
    extensions: [VSCODE, SUBPROJECT]
```

## Naming Convention Options

| Pattern | Result |
|---------|--------|
| `{name}_{date}` | `report_2025-03-15.pdf` |
| `{name}` | `report.pdf` |
| `none` | `report.pdf` (no date, no change) |

## Safety Features

- Files larger than `max_file_size_mb` are skipped
- Exclude patterns prevent unwanted files from moving
- Undo log preserves every move for full rollback
- Dry-run mode previews without touching files
- Duplicate names get `_2`, `_3` suffixes
