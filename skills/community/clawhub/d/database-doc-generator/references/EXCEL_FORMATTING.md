# Excel Formatting Guide

This document describes the Excel formatting applied by the Database Documentation Generator.

## Formatting Features

### 1. Merged Header Cell
- **Location**: Row 1, Columns A-E
- **Content**: `表: {table_name}`
- **Style**: Bold, size 14, centered
- **Purpose**: Clear table identification

### 2. Column Headers
- **Location**: Row 2
- **Columns**: 表名, 代码, 数据类型, 长度, 强制, 注释
- **Style**: Bold, size 12, centered, bordered
- **Purpose**: Clear column labels

### 3. Data Rows
- **Start**: Row 3
- **Style**: Size 10, vertically centered, bordered
- **Purpose**: Readable data presentation

### 4. Auto-Adjusted Column Widths
- **Method**: Calculates maximum content length per column
- **Padding**: +2 characters
- **Maximum**: 50 characters
- **Purpose**: Optimal readability without excessive width

### 5. Row Heights
- **Header Row (1)**: 30 points
- **Column Headers (2)**: 25 points
- **Data Rows**: Auto (default)

## Formatting Code

```python
from openpyxl.styles import Alignment, Font, Border, Side
from openpyxl.utils import get_column_letter

def apply_excel_formatting(writer, table_name, df):
    # Get workbook and worksheet
    workbook = writer.book
    worksheet = writer.sheets[table_name[:31]]
    
    # Define styles
    header_font = Font(bold=True, size=12)
    header_alignment = Alignment(horizontal='center', vertical='center')
    data_font = Font(size=10)
    data_alignment = Alignment(vertical='center')
    thin_border = Border(
        left=Side(style='thin'),
        right=Side(style='thin'),
        top=Side(style='thin'),
        bottom=Side(style='thin')
    )
    
    # Merge cells for table name
    worksheet.merge_cells(start_row=1, start_column=1, end_row=1, end_column=5)
    table_name_cell = worksheet.cell(row=1, column=1)
    table_name_cell.value = f"表: {table_name}"
    table_name_cell.font = Font(bold=True, size=14)
    table_name_cell.alignment = Alignment(horizontal='center', vertical='center')
    
    # Format column headers
    for col_num, column_title in enumerate(df.columns, 1):
        cell = worksheet.cell(row=2, column=col_num)
        cell.font = header_font
        cell.alignment = header_alignment
        cell.border = thin_border
    
    # Format data rows
    for row in range(3, worksheet.max_row + 1):
        for col in range(1, worksheet.max_column + 1):
            cell = worksheet.cell(row=row, column=col)
            cell.font = data_font
            cell.alignment = data_alignment
            cell.border = thin_border
    
    # Auto-adjust column widths
    for column in worksheet.columns:
        max_length = 0
        column_letter = get_column_letter(column[0].column)
        
        for cell in column[1:]:  # Skip merged header
            try:
                if cell.value:
                    cell_length = len(str(cell.value))
                    if cell_length > max_length:
                        max_length = cell_length
            except:
                pass
        
        adjusted_width = min(max_length + 2, 50)
        worksheet.column_dimensions[column_letter].width = adjusted_width
    
    # Set row heights
    worksheet.row_dimensions[1].height = 30
    worksheet.row_dimensions[2].height = 25
```

## Customization Options

### Change Font Sizes
```python
# Larger fonts
header_font = Font(bold=True, size=14)
data_font = Font(size=12)
table_name_font = Font(bold=True, size=16)

# Smaller fonts
header_font = Font(bold=True, size=10)
data_font = Font(size=9)
```

### Change Colors
```python
from openpyxl.styles import PatternFill

# Header background color
header_fill = PatternFill(start_color="FFCC99", end_color="FFCC99", fill_type="solid")
cell.fill = header_fill

# Alternate row colors
for row in range(3, worksheet.max_row + 1):
    if row % 2 == 1:  # Odd rows
        for col in range(1, worksheet.max_column + 1):
            cell = worksheet.cell(row=row, column=col)
            cell.fill = PatternFill(start_color="F0F0F0", end_color="F0F0F0", fill_type="solid")
```

### Change Border Styles
```python
# Thicker borders
thick_border = Border(
    left=Side(style='medium'),
    right=Side(style='medium'),
    top=Side(style='medium'),
    bottom=Side(style='medium')
)

# Dashed borders
dashed_border = Border(
    left=Side(style='dashed'),
    right=Side(style='dashed'),
    top=Side(style='dashed'),
    bottom=Side(style='dashed')
)
```

### Change Column Width Limits
```python
# Wider columns
adjusted_width = min(max_length + 5, 100)  # +5 padding, max 100

# Narrower columns
adjusted_width = min(max_length + 1, 30)  # +1 padding, max 30
```

## Output Examples

### Basic Format
```
表: users
┌─────────┬──────────┬────────────┬────────┬────────┬──────────┐
│ 表名    │ 代码     │ 数据类型   │ 长度   │ 强制   │ 注释     │
├─────────┼──────────┼────────────┼────────┼────────┼──────────┤
│ users   │ id       │ int8       │ 64     │ TRUE   │ 主键     │
│ users   │ username │ varchar    │ 2000   │ TRUE   │ 用户名   │
│ users   │ email    │ varchar    │ 2000   │ FALSE  │ 邮箱     │
└─────────┴──────────┴────────────┴────────┴────────┴──────────┘
```

### With Custom Formatting
- Colored headers
- Alternate row shading
- Different font styles
- Custom borders

## Security Considerations for Excel Output

### Data Sensitivity
- Database schema information may be sensitive
- Table and column names may reveal business logic
- Comments may contain proprietary information

### Output File Security
```python
# Secure output file handling
import os

# Set secure permissions (Unix-like systems)
output_path = "/secure/path/database_docs.xlsx"
os.chmod(output_path, 0o600)  # Owner read/write only

# Windows alternative: use secure directory with ACLs
output_dir = "C:\\Secure\\DatabaseDocs"
os.makedirs(output_dir, exist_ok=True)
```

### Information Redaction
```python
# Option to redact sensitive information
def redact_sensitive_info(df):
    """Redact sensitive column names or comments"""
    sensitive_patterns = ['EXAMPLE_PASSWORD', 'secret', 'token', 'key', 'credit']
    
    for pattern in sensitive_patterns:
        mask = df['代码'].str.contains(pattern, case=False, na=False)
        df.loc[mask, '代码'] = '[REDACTED]'
        df.loc[mask, '注释'] = '[REDACTED]'
    
    return df
```

## Best Practices

### Security Best Practices
1. **Secure Storage**: Store output files in secure directories
2. **Access Control**: Restrict file permissions to authorized users only
3. **Encryption**: Consider encrypting sensitive output files
4. **Audit Trail**: Log documentation generation events
5. **Cleanup**: Securely delete temporary and old files

### Technical Best Practices
1. **Consistency**: Use the same formatting across all worksheets
2. **Readability**: Ensure text is easily readable
3. **Printability**: Format should look good when printed
4. **Performance**: Avoid excessive formatting on large datasets
5. **Compatibility**: Use standard fonts for cross-platform compatibility

### Compliance Considerations
- **GDPR**: Ensure no personal data in schema documentation
- **HIPAA**: Additional protections for healthcare data
- **PCI DSS**: Special handling for payment card data environments

## Secure Usage Example

```python
from scripts.generate_database_doc import generate_database_documentation
import os

# Secure configuration from environment
db_config = {
    'host': os.environ['DB_HOST'],
    'port': int(os.environ.get('DB_PORT', 5432)),
    'database': os.environ['DB_NAME'],
    'user': os.environ['DB_USER'],
    'EXAMPLE_PASSWORD': os.environ['DB_PASSWORD']
}

# Secure output location
output_dir = os.environ.get('OUTPUT_DIR', '/secure/docs')
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, 'database_schema.xlsx')

# Generate with security considerations
result = generate_database_documentation(db_config, output_path=output_path)

if result:
    # Set secure permissions
    os.chmod(result, 0o600)
    print(f"✅ Secure documentation generated: {result}")
else:
    print("❌ Documentation generation failed")
```