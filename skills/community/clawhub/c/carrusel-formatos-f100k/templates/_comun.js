// Utilidades compartidas por las plantillas. build.js las inyecta en /*__COMUN__*/.

const esc = s => String(s ?? '').replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

// Marcado mínimo: **negrita** · *itálica* · ==resaltador== · __subrayado__ · salto de línea
function md(s) {
  return esc(s)
    .replace(/==(.+?)==/g, '<mark>$1</mark>')
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/__(.+?)__/g, '<u>$1</u>')
    .replace(/\*(.+?)\*/g, '<em>$1</em>')
    .replace(/\n/g, '<br>');
}

// Foto: "ruta" | {src, foco} | {color}. build.js ya convirtió las rutas en file:// absolutas.
function foto(f) {
  if (!f) return '<div class="foto" style="background:#222"></div>';
  if (typeof f === 'string') f = { src: f };
  if (f.color) return `<div class="foto" style="background:${esc(f.color)}"></div>`;
  return `<img class="foto" src="${esc(f.src)}" style="object-position:${esc(f.foco || '50% 50%')}">`;
}

// Autofit: encoge la fuente de la caja hasta que quepa en ALTO y en ANCHO.
// Medir solo el alto deja pasar una palabra larga que se sale por la derecha.
// Se comparan las CAJAS de los hijos contra la caja del contenedor, no scrollHeight:
// scrollHeight cuenta la tinta de las letras pesadas (Montserrat 900) y da falsos desbordes de 5 px.
function desborda(el) {
  if (!el.children.length) return el.scrollHeight > el.clientHeight + 1 || el.scrollWidth > el.clientWidth + 1;
  const r = el.getBoundingClientRect();
  const cs = getComputedStyle(el);
  const top = r.top + parseFloat(cs.paddingTop), bottom = r.bottom - parseFloat(cs.paddingBottom);
  const left = r.left + parseFloat(cs.paddingLeft), right = r.right - parseFloat(cs.paddingRight);
  for (const c of el.children) {
    if (getComputedStyle(c).position === 'absolute') continue;
    const q = c.getBoundingClientRect();
    if (q.top < top - 1 || q.bottom > bottom + 1 || q.left < left - 1 || q.right > right + 1) return true;
  }
  for (const c of el.querySelectorAll('*')) {
    const d = getComputedStyle(c).display;
    if (d === 'inline' || d === 'contents') continue;
    if (c.clientWidth > 0 && c.scrollWidth > c.clientWidth + 1) return true;
  }
  return false;
}

function ajustar(el) {
  const min = parseFloat(el.dataset.min || '0.35');
  el.style.fontSize = '';
  const base = parseFloat(getComputedStyle(el).fontSize);
  let k = 1;
  while (desborda(el) && k > min) {
    k = Math.round((k - 0.02) * 100) / 100;
    el.style.fontSize = (base * k) + 'px';
  }
  return { ok: !desborda(el), k };
}

// Arranque común: pinta, espera fuentes e imágenes, ajusta, corre ganchos post-layout
// y deja window.__reporte / window.__listo para que build.js revise antes de exportar.
async function arrancar({ pintar, familias = [], despues }) {
  const spec = window.SPEC;
  const cont = document.getElementById('carrusel');
  pintar(spec, cont);
  document.body.offsetHeight;
  await Promise.all(familias.map(f => document.fonts.load(`400 40px "${f}"`).catch(() => null)));
  await Promise.all(familias.map(f => document.fonts.load(`700 40px "${f}"`).catch(() => null)));
  await document.fonts.ready;
  const faltan = familias.filter(f => !document.fonts.check(`40px "${f}"`));
  await Promise.all([...document.images].map(img => img.complete ? null : new Promise(r => { img.onload = img.onerror = r; })));
  const reporte = [];
  faltan.forEach(f => reporte.push({ tipo: 'fuente', detalle: `no cargó la fuente ${f}` }));
  [...document.images].forEach(img => { if (!img.naturalWidth) reporte.push({ tipo: 'imagen', detalle: `no cargó ${decodeURI(img.src)}` }); });
  document.querySelectorAll('.slide').forEach((s, i) => {
    s.querySelectorAll('[data-fit]').forEach(el => {
      const r = ajustar(el);
      if (!r.ok) reporte.push({ tipo: 'no-cabe', slide: i + 1, detalle: el.textContent.slice(0, 60) });
      else if (r.k < 0.6) reporte.push({ tipo: 'letra-chica', slide: i + 1, detalle: `al ${Math.round(r.k * 100)}%: ${el.textContent.slice(0, 50)}` });
    });
  });
  if (despues) despues(spec, cont, reporte);
  window.__reporte = reporte;
  window.__listo = true;
}
