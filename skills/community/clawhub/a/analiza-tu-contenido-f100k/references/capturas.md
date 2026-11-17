# Las capturas de estadísticas avanzadas

El panel del computador da las **básicas** (vistas, % de no seguidores, interacciones, seguidores).
Las **avanzadas** solo están en la **app del teléfono**, y sin ellas dos de los 5 filtros quedan sin dato:

| Captura | Qué tiene que verse | Columnas en `datos.json` | Desbloquea |
|---|---|---|---|
| **Retención** | la gráfica por segundo, la **tasa de omisión** y el **tiempo de visualización promedio** | `retencion_3s` = 100 − tasa de omisión · `duracion_media` (s) | Filtro 2: ¿el problema es el gancho o el desarrollo? |
| **Actividad en el perfil** | **visitas al perfil**, **toques en enlaces externos** (y seguidores) | `visitas_perfil` · `toques_enlace` · `dms` (los cuenta ella) | Filtro 5 · Intención: corona el ángulo de venta y permite armar campaña |
| Básicas (solo si no hay Composio) | Visualizaciones con **Seguidores / No seguidores** (%) · me gusta, comentarios, **compartidos**, **guardados** · seguidores | `vistas` · `pct_no_seguidores` · `guardados` · `compartidos` · `seguidores_nuevos` | Filtros 1, 3 y 4 |

## Cuántas

- **Mínimo para leer un filtro:** 5 Reels de «este mes» y 5 de la línea base con ese dato. Con 2 sueltas no hay mediana y el motor lo deja sin dato.
- **Ideal:** los 30.
- **Por dónde empezar:** los 5 más recientes y, en la base, los que quedaron en ORO y CHATARRA (los que enseñan). El motor los lista en `calidadDatos.avanzadas[].prioridad` y el informe los muestra en «Tu data».

## El mensaje para pedirlas (cópialo y cambia los números)

> Para leer tu cuenta completa necesito 2 capturas por Reel **desde la app del teléfono** (el computador no las trae).
> Abre el Reel → **Ver estadísticas** y haz scroll:
> 1. **Retención**: que se vea la gráfica, la tasa de omisión y el tiempo de visualización promedio.
> 2. **Actividad en el perfil**: que se vean las visitas al perfil y los toques en enlaces.
> Empieza por estos 10: #1, #2, #3… (si puedes, después el resto).
> Mándamelas por aquí y escribe en el pie de cada foto el número del Reel y una letra: `01a` (retención), `01b` (perfil). El 01 es el más reciente.
> Si contaste los DMs que te trajo algún Reel, dímelo también.

## Al leerlas

- Lee cada imagen con Read y copia el número tal cual (sin redondear).
- Captura cortada, borrosa o de otro Reel = `null`. Lo que no se ve no se inventa.
- «Actividad en el perfil» agregada del panel web **no** es intención (en la cuenta medida era idéntica a «Seguidores nuevos»): solo vale el desglose de la app.
