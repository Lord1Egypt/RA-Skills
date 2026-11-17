#!/usr/bin/env python3
"""
Generador automático de la PROPUESTA INTEGRAL FINAL en .docx
para la skill creadora-comunidades-skool.

Toma un brief JSON (ver brief.schema.json) y produce un .docx con las
16 secciones aplicando las reglas de formato del memory
`feedback-docx-formato`:

  - Sin TOC
  - Texto justificado en todo el documento (incluido dentro de celdas)
  - Bordes solo en tablas reales (single, sz=6, color #4B5563)
  - Sin bullets decorativos ●/o/•  (solo listas numeradas 1, 2, 3)
  - Sin emojis decorativos en el cuerpo del .docx
  - Párrafos vacíos consecutivos colapsados

Uso:
    python3 build_docx.py brief.json [--out /ruta/salida.docx]

Si --out no se pasa, escribe a:
    entregables/<CLIENTE> - Propuesta Skool FINAL.docx

Dependencias: python-docx, emoji
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

import emoji
from docx import Document
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt, RGBColor, Cm, Inches

BORDER_COLOR = "4B5563"
BORDER_SIZE  = "6"   # 0.75pt
TEXT_FONT    = "Calibri"
HEAD_FONT    = "Calibri"


# ────────── helpers de XML / formato ──────────

def make_border(tag):
    el = OxmlElement(f"w:{tag}")
    el.set(qn("w:val"), "single")
    el.set(qn("w:sz"), BORDER_SIZE)
    el.set(qn("w:space"), "4")
    el.set(qn("w:color"), BORDER_COLOR)
    return el


def strip_emoji(text):
    if not text:
        return text
    cleaned = emoji.replace_emoji(text, replace="")
    cleaned = re.sub(r"[☀-➿⬀-⯿]", "", cleaned)
    cleaned = re.sub(r"  +", " ", cleaned).strip()
    return cleaned


def justify(paragraph):
    paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.JUSTIFY


def style_run(run, *, size=11, bold=False, color=None, font=TEXT_FONT):
    run.font.name = font
    run.font.size = Pt(size)
    run.bold = bold
    if color:
        run.font.color.rgb = RGBColor.from_string(color)


def add_paragraph(doc, text, *, size=11, bold=False, color=None,
                  align=WD_PARAGRAPH_ALIGNMENT.JUSTIFY, space_after=4):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_after = Pt(space_after)
    run = p.add_run(strip_emoji(text or ""))
    style_run(run, size=size, bold=bold, color=color)
    return p


def add_heading(doc, text, level=1):
    sizes = {1: 20, 2: 14, 3: 12}
    color = "1B2A41" if level == 1 else "111827"
    p = doc.add_paragraph()
    p.alignment = WD_PARAGRAPH_ALIGNMENT.LEFT
    p.paragraph_format.space_before = Pt(14 if level == 1 else 8)
    p.paragraph_format.space_after  = Pt(6)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(strip_emoji(text or ""))
    style_run(run, size=sizes.get(level, 11), bold=True, color=color, font=HEAD_FONT)
    return p


def add_table(doc, headers, rows, *, header_color="1B2A41", header_text_white=True):
    """Agrega una tabla con bordes single sz=6 color #4B5563 y texto justificado."""
    tbl = doc.add_table(rows=1, cols=len(headers))
    tbl.autofit = True

    # bordes a nivel tabla
    tblPr = tbl._element.find(qn("w:tblPr"))
    if tblPr is None:
        tblPr = OxmlElement("w:tblPr")
        tbl._element.insert(0, tblPr)
    for existing in tblPr.findall(qn("w:tblBorders")):
        tblPr.remove(existing)
    tblBorders = OxmlElement("w:tblBorders")
    for tag in ("top", "left", "bottom", "right", "insideH", "insideV"):
        tblBorders.append(make_border(tag))
    tblPr.append(tblBorders)

    # encabezados
    hdr_cells = tbl.rows[0].cells
    for i, h in enumerate(headers):
        cell = hdr_cells[i]
        cell.text = ""
        p = cell.paragraphs[0]
        p.alignment = WD_PARAGRAPH_ALIGNMENT.LEFT
        run = p.add_run(strip_emoji(str(h)))
        color = "FFFFFF" if header_text_white else "111827"
        style_run(run, size=10, bold=True, color=color)

        # sombreado del header
        tcPr = cell._element.get_or_add_tcPr()
        shd = OxmlElement("w:shd")
        shd.set(qn("w:val"), "clear")
        shd.set(qn("w:color"), "auto")
        shd.set(qn("w:fill"), header_color)
        tcPr.append(shd)

    # filas de datos
    for row in rows:
        cells = tbl.add_row().cells
        for i, val in enumerate(row):
            cell = cells[i]
            cell.text = ""
            for line in str(val).split("\n"):
                p = cell.paragraphs[0] if cell.paragraphs[0].text == "" else cell.add_paragraph()
                p.alignment = WD_PARAGRAPH_ALIGNMENT.JUSTIFY
                run = p.add_run(strip_emoji(line))
                style_run(run, size=10)

    # bordes por celda
    for row in tbl.rows:
        for cell in row.cells:
            tcPr = cell._element.get_or_add_tcPr()
            for existing in tcPr.findall(qn("w:tcBorders")):
                tcPr.remove(existing)
            tcBorders = OxmlElement("w:tcBorders")
            for tag in ("top", "left", "bottom", "right"):
                tcBorders.append(make_border(tag))
            tcPr.append(tcBorders)

    # respiro después de la tabla
    doc.add_paragraph()
    return tbl


def add_numbered_list(doc, items):
    for i, item in enumerate(items, 1):
        p = doc.add_paragraph()
        p.alignment = WD_PARAGRAPH_ALIGNMENT.JUSTIFY
        p.paragraph_format.left_indent = Cm(0.6)
        p.paragraph_format.space_after = Pt(2)
        run = p.add_run(f"{i}. {strip_emoji(item)}")
        style_run(run, size=11)


def add_blockquote_lines(doc, text):
    """Agrega un bloque tipo manifiesto: estrofas separadas por líneas en blanco."""
    for raw_line in text.split("\n"):
        p = doc.add_paragraph()
        line = strip_emoji(raw_line)
        if not line.strip():
            p.paragraph_format.space_after = Pt(4)
            continue
        p.alignment = WD_PARAGRAPH_ALIGNMENT.LEFT
        p.paragraph_format.left_indent = Cm(1)
        p.paragraph_format.space_after = Pt(2)
        run = p.add_run(line)
        style_run(run, size=11, color="1B2A41")
        run.italic = True


# ────────── secciones ──────────

def section_portada(doc, b):
    p = doc.add_paragraph()
    p.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    p.paragraph_format.space_before = Pt(80)
    run = p.add_run(strip_emoji(b["cliente"]).upper())
    style_run(run, size=36, bold=True, color="1B2A41", font=HEAD_FONT)

    if b.get("subtitle"):
        p = doc.add_paragraph()
        p.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
        run = p.add_run(strip_emoji(b["subtitle"]))
        style_run(run, size=14, color="374151")

    if b.get("tagline"):
        p = doc.add_paragraph()
        p.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
        p.paragraph_format.space_before = Pt(20)
        run = p.add_run(strip_emoji(b["tagline"]))
        style_run(run, size=12, color="6B7280")
        run.italic = True

    doc.add_page_break()


def section_1_resumen(doc, b):
    s = b.get("s1_resumen", {})
    add_heading(doc, "1. Resumen ejecutivo", level=1)

    if s.get("que_es"):
        add_heading(doc, f"¿Qué es {b['cliente']}?", level=3)
        add_paragraph(doc, s["que_es"])

    if s.get("por_que_ahora"):
        add_heading(doc, "¿Por qué ahora?", level=3)
        add_numbered_list(doc, s["por_que_ahora"])

    if s.get("tesis"):
        add_heading(doc, "La gran tesis estratégica", level=3)
        add_paragraph(doc, s["tesis"])


def section_2_brief(doc, b):
    s = b.get("s2_brief", {})
    add_heading(doc, "2. Brief consolidado del proyecto", level=1)

    if s.get("identidad_fundadora"):
        add_heading(doc, "Identidad de la fundadora", level=3)
        add_numbered_list(doc, s["identidad_fundadora"])

    if s.get("avatar_descripcion"):
        add_heading(doc, "Avatar", level=3)
        add_paragraph(doc, s["avatar_descripcion"])

    if s.get("como_se_ve_hoy"):
        add_heading(doc, "Cómo se ve hoy", level=3)
        add_numbered_list(doc, s["como_se_ve_hoy"])

    if s.get("dolores_verbatim"):
        add_heading(doc, "Dolores frecuentes (verbatim)", level=3)
        for d in s["dolores_verbatim"]:
            p = doc.add_paragraph()
            p.alignment = WD_PARAGRAPH_ALIGNMENT.JUSTIFY
            p.paragraph_format.left_indent = Cm(0.6)
            run = p.add_run(f'"{strip_emoji(d)}"')
            style_run(run, size=11, color="374151")
            run.italic = True

    if s.get("insight_estrategico"):
        add_heading(doc, "Insight estratégico", level=3)
        add_paragraph(doc, s["insight_estrategico"])


def section_3_benchmark(doc, b):
    s = b.get("s3_benchmark", {})
    add_heading(doc, "3. Análisis del mercado · Benchmark", level=1)

    if s.get("mapa_competitivo"):
        add_heading(doc, "Mapa competitivo", level=3)
        add_table(
            doc,
            ["Comunidad", "Plataforma", "Promesa principal", "Diferenciador", "Debilidad detectada"],
            [[r.get("comunidad", ""), r.get("plataforma", ""), r.get("promesa", ""),
              r.get("diferenciador", ""), r.get("debilidad", "")] for r in s["mapa_competitivo"]],
        )

    if s.get("lo_que_mercado_hace_mal"):
        add_heading(doc, "Lo que el mercado hace mal (la oportunidad)", level=3)
        add_paragraph(doc, s["lo_que_mercado_hace_mal"])

    if s.get("oportunidades"):
        add_heading(doc, "Oportunidades estratégicas detectadas", level=3)
        add_numbered_list(doc, s["oportunidades"])


def section_4_identidad(doc, b):
    s = b.get("s4_identidad", {})
    add_heading(doc, "4. Identidad de la comunidad · Narrativa profunda", level=1)

    if s.get("nombre_explicacion"):
        add_heading(doc, "Nombre", level=3)
        add_paragraph(doc, s["nombre_explicacion"])

    if s.get("manifiesto"):
        add_heading(doc, "Manifiesto fundacional", level=3)
        add_blockquote_lines(doc, s["manifiesto"])

    if s.get("mito_de_origen"):
        add_heading(doc, "Mito de origen", level=3)
        for para in s["mito_de_origen"].split("\n\n"):
            if para.strip():
                add_paragraph(doc, para)

    if s.get("contraste"):
        add_heading(doc, "El contraste · Cómo invertimos / construimos nosotras", level=3)
        add_table(
            doc,
            ["Ellos", "Nosotras"],
            [[r.get("ellos", ""), r.get("nosotras", "")] for r in s["contraste"]],
        )

    if s.get("identidad_miembros"):
        add_heading(doc, "Identidad de las miembros", level=3)
        add_paragraph(doc, s["identidad_miembros"])

    if s.get("valores"):
        add_heading(doc, "Valores fundacionales", level=3)
        add_numbered_list(doc, s["valores"])

    if s.get("frases_internas"):
        add_heading(doc, "Frases internas (cultura cotidiana)", level=3)
        for f in s["frases_internas"]:
            p = doc.add_paragraph()
            p.alignment = WD_PARAGRAPH_ALIGNMENT.JUSTIFY
            p.paragraph_format.left_indent = Cm(0.6)
            run = p.add_run(f'"{strip_emoji(f)}"')
            style_run(run, size=11)
            run.italic = True


def section_5_vehiculo(doc, b):
    s = b.get("s5_vehiculo", {})
    add_heading(doc, "5. Vehículo único · El Método", level=1)

    if s.get("nombre_metodo"):
        add_heading(doc, s["nombre_metodo"], level=2)
    if s.get("promesa_central"):
        add_paragraph(doc, s["promesa_central"])
    if s.get("tesis_fundacional"):
        add_heading(doc, "Tesis fundacional · Por qué SÍ podemos", level=3)
        add_paragraph(doc, s["tesis_fundacional"])

    if s.get("leyes"):
        add_heading(doc, "Las leyes · El filtro maestro", level=3)
        add_table(
            doc,
            ["Ley", "Pregunta filtro", "Qué activa", "Si la respuesta es NO →"],
            [[r.get("ley", ""), r.get("pregunta", ""), r.get("activa", ""), r.get("si_no", "")]
             for r in s["leyes"]],
        )

    if s.get("protocolo_decision"):
        add_heading(doc, "Protocolo de decisión", level=3)
        add_numbered_list(doc, s["protocolo_decision"])

    if s.get("reglas"):
        add_heading(doc, "Las reglas (la contranarrativa)", level=3)
        add_table(
            doc,
            ["Regla", "Explicación", "A qué se opone"],
            [[r.get("regla", ""), r.get("explicacion", ""), r.get("opone", "")] for r in s["reglas"]],
        )

    if s.get("fases_identidad"):
        add_heading(doc, "Las fases de identidad (el viaje interno)", level=3)
        add_table(
            doc,
            ["Fase", "Identidad", "Cómo se siente", "Qué necesita de la comunidad"],
            [[r.get("fase", ""), r.get("identidad", ""), r.get("como_se_siente", ""),
              r.get("necesita", "")] for r in s["fases_identidad"]],
        )


def section_5b_oferta(doc, b):
    s = b.get("s5b_oferta", {})
    add_heading(doc, "5B. Oferta concreta · Qué recibe quien entra", level=1)

    if s.get("transformacion"):
        add_heading(doc, "Estado A → Estado B", level=3)
        add_table(
            doc,
            ["Estado A · Antes", "Estado B · Después"],
            [[r.get("antes", ""), r.get("despues", "")] for r in s["transformacion"]],
        )

    if s.get("incluye"):
        add_heading(doc, "Qué incluye la membresía", level=3)
        add_table(
            doc,
            ["Componente", "Qué entrega"],
            [[r.get("componente", ""), r.get("entrega", "")] for r in s["incluye"]],
        )

    if s.get("valor_vs_precio"):
        add_heading(doc, "Valor percibido vs precio", level=3)
        rows = [[r.get("componente", ""), r.get("valor", "")] for r in s["valor_vs_precio"]]
        if s.get("valor_total"):
            rows.append(["VALOR TOTAL ANUAL EQUIVALENTE", s["valor_total"]])
        if s.get("precio"):
            rows.append(["PRECIO MEMBRESÍA", s["precio"]])
        add_table(doc, ["Componente", "Valor de mercado (USD)"], rows)

    if s.get("objeciones"):
        add_heading(doc, "Objeciones y respuestas", level=3)
        add_table(
            doc,
            ["Objeción", "Respuesta"],
            [[r.get("objecion", ""), r.get("respuesta", "")] for r in s["objeciones"]],
        )


def section_6_modulos(doc, b):
    mods = b.get("s6_modulos", [])
    if not mods:
        return
    add_heading(doc, "6. Estructura de módulos · Classroom", level=1)
    for m in mods:
        add_heading(doc, f"{m.get('codigo','')} — {m.get('titulo','')}", level=2)
        if m.get("objetivo"):
            add_paragraph(doc, f"Objetivo · {m['objetivo']}", bold=False)
        if m.get("temas"):
            add_heading(doc, "Temas", level=3)
            add_numbered_list(doc, m["temas"])
        if m.get("hook"):
            add_paragraph(doc, f"Por qué importa · {m['hook']}", bold=False)
        if m.get("resultado"):
            add_paragraph(doc, f"Resultado esperado · {m['resultado']}")
        if m.get("entregable"):
            add_paragraph(doc, f"Entregable de la miembro · {m['entregable']}")
        if m.get("estado"):
            add_paragraph(doc, f"Estado · {m['estado']}", bold=False)
        if m.get("titulos_alternativos"):
            add_heading(doc, "Opciones de título alternativas", level=3)
            add_numbered_list(doc, m["titulos_alternativos"])


def section_7_videos(doc, b):
    grupos = b.get("s7_videos", [])
    if not grupos:
        return
    add_heading(doc, "7. Detalle granular de los videos a grabar", level=1)
    add_paragraph(
        doc,
        "Convenciones · TH = Talking Head · SC = Screencast · MX = Mixto · MC = Masterclass.",
    )
    for g in grupos:
        title = f"{g.get('modulo','')} · {g.get('modulo_titulo','')}"
        if g.get("modulo_total"):
            title += f" ({g['modulo_total']})"
        add_heading(doc, title, level=2)
        add_table(
            doc,
            ["Código", "Título", "Duración", "Formato", "Ángulo / Hook", "Promesa concreta", "Estructura"],
            [[v.get("codigo", ""), v.get("titulo", ""), v.get("duracion", ""), v.get("formato", ""),
              v.get("hook", ""), v.get("promesa", ""), v.get("estructura", "")]
             for v in g.get("videos", [])],
        )


def section_8_dinamicas(doc, b):
    items = b.get("s8_dinamicas", [])
    if not items:
        return
    add_heading(doc, "8. Dinámicas únicas (accountability + experiencia)", level=1)
    add_table(
        doc,
        ["#", "Dinámica", "Qué es", "Cómo opera", "Gap del benchmark que cierra"],
        [[r.get("id", ""), r.get("dinamica", ""), r.get("que_es", ""), r.get("opera", ""), r.get("gap", "")]
         for r in items],
    )


def section_9_recursos(doc, b):
    items = b.get("s9_recursos", [])
    if not items:
        return
    add_heading(doc, "9. Tabla maestra · Recursos a desarrollar", level=1)
    add_table(
        doc,
        ["Tipo", "Cantidad", "Detalle", "Prioridad"],
        [[r.get("tipo", ""), r.get("cantidad", ""), r.get("detalle", ""), r.get("prioridad", "")]
         for r in items],
    )


def section_10_retos(doc, b):
    s = b.get("s10_retos", {})
    if not s:
        return
    add_heading(doc, "10. Retos por módulo", level=1)
    if s.get("onboarding"):
        add_heading(doc, "Retos de onboarding (primeros 7 días)", level=3)
        add_table(
            doc,
            ["#", "Reto", "Acción", "Resultado", "Recompensa"],
            [[r.get("n", ""), r.get("reto", ""), r.get("accion", ""), r.get("resultado", ""), r.get("recompensa", "")]
             for r in s["onboarding"]],
        )
    if s.get("por_modulo"):
        add_heading(doc, "Retos por módulo (quick win + reto principal)", level=3)
        add_table(
            doc,
            ["Módulo", "Tipo", "Reto", "Acción concreta", "Recompensa"],
            [[r.get("modulo", ""), r.get("tipo", ""), r.get("reto", ""), r.get("accion", ""), r.get("recompensa", "")]
             for r in s["por_modulo"]],
        )


def section_11_ritmo(doc, b):
    items = b.get("s11_ritmo", [])
    if not items:
        return
    add_heading(doc, "11. Ritmo semanal de la comunidad", level=1)
    add_table(
        doc,
        ["Día / Ritmo", "Contenido / Actividad", "Tipo"],
        [[r.get("dia", ""), r.get("actividad", ""), r.get("tipo", "")] for r in items],
    )


def section_12_foro(doc, b):
    items = b.get("s12_foro", [])
    if not items:
        return
    add_heading(doc, "12. Categorías del foro de Skool", level=1)
    add_table(
        doc,
        ["Categoría", "Propósito", "Quién publica", "Tipo de post esperado"],
        [[r.get("categoria", ""), r.get("proposito", ""), r.get("publica", ""), r.get("tipo_post", "")]
         for r in items],
    )


def section_13_complementos(doc, b):
    s = b.get("s13_complementos", {})
    if not s:
        return
    add_heading(doc, "13. Onboarding · Posts fijados · Leaderboard · VSL · Cancelación", level=1)

    if s.get("onboarding"):
        add_heading(doc, "Onboarding (6 bloques)", level=3)
        for para in s["onboarding"].split("\n\n"):
            if para.strip():
                add_paragraph(doc, para)

    if s.get("posts_fijados"):
        add_heading(doc, "Posts fijados (copy listo para pegar en Skool)", level=3)
        for i, post in enumerate(s["posts_fijados"], 1):
            add_heading(doc, f"Post {i}", level=3)
            # estos posts SÍ llevan emojis (van DENTRO de Skool); mantenerlos verbatim
            for line in post.split("\n"):
                p = doc.add_paragraph()
                p.alignment = WD_PARAGRAPH_ALIGNMENT.LEFT
                p.paragraph_format.left_indent = Cm(0.6)
                run = p.add_run(line)  # SIN strip_emoji — es copy para Skool
                style_run(run, size=11)

    if s.get("leaderboard"):
        add_heading(doc, "Leaderboard", level=3)
        add_table(
            doc,
            ["Nivel", "Nombre", "Criterio / Hito para subir"],
            [[r.get("nivel", ""), r.get("nombre", ""), r.get("criterio", "")] for r in s["leaderboard"]],
        )

    if s.get("vsl"):
        add_heading(doc, "Guion VSL (8 bloques)", level=3)
        for para in s["vsl"].split("\n\n"):
            if para.strip():
                add_paragraph(doc, para)

    if s.get("cancelacion"):
        add_heading(doc, "Guion del video de cancelación (6 bloques)", level=3)
        for para in s["cancelacion"].split("\n\n"):
            if para.strip():
                add_paragraph(doc, para)


def section_14_estetica(doc, b):
    s = b.get("s14_estetica", {})
    if not s:
        return
    add_heading(doc, "14. Estética visual y dirección de arte", level=1)

    if s.get("direccion_estrategica"):
        add_heading(doc, "Dirección estratégica", level=3)
        add_paragraph(doc, s["direccion_estrategica"])

    if s.get("paleta"):
        add_heading(doc, "Paleta de colores", level=3)
        add_table(
            doc,
            ["Rol", "Color", "Hex", "Significado"],
            [[r.get("rol", ""), r.get("color", ""), r.get("hex", ""), r.get("significado", "")]
             for r in s["paleta"]],
        )

    if s.get("tipografias"):
        add_heading(doc, "Tipografías", level=3)
        add_paragraph(doc, f"Títulos · {s['tipografias'].get('titulos','')}")
        add_paragraph(doc, f"Texto · {s['tipografias'].get('texto','')}")

    if s.get("si_usar") or s.get("no_usar"):
        add_heading(doc, "Estilo fotográfico", level=3)
        si = s.get("si_usar", [])
        no = s.get("no_usar", [])
        max_rows = max(len(si), len(no))
        rows = []
        for i in range(max_rows):
            rows.append([si[i] if i < len(si) else "", no[i] if i < len(no) else ""])
        add_table(doc, ["SÍ usar", "NO usar"], rows)

    if s.get("metafora_visual"):
        add_heading(doc, "Metáfora visual maestra", level=3)
        add_paragraph(doc, s["metafora_visual"])


def section_15_portadas(doc, b):
    s = b.get("s15_portadas", {})
    if not s:
        return
    add_heading(doc, "15. Propuestas de portada", level=1)
    if s.get("prompt_base"):
        add_heading(doc, "Prompt base (Nanobanana / Higgsfield / Midjourney)", level=3)
        p = doc.add_paragraph()
        p.alignment = WD_PARAGRAPH_ALIGNMENT.JUSTIFY
        p.paragraph_format.left_indent = Cm(0.6)
        run = p.add_run(f'"{s["prompt_base"]}"')
        style_run(run, size=10, color="374151")
        run.italic = True

    if s.get("specs"):
        add_heading(doc, "Specs técnicos", level=3)
        add_paragraph(doc, s["specs"])

    if s.get("portadas"):
        add_table(
            doc,
            ["Código", "Módulo", "Texto sobre portada", "Concepto visual"],
            [[r.get("codigo", ""), r.get("modulo", ""), r.get("texto", ""), r.get("concepto", "")]
             for r in s["portadas"]],
        )


def section_16_roadmap(doc, b):
    items = b.get("s16_roadmap", [])
    if not items:
        return
    add_heading(doc, "16. Roadmap de grabación", level=1)
    for m in items:
        title = f"{m.get('mes','')} · {m.get('tema','')}"
        add_heading(doc, title, level=2)
        if m.get("subtema"):
            add_paragraph(doc, m["subtema"])
        if m.get("bullets"):
            add_numbered_list(doc, m["bullets"])


# ────────── limpieza final ──────────

def cleanup_doc(doc):
    """Aplica las reglas finales:
       - quita w:pBdr y w:shd de párrafos sueltos (no de celdas de tabla),
       - colapsa párrafos vacíos consecutivos,
       - elimina headings vacíos.
    """
    body = doc.element.body
    body_only = list(body)

    # remove pBdr/shd en párrafos del body (NO toca los de tablas)
    for child in body_only:
        if child.tag != qn("w:p"):
            continue
        pPr = child.find(qn("w:pPr"))
        if pPr is None:
            continue
        for tag in ("w:pBdr", "w:shd"):
            for el in pPr.findall(qn(tag)):
                pPr.remove(el)

    # colapsa párrafos vacíos
    to_remove = []
    prev_empty = False
    for child in list(body):
        if child.tag == qn("w:p"):
            text = "".join(t.text or "" for t in child.iter(qn("w:t")))
            is_empty = not text.strip()
            if is_empty and prev_empty:
                to_remove.append(child)
            prev_empty = is_empty
        else:
            prev_empty = False
    for el in to_remove:
        body.remove(el)


# ────────── orquestador ──────────

def build(brief_path: Path, out_path: Path):
    with open(brief_path, "r", encoding="utf-8") as f:
        b = json.load(f)

    doc = Document()

    # margenes razonables
    for section in doc.sections:
        section.top_margin = Cm(2)
        section.bottom_margin = Cm(2)
        section.left_margin = Cm(2)
        section.right_margin = Cm(2)

    # default font
    style = doc.styles["Normal"]
    style.font.name = TEXT_FONT
    style.font.size = Pt(11)

    section_portada(doc, b)
    section_1_resumen(doc, b)
    section_2_brief(doc, b)
    section_3_benchmark(doc, b)
    section_4_identidad(doc, b)
    section_5_vehiculo(doc, b)
    section_5b_oferta(doc, b)
    section_6_modulos(doc, b)
    section_7_videos(doc, b)
    section_8_dinamicas(doc, b)
    section_9_recursos(doc, b)
    section_10_retos(doc, b)
    section_11_ritmo(doc, b)
    section_12_foro(doc, b)
    section_13_complementos(doc, b)
    section_14_estetica(doc, b)
    section_15_portadas(doc, b)
    section_16_roadmap(doc, b)

    cleanup_doc(doc)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(out_path))
    return out_path


def default_out(brief: dict) -> Path:
    home = Path.home()
    safe_cliente = re.sub(r"[/\\:]", "_", brief.get("cliente", "PROPUESTA").strip().upper())
    return home / "Downloads" / f"{safe_cliente} - Propuesta Skool FINAL.docx"


def main():
    parser = argparse.ArgumentParser(description="Genera la Propuesta Integral Final .docx")
    parser.add_argument("brief", help="Ruta al brief.json")
    parser.add_argument("--out", help="Ruta de salida del .docx", default=None)
    args = parser.parse_args()

    brief_path = Path(args.brief).expanduser().resolve()
    if not brief_path.exists():
        print(f"ERROR · no encuentro el brief en {brief_path}", file=sys.stderr)
        sys.exit(1)

    with open(brief_path, "r", encoding="utf-8") as f:
        brief = json.load(f)

    out_path = Path(args.out).expanduser().resolve() if args.out else default_out(brief)
    result = build(brief_path, out_path)
    print(f"OK · {result}")


if __name__ == "__main__":
    main()
