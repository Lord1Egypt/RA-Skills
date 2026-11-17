// KIT TIENDA DE ROPA — se carga después de nucleo/objetos.js
// ANATOMIA: estilizada — el maniquí es un torso de tienda sin cabeza ni extremidades (forma de busto de costura)
(() => {
const ROSA = '#ff8fab', MALVA = '#b98ae0', MOSTAZA = '#f2b33d', MARINO = '#2f3a5a', NEGRO = '#34323d', BLANCO = '#fbfaf6', MADERA = '#c98a4a', METAL = '#b7bdc7';

// una camisa/blusa vista de frente: cuerpo + los dos lados de tela de los costados, cuello en V
function camisa(col, o = {}) {
  const { y = 0, s = 1, cuello = true, botones = true } = o;
  _g.save(); _g.translate(0, y); _g.scale(s, s);
  F(pPoli([[-26, -86], [-46, -74], [-58, -40], [-44, -34], [-34, -58], [-32, -4], [32, -4], [34, -58], [44, -34], [58, -40], [46, -74], [26, -86]]), col, { sombra: 18, k: .88 });
  if (cuello) { F(pPoli([[-26, -86], [-12, -88], [0, -76], [12, -88], [26, -86], [0, -70]]), oscuro(col, .9));   // cuello camisero chico
    F(pPoli([[-14, -88], [0, -76], [-4, -70], [-18, -82]]), claro(col, .3)); F(pPoli([[14, -88], [0, -76], [4, -70], [18, -82]]), claro(col, .3)); }
  if (botones) [-54, -40, -26, -12].forEach(yy => F(pEl(0, yy, 2.6, 2.6), oscuro(col, .7), { linea: false }));
  _g.restore();
}

registrarObjeto('gancho-ropa', () => {
  L(pSuave([[0, -84], [6, -92], [0, -100], [-6, -94]], false, .8), METAL, 1.3);
  F(pPoli([[0, -84], [50, -46], [46, -40], [-46, -40], [-50, -46]]), MADERA, { sombra: 'abajo:-46' });
  F(pRR(-46, -46, 92, 8, 4), oscuro(MADERA, .85));
}, { ancho: 50 });

registrarObjeto('camisa-blanca', () => {
  L(pSuave([[0, -88], [4, -96], [0, -104], [-4, -98]], false, .8), METAL, 1.1);
  F(pPoli([[0, -88], [34, -80], [-34, -80]]), MADERA, { linea: false });
  camisa(BLANCO, { y: 4 });
  F(pRR(-24, -52, 14, 12, 2), oscuro(BLANCO, .92));                       // bolsillo
}, { ancho: 56 });

registrarObjeto('vestido', () => {
  L(pSuave([[0, -94], [4, -102], [0, -108], [-4, -103]], false, .8), METAL, 1.1);
  F(pPoli([[-16, -94], [-10, -94], [-6, -76], [6, -76], [10, -94], [16, -94], [18, -64], [-18, -64]]), ROSA, { sombra: 6 });   // tirantes y cuerpo
  F(pSuave([[-18, -64], [18, -64], [30, -40], [46, -6], [0, 0], [-46, -6], [-30, -40]], true, .5), ROSA, { sombra: 8, k: .86 });
  F(pRR(-19, -68, 38, 8, 3), oscuro(ROSA, .85));                          // cinturón
  [-24, -8, 8, 24].forEach(x => L(pLinea([[x * .5, -58], [x, -6]]), oscuro(ROSA, .88), .5));
}, { ancho: 48 });

registrarObjeto('pantalon-negro', () => {
  F(pPoli([[-30, -96], [30, -96], [34, -2], [10, -2], [0, -60], [-10, -2], [-34, -2]]), NEGRO, { sombra: 4, k: .8 });
  F(pRR(-31, -98, 62, 12, 3), oscuro(NEGRO, .8));
  [-18, 0, 18].forEach(x => F(pRR(x - 3, -98, 6, 12, 1), '#4a4854', { linea: false }));
  L(pLinea([[-20, -86], [-24, -4]]), '#4a4854', .4); L(pLinea([[20, -86], [24, -4]]), '#4a4854', .4);
  F(pEl(0, -92, 3, 3), METAL, { linea: false });
}, { ancho: 38 });

registrarObjeto('chaqueta-cuero', () => {
  F(pPoli([[-24, -88], [-48, -74], [-58, -8], [-44, -6], [-36, -54], [-34, -4], [34, -4], [36, -54], [44, -6], [58, -8], [48, -74], [24, -88]]), '#5b3a2e', { sombra: 16, k: .82 });
  F(pPoli([[-24, -88], [-4, -50], [-10, -30], [-22, -60]]), '#7a5040');   // solapas
  F(pPoli([[24, -88], [4, -50], [10, -30], [22, -60]]), '#6a4436');
  L(pLinea([[2, -48], [6, -6]]), '#c3c8d2', .7);                          // cierre
  F(pRR(-28, -34, 14, 4, 2), '#c3c8d2', { linea: false }); F(pRR(16, -34, 14, 4, 2), '#c3c8d2', { linea: false });
}, { ancho: 58 });

registrarObjeto('falda-larga', () => {
  F(pRR(-24, -96, 48, 10, 3), oscuro(MALVA, .8));
  F(pSuave([[-24, -86], [24, -86], [38, -40], [50, -4], [0, 0], [-50, -4], [-38, -40]], true, .5), MALVA, { sombra: 10, k: .86 });
  [-30, -12, 6, 24].forEach(x => L(pLinea([[x * .45, -84], [x, -4]]), oscuro(MALVA, .86), .5));
  F(pEl(-14, -60, 4, 4), '#ffffff', { linea: false }); F(pEl(16, -40, 4, 4), '#ffffff', { linea: false }); F(pEl(-24, -22, 4, 4), '#ffffff', { linea: false });
}, { ancho: 50 });

registrarObjeto('prenda-doblada', () => {                 // pila de 3 prendas dobladas
  [[MARINO, -2], [MOSTAZA, -24], [ROSA, -46]].forEach(([c, y], i) => {
    F(pRR(-46 + i * 3, y - 22, 92 - i * 6, 22, 7), c, { sombra: 'abajo:' + (y - 8) });
    L(pLinea([[-30 + i * 3, y - 11], [30 - i * 3, y - 11]]), oscuro(c, .85), .45);
  });
  F(pRR(-12, -80, 24, 12, 3), '#ffffff'); L(pLinea([[-6, -74], [6, -74]]), '#8a8fa0', .4);   // etiquetita
}, { ancho: 50 });

registrarObjeto('etiqueta-precio', () => {
  _g.save(); _g.translate(0, -50); _g.rotate(-.35);
  F(pPoli([[-30, -40], [18, -40], [40, 0], [18, 40], [-30, 40]]), '#ffe066', { sombra: 20, k: .88 });
  F(pEl(20, 0, 6, 6), '#ffffff');
  L(pSuave([[26, 0], [42, -14], [56, -30]], false), '#8a8fa0', .6);
  T('$', -8, 0, 36, '#b07d10');
  _g.restore();
}, { ancho: 46 });

registrarObjeto('bolsa-tienda', () => {
  L(pEl(-10, -78, 14, 16, 0, Math.PI, Math.PI * 2, false), MARINO, 1.5); L(pEl(10, -78, 14, 16, 0, Math.PI, Math.PI * 2, false), MARINO, 1.5);
  F(pRR(-38, -80, 76, 78, 4), '#ffffff', { sombra: 20 });
  F(pPoli([[38, -80], [50, -72], [50, -6], [38, -2]]), '#e6e8ee');
  F(pRR(-38, -38, 76, 14, 0), ROSA, { linea: false });
  F(pEl(0, -58, 10, 10), ROSA, { linea: false }); F(pEl(0, -58, 4, 4), '#ffffff', { linea: false });
}, { ancho: 48 });

registrarObjeto('perchero', () => {                      // riel con 4 prendas colgadas
  F(pRR(-58, -100, 116, 7, 3), METAL);
  F(pRR(-56, -100, 6, 98, 3), METAL); F(pRR(50, -100, 6, 98, 3), METAL);
  F(pRR(-66, -6, 30, 6, 3), '#8a909c'); F(pRR(36, -6, 30, 6, 3), '#8a909c');
  [[-30, ROSA], [-10, MOSTAZA], [10, MARINO], [30, BLANCO]].forEach(([x, c], i) => {
    L(pSuave([[x, -94], [x + 3, -99], [x, -103]], false, .8), '#8a909c', .6);
    _g.save(); _g.translate(x, -90); _g.scale(.34, .34);
    if (i === 1) { F(pSuave([[-22, 0], [22, 0], [44, 100], [-44, 100]], true, .4), c, { sombra: 10 }); }
    else camisa(c, { y: 88, botones: i !== 3 });
    _g.restore();
  });
}, { ancho: 60 });

registrarObjeto('maniqui', () => {                        // busto de costura sobre su pie: sin cabeza
  F(pRR(-4, -40, 8, 34, 3), MADERA);
  F(pPoli([[-26, -4], [26, -4], [30, 0], [-30, 0]]), oscuro(MADERA, .8));
  L(pLinea([[0, -8], [-22, -2]]), oscuro(MADERA, .8), 1); L(pLinea([[0, -8], [22, -2]]), oscuro(MADERA, .8), 1);
  F(pSuave([[-8, -100], [8, -100], [10, -92], [32, -86], [36, -70], [26, -56], [24, -46], [30, -38], [0, -34], [-30, -38], [-24, -46], [-26, -56], [-36, -70], [-32, -86], [-10, -92]], true, .7), '#e9d8c2', { sombra: 8, k: .88 });
  F(pRR(-6, -104, 12, 8, 3), MADERA);
  camisa(ROSA, { y: -36, s: .66, botones: false });                          // blusa puesta: cubre el pecho del busto
  L(pSuave([[-26, -56], [0, -50], [26, -56]], false), '#c8a98a', .5);
}, { ancho: 36 });

registrarObjeto('lavadora', t => {
  F(pRR(-46, -100, 92, 98, 8), '#f1f3f6', { sombra: 26 });
  F(pRR(-46, -100, 92, 18, 8), '#dfe3ea');
  F(pRR(18, -95, 20, 8, 3), '#7ee0a0'); F(pEl(-30, -91, 5, 5), '#8a909c');
  F(pEl(0, -46, 32, 32), '#c3c8d2');
  F(pEl(0, -46, 24, 24), '#bfe6ff', { linea: false });
  _g.save(); _g.clip(pEl(0, -46, 24, 24));
  const a = t * 5;
  [[ROSA, 0], [MARINO, 2.1], [MOSTAZA, 4.2]].forEach(([c, d]) => F(pEl(Math.cos(a + d) * 11, -46 + Math.sin(a + d) * 11, 10, 7, a + d), c, { linea: false }));
  F(pEl(-8, -56, 5, 8, -.5), '#ffffff', { linea: false });
  _g.restore();
  F(pRR(-40, -8, 10, 6, 2), '#8a909c'); F(pRR(30, -8, 10, 6, 2), '#8a909c');
}, { ancho: 48, anima: true });

registrarObjeto('espejo-probador', () => {
  F(pRR(-38, -100, 76, 94, 38), MADERA, { sombra: 24 });
  F(pRR(-30, -92, 60, 80, 30), '#dff3fb', { linea: false });
  F(pPoli([[-18, -80], [-6, -80], [-24, -40], [-30, -40]]), '#ffffff', { linea: false });
  F(pPoli([[4, -80], [10, -80], [-8, -46], [-12, -46]]), '#ffffff', { linea: false });
  F(pRR(-30, -6, 12, 6, 2), oscuro(MADERA, .8)); F(pRR(18, -6, 12, 6, 2), oscuro(MADERA, .8));
}, { ancho: 40 });

registrarEscenario('boutique', p => {
  const g = _g;
  g.fillStyle = _reg(p.pared); g.fillRect(0, 0, W, H);
  // papel tapiz de rombos suaves
  g.fillStyle = _reg(claro(p.pared, .3));
  for (let y = 0; y < PISO_Y; y += 120) for (let x = (y / 120 % 2) * 60; x < W; x += 120) { g.beginPath(); g.moveTo(x, y); g.lineTo(x + 30, y + 60); g.lineTo(x, y + 120); g.lineTo(x - 30, y + 60); g.fill(); }
  // probador: cabina con marco de madera, el hueco oscuro adentro y la cortina recogida a un lado
  F(pRR(30, 500, 300, 830, 14), MADERA, { sombra: 290 });
  F(pRR(56, 540, 248, 790, 6), oscuro(p.pared, .82), { linea: false });
  F(pRR(150, 640, 120, 300, 50), '#dff3fb');                                  // el espejo de adentro
  F(pPoli([[176, 670], [196, 670], [164, 760], [156, 760]]), '#ffffff', { linea: false });
  F(pRR(50, 548, 260, 12, 6), METAL);
  const cortina = pSuave([[58, 560], [150, 560], [140, 800], [120, 960], [132, 1240], [90, 1250], [52, 1244]], true, .5);
  F(cortina, p.acento, { sombra: 118, k: .86 });
  [74, 96, 118].forEach(x => L(pSuave([[x, 566], [x + 2, 800], [x - 8, 960], [x, 1236]], false), oscuro(p.acento, .82), .6));
  F(pRR(104, 930, 34, 22, 8), p.acento2);                                     // el lazo que la recoge
  F(pRR(120, 420, 120, 60, 10), '#ffffff'); T('PROBADOR', 180, 450, 20, oscuro(p.acento, .7));
  // perchero de pared (derecha) con prendas
  F(pRR(780, 700, 260, 10, 5), METAL);
  [[835, ROSA], [910, MOSTAZA], [985, MARINO]].forEach(([x, c], i) => {
    L(pSuave([[x, 706], [x + 5, 696], [x, 688]], false, .8), '#8a909c', .9);
    g.save(); g.translate(x, 712); g.scale(.95, .95); camisa(c, { y: 88, botones: i % 2 === 0 }); g.restore();
  });
  // estante con prendas dobladas
  F(pRR(780, 980, 260, 16, 6), oscuro(p.piso, .75));
  [[830, MARINO], [910, ROSA], [990, MALVA]].forEach(([x, c]) => [0, 1].forEach(j => F(pRR(x - 34, 980 - 22 - j * 22, 68, 20, 6), j ? claro(c, .2) : c)));
  // mostrador
  F(pRR(-20, PISO_Y - 6, W + 40, 146, 10), p.piso, { sombra: 'abajo:' + (PISO_Y + 118) });
  L(pLinea([[0, PISO_Y + 60], [W, PISO_Y + 60]]), oscuro(p.piso, .93), .5);
  g.fillStyle = _reg(p.fondo); g.fillRect(0, PISO_Y + 140, W, H - PISO_Y);
  g.fillStyle = _reg(oscuro(p.fondo, .9)); for (let x = 60; x < W; x += 180) g.fillRect(x, PISO_Y + 140, 8, H);
  g.fillStyle = _reg(oscuro(p.fondo, .82)); g.fillRect(0, PISO_Y + 140, W, 14);
});

registrarKit('tienda-ropa', {
  nombre: 'Moda',
  paleta: { fondo: '#d9c3ea', pared: '#f6ecf4', piso: '#fffaf5', acento: '#ff8fab', acento2: '#b98ae0', tinta: '#2e2436' },
  escenario: 'boutique',
  objetos: ['perchero', 'camisa-blanca', 'vestido', 'pantalon-negro', 'chaqueta-cuero', 'falda-larga', 'prenda-doblada', 'gancho-ropa', 'etiqueta-precio', 'bolsa-tienda', 'maniqui', 'lavadora', 'espejo-probador'],
});
registrarKit('ropa', KITS['tienda-ropa']);
})();
