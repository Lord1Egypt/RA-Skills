#!/usr/bin/env python3
"""ClawSheet Wizard — data-kvalitetsrapport (unik feature)."""
import sys


def quality_report(path: str) -> str:
    try:
        import pandas as pd
    except ImportError:
        sys.exit("FEJL: pip install pandas")

    out = [f"📊 Data-kvalitetsrapport: {path}", ""]
    try:
        df = pd.read_excel(path, sheet_name=None)
    except Exception as e:
        return f"FEJL ved læsning: {e}"

    for sheet, data in df.items():
        out.append(f"## Ark: {sheet} ({data.shape[0]} rækker × {data.shape[1]} kolonner)")
        issues = 0

        # Duplikater
        dups = data.duplicated().sum()
        if dups:
            out.append(f"  ⚠️ {dups} duplikat-rækker")
            issues += dups

        # Tomme celler
        empties = int(data.isna().sum().sum())
        if empties:
            out.append(f"  ⚠️ {empties} tomme celler")

        # Tekst der ligner tal / blandede typer
        for col in data.columns:
            s = data[col]
            non_null = s.dropna()
            if len(non_null) == 0:
                continue
            # ID'er afkortet (>15 cifre som tal)
            if pd.api.types.is_numeric_dtype(s):
                big = (s.abs() > 10**14).sum()
                if big:
                    out.append(f"  ⚠️ Kolonne '{col}': {big} værdier > 15 cifre (Excel afkorter!)")
                    issues += big
            # Tekst-tal blandet
            else:
                numeric = pd.to_numeric(non_null, errors="coerce").notna().sum()
                total = len(non_null)
                if 0 < numeric < total:
                    out.append(f"  ⚠️ Kolonne '{col}': {numeric}/{total} er tal, resten tekst — blandet type")
                    issues += 1

        if issues == 0:
            out.append("  ✅ Ingen kvalitets-problemer fundet i dette ark.")
        out.append("")

    return "\n".join(out)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("BRUG: python3 data_quality.py fil.xlsx [--out rapport.md]")
    report = quality_report(sys.argv[1])
    if "--out" in sys.argv:
        p = sys.argv[sys.argv.index("--out") + 1]
        with open(p, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"✅ Rapport gemt: {p}")
    else:
        print(report)
