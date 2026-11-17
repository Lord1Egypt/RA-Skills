// KIT MAKEUP ARTIST — se carga después de nucleo/objetos.js
(() => {
const ROSA = '#ff8fab', ROSA_F = '#e0527a', NUDE = '#e8b89a', DORADO = '#e9b949', NEGRO = '#2d2a33', LILA = '#c9a7ef', METAL = '#c3c8d2', BLANCO = '#ffffff';

function brocha(x, y, rot, largo, cerda, col) {          // brocha suelta: mango + casquillo + cerdas
  _g.save(); _g.translate(x, y); _g.rotate(rot);
  F(pRR(-4, -largo * .55, 8, largo * .55, 4), col, { sombra: 1 });
  F(pRR(-5.5, -largo * .72, 11, largo * .18, 2), METAL, { sombra: 1 });
  F(pSuave([[-5, -largo * .72], [-cerda, -largo * .86], [-cerda * .6, -largo], [0, -largo * 1.03], [cerda * .6, -largo], [cerda, -largo * .86], [5, -largo * .72]], true, .8), '#6b4a3a', { sombra: 1 });
  F(pSuave([[-cerda * .6, -largo * .95], [0, -largo * 1.03], [cerda * .6, -largo * .95], [0, -largo * .9]], true, .8), ROSA, { linea: false });
  _g.restore();
}

registrarObjeto('brocha', () => { brocha(0, 0, .12, 100, 13, NEGRO); }, { ancho: 18 });

registrarObjeto('vaso-brochas', () => {
  brocha(-14, -40, -.28, 92, 11, '#f0c0cf');
  brocha(2, -40, .04, 100, 14, NEGRO);
  brocha(16, -40, .3, 86, 8, DORADO);
  F(pRR(-26, -50, 52, 48, 8), LILA, { sombra: 12 });
  F(pRR(-26, -50, 52, 10, 5), claro(LILA, .3));
}, { ancho: 34 });

registrarObjeto('paleta-sombras', () => {
  _g.save(); _g.translate(0, -34);
  F(pRR(-54, -28, 108, 54, 8), NEGRO, { sombra: 'abajo:16' });
  const cols = ['#f6d5c5', '#e7a98f', '#c9785c', '#8a4a3a', '#f3c5dc', '#d98ab0', '#a35c8a', '#5c3a5a'];
  cols.forEach((c, i) => { const x = -42 + (i % 4) * 22, y = -18 + Math.floor(i / 4) * 22; F(pRR(x, y, 18, 18, 3), c, { linea: false, brillo: [x + 2, y + 2, 6, 4] }); });
  _g.restore();
  F(pRR(-54, -76, 108, 16, 6), '#3d3a45', { sombra: 20 });                      // tapa abierta atrás
  F(pRR(-40, -74, 80, 10, 3), '#9fd8ff', { linea: false });
}, { ancho: 56 });

registrarObjeto('labial', () => {
  F(pRR(-15, -44, 30, 42, 4), DORADO, { sombra: 4, brillo: [-11, -40, 5, 34] });
  F(pRR(-12, -58, 24, 16, 2), '#c9c9d2', { sombra: 4 });
  F(pPoli([[-9, -58], [9, -58], [9, -80], [-9, -94]]), ROSA_F, { sombra: 3 });
  F(pRR(22, -46, 22, 44, 5), NEGRO, { sombra: 36 });                            // la tapa, al lado
}, { ancho: 30 });

registrarObjeto('rubor', () => {                          // compacto abierto con rubor
  F(pEl(0, -76, 38, 22), '#3d3a45', { sombra: 8 });
  F(pEl(0, -76, 30, 16), '#bfe6ff', { linea: false });
  F(pEl(-10, -80, 6, 9, -.5), BLANCO, { linea: false });
  F(pEl(0, -24, 42, 22), NEGRO, { sombra: 10 });
  F(pEl(0, -28, 32, 15), '#ff9fb1', { linea: false, brillo: [-18, -38, 12, 6] });
  [[-10, -30], [8, -26], [0, -34]].forEach(([x, y]) => F(pEl(x, y, 2, 2), '#ffc3cf', { linea: false }));
}, { ancho: 42 });

registrarObjeto('base-maquillaje', () => {
  F(pRR(-22, -76, 44, 74, 10), NUDE, { sombra: 8, brillo: [-17, -70, 6, 58] });
  F(pRR(-10, -96, 20, 22, 4), NEGRO);
  F(pRR(-14, -56, 28, 24, 4), '#fff4ec', { linea: false });
  L(pLinea([[-8, -48], [8, -48]]), '#c9a28a', .5); L(pLinea([[-8, -40], [4, -40]]), '#c9a28a', .5);
}, { ancho: 26 });

registrarObjeto('rimel', () => {
  _g.save(); _g.rotate(.2);
  F(pRR(-9, -58, 18, 56, 8), '#ff6f9c', { sombra: 1, brillo: [-6, -54, 4, 44] });
  F(pRR(-7, -100, 14, 44, 6), NEGRO, { sombra: 1 });
  _g.restore();
  // el cepillito afuera
  _g.save(); _g.translate(30, -10); _g.rotate(.9);
  F(pRR(-2, -46, 4, 30, 2), METAL, { linea: false });
  F(pRR(-5, -64, 10, 20, 5), NEGRO);
  _g.restore();
}, { ancho: 30 });

registrarObjeto('esponja', () => {
  F(pSuave([[0, -84], [22, -70], [30, -38], [22, -8], [0, -2], [-22, -8], [-30, -38], [-22, -70]], true, 1), '#ff7aa2', { sombra: 8, brillo: [-18, -66, 8, 18] });
  [[-10, -40], [8, -30], [-4, -20], [12, -54], [-14, -60]].forEach(([x, y]) => F(pEl(x, y, 2, 2), '#e85f8a', { linea: false }));
}, { ancho: 32 });

registrarObjeto('espejo-focos', () => {                   // espejo de camerino con focos alrededor
  F(pRR(-50, -100, 100, 92, 8), '#f3e7d8', { sombra: 34 });
  F(pRR(-38, -88, 76, 68, 4), '#cfeeff', { linea: false });
  F(pPoli([[-26, -80], [-14, -80], [-32, -40], [-36, -40]]), BLANCO, { linea: false });
  const focos = [];
  for (let i = 0; i < 5; i++) focos.push([-40 + i * 20, -94]);
  for (let i = 1; i < 4; i++) { focos.push([-45, -94 + i * 20]); focos.push([45, -94 + i * 20]); }
  focos.forEach(([x, y]) => { F(pEl(x, y, 5.5, 5.5), '#fff3b0', { brillo: [x - 3, y - 4, 3, 3] }); });
  F(pRR(-30, -10, 60, 8, 3), oscuro('#f3e7d8', .82));
}, { ancho: 52 });

registrarObjeto('ring-light', () => {
  F(pRR(-3, -54, 6, 50, 3), '#555a66');
  L(pLinea([[0, -6], [-22, -2]]), '#555a66', 1); L(pLinea([[0, -6], [22, -2]]), '#555a66', 1); L(pLinea([[0, -6], [0, -1]]), '#555a66', 1);
  F(pEl(0, -76, 32, 32), '#e9edf2', { sombra: 10 });
  F(pEl(0, -76, 22, 22), '#fdfbff', { linea: false });
  L(pEl(0, -76, 27, 27), '#fff8d0', 1.5);
  F(pRR(-9, -94, 18, 30, 4), NEGRO);                                             // el celular al centro
  F(pRR(-6, -90, 12, 22, 2), '#7fc8f8', { linea: false });
}, { ancho: 36 });

registrarObjeto('estuche-maquillaje', () => {            // maletín de maquillista
  L(pRR(-18, -86, 36, 16, 6), NEGRO, 1.3);
  F(pRR(-50, -74, 100, 72, 8), ROSA, { sombra: 22 });
  F(pRR(-50, -74, 100, 22, 8), claro(ROSA, .2));
  F(pRR(-6, -60, 12, 12, 3), DORADO);
  [[-50, -52], [38, -52]].forEach(([x, y]) => F(pRR(x, y, 12, 6, 2), DORADO, { linea: false }));
  F(pRR(-50, -40, 100, 4, 0), oscuro(ROSA, .88), { linea: false });
}, { ancho: 52 });

registrarObjeto('perfume', () => {
  F(pRR(-8, -86, 16, 12, 3), DORADO);
  F(pRR(-4, -96, 8, 12, 2), METAL);
  F(pRR(-28, -74, 56, 72, 14), '#f7c6e0', { sombra: 8, brillo: [-22, -68, 8, 56] });
  F(pRR(-16, -46, 32, 18, 4), BLANCO, { linea: false });
}, { ancho: 30 });

registrarEscenario('estudio-maquillaje', p => {
  const g = _g;
  g.fillStyle = _reg(p.pared); g.fillRect(0, 0, W, H);
  g.fillStyle = _reg(claro(p.pared, .3)); for (let x = 0; x < W; x += 140) g.fillRect(x, 0, 70, PISO_Y);
  // gran espejo de camerino al centro-arriba (el texto va encima: el espejo queda claro y liso)
  F(pRR(210, 520, 660, 500, 26), '#f3e7d8');
  F(pRR(250, 560, 580, 420, 12), claro(p.fondo, .55), { linea: false });
  F(pPoli([[300, 600], [360, 600], [270, 900], [250, 900]]), '#ffffff', { linea: false });
  F(pPoli([[400, 600], [430, 600], [330, 860], [310, 860]]), '#ffffff', { linea: false });
  const focos = [];
  for (let i = 0; i < 8; i++) focos.push([250 + i * 83, 540]);
  for (let i = 1; i < 6; i++) { focos.push([230, 540 + i * 80]); focos.push([850, 540 + i * 80]); }
  focos.forEach(([x, y]) => { F(pEl(x, y, 18, 18), '#fff3b0'); F(pEl(x - 5, y - 6, 5, 5), '#ffffff', { linea: false }); });
  // repisas laterales con frascos
  F(pRR(20, 1100, 170, 14, 6), oscuro(p.piso, .75));
  [[60, '#f7c6e0', 70], [120, NUDE, 90], [165, LILA, 60]].forEach(([x, c, h]) => { F(pRR(x - 20, 1100 - h, 40, h, 10), c, { sombra: x + 8 }); F(pRR(x - 10, 1100 - h - 14, 20, 16, 4), NEGRO); });
  F(pRR(890, 1100, 170, 14, 6), oscuro(p.piso, .75));
  [[930, 1.1], [1010, 1]].forEach(([x, s], i) => { F(pRR(x - 22, 1100 - 60 * s, 44, 60 * s, 8), [LILA, ROSA][i]); [-10, 0, 10].forEach(d => F(pRR(x + d - 3, 1100 - 60 * s - 40, 6, 44, 3), NEGRO, { linea: false })); });
  // tocador
  F(pRR(-20, PISO_Y - 6, W + 40, 146, 10), p.piso, { sombra: 'abajo:' + (PISO_Y + 118) });
  L(pLinea([[0, PISO_Y + 60], [W, PISO_Y + 60]]), oscuro(p.piso, .93), .5);
  g.fillStyle = _reg(p.fondo); g.fillRect(0, PISO_Y + 140, W, H - PISO_Y);
  g.fillStyle = _reg(oscuro(p.fondo, .9)); for (let x = 0; x < W; x += 100) g.fillRect(x, PISO_Y + 140, 6, H);
  g.fillStyle = _reg(oscuro(p.fondo, .8)); g.fillRect(0, PISO_Y + 140, W, 14);
});

registrarKit('makeup', {
  nombre: 'Makeup',
  paleta: { fondo: '#f4c9d6', pared: '#fbe8ee', piso: '#fff7f2', acento: '#ff8fab', acento2: '#c9a7ef', tinta: '#34242e' },
  escenario: 'estudio-maquillaje',
  objetos: ['paleta-sombras', 'labial', 'vaso-brochas', 'brocha', 'rubor', 'base-maquillaje', 'rimel', 'esponja', 'espejo-focos', 'ring-light', 'estuche-maquillaje', 'perfume'],
});
registrarKit('maquillaje', KITS.makeup);
registrarKit('makeup-artist', KITS.makeup);
})();
