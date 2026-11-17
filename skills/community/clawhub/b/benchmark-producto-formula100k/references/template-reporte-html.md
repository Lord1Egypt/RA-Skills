# Template HTML · Reporte Benchmark F100K

Esta es la plantilla EXACTA que se usa para generar `01-REPORTE-COMPLETO.html`. No improvisar estilos — copiar este esqueleto y rellenar los `[PLACEHOLDERS]`.

El archivo final debe ser **HTML autocontenido**: un solo `.html`, sin assets locales. Tailwind y Google Fonts vía CDN.

---

## Esqueleto base

```html
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>Benchmark [NICHO] · FÓRMULA 100K</title>
<script src="https://cdn.tailwindcss.com"></script>
<link href="https://fonts.googleapis.com/css2?family=Caveat:wght@500;700&family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<script>
  tailwind.config = {
    theme: {
      extend: {
        fontFamily: {
          sans: ['Inter', 'sans-serif'],
          hand: ['Caveat', 'cursive'],
        },
        colors: {
          cream: { 50:'#FDFBF6', 100:'#F8F3E7', 200:'#F1E9D2', 300:'#E8DAB2' },
          ink: '#1A1A1A',
          accent: { yellow:'#FFD43B', pink:'#F472B6', green:'#84CC16', blue:'#60A5FA' },
        },
      }
    }
  }
</script>
<style>
  body { background: #FDFBF6; color: #1A1A1A; }
  .washi { position:relative; background:#FFD43B; padding:2px 10px; transform:rotate(-1deg); display:inline-block; box-shadow:1px 1px 0 rgba(0,0,0,0.1); }
  .postit { background:#FEF9C3; box-shadow:2px 4px 8px rgba(0,0,0,0.1); transform:rotate(-0.5deg); }
  .bar { height:10px; border-radius:5px; background:#F1E9D2; overflow:hidden; }
  .bar > div { height:100%; background:linear-gradient(90deg,#FFD43B,#F59E0B); }
  .ficha { background:white; border:1px solid #F1E9D2; border-radius:16px; box-shadow:0 4px 12px rgba(0,0,0,0.04); }
  table { border-collapse:collapse; }
  thead th { background:#1A1A1A; color:#FDFBF6; }
  tbody tr:nth-child(odd) { background:#FDFBF6; }
  tbody tr:nth-child(even) { background:#F8F3E7; }
  th, td { padding:10px 12px; text-align:left; font-size:14px; }
  td.num { text-align:center; font-weight:600; }
  .anchor { scroll-margin-top:24px; }
  .toc a:hover { color:#F59E0B; }
  .opp-card { background:white; border-left:4px solid #FFD43B; }
  .winner { background:linear-gradient(135deg,#FFD43B 0%,#F59E0B 100%); color:#1A1A1A; }
  details > summary { cursor:pointer; }
  details > summary::-webkit-details-marker { display:none; }
  .chip { display:inline-block; padding:2px 10px; border-radius:999px; font-size:11px; font-weight:600; }
  pre.map { background:#F8F3E7; padding:16px; border-radius:12px; font-family:ui-monospace,monospace; font-size:12px; line-height:1.5; }
</style>
</head>
<body class="font-sans">

  <!-- HERO -->
  <header class="bg-ink text-cream-50 px-6 py-12 md:px-16 md:py-20 relative overflow-hidden">
    <div class="absolute -top-6 -right-6 washi text-3xl">BENCHMARK</div>
    <div class="max-w-5xl mx-auto">
      <div class="font-hand text-accent-yellow text-2xl mb-2">Benchmark de producto</div>
      <h1 class="text-4xl md:text-6xl font-extrabold leading-tight mb-4">
        [CLIENTE] <span class="font-hand text-accent-yellow">vs</span> [DESCRIPCIÓN MERCADO]
      </h1>
      <p class="text-cream-200 text-lg md:text-xl max-w-3xl">[SUBTÍTULO]</p>
      <div class="flex flex-wrap gap-3 mt-6 text-sm">
        <span class="chip bg-cream-100 text-ink">📅 [FECHA]</span>
        <span class="chip bg-cream-100 text-ink">⚡ [PROFUNDIDAD]</span>
        <span class="chip bg-cream-100 text-ink">👥 [N] competidores</span>
        <span class="chip bg-accent-yellow text-ink">🏆 [CLIENTE]: [SCORE]/50</span>
      </div>
    </div>
  </header>

  <!-- LAYOUT 2 COLS -->
  <div class="max-w-7xl mx-auto px-6 md:px-12 py-12 flex gap-12">

    <!-- TOC STICKY -->
    <aside class="hidden lg:block w-64 flex-shrink-0">
      <div class="sticky top-6 toc">
        <div class="font-hand text-accent-yellow text-xl mb-3">📑 Contenido</div>
        <ul class="space-y-2 text-sm font-medium">
          <li><a href="#resumen" class="text-ink">1. Resumen ejecutivo</a></li>
          <li><a href="#mapa" class="text-ink">2. Mapa del mercado</a></li>
          <li><a href="#matriz" class="text-ink">3. Matriz scoring</a></li>
          <li><a href="#analisis" class="text-ink">4. Análisis por dimensión</a></li>
          <li><a href="#tendencias" class="text-ink">5. Tendencias</a></li>
          <li><a href="#oportunidades" class="text-ink">6. Oportunidades</a></li>
          <li><a href="#plan" class="text-ink">7. Plan 30/60/90</a></li>
          <li><a href="#fichas" class="text-ink">8. Fichas competidores</a></li>
          <li><a href="#apendice" class="text-ink">9. Apéndice</a></li>
        </ul>
      </div>
    </aside>

    <!-- MAIN -->
    <main class="flex-1 min-w-0 space-y-16">

      <!-- SECCIONES (ver detalle abajo) -->

    </main>
  </div>

</body>
</html>
```

---

## Componentes específicos por sección

### Sección Resumen Ejecutivo

```html
<section id="resumen" class="anchor">
  <div class="font-hand text-accent-yellow text-2xl">1.</div>
  <h2 class="text-3xl font-extrabold mb-6">Resumen ejecutivo</h2>

  <!-- Veredicto en post-it -->
  <div class="postit p-6 mb-8 max-w-3xl">
    <div class="font-hand text-2xl mb-2">Veredicto en una línea</div>
    <p class="text-lg">[VEREDICTO]</p>
  </div>

  <!-- 3 hallazgos en grid -->
  <h3 class="text-xl font-bold mb-4">3 hallazgos clave</h3>
  <div class="grid md:grid-cols-3 gap-4 mb-8">
    <div class="ficha p-5">
      <div class="text-3xl mb-2">[EMOJI]</div>
      <div class="font-bold mb-2">[TÍTULO HALLAZGO]</div>
      <p class="text-sm text-gray-700">[DETALLE]</p>
    </div>
    <!-- repetir x3 -->
  </div>

  <!-- Movimiento recomendado -->
  <div class="ficha p-6 border-l-4 border-accent-yellow">
    <div class="font-hand text-2xl text-accent-yellow mb-1">Movimiento recomendado · próximos 30 días</div>
    <p class="text-lg">[MOVIMIENTO]</p>
  </div>
</section>
```

### Sección Mapa del mercado (matriz 2x2 ASCII)

```html
<pre class="map">
                ALTA [EJE Y]
                    ↑
                    │
                    │   ●[CLIENTE]
COMUNIDAD ──────────┼────────────────── COMUNIDAD
PEQUEÑA             │                   GRANDE
                    │
                    │   ●[COMP A]   ●[COMP B]
                    ↓
                BAJA [EJE Y]
</pre>
```

### Sección Matriz scoring (con fila winner)

```html
<table class="w-full text-sm">
  <thead>
    <tr><th>Dimensión</th><th>[CLIENTE]</th><th>[C1]</th>...</tr>
  </thead>
  <tbody>
    <tr><td>1. Posicionamiento</td><td class="num">5</td>...</tr>
    <!-- N filas -->
    <tr class="winner font-bold">
      <td>TOTAL /50</td><td class="num">[X]</td>...
    </tr>
  </tbody>
</table>
```

### Sección Análisis dimensión por dimensión (cards expandibles)

```html
<details class="ficha p-5" [open si dim 1]>
  <summary class="font-bold text-lg">
    Dimensión [N] · [Nombre]
    <span class="chip bg-accent-yellow text-ink ml-2">[CLIENTE] gana</span>
  </summary>
  <p class="mt-3 text-gray-700">[ANÁLISIS]</p>
</details>
```

### Sección Tendencias (grid 10 cards)

```html
<div class="grid md:grid-cols-2 gap-4">
  <div class="ficha p-5">
    <div class="font-hand text-accent-yellow text-xl">#1</div>
    <div class="font-bold mb-2">[TÍTULO]</div>
    <p class="text-sm text-gray-700">[CONTENIDO]</p>
  </div>
  <!-- card destacada con ring -->
  <div class="ficha p-5 ring-2 ring-accent-yellow">...</div>
</div>
```

### Sección Oportunidades (cards con borde amarillo)

```html
<div class="opp-card p-5 rounded-lg shadow-sm">
  <div class="flex items-start gap-3">
    <div class="text-2xl font-bold text-accent-yellow">[N]</div>
    <div>
      <div class="font-bold text-lg mb-1">[TÍTULO]</div>
      <p class="text-sm text-gray-700 mb-2"><strong>Situación:</strong> ...</p>
      <p class="text-sm text-gray-700 mb-3"><strong>Movimiento:</strong> ...</p>
      <div class="flex gap-2 text-xs">
        <span class="chip bg-accent-green text-white">Impacto: Alto</span>
        <span class="chip bg-accent-blue text-white">Esfuerzo: Bajo</span>
        <span class="chip bg-cream-200 text-ink">Plazo: [X días]</span>
      </div>
    </div>
  </div>
</div>
```

### Sección Plan 30/60/90 (3 columnas)

```html
<div class="grid md:grid-cols-3 gap-4">
  <div class="ficha p-5">
    <div class="chip bg-accent-yellow text-ink mb-3">DÍAS 1-30</div>
    <div class="font-bold mb-3">Foundation</div>
    <ul class="text-sm space-y-2 text-gray-700">
      <li>☐ [ACCIÓN]</li>
    </ul>
  </div>
  <!-- DÍAS 31-60 con chip accent-pink -->
  <!-- DÍAS 61-90 con chip accent-green -->
</div>
```

### Sección Fichas (card por competidor)

```html
<div class="ficha p-6 mb-5 [ring-2 ring-accent-yellow si es cliente]">
  <div class="flex items-center justify-between mb-3">
    <div>
      <div class="text-xs text-gray-500">[TIPO RELACIÓN]</div>
      <div class="font-bold text-xl">[EMOJI] [NOMBRE] · [FUNDADOR]</div>
    </div>
    <div class="text-right text-sm">
      <div>$[PRECIO]/mes</div>
      <div class="text-gray-500">[N] miembros</div>
    </div>
  </div>
  <p class="text-sm text-gray-600 italic mb-3">"[HEADLINE]"</p>
  <div class="grid md:grid-cols-2 gap-4 text-sm">
    <div>
      <div class="font-bold mb-1">Vehículo único</div>
      <ul class="list-disc list-inside text-gray-700 space-y-1">
        <li>[BULLET]</li>
      </ul>
    </div>
    <div>
      <div class="font-bold mb-1">Cómo [CLIENTE] le gana</div>
      <ul class="list-disc list-inside text-gray-700 space-y-1">
        <li>[BULLET]</li>
      </ul>
    </div>
  </div>
</div>
```

### Barras de progreso (para TOTAL y miembros)

```html
<div class="space-y-3 max-w-2xl">
  <div>
    <div class="flex justify-between mb-1">
      <span class="font-semibold">🏆 [CLIENTE]</span>
      <span class="font-bold">[VALOR]</span>
    </div>
    <div class="bar"><div style="width:[%]%"></div></div>
  </div>
</div>
```

### Footer

```html
<footer class="border-t border-cream-200 pt-8 mt-16 text-sm text-gray-500 text-center">
  <p>Benchmark generado el [FECHA] · Metodología F100K · 10 dimensiones</p>
  <p class="mt-2 font-hand text-lg text-accent-yellow">[TU MARCA] · @tuhandle</p>
</footer>
```

---

## Reglas de oro

1. **Un solo archivo HTML.** Nada de CSS o JS externos más allá de Tailwind CDN + Google Fonts.
2. **No usar voseo argentino** (escribir en español neutro: tú/tienes, no vos/tenés).
3. **No emojis decorativos en exceso.** Sólo en hallazgos clave y chips (📅, ⚡, 🏆, 🤖, 💰, 🛡️, 🔥).
4. **Cliente siempre destacado:** ring amarillo, fila gradient winner, ⭐/🏆.
5. **El TOC debe ser sticky** en desktop. En mobile se oculta (`hidden lg:block`).
6. **Tabla scoring SIEMPRE con fila TOTAL** con clase `winner`.
7. **Cada oportunidad lleva chips de impacto/esfuerzo/plazo.** Sin chips, no es accionable.
8. **Cifras y nombres propios SIEMPRE entre `<strong>`** en párrafos descriptivos.
9. **Citar fuentes en el apéndice** con `<a>` clickeables (las URLs reales scrapadas).
10. **Footer obligatorio** con firma Caveat F100K + el handle del usuario.
