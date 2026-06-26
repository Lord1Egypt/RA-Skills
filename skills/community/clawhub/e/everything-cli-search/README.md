# Everything CLI Search

Fast file and folder search on Windows using Everything's command line interface.

## Overview

This skill provides comprehensive documentation and scripts for using Everything's command line interface (es.exe) for fast file and folder searching on Windows.

Everything is a lightweight, high-performance search engine that:
- Indexes all files on your NTFS volumes in seconds
- Provides instant search results
- Uses minimal system resources
- Supports advanced search syntax with operators, wildcards, macros, and modifiers
- Offers real-time file system monitoring

## Features

- **Fast Search**: Instant results with advanced filtering
- **Command Line Interface**: Full es.exe command line support
- **Multiple Scripts**: Python, Bash, and PowerShell implementations
- **Advanced Syntax**: Operators, wildcards, macros, modifiers, and functions
- **Remote Access**: HTTP and ETP server support
- **File Lists**: Index offline media (CDs, DVDs, etc.)
- **Keyboard Shortcuts**: Comprehensive shortcut reference

## Installation

### 1. Install Everything

Download and install Everything from https://www.voidtools.com

### 2. Enable Everything Service

- Open Everything
- Go to **Tools** → **Options** → **General**
- Check **"Run as service"**
- Click **OK**
- Restart Everything

### 3. Verify Installation

Open Command Prompt or PowerShell and run:

```bash
es.exe "test"
```

If you see search results, Everything CLI is ready to use!

## Quick Start

### Basic Search

```bash
# Search for files
es.exe "filename"

# Search with wildcards
es.exe "*.pdf"

# Search in specific path
es.exe -p "C:\Users" "filename"

# Search for PDF files containing "report"
es.exe "*.pdf report"
```

### Advanced Search

```bash
# Search files larger than 1MB modified today
es.exe "*.pdf size:>1mb datemodified:today"

# Search for audio files
es.exe "audio:"

# Search for hidden files
es.exe "attrib:H"

# Search with regex
es.exe -regex "test.*\.py"
```

## Scripts

### Python Script

```bash
python3 everything_search.py "query"
```

### Bash Script

```bash
./es_search.sh "query"
```

### PowerShell Script

```bash
.\es_search.ps1 "query"
```

## Documentation

See [SKILL.md](SKILL.md) for comprehensive documentation including:

- **Command Line Options**: Complete reference for all es.exe options
- **Search Syntax**: Operators, wildcards, macros, modifiers
- **Advanced Functions**: Size, date, attribute, content, image, media search
- **Keyboard Shortcuts**: Full shortcut reference
- **Indexes**: Database and indexing configuration
- **File Lists**: Creating and using EFU files
- **HTTP Server**: Web-based remote access
- **ETP Server**: Network file sharing
- **Examples**: Complex query examples and use cases

## Common Use Cases

### Find files modified today

```bash
es.exe "datemodified:today"
```

### Find large files

```bash
es.exe "size:>100mb"
```

### Find duplicate files

```bash
es.exe "dupe:"
```

### Find files containing specific text

```bash
es.exe "content:\"TODO\""
```

### Find images with specific dimensions

```bash
es.exe "width:1920 height:1080"
```

## Tips

1. **Use quotes for paths with spaces**: `es.exe -p "C:\Program Files" "filename"`
2. **Combine operators**: `es.exe "file1 file2|file3"`
3. **Use wildcards**: `*.txt`, `test_*.py`, `file?.ext`
4. **Sort for better results**: Use `-sort` and `-sort-descending`
5. **Use regex for complex patterns**: `es.exe -regex "pattern.*"`
6. **Enable fast sorting**: Check fast sort options in Indexes
7. **Use file lists for offline media**: Create EFU files for CDs, DVDs
8. **Use HTTP server for remote access**: Access files from phone

## Limitations

- Only works on Windows
- Requires Everything to be installed and running
- Everything service must be enabled for real-time indexing
- Content search requires files to be indexed

## Troubleshooting

### "es.exe not found" Error

1. Download and install Everything from https://www.voidtools.com
2. Add Everything installation directory to your PATH
3. Restart your terminal

### No Results Found

1. Make sure Everything service is running
2. Check if the path is correct
3. Try rebuilding the database: `es.exe -reindex`

### Slow Search Performance

1. Make sure Everything service is enabled
2. Check if NTFS indexing is enabled
3. Enable fast sorting options

## See Also

- [Everything Documentation](https://www.voidtools.com/support/everything/)
- [Everything Download](https://www.voidtools.com/)
- [SKILL.md](SKILL.md) - Comprehensive documentation

## License

This skill is part of OpenClaw and follows the same license.
