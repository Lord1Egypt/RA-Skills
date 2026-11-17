// KIT PSICÓLOGO / TERAPIA — se carga después de nucleo/objetos.js
(() => {
const VERDE = '#5c9e8f', MOSTAZA = '#e9b44c', MADERA = '#b98b5e', CREMA = '#f7efe2', ROSA = '#f29aa6', HOJA = '#5fae6a';

registrarObjeto('sillon', () => {
  F(pRR(-40, -12, 8, 12, 2), '#6b4a30'); F(pRR(32, -12, 8, 12, 2), '#6b4a30');        // patas
  F(pSuave([[-38, -52], [-36, -92], [0, -100], [36, -92], [38, -52]], true, .7), VERDE, { sombra: 18 });   // respaldo
  L(pLinea([[-12, -90], [-12, -56]]), oscuro(VERDE, .8), .5); L(pLinea([[12, -90], [12, -56]]), oscuro(VERDE, .8), .5);
  F(pRR(-42, -46, 84, 34, 10), claro(VERDE, .15), { sombra: 20 });                     // asiento
  F(pRR(-54, -62, 20, 52, 10), VERDE, { sombra: -40 }); F(pRR(34, -62, 20, 52, 10), VERDE, { sombra: 46 });   // brazos del sillón
  F(pRR(-20, -76, 36, 26, 10), MOSTAZA, { sombra: 8 });                                 // cojín
}, { ancho: 54 });

registrarObjeto('libreta', () => {
  _g.save(); _g.translate(0, -44); _g.rotate(-.08);
  F(pRR(-36, -46, 72, 88, 6), '#fffdf6', { sombra: 24 });
  F(pRR(-36, -46, 12, 88, 4), VERDE, { linea: false });
  for (let i = 0; i < 6; i++) L(pLinea([[-18, -30 + i * 12], [28, -30 + i * 12]]), '#b9c7d9', .4);
  for (let i = 0; i < 7; i++) L(pEl(-36, -38 + i * 12, 6, 3.5, 0, Math.PI * .5, Math.PI * 1.5, false), '#8a8fa0', .7);
  L(pSuave([[-14, -32], [0, -34], [14, -30]], false), '#6b7fa8', .5);
  _g.restore();
  _g.save(); _g.translate(18, -18); _g.rotate(-.9);                                      // pluma
  F(pRR(-5, -40, 10, 48, 4), MOSTAZA, { sombra: 2 }); F(pPoli([[-5, 8], [5, 8], [0, 18]]), '#f3d9a8'); F(pRR(-5, -44, 10, 8, 3), ROSA);
  _g.restore();
}, { ancho: 42 });

registrarObjeto('reloj-pared', t => {
  F(pEl(0, -50, 46, 46), MADERA, { sombra: 12 });
  F(pEl(0, -50, 38, 38), '#fffaf0', { linea: false });
  for (let i = 0; i < 12; i++) { const a = i / 12 * Math.PI * 2, l = i % 3 ? 3 : 7; L(pLinea([[Math.cos(a) * (34 - l), -50 + Math.sin(a) * (34 - l)], [Math.cos(a) * 34, -50 + Math.sin(a) * 34]]), '#6b4a30', .5); }
  const am = -Math.PI / 2 + t * 1.2, ah = -Math.PI / 2 + 2.1 + t * .1;
  L(pLinea([[0, -50], [Math.cos(ah) * 18, -50 + Math.sin(ah) * 18]]), TINTA_OBJ, 1.1);
  L(pLinea([[0, -50], [Math.cos(am) * 28, -50 + Math.sin(am) * 28]]), TINTA_OBJ, .7);
  F(pEl(0, -50, 4, 4), '#d9553f', { linea: false });
}, { ancho: 44, anima: true });

registrarObjeto('taza', t => {
  for (let i = 0; i < 3; i++) {                                                          // vapor que sube
    const f = (t * .6 + i / 3) % 1, x = -14 + i * 14;
    _g.save(); _g.globalAlpha = _modo === 'pixel' ? 1 : Math.sin(f * Math.PI) * .9;
    L(pSuave([[x, -64 - f * 20], [x + 5, -72 - f * 20], [x - 3, -82 - f * 20], [x + 3, -92 - f * 20]], false), '#c9ccd6', .8);
    _g.restore();
  }
  const asa = new Path2D(); asa.ellipse(32, -34, 16, 17, 0, 0, Math.PI * 2); asa.ellipse(32, -34, 8, 9, 0, Math.PI * 2, 0, true);
  F(asa, '#e8e2d6');
  F(pRR(-32, -62, 64, 60, 10), '#f4eee4', { sombra: 16 });
  F(pEl(0, -62, 32, 6), '#8a5a3b');
  F(pCorazon(-2, -32, 11), ROSA, { linea: false });
}, { ancho: 40, anima: true });

registrarObjeto('planta', () => {
  const hojas = [[-6, -40, -1.1, 1], [8, -44, .9, 1.05], [-2, -52, -.25, 1.15], [14, -34, 1.5, .85], [-16, -34, -1.6, .85], [4, -58, .25, 1]];
  hojas.forEach(([x, y, a, s], i) => { _g.save(); _g.translate(x * .3, -40); _g.rotate(a * .7); _g.scale(s, s);
    F(pSuave([[0, 0], [12, -18], [8, -42], [0, -54], [-8, -42], [-12, -18]], true, .9), i % 2 ? HOJA : '#77c587', { sombra: 0 });
    L(pLinea([[0, -4], [0, -46]]), '#3f8f55', .4); _g.restore(); });
  F(pPoli([[-28, -40], [28, -40], [22, -2], [-22, -2]]), '#e07a55', { sombra: 8 });
  F(pRR(-32, -46, 64, 12, 4), '#ee8d67', { sombra: 12 });
}, { ancho: 32 });

registrarObjeto('panuelos', () => {
  F(pRR(-44, -50, 88, 48, 8), '#bfe0dc', { sombra: 18 });
  [[-30, -20], [-6, -34], [18, -18], [32, -38]].forEach(([x, y]) => F(pEl(x, y, 5, 5), '#ffffff', { linea: false }));
  F(pRR(-22, -54, 44, 10, 5), '#6d9f97');
  F(pSuave([[-16, -52], [-20, -74], [-6, -90], [4, -76], [18, -88], [20, -70], [14, -52]], true, .8), '#ffffff', { sombra: 6, k: .92 });
}, { ancho: 46 });

registrarObjeto('lampara', () => {
  if (_modo === 'vector') { _g.save(); _g.globalAlpha = .35; _g.fillStyle = '#ffe9a8'; _g.fill(pPoli([[-24, -70], [24, -70], [52, 0], [-52, 0]])); _g.restore(); }
  F(pEl(0, -4, 22, 6), '#6b4a30');
  F(pRR(-3, -72, 6, 68, 3), '#8a5a3b');
  F(pPoli([[-20, -100], [20, -100], [32, -68], [-32, -68]]), MOSTAZA, { sombra: 8 });
  F(pEl(0, -68, 14, 4), '#fff1b8', { linea: false });
}, { ancho: 30 });

registrarObjeto('cerebro', () => {
  // vista de lado: cerebelo y tallo atrás, la masa con lóbulos festoneados, surcos que se leen de lejos
  F(pRR(4, -30, 13, 30, 6), '#e98ea2', { sombra: 12 });                                   // tallo
  F(pEl(28, -26, 20, 13, -.15), '#ef97aa', { sombra: 'abajo:-24', k: .86 });             // cerebelo
  L(pLinea([[14, -28], [42, -26]]), '#c9667d', .45); L(pLinea([[16, -21], [40, -20]]), '#c9667d', .45);
  const pts = []; for (let i = 0; i < 40; i++) { const a = i / 40 * Math.PI * 2, lob = 1 + .055 * Math.abs(Math.sin(a * 5.5));
    const rx = 52 * lob, ry = (Math.sin(a) > 0 ? 30 : 42) * lob; pts.push([Math.cos(a) * rx - 2, -58 + Math.sin(a) * ry]); }
  const masa = pSuave(pts, true, 1);
  F(masa, '#f7a8b8', { sombra: pEl(-2, -30, 60, 18), k: .88, brillo: [-34, -92, 34, 10] });
  const s = '#d06c84';
  L(pSuave([[-44, -50], [-22, -46], [-4, -40], [22, -42], [40, -36]], false), s, .8);   // cisura lateral
  L(pSuave([[2, -98], [0, -84], [6, -72], [0, -60]], false), s, .75);                    // surco central
  [[[-40, -80], [-30, -88], [-20, -78], [-14, -88]], [[-44, -64], [-32, -70], [-22, -60], [-12, -68]], [[14, -90], [24, -80], [34, -88], [42, -76]],
   [[12, -64], [22, -70], [32, -60], [44, -64]], [[-30, -36], [-18, -30], [-6, -34]]].forEach(q => L(pSuave(q, false), s, .6));
  F(pCorazon(40, -96, 10), '#ff5a6e');
}, { ancho: 50 });

registrarObjeto('puerta', () => {
  F(pRR(-40, -104, 80, 104, 4), '#8a5a3b', { sombra: 34 });
  F(pRR(-32, -96, 64, 96, 3), '#c99466', { sombra: 16 });
  F(pRR(-24, -88, 48, 34, 4), '#b8845a', { linea: false }); L(pRR(-24, -88, 48, 34, 4), '#a0714a', .5);
  F(pRR(-24, -46, 48, 36, 4), '#b8845a', { linea: false }); L(pRR(-24, -46, 48, 36, 4), '#a0714a', .5);
  F(pEl(20, -52, 5, 5), '#ffcc4d');
  F(pEl(0, -80, 10, 10), '#fff4d6'); F(pCorazon(0, -80, 5.5), '#f29aa6', { linea: false });
}, { ancho: 44 });

registrarEscenario('consultorio', p => {
  const g = _g;
  g.fillStyle = _reg(p.pared); g.fillRect(0, 0, W, PISO_Y);
  g.fillStyle = _reg(oscuro(p.pared, .95)); g.fillRect(0, PISO_Y - 330, W, 330);                      // zócalo
  F(pRR(-10, PISO_Y - 336, W + 20, 14, 4), claro(p.pared, .5));
  // ventana a la izquierda con cortina
  F(pRR(40, 720, 260, 330, 10), '#cfe8f5'); F(pRR(40, 720, 260, 330, 10), claro('#cfe8f5', .2), { linea: false });
  L(pLinea([[170, 720], [170, 1050]]), p.tinta, .8); L(pLinea([[40, 885], [300, 885]]), p.tinta, .8);
  F(pSuave([[20, 700], [120, 700], [95, 900], [110, 1080], [20, 1080]], true, .6), p.acento, { sombra: 70 });
  // cuadro a la derecha
  F(pRR(790, 760, 230, 170, 8), '#fffaf0'); F(pEl(860, 860, 40, 40), claro(p.acento2, .1), { linea: false }); F(pEl(930, 830, 48, 48), claro(p.acento, .2), { linea: false });
  // piso de madera y alfombra
  g.fillStyle = _reg(p.piso); g.fillRect(0, PISO_Y, W, H - PISO_Y);
  g.fillStyle = _reg(oscuro(p.piso, .9)); for (let y = PISO_Y + 60; y < H; y += 70) g.fillRect(0, y, W, 5);
  F(pEl(W / 2, PISO_Y + 120, 470, 90), claro(p.acento2, .25), { sombra: 'abajo:' + (PISO_Y + 150) });
  L(pEl(W / 2, PISO_Y + 120, 430, 70), p.acento2, .6);
  g.save(); g.globalAlpha = .16; g.fillStyle = '#fff6dc'; g.fill(pPoli([[40, 720], [300, 720], [720, PISO_Y + 200], [260, PISO_Y + 200]])); g.restore();   // haz de la ventana
}, (t, p) => {   // vivo: polvito que flota dentro del haz de luz
  const g = _g; g.fillStyle = '#fffbe8';
  for (let i = 0; i < 16; i++) { const f = (t * .05 + hash2(i, 2)) % 1, u = hash2(i, 5);
    const x = lerp(60, 280, u) + f * 380 + Math.sin(t * .8 + i) * 12, y = 740 + f * 560 + Math.sin(t * 1.1 + i * 2) * 10;
    g.globalAlpha = .7 * Math.sin(f * Math.PI); g.beginPath(); g.arc(x, y, 2.5 + hash2(i, 8) * 3, 0, 7); g.fill(); }
  g.globalAlpha = 1;
});

registrarKit('psicologo', {
  nombre: 'Psicólogo / terapia',
  paleta: { fondo: '#efe7dc', pared: '#eadfce', piso: '#b98b5e', acento: '#5c9e8f', acento2: '#e9a86b', tinta: '#2c2622' },
  escenario: 'consultorio',
  objetos: ['sillon', 'libreta', 'reloj-pared', 'taza', 'planta', 'panuelos', 'lampara', 'cerebro', 'puerta', 'calendario'],
});
})();
