# Industry Standards and Field Lessons

## CAD Standards

- **ISO 5455** — Technical drawings — Scales
- **ISO 128** — Technical drawings — General principles of presentation
- **BS 1192** — Collaborative production of architectural, engineering and construction information (UK)
- **AIA Layer Guidelines** — US architectural CAD layer naming
- **NCS (National CAD Standard)** — US national CAD standard for AEC

## EPC Document Control

- **ISO 9001:2015** — Quality management systems — Requirements
- **ISO 15926** — Industrial automation systems and integration
- **FIDIC** — International standard form of construction contracts

## Common Pitfalls

1. **Font substitution**: Client SHX fonts often differ from project standards. Always check `FONTALT` and `FONTMAP` before batch processing.
2. **Proxy objects**: Third-party objects (Civil 3D, Revit exports) explode or vanish in standard AutoCAD. Audit with `AUDIT` and `RECOVER`.
3. **Coordinate systems**: Never assume WGS84. Always request explicit CRS/EPSG from the surveyor.
4. **Scale consistency**: Client drawings may mix metric and imperial scales in the same project folder. Verify units with `UNITS` command.
5. **XREF recursion**: Nested external references can break when moved. Flatten or bind before standardization.
