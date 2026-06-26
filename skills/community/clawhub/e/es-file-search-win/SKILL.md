# Windows File Search Skill

**Skill Description:** This skill provides powerful file search capabilities on Windows systems using the Everything command line tool (es.exe). It allows for fast and efficient searching of files and folders across the entire file system.

## Overview

This skill enables advanced file search operations on Windows platforms by leveraging the Everything search engine's command line interface. The es.exe tool offers lightning-fast file searching capabilities, making it ideal for locating files and folders based on various criteria.

## Error Handling

When executing commands, if an `Error 8` is returned, the skill will automatically retry the command with the `-instance=1.5a` parameter to ensure compatibility with Everything version 1.5a.

**If the error persists even after adding the `-instance=1.5a` parameter:**

This indicates that the `es.exe` command-line tool is not properly installed or configured on your system. Please follow these steps:

1. **Download and Install Everything:**
   - Visit the official Everything website: https://www.voidtools.com/downloads/
   - Download and install the latest version of Everything
   - Ensure that the "ES Command Line Tool" option is selected during installation
   
   **Direct Download Links:**
   
   **Everything 1.4.1 (Stable Version):**
   - Portable ZIP: https://www.voidtools.com/Everything-1.4.1.1032.x64.zip
   - Installer: https://www.voidtools.com/Everything-1.4.1.1032.x64-Setup.exe
   
   **Everything 1.5.0a (Alpha Version with es.exe included):**
   - Portable ZIP: https://www.voidtools.com/Everything-1.5.0.1404a.x64.zip
   - Installer: https://www.voidtools.com/Everything-1.5.0.1404a.x64-Setup.exe


2. **Configure System PATH (Choose one of the following methods):**
   
   **Method A - Add es.exe directory to System PATH:**
   - Locate the es.exe file (typically in `C:\Program Files\Everything\`)
   - Add this directory to your system's PATH environment variable
   - Restart your terminal/command prompt for changes to take effect
   
   **Method B - Copy es.exe to System Directory:**
   - Copy the es.exe file to your Windows system directory (`%systemroot%`)
   - This is typically `C:\Windows`

3. **Verify Installation:**
   - Open a new command prompt
   - Type `es -version` to verify the tool is accessible
   - Type `es -get-everything-version` or `es -instance=1.5a -get-everything-version` to verify Everything.exe is accessible
   - If successful, you should see the version information for the es command and Everything.exe

## Core Capabilities

### 1. Basic Search Syntax

```
es [options] search_term
```

### 2. Common Search Options

**File Filtering:**

- `-p`: Match full path (including folder names)
- `-w`: Match whole words only
- `-n <num>`: Limit number of results
- `-path <path>`: Search within specified path
- `/ad`: Show only directories
- `/a-d`: Show only files (exclude directories)

**Example:** `es -path "C:\Users" -n 10 *.pdf`

### 3. Sorting and Display

**Sorting Options:**

- `-s`: Sort by full path
- `-sort name`: Sort by file name (supports `size`, `extension`, `date-modified`, etc.)
- Use `-` prefix for descending order (e.g., `-sort -date-modified`)

**Formatted Output:**

```
es -name -size -date-modified -path search_term
```

### 4. Advanced Features

**Data Export:**

- `-csv`: Export results as CSV format
- `-export-csv "filename.csv"`: Export to specific CSV file
- `-no-header`: Exclude header row in export

**Folder Size Calculation:**

- `-get-folder-size <filename>`: Calculate folder size
- `-get-total-size`: Calculate total size of search results

**Search Term Highlighting:**

- `-highlight`: Highlight matching text in results
- `-highlight-color 0x0c`: Set highlight color

## Usage Examples

**Example 1: Find recently modified Word documents**

```
es -path "C:\" -sort -date-modified -n 5 -name -size -date-modified *.docx
```

**Example 2: Export hidden files list to CSV**

```
es -path "C:\" /ah -export-csv "hidden_files.csv" -no-header
```

## Notes

- **Platform:** Windows only
- **Tool:** Everything command line tool (es.exe)
- **Compatibility:** Works with Everything version 1.4.1.950 or higher
- **Wildcards:** Supports `*` (any characters) and `?` (single character)
- **Quoting:** Use double quotes for paths or search terms containing spaces