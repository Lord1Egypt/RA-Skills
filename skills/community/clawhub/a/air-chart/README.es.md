<div align="center">

# Air-chart

**Una frase. Tu IA te dibuja un gráfico profesional de calidad del aire.**

English | [简体中文](README.zh.md) | **Español** | [हिन्दी](README.hi.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Français](README.fr.md)

![Claude Code](https://img.shields.io/badge/Claude%20Code-native-blue)
![Cursor](https://img.shields.io/badge/Cursor-native-blue)
![Codex CLI](https://img.shields.io/badge/Codex%20CLI-compatible-blue)
![ClawHub](https://img.shields.io/badge/ClawHub-publishable-green)
![skills.sh](https://img.shields.io/badge/skills.sh-installable-green)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

## ¿Qué hace esta skill?

Di una frase en tu chat de IA — **encuentra la estación, obtiene los datos y te devuelve un enlace al gráfico**, con [x-cmd Draw](https://x-cmd.com/draw): datos y gráfico en una sola URL:

> 💬 "Muéstrame la tendencia de PM2.5 de Pekín en la última semana"
> 💬 "Compara la calidad del aire de Tokio y Seúl de los últimos 7 días"
> 💬 "PM10 de Nueva Delhi en 30 días, frente a la guía de la OMS"
> 💬 "Ozono hora a hora en Singapur de las últimas 48 horas"
> 💬 "¿Qué estación de Pekín está peor ahora mismo?"

Detrás de escena, una canalización totalmente automatizada: resuelve la ciudad → elige una estación **genuinamente activa** de **OpenAQ** (datos gubernamentales de referencia de más de 100 países) → limpia valores atípicos y vacíos → renderiza un gráfico profesional.

**Por qué te va a gustar:**

- **El gráfico es una URL — la URL es el dato** — por defecto obtienes un enlace `x-cmd.com/draw` que a la vez renderiza el gráfico y lleva cada valor. Compártelo, intégralo en Markdown como imagen, o edita un número en la URL y el gráfico se actualiza. ¿Necesitas un archivo? `--out chart.svg` (o `.png`) lo descarga.
- **Renderizado por x-cmd Draw** — tu canalización local sigue siendo pura `bash`/`jq`/`awk`/`curl`; el motor de gráficos es [x-cmd Draw](https://x-cmd.com/draw), así que heredas una biblioteca creciente de tipos de gráfico (líneas, barras, áreas, tarta, radar, gauge, sankey, Gantt, mapas mentales y más), temas claro/oscuro, renderizado multilingüe, un editor en línea y cero código de renderizado que mantener. Nada que instalar, nada que actualizar.
- **Fiable por diseño** — prefiere estaciones gubernamentales de referencia; los gráficos etiquetan la concentración física (µg/m³) y superponen la **guía de 24 horas de la OMS** como serie de referencia, de modo que el límite viaja con el dato en lugar de ser una ocurrencia tardía. No es un número vanidoso de AQI: son datos que puedes poner en un informe.
- **Cobertura global, entrada tolerante** — coordenadas integradas de más de 250 ciudades; nombres difusos (`delhi`, `tOKyo`, `中山`) funcionan de entrada, y también se aceptan `lat,lon` en crudo.
- **Datos reales, no un juguete** — descarta estaciones «zombi» silenciosas y picos por fallo de sensor; las horas faltantes se omiten del eje, jamás se rellenan con 0.

## Galería

Cada gráfico de abajo es una **medición real de OpenAQ** renderizada en vivo desde su URL que contiene los datos — este repositorio no guarda ningún archivo de imagen. Haz clic en cualquier gráfico para abrirlo en el editor de x-cmd Draw y ajustar los valores.

| PM2.5 multiciudad, últimos 7 días (Tokio · Seúl · Londres) | Nueva Delhi PM2.5 / PM10, últimos 14 días |
| --- | --- |
| [![PM2.5 multiciudad, últimos 7 días (Tokio · Seúl · Londres)][sc1] | [![Nueva Delhi PM2.5 / PM10, últimos 14 días][sc3] |

| Ozono (O₃) de Londres, últimas 48 horas | Instantánea de PM10 por estación en Nueva Delhi (en vivo) |
| --- | --- |
| [![Ozono (O₃) de Londres, últimas 48 horas][sc2] | [![Instantánea de PM10 por estación en Nueva Delhi (en vivo)][sc4] |

| Tema oscuro: PM2.5 multiciudad | Nueva Delhi PM2.5, últimos 30 días |
| --- | --- |
| [![Tema oscuro: PM2.5 multiciudad][sc5] | [![Nueva Delhi PM2.5, últimos 30 días][sc6] |

[sc1]: https://x-cmd.com/draw?type=line&title=Comparaci%C3%B3n%20de%20PM2.5%20%C2%B7%20%C3%BAltimos%207d%20%C2%B7%20multiciudad%20%C2%B7%20mismo%20par%C3%A1metro&unit=%C2%B5g%2Fm%C2%B3&labels=11-07,11-08,11-09,11-10,11-11,11-12,11-13&series=Tokyo%20PM2.5:2.73,2.95,5,5.5,6.45,10.4,12.7&series=Seoul%20PM2.5:7.96,9.58,10.3,16.2,22.8,28.8,28.3&series=London%20PM2.5:58.3,82.4,49.4,23.9,15.8,10.8,13.7&series=OMS%2024h:15,15,15,15,15,15,15&w=960&h=500&t=opendata
[sc2]: https://x-cmd.com/draw?type=line&title=Tendencia%20de%20London%20O3%20%C2%B7%20%C3%BAltimos%2048h%20%C2%B7%20hora%20local%20%28Europe%2FLondon%29&unit=%C2%B5g%2Fm%C2%B3&labels=11-12%2001%3A00,11-12%2002%3A00,11-12%2003%3A00,11-12%2004%3A00,11-12%2005%3A00,11-12%2006%3A00,11-13%2000%3A00,11-13%2001%3A00,11-13%2002%3A00,11-13%2003%3A00,11-13%2004%3A00,11-13%2005%3A00,11-13%2006%3A00,11-13%2007%3A00&series=London%20O3:52.7,51.2,42.7,43.1,41,31.4,42.7,44.9,46.5,48.3,39.6,17.1,15.4,17&series=OMS%2024h:100,100,100,100,100,100,100,100,100,100,100,100,100,100&w=960&h=500&t=opendata
[sc3]: https://x-cmd.com/draw?type=line&title=Tendencia%20de%20New%20Delhi%20PM2.5%20%2F%20PM10%20%C2%B7%20%C3%BAltimos%2014d%20%C2%B7%20multipar%C3%A1metro&unit=%C2%B5g%2Fm%C2%B3&labels=10-31,11-01,11-02,11-03,11-04,11-05,11-06,11-07,11-08,11-09,11-10,11-11,11-12,11-13&series=New%20Delhi%20PM2.5:110,205,217,241,265,305,306,339,302,222,163,147,232,172&series=OMS%2024h:15,15,15,15,15,15,15,15,15,15,15,15,15,15&w=960&h=500&t=opendata
[sc4]: https://x-cmd.com/draw?type=hbar&title=Instant%C3%A1nea%20de%20New%20Delhi%20por%20estaci%C3%B3n%20%C2%B7%20PM10%20%C2%B7%202026-11-14%2013%3A26%20IST%20%C2%B7%20radio%20de%2025%20km&unit=%C2%B5g%2Fm%C2%B3&labels=Alipur,Anand%20Vihar,Ashok%20Vihar,Aya%20Nagar,Bawana,Burari%20Crossing&values=418.0,409.0,426.0,501.0,382.0,533.0&num=all&w=960&h=480&t=evil-glow
[sc5]: https://x-cmd.com/draw?type=line&title=Comparaci%C3%B3n%20de%20PM2.5%20%C2%B7%20%C3%BAltimos%207d%20%C2%B7%20multiciudad%20%C2%B7%20mismo%20par%C3%A1metro&unit=%C2%B5g%2Fm%C2%B3&labels=11-07,11-08,11-09,11-10,11-11,11-12,11-13&series=Tokyo%20PM2.5:2.73,2.95,5,5.5,6.45,10.4,12.7&series=Seoul%20PM2.5:7.96,9.58,10.3,16.2,22.8,28.8,28.3&series=London%20PM2.5:58.3,82.4,49.4,23.9,15.8,10.8,13.7&series=OMS%2024h:15,15,15,15,15,15,15&w=960&h=500&scheme=dark&t=opendata
[sc6]: https://x-cmd.com/draw?type=line&title=Tendencia%20de%20New%20Delhi%20PM2.5%20%C2%B7%20%C3%BAltimos%2030d%20%C2%B7%20hora%20local%20%28Asia%2FKolkata%29&unit=%C2%B5g%2Fm%C2%B3&labels=10-15,10-16,10-17,10-18,10-19,10-20,10-21,10-22,10-23,10-27,10-28,10-29,10-30,10-31,11-01,11-02,11-03,11-04,11-05,11-06,11-07,11-08,11-09,11-10,11-11,11-12,11-13&series=New%20Delhi%20PM2.5:73.6,65.7,94,127,94,125,142,136,142,138,131,95,44.7,110,205,217,241,265,305,306,339,302,222,163,147,232,172&series=OMS%2024h:15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15&w=960&h=500&t=opendata

## Características

- **Cero dependencias pesadas** — pura `bash` / `jq` / `awk` / `curl`; el renderizador SVG está escrito en awk.
- **Cobertura global** — coordenadas integradas de más de 200 ciudades principales, o pasa `lat,lon` directamente.
- **Selección inteligente de estación** — búsqueda en radio de 25 km → descarta estaciones «zombi» sin datos en 24 h (reintento a 72 h) → prioriza monitores gubernamentales de referencia.
- **Visuales profesionales** — unidades de concentración física (µg/m³) claramente etiquetadas, línea de la guía de 24 h de la OMS superpuesta por defecto (verde si cumple, roja si se excede), temas claro/oscuro.
- **Diseñado para uso real** — caché local (20 min para horas / 2 h para días), retroceso exponencial ante HTTP 429, renderizado consciente de huecos (los huecos rompen la línea — jamás se rellenan con 0), alineación UTC → hora local de la estación.

## Inicio rápido

### 1. Consigue una clave API (gratis, ~1 minuto)

1. Regístrate o inicia sesión en [OpenAQ Explorer](https://explore.openaq.org/register) (cuenta existente: [iniciar sesión](https://explore.openaq.org/login)).
2. Abre tu [página de cuenta](https://explore.openaq.org/account) — tu clave API aparece cerca del final; cópiala.
3. Configúrala — elige una:

```bash
export OPENAQ_API_KEY="your_key"                             # ephemeral / CI
echo 'OPENAQ_API_KEY=your_key' > ~/.config/air-chart/config  # persistent
```

No se requiere llavero del sistema — una credencial de servicio público y gratuita vive en un archivo de configuración en texto plano. Sin clave, el modo `--demo` aun así renderiza todo con datos de muestra.

### 2. Ejecuta

```bash
# Una ciudad, tendencia de PM2.5 a 7 días
./scripts/air_chart.sh --city Beijing --param pm25 --period 7d

# Comparación multiciudad (hasta 4 ciudades)
./scripts/air_chart.sh --city Tokyo --city Seoul --param pm25 --period 7d

# Una ciudad, multiparámetro (PM2.5 + PM10)
./scripts/air_chart.sh --city Beijing --param pm25 --param pm10 --period 30d

# Curva horaria de 48 horas (patrón día/noche)
./scripts/air_chart.sh --city Singapore --param o3 --period 48h

# Instantánea en barras de estaciones en tiempo real
./scripts/air_chart.sh --city Delhi --param pm10 --snapshot

# Tema oscuro, salida personalizada
./scripts/air_chart.sh --city London --param no2 --period 14d --theme dark -o london.svg
```

### 3. Instálala como skill de agente de IA

```bash
git clone https://github.com/qiakai/air-chart.git ~/.claude/skills/air-chart
# or: npx skills add qiakai/air-chart
```

Luego pídele a tu agente, por ejemplo: *«Compara el PM2.5 de Tokio y Seúl de los últimos 7 días».*

`SKILL.md` está escrito en inglés por compatibilidad con agentes y registros; hay una versión en chino en `SKILL.zh.md`. La salida de los gráficos admite `--lang en|zh|es|hi|ja|ko|fr` (por defecto se detecta del idioma del sistema).

## Referencia de CLI

| Flag | Description | Values |
| --- | --- | --- |
| `--city, -c` | Nombre de ciudad (repetible, ≤4) o coordenadas `"lat,lon"` | `Beijing`, `New Delhi`, `39.9,116.4` |
| `--param, -p` | Contaminante (por defecto `pm25`) | `pm25` `pm10` `o3` `no2` `so2` `co` |
| `--period, -t` | Rango temporal (por defecto `7d`) | `24h` `48h` (horario) · `7d` `14d` `30d` (diario) |
| `--snapshot` | Instantánea en barras de las estaciones activas de la ciudad | flag |
| `--theme` | Tema de color | `light` / `dark` |
| `--lang` | Idioma de salida (gráficos + mensajes) | `en` `zh` `es` `hi` `ja` `ko` `fr` (por defecto: autodetección del locale) |
| `--out, -o` | Descarga el gráfico como `.svg` o `.png` | por defecto: solo imprime la URL de x-cmd Draw |
| `--demo` | Modo demo, sin clave API | flag |

## Arquitectura

```text
[city / pollutant / time range]
   │
   ▼
geo_resolve.sh      city name → coordinates + timezone (built-in gazetteer / raw lat,lon)
   │
   ▼
openaq_client.sh    OpenAQ API v3: auth, User-Agent, md5 cache,
                    429 exponential backoff, liveness filter (24h/72h),
                    sensor match by fixed parameter ID, reference-grade first
   │
   ▼
data_transform.awk  cleaning (negatives / physically impossible spikes),
                    gap detection (breaks, never zero-filled), stats, local-time labels
   │
   ▼
render_draw.sh      x-cmd Draw URL builder (URL-as-Data; optional .svg/.png download)
```

`data/parameters.tsv` es un diccionario estático de parámetros alineado con los ID fijos de contaminantes de openaq-api: slug / param_id / nombre / unidad / guía 24 h de la OMS / tope físico / color por parámetro — sin viajes redundantes a `/parameters`. Los visuales siguen las convenciones de openaq-explorer: paleta por parámetro (PM2.5 `#E65100`, PM10 `#6A1B9A`, O3 `#0277BD`, NO2 `#00838F`), una paleta multiciudad apta para daltónicos y una línea de la guía OMS en verde de seguridad `#10B981` / rojo de alerta `#EF4444`. Si una estación reporta unidades distintas del valor por defecto del diccionario (p. ej. ppm), el eje Y usa las unidades reales y la línea OMS se suprime para evitar confusiones dimensionales.

## Códigos de salida

| Code | Meaning |
| --- | --- |
| 3 | Sin clave API configurada (imprime guía de configuración) |
| 4 | Error de red / API / reintentos de límite agotados |
| 5 | Sin estación activa o sin datos válidos |
| 2 | Nombre de ciudad irresoluble (imprime candidatos cercanos) |

## Licencia

MIT
