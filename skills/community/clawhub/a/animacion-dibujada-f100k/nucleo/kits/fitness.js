// KIT COACH FITNESS — se carga después de nucleo/objetos.js
(() => {
const NARANJA = '#ff6b3d', TEAL = '#2ec4b6', GRAFITO = '#2f3440', METAL = '#c3c8d2', BLANCO = '#f7f8fa', AMARILLO = '#ffd23f';

registrarObjeto('mancuerna', () => {                    // acostada en el piso
  F(pRR(-34, -38, 68, 14, 7), METAL, { sombra: 'abajo:-31' });                 // agarre
  for (let x = -26; x <= 26; x += 6) L(pLinea([[x, -37], [x - 3, -25]]), '#9aa2ae', .35);
  [-1, 1].forEach(s => {
    F(pRR(s > 0 ? 30 : -46, -60, 16, 58, 6), GRAFITO, { sombra: s > 0 ? 40 : -34, brillo: [s > 0 ? 33 : -43, -56, 4, 30] });
    F(pRR(s > 0 ? 44 : -60, -52, 16, 42, 6), GRAFITO, { sombra: s > 0 ? 54 : -48 });
    F(pRR(s > 0 ? 58 : -66, -36, 8, 12, 3), METAL);
  });
}, { ancho: 62 });

registrarObjeto('pesa-rusa', () => {
  L(pSuave([[-24, -58], [-28, -84], [-14, -100], [14, -100], [28, -84], [24, -58]], false, .9), GRAFITO, 3.2);
  L(pSuave([[-24, -58], [-28, -84], [-14, -100], [14, -100], [28, -84], [24, -58]], false, .9), '#4a505e', 1.6);
  const cuerpo = pSuave([[-12, -2], [-38, -12], [-46, -38], [-34, -66], [0, -76], [34, -66], [46, -38], [38, -12], [12, -2]], true, .9);
  F(cuerpo, NARANJA, { sombra: 16, brillo: [-34, -62, 10, 24] });
  F(pRR(-30, -46, 60, 10, 5), '#ffffff', { linea: false });                    // franja, sin números
}, { ancho: 48 });

registrarObjeto('tapete', () => {                        // enrollado, parado
  F(pRR(-22, -92, 44, 90, 12), TEAL, { sombra: 8, brillo: [-17, -84, 7, 70] });
  F(pEl(0, -92, 22, 10), '#7fded4');
  L(pSuave([[0, -92], [6, -95], [8, -90], [2, -86], [-6, -89], [-10, -95], [-2, -101], [10, -99], [14, -91]], false, .9), '#1f9d91', .55);
  F(pRR(-26, -62, 52, 8, 4), GRAFITO); F(pRR(-26, -30, 52, 8, 4), GRAFITO);   // correas
}, { ancho: 26 });

registrarObjeto('botella-agua', () => {
  F(pRR(-12, -100, 24, 12, 5), GRAFITO);                                         // pico
  F(pRR(-20, -90, 40, 12, 4), '#4a505e');
  const cuerpo = pRR(-24, -80, 48, 78, 12);
  F(cuerpo, '#dff4ff', { sombra: 10, k: .92 });
  _g.save(); _g.clip(cuerpo); F(pRR(-30, -48, 60, 60, 0), '#7cc8f0', { linea: false }); F(pRR(-30, -50, 60, 6, 3), '#a9dcf6', { linea: false }); _g.restore();
  if (_modo === 'vector') L(cuerpo, null, 1);
  F(pRR(-16, -72, 8, 50, 4), '#ffffff', { linea: false });
  L(pEl(28, -76, 8, 10), GRAFITO, .9);                                          // asa
}, { ancho: 28 });

registrarObjeto('cronometro', t => {
  F(pRR(-8, -104, 16, 12, 3), METAL); F(pRR(-14, -96, 28, 8, 3), GRAFITO);
  F(pRR(26, -94, 12, 10, 3), METAL, {});
  F(pEl(0, -46, 44, 44), NARANJA, { sombra: 16 });
  F(pEl(0, -46, 35, 35), '#ffffff', { linea: false });
  for (let i = 0; i < 12; i++) { const a = i / 12 * Math.PI * 2, r0 = i % 3 ? 30 : 26; L(pLinea([[Math.cos(a) * r0, -46 + Math.sin(a) * r0], [Math.cos(a) * 33, -46 + Math.sin(a) * 33]]), GRAFITO, .45); }
  const a = -Math.PI / 2 + t * 3.2;
  F(pEl(0, -46, 30, 30, 0, -Math.PI / 2, a, false), 'rgba(255,107,61,.18)', { linea: false });
  L(pLinea([[0, -46], [Math.cos(a) * 28, -46 + Math.sin(a) * 28]]), NARANJA, .8);
  F(pEl(0, -46, 4, 4), GRAFITO, { linea: false });
}, { ancho: 44, anima: true });

registrarObjeto('tenis', () => {                         // de lado, punta a la derecha
  // suela gruesa con dibujo
  F(pSuave([[-56, -2], [-58, -16], [50, -16], [62, -10], [60, -2]], true, .5), BLANCO, { sombra: 'abajo:-7' });
  for (let x = -48; x < 52; x += 12) L(pLinea([[x, -3], [x + 5, -3]]), '#b7bdc7', .6);
  // capellada: talón alto, tobillo abierto y punta baja
  const arriba = pSuave([[-54, -16], [-56, -52], [-50, -70], [-36, -72], [-24, -60], [-6, -52], [18, -40], [44, -30], [60, -18]], true, .7);
  F(arriba, NARANJA, { sombra: 'abajo:-26', brillo: [-50, -64, 7, 26] });
  F(pSuave([[-50, -68], [-38, -68], [-30, -60], [-44, -56]], true, .8), GRAFITO, { linea: false });      // boca del tobillo
  F(pSuave([[26, -36], [46, -28], [60, -18], [40, -18]], true, .7), '#ffffff', { sombra: 'abajo:-22' }); // puntera
  F(pSuave([[-56, -30], [-40, -30], [-40, -16], [-56, -16]], true, .4), GRAFITO);                        // contrafuerte
  [[-18, -56], [-8, -50], [2, -45], [12, -40]].forEach(([x, y]) => L(pLinea([[x - 6, y - 6], [x + 5, y + 4]]), '#ffffff', .9));
  L(pSuave([[-36, -34], [-4, -32], [26, -24]], false), '#ffffff', 1);                                     // la curva de lado
}, { ancho: 60 });

registrarObjeto('cinta-metrica', () => {
  F(pSuave([[-4, -10], [30, -12], [58, -6], [60, 0], [-4, 0]], true, .4), AMARILLO, { sombra: 'abajo:-4' });   // la cinta sale al piso
  for (let x = 6; x < 56; x += 7) L(pLinea([[x, -10], [x, x % 14 ? -6 : -3]]), GRAFITO, .35);
  F(pEl(-18, -40, 38, 38), TEAL, { sombra: -2 });
  F(pEl(-18, -40, 24, 24), '#8fe3da', { linea: false });
  F(pEl(-18, -40, 9, 9), GRAFITO);
  F(pRR(14, -18, 10, 16, 3), GRAFITO);
}, { ancho: 60 });

registrarObjeto('bote-suplemento', () => {               // «el bote que explica el suplemento»: sin marca
  F(pRR(-34, -100, 68, 16, 6), GRAFITO, { sombra: 18 });
  for (let x = -28; x <= 28; x += 7) L(pLinea([[x, -98], [x, -86]]), '#4a505e', .35);
  F(pRR(-38, -86, 76, 84, 12), BLANCO, { sombra: 18, brillo: [-32, -80, 8, 70] });
  F(pRR(-38, -66, 76, 42, 0), NARANJA, { linea: false });
  if (_modo === 'vector') L(pRR(-38, -86, 76, 84, 12), null, 1);
  F(pEstrella(0, -45, 14, 6), '#ffffff', { linea: false });
  L(pLinea([[-26, -16], [26, -16]]), '#c9ced8', .5); L(pLinea([[-18, -10], [18, -10]]), '#c9ced8', .5);
}, { ancho: 40 });

registrarObjeto('carpeta-rutinas', () => {               // la carpeta llena de rutinas descargadas
  F(pRR(-46, -72, 92, 70, 6), '#f0b35a', { sombra: 30 });
  [[-38, -96, -.12, '#ffffff'], [-26, -100, .06, '#eef4ff'], [-12, -94, .16, '#ffffff'], [2, -98, -.05, '#fff6e6']].forEach(([x, y, r, c]) => {
    _g.save(); _g.translate(x + 20, y + 30); _g.rotate(r);
    F(pRR(-20, -30, 44, 56, 3), c, { sombra: 'abajo:14', k: .93 });
    [-18, -10, -2, 6].forEach(yy => L(pLinea([[-12, yy], [16, yy]]), '#b7c0d0', .45));
    _g.restore();
  });
  F(pPoli([[-50, -60], [-12, -60], [-6, -66], [50, -66], [46, -2], [-46, -2]]), '#ffc46e', { sombra: 30 });
  L(pLinea([[-30, -30], [30, -30]]), '#d99a3e', .5);
}, { ancho: 52 });

registrarObjeto('banda-elastica', () => {               // liga de resistencia con agarraderas, colgando en U
  const tubo = pSuave([[-30, -86], [-34, -40], [-18, -8], [0, -2], [18, -8], [34, -40], [30, -86]], false, .9);
  if (_modo === 'vector') { _g.lineCap = 'round'; _g.strokeStyle = _tinta; _g.lineWidth = 11 + _lw * 2; _g.stroke(tubo); }
  _g.lineCap = 'round'; _g.strokeStyle = _reg(TEAL); _g.lineWidth = _modo === 'pixel' ? 9 : 11; _g.stroke(tubo);
  L(pSuave([[-27, -80], [-30, -40], [-16, -12]], false), '#8fe3da', .5);
  [-1, 1].forEach(s => {
    F(pRR(s * 30 - 7, -100, 14, 20, 4), '#8a909c');
    F(pRR(s * 30 - 20, -104, 40, 14, 7), GRAFITO, { brillo: [s * 30 - 16, -102, 12, 4] });
  });
}, { ancho: 40 });

registrarObjeto('toalla-gym', () => {                    // toallas dobladas, una sobre otra
  [[-2, '#ffffff', 0], [-28, TEAL, 4], [-54, NARANJA, -3]].forEach(([y, c, dx]) => {
    F(pRR(-44 + dx, y - 24, 88, 24, 8), c, { sombra: 'abajo:' + (y - 8), k: .88 });
    L(pLinea([[-38 + dx, y - 10], [38 + dx, y - 10]]), oscuro(c, .8), .4);
  });
}, { ancho: 46 });

registrarObjeto('libreta-progreso', () => {              // semanas y kilos levantados, nunca la báscula
  F(pRR(-40, -96, 80, 94, 6), '#ffffff', { sombra: 26 });
  F(pRR(-40, -96, 12, 94, 4), GRAFITO);
  for (let y = -84; y < -6; y += 12) F(pEl(-34, y, 3, 3), '#8a909c', { linea: false });
  L(pLinea([[-20, -16], [32, -16]]), '#b7c0d0', .5); L(pLinea([[-20, -16], [-20, -84]]), '#b7c0d0', .5);
  L(pLinea([[-16, -26], [-4, -36], [8, -32], [20, -54], [30, -70]]), NARANJA, .9);
  [[-16, -26], [-4, -36], [8, -32], [20, -54], [30, -70]].forEach(([x, y]) => F(pEl(x, y, 3.5, 3.5), NARANJA, { linea: false }));
}, { ancho: 42 });

registrarEscenario('gimnasio', p => {
  const g = _g;
  g.fillStyle = _reg(p.pared); g.fillRect(0, 0, W, PISO_Y);
  g.fillStyle = _reg(oscuro(p.pared, .93)); g.fillRect(0, PISO_Y - 300, W, 300);                           // zócalo
  g.fillStyle = _reg(p.acento); g.fillRect(0, PISO_Y - 318, W, 22);                                        // franja de color
  g.fillStyle = _reg(p.acento2); g.fillRect(0, PISO_Y - 296, W, 10);
  // árbol de discos a la izquierda: se reconoce de lejos
  F(pRR(126, 700, 16, 334, 5), '#8a909c'); F(pRR(80, 1024, 108, 14, 5), '#6e7482');
  [[134, 760, 76, '#2f3440'], [134, 880, 62, p.acento], [134, 972, 50, '#2f3440']].forEach(([x, y, r, c]) => {
    F(pEl(x, y, r, r), c, { sombra: x + r * .3, k: .85 }); F(pEl(x, y, r * .62, r * .62), oscuro(c, .8), { linea: false });
    F(pEl(x, y, r * .2, r * .2), '#c3c8d2');
  });
  // cuerda de saltar colgada en un gancho
  F(pRR(330, 760, 22, 22, 6), '#8a909c');
  L(pSuave([[330, 790], [300, 900], [318, 1000], [346, 1010], [360, 900], [352, 790]], false, .8), p.acento2, 1.2);
  F(pRR(290, 990, 18, 50, 7), '#2f3440'); F(pRR(352, 990, 18, 50, 7), '#2f3440');
  // espejo con marco a la derecha
  F(pRR(740, 640, 300, 420, 14), '#8a909c');
  F(pRR(756, 656, 268, 388, 8), '#dff1f7', { linea: false });
  F(pPoli([[790, 690], [850, 690], [780, 850]]), '#ffffff', { linea: false }); F(pPoli([[880, 690], [910, 690], [800, 960], [780, 960]]), '#ffffff', { linea: false });
  // piso de hule con juntas y la línea amarilla
  g.fillStyle = _reg(p.piso); g.fillRect(0, PISO_Y, W, H - PISO_Y);
  g.fillStyle = _reg(claro(p.piso, .14)); for (let x = 90; x < W; x += 180) g.fillRect(x, PISO_Y + 40, 5, H);
  for (let y = PISO_Y + 190; y < H; y += 170) g.fillRect(0, y, W, 5);
  g.fillStyle = _reg('#ffd23f'); g.fillRect(0, PISO_Y + 26, W, 12);
  g.fillStyle = _reg(oscuro(p.piso, .82)); g.fillRect(0, PISO_Y, W, 16);
});

registrarKit('fitness', {
  nombre: 'Fitness',
  paleta: { fondo: '#e7f6ee', pared: '#d6efe2', piso: '#6b7486', acento: '#ff6b3d', acento2: '#2ec4b6', tinta: '#1f2430' },
  escenario: 'gimnasio',
  objetos: ['pesa-rusa', 'botella-agua', 'tapete', 'bote-suplemento', 'tenis', 'cronometro', 'mancuerna', 'carpeta-rutinas', 'libreta-progreso', 'cinta-metrica', 'banda-elastica', 'toalla-gym'],
});
registrarKit('coach-fitness', KITS.fitness);
})();
