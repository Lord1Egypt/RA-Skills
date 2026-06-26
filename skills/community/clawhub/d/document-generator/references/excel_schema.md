# Excel Spreadsheet Configuration Schema

Complete reference for Excel spreadsheet JSON configuration.

## Top-Level Structure

```json
{
  "template": "path/to/template.xlsx",  // Optional: use existing template
  "sheets": [ ... ]                      // Array of sheet configurations
}
```

## Sheet Configuration

```json
{
  "name": "Sheet1",
  "data": [ ... ],           // 2D array of cell values
  "formatting": { ... }      // Formatting options
}
```

## Data Array

The data array is a 2D array where each inner array represents a row:

```json
{
  "data": [
    ["Name", "Age", "Salary", "Bonus"],
    ["Alice", 30, 50000, "=C2*0.1"],
    ["Bob", 25, 45000, "=C3*0.1"],
    ["Total", "", "=SUM(C2:C3)", "=SUM(D2:D3)"]
  ]
}
```

Formulas are strings starting with `=`.

## Formatting Options

### Column Widths

```json
{
  "formatting": {
    "column_widths": [20, 10, 15, 15]  // Width for each column
  }
}
```

### Row Heights

```json
{
  "formatting": {
    "row_heights": [25, 20, 20, 20]  // Height for each row
  }
}
```

### Header Row

Automatically format the first row as a header:

```json
{
  "formatting": {
    "header_row": 0  // 0-indexed row number
  }
}
```

### Cell-Specific Formatting

```json
{
  "formatting": {
    "cell_formatting": {
      "0,0": {  // Row 0, Column 0 (0-indexed)
        "font": {
          "name": "Arial",
          "size": 12,
          "bold": true,
          "italic": false,
          "underline": false,
          "color": "#FFFFFF"
        },
        "background": "#4472C4",
        "alignment": {
          "horizontal": "center",  // left, center, right
          "vertical": "middle",    // top, middle, bottom
          "wrap_text": true
        },
        "border": {
          "style": "thin",  // thin, medium, thick
          "left": true,
          "right": true,
          "top": true,
          "bottom": true
        },
        "number_format": "#,##0.00"  // Excel number format
      },
      "A2": {  // Can also use Excel cell reference
        "font": {"bold": true},
        "number_format": "$#,##0.00"
      }
    }
  }
}
```

### Merged Cells

```json
{
  "formatting": {
    "merged_cells": [
      "A1:D1",  // Merge cells A1 through D1
      "A10:B10"
    ]
  }
}
```

### Freeze Panes

```json
{
  "formatting": {
    "freeze_panes": "B2"  // Freeze rows above and columns left of B2
  }
}
```

### Auto-Filter

```json
{
  "formatting": {
    "auto_filter": "A1:D10"  // Enable auto-filter for this range
  }
}
```

## Number Formats

Common Excel number formats:

- `"General"` - Default
- `"0"` - Integer
- `"0.00"` - Two decimal places
- `"#,##0"` - Integer with thousands separator
- `"#,##0.00"` - Two decimals with thousands separator
- `"$#,##0.00"` - Currency (USD)
- `"0%"` - Percentage
- `"0.00%"` - Percentage with decimals
- `"m/d/yyyy"` - Date
- `"h:mm AM/PM"` - Time
- `"@"` - Text

## Complete Example

```json
{
  "sheets": [
    {
      "name": "Sales Report",
      "data": [
        ["Product", "Q1", "Q2", "Q3", "Q4", "Total"],
        ["Widget A", 1000, 1200, 1500, 1800, "=SUM(B2:E2)"],
        ["Widget B", 800, 900, 1100, 1300, "=SUM(B3:E3)"],
        ["Widget C", 600, 700, 800, 900, "=SUM(B4:E4)"],
        ["Total", "=SUM(B2:B4)", "=SUM(C2:C4)", "=SUM(D2:D4)", "=SUM(E2:E4)", "=SUM(F2:F4)"]
      ],
      "formatting": {
        "column_widths": [15, 12, 12, 12, 12, 12],
        "header_row": 0,
        "cell_formatting": {
          "0,0": {
            "font": {"bold": true, "color": "#FFFFFF"},
            "background": "#4472C4",
            "alignment": {"horizontal": "center"}
          },
          "0,1": {
            "font": {"bold": true, "color": "#FFFFFF"},
            "background": "#4472C4",
            "alignment": {"horizontal": "center"}
          },
          "0,2": {
            "font": {"bold": true, "color": "#FFFFFF"},
            "background": "#4472C4",
            "alignment": {"horizontal": "center"}
          },
          "0,3": {
            "font": {"bold": true, "color": "#FFFFFF"},
            "background": "#4472C4",
            "alignment": {"horizontal": "center"}
          },
          "0,4": {
            "font": {"bold": true, "color": "#FFFFFF"},
            "background": "#4472C4",
            "alignment": {"horizontal": "center"}
          },
          "0,5": {
            "font": {"bold": true, "color": "#FFFFFF"},
            "background": "#4472C4",
            "alignment": {"horizontal": "center"}
          },
          "4,0": {
            "font": {"bold": true},
            "background": "#D9E1F2"
          }
        },
        "freeze_panes": "B2",
        "auto_filter": "A1:F5"
      }
    },
    {
      "name": "Summary",
      "data": [
        ["Metric", "Value"],
        ["Total Sales", "='Sales Report'!F5"],
        ["Average", "=B2/4"],
        ["Growth Rate", "=((E2-B2)/B2)"]
      ],
      "formatting": {
        "column_widths": [20, 15],
        "cell_formatting": {
          "0,0": {"font": {"bold": true}},
          "0,1": {"font": {"bold": true}},
          "1,1": {"number_format": "#,##0"},
          "2,1": {"number_format": "#,##0.00"},
          "3,1": {"number_format": "0.00%"}
        }
      }
    }
  ]
}
```

## Tips

1. **Formulas**: Always use Excel formula syntax with `=` prefix
2. **Cell References**: Can use either "A1" notation or "0,0" (row,col) notation
3. **Cross-Sheet References**: Use `'Sheet Name'!A1` syntax
4. **Data Types**: Numbers are numbers, text is text, formulas are strings starting with `=`
5. **Colors**: Use hex format like `#4472C4`
6. **Merged Cells**: Format the top-left cell of the merged range
