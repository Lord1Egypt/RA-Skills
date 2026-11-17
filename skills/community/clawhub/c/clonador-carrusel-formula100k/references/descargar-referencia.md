# Descargar la referencia desde un ENLACE (Instagram / TikTok)

> Objetivo: cuando el usuario pasa un **link** de un carrusel (en vez de una captura), la skill baja
> sola todas las slides como imágenes, las guarda en orden y las lee con visión.
> Esto resuelve el error clásico: alumna manda un enlace de IG → la skill esperaba una captura → no salía.

---

## 0. Detectar el tipo de entrada

- ¿El argumento es un **path/adjunto de imagen** (`.png`, `.jpg`, `.jpeg`, `.webp`)? → NO es link, ir directo a Read (PASO 1 del SKILL).
- ¿Empieza con `http` y contiene `instagram.com` / `tiktok.com`? → es ENLACE, seguir abajo.

Carpeta de trabajo (temporal, del scratchpad de la sesión):
```
$SCRATCH/carrusel-ref/
```
Crear la carpeta antes de descargar.

---

## 1. Instagram (por defecto = Apify directo)

Patrón F100K `feedback_ig_apify_default`: **para Instagram sin sesión, ir directo a Apify** (no intentar
agent-browser primero).

### 1.1 Obtener las URLs de imagen del carrusel

Usar el MCP de Apify. Cargar el tool con ToolSearch (`select:mcp__apify__call-actor,mcp__apify__fetch-actor-details,mcp__apify__get-dataset-items`) y llamar al actor **`apify~instagram-scraper`**:

Input mínimo:
```json
{
  "directUrls": ["<EL_LINK_DEL_POST>"],
  "resultsType": "details",
  "resultsLimit": 1,
  "addParentData": false
}
```

De la salida (dataset items), extraer las URLs de imagen del carrusel, en orden:
- Post carrusel → campo **`images`** (array de URLs) **o** **`childPosts[].displayUrl`** (una por slide).
- Post de imagen única → **`displayUrl`**.
- Si solo devuelve `videoUrl` (es un reel de video, no carrusel) → avisar al usuario:
  "Este post es un video, no un carrusel de imágenes. El clonador trabaja con slides."

> Si el actor pide login/cookies para ese post (privado), avisar y ofrecer el fallback (sección 3).

### 1.2 Descargar cada imagen en orden

```bash
mkdir -p "$SCRATCH/carrusel-ref"
# por cada URL i (empezando en 1):
curl -L -s -o "$SCRATCH/carrusel-ref/slide-$(printf '%02d' $i).jpg" "<URL_i>"
```

Verificar que se bajaron N archivos y que pesan > 0 bytes.

---

## 2. TikTok (slideshow / fotos)

TikTok tiene "photo mode" (carrusel de imágenes). Buscar en Apify Store un actor de **TikTok scraper**
que devuelva las imágenes del slideshow (p. ej. buscar `search-actors` con "tiktok"), y usar `directUrls`/`postURLs`
según su schema (revisar con `fetch-actor-details` antes de llamar).
Extraer las URLs de las imágenes del slideshow y descargarlas igual que en 1.2.

Si el link de TikTok es un video normal (no photo mode) → avisar que el clonador es para carruseles de imágenes.

---

## 3. Fallback — capturas de la usuaria (nunca navegador logueado)

Solo si Apify falla (post privado, sin red, o el actor no devuelve imágenes):

1. Pídele por Telegram una captura de cada slide, en orden.
2. Abrir el post.
3. Capturar la portada y avanzar el carrusel capturando cada slide (una captura por slide) a
   `$SCRATCH/carrusel-ref/slide-XX.png`.

Este es el **respaldo**, no el camino principal (Apify primero, por `feedback_ig_apify_default`).

---

## 4. Entregar al flujo normal

Cuando ya existan `slide-01.*`, `slide-02.*`, … en `$SCRATCH/carrusel-ref/`:
- Confirmar al usuario: *"Bajé N slides del post de @referente."*
- Leer cada una con **Read** (visión).
- Continuar en el **PASO 1** del SKILL (extraer ADN de estilo) con esas imágenes.
