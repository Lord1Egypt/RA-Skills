"""
generate_brief.py
Motor de generación del PDF para Comité de Riesgos — México
Skill: banking-committee-brief-mx v1.0
"""

import os
import sys
import json
import re
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY


# ─────────────────────────────────────────────
# PALETA INSTITUCIONAL BANCARIA
# ─────────────────────────────────────────────
AZUL_INSTITUCIONAL  = colors.HexColor("#1B3A6B")  # Azul navy corporativo
AZUL_SECUNDARIO     = colors.HexColor("#2E5F9E")  # Azul medio secciones
GRIS_CABECERA       = colors.HexColor("#F2F4F7")  # Fondo tablas encabezado
GRIS_TEXTO          = colors.HexColor("#3D3D3D")  # Texto principal
VERDE_OK            = colors.HexColor("#1A7A4A")  # Semáforo verde
AMARILLO_ATENCION   = colors.HexColor("#B8860B")  # Semáforo amarillo
ROJO_ALERTA         = colors.HexColor("#B22222")  # Semáforo rojo
BLANCO              = colors.white


# ─────────────────────────────────────────────
# UMBRALES REGULATORIOS CNBV (Basilea III México)
# ─────────────────────────────────────────────
UMBRALES_CNBV = {
    "ICAP": {
        "nombre": "Índice de Capitalización",
        "minimo": 10.5,
        "atencion": 11.5,
        "unidad": "%",
        "ref": "CUB Art. 2 Bis 6"
    },
    "TIER1": {
        "nombre": "Capital Tier 1",
        "minimo": 8.5,
        "atencion": 10.0,
        "unidad": "%",
        "ref": "CUB Art. 2 Bis 7"
    },
    "IMOR": {
        "nombre": "Índice de Morosidad",
        "minimo": None,   # referencial sectorial
        "atencion": 2.5,
        "alerta": 4.0,
        "unidad": "%",
        "ref": "CNBV Boletín Estadístico",
        "invertido": True  # mayor = peor
    },
    "CCL": {
        "nombre": "Coeficiente de Cobertura de Liquidez",
        "minimo": 100.0,
        "atencion": 110.0,
        "unidad": "%",
        "ref": "CUB Art. 2 Bis 103"
    },
    "ROE": {
        "nombre": "Retorno sobre Capital (ROE)",
        "minimo": None,
        "atencion": 8.0,
        "alerta": 12.0,   # referencia sectorial positiva
        "unidad": "%",
        "ref": "CNBV Benchmarks Sectoriales",
        "invertido": False
    },
    "ROA": {
        "nombre": "Retorno sobre Activos (ROA)",
        "minimo": 0.5,
        "atencion": 1.0,
        "unidad": "%",
        "ref": "CNBV Benchmarks Sectoriales"
    },
}


def clasificar_semaforo(clave, valor_str):
    """Devuelve (emoji, color, etiqueta) según umbrales CNBV."""
    try:
        valor = float(str(valor_str).replace("%", "").replace(",", ".").strip())
    except (ValueError, TypeError):
        return ("⬜", colors.grey, "Sin dato")

    cfg = UMBRALES_CNBV.get(clave.upper(), {})
    if not cfg:
        return ("🔵", AZUL_SECUNDARIO, "Referencial")

    invertido = cfg.get("invertido", False)

    if invertido:
        # IMOR: mayor valor = mayor riesgo
        alerta = cfg.get("alerta", cfg.get("atencion", 999))
        atencion = cfg.get("atencion", 999)
        if valor >= alerta:
            return ("🔴", ROJO_ALERTA, "Alerta")
        elif valor >= atencion:
            return ("🟡", AMARILLO_ATENCION, "Atención")
        else:
            return ("🟢", VERDE_OK, "Adecuado")
    else:
        minimo = cfg.get("minimo") or 0
        atencion = cfg.get("atencion") or (minimo * 1.1 if minimo else 0)
        if minimo and valor < minimo:
            return ("🔴", ROJO_ALERTA, "Alerta")
        elif atencion and valor < atencion:
            return ("🟡", AMARILLO_ATENCION, "Atención")
        else:
            return ("🟢", VERDE_OK, "Adecuado")


def build_styles():
    """Construye estilos tipográficos institucionales."""
    base = getSampleStyleSheet()

    estilos = {
        "titulo_doc": ParagraphStyle(
            "titulo_doc",
            fontName="Helvetica-Bold",
            fontSize=16,
            textColor=AZUL_INSTITUCIONAL,
            alignment=TA_CENTER,
            spaceAfter=4,
        ),
        "subtitulo_doc": ParagraphStyle(
            "subtitulo_doc",
            fontName="Helvetica",
            fontSize=10,
            textColor=GRIS_TEXTO,
            alignment=TA_CENTER,
            spaceAfter=2,
        ),
        "confidencial": ParagraphStyle(
            "confidencial",
            fontName="Helvetica-Bold",
            fontSize=8,
            textColor=ROJO_ALERTA,
            alignment=TA_CENTER,
            spaceAfter=12,
        ),
        "seccion": ParagraphStyle(
            "seccion",
            fontName="Helvetica-Bold",
            fontSize=11,
            textColor=BLANCO,
            alignment=TA_LEFT,
            spaceAfter=6,
            spaceBefore=14,
        ),
        "cuerpo": ParagraphStyle(
            "cuerpo",
            fontName="Helvetica",
            fontSize=9,
            textColor=GRIS_TEXTO,
            alignment=TA_JUSTIFY,
            spaceAfter=6,
            leading=13,
        ),
        "bullet": ParagraphStyle(
            "bullet",
            fontName="Helvetica",
            fontSize=9,
            textColor=GRIS_TEXTO,
            leftIndent=14,
            spaceAfter=3,
            leading=12,
        ),
        "tabla_header": ParagraphStyle(
            "tabla_header",
            fontName="Helvetica-Bold",
            fontSize=8,
            textColor=BLANCO,
            alignment=TA_CENTER,
        ),
        "tabla_celda": ParagraphStyle(
            "tabla_celda",
            fontName="Helvetica",
            fontSize=8,
            textColor=GRIS_TEXTO,
            alignment=TA_LEFT,
        ),
        "tabla_celda_c": ParagraphStyle(
            "tabla_celda_c",
            fontName="Helvetica",
            fontSize=8,
            textColor=GRIS_TEXTO,
            alignment=TA_CENTER,
        ),
        "nota_pie": ParagraphStyle(
            "nota_pie",
            fontName="Helvetica-Oblique",
            fontSize=7,
            textColor=colors.HexColor("#888888"),
            alignment=TA_LEFT,
            spaceAfter=3,
        ),
    }
    return estilos


def seccion_header(titulo, s):
    """Devuelve un bloque de encabezado de sección con fondo azul."""
    tabla = Table(
        [[Paragraph(f"  {titulo}", s["seccion"])]],
        colWidths=[7.0 * inch],
    )
    tabla.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), AZUL_INSTITUCIONAL),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
    ]))
    return tabla


def construir_tabla_indicadores(indicadores_raw, s):
    """
    Recibe dict {clave: valor} y devuelve tabla ReportLab
    con semáforos y referencias normativas.
    """
    encabezado = [
        Paragraph("Indicador", s["tabla_header"]),
        Paragraph("Valor", s["tabla_header"]),
        Paragraph("Umbral CNBV", s["tabla_header"]),
        Paragraph("Estado", s["tabla_header"]),
        Paragraph("Referencia", s["tabla_header"]),
    ]
    filas = [encabezado]

    for clave, valor in indicadores_raw.items():
        cfg = UMBRALES_CNBV.get(clave.upper(), {})
        nombre = cfg.get("nombre", clave)
        umbral_str = f"≥ {cfg['minimo']}{cfg.get('unidad','')}" if cfg.get("minimo") else "Sectorial"
        ref = cfg.get("ref", "—")
        emoji, color_sem, etiqueta = clasificar_semaforo(clave, valor)

        fila = [
            Paragraph(nombre, s["tabla_celda"]),
            Paragraph(f"<b>{valor}{cfg.get('unidad','')}</b>", s["tabla_celda_c"]),
            Paragraph(umbral_str, s["tabla_celda_c"]),
            Paragraph(f"{emoji} {etiqueta}", s["tabla_celda_c"]),
            Paragraph(ref, s["tabla_celda"]),
        ]
        filas.append(fila)

    anchos = [2.2*inch, 0.9*inch, 1.1*inch, 0.9*inch, 1.9*inch]
    t = Table(filas, colWidths=anchos, repeatRows=1)
    t.setStyle(TableStyle([
        # Encabezado
        ("BACKGROUND", (0, 0), (-1, 0), AZUL_SECUNDARIO),
        ("TEXTCOLOR", (0, 0), (-1, 0), BLANCO),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 8),
        ("ALIGN", (0, 0), (-1, 0), "CENTER"),
        ("TOPPADDING", (0, 0), (-1, 0), 6),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 6),
        # Filas de datos
        ("FONTSIZE", (0, 1), (-1, -1), 8),
        ("TOPPADDING", (0, 1), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 1), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        # Alternado gris claro
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [BLANCO, GRIS_CABECERA]),
        # Borde general
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CCCCCC")),
        ("BOX", (0, 0), (-1, -1), 1, AZUL_SECUNDARIO),
    ]))
    return t


def inferir_resumen(indicadores, contexto):
    """
    Genera texto de resumen ejecutivo basado en los indicadores
    y el contexto de mercado. Lógica simple pero con conocimiento
    del dominio bancario mexicano.
    """
    alertas = []
    adecuados = []

    for clave, valor in indicadores.items():
        emoji, _, etiqueta = clasificar_semaforo(clave, valor)
        nombre = UMBRALES_CNBV.get(clave.upper(), {}).get("nombre", clave)
        if etiqueta == "Alerta":
            alertas.append(nombre)
        elif etiqueta == "Adecuado":
            adecuados.append(nombre)

    parrafos = []

    # Estado general
    if not alertas:
        estado = (
            "El perfil de riesgo de la institución se mantiene dentro de los parámetros "
            "regulatorios establecidos por la Comisión Nacional Bancaria y de Valores (CNBV). "
            "Los indicadores clave presentan niveles adecuados, sin señales de deterioro "
            "estructural en el período analizado."
        )
    elif len(alertas) <= 2:
        alertas_str = " y ".join(alertas)
        estado = (
            f"El perfil de riesgo presenta áreas de atención que requieren seguimiento "
            f"por parte del Comité. Se identificaron señales de alerta en: {alertas_str}. "
            "El resto de los indicadores se mantiene dentro de los rangos regulatorios, "
            "aunque el Comité deberá valorar el impacto potencial sobre la posición "
            "competitiva y regulatoria de la institución."
        )
    else:
        estado = (
            "El período analizado refleja un deterioro en múltiples métricas clave del perfil "
            "de riesgo. Se identificaron señales de alerta en varios indicadores regulatorios. "
            "El Comité deberá adoptar una postura activa y deliberar sobre acciones correctivas "
            "concretas en esta sesión, priorizando el cumplimiento del marco normativo de la CNBV."
        )

    parrafos.append(estado)

    # Contexto externo si hay
    if contexto and len(contexto.strip()) > 20:
        parrafos.append(
            "En cuanto al entorno externo, el contexto de mercado reciente incorpora "
            "variables macroeconómicas y regulatorias que podrían incidir en la dinámica "
            "de riesgo de la institución. Los detalles se desarrollan en la Sección 4."
        )

    # Señal principal
    if alertas:
        parrafos.append(
            f"<b>Señal principal de atención:</b> {alertas[0]} requiere análisis "
            "específico en la agenda del Comité. Se sugiere que la dirección de Riesgos "
            "presente el plan de mitigación correspondiente en esta sesión."
        )

    return parrafos


def generar_brief_pdf(
    indicadores: dict,
    contexto_mercado: str,
    periodo: str = None,
    nombre_institucion: str = "Institución Bancaria",
    output_path: str = None
) -> str:
    """
    Función principal. Genera el PDF del brief de Comité de Riesgos.

    Args:
        indicadores: dict con clave -> valor, ej: {"ICAP": "12.3", "IMOR": "1.8"}
        contexto_mercado: string con noticias/titulares del período
        periodo: string del período, ej: "Marzo 2026"
        nombre_institucion: nombre del banco (opcional, default genérico)
        output_path: ruta de salida del PDF

    Returns:
        Ruta del PDF generado
    """
    if not periodo:
        periodo = datetime.now().strftime("%B %Y").capitalize()

    if not output_path:
        mes_slug = datetime.now().strftime("%Y%m")
        output_path = f"/tmp/Brief_Comite_Riesgos_{mes_slug}.pdf"

    s = build_styles()
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        topMargin=0.7*inch,
        bottomMargin=0.7*inch,
        leftMargin=0.75*inch,
        rightMargin=0.75*inch,
        title=f"Brief Comité de Riesgos — {periodo}",
        author="banking-committee-brief-mx",
        subject="Uso interno confidencial",
    )

    story = []

    # ─── ENCABEZADO ──────────────────────────────────────
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("BRIEF EJECUTIVO", s["titulo_doc"]))
    story.append(Paragraph("Comité de Riesgos", s["titulo_doc"]))
    story.append(Paragraph(f"{nombre_institucion}  ·  {periodo}", s["subtitulo_doc"]))
    story.append(Paragraph(
        f"Fecha de generación: {datetime.now().strftime('%d de %B de %Y')}   ·   "
        "Uso interno confidencial — no reproducir",
        s["confidencial"]
    ))
    story.append(HRFlowable(width="100%", thickness=2, color=AZUL_INSTITUCIONAL, spaceAfter=10))

    # ─── SECCIÓN 1: RESUMEN EJECUTIVO ────────────────────
    story.append(seccion_header("1.  Resumen Ejecutivo", s))
    story.append(Spacer(1, 6))

    parrafos_resumen = inferir_resumen(indicadores, contexto_mercado)
    for p in parrafos_resumen:
        story.append(Paragraph(p, s["cuerpo"]))
    story.append(Spacer(1, 8))

    # ─── SECCIÓN 2: DASHBOARD DE INDICADORES CNBV ────────
    story.append(seccion_header("2.  Dashboard de Indicadores Regulatorios (CNBV)", s))
    story.append(Spacer(1, 6))

    if indicadores:
        tabla_ind = construir_tabla_indicadores(indicadores, s)
        story.append(KeepTogether([tabla_ind]))
    else:
        story.append(Paragraph(
            "No se proporcionaron indicadores cuantitativos en este período.",
            s["cuerpo"]
        ))

    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "* Umbrales basados en Circular Única de Bancos (CUB) y marcos de Basilea III "
        "implementados por CNBV. Los semáforos son orientativos; no sustituyen el análisis "
        "formal de cumplimiento normativo.",
        s["nota_pie"]
    ))
    story.append(Spacer(1, 10))

    # ─── SECCIÓN 3: SEÑALES DE ALERTA REGULATORIA ────────
    story.append(seccion_header("3.  Señales de Alerta Regulatoria", s))
    story.append(Spacer(1, 6))

    alertas_detectadas = []
    atenciones_detectadas = []

    for clave, valor in indicadores.items():
        _, _, etiqueta = clasificar_semaforo(clave, valor)
        cfg = UMBRALES_CNBV.get(clave.upper(), {})
        nombre = cfg.get("nombre", clave)
        ref = cfg.get("ref", "")
        if etiqueta == "Alerta":
            alertas_detectadas.append((nombre, valor, ref))
        elif etiqueta == "Atención":
            atenciones_detectadas.append((nombre, valor, ref))

    if not alertas_detectadas and not atenciones_detectadas:
        story.append(Paragraph(
            "🟢  No se detectaron señales de alerta ni indicadores en zona de atención "
            "en el período analizado. Se recomienda mantener el monitoreo rutinario.",
            s["cuerpo"]
        ))
    else:
        if alertas_detectadas:
            story.append(Paragraph("<b>Alertas activas (requieren acción):</b>", s["cuerpo"]))
            for nombre, valor, ref in alertas_detectadas:
                story.append(Paragraph(
                    f"🔴  <b>{nombre}:</b> Valor reportado {valor} — "
                    f"por debajo del umbral mínimo regulatorio. Ref.: {ref}",
                    s["bullet"]
                ))
            story.append(Spacer(1, 4))

        if atenciones_detectadas:
            story.append(Paragraph("<b>Indicadores en zona de atención:</b>", s["cuerpo"]))
            for nombre, valor, ref in atenciones_detectadas:
                story.append(Paragraph(
                    f"🟡  <b>{nombre}:</b> Valor reportado {valor} — "
                    f"dentro de rango mínimo pero sin margen de maniobra. Ref.: {ref}",
                    s["bullet"]
                ))

    story.append(Spacer(1, 10))

    # ─── SECCIÓN 4: CONTEXTO DE MERCADO ──────────────────
    story.append(seccion_header("4.  Contexto de Mercado y Entorno Regulatorio", s))
    story.append(Spacer(1, 6))

    if contexto_mercado and len(contexto_mercado.strip()) > 10:
        # Dividir en bullets si hay saltos de línea o puntos
        lineas = [l.strip() for l in contexto_mercado.split("\n") if l.strip()]
        if len(lineas) == 1:
            # Párrafo único
            story.append(Paragraph(contexto_mercado.strip(), s["cuerpo"]))
        else:
            story.append(Paragraph(
                "A continuación se sintetizan los elementos de contexto reportados "
                "y su implicación para el perfil de riesgo institucional:",
                s["cuerpo"]
            ))
            for linea in lineas:
                story.append(Paragraph(f"▸  {linea}", s["bullet"]))
    else:
        story.append(Paragraph(
            "No se proporcionó contexto de mercado para este período. Se recomienda "
            "incorporar en próximos ciclos: tipo de cambio, tasa objetivo Banxico, "
            "outlook sector bancario CNBV y noticias regulatorias relevantes.",
            s["cuerpo"]
        ))

    story.append(Spacer(1, 10))

    # ─── SECCIÓN 5: AGENDA RECOMENDADA ───────────────────
    story.append(seccion_header("5.  Agenda Recomendada para el Comité", s))
    story.append(Spacer(1, 6))

    # Generar puntos de agenda dinámicamente según alertas
    agenda = []

    if alertas_detectadas:
        for nombre, _, _ in alertas_detectadas[:2]:
            agenda.append(("Acción", f"Plan de mitigación: {nombre}"))

    if atenciones_detectadas:
        for nombre, _, _ in atenciones_detectadas[:2]:
            agenda.append(("Seguimiento", f"Monitoreo reforzado: {nombre}"))

    # Puntos estándar del Comité de Riesgos
    agenda += [
        ("Informativo", "Evolución del apetito de riesgo vs. límites aprobados"),
        ("Informativo", "Actualización del mapa de riesgos institucional"),
        ("Seguimiento", "Estatus de observaciones del período anterior"),
    ]

    colores_tipo = {
        "Acción": ROJO_ALERTA,
        "Seguimiento": AMARILLO_ATENCION,
        "Informativo": AZUL_SECUNDARIO,
    }

    filas_agenda = [[
        Paragraph("Tipo", s["tabla_header"]),
        Paragraph("Punto de discusión", s["tabla_header"]),
    ]]
    for tipo, punto in agenda[:6]:
        filas_agenda.append([
            Paragraph(tipo, s["tabla_celda_c"]),
            Paragraph(punto, s["tabla_celda"]),
        ])

    t_agenda = Table(filas_agenda, colWidths=[1.1*inch, 5.9*inch], repeatRows=1)
    t_agenda.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), AZUL_SECUNDARIO),
        ("TEXTCOLOR", (0, 0), (-1, 0), BLANCO),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [BLANCO, GRIS_CABECERA]),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CCCCCC")),
        ("BOX", (0, 0), (-1, -1), 1, AZUL_SECUNDARIO),
    ]))
    story.append(KeepTogether([t_agenda]))
    story.append(Spacer(1, 14))

    # ─── PIE DE PÁGINA ────────────────────────────────────
    story.append(HRFlowable(width="100%", thickness=1, color=AZUL_INSTITUCIONAL, spaceAfter=6))
    story.append(Paragraph(
        f"Generado por: banking-committee-brief-mx v1.0  ·  "
        f"Cobertura regulatoria: CNBV / Banco de México  ·  "
        f"Este documento es confidencial y de uso exclusivo del Comité de Riesgos.",
        s["nota_pie"]
    ))

    doc.build(story)
    return output_path


# ─────────────────────────────────────────────
# CLI — uso directo para pruebas
# ─────────────────────────────────────────────
if __name__ == "__main__":
    # Datos de ejemplo para demostración
    indicadores_ejemplo = {
        "ICAP": "11.2",
        "TIER1": "9.1",
        "IMOR": "3.4",
        "CCL": "108.5",
        "ROE": "10.3",
        "ROA": "0.9",
    }

    contexto_ejemplo = """
Banxico mantuvo la tasa de referencia en 9.0% en su última reunión, con señales de posibles recortes en H2 2026.
La cartera de crédito al consumo del sistema bancario creció 8.2% interanual, por encima del promedio histórico.
CNBV publicó actualización a las disposiciones de reservas preventivas para crédito PYME (Circular 15/2026).
El tipo de cambio peso/dólar cerró el mes con volatilidad moderada, en torno a $17.40 MXN/USD.
Moody's reafirmó perspectiva estable para el sistema bancario mexicano en su revisión trimestral.
"""

    output = generar_brief_pdf(
        indicadores=indicadores_ejemplo,
        contexto_mercado=contexto_ejemplo,
        periodo="Marzo 2026",
        nombre_institucion="Banco Ejemplo, S.A.",
        output_path="/tmp/Brief_Comite_Riesgos_demo.pdf"
    )
    print(f"✅ PDF generado: {output}")
