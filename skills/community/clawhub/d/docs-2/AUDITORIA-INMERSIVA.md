# SENDER-IMMERSIVE — AUDITORÍA INMERSIVA · FASE 1

**Repo:** `cristianoleamiranda-dotcom/sender-immersive`
**Commit auditado:** `83e3d4f` (incluye las correcciones que la propia auditoría disparó)
**Fecha:** 2026-09-29
**Método:** inventario por comando + navegador real (Chromium headless vía Playwright, escritorio / móvil táctil / reduced-motion) + evaluador de contraste WCAG 2.1 AA de `sender/qa/contrast.mjs`.

---

## 1. Veredicto en una línea

El sitio está **sólido y en producción**: cero errores de consola en tres contextos, rutas profundas completas, hechos verificados uno a uno contra la fuente, y el único defecto real encontrado (contraste de rótulos azules sobre gris oscuro) fue corregido y re-verificado en el mismo día.

## 2. Inventario verificado por comando (no de memoria)

| Control | Resultado |
|---|---|
| `npx tsc --noEmit` | OK, sin errores |
| `node qa/check.mjs` | `translations, palette, assets, alt text, seo shell — ok` |
| `npm run build` (con env del workflow) | 50 URLs, 49 shells estáticas |
| Rutas con shell | ES + EN completas, incluidos 7 categorías y 16 productos × 2 idiomas |
| Compresión / caché | gzip activo, `max-age=600` (GitHub Pages) |

## 3. Auditoría renderizada (Chromium, sitio en producción)

| Contexto | Resultado |
|---|---|
| Escritorio 1440×900 | Título exacto ES, sin `vite-error-overlay`, 0 errores de consola antes y después de scroll completo |
| Móvil táctil 390×844 (perfil S24) | Título exacto, 12 canvas 2D (Three.js correctamente ausente), 0 errores |
| `prefers-reduced-motion: reduce` | 0 errores, carga normal |
| Rutas `/productos/`, `/producto/serie-sender-ss/`, `/en/`, `/en/productos/`, `/en/producto/serie-sender-ss/` | HTTP 200, overlay ausente, 0 errores |
| `/soluciones/` | Redirige a `/productos/` en navegador real (fallback `404.html`) |
| El histórico "Tira error" | **No se reproduce** (tampoco en scroll agresivo automatizado) |

## 4. Verificaciones de hechos (regla: no inventar)

| Hecho | Resultado |
|---|---|
| Slugs del catálogo | 23/23 **idénticos** a `sender/src/content/catalog.ts` |
| AM-2500SS | 2000 W, confirmado en el repo fuente |
| Contacto | `tel:+56983864148`, `mailto:sender@sender.cl`, `mailto:bis.ltda@gmail.com`, `wa.me/56983864148`, Blanco Viel 1108 — exactos; **0 enlaces a redes sociales** |
| Formulario | Compone el correo en el cliente; no almacena nada |

## 5. Contraste WCAG 2.1 AA (con el evaluador de la casa)

**Hallazgo original:** 5 muestras bajo mínimo. Revisadas una a una con captura dirigida:
- **Falsos positivos:** botones inactivos de Ingeniería (viven en columna blanca) y marca del nav.
- **Fallas reales:** kickers y rótulos mono en `--signal`/`--cyan` sobre fondo `#494949` (Contacto, Proyectos, Hero) y `figcap` de la figura `.depth` (Nosotros), gris sobre gris.

**Corrección (`83e3d4f`):** en contexto oscuro (`[data-theme="dark"]`) los rótulos pasan a blanco y la `figcap` de `.depth` a blanco translúcido. Los azules de marca quedan reservados a fondo claro — convención que el sitio ya usaba en `.eng-index button.is-active`.

**Re-auditoría:** **0 muestras bajo mínimo** en la home completa. Verificado también visualmente.

## 6. SEO

- Títulos ES/EN exactos del brief en `<title>` y `og:title`, por ruta e idioma.
- `sitemap.xml` servido: 50 URLs hacia el Pages.
- **Decisión de marca a registrar:** `canonical`, `hreflang` y `robots.txt` apuntan a `www.sender.cl` — el Pages no compite con el sitio principal en buscadores. Si algún día se quiere indexar el Pages, regenerar con `VITE_SITE_URL` + robots propios.

## 7. Deuda conocida restante

1. Métricas Lighthouse/rendimiento aún no ejecutadas (presupuesto: el bundle Three vive en chunk aparte y se importa solo en escritorio).
2. La verificación final de **siempre** es en dispositivo real: S24 táctil, WhatsApp/`tel:`, video del hero (ver `sender/docs/proyecto/FLUJO-DE-TRABAJO.md`).
3. Fuente de las 4 referencias de movimiento: principios estudiados, no copia (ver `AGENTS.md` §referencias).
