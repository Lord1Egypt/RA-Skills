---
name: baby-photo-book
description: Generate professional baby photo books from photos with intelligent layout. Automatically organizes photos by baby's age stages, applies smart layouts to minimize whitespace, and outputs print-ready PDF. Use when user wants to create baby photo albums, generate photo books from baby pictures, or automatically layout photos for printing.
---

# Baby Photo Book Generator

Generate professional baby photo books with intelligent layout optimization.

## Features

- **Automatic Age Grouping**: Organizes photos by baby's growth stages (newborn, infant, toddler)
- **Smart Layout**: Minimizes whitespace while preserving photo aspect ratios
- **Multiple Layout Patterns**: Supports 1-4 photos per page with optimal arrangements
- **Print-Ready Output**: Generates A4 PDF suitable for professional printing

## Usage

### Basic Usage

```bash
python scripts/generate_photo_book.py <photo_folder> --name "Baby Name" --birth YYYY-MM-DD
```

### Parameters

- `photo_folder`: Path to folder containing baby photos
- `--name`: Baby's name for the cover
- `--birth`: Baby's birth date (YYYY-MM-DD format)
- `--output`: Output PDF filename (default: baby_photo_book.pdf)

### Example

```bash
python scripts/generate_photo_book.py ~/baby_photos --name "小明" --birth 2023-06-15
```

## Layout Algorithm

The skill uses an intelligent layout engine that:

1. **Analyzes photo aspect ratios** to determine optimal placement
2. **Calculates multiple layout options** for each page
3. **Selects the layout with minimum whitespace**
4. **Preserves photo proportions** without cropping

### Layout Patterns

| Photos | Layout Strategy |
|--------|-----------------|
| 1 | Full page, maximized to fill available space |
| 2 | Side-by-side or stacked, whichever minimizes whitespace |
| 3 | Left-1-Right-2 or Top-1-Bottom-2 based on photo orientations |
| 4 | 2×2 adaptive grid with aspect-ratio-aware cell sizing |

## Age Stages

Photos are automatically grouped by baby's age:

- **Newborn** (0-1 month)
- **Early Infant** (1-3 months)
- **Mid Infant** (3-6 months)
- **Late Infant** (6-9 months)
- **Crawling** (9-12 months)
- **Early Toddler** (1-1.5 years)
- **Mid Toddler** (1.5-2 years)
- **Late Toddler** (2-3 years)

## Dependencies

- Python 3.8+
- Pillow (image processing)
- ReportLab (PDF generation)

Install dependencies:
```bash
pip install Pillow reportlab
```

## Output

Generates a PDF with:
- Cover page with baby name
- Chapter pages for each age stage
- Photo pages with intelligent layouts
- Date and age annotations on each photo