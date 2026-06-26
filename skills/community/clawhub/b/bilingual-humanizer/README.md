# bilingual-humanicer

> **Fork y refactorización completa de [brandonwise/humanizer](https://github.com/brandonwise/humanizer)**
>
> El proyecto original solo soportaba inglés. Para permitir escalabilidad a múltiples idiomas, se realizó una refactorización casi completa de la arquitectura, separando la lógica core de la presentación, añadiendo soporte nativo para español con patrones específicos (PatternES-01 a PatternES-20), y reorganizando el código en módulos reutilizables por idioma.

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Tests](https://img.shields.io/badge/tests-318%20passing-brightgreen)
![Node >= 18](https://img.shields.io/badge/node-%3E%3D18-brightgreen)

Detecta y elimina patrones de escritura generada por IA en **español e inglés**.

Analiza texto con **49 detectores de patrones** (29 EN + 20 ES), **500+ términos de vocabulario** en tres niveles, y **análisis estadístico** (burstiness, type-token ratio, legibilidad) — luego da sugerencias accionables para corregirlos.

Disponible como **skill para agentes** (OpenClaw, Claude Desktop), **MCP server** y **CLI standalone**.

Basado en [Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), [investigación estilométrica de Copyleaks](https://arxiv.org/abs/2503.01659) y [blader/humanizer](https://github.com/blader/humanizer).

**→ [Guía completa de uso](docs/GUIDE.md)** — todos los comandos, opciones, API, referencia de patrones, CI/CD.

---

## Instalación

Elige según tu agente o entorno:

| Agente / Entorno | Cómo instalar la skill | CLI / MCP |
| --- | --- | --- |
| OpenClaw | `clawhub install bilingual-humanicer` | `npm install -g bilingual-humanizer` |
| Claude Code | Clonar repo + copiar `SKILL.md` y `knowledge/` | `npm install -g bilingual-humanizer` |
| Claude Desktop | Clonar repo + copiar `SKILL.md` y `knowledge/` | Configurar MCP server |
| Desarrolladores | Clonar repo | Código fuente + tests incluidos |

### Opción A — Skill (todos los agentes)

La skill funciona de forma autónoma con su `knowledge/` — el agente aplica los 49 detectores de patrones directamente, sin herramientas externas.

**OpenClaw:** instala con un solo comando:

```bash
clawhub install bilingual-humanicer
```

**Claude Code, Claude Desktop y otros agentes:** clona el repositorio y copia `SKILL.md` y la carpeta `knowledge/` al directorio de skills de tu agente:

```bash
git clone https://github.com/SitoSt/bilingual-humanicer.git
# Luego copia SKILL.md y knowledge/ a la ubicación que tu agente reconoce
```

Para análisis estadístico preciso (burstiness, TTR, score numérico), combínala con el MCP server (opción B) o la CLI (opción C).

### Opción B — MCP server (Claude Desktop)

```bash
npm install -g bilingual-humanizer
```

Añade a tu `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "humanizer": {
      "command": "node",
      "args": ["/ruta/a/bilingual-humanicer/mcp-server/index.js"]
    }
  }
}
```

Herramientas disponibles: `humanizer.score`, `humanizer.analyze`, `humanizer.humanize`, `humanizer.stats`.

### Opción C — CLI (Claude Code, terminal)

> **Nota de seguridad:** el CLI y el MCP server se instalan desde npm/GitHub y contienen código fuente que no forma parte del artefacto revisado en ClawHub. Revisa el [repositorio](https://github.com/SitoSt/bilingual-humanicer) antes de instalar, y usa una versión pinada si lo integras en entornos de producción.

```bash
npm install -g bilingual-humanizer@3.2.0
humanizer --help
```

O sin instalación global:

```bash
git clone https://github.com/SitoSt/bilingual-humanicer.git
cd bilingual-humanicer && npm install
node src/cli/index.js --help
```

---

## Quickstart

El idioma por defecto es **español**. Para inglés: `--lang en`.

```bash
# Puntuación rápida (0-100, mayor = más IA)
humanizer score -f borrador.md

# Análisis completo con matches y estadísticas
humanizer analyze -f artículo.md

# Sugerencias de humanización
humanizer humanize -f post.md

# Aplicar correcciones automáticas seguras
humanizer humanize --autofix -f post.md > post-v2.md

# Ver exactamente qué mejoró entre versiones
humanizer compare --before post.md --after post-v2.md

# Escanear toda una carpeta y detectar hotspots
humanizer scan docs --ext md,txt --fail-above 50

# Inglés
humanizer analyze -f article.md --lang en
```

---

## Comandos

| Comando    | Descripción                                                             |
| ---------- | ----------------------------------------------------------------------- |
| `score`    | Puntuación rápida: `🟢 12/100`                                          |
| `analyze`  | Análisis completo con patrones, estadísticas y confiabilidad            |
| `humanize` | Sugerencias agrupadas por prioridad + guidance de escritura             |
| `suggest`  | Solo sugerencias, sin estadísticas                                      |
| `report`   | Informe Markdown completo (para guardar o enviar)                       |
| `stats`    | Solo métricas estadísticas del texto                                    |
| `scan`     | Escanea un directorio, rankea archivos, detecta hotspots entre archivos |
| `compare`  | Compara dos versiones y muestra qué patrones mejoraron/empeoraron       |

Todas las formas de leer texto:

```bash
# Desde archivo
humanizer score -f borrador.md

# Desde stdin
echo "Texto aquí" | humanizer score
cat artículo.txt | humanizer analyze

# compare requiere --before y --after
humanizer compare --before v1.md --after v2.md
```

---

## Puntuación

```text
Score = (Pattern Score × 0.70) + (Uniformity Score × 0.30)
```

| Badge | Rango  | Nivel                    |
| ----- | ------ | ------------------------ |
| 🟢    | 0–19   | Mostly human-sounding    |
| 🟡    | 20–44  | Lightly AI-touched       |
| 🟠    | 45–69  | Moderately AI-influenced |
| 🔴    | 70–100 | Heavily AI-generated     |

Junto al score se muestra un nivel de **confiabilidad** (`high` / `medium` / `low`) basado en la longitud del texto. Confiabilidad alta requiere ≥150 palabras.

---

## Arquitectura del motor de scoring

```text
┌──────────────────────────────────────────────────────┐
│                 Score compuesto (0-100)               │
├─────────────────────────┬────────────────────────────┤
│    Pattern Score (70%)  │   Uniformity Score (30%)   │
├─────────────────────────┼────────────────────────────┤
│ • 39 detectores de      │ • Burstiness (variación    │
│   patrones (29 EN,      │   longitud de oraciones)   │
│   20 ES)               │ • Type-token ratio         │
│ • 500+ términos de      │ • Repetición de trigramas  │
│   vocabulario (3 tiers) │ • Legibilidad (IFSZ / FK)  │
│ • Scoring por densidad  │ • Densidad de conectores   │
│ • Bonus por amplitud    │   (español)                │
│   y diversidad de       │                            │
│   categorías            │                            │
└─────────────────────────┴────────────────────────────┘
```

**Pattern score:** densidad de matches por 100 palabras en curva logarítmica, con bonificación por amplitud (patrones únicos detectados) y diversidad de categorías.

**Uniformity score:** el texto humano tiene alta burstiness (variación de longitud), vocabulario diverso y baja repetición de n-gramas. El texto de IA es mecánicamente uniforme.

---

## Análisis estadístico

| Métrica                     | Texto humano | Texto IA  | Por qué importa                                                                           |
| --------------------------- | ------------ | --------- | ----------------------------------------------------------------------------------------- |
| **Burstiness**              | 0.5–1.0      | 0.1–0.3   | Los humanos escriben en ráfagas: oraciones cortas y largas mezcladas. La IA es metrónomo. |
| **Type-token ratio**        | 0.5–0.7      | 0.3–0.5   | Los humanos usan vocabulario más variado. La IA recicla las mismas palabras.              |
| **Sentence CoV**            | 0.4–0.8      | 0.15–0.35 | Coeficiente de variación de longitud de oraciones. Bajo = uniformidad robótica.           |
| **Trigram repetition**      | < 0.05       | > 0.10    | La IA reutiliza las mismas frases de 3 palabras con más frecuencia.                       |
| **IFSZ** (español)          | 60–85        | 50–65     | Índice Flesch-Szigriszt. La IA tiende a niveles de legibilidad consistentes.              |
| **Flesch-Kincaid** (inglés) | Varía        | 8–12      | La IA tiende a escribir en un nivel de grado constante.                                   |

---

## Soporte bilingüe

| Aspecto | Español (`--lang es`, defecto) | Inglés (`--lang en`) |
| --- | --- | --- |
| Patrones activos | PatternES-01–20 + PatternEN-7 (vocab. IA) | PatternEN-1–29 |
| Legibilidad | IFSZ (Flesch-Szigriszt) | Flesch-Kincaid grade |
| Métrica extra | Densidad de conectores | — |
| Vocabulario | ~400 términos ES inflados | 500+ términos AI EN |

**Patrones exclusivos del español:**

- Gerundios encadenados (_aprovechando las oportunidades, generando valor, facilitando…_)
- Aperturas con contexto vago (_En el contexto actual de la transformación digital…_)
- Tríadas de abstractos (_eficiencia, innovación y sostenibilidad_)
- Tono sycofántico (_Excelente pregunta, es un honor responder…_)
- Énfasis metacomentario (_Es importante destacar, cabe señalar, resulta fundamental…_)
- Conclusiones genéricas (_En conclusión, es fundamental considerar…_)
- Atribuciones vagas (_Según los expertos, los estudios demuestran…_)

---

## Opciones

```text
-f, --file <ruta>          Leer desde archivo (por defecto: stdin)
--lang <en|es>             Idioma de análisis (defecto: es)
--json                     Salida en JSON
--verbose, -v              Mostrar todos los matches (por defecto: top 5)
--autofix                  Aplicar correcciones automáticas (humanize)
--patterns <ids>           Sólo analizar patrones indicados (ej: 7,19,22)
--threshold <n>            Sólo mostrar patrones con peso ≥ n
--ignore-code              Ignorar bloques de código fenced e inline
--before <ruta>            Archivo anterior (compare)
--after <ruta>             Archivo nuevo (compare)
--ext <lista>              Extensiones para scan (defecto: md,txt,rst,adoc)
--min-words <n>            Ignorar archivos con menos de n palabras
--fail-above <n>           Salir con código 2 si score ≥ n (scan)
--baseline <archivo>       JSON de scan previo para comparar (scan)
--regression-threshold <n> Delta mínimo para considerar regresión (defecto: 1)
--fail-on-regression       Salir con código 3 si hay regresiones (scan)
--ignore-dirs <lista>      Directorios extra a ignorar (scan)
--no-default-ignore        Desactivar ignores predefinidos (.git, node_modules…)
--config <archivo>         Cargar defaults de scan desde JSON
--help, -h                 Mostrar ayuda
```

---

## Archivo de configuración

Crea `.humanizer.json` para reutilizar opciones de `scan`:

```json
{
  "scan": {
    "extensions": ["md", "txt"],
    "minWords": 30,
    "failAbove": 50,
    "baseline": ".humanizer-baseline.json",
    "regressionThreshold": 3,
    "failOnRegression": true,
    "ignoreDirs": ["generated", "vendor"],
    "includeDefaultIgnore": true,
    "ignoreCode": true
  }
}
```

```bash
humanizer scan docs --config .humanizer.json
# Los flags CLI sobreescriben el config
humanizer scan docs --config .humanizer.json --fail-above 40
```

---

## Uso en CI/CD

```bash
# Gate básico: fallar si algún archivo supera score 50
humanizer scan docs --ext md --fail-above 50

# Gate de regresiones: sólo fallar si algo empeora
humanizer scan docs --json > .humanizer-baseline.json   # guardar baseline
humanizer scan docs --baseline .humanizer-baseline.json --fail-on-regression
```

Códigos de salida: `0` éxito · `1` error · `2` fail-above · `3` regresión.

---

## API programática

```javascript
const { analyze, score } = require('./src/core/analyzer');

// Score rápido
const s = score('Tu texto aquí', { lang: 'es' }); // 0-100

// Análisis completo
const result = analyze(text, {
  lang: 'es', // 'es' | 'en'
  verbose: false, // true: todos los matches
  ignoreCode: false, // true: ignora bloques de código
  includeStats: true,
});

console.log(result.score); // 0-100
console.log(result.patternScore); // componente de patrones (70%)
console.log(result.uniformityScore); // componente estadístico (30%)
console.log(result.reliability); // { level, score, recommendation }
console.log(result.stats); // burstiness, typeTokenRatio, ifsz…
console.log(result.findings); // patrones detectados con matches
console.log(result.categories); // agrupado por categoría
```

```javascript
const { humanize, autoFix } = require('./src/core/humanizer');

const result = humanize(text, { lang: 'es', autofix: true });
console.log(result.critical); // issues con peso ≥ 4
console.log(result.important); // issues con peso 2–3
console.log(result.guidance); // consejos de escritura
console.log(result.autofix.text); // texto corregido
console.log(result.autofix.fixes); // lista de correcciones aplicadas
```

```javascript
const { scanPath, compareScanResults } = require('./src/workflows');

const scan = scanPath('docs', { exts: ['.md'], lang: 'es', ignoreCode: true });
console.log(scan.summary); // { scannedFiles, averageScore, maxScore… }
console.log(scan.files); // ordenado por score desc
console.log(scan.patternHotspots); // patrones más frecuentes entre archivos
```

→ [Documentación completa de la API](docs/GUIDE.md#api-programática)

---

## Bake-in: Que tu agente escriba siempre como humano

La forma más efectiva de usar humanizer no es corregir después, sino evitar los patrones desde el inicio.

### Para Claude (`CLAUDE.md`)

```text
Escribe como un humano directo, no como una IA. Nunca uses: "destacar",
"transformador", "exhaustivo", "fundamental", "paradigma", "potenciar",
"ecosistema", "En el contexto actual", "Es importante señalar", "Cabe destacar",
"En conclusión, es fundamental". Usa "es" en lugar de "sirve como".
Varía la longitud de las oraciones. Ten opiniones. Usa números y nombres
concretos en lugar de "los expertos dicen". Termina con algo específico,
no con "el futuro es prometedor".
```

### Para ChatGPT (Custom Instructions)

```text
Write like a specific human, not a generic AI. Never use: delve, tapestry,
vibrant, crucial, robust, seamless, groundbreaking, transformative, leverage,
synergy, paramount. Never write "Great question!" or "I hope this helps!".
Use "is" not "serves as". Vary sentence length. Have opinions. Use real
numbers and names, not "experts say" or "studies show".
```

### Verificar

```bash
echo "Respuesta de tu agente aquí" | humanizer score
# Objetivo: bajo 20 consistentemente
```

---

## Estructura del proyecto

```text
humanizer/
├── src/
│   ├── constants.js          # DEFAULT_LANG, SCORE_THRESHOLDS, scoreLabel
│   ├── vocabulary.js         # 500+ palabras y frases IA (inglés)
│   ├── workflows.js          # scanPath, compareTexts, compareScanResults
│   ├── locales/              # Vocabulario y configuración por idioma
│   │   ├── en.js
│   │   └── es.js
│   ├── core/                 # Cómputo puro (sin ANSI, sin console.log)
│   │   ├── analyzer.js       # analyze(), score()
│   │   ├── humanizer.js      # humanize(), autoFix()
│   │   ├── stats.js          # computeStats(), computeUniformityScore()
│   │   ├── utils.js          # Helpers de labels y texto
│   │   └── patterns/         # 39 detectores de patrones
│   │       ├── en.js         # PatternEN-1 a PatternEN-29
│   │       └── es.js         # PatternES-01 a PatternES-20
│   ├── formatters/           # Texto plano, sin ANSI
│   │   ├── report.js         # formatText(), formatMarkdown(), buildSummary()
│   │   ├── suggestions.js    # formatGroupedSuggestions()
│   │   ├── stats.js          # formatStatsReport()
│   │   └── scan.js           # formatScanReport(), formatComparisonReport()
│   └── cli/                  # Capa CLI (ANSI, I/O)
│       ├── index.js          # Punto de entrada
│       ├── flags.js          # parseArgs(), resolveOpts()
│       ├── input.js          # Lectura stdin/archivo
│       ├── renderer.js       # Render con colores ANSI
│       └── commands/         # analyze, score, humanize, report,
│                             # suggest, stats, scan, compare
├── tests/                    # 318 tests (vitest)
├── docs/
│   ├── GUIDE.md              # Guía completa de uso
│   └── ...
└── SKILL.md                  # Definición del skill OpenClaw
```

---

## Qué lo diferencia

| Característica                 | humanizer                         | GPTZero       | Copyleaks        | ZeroGPT       |
| ------------------------------ | --------------------------------- | ------------- | ---------------- | ------------- |
| Open source                    | ✅                                | ❌            | ❌               | ❌            |
| Scoring transparente           | ✅ Explicable por patrón          | ❌ Caja negra | ❌ Caja negra    | ❌ Caja negra |
| Sugerencias accionables        | ✅ Por patrón con fix             | ❌ Solo score | ❌ Solo score    | ❌ Solo score |
| Auto-fix                       | ✅ Correcciones mecánicas seguras | ❌            | ❌               | ❌            |
| Soporte español                | ✅ 20 patrones ES + IFSZ          | Parcial       | Parcial          | ❌            |
| Análisis estadístico           | ✅ Burstiness, TTR, IFSZ/FK       | ✅ Perplexity | ✅ Estilométrico | ❌            |
| Sin API key                    | ✅                                | ❌            | ❌               | ❌            |
| Funciona offline               | ✅                                | ❌            | ❌               | ❌            |
| Sin dependencias de producción | ✅                                | N/A           | N/A              | N/A           |

---

## Contribuir

1. Fork y crear rama
2. Añadir o mejorar detectores (ver `src/core/patterns/`)
3. Escribir tests para los cambios
4. `npm run check` — lint + format + tests deben pasar
5. Abrir PR

## Licencia

[MIT](LICENSE)
