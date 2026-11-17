# FLUJO DE TRABAJO OPTIMIZADO — SENDER INMERSIVO

Destilado del método del video de referencia (Design DNA + Design Loop), de las skills del
departamento (`sender-motion-kit`, `sender-design-ops`), de `nexu-io/open-design` como motor de
decisión, y de **8 loops reales ejecutados** en este proyecto. Es el flujo canónico para iterar
este sitio — y el molde para cualquier otro del portafolio.

## 0 · Actores y regla de oro

| Actor | Rol |
|---|---|
| **Persona** | Aprueba visual, provee assets reales, define la siguiente ronda (capturas > opiniones) |
| **Agente (Arena)** | Carga skills, ejecuta DNA→loop→build→deploy, mide con datos duros, documenta |
| **GitHub** | Fuente de verdad; Actions decide si se publica; Pages sirve |

**La persona aprueba; el agente ejecuta y mide; GitHub decide si se publica.**

## 1 · Activación (cada sesión)

1. Leer `AGENTS.md` (contrato) + `docs/SENDER-DESIGN-DNA.md` (autoridad de diseño).
2. Cargar skills: `sender-motion-kit/SKILL.md` (departamento, gates, patterns),
   `sender-design-ops/AGENTS.md` (reglas de construcción), `docs/SKILLS.md` (memoria del método).
3. Revisar `docs/DESIGN-REVIEW.md` → saber en qué loop quedó la última ronda y qué deuda hay.

## 2 · El flujo por ronda (gates propios, adaptados de motion-kit G0–G7)

```
G0 BRIEF/ASSETS    pedido + capturas/activos reales → se registra en DESIGN-REVIEW
G1 REFERENCIA      videos/repos de método → principios, jamás copia.
                   Referencias de la persona por link temporal (litterbox/tmpfiles/
                   onlyfiles): descargar YA (expiran), extraer frames con ffmpeg,
                   analizar (freezedetect para.motion, composición, paleta) y anotar
                   los principios en DESIGN-REVIEW antes de tocar código.
G2 DNA CHECK       toda pieza se justifica contra SENDER-DESIGN-DNA (anti-slop incluido)
G3 PROTOTIPO       el cambio mínimo que demuestra la idea (rama/commit por hito)
G4 DESIGN LOOP     render → inspección con datos duros (no capturas sueltas) → fix → re-render
                   (Chromium: escritorio + móvil táctil + reduced-motion; matriz de transform,
                   currentTime, contraste WCAG con el evaluador de sender/qa)
G5 APROBACIÓN      la persona ve frames/preview; nadie pasa de la escena héroe sin aprobar
G6 PERFORMANCE     sólo tras aprobación visual: pesos, lazy, degradaciones, Lighthouse
G7 SHIP + LOOP     commit por hito → push → Actions verde → verificación en producción →
                   anti-caché ?v=N → DESIGN-REVIEW actualizado → S24 de la persona
```

## 3 · Reglas que este proyecto ya pagó con errores (no repetir)

1. **Pages = hosting estático:** toda ruta nueva necesita shell en `scripts/seo.mjs` (ES y EN).
2. **Anchors crudos** siempre con `fullPath()` (base del deploy); `<Link>` con `path()`.
3. **Probar SIEMPRE el build con `VITE_BASE_PATH=/sender-immersive/`** — dev con base `/` esconde
   los 404 de producción.
4. **Font boosting de Chrome Android:** `text-size-adjust: 100%` — sin eso, columnas aplastadas.
5. **Táctil:** el film lleva control SIEMPRE visible (preload degradado + autoplay bloqueado es
   lo normal en datos móviles); red de seguridad temporal para mostrar el control.
6. **`prefers-reduced-motion`** (S24 «Quitar animaciones»): apaga decoración, nunca el contenido —
   el film queda disponible por decisión de la persona (botón), la foto sostiene la escena.
7. **Anti-caché:** cada ronda pública se verifica con `?v=N` (Pages cachea 10 min; el usuario
   ve lo viejo y reporta bugs ya arreglados).
8. **PAT mínimo** (fine-grained 7 días, un repo, Contents RW) + revocación al cerrar la ronda.
9. **Un solo SignalField, un contexto WebGL** (desktop fine-pointer), dispose al desmontar.
10. **Degradación sin huecos:** todo film corre ENCIMA de su foto real; si no carga, la foto +
    Ken Burns sostiene la escena.

## 4 · Pipeline de activos (§11–§14)

```
FOTO REAL (repo fuente / design-ops)
  ↓ verificación de identidad (frame a frame: ¿es la misma escena?)
FILM (profundidad + cámara + luz) ← videoteca del proyecto en sender-design-ops
  ↓ public/media/film-*.mp4 (lazy, preload none, IO play/pause)
CinematicImage(video=…) → film sobre foto → fade al reproducir → Ken Burns si no carga
```

Para films nuevos (fuera de este entorno): generar SOLO desde fotos reales de SENDER,
presupuesto <5 MB, H.264 MP4 (WebM opcional), y registrar el origen en TRACEABILITY.

## 5 · Los 5 comandos de cada ronda

```bash
npx tsc --noEmit && node qa/check.mjs            # QA mínimo
VITE_BASE_PATH=/sender-immersive/ npm run build  # build como producción
# loop renderizado (Playwright): datos duros por escena
git commit -m "hitoloop: qué y por qué (evidencia)"   # commit atómico por ronda
git push → Actions verde → verificar ?v=N en producción → DESIGN-REVIEW
```

## 6 · Estado y siguiente ronda

Vivo en `docs/DESIGN-REVIEW.md` (loops 01–08). Deuda priorizada: Lighthouse CI (G6 formal),
PROCESS (cuando haya contenido real), films en Proyectos/Productos con la videoteca restante,
components SectionMarker/TechnicalLabel, verificación S24 final.
