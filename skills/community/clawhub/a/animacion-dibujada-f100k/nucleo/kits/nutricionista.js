// KIT NUTRICIONISTA — se carga después de nucleo/objetos.js
(() => {
const VERDE = '#5cbf6a', VERDE_O = '#3f9b52', NARANJA = '#ff9a3c', ROJO = '#ff5a5e', CREMA = '#fff6e6', AZUL = '#8fd3ff', METAL = '#c3c8d2', CAFE = '#c98a4a';

registrarObjeto('plato-buen-comer', () => {              // plato visto un poco desde arriba, dividido en 3
  F(pEl(0, -30, 56, 26), '#e9edf2', { sombra: 'abajo:-26' });
  F(pEl(0, -34, 46, 20), '#ffffff', { linea: false });
  _g.save(); _g.clip(pEl(0, -34, 44, 19));
  F(pPoli([[0, -34], [-60, -80], [-60, 10], [0, 10]]), '#9be07a', { linea: false });           // verduras: mitad izquierda
  F(pPoli([[0, -34], [60, -80], [60, -34]]), '#ffd166', { linea: false });                   // cereal
  F(pPoli([[0, -34], [60, -34], [60, 10], [0, 10]]), '#ff9f7a', { linea: false });            // proteína
  _g.restore();
  L(pLinea([[0, -52], [0, -16]]), '#ffffff', 1.2); L(pLinea([[0, -34], [44, -34]]), '#ffffff', 1.2);
  // detalles de comida
  [[-26, -40, 7], [-16, -28, 6], [-30, -26, 5]].forEach(([x, y, r]) => F(pEl(x, y, r, r * .8), VERDE_O, { linea: false }));
  F(pEl(-12, -44, 5, 4), ROJO, { linea: false });
  [[16, -44], [26, -42], [21, -40], [30, -46]].forEach(([x, y]) => F(pEl(x, y, 3, 2), '#e8b340', { linea: false }));
  F(pEl(22, -24, 12, 6, -.2), '#e57a55', { linea: false });
  L(pEl(0, -34, 46, 20), TINTA_OBJ, .5);
  // tenedor a la izquierda: mango + cabeza con 3 dientes
  F(pRR(-66, -40, 6, 38, 3), METAL);
  F(pRR(-69, -54, 12, 16, 4), METAL);
  [-68, -63.5, -59].forEach(x => F(pRR(x, -66, 3, 14, 1.5), METAL, { linea: false }));
}, { ancho: 62 });

registrarObjeto('manzana', () => {
  F(pSuave([[0, -70], [22, -82], [40, -64], [38, -30], [20, -4], [0, -10], [-20, -4], [-38, -30], [-40, -64], [-22, -82]], true, .9), ROJO, { sombra: 10, brillo: [-28, -66, 9, 20] });
  F(pRR(-2, -94, 5, 22, 2.5), '#7a4a2a');
  F(pSuave([[3, -86], [18, -98], [30, -94], [18, -84]], true, .9), VERDE, { sombra: 16 });
}, { ancho: 40 });

registrarObjeto('aguacate', () => {
  F(pSuave([[0, -100], [20, -86], [34, -46], [26, -12], [0, -2], [-26, -12], [-34, -46], [-20, -86]], true, .9), '#3d7a3a', { sombra: 12 });
  F(pSuave([[0, -90], [15, -78], [26, -44], [20, -16], [0, -10], [-20, -16], [-26, -44], [-15, -78]], true, .9), '#c8e38a', { linea: false });
  F(pEl(0, -36, 14, 16), '#a0673a', { brillo: [-8, -46, 5, 8] });
}, { ancho: 36 });

registrarObjeto('brocoli', () => {
  F(pPoli([[-10, -48], [10, -48], [14, -2], [-14, -2]]), '#a6d67a', { sombra: 4 });
  L(pLinea([[-2, -40], [-12, -56]]), '#8cc060', 1.4); L(pLinea([[3, -40], [14, -58]]), '#8cc060', 1.4);
  [[-26, -64, 20], [0, -78, 24], [26, -64, 20], [-12, -56, 16], [14, -56, 16]].forEach(([x, y, r], i) =>
    F(pEl(x, y, r, r * .9), i < 3 ? VERDE_O : VERDE, { sombra: x + r * .3, k: .85 }));
  [[-6, -86], [8, -80], [-24, -70], [22, -72]].forEach(([x, y]) => F(pEl(x, y, 3, 3), '#8fd88a', { linea: false }));
}, { ancho: 44 });

registrarObjeto('vaso-agua', t => {
  const vaso = pPoli([[-26, -92], [26, -92], [20, -2], [-20, -2]]);
  F(vaso, '#eaf6ff', { linea: false });
  _g.save(); _g.clip(vaso);
  const ola = Math.sin(t * 3) * 2;
  F(pSuave([[-40, -64 + ola], [-10, -68 - ola], [20, -62 + ola], [40, -66], [40, 10], [-40, 10]], true, .6), AZUL, { linea: false, sombra: 10, k: .9 });
  F(pRR(-18, -58, 6, 46, 3), '#ffffff', { linea: false });
  _g.restore();
  if (_modo === 'vector') L(vaso, null, 1);
  F(pEl(8, -76, 14, 14, 0), '#ffe066', { linea: false }); L(pEl(8, -76, 14, 14), '#e8b800', .5);     // rodaja de limón
  L(pLinea([[8, -76], [8, -88]]), '#e8b800', .35); L(pLinea([[8, -76], [18, -70]]), '#e8b800', .35); L(pLinea([[8, -76], [-2, -70]]), '#e8b800', .35);
}, { ancho: 30, anima: true });

registrarObjeto('tupper', () => {                        // domingo de tuppers: recipiente con tapa y comida
  F(pRR(-50, -52, 100, 50, 10), '#eaf6ff', { sombra: 26 });
  _g.save(); _g.clip(pRR(-48, -50, 96, 46, 9));
  F(pRR(-50, -40, 48, 40, 0), '#ffd166', { linea: false });
  F(pRR(-2, -40, 52, 40, 0), '#9be07a', { linea: false });
  [[-36, -30], [-20, -24], [-30, -18]].forEach(([x, y]) => F(pEl(x, y, 5, 3), '#e8b340', { linea: false }));
  [[14, -28, 7], [30, -22, 6], [22, -14, 5]].forEach(([x, y, r]) => F(pEl(x, y, r, r), VERDE_O, { linea: false }));
  F(pEl(-8, -20, 12, 7), '#ff9f7a', { linea: false });
  _g.restore();
  F(pRR(-54, -66, 108, 16, 8), '#7ec8a8', { sombra: 30 });
  F(pRR(-12, -72, 24, 8, 4), '#5fae8f');
  [-40, 40].forEach(x => F(pRR(x - 6, -60, 12, 10, 3), '#5fae8f'));
}, { ancho: 56 });

registrarObjeto('carrito-super', () => {
  L(pLinea([[-56, -96], [-40, -96], [-30, -30], [40, -30]]), '#555a66', 1.4);
  const canasta = pPoli([[-40, -86], [54, -86], [44, -40], [-32, -40]]);
  F(canasta, '#e9edf2', { linea: false });
  _g.save(); _g.clip(canasta);
  for (let x = -40; x < 60; x += 12) L(pLinea([[x, -90], [x - 4, -36]]), '#9aa2ae', .5);
  for (let y = -80; y < -36; y += 11) L(pLinea([[-44, y], [60, y]]), '#9aa2ae', .5);
  _g.restore(); if (_modo === 'vector') L(canasta, null, 1);
  // lo que va dentro
  F(pRR(-26, -110, 22, 30, 3), '#ffd166'); F(pEl(8, -94, 12, 13), ROJO); F(pSuave([[20, -84], [26, -112], [34, -114], [38, -86]], true, .8), VERDE);
  F(pEl(-28, -8, 8, 8), '#2d2a3a'); F(pEl(34, -8, 8, 8), '#2d2a3a');
  F(pEl(-28, -8, 3, 3), '#9aa2ae', { linea: false }); F(pEl(34, -8, 3, 3), '#9aa2ae', { linea: false });
  L(pLinea([[-32, -30], [-28, -16]]), '#555a66', 1); L(pLinea([[36, -30], [34, -16]]), '#555a66', 1);
}, { ancho: 58 });

registrarObjeto('caja-cereal', () => {
  F(pPoli([[34, -94], [46, -86], [46, -2], [34, -2]]), '#e0902c');
  F(pRR(-34, -96, 68, 94, 4), NARANJA, { sombra: 'abajo:-8' });
  F(pRR(-26, -86, 52, 22, 5), '#ffffff'); T('CEREAL', 0, -75, 12, '#e0662c');
  F(pEl(0, -36, 22, 13), '#ffffff');                                         // tazón con cereal
  F(pSuave([[-20, -40], [-10, -50], [4, -48], [18, -50], [22, -40]], true, .8), '#ffd166', { linea: false });
  F(pEl(0, -30, 22, 9, 0, 0, Math.PI), '#8fd3ff', { linea: false });
  F(pEstrella(22, -58, 9, 4), '#ffffff', { linea: false });
}, { ancho: 46 });

registrarObjeto('barra-proteina', () => {
  _g.save(); _g.translate(0, -34); _g.rotate(-.18);
  F(pPoli([[-54, -14], [-46, -20], [46, -20], [54, -14], [54, 14], [46, 20], [-46, 20], [-54, 14]]), '#7b5cd6', { sombra: 'abajo:6' });
  [-50, 50].forEach(x => { for (let i = -14; i <= 14; i += 7) L(pLinea([[x, i], [x + (x < 0 ? 4 : -4), i + 3]]), '#5c43b0', .4); });
  F(pRR(-34, -12, 68, 24, 5), '#ffffff', { linea: false });
  T('BARRA', 0, 0, 13, '#7b5cd6');
  _g.restore();
  F(pEstrella(38, -66, 9, 4), '#ffd23f', { linea: false });
}, { ancho: 56 });

registrarObjeto('pan-molde', () => {
  F(pSuave([[-44, -2], [-46, -60], [-38, -84], [-16, -92], [0, -86], [16, -92], [38, -84], [46, -60], [44, -2]], true, .7), '#d99a5b', { sombra: 20 });
  F(pSuave([[-36, -8], [-38, -56], [-30, -76], [-14, -82], [0, -76], [14, -82], [30, -76], [38, -56], [36, -8]], true, .7), '#fbe6c2', { linea: false });
  [[-14, -50], [10, -38], [-6, -24], [18, -60]].forEach(([x, y]) => F(pEl(x, y, 3, 2), '#e8c89a', { linea: false }));
}, { ancho: 46 });

registrarObjeto('etiqueta-nutrimental', () => {           // tabla genérica, sin cifras: barras que se leen como datos
  F(pRR(-40, -100, 80, 98, 5), '#ffffff', { sombra: 26 });
  F(pRR(-34, -92, 68, 12, 2), TINTA_OBJ, { linea: false });
  L(pLinea([[-34, -74], [34, -74]]), TINTA_OBJ, 1.1);
  for (let i = 0; i < 6; i++) {
    const y = -64 + i * 10;
    F(pRR(-32, y - 3, 30 - (i % 3) * 5, 5, 2), '#8a8fa0', { linea: false });
    F(pRR(18 - (i % 2) * 6, y - 3, 14 + (i % 2) * 6, 5, 2), i === 2 ? ROJO : '#8a8fa0', { linea: false });
    L(pLinea([[-34, y + 5], [34, y + 5]]), '#d6d9e0', .35);
  }
  L(pLinea([[-34, -8], [34, -8]]), TINTA_OBJ, 1.1);
}, { ancho: 42 });

registrarObjeto('cinta-metrica', () => {
  F(pEl(-10, -46, 36, 36), '#ffd23f', { sombra: 4, k: .86 });
  F(pEl(-10, -46, 14, 14), '#e8b800');
  F(pEl(-10, -46, 5, 5), '#ffffff', { linea: false });
  const cinta = pPoli([[20, -24], [58, -12], [56, -2], [16, -12]]);
  F(cinta, '#fff4bf');
  for (let i = 0; i < 6; i++) { const x = 22 + i * 6.5; L(pLinea([[x, -20 + i * 2], [x - 1, -15 + i * 2]]), TINTA_OBJ, .35); }
  F(pRR(52, -16, 8, 16, 2), '#555a66');
}, { ancho: 50 });

registrarObjeto('bascula-bano', () => {                // vista de 3/4: la tapa se ve desde arriba
  F(pRR(-50, -30, 100, 26, 10), '#cfd5de', { sombra: 24 });
  F(pPoli([[-40, -70], [40, -70], [52, -30], [-52, -30]]), '#f3f5f8', { sombra: 26 });
  F(pRR(-16, -62, 32, 14, 4), '#2d2a3a');
  F(pRR(-11, -58, 22, 6, 2), '#7ee0a0', { linea: false });
  F(pEl(-20, -40, 14, 6), '#e2e6ec', { linea: false }); F(pEl(20, -40, 14, 6), '#e2e6ec', { linea: false });   // donde van los pies
}, { ancho: 54 });

registrarEscenario('consultorio-nutricion', p => {
  const g = _g;
  g.fillStyle = _reg(p.pared); g.fillRect(0, 0, W, H);
  g.fillStyle = _reg(claro(p.pared, .35)); for (let y = 0; y < PISO_Y; y += 90) g.fillRect(0, y, W, 44);     // pared a rayas horizontales suaves
  // repisa con frascos de semillas y una planta, a los lados
  F(pRR(40, 900, 260, 18, 6), oscuro(p.piso, .75));
  [[88, '#ffd166', 80], [160, '#c8e38a', 100], [232, '#ff9f7a', 70]].forEach(([x, c, h]) => {
    F(pRR(x - 28, 900 - h, 56, h, 12), '#eaf6ff', { sombra: x + 12 });
    F(pRR(x - 22, 900 - h * .6, 44, h * .6 - 6, 8), c, { linea: false });
    F(pRR(x - 24, 900 - h - 14, 48, 16, 5), oscuro(p.acento, .9));
  });
  F(pRR(800, 900, 240, 18, 6), oscuro(p.piso, .75));
  F(pPoli([[870, 900], [950, 900], [940, 820], [880, 820]]), p.acento2);
  [[-.7, 60], [-.2, 80], [.35, 70], [.8, 55]].forEach(([a, l]) => F(pEl(910 + Math.sin(a) * l * .5, 800 - Math.cos(a) * l * .5, 14, l * .5, a), VERDE, { sombra: 910 }));
  F(pEl(990, 860, 24, 26), ROJO, { brillo: [976, 846, 6, 10] });
  // pizarrón de menú semanal (sin texto: renglones)
  F(pRR(820, 400, 220, 280, 14), '#3c4a44');
  L(pRR(820, 400, 220, 280, 14), oscuro(p.piso, .6), 1.4);
  for (let i = 0; i < 6; i++) { F(pRR(846, 440 + i * 38, 30, 10, 4), '#ffffff', { linea: false }); F(pRR(890, 440 + i * 38, 110 - (i % 3) * 22, 10, 4), claro(p.acento2, .4), { linea: false }); }
  // mesa/escritorio
  F(pRR(-20, PISO_Y - 6, W + 40, 146, 10), p.piso, { sombra: 'abajo:' + (PISO_Y + 118) });
  L(pLinea([[0, PISO_Y + 60], [W, PISO_Y + 60]]), oscuro(p.piso, .93), .5);
  g.fillStyle = _reg(p.fondo); g.fillRect(0, PISO_Y + 140, W, H - PISO_Y);
  g.fillStyle = _reg(oscuro(p.fondo, .92)); for (let x = 0; x < W; x += 120) g.fillRect(x, PISO_Y + 140, 6, H);
  g.fillStyle = _reg(oscuro(p.fondo, .85)); g.fillRect(0, PISO_Y + 140, W, 14);
});

registrarKit('nutricionista', {
  nombre: 'Nutrición',
  paleta: { fondo: '#cfe9d0', pared: '#eaf6e6', piso: '#fdfaf2', acento: '#5cbf6a', acento2: '#ff9a3c', tinta: '#23352a' },
  escenario: 'consultorio-nutricion',
  objetos: ['plato-buen-comer', 'manzana', 'aguacate', 'brocoli', 'vaso-agua', 'tupper', 'carrito-super', 'caja-cereal', 'barra-proteina', 'pan-molde', 'etiqueta-nutrimental', 'cinta-metrica', 'bascula-bano'],
});
})();
