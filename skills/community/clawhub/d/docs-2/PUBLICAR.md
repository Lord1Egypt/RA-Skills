# Publicar el sitio inmersivo en GitHub Pages

Todo el trabajo técnico está hecho y verificado. Falta **una sola cosa**: la
credencial para empujar. Este documento es el camino más corto hasta la URL.

---

## Destino

| | |
|---|---|
| Repositorio | `cristianoleamiranda-dotcom/sender-immersive` (público, Pages ya activo) |
| Rama de trabajo | `immersive-redesign` (ya existe; aquí va la reconstrucción) |
| Rama intacta | `main` — sigue sirviendo el sitio publicado actual |
| URL en vivo | `https://cristianoleamiranda-dotcom.github.io/sender-immersive/` |
| Despliegue | `.github/workflows/pages.yml` (`workflow_dispatch` desde la rama) |

**El repositorio no se rompe.** `main` no se toca, y el despliegue se lanza
desde `immersive-redesign`. Si algo no gusta, volver atrás es:

```bash
gh workflow run pages.yml --repo cristianoleamiranda-dotcom/sender-immersive --ref main
```

---

## Camino A — 3 minutos (recomendado)

### 1. Crear el token

Abre este enlace (repositorio y permisos ya vienen marcados):

**https://github.com/settings/personal-access-tokens/new?name=SENDER+Pages&expires_in=7&description=Publicar+el+sitio+inmersivo&target_name=cristianoleamiranda-dotcom&contents=write&actions=write**

Comprueba que dice:

- **Repository access** → `Only select repositories` → `sender-immersive`
- **Permissions → Repository permissions**
  - `Contents` → **Read and write**
  - `Actions` → **Read and write**
- **Expiration** → 7 días (este proyecto ya trabaja así; ver `SEGURIDAD.md`)

Pulsa **Generate token** y copia el valor (`github_pat_…`). Sólo se muestra una
vez.

### 2. Publícalo

En el chat, pega el token. Yo ejecuto:

```bash
GITHUB_TOKEN=github_pat_… bash scripts/publicar.sh
```

Eso clona, aplica el árbol sobre `immersive-redesign`, hace los **12 commits por
hito**, empuja y lanza el despliegue.

### 3. Revócalo

Cuando la URL funcione, borra el token en
`https://github.com/settings/tokens?type=beta` (botón *Delete*). El sitio sigue
publicado: el token sólo sirve para empujar, no para servir.

---

## Camino B — hacerlo tú, sin darme el token

Descarga el proyecto desde este workspace y, en tu máquina:

```bash
cd /ruta/al/proyecto
npm install
GITHUB_TOKEN=github_pat_… bash scripts/publicar.sh
```

Las credenciales nunca pasan por aquí.

---

## Camino C — todo por interfaz web (sin token, más lento)

1. Descarga el proyecto del workspace.
2. En tu máquina: `npm install && npm run build:pages`.
3. En GitHub, entra en el repo → rama `immersive-redesign` → **Add file** →
   *Upload files*.
4. Sube **el contenido de `dist/`** (no la carpeta), en dos tandas si hacen
   falta: GitHub acepta 100 archivos por subida.
5. Commit. Pages publica en la URL de arriba.

Este camino sube el sitio **compilado**, no el código fuente: funciona igual,
pero los 12 commits por hito no se ven y el workflow no reconstruye nada.

---

## Trampas del entorno de despliegue

Dos fallos costaron dos intentos de publicación, y ninguno era del sitio. Quedan
anotados porque son reglas del repositorio, no del código:

**1. El entorno `github-pages` solo permite desplegar desde `main`.**
El repositorio trae una regla de ramas en el entorno, y cualquier despliegue
desde otra rama muere con el trabajo de despliegue **en cero pasos** y sin
registro. Se arregla añadiendo la rama a las políticas:

```bash
curl -X POST -H "Authorization: Bearer $GITHUB_TOKEN" \
  https://api.github.com/repos/cristianoleamiranda-dotcom/sender-immersive/environments/github-pages/deployment-branch-policies \
  -d '{"name":"immersive-redesign","type":"branch"}'
```

Es **aditivo**: `main` sigue permitida. Quitarla es un `DELETE` sobre la misma
ruta con el `id` de la política.

**2. `git add` con rutas concretas no registra eliminaciones.**
El primer intento dejó el `src/` del sitio anterior conviviendo con el nuevo y
el compilador de CI intentó compilar los dos. El generador de hitos ahora retira
del índice lo que el árbol ya no tiene (`git ls-files --deleted`) y, al final,
**comprueba que el árbol confirmado coincide con el de trabajo** y falla si no:
un fallo silencioso aquí se convierte en un despliegue roto allá.

## Después de publicar — qué comprobar

En `https://cristianoleamiranda-dotcom.github.io/sender-immersive/`:

- [ ] La raíz redirige a `/es/` y el conmutador lleva a `/en/`.
- [ ] La escena 00 hace *scrub* del video con el scroll.
- [ ] Ningún enlace interno se sale del subdirectorio (lo típico: un `/contacto`
      que apunta a `usuario.github.io/contacto`).
- [ ] Abrir `/sender-immersive/es/` **directamente** en una pestaña nueva: sin
      `es/index.html` real esto daría 404; el post-compilado lo genera.
- [ ] En móvil, la torre del hero queda dentro del encuadre.
- [ ] El HTML servido (no el DOM) declara la canónica del sitio publicado y no
      la de otro dominio: `curl -s URL/es/ | grep canonical`.

Si el despliegue falla, el registro está en
`https://github.com/cristianoleamiranda-dotcom/sender-immersive/actions`.

---

## Lo que ya está verificado en local

Bajo el simulador de Pages (`node scripts/serve-pages.mjs 8899`, que responde a
`Range` con 206 como el servidor real):

```
/     → /sender-immersive/es/     canonical ✓  hreflang es-CL/en/x-default ✓
/es/                              canonical ✓  8 escenas · 7 imágenes · 0 rotas
/en/                              canonical ✓  html lang="en"
video                             4/4 · 12,0 s · 1920×1080
respuestas 4xx/5xx                ninguna
errores de consola                ninguno
```

Ayer quedaban dos fallos sin diagnosticar. Eran tres cosas reales:

1. **`hero-poster-960.webp` daba 404.** Los pósters del hero se habían perdido al
   limpiar `public/media/` antes de optimizar, y el optimizador no los
   regeneraba. Ya están de vuelta **dentro del pipeline**, para que no vuelva a
   pasar.
2. **`favicon.svg` y `apple-touch-icon.png` no existían** pero el HTML los
   declaraba. Ahora existe el favicon —el mástil con su frente de onda, la misma
   figura que gobierna la escena 01— y su PNG de 180 px.
3. **`sender-hero.mp4 (net::ERR_ABORTED)`** era el simulador antiguo, que no
   entendía `Range`. Con `serve-pages.mjs` el video carga entero.

---

## Advertencia sobre el repositorio de destino

`sender-immersive` ya aloja **otro sitio publicado** («ENGINEERING THE SIGNAL»,
con Instrument Sans), y su `AGENTS.md` dice que *«la experiencia ya está
resuelta; los cambios son quirúrgicos»*. Esta reconstrucción es lo contrario: se
hizo desde cero, con otra tipografía y otra arquitectura.

El script está escrito para convivir con eso:

- **Se conservan** `AGENTS.md`, `LICENSE`, `.github/` (el workflow que publica) y
  el `docs/` del destino, que se fusiona en lugar de reemplazarse.
- **Se sustituye** la aplicación: `src/`, `public/`, `assets/`.
- **Se retira** el `qa/` anterior (el QA vive ahora en `scripts/`).

El cambio son ~195 archivos nuevos y 2 retirados. Está probado contra una copia
del repositorio: nada de lo que el destino quiere conservar se pierde.
