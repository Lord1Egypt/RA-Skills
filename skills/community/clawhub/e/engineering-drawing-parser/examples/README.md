# Examples · 示例

`sample_drawing.txt` is a text-layer dump of a mechanical drawing's title block + BOM + dimensions, the format produced by `pdfplumber` or `ezdxf` for vector PDFs/DWGs.

```bash
python3 ../scripts/run_pipeline.py --input sample_drawing.txt --domain mechanical --standard GB
```

Expected: title block 6 fields, BOM 3 rows, dimensions list with H7/g6 fit and φ120±0.05.
