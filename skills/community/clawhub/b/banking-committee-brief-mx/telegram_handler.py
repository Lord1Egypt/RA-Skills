"""
telegram_handler.py
Integración con Telegram Bot API para banking-committee-brief-mx
Skill: banking-committee-brief-mx v1.0

Flujo:
  Usuario escribe en Telegram → bot recolecta indicadores + contexto
  → genera PDF → adjunta en el mismo chat

Instalación:
  pip install python-telegram-bot --break-system-packages
  export TELEGRAM_BOT_TOKEN=tu_token_aqui
  python3 telegram_handler.py
"""

import os
import logging
import re
from datetime import datetime
from telegram import Update, InputFile
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters,
)
from generate_brief import generar_brief_pdf

logging.basicConfig(
    format="%(asctime)s — %(name)s — %(levelname)s — %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Estados de conversación
ESPERANDO_INDICADORES, ESPERANDO_CONTEXTO, CONFIRMANDO = range(3)

# ─────────────────────────────────────────────
# PARSER DE INDICADORES
# Acepta formatos como:
#   ICAP: 11.2
#   IMOR = 3.4%
#   CCL 108.5
# ─────────────────────────────────────────────
def parsear_indicadores(texto: str) -> dict:
    claves_validas = {"ICAP", "TIER1", "IMOR", "CCL", "ROE", "ROA"}
    resultado = {}
    patron = re.compile(
        r'\b(ICAP|TIER1?|IMOR|CCL|ROE|ROA)\s*[=:\s]\s*([\d.,]+)\s*%?',
        re.IGNORECASE
    )
    for match in patron.finditer(texto):
        clave = match.group(1).upper().replace("TIER", "TIER1")
        valor = match.group(2).replace(",", ".")
        if clave in claves_validas:
            resultado[clave] = valor
    return resultado


# ─────────────────────────────────────────────
# HANDLERS
# ─────────────────────────────────────────────

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /brief — inicia el flujo."""
    await update.message.reply_text(
        "📋 *Brief de Comité de Riesgos — México*\n\n"
        "Voy a generar tu brief ejecutivo\\. Necesito dos insumos:\n\n"
        "1️⃣ *Indicadores CNBV* — Pega los datos del período\\.\n"
        "   Ejemplo: `ICAP: 11.2  IMOR: 3.4  CCL: 108.5  ROE: 10.3`\n\n"
        "Envía tus indicadores ahora 👇",
        parse_mode="MarkdownV2"
    )
    return ESPERANDO_INDICADORES


async def recibir_indicadores(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Recibe y parsea los indicadores CNBV."""
    texto = update.message.text
    indicadores = parsear_indicadores(texto)

    if not indicadores:
        await update.message.reply_text(
            "⚠️ No encontré indicadores reconocibles\\.\n\n"
            "Usa este formato:\n"
            "`ICAP: 11.2  IMOR: 3.4  CCL: 108.5  ROE: 10.3  ROA: 0.9`\n\n"
            "Los indicadores soportados son: ICAP, TIER1, IMOR, CCL, ROE, ROA",
            parse_mode="MarkdownV2"
        )
        return ESPERANDO_INDICADORES

    context.user_data["indicadores"] = indicadores
    claves_encontradas = ", ".join(indicadores.keys())

    await update.message.reply_text(
        f"✅ Indicadores recibidos: *{claves_encontradas}*\n\n"
        "2️⃣ Ahora pega el *contexto de mercado*\\:\n"
        "Titulares, notas Banxico, noticias del sector, tipo de cambio, etc\\.\n\n"
        "Si no tienes contexto, escribe: `sin contexto`",
        parse_mode="MarkdownV2"
    )
    return ESPERANDO_CONTEXTO


async def recibir_contexto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Recibe el contexto de mercado y genera el PDF."""
    texto = update.message.text
    contexto = "" if texto.lower().strip() in ["sin contexto", "no", "n/a", "-"] else texto

    context.user_data["contexto"] = contexto

    # Confirmación antes de generar
    n_ind = len(context.user_data.get("indicadores", {}))
    tiene_contexto = "Sí" if contexto else "No"

    await update.message.reply_text(
        f"⚙️ Generando brief\\.\\.\\.\n\n"
        f"Indicadores: *{n_ind}* cargados\n"
        f"Contexto de mercado: *{tiene_contexto}*\n\n"
        "Un momento\\.\\.\\.",
        parse_mode="MarkdownV2"
    )

    # Generar PDF
    try:
        periodo = datetime.now().strftime("%B %Y").capitalize()
        mes_slug = datetime.now().strftime("%Y%m")
        output_path = f"/tmp/Brief_Comite_Riesgos_{mes_slug}_{update.effective_user.id}.pdf"

        pdf_path = generar_brief_pdf(
            indicadores=context.user_data["indicadores"],
            contexto_mercado=contexto,
            periodo=periodo,
            output_path=output_path
        )

        # Enviar PDF como documento adjunto
        with open(pdf_path, "rb") as f:
            await update.message.reply_document(
                document=InputFile(f, filename=f"Brief_Comite_Riesgos_{mes_slug}.pdf"),
                caption=(
                    f"✅ *Brief listo — {periodo}*\n\n"
                    "El documento incluye:\n"
                    "• Resumen ejecutivo\n"
                    "• Dashboard de indicadores \\(CNBV\\)\n"
                    "• Señales de alerta regulatoria\n"
                    "• Contexto de mercado\n"
                    "• Agenda recomendada para el Comité\n\n"
                    "Para generar otro brief usa /brief"
                ),
                parse_mode="MarkdownV2"
            )

    except Exception as e:
        logger.error(f"Error generando PDF: {e}")
        await update.message.reply_text(
            f"❌ Error al generar el PDF: {str(e)}\n\n"
            "Intenta de nuevo con /brief"
        )

    context.user_data.clear()
    return ConversationHandler.END


async def cancelar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancela el flujo actual."""
    context.user_data.clear()
    await update.message.reply_text(
        "❌ Generación cancelada\\. Usa /brief para iniciar de nuevo\\.",
        parse_mode="MarkdownV2"
    )
    return ConversationHandler.END


async def ayuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /help."""
    await update.message.reply_text(
        "🏦 *Banking Committee Brief — México*\n\n"
        "*Comandos:*\n"
        "/brief — Iniciar generación de brief\n"
        "/cancelar — Cancelar operación actual\n"
        "/help — Esta ayuda\n\n"
        "*Indicadores soportados:*\n"
        "• ICAP — Índice de Capitalización\n"
        "• TIER1 — Capital Tier 1\n"
        "• IMOR — Índice de Morosidad\n"
        "• CCL — Coef\\. Cobertura de Liquidez\n"
        "• ROE — Retorno sobre Capital\n"
        "• ROA — Retorno sobre Activos\n\n"
        "*Skill:* banking\\-committee\\-brief\\-mx v1\\.0\n"
        "*Cobertura:* CNBV / Banco de México",
        parse_mode="MarkdownV2"
    )


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
def main():
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        raise ValueError(
            "❌ TELEGRAM_BOT_TOKEN no encontrado.\n"
            "Ejecuta: export TELEGRAM_BOT_TOKEN=tu_token_aqui"
        )

    app = ApplicationBuilder().token(token).build()

    # Flujo de conversación principal
    conv = ConversationHandler(
        entry_points=[CommandHandler("brief", start)],
        states={
            ESPERANDO_INDICADORES: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, recibir_indicadores)
            ],
            ESPERANDO_CONTEXTO: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, recibir_contexto)
            ],
        },
        fallbacks=[CommandHandler("cancelar", cancelar)],
        allow_reentry=True,
    )

    app.add_handler(conv)
    app.add_handler(CommandHandler("help", ayuda))
    app.add_handler(CommandHandler("start", ayuda))

    logger.info("🏦 Bot banking-committee-brief-mx activo. Esperando mensajes...")
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
