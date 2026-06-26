# audio-analyze-skill-for-openclaw

Transcribe y analiza contenido de audio/video con alta precisión. [Impulsado por Evolink.ai](https://evolink.ai/?utm_source=github&utm_medium=skill&utm_campaign=audio-analyze)

🌐 English | [日本語](README.ja.md) | [简体中文](README.zh-CN.md) | [한국어](README.ko.md) | [Español](README.es.md) | [Français](README.fr.md) | [Deutsch](README.de.md) | [Türkçe](README.tr.md) | [Русский](README.ru.md)

## ¿Qué es esto?

Transcribe y analiza tus archivos de audio/video automáticamente usando Gemini 3.1 Pro. [Obtén tu clave API gratuita →](https://evolink.ai/signup?utm_source=github&utm_medium=skill&utm_campaign=audio-analyze)

## Instalación

### Vía ClawHub (Recomendado)

```bash
openclaw skills add https://github.com/EvoLinkAI/audio-analyze-skill-for-openclaw
```

### Instalación manual

```bash
git clone https://github.com/EvoLinkAI/audio-analyze-skill-for-openclaw
cd audio-analyze-skill-for-openclaw
pip install -r requirements.txt
```

## Configuración

| Variable | Descripción | Predeterminado |
| :--- | :--- | :--- |
| `EVOLINK_API_KEY` | Clave API de EvoLink | (Requerido) |
| `EVOLINK_MODEL` | Modelo de transcripción | gemini-3.1-pro-preview-customtools |

*Para obtener información detallada sobre la configuración de la API y el soporte de modelos, consulta la [Documentación de la API de EvoLink](https://docs.evolink.ai/en/api-manual/language-series/gemini-3.1-pro-preview-customtools/openai-sdk/openai-sdk-quickstart?utm_source=github&utm_medium=skill&utm_campaign=audio-analyze).*

## Uso

### Uso básico

```bash
export EVOLINK_API_KEY="your-key-here"
./scripts/transcribe.sh audio.mp3
```

### Uso avanzado

```bash
./scripts/transcribe.sh audio.mp3 --diarize --lang ja
```

### Ejemplo de salida

* **TL;DR**: El audio es una pista de muestra para pruebas.
* **Puntos clave**: Sonido de alta fidelidad, respuesta de frecuencia clara.
* **Elementos de acción**: Subir a producción para pruebas finales.

## Modelos disponibles

- **Serie Gemini** (API de OpenAI — `/v1/chat/completions`)

## Estructura de archivos

```
.
├── README.md
├── SKILL.md
├── _meta.json
├── scripts/
│   └── transcribe.sh
└── references/
    └── api-params.md
```

## Solución de problemas

- **La lista de argumentos es demasiado larga**: Usa archivos temporales para datos de audio grandes.
- **Error de clave API**: Asegúrate de que `EVOLINK_API_KEY` esté exportada.

## Enlaces

- [ClawHub](https://clawhub.ai/EvoLinkAI/audio-analyze)
- [Referencia de la API](https://docs.evolink.ai/en/api-manual/language-series/gemini-3.1-pro-preview-customtools/openai-sdk/openai-sdk-quickstart?utm_source=github&utm_medium=skill&utm_campaign=audio-analyze)
- [Comunidad](https://discord.com/invite/5mGHfA24kn)
- [Soporte](mailto:support@evolink.ai)

## Licencia

MIT