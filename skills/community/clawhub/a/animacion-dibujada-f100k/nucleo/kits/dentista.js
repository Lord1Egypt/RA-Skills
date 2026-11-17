// KIT DENTISTA — se carga después de nucleo/objetos.js
(() => {
const MENTA = '#2bb3a3', CIELO = '#6ec3ff', BLANCO = '#ffffff', GRIS = '#c3c8d2';

function muela(cariada) {
  const c = pSuave([[-38, -78], [-20, -92], [0, -84], [20, -92], [38, -78], [36, -52], [28, -36], [22, -8], [12, -2], [6, -22], [0, -30], [-6, -22], [-12, -2], [-22, -8], [-28, -36], [-36, -52]], true, .9);
  F(c, cariada ? '#f3e7c4' : BLANCO, { sombra: 12, k: .9, brillo: cariada ? null : [-28, -80, 10, 20] });
  if (cariada) {
    F(pSuave([[6, -76], [20, -70], [16, -58], [4, -60]], true, .9), '#8a5a3b', { linea: false });
    F(pEl(-18, -60, 5, 4), '#a8763f', { linea: false });
    L(pLinea([[-4, -88], [0, -76], [-6, -66]]), '#8a5a3b', .6);
  } else {
    estrellasDiente();
  }
}
function estrellasDiente() { [[40, -94, 10], [48, -70, 6]].forEach(([x, y, r]) => F(pEstrella(x, y, r, r * .35, 4, 0), '#ffe27a', { linea: false })); }

registrarObjeto('diente', () => muela(false), { ancho: 36 });
registrarObjeto('diente-caries', () => muela(true), { ancho: 36 });

registrarObjeto('cepillo', () => {
  // cepillo grande, inclinado, con su montañita de pasta: mango con agarre, cabeza, cerdas en dos colores
  _g.save(); _g.translate(-38, -4); _g.rotate(-1.0);
  F(pRR(-4, -10, 104, 20, 10), CIELO, { sombra: 'abajo:2', brillo: [6, -6, 70, 4] });
  F(pRR(20, -6, 40, 12, 6), claro(CIELO, .45), { linea: false });                         // agarre de goma
  for (let i = 0; i < 4; i++) L(pLinea([[26 + i * 9, -4], [26 + i * 9, 4]]), CIELO, .5);
  F(pRR(96, -9, 34, 16, 7), '#e9f7ff', { sombra: 'abajo:2' });
  F(pRR(98, -30, 31, 22, 4), '#bfe6ff', { sombra: 'abajo:-14' });                      // un solo bloque de cerdas con contorno
  _g.save(); _g.clip(pRR(98, -30, 31, 22, 4)); for (let i = 0; i < 3; i++) F(pRR(101 + i * 10, -31, 5, 24, 0), BLANCO, { linea: false }); _g.restore();
  F(pSuave([[96, -30], [104, -42], [114, -36], [124, -46], [132, -32]], true, .8), '#ffffff', { sombra: 'abajo:-34' });
  L(pSuave([[100, -35], [113, -39], [127, -34]], false), MENTA, .9);
  _g.restore();
}, { ancho: 44 });

registrarObjeto('pasta-dental', () => {
  _g.save(); _g.translate(0, -6); _g.rotate(-.12);
  F(pRR(-14, -20, 28, 18, 5), MENTA, { sombra: 6 });                                   // tapa
  F(pSuave([[-22, -20], [22, -20], [26, -60], [34, -92], [-34, -92], [-26, -60]], true, .4), '#ffffff', { sombra: 12 });
  F(pRR(-36, -98, 72, 8, 2), GRIS);
  F(pPoli([[-24, -70], [24, -70], [23, -50], [-23, -50]]), MENTA, { linea: false });
  T('PASTA', 0, -60, 11, '#ffffff');
  _g.restore();
}, { ancho: 34 });

registrarObjeto('silla-dental', () => {
  L(pSuave([[26, -20], [30, -80], [52, -96], [62, -92]], false), GRIS, 1.4);             // brazo de la lámpara
  F(pEl(56, -92, 14, 8, .4), '#fff1b8');
  F(pRR(-22, -6, 44, 6, 3), '#9aa2ae'); F(pRR(-6, -26, 12, 22, 3), '#9aa2ae');
  F(pSuave([[-52, -64], [-40, -60], [-16, -34], [30, -34], [40, -40], [44, -30], [34, -24], [-22, -24], [-50, -50]], true, .6), MENTA, { sombra: 'abajo:-32' });
  F(pRR(-62, -76, 22, 16, 7), claro(MENTA, .1));                                        // cabecera
  F(pRR(-20, -46, 34, 8, 4), claro(MENTA, .25), { linea: false });
}, { ancho: 52 });

registrarObjeto('espejo-dental', () => {
  _g.save(); _g.translate(0, -4); _g.rotate(-.35);
  F(pRR(-5, -70, 10, 70, 5), GRIS, { sombra: 1 });
  [-56, -46, -36].forEach(y => L(pLinea([[-4, y], [4, y]]), '#8a909c', .4));
  L(pLinea([[0, -70], [6, -82]]), '#8a909c', .8);
  F(pEl(10, -92, 14, 14), '#9aa2ae'); F(pEl(10, -92, 10, 10), '#dff3fb', { linea: false }); F(pEl(6, -96, 3, 4), BLANCO, { linea: false });
  _g.restore();
}, { ancho: 20 });

registrarObjeto('sonrisa', () => {
  const labios = pSuave([[-50, -62], [-26, -70], [0, -64], [26, -70], [50, -62], [36, -34], [0, -22], [-36, -34]], true, .8);
  F(labios, '#f06a7a', { sombra: 'abajo:-44' });
  const boca = pSuave([[-40, -60], [0, -56], [40, -60], [26, -40], [0, -34], [-26, -40]], true, .8);
  F(boca, '#6b2a36', { linea: false });
  _g.save(); _g.clip(boca);
  for (let i = -3; i <= 3; i++) F(pRR(i * 11 - 5, -62, 10, 13, 3), BLANCO, { linea: false });
  for (let i = -2; i <= 2; i++) F(pRR(i * 11 - 5, -42, 10, 10, 3), '#f4f4f4', { linea: false });
  _g.restore();
  estrellasDiente();
}, { ancho: 48 });

registrarObjeto('hilo-dental', () => {
  F(pRR(-26, -56, 52, 54, 12), MENTA, { sombra: 12 });
  F(pEl(0, -28, 14, 14), claro(MENTA, .4), { linea: false });
  F(pRR(-20, -64, 40, 12, 6), claro(MENTA, .2));
  L(pSuave([[6, -60], [18, -78], [34, -84], [46, -100]], false), '#ffffff', .8);
  L(pSuave([[6, -60], [18, -78], [34, -84], [46, -100]], false), '#bfe6ff', .3);
}, { ancho: 30 });

registrarObjeto('lampara-dental', () => {
  // la lámpara de consultorio: poste, brazo articulado y cabeza ovalada que alumbra hacia abajo
  if (_modo === 'vector') { _g.save(); _g.globalAlpha = .28; _g.fillStyle = '#fff1b8'; _g.fill(pPoli([[18, -66], [50, -74], [70, 0], [-4, 0]])); _g.restore(); }
  F(pEl(-34, -3, 22, 6), '#8b929e', { sombra: -34 });
  F(pRR(-38, -76, 9, 74, 4), '#b8bfca', { sombra: -34 });
  F(pEl(-33, -76, 7, 7), '#8b929e');
  _g.save(); _g.translate(-33, -76); _g.rotate(-.22); F(pRR(0, -5, 52, 10, 5), '#b8bfca', { sombra: 'abajo:0' }); _g.restore();
  F(pEl(18, -88, 6, 6), '#8b929e');
  _g.save(); _g.translate(34, -82); _g.rotate(.28);
  F(pEl(0, 0, 26, 15), '#e9edf2', { sombra: 'abajo:2', brillo: [-16, -11, 18, 5] });
  F(pEl(0, 7, 18, 6), '#fff1b8', { linea: false });
  _g.restore();
}, { ancho: 40 });

registrarObjeto('enjuague', () => {
  F(pRR(-12, -100, 24, 18, 4), '#ffffff', { sombra: 4 });
  F(pSuave([[-12, -84], [12, -84], [26, -64], [26, -6], [-26, -6], [-26, -64]], true, .4), '#bfe6ff', { sombra: 10 });
  _g.save(); _g.clip(pSuave([[-12, -84], [12, -84], [26, -64], [26, -6], [-26, -6], [-26, -64]], true, .4));
  F(pRR(-30, -58, 60, 60, 0), '#3fa9f5', { linea: false }); _g.restore();
  F(pRR(-18, -48, 36, 24, 4), '#ffffff'); F(pEstrella(0, -36, 8, 3, 4, 0), MENTA, { linea: false });
}, { ancho: 30 });

registrarEscenario('clinica-dental', p => {
  const g = _g;
  g.fillStyle = _reg(p.pared); g.fillRect(0, 0, W, PISO_Y);
  g.fillStyle = _reg(claro(p.pared, .45)); g.fillRect(0, 980, W, PISO_Y - 980);         // azulejo bajo
  g.fillStyle = _reg(oscuro(p.pared, .93));
  for (let y = 980; y < PISO_Y; y += 70) g.fillRect(0, y, W, 4);
  for (let y = 980, f = 0; y < PISO_Y; y += 70, f++) for (let x = (f % 2) * 45; x < W; x += 90) g.fillRect(x, y, 4, 70);
  // cartel con diente a la derecha y repisa con frascos a la izquierda
  F(pRR(800, 720, 210, 220, 16), '#ffffff'); F(pEl(905, 810, 44, 40), claro(p.acento, .7), { linea: false });
  F(pSuave([[875, 790], [890, 776], [905, 784], [920, 776], [935, 790], [930, 815], [920, 840], [912, 845], [905, 826], [898, 845], [890, 840], [880, 815]], true, .9), '#ffffff');
  F(pRR(40, 900, 240, 16, 6), oscuro(p.pared, .8));
  [[80, p.acento], [150, p.acento2], [220, '#ffffff']].forEach(([x, c]) => { F(pRR(x - 22, 820, 44, 80, 10), c); F(pRR(x - 16, 806, 32, 16, 5), '#ffffff'); });
  g.fillStyle = _reg(p.piso); g.fillRect(0, PISO_Y, W, H - PISO_Y);
  g.fillStyle = _reg(oscuro(p.piso, .93)); for (let x = 0; x < W; x += 180) g.fillRect(x, PISO_Y, 4, H);
  for (let y = PISO_Y + 120; y < H; y += 150) g.fillRect(0, y, W, 4);
  F(pRR(-10, PISO_Y - 8, W + 20, 20, 4), p.acento);
}, t => {   // vivo: el diente del cartel destella cada tanto
  const f = (t % 2.4) / 2.4, a = Math.sin(clamp(f / .35) * Math.PI);
  if (a > 0) { estrellita(946, 782, 26 * a, '255,255,255', a); estrellita(962, 812, 12 * a, '255,244,180', a * .8); }
});

registrarKit('dentista', {
  nombre: 'Dentista',
  paleta: { fondo: '#e6f6f4', pared: '#d5f0ec', piso: '#eef3f5', acento: '#2bb3a3', acento2: '#6ec3ff', tinta: '#1f3340' },
  escenario: 'clinica-dental',
  objetos: ['diente', 'diente-caries', 'cepillo', 'pasta-dental', 'silla-dental', 'espejo-dental', 'sonrisa', 'hilo-dental', 'lampara-dental', 'enjuague'],
});
})();
