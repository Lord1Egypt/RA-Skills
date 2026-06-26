# cv-driven-job-hunter — skill para openclaw

Asistente proactivo de búsqueda laboral. A partir de un CV, calibra tu banda salarial real, escanea boards y career pages, scorea matches y acompaña todo el ciclo de postulación con seguimiento.

## Instalación

```bash
# Opción A — workspace local (precedencia más alta)
cp -r cv-driven-job-hunter /c/openclaw/skills/

# Opción B — compartido entre todos los agentes
cp -r cv-driven-job-hunter ~/.openclaw/skills/

# Opción C — registrar un directorio externo
# Editá ~/.openclaw/openclaw.json y agregá:
# {
#   "skills": { "load": { "extraDirs": ["/path/a/cv-driven-job-hunter/parent"] } }
# }

# Recargá:
openclaw gateway restart
# o simplemente:
/new

# Verificá que se cargó:
openclaw skills list | grep cv-driven-job-hunter
```

Las paths estándar de openclaw, en orden de precedencia:

| Path | Scope |
|---|---|
| `<workspace>/skills/` | per-agent del workspace |
| `<workspace>/.agents/skills/` | per-workspace agent |
| `~/.agents/skills/` | shared agent profile |
| `~/.openclaw/skills/` | shared (todos los agentes) |
| bundled | global |

## Setup inicial (una vez)

1. **Copiá la config plantilla y personalizala:**

   ```bash
   cd /c/openclaw/skills/cv-driven-job-hunter
   cp config.example.json data/config.json
   ```

   Editá `data/config.json` ajustando:
   - `candidate.salary` — tu min/target/stretch en USD mensuales
   - `candidate.preferred_titles` — los roles que te interesan
   - `candidate.deal_breakers` — qué no aceptás
   - `markets` — mercados que te interesa explorar
   - `platforms.*.enabled` — qué boards usar
   - `platforms.company_pages.companies` — empresas target

2. **Pasale tu CV al skill:**

   ```bash
   cp ~/Documents/mi-cv.pdf /c/openclaw/skills/cv-driven-job-hunter/data/cv.pdf
   ```

   O simplemente decile al agente "acá tenés mi CV" y pasalo en chat.

3. **(Opcional) Instalá deps de parsing en un venv aislado con versiones pinneadas:**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate    # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

   Solo necesario si tu CV está en PDF o DOCX. Si está en TXT/MD, no hacen falta.
   Las versiones pinneadas en `requirements.txt` están auditadas — actualizalas a conciencia, no automáticamente.

4. **Decile al agente:** "Hola, acabo de instalar cv-driven-job-hunter, mi CV está en `data/cv.pdf`, vamos."

   El agente va a:
   - Parsear el CV
   - Generarte el análisis de seniority + banda salarial real
   - Mostrarte gaps con tips para subir banda
   - Sugerir empresas target
   - Esperar tu OK antes de empezar a escanear

## Uso día a día

### Pedir un escaneo

> "Escaneá ofertas nuevas"

El agente corre `scan_queries.py`, fetchea las URLs de las plataformas habilitadas, scorea cada oferta nueva con `match_jobs.py`, y te presenta los top matches con call-to-action.

### Postular a una oferta

> "Postulemos a la 3"

El agente prepara CV adaptado + cover letter + crea registro en `applications.json` con status `drafted`. Vos hacés el submit final.

### Confirmar postulación enviada

> "Listo, postulé a {empresa}"

El agente actualiza el registro a status `submitted` y agenda los follow-ups.

### Pedir digest / status

> "Cómo va mi pipeline"

El agente corre `notify.py` y te muestra: matches calientes nuevos + follow-ups pendientes + estado del pipeline.

### Updates externos (entrevista, rechazo, oferta)

> "Me llamaron de Acme para entrevista técnica"

El agente actualiza el registro a `interview` con la nota.

### Repensar la estrategia

> "¿A cuánto puedo aspirar realmente con mi CV?"

El agente vuelve a correr `analyze_profile.py` y te muestra la banda actualizada + gaps en orden de ROI.

## Estructura del skill

```
cv-driven-job-hunter/
├── SKILL.md                      ← instrucciones para el agente
├── README.md                     ← este archivo
├── config.example.json           ← plantilla de config
├── data/                         ← estado persistente (gitignored si commiteás)
│   ├── config.json
│   ├── cv.pdf|docx|txt
│   ├── profile.json              ← generado por parse_cv.py
│   ├── analysis.json             ← generado por analyze_profile.py
│   ├── applications.json         ← tracking de postulaciones
│   ├── seen_jobs.json            ← dedup de ofertas
│   └── applications/{slug}/      ← drafts de CV/cover por postulación
├── references/
│   ├── job-boards.md
│   ├── world-class-companies.md
│   └── salary-benchmarks.md
├── templates/
│   ├── cover-letter.md
│   ├── cv-tailoring-prompt.md
│   ├── application-record.schema.json
│   └── notification-message.md
└── scripts/
    ├── parse_cv.py
    ├── analyze_profile.py
    ├── match_jobs.py
    ├── track_applications.py
    ├── scan_queries.py
    └── notify.py
```

## Privacidad e higiene de datos

- `data/cv.*`, `data/profile.json`, `data/applications.json`, `data/seen_jobs.json` contienen info personal. **Si versionás este skill, mantené `data/` fuera del repo** (este repo ya tiene un `.gitignore` que cubre los archivos generados).
- El skill no manda nada por red por sí mismo. El agente usa sus tools (WebFetch/browser) y vos ves cada llamada en la sesión.
- **Nunca pongas tokens/credenciales en `config.json`.** Si necesitás credenciales (ej: API keys de boards), usalas via `env` o el sistema de secretos de openclaw.
- **No instales el skill en un perfil compartido entre múltiples usuarios** — el `data/` queda accesible para todos los agentes en ese scope. Para CV personal, usá scope per-workspace o per-agent.
- **Revisá `data/seen_jobs.json` periódicamente** (cada 4-6 semanas o si los digests parecen raros). Una entry corrupta o un dedup mal hecho puede suprimir matches futuros. Si dudás, borralo — el peor caso es re-ver ofertas viejas una vez.
- **Reseteá `data/profile.json`** si tu CV cambia mucho (cambio de stack, salto de seniority): borralo y volvé a parsear desde el CV nuevo. Un profile stale arrastra scoring impreciso por muchas scans.
- **Las búsquedas que hacés se loggean en los boards externos** (LinkedIn, Indeed, etc.). Mantené los queries y filtros en `config.json` mínimos — no metas info que no quieras que esos sites tengan.

## Seguridad del scoring

- `match_jobs.py` solo acepta `--job-file <path>` o `--stdin` para el JSON del job. **No existe `--job '<json>'`** — los postings vienen de fuentes externas y un campo con comillas/backticks/control chars podría romper el quoting del shell. El agente debe escribir el JSON a un archivo temporal antes de scorearlo.

## Troubleshooting

**El agente no detecta el skill:**
- Verificá que `SKILL.md` esté en la raíz del directorio del skill
- Confirmá la ubicación con `openclaw skills list`
- Revisá frontmatter del `SKILL.md` — el `name` debe matchear el nombre del directorio

**`parse_cv.py` falla con "Falta pdfminer.six":**
- `pip install pdfminer.six python-docx`
- O convertí el CV a TXT/MD antes de pasarlo

**El score de los matches parece bajo aún para ofertas perfectas:**
- Probablemente el `profile.json` no detectó bien tus skills. Abrilo y agregá manualmente las que falten.
- O bajá `scan.min_match_score` en config si querés ver más opciones.

**LinkedIn bloquea fetches:**
- Es esperable, LinkedIn tiene anti-scraping fuerte. El agente debería darse cuenta y pasarte los URLs para que abras vos.
- Considerá usar la app oficial de LinkedIn con búsquedas guardadas, y delegar a cv-driven-job-hunter solo el resto de boards.

**Quiero agregar un board nuevo:**
1. Editá `references/job-boards.md` con la URL/método de extracción
2. Agregá un handler en `scripts/scan_queries.py` siguiendo el patrón existente
3. Agregá la entrada al `config.example.json` y a tu `data/config.json`

## Calibración

Las bandas salariales en `references/salary-benchmarks.md` son una foto de mercado 2026-Q1. **Recalibralas cada 6 meses** cruzando con:

- [levels.fyi](https://levels.fyi)
- [Repvue](https://repvue.com)
- "Who is hiring?" mensual de HN
- Surveys (Stack Overflow, JetBrains)

Si ves divergencia significativa entre lo que el skill predice y lo que el mercado paga, ajustá los rangos en `salary-benchmarks.md` y los modificadores en `analyze_profile.py`.

## Limitaciones conscientes

- **No auto-aplica.** Diseño explícito — el usuario submitea manualmente. El skill prepara material y agenda follow-ups.
- **No accede a tu inbox.** No leemos email, no respondemos a recruiters por vos. Si querés ese loop, conectalo separadamente vía un canal de openclaw + un skill aparte.
- **Heurísticas, no ML.** El scoring es reglas explícitas. Si querés algo más sofisticado (LLM-based ranking), reemplazá `match_jobs.py` con una versión que llame a un modelo. La interfaz se mantiene.
- **Sin garantía de precisión salarial.** Los números son orientativos. La negociación real depende de mil factores fuera de este skill.
