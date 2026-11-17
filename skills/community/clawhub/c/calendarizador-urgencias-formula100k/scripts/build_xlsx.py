#!/usr/bin/env python3
"""
build_xlsx.py — Genera el Excel del calendario de urgencias a partir de un JSON
intermedio armado por la skill `calendarizador-urgencias-formula100k`.

Uso:
    python3 build_xlsx.py --json /tmp/urgencias-<slug>.json --out <out>.xlsx

Estructura del JSON: ver `references/anatomia-urgencia.md` §7.
"""

import argparse
import json
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter


THIN = Side(border_style="thin", color="CCCCCC")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)

HEADER_FILL = PatternFill("solid", fgColor="1F2937")
HEADER_FONT = Font(name="Calibri", size=12, bold=True, color="FFFFFF")

TITLE_FILL = PatternFill("solid", fgColor="F59E0B")
TITLE_FONT = Font(name="Calibri", size=14, bold=True, color="FFFFFF")

ALT_FILL = PatternFill("solid", fgColor="FFF7ED")
WHITE_FILL = PatternFill("solid", fgColor="FFFFFF")

WRAP = Alignment(wrap_text=True, vertical="top", horizontal="left")
CENTER = Alignment(wrap_text=True, vertical="center", horizontal="center")

TRIGGER_COLORS = {
    "urgencia táctica":      "FECACA",
    "escasez cruda":         "FED7AA",
    "prueba social":         "FDE68A",
    "exclusividad":          "DDD6FE",
    "aversión a la pérdida": "FBCFE8",
    "identidad":             "BFDBFE",
    "anticipación":          "BBF7D0",
    "consistencia":          "A7F3D0",
    "novedad":               "E0E7FF",
    "afecto":                "FBCFE8",
    "reconocimiento":        "FDE68A",
    "generosidad":           "FECACA",
    "fomo":                  "FECACA",
}


def color_for_trigger(text: str) -> str:
    if not text:
        return "F3F4F6"
    low = text.lower()
    for key, color in TRIGGER_COLORS.items():
        if key in low:
            return color
    return "F3F4F6"


def style_header(ws, row: int, last_col: int) -> None:
    for c in range(1, last_col + 1):
        cell = ws.cell(row=row, column=c)
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT
        cell.alignment = CENTER
        cell.border = BORDER


def style_title(ws, row: int, last_col: int, text: str) -> None:
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=last_col)
    cell = ws.cell(row=row, column=1, value=text)
    cell.fill = TITLE_FILL
    cell.font = TITLE_FONT
    cell.alignment = CENTER
    ws.row_dimensions[row].height = 28


def autosize(ws, widths: list) -> None:
    for i, w in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(i)].width = w


def fill_row(ws, row: int, values: list, fill: PatternFill, height: int = None) -> None:
    for j, v in enumerate(values, start=1):
        cell = ws.cell(row=row, column=j, value=v)
        cell.alignment = WRAP
        cell.border = BORDER
        cell.fill = fill
    if height:
        ws.row_dimensions[row].height = height


def build(data: dict, out_path: Path) -> None:
    producto = data.get("producto", {})
    nicho = data.get("nicho", {})
    nombre = producto.get("nombre", "Producto")

    wb = Workbook()

    # ───── Hoja 1: Resumen ─────────────────────────────────────────────
    ws = wb.active
    ws.title = "Resumen"

    style_title(ws, 1, 4, f"CALENDARIO DE RAZONES DE URGENCIA — {nombre.upper()}")
    ws.cell(
        row=2,
        column=1,
        value=(
            f"Calendario maestro de gatillos para {nombre} — eventos reales del año "
            f"+ activos propios del producto. Nicho: {nicho.get('rubro', '?')} · "
            f"Geo: {', '.join(nicho.get('geo', []) or ['?'])} · "
            f"Idioma: {nicho.get('idioma', '?')}."
        ),
    )
    ws.merge_cells("A2:D2")
    ws.cell(row=2, column=1).alignment = WRAP
    ws.row_dimensions[2].height = 50

    # Motor biológico
    ws.cell(row=4, column=1, value="MOTOR BIOLÓGICO").font = Font(bold=True, size=12, color="1F2937")
    ws.cell(
        row=5,
        column=1,
        value=(
            "La urgencia activa la amígdala (emoción) y secuestra al córtex prefrontal "
            "(razón). Libera dopamina del DESEO. El 68% de los consumidores ceden ante "
            "cronómetros visibles — no es manipulación, es neurobiología."
        ),
    )
    ws.merge_cells("A5:D5")
    ws.cell(row=5, column=1).alignment = WRAP
    ws.row_dimensions[5].height = 55

    # 5 gatillos
    ws.cell(row=7, column=1, value="LOS 5 GATILLOS DE DECISIÓN").font = Font(bold=True, size=12, color="1F2937")
    gatillos = [
        ("Gatillo", "Dimensión", "Qué hace", "Ejemplo"),
        ("Urgencia táctica", "Tiempo", "Impone deadline real para forzar decisión.", "Cohorte cierra el día X a las 23:59"),
        ("Escasez cruda", "Cantidad", "Limita el volumen disponible.", "Solo N plazas / cap operativo real"),
        ("Prueba social", "Social", "Valida con el comportamiento de la mayoría.", "127 emprendedoras ya entraron esta semana"),
        ("Exclusividad", "Contexto", "Restringe el acceso para generar estatus.", "App exclusiva solo dentro del producto"),
        ("Aversión a la pérdida", "Psicología", "Enfoca en lo que se PIERDE si no actúa.", "Sigues 6 meses más con la misma historia"),
    ]
    for i, row in enumerate(gatillos):
        for j, val in enumerate(row):
            c = ws.cell(row=8 + i, column=1 + j, value=val)
            c.alignment = WRAP
            c.border = BORDER
            if i == 0:
                c.fill = HEADER_FILL
                c.font = HEADER_FONT
                c.alignment = CENTER
            else:
                c.fill = PatternFill("solid", fgColor=color_for_trigger(row[0]))

    # Precios
    ws.cell(row=16, column=1, value="PRECIOS Y OFERTA").font = Font(bold=True, size=12, color="1F2937")
    ws.cell(row=17, column=1, value="Plan").fill = HEADER_FILL
    ws.cell(row=17, column=2, value="Precio").fill = HEADER_FILL
    ws.cell(row=17, column=3, value="Notas").fill = HEADER_FILL
    for c in (1, 2, 3):
        cell = ws.cell(row=17, column=c)
        cell.font = HEADER_FONT
        cell.alignment = CENTER
        cell.border = BORDER

    precios = producto.get("precios", [])
    for i, p in enumerate(precios):
        fill = ALT_FILL if i % 2 == 0 else WHITE_FILL
        fill_row(
            ws,
            18 + i,
            [p.get("plan", ""), p.get("precio", ""), p.get("notas", "")],
            fill,
            30,
        )

    autosize(ws, [32, 18, 50, 50])

    # ───── Hoja 2: Calendario mensual ──────────────────────────────────
    ws2 = wb.create_sheet("Calendario mensual")
    style_title(ws2, 1, 5, "CALENDARIO MENSUAL — 12 MESES")

    headers = ["Mes", "Eventos reales", "Gatillo dominante", "Razones de urgencia", "Mensaje tipo"]
    for j, h in enumerate(headers):
        ws2.cell(row=2, column=j + 1, value=h)
    style_header(ws2, 2, len(headers))

    meses = data.get("calendario_mensual", [])
    for i, m in enumerate(meses):
        razones_str = "\n".join(f"{n + 1}. {r}" for n, r in enumerate(m.get("razones", [])))
        eventos_str = "\n".join(f"• {e}" for e in m.get("eventos_reales", []))
        fill = PatternFill("solid", fgColor=color_for_trigger(m.get("gatillo_dominante", "")))
        fill_row(
            ws2,
            3 + i,
            [
                m.get("mes", ""),
                eventos_str,
                m.get("gatillo_dominante", ""),
                razones_str,
                m.get("mensaje_tipo", ""),
            ],
            fill,
            150,
        )

    autosize(ws2, [22, 32, 26, 60, 60])
    ws2.freeze_panes = "A3"

    # ───── Hoja 3: Pool semanal ────────────────────────────────────────
    ws3 = wb.create_sheet("Pool semanal")
    style_title(ws3, 1, 5, "POOL DE RAZONES SEMANALES (rotativas)")

    headers3 = ["Razón", "Activo del producto", "Gatillo", "Cuándo activar", "Copy modelo"]
    for j, h in enumerate(headers3):
        ws3.cell(row=2, column=j + 1, value=h)
    style_header(ws3, 2, len(headers3))

    pool = data.get("pool_semanal", [])
    for i, r in enumerate(pool):
        fill = PatternFill("solid", fgColor=color_for_trigger(r.get("gatillo", "")))
        fill_row(
            ws3,
            3 + i,
            [
                r.get("razon", ""),
                r.get("activo", ""),
                r.get("gatillo", ""),
                r.get("cuando", ""),
                r.get("copy", ""),
            ],
            fill,
            55,
        )

    autosize(ws3, [40, 28, 24, 30, 50])
    ws3.freeze_panes = "A3"

    # ───── Hoja 4: Activos reales ──────────────────────────────────────
    ws4 = wb.create_sheet("Activos reales")
    style_title(ws4, 1, 3, "ACTIVOS REALES DEL PRODUCTO QUE GENERAN URGENCIA HONESTA")

    ws4.cell(
        row=2,
        column=1,
        value=(
            "Toda urgencia debe apoyarse en al menos UNO de estos activos. "
            "Si no lo hace, la urgencia es falsa y quema marca."
        ),
    )
    ws4.merge_cells("A2:C2")
    ws4.cell(row=2, column=1).alignment = WRAP
    ws4.row_dimensions[2].height = 38

    headers4 = ["Activo", "Tipo de escasez", "Cuándo activarlo"]
    for j, h in enumerate(headers4):
        ws4.cell(row=3, column=j + 1, value=h)
    style_header(ws4, 3, len(headers4))

    activos = data.get("activos", [])
    for i, a in enumerate(activos):
        fill = ALT_FILL if i % 2 == 0 else WHITE_FILL
        fill_row(
            ws4,
            4 + i,
            [a.get("activo", ""), a.get("tipo_escasez", ""), a.get("cuando_activar", "")],
            fill,
            42,
        )

    autosize(ws4, [40, 32, 50])
    ws4.freeze_panes = "A4"

    # ───── Hoja 5: Reglas operativas ───────────────────────────────────
    ws5 = wb.create_sheet("Reglas operativas")
    style_title(ws5, 1, 3, "REGLAS PARA ACTIVAR URGENCIA (CHECKLIST)")

    headers5 = ["#", "Regla", "Por qué importa"]
    for j, h in enumerate(headers5):
        ws5.cell(row=2, column=j + 1, value=h)
    style_header(ws5, 2, len(headers5))

    reglas = data.get("reglas") or [
        (1, "Cronómetro visible en TODO", "El 68% cede ante el reloj. Sin reloj la urgencia es decorativa."),
        (2, "Cadencia día -7, -3, -1, -horas, -minutos", "La urgencia se construye en capas, no en el último día."),
        (3, "Una urgencia, un cierre", "Dos campañas paralelas se diluyen entre sí."),
        (4, "Verifica el 'después' antes de prometerlo", "Si dices que el precio sube, debe subir y quedarse arriba 30+ días."),
        (5, "Prueba social en cada deadline", "Número real, captura real. \"27 en las últimas 6 horas\"."),
        (6, "El día DESPUÉS del cierre, mostrar el cierre", "Refuerza credibilidad para la próxima campaña."),
        (7, "Nunca extender un cierre", "Una extensión = 6 meses sin credibilidad."),
    ]
    for i, r in enumerate(reglas):
        fill = ALT_FILL if i % 2 == 0 else WHITE_FILL
        if isinstance(r, (list, tuple)):
            vals = list(r)
        elif isinstance(r, dict):
            vals = [r.get("n", i + 1), r.get("regla", ""), r.get("por_que", "")]
        else:
            vals = [i + 1, str(r), ""]
        fill_row(ws5, 3 + i, vals, fill, 50)

    autosize(ws5, [5, 48, 60])
    ws5.freeze_panes = "A3"

    # ───── Hoja 6: Pendientes ──────────────────────────────────────────
    ws6 = wb.create_sheet("Pendientes")
    style_title(ws6, 1, 3, "PENDIENTES PARA VERIFICAR ANTES DE EJECUTAR")

    headers6 = ["Pendiente", "Por qué importa", "Estado"]
    for j, h in enumerate(headers6):
        ws6.cell(row=2, column=j + 1, value=h)
    style_header(ws6, 2, len(headers6))

    pendientes = data.get("pendientes", [])
    for i, p in enumerate(pendientes):
        fill = ALT_FILL if i % 2 == 0 else WHITE_FILL
        if isinstance(p, (list, tuple)):
            vals = list(p) + [""] * (3 - len(p))
        elif isinstance(p, dict):
            vals = [p.get("pendiente", ""), p.get("por_que", ""), p.get("estado", "☐ Pendiente")]
        else:
            vals = [str(p), "", "☐ Pendiente"]
        fill_row(ws6, 3 + i, vals[:3], fill, 42)

    autosize(ws6, [50, 60, 18])
    ws6.freeze_panes = "A3"

    # ───── Hoja 7: Fuentes Tavily (opcional) ───────────────────────────
    fuentes = data.get("fuentes_tavily") or []
    if fuentes:
        ws7 = wb.create_sheet("Fuentes Tavily")
        style_title(ws7, 1, 2, "FUENTES CONSULTADAS (TAVILY)")
        for j, h in enumerate(["Título", "URL"]):
            ws7.cell(row=2, column=j + 1, value=h)
        style_header(ws7, 2, 2)
        for i, f in enumerate(fuentes):
            fill = ALT_FILL if i % 2 == 0 else WHITE_FILL
            fill_row(ws7, 3 + i, [f.get("titulo", ""), f.get("url", "")], fill, 28)
        autosize(ws7, [50, 80])
        ws7.freeze_panes = "A3"

    out_path.parent.mkdir(parents=True, exist_ok=True)
    wb.save(out_path)
    print(f"Saved: {out_path}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", required=True, help="Path al JSON intermedio")
    ap.add_argument("--out", required=True, help="Path de salida .xlsx")
    args = ap.parse_args()

    with open(args.json, "r", encoding="utf-8") as f:
        data = json.load(f)

    build(data, Path(args.out))


if __name__ == "__main__":
    main()
