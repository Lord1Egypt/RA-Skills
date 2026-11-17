// ============================================================================
// TÍTERE de animacion-dibujada-f100k — anima un PNG que trae la persona (su foto recortada,
// su mascota, el dibujo de su marca) SIN redibujarlo: se deforma como un muñeco de papel
// y los GESTOS se leen con la gramática del explainer (mitón que saluda, flecha que señala,
// nube de pensamiento, destellos), dibujados alrededor, nunca pegados como brazos falsos.
// Se carga DESPUÉS de nucleo.js. Todo es función pura de t (mismo t = mismo cuadro).
// ANATOMIA: estilizada — el títere es la foto o el dibujo real; el único «mitón» es un guante de caricatura.
//
//   const p = crearTitere(img, { cara, ancho: 520, estilo, partes, gestos, colores })
//     img     : Image o canvas con fondo transparente (sale de preparar-foto.mjs)
//     cara    : el JSON de cara.swift, o ojos/boca escritos a mano; null = sin parpadeo ni boca
//     ancho   : ancho en pixeles del video
//     estilo  : 'foto' (tal cual) | 'sticker' (borde blanco liso) | 'recorte-papel' (borde blanco irregular,
//               grano de papel, sombra corrida y movimiento a 12 cuadros por segundo). sticker: true = 'sticker'.
//     partes  : OPCIONAL, brazos recortables del PNG para que se muevan de verdad (coordenadas del PNG original):
//               { brazoIzq: { poligono: [[x,y],…], hombro: [x,y] }, brazoDer: { … } }
//               izq/der = como se ve en pantalla. Sirve para dibujos con bracitos separados del cuerpo.
//     gestos  : true (por defecto) = dibuja los gestos de explainer alrededor
//     colores : { tinta: '#1d1a24', mano: '#ffffff', acento: '#ffd84d', nube: '#ffffff' }
//   p.ancho, p.alto, p.cortado (true = busto/selfie cortado abajo: apóyalo en el borde de abajo del video, sin piso)
//   p.dibujar(ctx, x, y, { accion, t, mira = 1, escala = 1, sombra = true, hacia })
//     (x, y) = el centro de la BASE (los pies, o el borde de abajo del recorte)
//     accion: 'quieto' | 'caminar' | 'saludar' | 'saltar' | 'hablar' | 'festejar' | 'pensar' | 'señalar' | 'sorpresa'
//     t     : segundos desde que empezó la acción (el ciclo se repite)
//     mira  : 1 = como viene la foto, -1 = espejo
//     hacia : a dónde señala: 'der' | 'izq' | 'arriba' | 'abajo' (por defecto, hacia donde mira)
//
//   stickerDe(img, { borde: 16, color: '#fff', sombra: true, irregular: false }) → canvas con borde grueso tipo sticker
// ============================================================================

// ---------- silueta dilatada y SUAVE: difumina el alfa y lo corta con un umbral ----------
// (así el pelo fino y los mechones sueltos quedan dentro de un borde redondo, sin dientes de sierra)
function _silueta(img, borde, m, irregular, semilla = 3) {
  const w = img.width + 2 * m, h = img.height + 2 * m;
  const c = document.createElement('canvas'); c.width = w; c.height = h;
  const g = c.getContext('2d', { willReadFrequently: true });
  // 1. primero se «peina» el alfa (difuminado chico + umbral): los pelos sueltos se juntan en una masa
  g.filter = `blur(${Math.max(1.5, borde * .12)}px)`; g.drawImage(img, m, m); g.filter = 'none';
  let d = g.getImageData(0, 0, w, h);
  for (let i = 3; i < d.data.length; i += 4) d.data[i] = d.data[i] > 90 ? 255 : 0;
  g.putImageData(d, 0, 0);
  // 2. dilatación redonda: difuminar con sigma ≈ borde/2 y cortar muy abajo
  const t = document.createElement('canvas'); t.width = w; t.height = h; const tg = t.getContext('2d', { willReadFrequently: true });
  tg.filter = `blur(${borde * .5}px)`; tg.drawImage(c, 0, 0); tg.filter = 'none';
  d = tg.getImageData(0, 0, w, h);
  for (let y = 0, i = 3; y < h; y++) for (let x = 0; x < w; x++, i += 4) {
    let umbral = 14;
    if (irregular) umbral = 3 + 105 * vnoise(x / 55 + semilla, y / 55) ** 1.4 + 22 * vnoise(x / 7, y / 7 + semilla);   // borde de tijera, no de regla
    d.data[i] = d.data[i] > umbral ? 255 : 0;
  }
  tg.putImageData(d, 0, 0);
  // 3. antialias final
  g.clearRect(0, 0, w, h); g.filter = 'blur(.8px)'; g.drawImage(t, 0, 0); g.filter = 'none';
  return c;
}

function stickerDe(img, { borde = 16, color = '#fff', sombra = true, irregular = false, papel = false } = {}) {
  const m = borde + (sombra ? 34 : 4);
  const sil = _silueta(img, borde, m, irregular);
  const w = sil.width, h = sil.height;
  const s = sil.getContext('2d');
  s.globalCompositeOperation = 'source-in'; s.fillStyle = color; s.fillRect(0, 0, w, h); s.globalCompositeOperation = 'source-over';
  if (papel) {                                          // grano y fibras del papel sobre el borde blanco
    const r = rng(19); s.globalCompositeOperation = 'source-atop';
    for (let i = 0; i < w * h / 60; i++) { s.fillStyle = r() < .5 ? 'rgba(120,100,70,.10)' : 'rgba(255,255,255,.5)'; s.fillRect(r() * w, r() * h, 1 + r() * 2, 1 + r() * 2); }
    s.strokeStyle = 'rgba(150,120,90,.12)'; s.lineWidth = 1;
    for (let i = 0; i < w * h / 4000; i++) { const x = r() * w, y = r() * h, a = r() * 6.28; s.beginPath(); s.moveTo(x, y); s.lineTo(x + Math.cos(a) * 14, y + Math.sin(a) * 14); s.stroke(); }
    s.globalCompositeOperation = 'source-over';
  }
  const c = document.createElement('canvas'); c.width = w; c.height = h;
  const g = c.getContext('2d');
  if (sombra) {                                         // sombra oscura y suave, un poco corrida hacia abajo
    const so = document.createElement('canvas'); so.width = w; so.height = h; const sg = so.getContext('2d');
    sg.drawImage(sil, 0, 0); sg.globalCompositeOperation = 'source-in'; sg.fillStyle = 'rgb(30,20,40)'; sg.fillRect(0, 0, w, h);
    g.save(); g.filter = 'blur(12px)'; g.globalAlpha = .33; g.drawImage(so, 6, 14); g.restore();
  }
  g.drawImage(sil, 0, 0);
  g.drawImage(img, m, m);
  c.margen = m;                                         // cuánto se corrió la imagen (para mover la cara)
  return c;
}

// ---------- piezas gráficas de los gestos (el lenguaje del explainer) ----------
function _contorno(g, tinta, ancho) { g.lineJoin = g.lineCap = 'round'; g.strokeStyle = tinta; g.lineWidth = ancho; g.stroke(); }

// mitón de caricatura (guante redondo con pulgar y puño), centrado en su muñeca, apuntando hacia arriba
function _miton(g, tam, col) {
  const s = tam / 100;
  g.save(); g.scale(s, s);
  g.beginPath(); g.roundRect(-30, -6, 60, 26, 10);          // puño
  g.fillStyle = col.mano; g.fill(); _contorno(g, col.tinta, 7);
  g.beginPath();                                              // palma con los dedos juntos
  g.moveTo(-32, -4); g.bezierCurveTo(-40, -60, -26, -96, 2, -98); g.bezierCurveTo(30, -98, 40, -64, 34, -4); g.closePath();
  g.fillStyle = col.mano; g.fill(); _contorno(g, col.tinta, 7);
  g.beginPath(); g.ellipse(-38, -40, 14, 24, -.5, 0, Math.PI * 2);   // pulgar
  g.fillStyle = col.mano; g.fill(); _contorno(g, col.tinta, 7);
  g.beginPath(); g.moveTo(-6, -70); g.lineTo(-6, -40); g.moveTo(12, -72); g.lineTo(12, -42); _contorno(g, col.tinta, 5);   // rayitas de dedos
  g.restore();
}

// flecha gruesa con contorno (legible sobre cualquier fondo), de (0,0) hacia +x, largo L
function _flecha(g, L, k, col) {
  const pts = []; for (let i = 0; i <= 20; i++) { const u = i / 20; pts.push([u * L, Math.sin(u * Math.PI) * -L * .12]); }
  const n = Math.max(2, Math.round(pts.length * k));
  const traza = w => { g.beginPath(); pts.slice(0, n).forEach(([x, y], i) => i ? g.lineTo(x, y) : g.moveTo(x, y)); _contorno(g, w.c, w.w); };
  traza({ c: col.tinta, w: 30 }); traza({ c: col.acento, w: 16 });
  if (k >= .98) {                                             // la punta aparece al terminar el trazo
    const [ex, ey] = pts[pts.length - 1], a = Math.atan2(ey - pts[pts.length - 3][1], ex - pts[pts.length - 3][0]);
    g.save(); g.translate(ex, ey); g.rotate(a);
    g.beginPath(); g.moveTo(26, 0); g.lineTo(-22, -30); g.lineTo(-12, 0); g.lineTo(-22, 30); g.closePath();
    g.fillStyle = col.acento; g.fill(); _contorno(g, col.tinta, 8); g.restore();
  }
}

function _estrellita(g, x, y, r, col) {                    // destello de 4 puntas
  g.beginPath();
  for (let i = 0; i < 8; i++) { const a = i * Math.PI / 4, rr = i % 2 ? r * .32 : r; g.lineTo(x + Math.cos(a - Math.PI / 2) * rr, y + Math.sin(a - Math.PI / 2) * rr); }
  g.closePath(); g.fillStyle = col.acento; g.fill(); _contorno(g, col.tinta, Math.max(3, r * .16));
}

// ---------- el títere ----------
function crearTitere(img, { cara = null, ancho = 520, sticker = false, borde = 16, estilo = null, partes = null, gestos = true, colores = {} } = {}) {
  estilo = estilo || (sticker ? 'sticker' : 'foto');
  const col = { tinta: '#1d1a24', mano: '#ffffff', acento: '#ffd84d', nube: '#ffffff', ...colores };
  let fuente = img, corre = 0;
  if (estilo === 'sticker') { fuente = stickerDe(img, { borde, sombra: false }); corre = fuente.margen; }
  if (estilo === 'recorte-papel') { fuente = stickerDe(img, { borde: Math.max(borde, 30), sombra: false, irregular: true, papel: true, color: '#fffdf6' }); corre = fuente.margen; }
  const esc = ancho / fuente.width, alto = Math.round(fuente.height * esc);
  // la imagen se escala UNA vez (así cada cuadro solo copia)
  const base = document.createElement('canvas'); base.width = Math.round(ancho); base.height = alto;
  const bg = base.getContext('2d', { willReadFrequently: true }); bg.imageSmoothingQuality = 'high';
  bg.drawImage(fuente, 0, 0, base.width, base.height);
  const P = p => p ? [(p[0] + corre) * esc, (p[1] + corre) * esc] : null;

  // brazos recortables: se sacan del cuerpo y se dibujan girando en su hombro
  const BRAZOS = [];
  if (partes) for (const [nombre, sgn] of [['brazoIzq', 1], ['brazoDer', -1]]) {
    const b = partes[nombre]; if (!b || !b.poligono || !b.hombro) continue;
    const capa = document.createElement('canvas'); capa.width = base.width; capa.height = alto;
    const cg0 = capa.getContext('2d');
    const poli = b.poligono.map(P);
    cg0.beginPath(); poli.forEach(([x, y], i) => i ? cg0.lineTo(x, y) : cg0.moveTo(x, y)); cg0.closePath(); cg0.clip();
    cg0.drawImage(base, 0, 0);
    bg.save(); bg.globalCompositeOperation = 'destination-out';
    bg.beginPath(); poli.forEach(([x, y], i) => i ? bg.lineTo(x, y) : bg.moveTo(x, y)); bg.closePath(); bg.fill(); bg.restore();
    BRAZOS.push({ capa, hombro: P(b.hombro), sgn, lado: nombre === 'brazoIzq' ? 'izq' : 'der' });
  }

  // dónde quedó la cara en el títere escalado
  const C = cara && (cara.ojoIzq || cara.boca) ? {
    ojos: [P(cara.ojoIzq), P(cara.ojoDer)].filter(Boolean),
    ojoAncho: (cara.ojoAncho || (cara.cara ? cara.cara[2] * .2 : 30)) * esc,
    boca: P(cara.boca), bocaAncho: (cara.bocaAncho || 40) * esc, bocaAlto: (cara.bocaAlto || 14) * esc,
    caraAlto: cara.cara ? cara.cara[3] * esc : 0, caraAncho: cara.cara ? cara.cara[2] * esc : 0,
    caraCentro: cara.cara ? P([cara.cara[0] + cara.cara[2] / 2, cara.cara[1] + cara.cara[3] / 2]) : null,
    bocaColor: cara.bocaColor,
  } : null;
  // tono para el párpado de CADA ojo: el que se escriba a mano, o el de alrededor de ese ojo (sirve con rayas o sombras)
  if (C && C.ojos.length) {
    C.ojoAlto = (cara.ojoAlto || cara.ojoAncho * .55 || 16) * esc;
    C.foto = !!cara.cara;                                // foto real (Vision halló la cara) o dibujo (ojos a mano)
    const oscurece = c => c.replace(/\d+/g, v => String(Math.round(v * .45)));
    C.pieles = C.ojos.map(([ox, oy]) => {
      if (cara.piel) return cara.piel;
      const muestras = [], r = Math.max(C.ojoAncho, C.ojoAlto) * .85;
      for (let k = 0; k < 16; k++) { const a = k / 16 * Math.PI * 2;
        const d = bg.getImageData(Math.round(ox + Math.cos(a) * r * 1.05), Math.round(oy + Math.sin(a) * r * .95), 1, 1).data;
        if (d[3] > 200) muestras.push([d[0], d[1], d[2]]); }
      // se queda con los tonos del medio de la vuelta (descarta pestañas y cejas, y también los brillos)
      muestras.sort((a, b) => (b[0] + b[1] + b[2]) - (a[0] + a[1] + a[2]));
      const claros = muestras.slice(Math.floor(muestras.length * .2), Math.max(1, Math.ceil(muestras.length * .7)));
      const med = k => claros.map(q => q[k]).sort((a, b) => a - b)[Math.floor(claros.length / 2)];
      return muestras.length ? `rgb(${med(0)},${med(1)},${med(2)})` : '#e8b894';
    });
    C.linea = cara.linea || oscurece(C.pieles[0].startsWith('rgb') ? C.pieles[0] : 'rgb(120,80,60)');
  }
  // ¿viene cortado abajo? (un busto o un selfie): la última fila tiene mucho relleno ⇒ va apoyado en el borde del video, sin piso
  const fila = bg.getImageData(0, alto - 2, base.width, 1).data; let llenos = 0;
  for (let i = 3; i < fila.length; i += 4) if (fila[i] > 128) llenos++;
  const cortado = llenos / base.width > .25;
  // la cabeza: la cara si Vision la halló, los ojos si vienen a mano, o el cuarto de arriba
  const cabeza = (() => {
    if (C && C.caraCentro) return { x: C.caraCentro[0], y: C.caraCentro[1], r: Math.max(C.caraAncho, C.caraAlto) * .62 };
    const tope = (() => { const d = bg.getImageData(0, 0, base.width, alto).data;   // la primera fila con algo opaco
      for (let yy = 0; yy < alto; yy++) for (let xx = 0; xx < base.width; xx += 2) if (d[(yy * base.width + xx) * 4 + 3] > 128) return yy; return 0; })();
    if (C && C.ojos.length) { const x = C.ojos.reduce((a, o) => a + o[0], 0) / C.ojos.length, yo = C.ojos.reduce((a, o) => a + o[1], 0) / C.ojos.length;
      const r = clamp((yo - tope) * .55, base.width * .22, base.width * .45);
      return { x, y: Math.min(yo, tope + r), r }; }
    return { x: base.width / 2, y: tope + base.width * .3, r: base.width * .3 };
  })();
  const cuadro = document.createElement('canvas'); cuadro.width = base.width; cuadro.height = alto;
  const cg = cuadro.getContext('2d');
  const párpado = document.createElement('canvas');   // lienzo chico para el párpado de foto
  // silueta oscura del cuadro (para la sombra corrida del recorte de papel)
  const silo = document.createElement('canvas'); silo.width = base.width; silo.height = alto; const sog = silo.getContext('2d');

  // --- cuánto cierra los ojos: 0..1, en 5 cuadros (medio, cerrado, medio): se ve a cualquier velocidad ---
  const parpadeo = t => { const c = (t + .37) % 3.3, d = .2; if (c < 3.3 - d - .05 || c > 3.25) return 0;
    const u = (c - (3.3 - d - .05)) / d; return clamp(1 - Math.abs(u * 2 - 1) * 1.15); };
  const boca = t => {                                   // cambia cada 3 cuadros como en los dibujos animados: 0, medio o abierto
    const f = Math.floor(t * 10);
    const v = Math.abs(Math.sin(f * 1.7) + Math.sin(f * .63) * .6);
    return v < .35 ? 0 : v < 1 ? .55 : 1;
  };

  // --- la pose de cada acción: { dy (sube), sx, sy (squash/stretch), gira, curva, bI, bD (brazos, radianes hacia arriba) } ---
  function pose(accion, t, hacia) {
    const respira = Math.sin(t * Math.PI * 2 / 2.4);
    const p = { dy: 0, sx: 1 - respira * .006, sy: 1 + respira * .012, gira: 0, curva: 0, bI: respira * .04, bD: -respira * .04 };
    const entra = ease(clamp(t / .28));
    switch (accion) {
      case 'caminar': {                                  // bamboleo: sube y baja 2 veces por ciclo, se mece
        const f = t * 2.6 * Math.PI;
        p.dy = Math.abs(Math.sin(f)) * .045 * alto;
        const golpe = 1 - Math.abs(Math.sin(f));         // al pisar, se aplasta un poco
        p.sy -= golpe * .035; p.sx += golpe * .025;
        p.gira = Math.sin(f) * .035; p.curva = Math.cos(f) * .035;
        p.bI = Math.sin(f) * .35; p.bD = -Math.sin(f) * .35;
        break; }
      case 'saltar': {                                   // ciclo de 1,1 s: se agacha, vuela estirado, cae y rebota
        const c = t % 1.1;
        if (c < .18) { const k = ease(c / .18); p.sy -= .1 * k; p.sx += .07 * k; }
        else if (c < .68) { const k = (c - .18) / .5; p.dy = Math.sin(k * Math.PI) * .32 * alto; p.sy += .07 * Math.sin(k * Math.PI); p.sx -= .04 * Math.sin(k * Math.PI);
          p.gira = Math.sin(k * Math.PI * 2) * .03; p.bI = p.bD = Math.sin(k * Math.PI) * 1.3; }
        else { const k = (c - .68) / .42; const rebote = Math.exp(-6 * k) * Math.cos(k * 18); p.sy -= .09 * rebote; p.sx += .06 * rebote; }
        break; }
      case 'saludar': {                                  // se mece hacia el lado del saludo, alegre
        const f = t * Math.PI * 2 * 1.4;
        p.curva = (.04 + Math.sin(f) * .05) * entra; p.gira = Math.sin(f) * .02;
        p.dy = Math.max(0, Math.sin(f * 2)) * .012 * alto;
        p.bD = (2.35 + Math.sin(t * Math.PI * 2 * 2.2) * .38) * entra; p.bI = .12;
        break; }
      case 'hablar': {                                   // cabecea suave, como quien explica
        const f = t * Math.PI * 2 * .9;
        p.curva = Math.sin(f) * .025; p.gira = Math.sin(f * .5) * .012;
        p.dy = Math.abs(Math.sin(t * 7)) * .006 * alto;
        p.bD = (.5 + .45 * Math.max(0, Math.sin(t * 2.3))) * entra; p.bI = (.3 + .3 * Math.max(0, Math.sin(t * 1.7 + 1))) * entra;
        break; }
      case 'festejar': {                                 // saltitos seguidos y se sacude
        const c = t % .5, k = c / .5;
        p.dy = Math.sin(k * Math.PI) * .12 * alto;
        const aire = Math.sin(k * Math.PI);
        p.sy += .05 * aire - (k > .9 || k < .1 ? .05 : 0); p.sx -= .03 * aire;
        p.curva = Math.sin(t * Math.PI * 2 * 2) * .07; p.gira = Math.sin(t * Math.PI * 2 * 2) * .03;
        p.bI = p.bD = (2.45 + Math.sin(t * Math.PI * 4) * .25) * entra;
        break; }
      case 'pensar': {                                   // se inclina hacia un lado y se queda ahí, meciéndose apenas
        const e = ease(clamp(t / .6));
        p.gira = -.07 * e + Math.sin(t * 2) * .006; p.curva = -.05 * e;
        p.bD = 1.75 * e; p.bI = .1;
        break; }
      case 'señalar': {                                  // se inclina hacia donde señala, con un empujoncito cada 1,2 s
        const c = t % 1.2, emp = c < .25 ? Math.sin(c / .25 * Math.PI) : 0, lado = hacia === 'izq' ? -1 : 1;
        p.gira = .06 * entra * lado + emp * .025 * lado; p.curva = .08 * entra * lado + emp * .05 * lado;
        const r = hacia === 'arriba' ? 2.5 : hacia === 'abajo' ? .7 : 1.55;
        if (lado > 0) p.bD = (r + emp * .12) * entra; else p.bI = (r + emp * .12) * entra;
        break; }
      case 'sorpresa': {                                 // brinco corto hacia arriba, estirado, y se queda tenso
        const k = clamp(t / .35);
        p.dy = Math.sin(Math.min(k, 1) * Math.PI) * .07 * alto;
        p.sy += .06 * ease(k) - .02; p.sx -= .035 * ease(k);
        p.bI = p.bD = 1.9 * ease(clamp(t / .2));
        break; }
    }
    if (cortado) p.dy = 0;                              // un busto nunca se despega del borde de abajo
    return p;
  }

  // --- los gestos dibujados (espacio del video; hx, hy = centro de la cabeza, R = su radio REAL, lado = hacia afuera) ---
  // R ubica el gesto AFUERA de la cabeza; Rt es el tamaño del dibujo (ni diminuto en un cuerpo entero ni gigante en un selfie).
  function gesto(ctx, accion, t, hx, hy, R, lado, hacia, baseX, baseY, W0) {
    if (!gestos) return;
    const g = ctx; g.save();
    const LW = g.canvas.width, dentroX = (v, r) => clamp(v, r + 24, LW - r - 24), dentroY = (v, r) => Math.max(r + 24, v);
    const Rt = clamp(R, 110, 180);
    if (accion === 'saludar' && !BRAZOS.some(b => b.lado === (lado > 0 ? 'der' : 'izq'))) {
      // el mitón se asoma por el lado de la cabeza, arriba del hombro, y agita; arcos de movimiento
      const e = back(clamp(t / .35)), mx = dentroX(hx + lado * (R * 1.1 + Rt * .6), Rt * .7), my = hy + Rt * .35;
      const a = Math.sin(t * Math.PI * 2 * 2.2) * .42;
      g.save(); g.translate(mx, my); g.rotate(a * lado + lado * .2); g.scale(e * lado, e); _miton(g, Rt * 1.05, col); g.restore();
      if (t > .3) for (let i = 0; i < 2; i++) {
        const ra = Rt * (1.2 + i * .3), al = .55 + .35 * Math.sin(t * 14 + i);
        g.globalAlpha = clamp(al); g.beginPath(); g.arc(mx, my, ra, -Math.PI / 2 - .5, -Math.PI / 2 + .5); _contorno(g, col.tinta, 7); g.globalAlpha = 1;
      }
    }
    if (accion === 'señalar') {
      const dir = hacia === 'izq' ? Math.PI : hacia === 'arriba' ? -Math.PI / 2 : hacia === 'abajo' ? Math.PI / 2 : 0;
      const c = t % 1.2, emp = c < .25 ? Math.sin(c / .25 * Math.PI) : 0;
      let L = Rt * 1.6, ox = hx, oy = hy + R * .25;
      const k = easeOut(clamp((t - .1) / .35));
      // la flecha nace AFUERA de la cabeza; si no cabe completa, se acorta (nunca se corre encima de la cara)
      if (dir === 0) { ox = hx + R * 1.15; L = clamp(LW - 50 - ox, 110, L); }
      else if (dir === Math.PI) { ox = hx - R * 1.15; L = clamp(ox - 50, 110, L); }
      else { ox = dentroX(hx + R * 1.3, 40); oy = dir < 0 ? hy - R * .3 : hy + R * .9; }
      g.save(); g.translate(ox + Math.cos(dir) * emp * 18, oy + Math.sin(dir) * emp * 18); g.rotate(dir);
      if (dir === Math.PI) g.scale(1, -1);
      _flecha(g, L, k, col); g.restore();
    }
    if (accion === 'pensar') {
      // tres burbujas que suben desde la sien y la nube A UN LADO (arriba suele ir el globo de texto)
      const cx = dentroX(hx + lado * (R * 1.15 + Rt * 1.05), Rt * 1.35), cy = dentroY(hy - R * .5 - Rt * .25, Rt * .9);
      const sx = hx + lado * R * .95, sy = hy - R * .35;
      [[.2, .13], [.45, .19], [.7, .26]].forEach(([u, r], i) => { const k = back(clamp((t - .15 * i) / .3)); if (k <= 0) return;
        g.beginPath(); g.arc(lerp(sx, cx, u), lerp(sy, cy + Rt * .45, u), Rt * r * .6 * k, 0, 7); g.fillStyle = col.nube; g.fill(); _contorno(g, col.tinta, 6); });
      const k = back(clamp((t - .5) / .4));
      if (k > 0) {
        const rw = Rt * .95 * k, rh = Rt * .6 * k;
        g.beginPath();
        const bolas = 9; for (let i = 0; i < bolas; i++) { const an = i / bolas * Math.PI * 2; g.moveTo(cx + Math.cos(an) * rw + rh * .42, cy + Math.sin(an) * rh); g.arc(cx + Math.cos(an) * rw, cy + Math.sin(an) * rh, rh * .42, 0, Math.PI * 2); }
        g.fillStyle = col.nube; g.fill(); g.strokeStyle = col.tinta; g.lineWidth = 7; g.stroke();
        g.beginPath(); g.ellipse(cx, cy, rw * .98, rh * .98, 0, 0, 7); g.fill();       // tapa las costuras de adentro
        for (let i = 0; i < 3; i++) { const on = Math.floor(t * 3) % 4 > i; g.globalAlpha = on ? 1 : .25;
          g.beginPath(); g.arc(cx - rw * .42 + i * rw * .42, cy, rh * .16, 0, 7); g.fillStyle = col.tinta; g.fill(); }
        g.globalAlpha = 1;
      }
    }
    if (accion === 'festejar') {
      // destellos que revientan alrededor de la cabeza, en oleadas
      for (let i = 0; i < 7; i++) {
        const fase = (t * 1.6 + hash2(i, 5)) % 1, an = -Math.PI * .95 + i / 6 * Math.PI * .9;
        const d = R * 1.1 + Rt * (.2 + fase * .6), s = Math.sin(fase * Math.PI);
        if (s <= .05) continue;
        const x = hx + Math.cos(an) * d, y = hy + Math.sin(an) * d;
        if (i % 2) _estrellita(g, x, y, Rt * .17 * s + 6, col);
        else { g.globalAlpha = s; g.beginPath(); g.moveTo(hx + Math.cos(an) * (d - Rt * .3), hy + Math.sin(an) * (d - Rt * .3)); g.lineTo(x, y); _contorno(g, col.tinta, 8); g.globalAlpha = 1; }
      }
    }
    if (accion === 'hablar') {
      // rayitas de voz que laten junto a la boca
      const k = clamp(t / .3), v = .55 + .45 * Math.abs(Math.sin(t * 9));
      const bx = hx + lado * R * 1.02, by = hy + R * .2;
      for (let i = 0; i < 3; i++) { const an = (i - 1) * .55; g.globalAlpha = k * v;
        g.beginPath(); g.moveTo(bx + lado * Math.cos(an) * Rt * .14, by + Math.sin(an) * Rt * .3); g.lineTo(bx + lado * Math.cos(an) * Rt * .4, by + Math.sin(an) * Rt * .52); _contorno(g, col.tinta, 8); }
      g.globalAlpha = 1;
    }
    if (accion === 'sorpresa') {
      // signo de admiración que brinca junto a la cabeza (arriba suele ir el globo) + rayitas de susto
      const k = back(clamp(t / .3)), x = dentroX(hx + lado * (R * 1.05 + Rt * .25), Rt * .4), y = dentroY(hy - R * .85, Rt * .6);
      g.save(); g.translate(x, y); g.rotate(lado * .18); g.scale(k, k);
      g.font = `900 ${Math.round(Rt * 1.1)}px ${LETRA_LIMPIA}`; g.textAlign = 'center'; g.textBaseline = 'middle';
      g.lineWidth = Rt * .12; g.strokeStyle = col.tinta; g.lineJoin = 'round'; g.strokeText('!', 0, 0); g.fillStyle = col.acento; g.fillText('!', 0, 0);
      g.restore();
      for (let i = 0; i < 3; i++) { g.globalAlpha = k;
        const a2 = lado > 0 ? -Math.PI / 2 - (.35 + i * .35) : -Math.PI / 2 + (.35 + i * .35);
        g.beginPath(); g.moveTo(hx + Math.cos(a2) * (R + Rt * .1), hy + Math.sin(a2) * (R + Rt * .1)); g.lineTo(hx + Math.cos(a2) * (R + Rt * .38), hy + Math.sin(a2) * (R + Rt * .38)); _contorno(g, col.tinta, 8); }
      g.globalAlpha = 1;
    }
    if (accion === 'caminar' && !cortado) {
      // nubecitas de polvo en los pies, dos por paso
      for (let i = 0; i < 4; i++) {
        const fase = (t * 2.6 + i * .5) % 2 / 2, s = Math.sin(fase * Math.PI);
        if (fase > .6) continue;
        const x = baseX - lado * (W0 * .28 + fase * 80) + (i % 2 ? 20 : -20), y = baseY - 12 - fase * 30;
        g.globalAlpha = s * .8; g.beginPath(); g.arc(x, y, 12 + fase * 30, 0, 7); g.fillStyle = '#ffffff'; g.fill(); _contorno(g, col.tinta, 4);
      }
      g.globalAlpha = 1;
    }
    g.restore();
  }

  function dibujar(ctx, x, y, { accion = 'quieto', t = 0, mira = 1, escala = 1, sombra = true, hacia = null } = {}) {
    hacia = hacia || (mira < 0 ? 'izq' : 'der');
    let tq = t, tiembla = 0;
    if (estilo === 'recorte-papel') {                   // stop-motion: 12 poses por segundo con un leve temblor de mano
      const q = Math.floor(t * 12); tq = q / 12; tiembla = (hash2(q, 7) - .5);
    }
    // 1. el cuadro sin deformar: imagen + brazos + párpados + boca
    cg.clearRect(0, 0, cuadro.width, alto);
    const p = pose(accion, tq, mira < 0 ? ({ izq: 'der', der: 'izq' }[hacia] || hacia) : hacia);
    for (const b of BRAZOS) {                           // los brazos van DETRÁS del cuerpo: al subirlos no tapan la cara
      const ang = (b.lado === 'izq' ? p.bI : p.bD) * b.sgn;
      cg.save(); cg.translate(b.hombro[0], b.hombro[1]); cg.rotate(ang); cg.translate(-b.hombro[0], -b.hombro[1]); cg.drawImage(b.capa, 0, 0); cg.restore();
    }
    cg.drawImage(base, 0, 0);
    const cierra = C && C.ojos.length ? parpadeo(tq) : 0;
    if (cierra > 0) {
      C.ojos.forEach(([ox, oy], i) => {
        const w = C.ojoAncho * .66, h = C.ojoAlto * .66, top = oy - h;
        if (C.foto) {
          // FOTO: el párpado es la piel REAL de encima del ojo, estirada hacia abajo, con máscara difuminada
          // (un color plano se ve como un parche pegado sobre el ojo)
          const pw = Math.ceil(w * 3), ph = Math.ceil(h * 3.4);
          párpado.width = pw; párpado.height = ph; const pg = párpado.getContext('2d');
          const x0 = ox - pw / 2, y0 = top - h * .7, baja = h * 2.2 * cierra + h * .45;
          pg.drawImage(base, x0, top - h * 1.25, pw, h * .95, 0, 0, pw, baja);          // la franja de piel entre la ceja y el ojo
          pg.globalCompositeOperation = 'destination-in';
          pg.save(); pg.translate(pw / 2, ph * .42); pg.scale(1, (h * 1.25) / (w * 1.25));
          const gr = pg.createRadialGradient(0, 0, w * .55, 0, 0, w * 1.25);
          gr.addColorStop(0, 'rgba(0,0,0,1)'); gr.addColorStop(1, 'rgba(0,0,0,0)');
          pg.fillStyle = gr; pg.fillRect(-pw, -ph * 3, pw * 2, ph * 6); pg.restore();
          pg.globalCompositeOperation = 'source-over';
          cg.drawImage(párpado, x0, y0);
          if (cierra > .6) {                            // la línea de las pestañas, suave
            const yl = top + h * 2 * cierra - h * .15;
            cg.save(); cg.filter = 'blur(1px)'; cg.strokeStyle = C.linea; cg.lineWidth = Math.max(2, C.ojoAncho * .07); cg.lineCap = 'round';
            cg.globalAlpha = .6 * clamp((cierra - .6) / .3);
            cg.beginPath(); cg.moveTo(ox - w * .85, yl - h * .2); cg.quadraticCurveTo(ox, yl + h * .3, ox + w * .85, yl - h * .2); cg.stroke(); cg.restore();
          }
          return;
        }
        // DIBUJO: párpado de caricatura que baja desde arriba del ojo
        cg.save(); cg.beginPath(); cg.ellipse(ox, oy, w * 1.05, h * 1.05, 0, 0, Math.PI * 2); cg.clip();
        cg.fillStyle = C.pieles[i]; cg.fillRect(ox - w * 1.2, top - h * .2, w * 2.4, h * 2.2 * cierra + h * .2);
        cg.restore();
        if (cierra > .6) {
          const yl = top + h * 2 * cierra;
          cg.strokeStyle = C.linea; cg.lineWidth = Math.max(2, C.ojoAncho * .14); cg.lineCap = 'round';
          cg.globalAlpha = clamp((cierra - .6) / .3);
          cg.beginPath(); cg.moveTo(ox - w * .8, yl - h * .15); cg.quadraticCurveTo(ox, yl + Math.min(h, w) * .35, ox + w * .8, yl - h * .15); cg.stroke();
          cg.globalAlpha = 1;
        }
      });
    }
    if (C && C.boca && accion === 'hablar') {
      const a = boca(tq);
      const [bx, by] = C.boca;
      if (a > 0 && C.foto && C.caraAlto) {
        // FOTO: nada de disco negro. Se estira la mandíbula del labio a la barbilla (columna por columna,
        // con caída suave hacia las mejillas) y se oscurece apenas la línea de los labios: se lee la boca abierta.
        const y0 = by - C.bocaAlto * .05, y1 = Math.min(alto - 1, by + C.caraAlto * .42), h0 = y1 - y0;
        const mitad = Math.max(C.bocaAncho * 1.1, C.caraAncho * .42), colw = 3;
        for (let xx = Math.floor(bx - mitad); xx < bx + mitad; xx += colw) {
          const u = (xx + colw / 2 - bx) / mitad, peso = Math.cos(clamp(Math.abs(u)) * Math.PI / 2) ** 2;
          const h1 = h0 * (1 + a * .14 * peso);
          cg.drawImage(base, xx, y0, colw, h0, xx, y0, colw, h1);
        }
        cg.save(); cg.globalCompositeOperation = 'multiply'; cg.filter = `blur(${Math.max(1.5, C.bocaAlto * .35)}px)`;
        cg.fillStyle = `rgba(80,25,35,${.55 * a})`;
        cg.beginPath(); cg.ellipse(bx, by + C.bocaAlto * .22 * a, C.bocaAncho * .34, C.bocaAlto * (.18 + .3 * a), 0, 0, Math.PI * 2); cg.fill();
        cg.restore();
      } else if (a > 0) {
        // DIBUJO: boca abierta de caricatura sobre la boca que trae el personaje
        const bw = C.bocaAncho * .42, bh = Math.max(C.bocaAlto * .7, C.bocaAncho * .24) * a;
        cg.fillStyle = C.bocaColor || 'rgba(70,20,28,.96)'; cg.beginPath(); cg.ellipse(bx, by + bh * .2, bw, bh, 0, 0, Math.PI * 2); cg.fill();
        cg.fillStyle = 'rgba(255,120,130,.9)'; cg.beginPath(); cg.ellipse(bx, by + bh * .75, bw * .55, bh * .35, 0, 0, Math.PI * 2); cg.fill();   // lengüita
      }
    }
    // 2. deformación: squash/stretch con el pivote en la base + flexión por franjas (la base no se mueve)
    const W0 = cuadro.width * escala, H0 = alto * escala;
    const gira = p.gira + tiembla * .012, dxT = tiembla * 3;
    if (sombra) {                                       // sombra de contacto: núcleo oscuro + halo suave; se achica al subir
      const s = 1 - clamp(p.dy / (alto * .4)) * .55;
      ctx.save(); ctx.filter = 'blur(10px)'; ctx.fillStyle = `rgba(20,12,30,${.18 * s})`;
      ctx.beginPath(); ctx.ellipse(x, y + 4, W0 * .42 * s, W0 * .075 * s, 0, 0, Math.PI * 2); ctx.fill(); ctx.restore();
      ctx.save(); ctx.filter = 'blur(3px)'; ctx.fillStyle = `rgba(20,12,30,${.3 * s * s})`;
      ctx.beginPath(); ctx.ellipse(x, y + 2, W0 * .27 * s, W0 * .03 * s, 0, 0, Math.PI * 2); ctx.fill(); ctx.restore();
    }
    const N = 36;                                       // franjas horizontales
    const pinta = (dest, src, ox, oy) => {
      dest.save();
      dest.translate(x + dxT + ox, y - p.dy * escala + oy); dest.rotate(gira * mira); dest.scale(mira * p.sx, p.sy);
      for (let i = 0; i < N; i++) {
        const y0 = i * alto / N, h = alto / N + 1;     // +1: sin rendijas entre franjas
        const altura = 1 - (y0 + h / 2) / alto;         // 0 en la base, 1 arriba
        const dx = p.curva * altura * altura * H0;
        dest.drawImage(src, 0, y0, cuadro.width, h, -W0 / 2 + dx, -H0 + y0 * escala, W0, h * escala);
      }
      dest.restore();
    };
    if (estilo === 'recorte-papel') {                   // sombra corrida y dura de recorte pegado sobre el fondo
      sog.clearRect(0, 0, silo.width, alto); sog.globalCompositeOperation = 'source-over'; sog.drawImage(cuadro, 0, 0);
      sog.globalCompositeOperation = 'source-in'; sog.fillStyle = 'rgba(40,25,15,1)'; sog.fillRect(0, 0, silo.width, alto); sog.globalCompositeOperation = 'source-over';
      ctx.save(); ctx.globalAlpha = .28; ctx.filter = 'blur(3px)'; pinta(ctx, silo, 10 * escala, 12 * escala); ctx.restore();
    }
    pinta(ctx, cuadro, 0, 0);
    // 3. los gestos, sobre la posición real de la cabeza (misma deformación, aproximada)
    const alturaCab = 1 - cabeza.y / alto;
    const hx = x + dxT + mira * ((cabeza.x - cuadro.width / 2) * escala * p.sx + p.curva * alturaCab * alturaCab * H0) + Math.sin(gira * mira) * (alto - cabeza.y) * escala;
    const hy = y - p.dy * escala - (alto - cabeza.y) * escala * p.sy;
    const lado = hacia === 'izq' ? -1 : 1;
    gesto(ctx, accion, tq, hx, hy, cabeza.r * escala, accion === 'señalar' ? lado : mira, hacia, x, y, W0);
  }

  return { ancho: base.width, alto, dibujar, cara: C, cortado, cabeza, estilo, brazos: BRAZOS.length };
}

// ---------- la cara: un objeto ya escrito, o la ruta al JSON de preparar-foto.mjs ----------
// Con doble clic en Chrome normal la ruta puede no cargar (file://): entonces el títere sale sin parpadeo, sin romperse.
function cargarCara(cara) {
  if (!cara) return Promise.resolve(null);
  if (typeof cara === 'object') return Promise.resolve(cara);
  return new Promise(ok => {
    try {
      const x = new XMLHttpRequest(); x.open('GET', cara);
      x.onload = () => { try { ok(JSON.parse(x.responseText)); } catch (e) { ok(null); } };
      x.onerror = () => ok(null); x.send();
    } catch (e) { ok(null); }
  });
}
