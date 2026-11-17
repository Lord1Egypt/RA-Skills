// KIT CENTRO ESTÉTICO — se carga después de nucleo/objetos.js
(() => {
const NUDE = '#f3d9cc', ROSADO = '#e8a598', ORO = '#c9a063', SALVIA = '#9ecfb8', SALVIA_F = '#5f9e84', BLANCO = '#fbf8f4', AMBAR = '#c9772f', LAVANDA = '#c7b8e8';

function rollo(cx, cy, r, col) {                          // toalla enrollada vista de frente: espiral
  F(pEl(cx, cy, r, r), col, { sombra: cx + r * .35, k: .88 });
  L(pSuave([[cx, cy], [cx + r * .28, cy - r * .1], [cx + r * .2, cy + r * .32], [cx - r * .3, cy + r * .28], [cx - r * .45, cy - r * .2], [cx - r * .05, cy - r * .6], [cx + r * .55, cy - r * .45], [cx + r * .72, cy + r * .1]], false, .9), oscuro(col, .78), .6);
}

registrarObjeto('camilla', () => {                     // camilla de cabina: alta, con respaldo levantado y toalla
  [[-50, '#b7bdc7'], [42, '#b7bdc7']].forEach(([x, c]) => F(pRR(x, -40, 8, 38, 3), c));            // patas
  F(pRR(-50, -14, 100, 6, 3), '#d0d5dd', { linea: false });                                         // travesaño
  F(pRR(-60, -52, 120, 14, 5), '#e9e4df', { sombra: 'abajo:-44' });                                 // estructura
  F(pSuave([[-60, -52], [-60, -68], [22, -68], [38, -94], [56, -88], [48, -52]], true, .3), NUDE, { sombra: 'abajo:-60', brillo: [-52, -66, 70, 4] });
  F(pRR(-56, -78, 70, 12, 6), BLANCO, { sombra: 'abajo:-70' });                                     // sábana doblada a los pies
  L(pLinea([[-50, -72], [8, -72]]), '#e3dbd3', .4);
  rollo(40, -100, 11, SALVIA);                                                                       // toalla en la cabecera
}, { ancho: 62 });

registrarObjeto('toalla-enrollada', () => {             // tres rollitos en pirámide
  rollo(-22, -20, 20, BLANCO); rollo(22, -20, 20, SALVIA); rollo(0, -54, 20, NUDE);
  F(pEl(0, -78, 5, 5), SALVIA_F, { linea: false });
  L(pSuave([[0, -78], [-6, -90], [-2, -98]], false), SALVIA_F, .6);                     // ramita de eucalipto
  F(pEl(-5, -90, 5, 3, -.6), SALVIA, { linea: false }); F(pEl(3, -96, 5, 3, .5), SALVIA, { linea: false });
}, { ancho: 44 });

registrarObjeto('velas', t => {
  [[-26, 60, '#fbf0e4'], [4, 84, '#f3ddd0'], [30, 48, '#fbf0e4']].forEach(([x, h, c], i) => {
    F(pRR(x - 13, -h, 26, h - 2, 5), c, { sombra: x + 5 });
    F(pEl(x, -h, 13, 3.5), oscuro(c, .92), { linea: false });
    L(pLinea([[x, -h], [x, -h - 7]]), '#3a2c2c', .5);
    const f = 1 + .14 * Math.sin(t * 15 + i * 2) + .05 * Math.sin(t * 27 + i), inc = Math.sin(t * 9 + i) * 1.6;
    F(pSuave([[x, -h - 6], [x + 5 * f, -h - 12], [x + inc, -h - 26 * (.9 + .1 * f)], [x - 5 * f, -h - 12]], true, .9), '#ffb347', { linea: false });
    F(pSuave([[x, -h - 7], [x + 2.5, -h - 11], [x + inc * .5, -h - 17], [x - 2.5, -h - 11]], true, .9), '#fff1b8', { linea: false });
  });
  F(pEl(0, -2, 52, 5), '#e0d5cc', { linea: false });
}, { ancho: 48, anima: true });

registrarObjeto('crema', () => {                          // tarro con tapa y crema abierta
  F(pRR(-40, -52, 80, 50, 12), BLANCO, { sombra: 16, brillo: [-34, -46, 8, 34] });
  F(pRR(-40, -38, 80, 16, 0), ROSADO, { linea: false }); if (_modo === 'vector') L(pRR(-40, -52, 80, 50, 12), null, 1);
  F(pEl(0, -52, 38, 9), '#fff7f2');
  F(pSuave([[-14, -56], [-6, -66], [2, -60], [10, -70], [16, -58]], true, .8), '#ffffff', { sombra: 8 });   // copete de crema
  _g.save(); _g.translate(30, -64); _g.rotate(.5);                                          // la tapa apoyada atrás
  F(pRR(-36, -12, 72, 18, 7), ORO, { sombra: 10, brillo: [-30, -9, 40, 4] });
  _g.restore();
}, { ancho: 48 });

registrarObjeto('gotero', () => {                         // frasco ámbar con gotero
  F(pEl(0, -94, 10, 10), '#3a2c2c');
  F(pRR(-9, -90, 18, 20, 4), '#3a2c2c');
  F(pRR(-13, -72, 26, 10, 3), ORO, { brillo: [-10, -71, 12, 3] });
  F(pSuave([[-13, -62], [13, -62], [26, -46], [28, -8], [22, -2], [-22, -2], [-28, -8], [-26, -46]], true, .5), AMBAR, { sombra: 8, brillo: [-20, -44, 7, 32] });
  F(pRR(-18, -36, 36, 22, 3), BLANCO, { linea: false });
  L(pLinea([[-12, -28], [12, -28]]), '#d9c7bb', .5); L(pLinea([[-8, -21], [8, -21]]), '#d9c7bb', .5);
}, { ancho: 30 });

registrarObjeto('espejo-ovalado', () => {                 // espejo de tocador con pie
  F(pRR(-26, -8, 52, 8, 4), ORO, { sombra: 10 });
  F(pRR(-4, -30, 8, 24, 3), ORO);
  F(pEl(0, -64, 34, 40), ORO, { sombra: 14 });
  F(pEl(0, -64, 27, 33), '#dcecf2', { linea: false });
  F(pPoli([[-16, -82], [-6, -86], [-20, -52], [-24, -58]]), '#ffffff', { linea: false });
  F(pPoli([[0, -88], [6, -90], [-10, -48], [-14, -50]]), '#ffffff', { linea: false });
}, { ancho: 36 });

registrarObjeto('aparato-facial', t => {                  // aparato genérico: base, pantallita y cabezal con cable
  F(pRR(-44, -60, 60, 58, 10), BLANCO, { sombra: 4 });
  F(pRR(-36, -52, 44, 26, 5), '#bfe6f2', { linea: false });
  L(pLinea([[-30, -38], [-20, -44], [-10, -34], [0, -42]]), SALVIA_F, .6);                 // onda en la pantalla
  [-30, -18, -6].forEach(x => F(pEl(x, -14, 4, 4), [ROSADO, SALVIA, ORO][(x + 30) / 12]));
  L(pSuave([[16, -30], [34, -24], [40, -52], [30, -74]], false), '#8a909c', .8);           // cable
  _g.save(); _g.translate(32, -78); _g.rotate(.35);
  F(pRR(-8, -8, 16, 34, 7), LAVANDA, { sombra: 2 });
  F(pEl(0, -12, 12, 7), '#e9e4f7', { brillo: [-8, -16, 8, 3] });
  _g.restore();
  const b = .5 + .5 * Math.sin(t * 5);
  if (_modo === 'vector') { _g.save(); _g.globalAlpha = .3 * b; F(pEl(28, -92, 12, 6), '#fff1a8', { linea: false }); _g.restore(); }
}, { ancho: 48, anima: true });

registrarObjeto('protector-solar', () => {
  _g.save(); _g.rotate(-.08);
  F(pRR(-12, -12, 24, 12, 3), '#ffb347');                                                   // tapa
  F(pSuave([[-22, -12], [22, -12], [26, -80], [24, -96], [-24, -96], [-26, -80]], true, .4), '#fff6d8', { sombra: 10, brillo: [-18, -88, 6, 60] });
  F(pRR(-26, -100, 52, 8, 3), '#f3dfa8');
  F(pEl(0, -58, 13, 13), '#ffb347', { linea: false });                                      // el sol
  for (let i = 0; i < 8; i++) { const a = i / 8 * Math.PI * 2; L(pLinea([[Math.cos(a) * 17, -58 + Math.sin(a) * 17], [Math.cos(a) * 22, -58 + Math.sin(a) * 22]]), '#ffb347', .55); }
  _g.restore();
}, { ancho: 30 });

registrarObjeto('toalla-doblada', () => {                 // «la toalla, cada cuánto se cambia»
  F(pRR(-46, -30, 92, 28, 8), BLANCO, { sombra: 'abajo:-14', k: .9 });
  F(pRR(-42, -58, 84, 28, 8), SALVIA, { sombra: 'abajo:-42', k: .88 });
  F(pRR(-42, -46, 84, 6, 0), SALVIA_F, { linea: false });
  F(pRR(-38, -84, 76, 26, 8), NUDE, { sombra: 'abajo:-70', k: .9 });
  L(pLinea([[-32, -72], [32, -72]]), oscuro(NUDE, .85), .4);
}, { ancho: 48 });

registrarObjeto('planta-monstera', () => {
  F(pPoli([[-26, -44], [26, -44], [20, -2], [-20, -2]]), '#e9e4df', { sombra: 8 });
  F(pRR(-28, -48, 56, 8, 3), '#d9d2cb');
  [[-26, -78, -.7, 26], [22, -86, .6, 28], [-2, -100, 0, 24]].forEach(([x, y, r, s]) => {
    L(pSuave([[0, -46], [x * .5, (y - 46) / 2 - 10], [x, y]], false), SALVIA_F, .6);
    _g.save(); _g.translate(x, y); _g.rotate(r);
    const hoja = pSuave([[0, s * .9], [-s * .95, s * .1], [-s * .7, -s * .75], [0, -s], [s * .7, -s * .75], [s * .95, s * .1]], true, .9);
    F(hoja, SALVIA, { sombra: 0, k: .82 });
    L(pLinea([[0, s * .8], [0, -s * .8]]), SALVIA_F, .45);
    [-1, 1].forEach(k => L(pLinea([[k * s * .5, -s * .1], [k * s * .95, -s * .2]]), '#fbf8f4', .55));   // los cortes de la hoja
    _g.restore();
  });
}, { ancho: 40 });

registrarObjeto('brocha-mascarilla', () => {
  _g.save(); _g.rotate(.35); _g.translate(0, -6);
  F(pRR(-5, -64, 10, 62, 5), '#d49a5f', { sombra: 1 });
  F(pRR(-7, -72, 14, 12, 2), ORO);
  F(pSuave([[-9, -72], [-12, -92], [0, -100], [12, -92], [9, -72]], true, .8), '#f7efe8', { sombra: 2 });
  F(pSuave([[-10, -86], [-11, -95], [0, -100], [11, -95], [10, -86]], true, .8), SALVIA, { linea: false });    // punta con mascarilla
  _g.restore();
  F(pEl(28, -12, 22, 10), '#ffffff', { sombra: 34 });                                         // cuenco
  F(pEl(28, -16, 16, 5), SALVIA, { linea: false });
}, { ancho: 44 });

registrarObjeto('bata', () => {                          // bata colgada en un gancho
  L(pSuave([[0, -96], [4, -104], [0, -110], [-4, -104]], false), '#8a909c', .8);
  L(pLinea([[-30, -84], [0, -98], [30, -84]]), '#8a909c', 1);
  F(pSuave([[-30, -86], [30, -86], [38, -60], [34, -4], [-34, -4], [-38, -60]], true, .4), BLANCO, { sombra: 12 });
  F(pPoli([[-30, -86], [0, -86], [0, -30], [-8, -30]]), '#f1ece6', { linea: false });
  L(pLinea([[-12, -86], [4, -40]]), '#d9d0c8', .6); L(pLinea([[12, -86], [-2, -52]]), '#d9d0c8', .6);
  F(pRR(-36, -46, 72, 8, 4), SALVIA);                                                         // cinturón
  F(pRR(14, -40, 7, 22, 3), SALVIA, { linea: false });
}, { ancho: 40 });

registrarObjeto('difusor', t => {                       // difusor de aroma: base de madera, cuerpo claro y vapor
  F(pRR(-30, -16, 60, 14, 6), '#c89a6a', { sombra: 16 });
  L(pLinea([[-24, -9], [24, -9]]), '#b3834f', .4);
  F(pSuave([[-24, -16], [-28, -40], [-18, -66], [0, -72], [18, -66], [28, -40], [24, -16]], true, .7), '#f5efe8', { sombra: 8, brillo: [-20, -58, 6, 22] });
  F(pRR(-24, -30, 48, 5, 2), '#9ecfb8', { linea: false });                                            // luz de colores
  F(pEl(0, -71, 7, 2.5), '#c9b9a8', { linea: false });
  for (let i = 0; i < 3; i++) {                                                                       // vapor que sube
    const f = (t * .6 + i / 3) % 1, y = -76 - f * 30, dx = Math.sin(f * 6 + i) * 5;
    const a = _modo === 'vector' ? .7 * Math.sin(f * Math.PI) : (f < .75 ? 1 : 0);
    if (a <= 0) continue;
    _g.save(); _g.globalAlpha = a; F(pEl(dx, y, 5 + f * 7, 4 + f * 5), '#dfe9ee', { linea: false }); _g.restore();
  }
}, { ancho: 32, anima: true });

registrarEscenario('cabina-estetica', p => {
  const g = _g;
  g.fillStyle = _reg(p.pared); g.fillRect(0, 0, W, PISO_Y);
  g.fillStyle = _reg(oscuro(p.pared, .95)); for (let x = 0; x < W; x += 90) g.fillRect(x, 0, 3, PISO_Y);         // panel fino de madera
  // nicho en arco, color salvia claro: se lee como cabina
  F(pSuave([[250, PISO_Y], [250, 900], [320, 770], [540, 715], [760, 770], [830, 900], [830, PISO_Y]], true, .6), claro(p.acento2, .55), { linea: false });
  L(pSuave([[250, PISO_Y], [250, 900], [320, 770], [540, 715], [760, 770], [830, 900], [830, PISO_Y]], false, .6), p.acento, .9);
  // repisa izquierda con frascos
  F(pRR(30, 960, 200, 16, 6), p.acento);
  [[62, 60, '#fbf8f4'], [112, 84, claro(p.acento2, .1)], [162, 50, '#c9772f'], [204, 40, '#fbf8f4']].forEach(([x, h, c]) => {
    F(pRR(x - 17, 960 - h, 34, h, 8), c, { sombra: x + 6 }); F(pRR(x - 8, 960 - h - 12, 16, 12, 3), p.acento);
  });
  // espejo redondo con marco dorado a la derecha y lámpara
  F(pEl(950, 900, 100, 100), p.acento, { sombra: 990 }); F(pEl(950, 900, 86, 86), '#e3eef1', { linea: false });
  F(pPoli([[900, 850], [930, 830], [880, 930], [868, 912]]), '#ffffff', { linea: false });
  L(pLinea([[930, 0], [930, 600]]), p.tinta, .5);
  F(pSuave([[880, 660], [890, 606], [970, 606], [980, 660]], true, .5), p.acento, { sombra: 930 });
  if (_modo === 'vector') { const gr = g.createRadialGradient(930, 680, 10, 930, 740, 330); gr.addColorStop(0, 'rgba(255,230,190,.6)'); gr.addColorStop(1, 'rgba(255,230,190,0)'); g.fillStyle = gr; g.fillRect(560, 640, 520, 520); }
  // hojas de planta asomando por el costado izquierdo
  [[-10, 1100, .8], [30, 1180, .4], [-20, 1260, 1.1]].forEach(([x, y, r]) => { g.save(); g.translate(x, y); g.rotate(r);
    F(pSuave([[0, 0], [60, -40], [150, -20], [200, 10], [140, 40], [60, 30]], true, .8), p.acento2, { sombra: 'abajo:8', k: .85 }); g.restore(); });
  // piso de madera clara
  g.fillStyle = _reg(p.piso); g.fillRect(0, PISO_Y, W, H - PISO_Y);
  g.fillStyle = _reg(oscuro(p.piso, .93)); for (let y = PISO_Y + 70; y < H; y += 80) g.fillRect(0, y, W, 5);
  for (let y = PISO_Y + 70, i = 0; y < H; y += 80, i++) for (let x = (i % 2) * 180 + 90; x < W; x += 360) g.fillRect(x, y, 5, 80);
  g.fillStyle = _reg(oscuro(p.piso, .85)); g.fillRect(0, PISO_Y, W, 14);
});

registrarKit('centro-estetico', {
  nombre: 'Estética',
  paleta: { fondo: '#f7efeb', pared: '#eed8cd', piso: '#e6d3c6', acento: '#c9a063', acento2: '#9ecfb8', tinta: '#3a2c2c' },
  escenario: 'cabina-estetica',
  objetos: ['camilla', 'crema', 'gotero', 'toalla-enrollada', 'velas', 'protector-solar', 'espejo-ovalado', 'aparato-facial', 'toalla-doblada', 'planta-monstera', 'brocha-mascarilla', 'bata', 'difusor'],
});
registrarKit('estetica', KITS['centro-estetico']);
})();
