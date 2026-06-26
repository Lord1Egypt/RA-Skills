# Clean Filename

Removes invalid or unsafe characters from filenames and normalizes them for cross-platform use. Ideal for cleaning up messy file exports, downloads, or collaborative projects.

## Usage

```bash
# Clean a single file
clean_filename "report:final?.txt"

# Clean all files in a directory (non-recursive)
clean_filename ./downloads/

# Clean recursively
clean_filename ./project/ --recursive

# See changes without applying
clean_filename ./data/ --dry-run
```

## Price

$2.00
