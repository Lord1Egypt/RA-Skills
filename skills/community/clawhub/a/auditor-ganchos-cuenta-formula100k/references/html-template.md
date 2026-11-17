# Plantilla del index.html interactivo

Single-file HTML auto-contenido. Dark theme + accent amarillo F100K. Inter (UI) + Caveat (números/firma) desde Google Fonts.

## Estructura general

```html
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Auditoría @<usuario> · F100K</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=Caveat:wght@500;700&display=swap" rel="stylesheet">
  <style>/* CSS canónico, ver abajo */</style>
</head>
<body>
  <header>…</header>
  <nav class="tabs">…</nav>
  <section id="formula" class="active">…</section>
  <section id="data">…</section>
  <section id="compare">…</section>
  <section id="deep">…</section>
  <section id="proposals">…</section>
  <section id="builder">…</section>
  <footer>…</footer>
  <div class="modal-overlay" id="modal">…</div>
  <script>/* JS canónico, ver abajo */</script>
</body>
</html>
```

## Paleta de variables CSS obligatoria

```css
:root{
  --bg:#0a0b0d;
  --bg-2:#13151a;
  --bg-3:#1c1f26;
  --line:#2a2e38;
  --text:#f5f5f7;
  --text-2:#a8aab2;
  --text-3:#6b6e78;
  --yellow:#ffd60a;
  --yellow-soft:rgba(255,214,10,.15);
  --green:#34d399;
  --red:#f87171;
  --amber:#fbbf24;
}
```

## Tabs sticky (template canónico)

```html
<nav class="tabs">
  <div class="tabs-inner">
    <button class="tab active" data-tab="formula">📐 La fórmula</button>
    <button class="tab" data-tab="data">📊 Los N reels</button>
    <button class="tab" data-tab="compare">⚖️ Top vs Bottom</button>
    <button class="tab" data-tab="deep">🧠 Por qué funcionó</button>
    <button class="tab" data-tab="proposals">✨ N propuestas nuevas</button>
    <button class="tab" data-tab="builder">🛠️ Hook builder</button>
  </div>
</nav>
```

```css
nav.tabs{position:sticky;top:0;z-index:50;background:rgba(10,11,13,.85);backdrop-filter:blur(20px);border-bottom:1px solid var(--line);padding:0 32px}
.tabs-inner{display:flex;gap:4px;overflow-x:auto;max-width:1280px;margin:0 auto;scrollbar-width:none}
.tab{padding:18px 16px;font-size:14px;font-weight:500;color:var(--text-2);position:relative;white-space:nowrap}
.tab.active{color:var(--yellow)}
.tab.active::after{content:"";position:absolute;bottom:-1px;left:16px;right:16px;height:2px;background:var(--yellow)}
```

```js
const tabs = document.querySelectorAll('.tab');
const sections = document.querySelectorAll('section');
tabs.forEach(t=>t.addEventListener('click',()=>{
  tabs.forEach(x=>x.classList.remove('active'));
  sections.forEach(x=>x.classList.remove('active'));
  t.classList.add('active');
  document.getElementById(t.dataset.tab).classList.add('active');
  window.scrollTo({top:0,behavior:'smooth'});
}));
```

## Componente: reel card con modal

```html
<div class="reel-card" onclick="openModal(<pos>)">
  <div class="reel-thumb">
    <img src="hook_<pos>.png"/>
    <div class="reel-rank top">🥇 TOP 1</div>
  </div>
  <div class="reel-info">
    <div class="reel-stats">
      <div class="stat"><span class="stat-val big"><K_format></span><span class="stat-lbl">Plays</span></div>
      <div class="stat"><span class="stat-val"><likes></span><span class="stat-lbl">Likes</span></div>
      <div class="stat"><span class="stat-val"><coms></span><span class="stat-lbl">Coments</span></div>
    </div>
    <div class="reel-tema"><tema></div>
  </div>
</div>
```

Modal con transcripción completa, stats grid, link directo a IG, botón cerrar.

## Componente: pattern card (sección deep)

```html
<div class="pattern-card">
  <div class="pattern-header">
    <div class="pattern-num">01</div>
    <div class="pattern-title"><nombre del patrón></div>
  </div>
  <div class="pattern-principle"><principio científico></div>
  <div class="pattern-desc"><explicación breve></div>
  <div class="pattern-evidence"><evidencia del feed></div>
</div>
```

## Componente: reason accordion (sección deep)

Usar `<details>` para no necesitar JS:

```html
<details class="reason top">
  <summary>
    <div class="reason-thumb" style="background-image:url('hook_<pos>.png')"></div>
    <div class="reason-main">
      <div class="reason-tag">🥇 TOP 1 · <tema></div>
      <div class="reason-name"><por qué funcionó en 1 frase></div>
      <div class="reason-quote">"<primeras palabras>"</div>
    </div>
    <div class="reason-plays"><K><small>plays</small></div>
    <div class="reason-toggle">+</div>
  </summary>
  <div class="reason-body">
    <div class="reason-section">
      <h5>Los 6 disparadores específicos que lo hicieron explotar</h5>
      <ul>
        <li><strong>"<palabra clave>"</strong>: <análisis cognitivo></li>
        ...
      </ul>
    </div>
    <div class="reason-takeaway"><strong>Replicable en cualquier nicho:</strong> ...</div>
  </div>
</details>
```

## Componente: propuesta Higgsfield card

```html
<div class="prop-card">
  <div class="prop-thumb">
    <span class="prop-cat"><categoría></span>
    <span class="prop-num"><N></span>
    <img src="propuestas/p<N>.png"/>
  </div>
  <div class="prop-body">
    <div class="prop-title"><título corto></div>
    <div class="prop-hook">
      <strong>Texto en pantalla</strong>
      <texto overlay>
    </div>
    <div class="prop-hook" style="border-left-color:var(--green)">
      <strong style="color:var(--green)">Primeras palabras del audio</strong>
      <audio>
    </div>
    <div class="prop-why">
      <ul>
        <li><razón 1></li>
        <li><razón 2></li>
        <li><razón 3></li>
      </ul>
    </div>
    <div class="prop-actions">
      <button class="prop-btn" onclick="copyHook(this,'<overlay>')">📋 Copiar overlay</button>
      <button class="prop-btn" onclick="copyHook(this,'<audio>')">🎙 Copiar audio</button>
    </div>
  </div>
</div>
```

## Componente: hook builder (sección builder)

3 grupos de pills (template + data + emotion) que actualizan en vivo el preview:

```js
const builderState = {template:"Tenemos {N} minutos para",data:"llegar al embarque",emotion:"😭"};
function renderBuild(){
  let text = builderState.template.replace('{N}','30') + ' ' + builderState.data;
  if(builderState.emotion) text += ' ' + builderState.emotion;
  document.getElementById('build-text').textContent = text;
  document.getElementById('build-chars').textContent = text.length;
  document.getElementById('build-secs').textContent = (text.length/28).toFixed(1)+'s';
  const opens = !/(menos|más|para vivir|el centro)$/.test(text.replace(builderState.emotion,'').trim());
  const score = document.getElementById('build-score');
  if(opens){score.textContent='✓ Abre loop';score.style.color='var(--green)'}
  else{score.textContent='✗ Cierra idea';score.style.color='var(--red)'}
}
```

## Copy-to-clipboard pattern

```js
function copyHook(btn,text){
  navigator.clipboard.writeText(text);
  const orig = btn.textContent;
  btn.textContent = '✓ Copiado';
  btn.classList.add('copied');
  setTimeout(()=>{btn.textContent=orig;btn.classList.remove('copied')},1500);
}
```

## Inyección de datos (al final del `<script>`)

Hardcodear los arrays `reels` y `proposals` directamente en el JS — NO usar fetch, el HTML debe funcionar offline al abrirlo por doble-click.

```js
const reels = [
  {pos:6,short:"DYd1LFFuVJH",date:"2026-05-18",plays:56985,views:31142,likes:621,comments:17,duration:51.8,tema:"...",hook:"...",transcript:"..."},
  ...
];
const proposals = [
  {n:1,file:"propuestas/p1_aeropuerto.png",cat:"Urgencia + número",title:"...",overlay:"...",audio:"...",why:["...","...","..."]},
  ...
];
```

## Responsive obligatorio

```css
@media(max-width:768px){
  section{padding:40px 20px}
  header{padding:32px 20px 20px}
  nav.tabs{padding:0 16px}
  .compare-grid{grid-template-columns:1fr}
  .modal{grid-template-columns:1fr;max-height:95vh}
  .builder{grid-template-columns:1fr;padding:20px}
}
```

## Header obligatorio

```html
<header>
  <div class="container">
    <span class="eyebrow">Auditoría F100K · <fecha></span>
    <h1>El patrón que separa <em><top_K></em> de <em><bot_K></em> vistas en la misma cuenta.</h1>
    <p class="lede">…</p>
    <div class="meta-row">
      <div class="meta-item"><span class="meta-label">Cuenta</span><span class="meta-value">@<usuario></span></div>
      <div class="meta-item"><span class="meta-label">Ventana</span><span class="meta-value"><inicio> – <fin></span></div>
      <div class="meta-item"><span class="meta-label">Reels analizados</span><span class="meta-value"><N></span></div>
      <div class="meta-item"><span class="meta-label">Plays totales</span><span class="meta-value">~<sum>K</span></div>
      <div class="meta-item"><span class="meta-label">Brecha top/bottom</span><span class="meta-value" style="color:var(--yellow)"><Nx></span></div>
    </div>
  </div>
</header>
```

## Referencia ejecutada

Para el HTML canónico completo (1177 líneas) que esta plantilla resume, ver:
(la implementación de referencia de 1177 líneas no viene en este paquete: arma el HTML con esta plantilla)

Esa es la implementación de referencia — clonar su estructura cambiando solo los datos hardcoded en el `<script>` al final.
