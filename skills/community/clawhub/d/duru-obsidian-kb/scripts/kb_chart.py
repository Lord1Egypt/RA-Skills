#!/usr/bin/env python3
import argparse
import json
from datetime import datetime
from pathlib import Path


def import_or_exit():
    try:
        import pandas as pd
        import matplotlib.pyplot as plt
        return pd, plt
    except Exception as exc:
        raise SystemExit(f"Missing deps for charting (pandas/matplotlib): {exc}")


def slugify(text: str) -> str:
    import re
    text = (text or '').strip().lower()
    text = re.sub(r'[^a-z0-9\u4e00-\u9fff]+', '-', text)
    text = re.sub(r'-+', '-', text).strip('-')
    return text[:80] or 'chart'


def resolve_data_path(root: Path, data: str) -> Path:
    p = Path(data).expanduser()
    if p.exists():
        return p.resolve()
    p2 = (root / data).resolve()
    if p2.exists():
        return p2
    raise SystemExit(f"Data file not found: {data}")


def pick_columns(df, x_col=None, y_col=None):
    cols = list(df.columns)
    if not cols:
        raise SystemExit("No columns found in data")

    if x_col and x_col not in cols:
        raise SystemExit(f"x-col not found: {x_col}")
    if y_col and y_col not in cols:
        raise SystemExit(f"y-col not found: {y_col}")

    if x_col is None:
        x_col = cols[0]

    if y_col is None:
        numeric_cols = [c for c in cols if c != x_col and str(df[c].dtype) not in ('object', 'bool')]
        if not numeric_cols:
            # fallback: try any different column
            numeric_cols = [c for c in cols if c != x_col]
        if not numeric_cols:
            raise SystemExit("Could not infer y column")
        y_col = numeric_cols[0]

    return x_col, y_col


from typing import Optional

def load_dataframe(path: Path, sheet: Optional[str]):
    pd, _ = import_or_exit()
    suffix = path.suffix.lower()
    if suffix in ('.csv', '.tsv'):
        sep = ',' if suffix == '.csv' else '\t'
        return pd.read_csv(path, sep=sep)
    if suffix in ('.xlsx', '.xlsm', '.xls'):
        if sheet:
            return pd.read_excel(path, sheet_name=sheet)
        return pd.read_excel(path)
    raise SystemExit(f"Unsupported file type: {suffix}")


def main():
    parser = argparse.ArgumentParser(description='Generate chart png+md from csv/xlsx into KB outputs')
    parser.add_argument('--root', required=True)
    parser.add_argument('--data', required=True, help='Data file path (absolute or relative to kb root)')
    parser.add_argument('--x-col', default=None)
    parser.add_argument('--y-col', default=None)
    parser.add_argument('--sheet', default=None)
    parser.add_argument('--kind', choices=['line', 'bar', 'scatter'], default='line')
    parser.add_argument('--title', default='')
    parser.add_argument('--file-back', action='store_true', help='Also append chart link to target concept memo')
    parser.add_argument('--target-concept', default=None, help='Concept slug/name under wiki/concepts (without .md)')
    args = parser.parse_args()

    pd, plt = import_or_exit()

    root = Path(args.root).expanduser().resolve()
    outputs = root / 'outputs'
    outputs.mkdir(parents=True, exist_ok=True)

    data_path = resolve_data_path(root, args.data)
    df = load_dataframe(data_path, args.sheet)
    if df.empty:
        raise SystemExit('Dataframe is empty')

    x_col, y_col = pick_columns(df, args.x_col, args.y_col)

    title = args.title.strip() or f"{y_col} by {x_col}"
    date_prefix = datetime.utcnow().strftime('%Y-%m-%d')
    slug = slugify(title)

    png_path = outputs / f"{date_prefix}-{slug}.png"
    md_path = outputs / f"{date_prefix}-{slug}.md"

    fig = plt.figure(figsize=(10, 5))
    ax = fig.add_subplot(111)

    x = df[x_col]
    y = pd.to_numeric(df[y_col], errors='coerce')
    plot_df = df.copy()
    plot_df[y_col] = y
    plot_df = plot_df.dropna(subset=[y_col])

    if plot_df.empty:
        raise SystemExit(f"No numeric values available in y column: {y_col}")

    if args.kind == 'line':
        ax.plot(plot_df[x_col], plot_df[y_col], marker='o')
    elif args.kind == 'bar':
        ax.bar(plot_df[x_col].astype(str), plot_df[y_col])
    else:
        ax.scatter(plot_df[x_col], plot_df[y_col])

    ax.set_title(title)
    ax.set_xlabel(x_col)
    ax.set_ylabel(y_col)
    ax.grid(True, alpha=0.25)
    fig.autofmt_xdate()
    fig.tight_layout()
    fig.savefig(png_path, dpi=150)
    plt.close(fig)

    rel_png = png_path.relative_to(root).as_posix()
    rel_data = data_path.relative_to(root).as_posix() if str(data_path).startswith(str(root)) else str(data_path)
    chart_ref = png_path.name

    md_lines = [
        f"# {title}",
        "",
        "## Chart",
        "",
        f"![{title}]({chart_ref})",
        "",
        "## Metadata",
        "",
        f"- kind: {args.kind}",
        f"- source_data: `{rel_data}`",
        f"- x_col: `{x_col}`",
        f"- y_col: `{y_col}`",
        f"- rows_used: {len(plot_df)}",
        "",
        "## Notes",
        "",
        "- Review outliers and missing values before filing into concept pages.",
        "",
    ]
    md_path.write_text('\n'.join(md_lines), encoding='utf-8')

    filed_back = None
    if args.file_back and args.target_concept:
        concept_path = root / 'wiki' / 'concepts' / f"{args.target_concept}.md"
        if concept_path.exists():
            append = f"\n\n## Chart artifact\n\n- [{title}](../../{rel_png})\n- Source note: [[../../{md_path.relative_to(root).as_posix()}|{md_path.name}]]\n"
            concept_path.write_text(concept_path.read_text(encoding='utf-8') + append, encoding='utf-8')
            filed_back = str(concept_path)

    print(json.dumps({
        'ok': True,
        'root': str(root),
        'data': str(data_path),
        'title': title,
        'kind': args.kind,
        'x_col': x_col,
        'y_col': y_col,
        'rows_used': int(len(plot_df)),
        'png': str(png_path),
        'note': str(md_path),
        'filed_back': filed_back,
    }, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
