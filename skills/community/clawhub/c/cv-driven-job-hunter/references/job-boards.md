# Job boards — referencia operativa

Este archivo es el catálogo del que `scan_queries.py` y el agente toman URLs y reglas de extracción. Cuando agregues un board nuevo, registralo acá.

## Globales / USD

### LinkedIn Jobs
- **URL base de búsqueda:** `https://www.linkedin.com/jobs/search/?keywords={query}&f_WT=2&f_TPR=r604800`
- **Flags útiles:** `f_WT=2` = remoto; `f_TPR=r604800` = posteado última semana; `f_SB2=4` = $100k+ (US)
- **Cómo extraer:** WebFetch al search URL, parsear cards (título, empresa, ubicación, link). El detalle de la oferta requiere ir al link individual.
- **Fricción:** anti-scraping fuerte. Si bloquea, generale al usuario el link directo para que vea él mismo.
- **Easy Apply:** detectable por presencia del badge en el HTML de la oferta. Útil para ofertas que se postulan sin abandonar LinkedIn.

### RemoteOK
- **API JSON pública:** `https://remoteok.com/api`
- **Filtro por tag:** `https://remoteok.com/remote-{tag}-jobs` o filtrar el JSON por `tags`
- **Sin auth.** Devuelve array con: `id`, `position`, `company`, `tags`, `salary_min`, `salary_max`, `url`, `date`.
- **Ideal para:** scan automático de alta señal. Usar como primera fuente.

### WeWorkRemotely
- **URL base:** `https://weworkremotely.com/categories/remote-programming-jobs`
- **RSS:** `https://weworkremotely.com/categories/remote-programming-jobs.rss` — la opción más limpia
- **Sin salario expuesto** la mayoría — flaggear cuando aplique.

### Wellfound (ex-AngelList)
- **URL base:** `https://wellfound.com/jobs`
- **Filtros vía query params:** `remote=true`, `salary_min=`, `role=` (slug)
- **Requiere auth para detalles completos.** Sin login, solo se ve el resumen. Recomendarle al usuario que abra el link manualmente para ver el equity y rango exacto.

### Hacker News "Who is hiring"
- **URL del thread mensual más reciente:** ir a `https://news.ycombinator.com/submitted?id=whoishiring` y tomar el último post titulado "Ask HN: Who is hiring?"
- **Alta señal** — empresas tech serias, comments individuales son la oferta.
- **Filtrar por:** "REMOTE" en el primer paréntesis del comment.
- **Sin tracking nativo.** El agente debe deduplicar por contenido del comment.

### Y Combinator Work at a Startup
- **URL base:** `https://www.workatastartup.com/jobs`
- **Requiere login YC.** Si el usuario tiene cuenta, le pasamos URLs filtradas. Si no, saltarlo.

## LATAM

### Get on Board
- **URL base:** `https://www.getonbrd.com/search-jobs/category/programming/remote/yes`
- **Query params:** `q=`, `salary=` (rango), `seniority=`
- **Salarios casi siempre expuestos en USD para roles remotos.** Excelente señal.

### Torre.co
- **API:** `https://torre.co/api/entities/_searchStream` (POST con body JSON)
- **Filtros:** `remote=true`, `compensation` rango.
- **Devuelve perfiles + ofertas.** Para ofertas, filtrar por `subjectType: "job"`.
- **Ideal para roles "world class" para LATAM** (cross-border).

### Workana
- **URL base:** `https://www.workana.com/jobs`
- **Mayormente freelance/proyectos**, no empleos full-time. Habilitarlo solo si el usuario quiere freelance.

### Empleos.clarin / Bumeran / Computrabajo
- **Volumen alto, calidad heterogénea.** Habilitar solo si el usuario busca on-site/local en Argentina, México, Colombia, etc.
- **Filtros agresivos** son críticos para evitar ruido.

## Europa / España

### LinkedIn (filtros UE)
- Usar el mismo base con `geoId=` específicos: España = `105646813`, Alemania = `101282230`, Portugal = `100364837`.
- `f_WT=2` para remoto.

### Honeypot.io
- **URL:** `https://www.honeypot.io/`
- **Modelo invertido**: las empresas postulan al candidato. Vale la pena registrarse y dejar el perfil activo, no scrapeable como board normal.

### Welcome to the Jungle
- **URL:** `https://www.welcometothejungle.com/en/jobs?query=&refinementList%5Bremote%5D%5B0%5D=fulltime`
- **Buena UX y descripciones detalladas.** Ideal para empresas EU mid/large.

### Otta (parte de Welcome to the Jungle)
- **URL:** `https://app.otta.com/`
- **Curado, alta señal**, requiere registro pero ofrece daily digest interno.

## Especialistas / nichos altos

### Levels.fyi (jobs)
- **URL:** `https://www.levels.fyi/jobs/`
- **Solo tech roles, salarios totales (base + equity + bonus) expuestos.** Estándar oro para benchmarks.

### Crypto Jobs List, Web3 Career
- **Solo si** el usuario explícitamente quiere crypto/web3. Si está en `deal_breakers`, saltar.

### Triplebyte (cuando esté disponible)
- Modelo de assessment + matching. Vale la pena si el usuario quiere bypass al funnel tradicional.

## Reglas de scraping responsable

1. **Respetar robots.txt** — RemoteOK, WWR, Get on Board permiten scraping; LinkedIn no.
2. **Throttling:** mínimo 2s entre requests al mismo dominio.
3. **User-Agent identificable** (no spoof de browser real). Fallback: si el sitio bloquea, pedirle al usuario que abra el link manualmente.
4. **Cache local:** `data/seen_jobs.json` evita re-procesar. TTL de re-fetch para detalles de oferta: 7 días.

## Cómo agregar un board nuevo

Editá `scan_queries.py` agregando un handler que reciba `(profile, config)` y devuelva una lista de `{"platform": str, "url": str, "method": "fetch"|"api"|"rss"}`. Documentá el formato de respuesta esperado en este archivo.
