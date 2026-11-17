// KIT RESTAURANTE — se carga después de nucleo/objetos.js
(() => {
const ROJO = '#e0463a', DORADO = '#f2b544', MADERA = '#8a5a3b', BLANCO = '#ffffff', METAL = '#c3c8d2', HOJA = '#56b870';

registrarObjeto('plato', t => {
  F(pEl(0, -18, 54, 18), '#e9edf2', { sombra: 'abajo:-14' });
  F(pEl(0, -21, 40, 12), BLANCO, { linea: false });
  // espagueti: un nido de fideos enroscados, salsa encima, 2 albóndigas y albahaca
  const nido = pSuave([[-34, -24], [-30, -40], [-14, -52], [8, -54], [26, -46], [34, -30], [30, -22]], true, .8);
  F(nido, '#f6d27a', { sombra: 12, k: .9 });
  _g.save(); _g.clip(nido);
  for (let i = 0; i < 7; i++) { const cx = -26 + i * 9 + (i % 2) * 3, cy = -30 - (i % 3) * 7;
    L(pEl(cx, cy, 9, 5, (i % 2 ? .5 : -.4), Math.PI * .1, Math.PI * 1.7, false), '#dcaa45', .5); }
  _g.restore();
  F(pSuave([[-16, -46], [-2, -56], [16, -50], [20, -40], [2, -38], [-14, -38]], true, .9), ROJO, { sombra: 'abajo:-42', k: .85 });
  F(pEl(-6, -48, 7, 6), '#8a4a2e', { brillo: [-10, -53, 5, 2] }); F(pEl(9, -46, 6.5, 5.5), '#8a4a2e', { brillo: [5, -50, 4, 2] });
  F(pEl(2, -58, 8, 4, -.5), HOJA); F(pEl(12, -57, 7, 3.5, .6), '#77c587');
  for (let i = 0; i < 2; i++) { const f = (t * .5 + i / 2) % 1; _g.save(); _g.globalAlpha = _modo === 'pixel' ? 1 : Math.sin(f * Math.PI) * .8;
    L(pSuave([[-8 + i * 16, -60 - f * 22], [-3 + i * 16, -70 - f * 22], [-10 + i * 16, -80 - f * 22]], false), '#c9ccd6', .7); _g.restore(); }
}, { ancho: 54, anima: true });

registrarObjeto('mesa', () => {
  F(pRR(-40, -44, 8, 44, 3), MADERA); F(pRR(32, -44, 8, 44, 3), MADERA);
  const mantel = pSuave([[-56, -66], [56, -66], [58, -40], [44, -34], [30, -40], [14, -34], [0, -40], [-14, -34], [-30, -40], [-44, -34], [-58, -40]], true, .5);
  F(mantel, BLANCO);
  _g.save(); _g.clip(mantel);
  for (let x = -60; x < 60; x += 16) F(pRR(x, -70, 8, 40, 0), ROJO, { linea: false });
  for (let y = -66; y < -30; y += 16) { _g.save(); _g.globalAlpha = .55; F(pRR(-60, y, 120, 8, 0), ROJO, { linea: false }); _g.restore(); }
  _g.restore(); if (_modo === 'vector') L(mantel, null, 1);
  F(pEl(0, -70, 58, 6), '#f4f4f4');
}, { ancho: 56 });

registrarObjeto('copa', () => {
  const cuerpo = pSuave([[-24, -98], [24, -98], [22, -72], [0, -56], [-22, -72]], true, .7);
  F(cuerpo, '#eef7fb');
  _g.save(); _g.clip(cuerpo); F(pRR(-30, -82, 60, 30, 0), '#9c2a3e', { linea: false }); F(pEl(0, -82, 26, 4), '#b8364d', { linea: false }); _g.restore();
  if (_modo === 'vector') L(cuerpo, null, 1);
  F(pRR(-3, -58, 6, 50, 3), '#eef7fb');
  F(pEl(0, -6, 20, 5), '#eef7fb');
  F(pEl(-14, -88, 3, 7), BLANCO, { linea: false });
}, { ancho: 22 });

registrarObjeto('comanda', () => {
  _g.save(); _g.translate(-4, -48); _g.rotate(-.06);
  const hoja = new Path2D(); hoja.moveTo(-32, -44); for (let x = -32; x <= 32; x += 8) hoja.lineTo(x + 4, -48), hoja.lineTo(x + 8, -44);
  hoja.lineTo(32, 44); hoja.lineTo(-32, 44); hoja.closePath();
  F(hoja, '#fffbe8', { sombra: 18 });
  T('MESA 4', 0, -30, 11, ROJO);
  for (let i = 0; i < 4; i++) { L(pLinea([[-22, -12 + i * 14], [6 + (i % 2) * 8, -12 + i * 14]]), '#7a8599', .45); F(pEl(20, -12 + i * 14, 2.5, 2.5), '#7a8599', { linea: false }); }
  _g.restore();
  _g.save(); _g.translate(30, -12); _g.rotate(-.7);
  F(pRR(-4, -46, 8, 44, 2), DORADO); F(pPoli([[-4, -2], [4, -2], [0, 8]]), '#f3d9a8'); F(pRR(-4, -50, 8, 6, 2), '#f29aa6');
  _g.restore();
}, { ancho: 40 });

registrarObjeto('campana', t => {
  const golpe = Math.max(0, Math.sin(t * 3)) ** 8;
  F(pEl(0, -6, 44, 7), '#8a909c', { sombra: 'abajo:-4' });
  F(pRR(-4, -66, 8, 10, 3), '#8a909c'); F(pEl(0, -70 + golpe * 3, 8, 5), '#6e7482');
  F(pEl(0, -12, 38, 46, 0, Math.PI, Math.PI * 2), DORADO, { sombra: 10, brillo: [-26, -44, 8, 22] });
  F(pRR(-40, -14, 80, 6, 3), '#d99a2b');
  [0, 1, 2].forEach(i => { _g.save(); _g.globalAlpha = _modo === 'pixel' ? 1 : golpe; L(pLinea([[-44 - i * 6, -52 + i * 10], [-54 - i * 6, -58 + i * 10]]), DORADO, .8); L(pLinea([[44 + i * 6, -52 + i * 10], [54 + i * 6, -58 + i * 10]]), DORADO, .8); _g.restore(); });
}, { ancho: 44, anima: true });

registrarObjeto('sarten', () => {
  F(pRR(34, -30, 44, 10, 5), '#3b3441', { sombra: 'abajo:-24' });
  F(pEl(-8, -28, 46, 22), '#3b3441', { sombra: 'abajo:-22' });
  F(pEl(-8, -30, 38, 16), '#56505c', { linea: false });
  F(pSuave([[-30, -32], [-22, -42], [-6, -44], [8, -40], [12, -30], [2, -22], [-16, -22], [-28, -26]], true, .8), BLANCO, { linea: false });
  F(pEl(-8, -34, 9, 7), '#ffbe2e', { brillo: [-12, -38, 3, 3] });
}, { ancho: 50 });

registrarObjeto('gorro-chef', () => {
  F(pRR(-26, -40, 52, 36, 4), BLANCO, { sombra: 14 });
  L(pLinea([[-26, -16], [26, -16]]), '#d9dde4', .6);
  F(pSuave([[-26, -40], [-40, -58], [-30, -84], [-10, -84], [0, -98], [16, -88], [36, -84], [40, -62], [26, -40]], true, .9), BLANCO, { sombra: 18, k: .92 });
  L(pLinea([[-10, -40], [-12, -60]]), '#d9dde4', .5); L(pLinea([[10, -40], [12, -62]]), '#d9dde4', .5);
}, { ancho: 34 });

registrarObjeto('menu', () => {
  F(pPoli([[-40, -96], [0, -90], [0, -2], [-40, -8]]), ROJO, { sombra: -10 });
  F(pPoli([[0, -90], [40, -96], [40, -8], [0, -2]]), '#fff6e3', { sombra: 30 });
  T('MENÚ', 20, -78, 9, ROJO);
  for (let i = 0; i < 5; i++) L(pLinea([[8, -62 + i * 11], [32, -63 + i * 11]]), '#b9a78a', .45);
  F(pEstrella(-20, -54, 9, 4), DORADO, { linea: false });
}, { ancho: 42 });

registrarObjeto('cubiertos', () => {
  _g.save(); _g.translate(0, -46); _g.rotate(-.38);
  F(pRR(-4, -36, 8, 82, 4), METAL);                                                      // tenedor: mango
  F(pSuave([[-4, -34], [-11, -44], [-11, -50], [11, -50], [11, -44], [4, -34]], true, .5), METAL);   // cuello
  [-8.5, -2.8, 2.8, 8.5].forEach(x => { const d = pLinea([[x, -48], [x, -76]]);            // cuatro dientes largos
    if (_modo === 'vector') { L(d, null, 1.5); L(d, METAL, .55); } else F(pRR(x - 1.6, -76, 3.2, 30, 1.6), METAL); });
  _g.restore();
  _g.save(); _g.translate(0, -46); _g.rotate(.38);
  F(pRR(-4, -6, 8, 52, 4), '#6b4a30');                                                   // cuchillo
  F(pSuave([[-4, -6], [-4, -56], [2, -60], [7, -40], [4, -6]], true, .6), METAL, { brillo: [-2, -52, 2, 40] });
  _g.restore();
}, { ancho: 34 });

registrarObjeto('olla', t => {
  for (let i = 0; i < 3; i++) { const f = (t * .55 + i / 3) % 1; _g.save(); _g.globalAlpha = _modo === 'pixel' ? 1 : Math.sin(f * Math.PI) * .85;
    L(pSuave([[-16 + i * 16, -74 - f * 22], [-10 + i * 16, -84 - f * 22], [-18 + i * 16, -94 - f * 22]], false), '#c9ccd6', .8); _g.restore(); }
  F(pRR(-54, -52, 14, 10, 5), '#6e7482'); F(pRR(40, -52, 14, 10, 5), '#6e7482');
  F(pRR(-42, -58, 84, 56, 10), ROJO, { sombra: 20, brillo: [-34, -50, 6, 36] });
  F(pEl(0, -60, 44, 8), '#c23a30');
  F(pEl(0, -66, 10, 5), '#6e7482');
}, { ancho: 48, anima: true });

registrarEscenario('restaurante', p => {
  const g = _g;
  g.fillStyle = _reg(p.pared); g.fillRect(0, 0, W, PISO_Y);
  g.fillStyle = _reg(oscuro(p.pared, .9));                                                  // ladrillo
  for (let y = 0, f = 0; y < PISO_Y - 300; y += 60, f++) { g.fillRect(0, y, W, 5); for (let x = (f % 2) * 70; x < W; x += 140) g.fillRect(x, y, 5, 60); }
  g.fillStyle = _reg(p.fondo); g.fillRect(0, PISO_Y - 300, W, 300);                           // lambrín de madera clara
  g.fillStyle = _reg(oscuro(p.fondo, .9)); for (let x = 0; x < W; x += 60) g.fillRect(x, PISO_Y - 300, 4, 300);
  F(pRR(-10, PISO_Y - 312, W + 20, 18, 4), MADERA);
  // lámparas colgantes a los lados
  if (_modo === 'pixel') [[170, 780], [910, 740]].forEach(([x, y]) => { L(pLinea([[x, 0], [x, y - 60]]), p.tinta, .6);   // en pixel, quietas
    F(pEl(x, y, 70, 60, 0, Math.PI, Math.PI * 2), p.acento2); F(pEl(x, y, 18, 8), '#fff1b8'); });
  g.fillStyle = _reg(p.piso); g.fillRect(0, PISO_Y, W, H - PISO_Y);
  g.fillStyle = _reg(oscuro(p.piso, .88)); for (let y = PISO_Y + 50; y < H; y += 60) g.fillRect(0, y, W, 4);
  for (let y = PISO_Y, f = 0; y < H; y += 60, f++) for (let x = (f % 3) * 130; x < W; x += 390) g.fillRect(x, y, 4, 60);
  F(pRR(-10, PISO_Y - 6, W + 20, 26, 6), oscuro(p.piso, .75));
}, (t, p) => {   // vivo: lámparas colgantes que se mecen apenas; la luz las sigue
  [[170, 780, 0], [910, 740, 1.7]].forEach(([x, y, fase]) => {
    const a = Math.sin(t * 1.1 + fase) * .035, g = _g;
    g.save(); g.translate(x, 0); g.rotate(a); g.translate(-x, 0);
    g.save(); g.globalAlpha = .2; g.fillStyle = '#ffe9a8'; g.fill(pPoli([[x - 40, y], [x + 40, y], [x + 160, PISO_Y - 320], [x - 160, PISO_Y - 320]])); g.restore();
    L(pLinea([[x, 0], [x, y - 60]]), p.tinta, .6);
    F(pEl(x, y, 70, 60, 0, Math.PI, Math.PI * 2), p.acento2, { brillo: [x - 50, y - 50, 30, 12] }); F(pEl(x, y, 18, 8), '#fff1b8');
    g.restore(); });
});

registrarKit('restaurante', {
  nombre: 'Restaurante',
  paleta: { fondo: '#f3dcb8', pared: '#c7654c', piso: '#8a5a3b', acento: '#e0463a', acento2: '#f2b544', tinta: '#2b1d17' },
  escenario: 'restaurante',
  objetos: ['plato', 'mesa', 'copa', 'comanda', 'campana', 'sarten', 'gorro-chef', 'menu', 'cubiertos', 'olla'],
});
})();
