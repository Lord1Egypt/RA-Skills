# Benchmarks salariales — referencia para `analyze_profile.py`

Este archivo provee bandas de referencia para que el script de análisis le diga al usuario "a esto podés aspirar hoy con tu CV". Las bandas son **mensuales en USD**, total cash (excluye equity), para roles tech individuales en empresas serias.

⚠️ **Estos números cambian.** Última calibración: 2026-Q1. Refrescá cada 6 meses cruzando con levels.fyi, Repvue, surveys recientes (Stack Overflow, ICTjob, JetBrains), y posts de "Who is hiring" de HN.

## Backend / Full-stack — engineer track

| Seniority | LATAM remoto (USD) | US remoto (USD) | EU remoto (EUR) |
|---|---|---|---|
| Junior (0-2 yr) | 1.5k – 3k | 5k – 7k | 3k – 4.5k |
| Mid (2-5 yr) | 3k – 5.5k | 7k – 11k | 4.5k – 7k |
| Senior (5-8 yr) | 5k – 9k | 11k – 16k | 7k – 10k |
| Staff (8-12 yr) | 8k – 14k | 16k – 24k | 10k – 14k |
| Principal (12+ yr) | 12k – 22k | 22k – 35k+ | 14k – 20k+ |

## Frontend especializado

Bandas similares a backend, con leve descuento (~10%) en mid-senior, paridad o premium en staff+ si tiene expertise en performance/design systems.

## Mobile (iOS / Android nativo)

Premium del 5-15% sobre backend en LATAM y EU por escasez. Paridad en US.

## Data engineering / ML engineering

Premium del 10-25% sobre backend en todos los mercados. Para ML applied (no investigación), aplicar los rangos de senior+ subidos un escalón.

## DevOps / SRE / Platform

Paridad con backend hasta senior; premium en staff+ por escasez de seniority real (mucha gente con título senior pero experiencia operativa baja).

## Engineering Management

| Nivel | LATAM remoto | US remoto | EU remoto |
|---|---|---|---|
| Tech Lead (sin people mgmt formal) | 6k – 10k | 13k – 18k | 8k – 12k |
| Engineering Manager | 8k – 13k | 16k – 22k | 11k – 15k |
| Senior EM / Director | 11k – 18k | 22k – 35k | 14k – 20k |

## Modificadores

Aplicar al rango base detectado por seniority + stack:

- **+15-25% si:** trabajó en empresa Tier S (Stripe, Shopify, etc.) en los últimos 3 años
- **+10% si:** tiene OSS contributions reales (no docs ni typo fixes — features mergeadas en proyectos con > 5k stars)
- **+5-10% si:** charlas en conferencias técnicas verificables
- **+10-20% si:** rol de specialist (security, performance, distributed systems) con casos documentados
- **-10-20% si:** stack legacy dominante (PHP no-laravel, JSP, Cobol, Delphi) — incluso con seniority real, achica el pool de empresas que ofrecen banda alta
- **-15% si:** sin inglés C1 verificable y target es US/EU remoto

## Heurística de seniority

`analyze_profile.py` estima seniority cruzando:

1. **Años totales** (peso 30%)
2. **Años en el rol más senior listado** (peso 25%)
3. **Indicadores de scope** en bullets (peso 25%):
   - "led", "architected", "designed system that…" → +seniority
   - "implemented feature", "fixed bug" → mid
   - "learned", "assisted" → junior
4. **Métricas de impacto** (peso 20%):
   - Números concretos (latencia, costos, throughput, usuarios) → +seniority percibida

Si el CV no tiene métricas en ningún bullet, devolver el rango bajo de la banda detectada y flaggear como gap top-1.

## Cómo usar para "tips para subir banda"

Cuando el análisis ubique al usuario en, digamos, banda Senior LATAM (5k-9k):

1. **Camino corto (3-6 meses):** mejorar el CV — métricas de impacto en cada rol, eliminar bullets vagos, agregar 2-3 logros con números. Esto sube la *percepción* sin cambiar el rol real. Ganancia esperada: pasar del piso al techo de la misma banda (~30-50% upside).

2. **Camino medio (6-18 meses):** moverse a mercado superior. Si está en banda LATAM, postular a empresas que pagan en US remoto. Mismo seniority, ~2x cash. Requiere inglés C1 verificable y CV con keywords/cultura US.

3. **Camino largo (1-3 años):** subir de nivel real. Senior → Staff requiere demostrar:
   - Liderazgo técnico cross-team
   - Diseño de sistemas que escalaron
   - Influencia en decisiones de roadmap
   - Mentoría documentada
   Sin esto, hay un techo en Senior aunque pasen los años.

Presentale al usuario los tres caminos en orden de ROI/esfuerzo. El primero casi siempre es el de mejor relación.
