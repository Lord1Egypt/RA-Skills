# Flujo de trabajo: sitio inmersivo en repo paralelo (`sender-immersive`)

Complemento de `FLUJO-DE-TRABAJO.md` (el flujo maestro Arena AI + GitHub + Samsung S24).
Este documento registra la variante usada para construir y publicar
**sender-immersive** — ENGINEERING THE SIGNAL — y sirve para repetirla.

**Sitio publicado:** https://cristianoleamiranda-dotcom.github.io/sender-immersive/

---

## 1. Topología del proyecto

| Repositorio | Rol en el flujo |
|---|---|
| `sender` | **Fuente de verdad**: hechos, textos, fotos, video, catálogo. Su `src/content/catalog.ts` es el catálogo auditado. Su `docs/proyecto/` guarda la memoria del proyecto (este archivo, el flujo maestro, inventario, seguridad). |
| `scroll-craft` | **Fábrica de ramas-skill**: cada sesión de agente construye en una rama `arena/*` aislada. `main` queda intacto. |
| `sender-immersive` | **Producto publicado**: solo se recibe árbol aprobado + `AGENTS.md` (contrato operativo) + `docs/AUDITORIA-INMERSIVA.md`. Pages por Actions. |
| `sender-motion-kit` / `sender-design-ops` | Skills y criterios (DNA): scroll como transporte, presupuesto WebGL, anti-plantilla. |

Regla que se mantuvo: **la persona aprueba, el agente ejecuta y mide, GitHub decide si se publica.**

## 2. El flujo, etapa por etapa

```
brief ──► rama-skill en scroll-craft (agente aislado)
              │  construye + QA local (tsc, qa/check.mjs, build)
              ▼
      paquete de entrega (estado verificado + encargo + prohibiciones)
              ▼
      sesión de publicación + PAT mínimo de duración corta
              │  push fast-forward a sender-immersive@main
              ▼
      GitHub Actions: build + Pages (~1 min)
              ▼
      auditoría: repo QA + Chromium renderizado + WCAG + cruce de hechos
              ▼
      verificación final en S24 (flujo maestro §S24)
```

1. **Construir** en rama `arena/*` de `scroll-craft`. Nunca en `main`.
2. **Empaquetar**: documento con estado verificado por comando (qué existe, qué no se
   puede inventar, encargo listo para pegar). El paquete de esta web incluyó el ZIP
   de la rama, las prohibiciones (no copiar sender-onair/open-design/videos) y los
   datos de contacto verificados.
3. **Publicar**: sesión con credencial mínima.
4. **Auditar** (ver `sender-immersive/docs/AUDITORIA-INMERSIVA.md`): QA del repo +
   navegador real en tres contextos + WCAG con el evaluador de `sender/qa` +
   cruce de hechos contra `sender`.
5. **Verificar en S24**: táctil, scroll, hero, WhatsApp/`tel:`, ruta profunda compartida.

## 3. Seguridad (lo aprendido a la dura)

- PAT **fine-grained**, expiración ≤ 7 días, un solo repo, permiso **Contents: Read/Write**
  (o clásico con scope `repo` si se necesita activar Pages por API).
- Dos intentos con fine-grained quedaron **read-only** (403 en push sin modificar la
  API de lectura): verificar siempre el permiso de escritura antes de culpar al flujo.
- El token pasa por credential helper **en memoria** (`git -c credential.helper=…`),
  nunca a `.git/config` ni al disco. Se revoca al terminar, siempre.
- Nada de secretos dentro de los repos: la memoria del proyecto (estos documentos)
  documenta el proceso, no las credenciales.

## 4. Las tres trampas de esta variante

1. **Pages es hosting estático**: toda ruta nueva necesita su shell en
   `scripts/seo.mjs` (ES **y** EN) o cae a 404 en acceso directo. El `404.html`
   es el fallback: base del repo + redirects estáticos de legado (`/soluciones`).
2. **El README y la LICENSE del repo destino mandan**: el árbol que llega de la
   rama-skill puede traer README corrupto (un YAML aplanado) o licencia distinta;
   se conservan la licencia del repo publicado y un README documentado.
3. **El preview ≠ producción**: probar el build con las variables del workflow
   (`VITE_BASE_PATH=/sender-immersive/`) antes de pushear.

## 5. Checklist de publicación

- [ ] QA local: `npx tsc --noEmit` + `node qa/check.mjs` + `npm run build`
- [ ] Commit atómico, push **fast-forward** (sin `--force`, jamás)
- [ ] Actions en verde y home HTTP 200 en producción
- [ ] Una ruta profunda ES y una EN HTTP 200 con título correcto
- [ ] `/soluciones/` redirige; formulario abre el correo; contacto exacto
- [ ] Auditoría renderizada (3 contextos + WCAG) sin hallazgos abiertos
- [ ] PAT revocado
- [ ] Verificación final en S24
