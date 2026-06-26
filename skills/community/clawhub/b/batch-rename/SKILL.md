# Batch Rename

Batch rename images and corresponding annotation files with customizable patterns. Use when user needs to rename image datasets with sequential numbers, prefixes, or custom patterns.

## Features

- **Sequential Numbering**: Add sequential numbers to filenames
- **Custom Prefix/Suffix**: Add prefix or suffix to filenames
- **Annotation Aware**: Rename corresponding annotation files together
- **Handle Missing**: Gracefully handle images without annotation files
- **Preview Mode**: Preview changes before applying
- **Undo Support**: Restore original filenames

## Usage

```bash
# Rename with sequential numbers
python scripts/rename.py rename /path/to/images/ --pattern "img_{:04d}"

# Rename with prefix
python scripts/rename.py rename /path/to/images/ --prefix "dataset1_"

# Rename images and annotations together
python scripts/rename.py rename /path/to/images/ --pattern "img_{:04d}" --annotations /path/to/labels/

# Preview first
python scripts/rename.py rename /path/to/images/ --pattern "img_{:04d}" --preview
```

## Examples

```
$ python scripts/rename.py rename ./images --pattern "img_{:04d}" --annotations ./labels

Found 100 images
Preview (first 10):
  image1.jpg -> img_0001.jpg
  image2.jpg -> img_0002.jpg
  image3.jpg -> img_0003.jpg
  ...

Apply changes? (y/n): y
✓ Renamed 100 images
✓ Renamed 95 annotation files
```

## Pattern Options

- `{:04d}` - Sequential number with leading zeros
- `{date}` - Current date (YYYYMMDD)
- `{original}` - Original filename without extension

## Installation

No additional installation required.

## Options

- `--pattern`: Output filename pattern
- `--prefix`: Add prefix to filename
- `--suffix`: Add suffix to filename
- `--start`: Starting number for sequential renaming
- `--annotations`: Path to annotation files (will be renamed together)
- `--preview`: Preview changes without applying
- `--force`: Overwrite existing files
