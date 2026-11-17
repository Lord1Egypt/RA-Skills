# Patrones para integrar fotos reales del usuario

Cómo incluir fotos personales (el usuario u otra) en los slides sin romper el brandkit scrapbook.

> **Regla maestra:** la foto es UN elemento más del collage, no el protagonista que aplasta todo. Sigue conviviendo con post-its, washi tape, stickers y doodles.

---

## CARPETAS DEFAULT DE FOTOS

| Carpeta | Cuándo usar |
|---|---|
| `cerebro/fotos` | 3-5 fotos curadas del usuario, default si no especifica otra. Tags conocidos. Más rápido. |
| `cerebro/fotos` | Pool grande sin tags. Variedad de poses/contextos. Usar cuando haga falta variedad. |

> Si ninguna de las dos carpetas existe en la máquina del usuario, **pregúntale dónde tiene sus fotos**. No inventes rutas.

**Antes de usar una foto:**
1. `Read` la foto para verificar qué muestra (cara, pose, fondo, vestuario)
2. Elegir la que mejor calce con el tono del slide
3. Copiar la foto a la carpeta de output con nombre simple (`foto.jpg`, `slide-3-foto.jpg`) → el `<img>` usa ruta relativa

---

## PATRÓN 1 — POLAROID (recomendado para portada y testimonios)

**Cuándo:** slides personales, intros, "esto es mío", testimonios, presentaciones.

**Look:** foto con borde blanco grueso, leve rotación, sombra dramática, caption handwritten abajo. Como recorte de álbum.

```html
<div class="polaroid">
  <img src="foto.jpg" alt="">
  <div class="caption">~ creadora indie ~</div>
</div>
<!-- washi tape encima del polaroid (fuera del div para z-index limpio) -->
<div class="tape tape-poL"></div>
```

```css
.polaroid {
  position: absolute;
  top: 420px; left: 70px;
  width: 470px;
  background: #FCFAF3;
  padding: 22px 22px 78px 22px;       /* extra abajo para caption */
  box-shadow: 0 22px 44px rgba(0,0,0,0.20),
              0 6px 12px rgba(0,0,0,0.12);
  transform: rotate(-3.5deg);          /* siempre ±2°-±5° */
  z-index: 2;
}
.polaroid img {
  width: 100%; height: 520px;
  object-fit: cover; display: block;
  filter: contrast(1.02) saturate(1.05);
}
.polaroid .caption {
  position: absolute; bottom: 22px; left: 0; right: 0;
  font-family: 'Caveat'; font-weight: 600;
  font-size: 40px; text-align: center;
  color: #2B2218;
}
.tape-poL {
  position: absolute; top: 388px; left: 130px;
  width: 130px; height: 32px;
  background: rgba(143,175,138,0.65);
  transform: rotate(-14deg); z-index: 5;
  border-left: 1px dashed rgba(0,0,0,0.10);
  border-right: 1px dashed rgba(0,0,0,0.10);
}
```

**Reglas:**
- Caption siempre handwritten (Caveat) y entre tildes "~ texto ~"
- Sombra dramática (no plana) — da peso de objeto físico
- Rotación entre ±2° y ±5°, nunca más
- Width recomendado: 440-500px (suficiente para que la foto respire pero deje espacio para post-its/texto al lado)

---

## PATRÓN 2 — HERO BACKGROUND (foto fill + overlay)

**Cuándo:** slide impactante con UNA frase fuerte. Cuando la foto en sí es el contenido (gancho visual). Tipo cover de revista.

**Look:** foto cubre el slide entero, con overlay translúcido para legibilidad del texto encima.

```html
<div class="slide hero">
  <div class="hero-bg" style="background-image: url('foto.jpg');"></div>
  <div class="hero-overlay"></div>
  <div class="hero-content">
    <h1 class="hero-title">Mis top 5 películas <span class="red">de terror</span></h1>
    <!-- post-its / lista encima -->
  </div>
  <!-- handle, tape, stickers -->
</div>
```

```css
.hero { position: relative; overflow: hidden; }
.hero-bg {
  position: absolute; inset: 0;
  background-size: cover;
  background-position: center;
  filter: contrast(1.05) saturate(1.05);
}
/* Overlay crema semitransparente para mantener brandkit + legibilidad */
.hero-overlay {
  position: absolute; inset: 0;
  background:
    linear-gradient(180deg, rgba(245,239,224,0.85) 0%, rgba(245,239,224,0.55) 40%, rgba(245,239,224,0.85) 100%),
    url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='200' height='200'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='2' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 0.2  0 0 0 0 0.15  0 0 0 0 0.1  0 0 0 0.06 0'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>");
}
.hero-content { position: relative; z-index: 2; }
```

**Reglas:**
- Overlay SIEMPRE crema (`#F5EFE0`) al 55-85% — nunca negro/oscuro (rompe el brandkit)
- Mantener la textura noise también encima del overlay para no perder la sensación de papel
- Texto encima: usar fondos sólidos (post-it, caja blanca) para garantizar legibilidad
- Tamaños de título idénticos al brandkit (Caveat 100-180px)

---

## PATRÓN 3 — CUTOUT CIRCULAR (profile pic)

**Cuándo:** slide con varios elementos donde la foto es secundaria — ej. al lado de una cita, junto a un dato, en lista de "yo soy...".

**Look:** círculo perfecto con sombra suave, tipo "profile picture" recortado.

```html
<div class="cutout">
  <img src="foto.jpg" alt="">
</div>
```

```css
.cutout {
  position: absolute;
  top: 200px; right: 80px;
  width: 220px; height: 220px;
  border-radius: 50%;
  overflow: hidden;
  background: #FCFAF3;
  padding: 8px;
  box-shadow: 0 14px 30px rgba(0,0,0,0.18),
              0 4px 8px rgba(0,0,0,0.10);
  transform: rotate(-3deg);
}
.cutout img {
  width: 100%; height: 100%;
  border-radius: 50%;
  object-fit: cover;
  display: block;
  filter: contrast(1.02) saturate(1.05);
}
```

**Reglas:**
- Tamaño: 180-260px de diámetro (más grande pierde el feel de "cutout")
- Borde de papel crema visible (padding 6-10px) — no la foto raw
- Sombra suave + leve rotación (±2°-±4°)

---

## PATRÓN 4 — PHOTO STRIP (tira de fotomatón)

**Cuándo:** slide "evolución", "antes vs ahora", "mi semana", "3 looks" — cuando hay narrativa de varias fotos en secuencia.

**Look:** 3-4 fotos pequeñas en columna o fila, tipo tira de fotomatón con borde blanco compartido.

```html
<div class="photo-strip">
  <img src="foto-1.jpg" alt="">
  <img src="foto-2.jpg" alt="">
  <img src="foto-3.jpg" alt="">
</div>
```

```css
.photo-strip {
  position: absolute;
  top: 360px; right: 80px;
  width: 240px;
  background: #FCFAF3;
  padding: 14px;
  box-shadow: 0 16px 34px rgba(0,0,0,0.18);
  transform: rotate(2.5deg);
  display: flex; flex-direction: column; gap: 12px;
}
.photo-strip img {
  width: 100%; aspect-ratio: 1 / 1;
  object-fit: cover; display: block;
  filter: contrast(1.02) saturate(1.05);
}
```

**Reglas:**
- Mismo aspect ratio en todas (1:1 o 4:5)
- Mismo filter en todas para que la tira se sienta una unidad
- Rotación de la tira completa, no foto por foto

---

## CHECKLIST CUANDO USES FOTO

- [ ] ¿La foto fue copiada a la carpeta de output? (no usar rutas absolutas en `<img src>`)
- [ ] ¿El patrón elegido encaja con el rol del slide? (polaroid = personal, hero = impacto, cutout = secundario, strip = narrativa)
- [ ] ¿La foto sigue conviviendo con washi tape, post-its o stickers? (si la foto está sola se siente plana — añade al menos 1 tape encima del polaroid o 1 sticker al lado)
- [ ] ¿La rotación es sutil (±2°-±5°)?
- [ ] ¿Hay sombra dramática para dar peso de objeto físico?
- [ ] ¿El filter de saturación/contraste es ligero (no fotopópico, mantiene tono cálido del brandkit)?

---

## CÓMO ELEGIR LA FOTO CORRECTA

Cuando el usuario pasa una carpeta, NO leer las 45 fotos. Estrategia:

1. Listar la carpeta y elegir 4-6 candidatas por **fecha modificada reciente** o **tamaño grande** (proxy de calidad)
2. Hacer `Read` solo de esas candidatas
3. Filtrar por composición:
   - **Para polaroid en portada** → close-up, cara mirando a cámara, fondo limpio
   - **Para hero** → vertical, persona centrada, espacio negativo arriba/abajo para texto
   - **Para cutout** → cualquier selfie con cara despejada
   - **Para strip** → varias fotos del mismo "set" (mismo outfit/lugar) si están disponibles
4. Si ninguna calza, pedirle al usuario más fotos o sugerir generar una nueva con la skill `banana`

---

## CASOS DE USO TÍPICOS

| Tipo de carrusel | Patrón sugerido |
|---|---|
| Top 5 / lista personal (ej. "películas de terror") | Polaroid izq + post-its der |
| "Mi historia" / storytelling | Polaroid en portada, cutouts en slides intermedios |
| "Antes vs ahora" | Photo strip (2 fotos) |
| Vlog / "mi semana" | Photo strip (3-4 fotos) |
| Anuncio / lanzamiento | Hero background con CTA encima |
| Tip educativo (sin protagonismo) | Cutout pequeño en esquina + post-its principales |
