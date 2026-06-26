# Everything CLI Search Examples

Practical examples for using Everything CLI search in various scenarios.

## Basic Search Examples

### Simple File Search

```bash
# Search for a specific file
es.exe "filename.txt"

# Search with wildcards
es.exe "*.pdf"
es.exe "test_*.py"
es.exe "file?.txt"

# Search in specific directory
es.exe -p "C:\Users\Documents" "report"
```

### Multiple File Types

```bash
# Search for PDF or DOCX files
es.exe "*.pdf|*.docx"

# Search for multiple image formats
es.exe "*.jpg|*.png|*.gif|*.webp"

# Search for code files
es.exe "*.py|*.js|*.ts|*.java|*.cpp"
```

## Advanced Search Examples

### Size-Based Search

```bash
# Find files larger than 100MB
es.exe "size:>100mb"

# Find files smaller than 1KB
es.exe "size:<1kb"

# Find files between 10MB and 100MB
es.exe "size:10mb..100mb"

# Find tiny files (0-10KB)
es.exe "size:tiny"

# Find huge files (16-128MB)
es.exe "size:huge"

# Find gigantic files (>128MB)
es.exe "size:gigantic"

# Find empty files
es.exe "size:empty"

# Find large PDF files
es.exe "*.pdf size:>10mb"
```

### Date-Based Search

```bash
# Find files modified today
es.exe "datemodified:today"

# Find files modified yesterday
es.exe "datemodified:yesterday"

# Find files modified this week
es.exe "datemodified:thisweek"

# Find files modified last week
es.exe "datemodified:lastweek"

# Find files modified this month
es.exe "datemodified:thismonth"

# Find files modified last month
es.exe "datemodified:lastmonth"

# Find files modified this year
es.exe "datemodified:thisyear"

# Find files modified in 2024
es.exe "datemodified:2024"

# Find files created last 7 days
es.exe "datecreated:last7days"

# Find files accessed last 30 days
es.exe "dateaccessed:last30days"

# Find PDF files modified today
es.exe "*.pdf datemodified:today"
```

### Attribute-Based Search

```bash
# Find hidden files
es.exe "attrib:H"

# Find read-only files
es.exe "attrib:R"

# Find system files
es.exe "attrib:S"

# Find encrypted files
es.exe "attrib:E"

# Find hidden and read-only files
es.exe "attrib:HR"

# Find directories
es.exe "attrib:D"

# Find archive files
es.exe "attrib:A"

# Find compressed files
es.exe "attrib:C"

# Find hidden PDF files
es.exe "*.pdf attrib:H"
```

### Content Search

```bash
# Find files containing "TODO"
es.exe "content:\"TODO\""

# Find files containing "error" or "warning"
es.exe "content:\"error|warning\""

# Find files containing specific phrase
es.exe "content:\"hello world\""

# Find Python files containing "import"
es.exe "*.py content:\"import\""

# Find files with UTF-8 content
es.exe "content:\"test\" encoding:utf8"

# Find files with UTF-16 content
es.exe "content:\"test\" encoding:utf16"
```

### Image Search

```bash
# Find images with width 1920
es.exe "width:1920"

# Find images with height 1080
es.exe "height:1080"

# Find landscape images
es.exe "orientation:landscape"

# Find portrait images
es.exe "orientation:portrait"

# Find 4K images
es.exe "width:3840 height:2160"

# Find Full HD images
es.exe "width:1920 height:1080"

# Find images with specific dimensions
es.exe "dimensions:1920x1080"

# Find 24-bit images
es.exe "bitdepth:24"

# Find landscape JPEG images
es.exe "*.jpg orientation:landscape"
```

### Media Search

```bash
# Find files by album
es.exe "album:\"Dark Side of the Moon\""

# Find files by artist
es.exe "artist:\"Pink Floyd\""

# Find files by genre
es.exe "genre:Rock"

# Find files by title
es.exe "title:\"Comfortably Numb\""

# Find track 5
es.exe "track:5"

# Find files by comment
es.exe "comment:\"favorite\""

# Find rock music
es.exe "audio: genre:Rock"

# Find specific artist's songs
es.exe "artist:\"Queen\" audio:"
```

## Complex Query Examples

### Combined Operators

```bash
# PDF files containing "report" or "summary"
es.exe "*.pdf <report|summary>"

# Files containing "file1" and "file2" but not "temp"
es.exe "file1 file2 !temp"

# PDF or DOCX files containing "invoice"
es.exe "<*.pdf|*.docx> invoice"

# Images or videos modified today
es.exe "<pic:|video:> datemodified:today"

# Files with "test" but not "temp" or "backup"
es.exe "test !<temp|backup>"
```

### Combined Functions

```bash
# PDF files larger than 1MB modified today
es.exe "*.pdf size:>1mb datemodified:today"

# Python files modified last week
es.exe "*.py datemodified:lastweek"

# Hidden files in Documents
es.exe "attrib:H infolder:\"C:\Documents\""

# Large images modified this month
es.exe "pic: size:>5mb datemodified:thismonth"

# Recent error logs
es.exe "*.log content:\"error\" datemodified:last7days"

# Old temporary files
es.exe "*tmp* datemodified:lastyear"
```

### Combined Modifiers

```bash
# Case-sensitive whole filename search
es.exe "case:wfn:Test.txt"

# Whole word file-only search
es.exe "ww:file:test"

# Start with and end with
es.exe "startwith:test endwith:.pdf"

# Case-sensitive regex search
es.exe "case:regex:test.*\.py"

# Whole word in path
es.exe "ww:path:test"
```

### All Combined

```bash
# Complex query with operators, functions, and modifiers
es.exe "<*.pdf|*.docx> size:>1mb datemodified:lastweek case:wfn:report"

# Audio files modified today, sorted by date
es.exe "audio: datemodified:today"

# Images with specific dimensions and orientation
es.exe "pic: dimensions:1920x1080 orientation:landscape"

# Files containing "error" in content, modified last week
es.exe "content:\"error\" datemodified:lastweek"

# Large PDF files not containing "draft"
es.exe "*.pdf size:>10mb !content:\"draft\""
```

## Practical Use Cases

### Development Workflow

```bash
# Find all Python files in project
es.exe -p "F:\projects\myapp" "*.py"

# Find test files
es.exe "*test*.py"

# Find configuration files
es.exe "*.json|*.yaml|*.yml|*.toml|*.ini"

# Find files with "TODO" comments
es.exe "*.py content:\"TODO\""

# Find recently modified code files
es.exe "<*.py|*.js|*.ts> datemodified:today"

# Find large log files
es.exe "*.log size:>10mb"
```

### Document Management

```bash
# Find all PDF documents
es.exe "*.pdf"

# Find recent reports
es.exe "*report* datemodified:thismonth"

# Find large documents
es.exe "<*.pdf|*.docx|*.pptx> size:>5mb"

# Find documents by content
es.exe "<*.pdf|*.docx> content:\"contract\""

# Find old documents
es.exe "<*.pdf|*.docx> datemodified:lastyear"

# Find invoices
es.exe "*invoice* <*.pdf|*.docx>"
```

### Media Management

```bash
# Find all images
es.exe "pic:"

# Find 4K images
es.exe "width:3840 height:2160"

# Find landscape photos
es.exe "orientation:landscape"

# Find recent photos
es.exe "pic: datemodified:thismonth"

# Find large images
es.exe "pic: size:>5mb"

# Find screenshots
es.exe "*screenshot* <*.png|*.jpg>"

# Find all music files
es.exe "audio:"

# Find music by artist
es.exe "artist:\"Beatles\" audio:"

# Find rock music
es.exe "genre:Rock audio:"
```

### System Administration

```bash
# Find hidden files
es.exe "attrib:H"

# Find system files
es.exe "attrib:S"

# Find large files taking up space
es.exe "size:>100mb"

# Find empty folders
es.exe "empty:"

# Find duplicate files
es.exe "dupe:"

# Find temporary files
es.exe "*.tmp|*.temp"

# Find log files
es.exe "*.log"

# Find recently modified system files
es.exe "datemodified:today attrib:S"
```

### Backup and Cleanup

```bash
# Find old temporary files
es.exe "*tmp* datemodified:last30days"

# Find large files for cleanup
es.exe "size:>500mb"

# Find duplicate files
es.exe "dupe:"

# Find old downloads
es.exe -p "C:\Users\Downloads" "datemodified:last90days"

# Find old backups
es.exe "*backup* datemodified:lastyear"

# Find log files older than 7 days
es.exe "*.log datemodified:<last7days"
```

## OpenClaw-Skills Specific Examples

### Find Skill Files

```bash
# Find all SKILL.md files
es.exe -p "F:\openclaw-skills" "SKILL.md"

# Find all README.md files
es.exe -p "F:\openclaw-skills" "README.md"

# Find all Python scripts
es.exe -p "F:\openclaw-skills" "*.py"

# Find all PowerShell scripts
es.exe -p "F:\openclaw-skills" "*.ps1"

# Find all Bash scripts
es.exe -p "F:\openclaw-skills" "*.sh"
```

### Find Skills by Category

```bash
# Find browser-related skills
es.exe -p "F:\openclaw-skills\skills" -regex ".*browser.*"

# Find API-related skills
es.exe -p "F:\openclaw-skills\skills" -regex ".*api.*"

# Find database-related skills
es.exe -p "F:\openclaw-skills\skills" -regex ".*database.*"

# Find search-related skills
es.exe -p "F:\openclaw-skills\skills" -regex ".*search.*"
```

### Find Recent Changes

```bash
# Find skills modified today
es.exe -p "F:\openclaw-skills" "datemodified:today"

# Find skills modified this week
es.exe -p "F:\openclaw-skills" "datemodified:thisweek"

# Find recently modified Python scripts
es.exe -p "F:\openclaw-skills" "*.py datemodified:last7days"
```

## Command Line Options Examples

### Search Options

```bash
# Case-sensitive search
es.exe -case "Test"

# Regex search
es.exe -regex "test.*\.py"

# Whole word search
es.exe -wholeword "test"

# Path matching
es.exe -matchpath "test"

# Search in specific path
es.exe -p "C:\Users" "filename"

# Search in parent path only
es.exe -parent "C:\Users" "filename"
```

### Result Options

```bash
# Sort by size
es.exe -sort size "*.pdf"

# Sort by date modified
es.exe -sort "Date Modified"

# Sort descending
es.exe -sort size -sort-descending "*.pdf"

# Show details view
es.exe -details "*.pdf"

# Show thumbnails
es.exe -thumbnails "pic:"

# Set thumbnail size
es.exe -thumbnails -thumbnail-size 256 "pic:"

# Limit results
es.exe -limit 10 "*.pdf"
```

### Database Options

```bash
# Force database rebuild
es.exe -reindex

# Save database to disk
es.exe -update

# Read-only mode
es.exe -read-only "test"

# Rescan all folder indexes
es.exe -rescan-all

# Pause monitors
es.exe -monitor-pause

# Resume monitors
es.exe -monitor-resume
```

### Window Options

```bash
# Show new window
es.exe -newwindow "test"

# Maximize window
es.exe -maximized "test"

# Minimize window
es.exe -minimized "test"

# Fullscreen
es.exe -fullscreen "test"

# Always on top
es.exe -ontop "test"

# Close window
es.exe -close

# Toggle window
es.exe -toggle-window
```

### File List Options

```bash
# Create file list
es.exe -create-file-list "music.efu" "D:\Music"

# Include only specific files
es.exe -create-file-list "music.efu" "D:\Music" -create-file-list-include-only-files "*.mp3;*.flac"

# Exclude files
es.exe -create-file-list "music.efu" "D:\Music" -create-file-list-exclude-files "*.tmp;thumbs.db"

# Exclude folders
es.exe -create-file-list "music.efu" "D:\Music" -create-file-list-exclude-folders "temp;cache"

# Open file list
es.exe -f "music.efu"

# Edit file list
es.exe -edit "music.efu"
```

### ETP/FTP Options

```bash
# Connect to ETP server
es.exe -connect "username:password@hostname:port"

# Use drive links
es.exe -connect "hostname" -drive-links

# Use FTP links
es.exe -connect "hostname" -ftp-links
```

## Tips and Tricks

### Performance Tips

1. **Use specific paths**: Limit search to specific directories for faster results
   ```bash
   es.exe -p "C:\Users\Documents" "report"
   ```

2. **Use wildcards effectively**: Be specific with your patterns
   ```bash
   es.exe "report_2024_*.pdf"
   ```

3. **Combine filters**: Use multiple filters to narrow down results
   ```bash
   es.exe "*.pdf size:>1mb datemodified:today"
   ```

4. **Use sorting**: Sort results to find what you need faster
   ```bash
   es.exe -sort size -sort-descending "*.pdf"
   ```

5. **Limit results**: Use limit when you only need a few results
   ```bash
   es.exe -limit 10 "*.pdf"
   ```

### Search Tips

1. **Use quotes for spaces**: Always quote paths and queries with spaces
   ```bash
   es.exe -p "C:\Program Files" "filename"
   ```

2. **Use operators for complex queries**: Combine AND, OR, NOT operators
   ```bash
   es.exe "file1 file2|file3 !temp"
   ```

3. **Use grouping for complex logic**: Group expressions with < >
   ```bash
   es.exe "<*.pdf|*.docx> report"
   ```

4. **Use modifiers for precision**: Use case, wfn, ww modifiers
   ```bash
   es.exe "case:wfn:Test.txt"
   ```

5. **Use macros for quick filtering**: Use audio:, pic:, video: macros
   ```bash
   es.exe "audio: datemodified:today"
   ```

### Productivity Tips

1. **Create aliases**: Create aliases for common searches
   ```bash
   # In PowerShell
   function Find-PDF { es.exe "*.pdf $args" }
   Find-PDF "report"
   ```

2. **Use bookmarks**: Save frequently used searches as bookmarks
   ```bash
   es.exe -bookmark "mysearch"
   ```

3. **Use filters**: Create and use custom filters
   ```bash
   es.exe -filter "audio"
   ```

4. **Export results**: Export results for further processing
   ```bash
   es.exe -s "test" | Out-File results.txt
   ```

5. **Use hotkeys**: Set up hotkeys for quick access to Everything

## Troubleshooting Examples

### No Results Found

```bash
# Check if Everything service is running
# Rebuild database
es.exe -reindex

# Try simpler query
es.exe "test"

# Check path
es.exe -p "C:\Users" "test"
```

### Slow Performance

```bash
# Enable fast sorting
# In Everything: Tools → Options → Indexes → Check fast sort options

# Limit search scope
es.exe -p "C:\Users\Documents" "test"

# Use specific filters
es.exe "*.pdf size:>1mb"
```

### Permission Issues

```bash
# Run as administrator
es.exe -admin "test"

# Check file attributes
es.exe "attrib:H"
```

## Integration Examples

### With PowerShell

```powershell
# Find and process files
$files = es.exe "*.pdf" | ForEach-Object { $_.Trim() }
foreach ($file in $files) {
    Write-Host "Processing: $file"
}

# Find large files and report
$largeFiles = es.exe "size:>100mb"
Write-Host "Found $($largeFiles.Count) large files"

# Find and delete old temp files
$oldTemp = es.exe "*tmp* datemodified:last30days"
foreach ($file in $oldTemp) {
    Remove-Item $file -Force
}
```

### With Python

```python
import subprocess

# Find files
result = subprocess.run(['es.exe', '*.pdf'], capture_output=True, text=True)
files = result.stdout.strip().split('\n')

# Process files
for file in files:
    if file:
        print(f"Processing: {file}")
```

### With Batch

```batch
@echo off
REM Find PDF files
for /f "delims=" %%f in ('es.exe "*.pdf"') do (
    echo Processing: %%f
)
```

## See Also

- [SKILL.md](SKILL.md) - Comprehensive documentation
- [README.md](README.md) - Quick start guide
- [Everything Documentation](https://www.voidtools.com/support/everything/)
- [Everything Command Line Options](https://www.voidtools.com/support/everything/command_line_options)
