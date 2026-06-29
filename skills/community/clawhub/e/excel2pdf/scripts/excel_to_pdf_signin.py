"""
Excel Sign-in Sheet → A4 PDF Converter (Generic)
================================================
Convert an Excel sign-in/roster sheet to a print-ready A4 PDF.

Usage:
    python excel_to_pdf_signin.py <excel_path> [options]

Options:
    --title TEXT          PDF title (default: auto-detect from Excel content)
    --sheet TEXT          Sheet name to process (default: active sheet)
    --orientation PORTRAIT|LANDSCAPE  (default: auto based on column count)
    --margin N            Page margin in mm (default: 8)
    --row-height N        Row top/bottom padding in pt (default: 6)
    --columns LIST        Column indices to include, 0-based, comma-separated
                          (default: auto — drops empty "sign number" columns)
    --col-widths LIST     Column width ratios (e.g. "0.1,0.2,0.15,0.2,0.2,0.15")
                          (default: equal distribution)
    --font PATH           Path to .ttf/.ttc Chinese font (default: auto-detect)
    --font-size N         Cell font size (default: 10)
    --out PATH            Output PDF path (default: same name as input, .pdf)

Examples:
    python excel_to_pdf_signin.py 签到表.xlsx
    python excel_to_pdf_signin.py roster.xlsx --title "Attendance Sheet" --margin 12
    python excel_to_pdf_signin.py sheet.xlsx --columns 0,1,2,3,7,8
    python excel_to_pdf_signin.py rooms.xlsx --orientation LANDSCAPE
    python excel_to_pdf_signin.py multi.xlsx --sheet "1号台"

Dependencies: openpyxl, reportlab
"""

import openpyxl
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os, sys, glob, argparse


# ── Chinese font auto-detection ──────────────────────────────────────────
def find_chinese_font():
    """Search system font directories for a suitable Chinese font."""
    candidates = []
    # Windows
    for root in [r'C:\Windows\Fonts', r'C:\WINNT\Fonts']:
        if os.path.isdir(root):
            for pattern in ['msyh.*', 'simhei.*', 'simkai.*', 'simsun.*', 'simfang.*']:
                candidates.extend(glob.glob(os.path.join(root, pattern)))
    # macOS
    for root in ['/System/Library/Fonts', '/Library/Fonts']:
        if os.path.isdir(root):
            for name in ['PingFang.ttc', 'STHeiti Light.ttc', 'STHeiti Medium.ttc', 'STKaiti.ttc']:
                path = os.path.join(root, name)
                if os.path.isfile(path):
                    candidates.append(path)
    # Linux
    for root in ['/usr/share/fonts', '/usr/local/share/fonts']:
        if os.path.isdir(root):
            for dn, _, files in os.walk(root):
                for fn in files:
                    lp = fn.lower()
                    if any(k in lp for k in ['noto', 'cjk', 'wqy', 'wenquan', 'droid']):
                        if lp.endswith(('.ttf', '.ttc', '.otf')):
                            candidates.append(os.path.join(dn, fn))
    return candidates[0] if candidates else None


# ── Auto-detect columns to keep ──────────────────────────────────────────
def auto_detect_columns(rows, header_index=0):
    """
    Return column indices to include, dropping columns where:
    - header cell is empty, AND
    - NO data row has a non-empty value in that column.
    Typical use case: skipping merged "签号" placeholder columns in sign-in sheets.
    """
    if not rows:
        return []
    ncols = max(len(r) for r in rows)
    keep = []
    for j in range(ncols):
        hdr = rows[header_index][j] if j < len(rows[header_index]) else None
        has_hdr = hdr is not None and str(hdr).strip() != ''
        has_data = any(
            j < len(r) and r[j] is not None and str(r[j]).strip() != ''
            for r in rows[header_index+1:]
        )
        if has_hdr or has_data:
            keep.append(j)
    return keep


# ── Column header labels ──────────────────────────────────────────────────
def get_col_labels(rows, keep_cols, header_index=0):
    """Derive header labels from row headers; keep original text."""
    labels = []
    for j in keep_cols:
        raw = str(rows[header_index][j]).strip() if j < len(rows[header_index]) and rows[header_index][j] else ''
        labels.append(raw if raw else f'Col{j}')
    return labels


# ── Main ──────────────────────────────────────────────────────────────────
def excel_to_pdf(excel_path, title=None, sheet_name=None, orientation=None, margin_mm=8,
                 row_padding=6, columns=None, col_width_ratios=None,
                 font_path=None, font_size=10, out_path=None):

    # 1. Read Excel
    wb = openpyxl.load_workbook(excel_path, data_only=True)
    ws = wb.active
    if sheet_name:
        ws = wb[sheet_name]
    all_rows = [list(row) for row in ws.iter_rows(values_only=True)]
    wb.close()

    # 2. Font
    if font_path is None:
        font_path = find_chinese_font()
    if font_path is None:
        raise RuntimeError('No Chinese font found. Specify --font PATH to a .ttf/.ttc file.')
    pdfmetrics.registerFont(TTFont('CN', font_path))

    # 3. Columns
    keep_cols = columns if columns is not None else auto_detect_columns(all_rows)
    headers = get_col_labels(all_rows, keep_cols)

    # 4. Filter: skip rows where all kept-column values are empty
    data_rows = [
        row for row in all_rows[1:]
        if any(
            j < len(row) and row[j] is not None and str(row[j]).strip()
            for j in keep_cols
        )
    ]

    # 5. Title
    if title is None:
        title = os.path.splitext(os.path.basename(excel_path))[0]

    ncols = len(keep_cols)

    # 6. Orientation
    if orientation is None:
        orientation = 'LANDSCAPE' if (ncols >= 7 or len(data_rows) > 35) else 'PORTRAIT'

    PAGE_W, PAGE_H = landscape(A4) if orientation.upper() == 'LANDSCAPE' else A4
    M = margin_mm * mm
    usable_w = PAGE_W - 2 * M

    # 6. Col widths
    if col_width_ratios:
        col_widths = [usable_w * r for r in col_width_ratios]
    else:
        col_widths = [usable_w / ncols] * ncols

    # 7. Output
    if out_path is None:
        out_path = excel_path.replace('.xlsx', '.pdf')
    doc = SimpleDocTemplate(out_path, pagesize=(PAGE_W, PAGE_H),
        leftMargin=M, rightMargin=M, topMargin=10*mm, bottomMargin=8*mm)

    # 8. Styles
    title_style = ParagraphStyle('T', fontName='CN', fontSize=font_size+6, leading=(font_size+6)*1.4,
                                  alignment=TA_CENTER, spaceAfter=5*mm)
    header_style = ParagraphStyle('H', fontName='CN', fontSize=font_size, leading=font_size*1.4,
                                   alignment=TA_CENTER, textColor=colors.white)
    cell_style = ParagraphStyle('C', fontName='CN', fontSize=font_size, leading=font_size*1.4,
                                 alignment=TA_CENTER)

    # 9. Build table
    elements = [Paragraph(title, title_style)]
    table_data = [[Paragraph(h, header_style) for h in headers]]

    for row in data_rows:
        vals = []
        for j in keep_cols:
            v = row[j] if j < len(row) and row[j] is not None else ''
            if isinstance(v, (int, float)):
                v = str(int(v))
            vals.append(Paragraph(str(v), cell_style))
        table_data.append(vals)

    t = Table(table_data, colWidths=col_widths, repeatRows=1)
    cmds = [
        ('FONTNAME', (0, 0), (-1, -1), 'CN'),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4472C4')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5*mm, colors.black),
        ('LINEBELOW', (0, 0), (-1, 0), 0.8*mm, colors.HexColor('#2F5496')),
        ('TOPPADDING', (0, 0), (-1, -1), row_padding),
        ('BOTTOMPADDING', (0, 0), (-1, -1), row_padding),
        ('LEFTPADDING', (0, 0), (-1, -1), max(2, row_padding // 2)),
        ('RIGHTPADDING', (0, 0), (-1, -1), max(2, row_padding // 2)),
    ]
    t.setStyle(TableStyle(cmds))
    elements.append(t)
    doc.build(elements)

    return out_path


def main():
    parser = argparse.ArgumentParser(description='Convert Excel sign-in sheet to A4 PDF')
    parser.add_argument('excel', help='Path to Excel (.xlsx) file')
    parser.add_argument('--title', help='PDF title (default: derive from filename)')
    parser.add_argument('--sheet', help='Sheet name to process (default: active sheet)')
    parser.add_argument('--orientation', choices=['PORTRAIT', 'LANDSCAPE'], help='Page orientation (default: auto)')
    parser.add_argument('--margin', type=int, default=8, help='Page margin in mm (default: 8)')
    parser.add_argument('--row-height', type=int, default=6, help='Row padding in pt (default: 6)')
    parser.add_argument('--columns', help='Column indices to include, comma-separated (default: auto-detect)')
    parser.add_argument('--col-widths', help='Column width ratios, comma-separated (default: equal)')
    parser.add_argument('--font', help='Path to Chinese font file')
    parser.add_argument('--font-size', type=int, default=10, help='Cell font size (default: 10)')
    parser.add_argument('--out', help='Output PDF path (default: same name, .pdf)')
    args = parser.parse_args()

    columns = None
    if args.columns:
        columns = [int(x.strip()) for x in args.columns.split(',')]

    col_width_ratios = None
    if args.col_widths:
        col_width_ratios = [float(x.strip()) for x in args.col_widths.split(',')]

    out = excel_to_pdf(
        excel_path=args.excel,
        title=args.title,
        sheet_name=args.sheet,
        orientation=args.orientation,
        margin_mm=args.margin,
        row_padding=args.row_height,
        columns=columns,
        col_width_ratios=col_width_ratios,
        font_path=args.font,
        font_size=args.font_size,
        out_path=args.out,
    )
    print(f'PDF created: {out}')


if __name__ == '__main__':
    main()
