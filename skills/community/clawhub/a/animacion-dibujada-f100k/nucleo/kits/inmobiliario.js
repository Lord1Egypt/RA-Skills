// KIT AGENTE INMOBILIARIO — se carga después de nucleo/objetos.js
(() => {
const TEJA = '#e0674a', MURO = '#fff1dc', AZUL = '#4c7fd6', VERDE = '#5cbf6a', PAPEL = '#ffffff', MADERA = '#b97e45', DORADO = '#f2b33d', METAL = '#b7bdc7';

registrarObjeto('casa', () => {
  F(pRR(26, -100, 14, 26, 2), '#a55a42');                                          // chimenea
  F(pRR(-44, -60, 88, 58, 3), MURO, { sombra: 24 });
  F(pPoli([[-54, -56], [0, -98], [54, -56]]), TEJA, { sombra: 0, k: .86, grosor: 1.1 });
  F(pRR(-12, -38, 24, 36, 3), '#8a5a3b'); F(pEl(6, -20, 2.4, 2.4), DORADO, { linea: false });
  [[-34, -46], [18, -46]].forEach(([x, y]) => { F(pRR(x, y, 18, 18, 2), '#9fd8ff'); L(pLinea([[x + 9, y], [x + 9, y + 18]]), PAPEL, .6); L(pLinea([[x, y + 9], [x + 18, y + 9]]), PAPEL, .6); });
  F(pEl(0, -70, 7, 7), '#9fd8ff');
  F(pEl(-52, -8, 12, 10), VERDE, { sombra: -52 }); F(pEl(52, -8, 12, 10), VERDE, { sombra: 52 });
}, { ancho: 56 });

registrarObjeto('edificio', () => {
  F(pRR(-34, -100, 68, 98, 4), '#c9d6ea', { sombra: 16 });
  F(pRR(-38, -104, 76, 8, 3), '#9fb2d0');
  for (let f = 0; f < 5; f++) for (let c = 0; c < 3; c++) {
    const on = (f * 3 + c) % 4 === 1;
    F(pRR(-26 + c * 19, -92 + f * 16, 13, 10, 2), on ? '#ffe680' : '#7aa7e0', { linea: false });
  }
  F(pRR(-9, -18, 18, 16, 2), '#6b7fa0');
}, { ancho: 40 });

registrarObjeto('llave', () => {
  _g.save(); _g.translate(0, -50); _g.rotate(-.5);
  F(pEl(-30, 0, 20, 20), DORADO, { sombra: -24 });
  F(pEl(-30, 0, 8, 8), '#fff4bf', { linea: false });
  F(pRR(-12, -6, 62, 12, 3), DORADO, { sombra: 'abajo:2' });
  F(pRR(30, 4, 8, 12, 1), DORADO); F(pRR(42, 4, 8, 9, 1), DORADO);
  _g.restore();
  // argolla y llavero colgando del ojo de la llave
  L(pEl(-40, -24, 9, 9), METAL, .9);
  F(pSuave([[-44, -16], [-34, -16], [-30, 0], [-48, 0]], true, .6), AZUL);
  F(pEl(-39, -8, 2.6, 2.6), '#ffffff', { linea: false });
}, { ancho: 50 });

registrarObjeto('letrero-se-vende', () => {
  F(pRR(-5, -70, 10, 68, 3), MADERA, { sombra: 0 });
  F(pRR(-5, -86, 58, 7, 3), MADERA);                                             // brazo del poste
  L(pLinea([[10, -79], [10, -70]]), '#555a66', .6); L(pLinea([[46, -79], [46, -70]]), '#555a66', .6);
  _g.save(); _g.translate(28, -52); _g.rotate(.04);
  F(pRR(-34, -20, 68, 40, 4), PAPEL, { sombra: 'abajo:8' });
  F(pRR(-34, -20, 68, 12, 4), '#e04a4a', { linea: false });
  T('SE VENDE', 0, 4, 12, '#e04a4a');
  _g.restore();
  F(pEl(0, -3, 16, 5), VERDE, { linea: false });
}, { ancho: 44 });

registrarObjeto('plano', () => {                          // plano de la casa, papel azul con líneas blancas
  _g.save(); _g.translate(0, -48); _g.rotate(-.06);
  F(pRR(-50, -40, 100, 80, 4), '#3f73c8', { sombra: 'abajo:30' });
  const b = '#dbe8ff';
  L(pRR(-38, -30, 76, 60, 1), b, .8);
  L(pLinea([[-4, -30], [-4, 4]]), b, .6); L(pLinea([[-38, 4], [18, 4]]), b, .6); L(pLinea([[18, 4], [18, 30]]), b, .6);
  L(pEl(-4, 4, 10, 10, 0, -Math.PI / 2, 0, false), b, .45);
  [[-26, -20], [12, -18], [-22, 16], [28, 16]].forEach(([x, y]) => F(pRR(x, y, 10, 5, 1), b, { linea: false }));
  F(pSuave([[40, 34], [52, 24], [56, 40], [46, 46]], true, .8), '#2f5aa0');     // esquina doblada
  _g.restore();
}, { ancho: 52 });

registrarObjeto('contrato', () => {
  F(pRR(-34, -96, 72, 92, 4), '#eef1f6', { sombra: 20 });                        // hoja de atrás
  F(pRR(-40, -100, 72, 92, 4), PAPEL, { sombra: 16 });
  F(pRR(-32, -90, 40, 7, 3), '#8a8fa0', { linea: false });
  for (let i = 0; i < 6; i++) F(pRR(-32, -76 + i * 9, 56 - (i % 3) * 10, 4, 2), '#c3c8d2', { linea: false });
  L(pSuave([[-30, -18], [-20, -26], [-12, -16], [-2, -24], [8, -18]], false), AZUL, .7);   // firma
  L(pLinea([[-32, -12], [22, -12]]), '#8a8fa0', .4);
  // pluma
  _g.save(); _g.translate(30, -30); _g.rotate(.7);
  F(pRR(-5, -40, 10, 44, 4), '#2d2a3a'); F(pPoli([[-5, 4], [5, 4], [0, 14]]), DORADO);
  _g.restore();
}, { ancho: 44 });

registrarObjeto('mapa-pin', () => {
  F(pPoli([[-50, -52], [-18, -60], [16, -50], [50, -58], [50, -4], [16, 4], [-18, -6], [-50, 2]]), '#e9f5dd', { sombra: 16 });
  F(pPoli([[-18, -60], [16, -50], [16, 4], [-18, -6]]), '#d9eccb', { linea: false });
  L(pSuave([[-46, -20], [-20, -34], [10, -22], [44, -36]], false), '#ffffff', 1.6);
  L(pSuave([[-30, -52], [-24, -26], [-30, 0]], false), '#ffffff', 1.2);
  F(pEl(30, -18, 12, 8), '#9fd8ff', { linea: false });
  // pin
  F(pSuave([[8, -58], [8, -96], [0, -104], [-8, -96], [-8, -58], [0, -46]], true, .9), '#e04a4a', { linea: false });
  F(pSuave([[0, -48], [-16, -74], [-14, -94], [0, -102], [14, -94], [16, -74]], true, .9), '#e04a4a', { sombra: 2 });
  F(pEl(0, -84, 6, 6), PAPEL, { linea: false });
}, { ancho: 52 });

registrarObjeto('calculadora', () => {
  F(pRR(-34, -100, 68, 98, 10), '#555a66', { sombra: 16 });
  F(pRR(-26, -90, 52, 22, 4), '#c9ecc0', { linea: false });
  T('- -', 8, -79, 12, '#3a5a36');
  for (let f = 0; f < 4; f++) for (let c = 0; c < 3; c++) F(pRR(-26 + c * 18, -60 + f * 14, 14, 10, 3), c === 2 && f === 3 ? '#ff8a5b' : '#e9edf2', { linea: false });
}, { ancho: 36 });

registrarObjeto('alcancia', () => {                        // cochinito para el enganche
  F(pRR(-26, -18, 10, 16, 4), '#f38aa6'); F(pRR(16, -18, 10, 16, 4), '#f38aa6');
  F(pEl(0, -46, 44, 34), '#ffa3bb', { sombra: 14, brillo: [-30, -68, 12, 18] });
  F(pEl(40, -46, 10, 12), '#ff8fab'); F(pEl(38, -48, 2.4, 2.4), '#c9557a', { linea: false }); F(pEl(38, -42, 2.4, 2.4), '#c9557a', { linea: false });
  F(pPoli([[18, -74], [26, -90], [32, -72]]), '#ff8fab');
  F(pEl(24, -58, 3.4, 3.4), TINTA_OBJ, { linea: false });
  F(pRR(-12, -82, 24, 5, 2), '#c9557a', { linea: false });
  // moneda entrando
  F(pEl(0, -94, 12, 12), DORADO); T('$', 0, -94, 13, '#b07d10');
}, { ancho: 46 });

registrarObjeto('carpeta', () => {                        // expediente de papeles
  F(pRR(-44, -80, 88, 76, 6), '#e9b949', { sombra: 20 });
  F(pRR(-36, -92, 62, 20, 4), PAPEL); F(pRR(-30, -100, 62, 20, 4), '#f6f8fb');
  F(pPoli([[-44, -68], [-12, -68], [-4, -78], [44, -78], [44, -4], [-44, -4]]), '#f2c85e', { sombra: 20 });
  F(pRR(-16, -46, 32, 14, 3), PAPEL); L(pLinea([[-10, -39], [10, -39]]), '#8a8fa0', .4);
}, { ancho: 46 });

registrarObjeto('porcentaje', () => {                     // globo de porcentaje (tasas, enganche)
  F(pEl(0, -52, 44, 44), AZUL, { sombra: 14, k: .86 });
  T('%', 0, -50, 50, '#ffffff');
}, { ancho: 44 });

registrarObjeto('lista-inspeccion', () => {               // tabla con lista palomeada (lo que se revisa en la visita)
  F(pRR(-38, -100, 76, 98, 6), '#c98a4a', { sombra: 18 });
  F(pRR(-30, -88, 60, 80, 3), PAPEL, { linea: false });
  F(pRR(-14, -106, 28, 14, 4), METAL);
  for (let i = 0; i < 4; i++) {
    const y = -76 + i * 18, ok = i < 3;
    F(pRR(-24, y, 10, 10, 2), '#eef1f6');
    if (ok) L(pLinea([[-22, y + 5], [-19, y + 8], [-13, y]]), VERDE, .8);
    F(pRR(-8, y + 3, 30 - (i % 2) * 8, 4, 2), '#c3c8d2', { linea: false });
  }
}, { ancho: 40 });

registrarEscenario('oficina-inmobiliaria', p => {
  const g = _g;
  g.fillStyle = _reg(p.pared); g.fillRect(0, 0, W, H);
  g.fillStyle = _reg(claro(p.pared, .3)); g.fillRect(0, PISO_Y - 380, W, 20);                     // moldura
  // ventana grande con vista a casas (derecha)
  F(pRR(640, 420, 380, 460, 18), '#ffffff');
  F(pRR(662, 442, 336, 416, 10), '#bfe6ff', { linea: false });
  g.save(); g.beginPath(); g.rect(662, 442, 336, 416); g.clip();
  F(pEl(760, 520, 40, 22), '#ffffff', { linea: false }); F(pEl(900, 560, 50, 24), '#ffffff', { linea: false });
  F(pRR(662, 780, 336, 80, 0), '#9bd88a', { linea: false });
  [[710, 780, TEJA], [800, 790, '#7aa7e0'], [900, 776, TEJA]].forEach(([x, y, c]) => {
    F(pRR(x - 34, y - 50, 68, 50, 2), MURO, { linea: false }); F(pPoli([[x - 42, y - 48], [x, y - 84], [x + 42, y - 48]]), c, { linea: false });
    F(pRR(x - 8, y - 26, 16, 26, 2), '#8a5a3b', { linea: false });
  });
  g.restore();
  F(pRR(826, 442, 8, 416, 2), '#ffffff', { linea: false }); F(pRR(662, 646, 336, 8, 2), '#ffffff', { linea: false });
  // cuadro de una casa (izquierda) y planta alta
  F(pRR(70, 560, 220, 170, 10), MADERA);
  F(pRR(84, 574, 192, 142, 4), '#3f73c8', { linea: false });
  L(pRR(110, 600, 140, 90, 1), '#dbe8ff', .7); L(pLinea([[180, 600], [180, 645]]), '#dbe8ff', .5); L(pLinea([[110, 645], [220, 645]]), '#dbe8ff', .5);
  F(pPoli([[930, 1330], [1010, 1330], [1000, 1240], [940, 1240]]), p.acento2);   // planta bajo la ventana (a la izquierda la tapaban los objetos)
  [[-.6, 110], [-.15, 150], [.3, 130], [.75, 100]].forEach(([a, l]) => F(pEl(970 + Math.sin(a) * l * .45, 1210 - Math.cos(a) * l * .45, 22, l * .5, a), VERDE, { sombra: 970 }));
  // escritorio
  F(pRR(-20, PISO_Y - 6, W + 40, 146, 10), p.piso, { sombra: 'abajo:' + (PISO_Y + 118) });
  L(pLinea([[0, PISO_Y + 60], [W, PISO_Y + 60]]), oscuro(p.piso, .93), .5);
  g.fillStyle = _reg(p.fondo); g.fillRect(0, PISO_Y + 140, W, H - PISO_Y);
  g.fillStyle = _reg(oscuro(p.fondo, .9)); for (let x = 0; x < W; x += 140) g.fillRect(x, PISO_Y + 140, 70, H);
  g.fillStyle = _reg(oscuro(p.fondo, .8)); g.fillRect(0, PISO_Y + 140, W, 14);
});

registrarKit('inmobiliario', {
  nombre: 'Inmuebles',
  paleta: { fondo: '#c7d3e8', pared: '#eef3fa', piso: '#f7efe3', acento: '#4c7fd6', acento2: '#e0674a', tinta: '#232b3d' },
  escenario: 'oficina-inmobiliaria',
  objetos: ['casa', 'letrero-se-vende', 'llave', 'plano', 'contrato', 'mapa-pin', 'calculadora', 'alcancia', 'carpeta', 'porcentaje', 'lista-inspeccion', 'edificio'],
});
registrarKit('agente-inmobiliario', KITS.inmobiliario);
registrarKit('bienes-raices', KITS.inmobiliario);
})();
