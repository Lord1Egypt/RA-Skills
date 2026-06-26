<p align="center">
  <strong>🌐 Idiomas:</strong>
  <a href="README.zh.md">中文</a> |
  <a href="README.en.md">English</a> |
  <a href="README.es.md">Español</a> |
  <a href="README.ar.md">العربية</a>
</p>

# Agent PaddleOCR Vision —— Comprensión de Documentos y Acciones del Agente con PaddleOCR

**Transforma documentos en instrucciones accionables para agents de IA.** Esta herramienta utiliza exclusivamente la API en la nube de PaddleOCR, clasifica automáticamente los tipos de documentos y proporciona sugerencias de parámetros y prompts estructurados.

## Características generales

- OCR mediante PaddleOCR en la nube (compatible con tablas, fórmulas y múltiples idiomas)
- Clasificación automática en 15 tipos: invoice, business_card, receipt, table, contract, id_card, passport, bank_statement, driver_license, tax_form, financial_report, meeting_minutes, resume, travel_itinerary, general
- Reintentos automáticos en errores 5xx/timeout
- Procesamiento paralelo por lotes (bandera `--workers`)
- Exportación CSV (`--format csv`)
- Salida legible para humanos (`--format pretty`)
- Genera sugerencias de acciones para cada tipo (create_expense, add_contact, summarize, etc.)
- Procesamiento por lotes de directorios completos
- Generación de PDFs con capa de texto seleccionable (basada en bounding boxes, permite selección y búsqueda)
- Produce `extracted_fields` datos estructurados para uso directo del agente

## Instalación

### Dependencias del sistema

Ubuntu/Debian:

```bash
sudo apt-get update
sudo apt-get install -y python3 python3-pip poppler-utils
```

macOS:

```bash
brew install python poppler
```

### Paquetes Python

```bash
cd skills/agent-paddleocr-vision
pip3 install -r scripts/requirements.txt
```

### Configuración de la API de PaddleOCR

Deben definirse dos variables de entorno:

```bash
export PADDLEOCR_DOC_PARSING_API_URL=https://your-api.paddleocr.com/layout-parsing
export PADDLEOCR_ACCESS_TOKEN=your_access_token
```

*Nota: La URL de la API debe terminar en `/layout-parsing`.*

## Uso

### Documento individual

```bash
# Uso básico: procesa imagen o PDF, genera JSONpretty
python3 scripts/doc_vision.py --file-path ./invoice.jpg --pretty

# También genera PDF buscable
python3 scripts/doc_vision.py --file-path ./document.pdf --make-searchable-pdf --output result.json

# Solo texto
python3 scripts/doc_vision.py --file-path ./doc.pdf --format text
```

### Procesamiento por lotes

```bash
# Procesa todos los archivos compatibles en un directorio (.pdf, .png, .jpg, .jpeg, .bmp, .tiff, .webp)
python3 scripts/doc_vision.py --batch-dir ./inbox --output-dir ./out
```

Resultados por lotes:
- Se genera un JSON resumen (con totales, éxitos/fallos, estadísticas por tipo)
- Cada archivo obtiene su propio JSON en `--output-dir`

### Docker

```bash
docker build -t agent-paddleocr-vision:latest .
docker run --rm -v $(pwd)/data:/data \
  -e PADDLEOCR_DOC_PARSING_API_URL -e PADDLEOCR_ACCESS_TOKEN \
  agent-paddleocr-vision:latest \
  --file-path /data/invoice.jpg --pretty --make-searchable-pdf
```

## Formato de salida

```json
{
  "ok": true,
  "document_type": "invoice",
  "confidence": 0.94,
  "text": "Texto completo extraído (páginas separadas por doble salto de línea)",
  "pruned_result": { ... estructura de respuesta cruda de PaddleOCR ... },
  "suggested_actions": [
    {
      "action": "create_expense",
      "description": "Registrar esta factura en el sistema contable",
      "parameters": {
        "amount": "1200",
        "vendor": "某某科技有限公司",
        "date": "2025-03-15",
        "tax_id": "12345678"
      },
      "confidence": 0.92
    },
    {
      "action": "archive",
      "description": "Archivar esta factura en la biblioteca de documentos",
      "parameters": {},
      "confidence": 0.96
    },
    {
      "action": "tax_report",
      "description": "Incluir en el reporte fiscal actual",
      "parameters": { "tax_period": "2025-03" },
      "confidence": 0.78
    }
  ],
  "extracted_fields": {
    "amount": "1200",
    "vendor": "某某科技有限公司",
    "date": "2025-03-15"
  },
  "top_action": "create_expense",
  "metadata": {
    "pages": 1,
    "backend": "paddleocr",
    "source": "/ruta/absoluta/a/factura.jpg"
  },
  "searchable_pdf": "/ruta/absoluta/a/factura.searchable.pdf"
}
```

### Referencia de campos

| Campo | Descripción |
|------|-------------|
| ok | Indica si el procesamiento fue exitoso |
| document_type | Tipo de documento (invoice, business_card, …) |
| confidence | Puntuación de confianza de clasificación (0–1) |
| text | Todo el texto extraído de todas las páginas (formato Markdown) |
| pruned_result | Respuesta cruda de la API; incluye layoutParsingResults por página para procesamiento avanzado |
| suggested_actions | Lista de acciones sugeridas, ordenadas por confianza |
| extracted_fields | Campos estructurados (monto, fecha, nombre, etc.) para uso directo |
| top_action | Nombre de la acción con mayor confianza |
| metadata | Incluye número de páginas, backend utilizado, ruta de origen, etc. |
| searchable_pdf | Ruta al PDF con capa de texto (solo cuando se usa `--make-searchable-pdf`) |

## Integración con Agent

1. **Usar `extracted_fields`**: Acceder directamente a datos estructurados (monto, fecha, vendedor, etc.).
2. **Botones interactivos**: Convertir `suggested_actions` en botones de respuesta rápida.
3. **Ejecución automática**: Tras confirmar, llamar a la función con `parameters` de `suggested_actions`.

Ejemplo (pseudo-código estilo Node.js):

```javascript
const result = await callAgentVision({ 'file-path': '/ruta/doc.pdf' });
if (result.document_type === 'invoice') {
  for (const act of result.suggested_actions) {
    showButton(act.description, { action: act.action, params: act.parameters });
  }
}
```

## PDF con capa de texto buscable

`--make-searchable-pdf` crea un PDF con una capa de texto seleccionable y buscable. Funciona así:

1. Cada página del PDF de entrada se rasteriza a 200 DPI (con `pdf2image` y `poppler` del sistema)
2. Con las coordenadas `bbox` de fragmentos provenientes de `layoutParsingResults[].prunedResult` de PaddleOCR, se coloca texto invisible en las posiciones correspondientes (usando `reportlab`)
3. La imagen se mantiene como fondo; la capa de texto se superpone. Los lectores de PDF harán búsquedas sobre el texto incrustado

Si la API no devuelve bounding boxes, la versión de respaldo superpone el texto completo de la página en la parte inferior; permite búsqueda pero con posiciones aproximadas.

### Software requerido

- Sistema: `poppler-utils` (Ubuntu: `apt-get install poppler-utils`; macOS: `brew install poppler`)
- Python: `reportlab`, `pypdf`, `pillow`, `pdf2image`

## Tipos de documentos y acciones

| Tipo | Identificación | Acciones sugeridas |
|------|----------------|-------------------|
| Factura (invoice) | número de factura, monto, ID fiscal, vendedor/comprador | create_expense, archive, tax_report |
| Tarjeta de visita (business_card) | nombre, teléfono, email, puesto | add_contact, save_vcard |
| Recibo (receipt) | comercio, monto pagado, fecha de transacción | create_expense, split_bill |
| Tabla (table) | líneas de cuadrícula, multi-columna, encabezado | export_csv, analyze_data |
| Contrato (contract) | número de cláusula, firmas, fecha efectiva | summarize, extract_dates, flag_obligations |
| DNI (id_card) | número de identidad, nombre, fecha nacimiento, género | extract_id_info, verify_age |
| Pasaporte (passport) | número de pasaporte, nacionalidad, fechas emisión/expiración | store_passport_info, check_validity |
| Estado de cuenta (bank_statement) | número de cuenta, periodo, saldo, historial de transacciones | categorize_transactions, generate_report |
| Licencia de conducir (driver_license) | número de licencia, clase, vencimiento, dirección | store_license_info, check_expiry |
| Formulario fiscal (tax_form) | año fiscal, ingreso total, impuesto a pagar, deducciones | summarize_tax, suggest_deductions |
| General (general) | sin patrón específico | summarize, translate, search_keywords |
| Informe financiero (financial_report) | ingresos, beneficios, márgenes | summarize_financials, compare_periods, flag_risks |
| Minutas de reunión (meeting_minutes) | asistentes, decisiones, acciones | extract_action_items, create_calendar_events, send_summary |
| Currículum (resume) | nombre, email, educación, habilidades | create_candidate_profile, match_jobs, extract_skills |
| Itinerario de viaje (travel_itinerary) | vuelos, hoteles, fechas | create_calendar_events, set_reminders, check_visa |

## Solución de problemas

### La API de PaddleOCR devuelve 403 o 404

Verificar:
- `PADDLEOCR_DOC_PARSING_API_URL` es correcto y termina en `/layout-parsing`
- `PADDLEOCR_ACCESS_TOKEN` es válido y no ha expirado
- Conectividad de red al endpoint de la API

### Fallo en la generación del PDF buscable

Asegurarse de tener instalado:
```bash
pip3 show reportlab pypdf pdf2image
```
Y que el sistema tenga `poppler`:
```bash
which pdftoppm  # debería existir
```

Si persiste, revisar `stderr`; causas comunes:
- PDF de entrada corrupto o encriptado
- Datos de bounding box faltantes (se generará PDF pero con ubicación de texto aproximada)

### Baja calidad de OCR

- Asegurar que el documento esté nítido, bien iluminado y con buen contraste
- Para chino, PaddleOCR lo maneja; otros idiomas suelen autodetectarse
- Aumentar el DPI de origen (recomendado 300+)

### Procesamiento por lotes lento

- Considerar procesamiento paralelo (ej. GNU parallel)
- Si se usa la API en la nube, respetar límites de velocidad; aumentar timeout o dividir en lotes más pequeños

## Arquitectura

```
doc_vision.py  →  punto de entrada principal
   ├─ ocr_engine.py      → llama a la API de PaddleOCR, devuelve texto + pruned_result
   ├─ classify.py        → clasifica el tipo de documento según el contenido de texto
   ├─ actions.py         → extrae parámetros y genera lista de acciones sugeridas
   ├─ (sin plantillas)   → datos estructurados directos, sin plantillas
   └─ make_searchable_pdf.py → genera PDF con capa de texto usando bboxes
```

## Desarrollo de nuevos tipos de documento

1. En `scripts/classify.py`, añadir función de coincidencia y constante:
   ```python
   DOC_TYPE_MY_TYPE = "my_type"
   def match_my_type(text: str) -> float:
       patterns = [r"palabra_clave1", r"palabra_clave2"]
       return sum(bool(re.search(p, text, re.IGNORECASE)) for p in patterns) / len(patterns)
   ```
   Luego agregar `DOC_TYPE_MY_TYPE: match_my_type(text)` al diccionario `scores` en `classify()`.

2. En `scripts/actions.py`, añadir función generadora:
   ```python
   def suggest_my_type(text: str, metadata) -> List[Action]:
       # extrae parámetros, devuelve lista de Action
       ...
   SUGGESTION_DISPATCH[DOC_TYPE_MY_TYPE] = suggest_my_type
   ```

3. Añadir `templates/my_type.md` (plantilla Jinja2) con instrucciones y parámetros para el agente.

4. Añadir una fila en la tabla “Document Type Reference” de `docs/README.zh.md`.

## Rendimiento y recursos

- Latencia típica por solicitud: 2–15 segundos (dependiendo del número de páginas y velocidad de la API)
- Uso de memoria: hasta 2–3× el tamaño del archivo al procesar PDFs
- El modo por lotes no incluye paralelismo integrado; envolverlo con multiprocessing si es necesario

## Licencia

MIT-0

## Historial de versiones

- v1.0.0 — Versión inicial (2025-03-15)

---

**¿Problemas?** Revise la salida `stderr` o abra un issue en GitHub.
