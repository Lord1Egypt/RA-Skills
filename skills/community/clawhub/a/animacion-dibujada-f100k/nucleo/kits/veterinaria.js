// KIT CLÍNICA VETERINARIA — se carga después de nucleo/objetos.js
// Los animales son personajes de caricatura redondos (cabeza grande, sin detalle realista).
(() => {
const CANELA = '#e3a15c', CANELA_C = '#f8dfb8', CAFE = '#8f5a32', GRIS = '#a3adbf', GRIS_F = '#7c879b', BLANCO = '#fbfbf8',
      ROJO = '#ef5b5b', ORO = '#f2c14e', MENTA = '#5bb5a2', AZUL = '#6fb7e8', ROSA = '#ff9fb2', TINTA_C = '#2a2530';

function ojito(x, y, r = 4.5) { F(pEl(x, y, r, r * 1.1), TINTA_C, { linea: false }); F(pEl(x - r * .35, y - r * .4, r * .38, r * .38), '#ffffff', { linea: false }); }
function huella(cx, cy, s, col) {                         // huellita: almohadilla + 4 deditos redondos
  F(pEl(cx, cy + s * .25, s * .55, s * .45), col, { linea: false });
  [[-.55, -.25], [-.2, -.55], [.2, -.55], [.55, -.25]].forEach(([a, b]) => F(pEl(cx + a * s, cy + b * s, s * .2, s * .24), col, { linea: false }));
}

registrarObjeto('perro', t => {                          // perrito sentado de frente, mueve la cola
  const mov = Math.sin(t * 9) * .35;
  _g.save(); _g.translate(26, -24); _g.rotate(-.6 + mov);
  F(pSuave([[0, 0], [10, -14], [16, -32], [8, -36], [2, -18]], true, .8), CANELA, { sombra: 'abajo:-20' });
  _g.restore();
  F(pSuave([[-34, -2], [-38, -30], [-24, -58], [0, -64], [24, -58], [38, -30], [34, -2]], true, .8), CANELA, { sombra: 14, k: .86 });   // cuerpo
  F(pSuave([[-14, -4], [-16, -30], [0, -46], [16, -30], [14, -4]], true, .8), CANELA_C, { linea: false });                          // pancita
  [-13, 13].forEach(x => F(pRR(x - 8, -30, 16, 30, 8), CANELA, { sombra: x + 4 }));                                               // patitas
  [-13, 13].forEach(x => [-4, 0, 4].forEach(d => L(pLinea([[x + d, -6], [x + d, -2]]), CAFE, .35)));
  F(pRR(-20, -64, 40, 9, 4), ROJO); F(pEl(0, -52, 6, 6), ORO, { brillo: [-3, -55, 2, 3] });                                        // collar y placa
  F(pEl(0, -80, 30, 27), CANELA, { sombra: 12, k: .9 });                                                                            // cabeza
  [-1, 1].forEach(s => { _g.save(); _g.translate(s * 27, -86); _g.rotate(s * .35);
    F(pSuave([[0, -10], [s * 12, -2], [s * 10, 22], [0, 26], [-s * 4, 6]], true, .8), CAFE, { sombra: s > 0 ? 0 : 99 }); _g.restore(); });   // las caídas
  F(pEl(0, -70, 16, 12), CANELA_C);                                                                                                 // hocico
  F(pEl(0, -76, 6, 4.5), TINTA_C, { linea: false }); F(pEl(-2, -77.5, 2, 1.2), '#ffffff', { linea: false });                        // trufa
  L(pSuave([[-6, -66], [0, -64], [6, -66]], false), TINTA_C, .5);
  F(pSuave([[-4, -64], [4, -64], [3, -57], [-3, -57]], true, .7), ROSA, { linea: false });                                          // lengüita
  ojito(-11, -88); ojito(11, -88);
  F(pEl(-22, -72, 5, 3), '#ffb3a7', { linea: false }); F(pEl(22, -72, 5, 3), '#ffb3a7', { linea: false });
}, { ancho: 40, anima: true });

registrarObjeto('gato', t => {                           // gatito sentado, la cola se enrosca adelante
  const punta = Math.sin(t * 3) * 3;
  F(pSuave([[-30, -2], [-36, -28], [-24, -56], [0, -62], [24, -56], [36, -28], [30, -2]], true, .8), GRIS, { sombra: 12, k: .86 });
  F(pSuave([[-12, -6], [-14, -34], [0, -46], [14, -34], [12, -6]], true, .8), BLANCO, { linea: false });                          // pechito blanco
  [[-26, -40], [26, -40], [-30, -24], [30, -24]].forEach(([x, y]) => L(pLinea([[x, y], [x * .8, y + 4]]), GRIS_F, .6));          // rayitas
  [-11, 11].forEach(x => F(pRR(x - 7, -24, 14, 24, 7), BLANCO, { sombra: x + 3 }));
  L(pSuave([[28, -6], [46, -10], [44 + punta, -30], [34, -34]], false, .8), GRIS, 2.4);                                            // cola
  L(pSuave([[28, -6], [46, -10], [44 + punta, -30], [34, -34]], false, .8), GRIS_F, .5);
  [-1, 1].forEach(s => { F(pPoli([[s * 12, -98], [s * 28, -110], [s * 30, -86]]), GRIS, { sombra: s > 0 ? 20 : 99 });
    F(pPoli([[s * 16, -96], [s * 26, -104], [s * 27, -90]]), ROSA, { linea: false }); });                                           // las puntiagudas
  F(pEl(0, -78, 30, 25), GRIS, { sombra: 12, k: .9 });                                                                              // cabeza
  [[-8, -100], [0, -102], [8, -100]].forEach(([x, y]) => L(pLinea([[x, y + 4], [x, y + 10]]), GRIS_F, .6));
  F(pEl(0, -70, 12, 8), BLANCO, { linea: false });
  F(pPoli([[-4, -74], [4, -74], [0, -70]]), ROSA, { linea: false });                                                                // trufa
  L(pSuave([[-6, -66], [0, -68], [6, -66]], false), TINTA_C, .5);
  [-1, 1].forEach(s => [[-2, .6], [2, .5]].forEach(([dy, w]) => L(pLinea([[s * 12, -70 + dy], [s * 32, -72 + dy * 3]]), TINTA_C, .3)));  // bigotes
  ojito(-11, -82, 5); ojito(11, -82, 5);
  F(pRR(-18, -58, 36, 7, 3), MENTA);                                                                                                // collarcito
}, { ancho: 40, anima: true });

registrarObjeto('hueso', () => {
  _g.save(); _g.translate(0, -40); _g.rotate(-.35);
  F(pRR(-40, -10, 80, 20, 6), '#f4ead6', { linea: false });
  [[-40, -10], [-40, 10], [40, -10], [40, 10]].forEach(([x, y]) => F(pEl(x, y, 14, 14), '#f4ead6', { linea: false }));
  if (_modo === 'vector') { _g.lineWidth = _lw; _g.strokeStyle = _tinta;
    [[-40, -10, Math.PI * .45, Math.PI * 1.85], [-40, 10, Math.PI * .15, Math.PI * 1.55], [40, -10, -Math.PI * .85, Math.PI * .55], [40, 10, -Math.PI * .55, Math.PI * .85]].forEach(([x, y, a0, a1]) => { const p = new Path2D(); p.arc(x, y, 14, a0, a1); _g.stroke(p); });
    L(pLinea([[-30, -16], [30, -16]]), null, 1); L(pLinea([[-30, 16], [30, 16]]), null, 1); }
  F(pRR(-26, 2, 52, 8, 4), '#e2d3b6', { linea: false });
  _g.restore();
}, { ancho: 56 });

registrarObjeto('plato-croquetas', () => {
  F(pSuave([[-50, -30], [50, -30], [40, -2], [-40, -2]], true, .4), ROJO, { sombra: 22 });
  F(pEl(0, -30, 50, 10), oscuro(ROJO, .8));
  for (let i = 0; i < 22; i++) { const x = (hash2(i, 4) - .5) * 80, y = -34 - hash2(i, 8) * 14 * (1 - Math.abs(x) / 50);
    F(pEl(x, y, 6, 4.5, hash2(i, 2) * 3), i % 3 ? '#b8743a' : '#9a5c2a', { linea: _modo === 'vector', grosor: .35 }); }
  huella(0, -16, 10, '#ffffff');
}, { ancho: 52 });

registrarObjeto('bebedero', t => {                       // «lleva doce horas sin beber»: plato con agua
  F(pSuave([[-50, -30], [50, -30], [40, -2], [-40, -2]], true, .4), AZUL, { sombra: 22 });
  F(pEl(0, -30, 50, 10), '#bfe4f7');
  const r = (t * .8) % 1;
  if (_modo === 'vector') L(pEl(6, -31, 10 + r * 30, 2 + r * 6), 'rgba(255,255,255,.9)', .5);
  F(pEl(-18, -32, 8, 2.5), '#ffffff', { linea: false });
  L(pLinea([[-24, -16], [24, -16]]), '#4d98c9', .5);
}, { ancho: 52, anima: true });

registrarObjeto('collar-placa', () => {
  const aro = pEl(0, -58, 40, 26);
  _g.save(); if (_modo === 'vector') { _g.strokeStyle = _tinta; _g.lineWidth = 12 + _lw * 2; _g.stroke(aro); }
  _g.strokeStyle = _reg(ROJO); _g.lineWidth = _modo === 'pixel' ? 9 : 12; _g.stroke(aro); _g.restore();
  F(pRR(-8, -40, 16, 10, 3), '#c3c8d2');                                                                                         // hebilla
  L(pLinea([[0, -30], [0, -24]]), '#c3c8d2', .7);
  F(pEl(0, -12, 13, 13), ORO, { brillo: [-8, -20, 4, 6] });
  huella(0, -12, 7, oscuro(ORO, .7));
}, { ancho: 42 });

registrarObjeto('estetoscopio', () => {
  L(pSuave([[-22, -96], [-26, -70], [-10, -48], [0, -46]], false, .8), '#3c4452', 1.8);                                        // tubos
  L(pSuave([[22, -96], [26, -70], [10, -48], [0, -46]], false, .8), '#3c4452', 1.8);
  L(pSuave([[0, -46], [0, -30], [18, -18], [36, -24]], false, .8), '#3c4452', 1.8);
  F(pEl(-22, -98, 5, 5), '#c3c8d2'); F(pEl(22, -98, 5, 5), '#c3c8d2');                                                           // olivas
  F(pEl(40, -26, 18, 18), '#c3c8d2', { sombra: 46 }); F(pEl(40, -26, 11, 11), MENTA, { linea: false });                          // campana
  F(pEl(36, -30, 3, 3), '#ffffff', { linea: false });
}, { ancho: 44 });

registrarObjeto('jeringa', () => {                       // jeringa de plástico con tapita: la aguja no se ve
  _g.save(); _g.translate(0, -44); _g.rotate(-.5);
  F(pRR(-40, -4, 20, 8, 3), '#dde1e7');                                                                                          // vástago
  F(pRR(-50, -16, 10, 32, 4), '#c3c8d2', { sombra: 'abajo:4' });                                                                // tope del émbolo
  F(pRR(-24, -12, 56, 24, 5), '#eef7fb', { sombra: 'abajo:4', k: .93 });
  F(pRR(-20, -9, 30, 18, 3), '#9fd9ee', { linea: false });
  for (let x = -16; x < 28; x += 8) L(pLinea([[x, -12], [x, -6]]), '#7a8699', .4);
  F(pRR(-28, -18, 6, 36, 3), '#dde1e7');
  F(pRR(32, -5, 10, 10, 2), '#dde1e7'); F(pRR(40, -6, 20, 12, 5), MENTA);                                                       // tapita
  _g.restore();
}, { ancho: 48 });

registrarObjeto('transportadora', () => {
  F(pRR(-54, -74, 108, 72, 12), '#f2f2ee', { sombra: 26 });
  F(pRR(-54, -46, 108, 8, 0), '#dcdcd6', { linea: false });
  F(pRR(-38, -66, 52, 52, 8), '#5a6272');                                                                                         // puerta con rejita
  for (let x = -30; x <= 6; x += 9) L(pLinea([[x, -62], [x, -18]]), '#c3c8d2', .8);
  F(pEl(-12, -30, 12, 9), GRIS, { linea: false }); ojito(-16, -36, 3); ojito(-8, -36, 3);                                          // alguien se asoma
  [26, 38].forEach(x => [-60, -48, -36].forEach(y => F(pRR(x, y, 8, 6, 2), '#dcdcd6', { linea: false })));                        // ventilas
  F(pSuave([[-26, -74], [-20, -92], [20, -92], [26, -74], [18, -74], [14, -84], [-14, -84], [-18, -74]], true, .4), MENTA, { sombra: 10 });   // asa
}, { ancho: 56 });

registrarObjeto('casita', () => {
  F(pRR(-46, -58, 92, 56, 4), '#e8a15c', { sombra: 20 });
  for (let y = -48; y < -4; y += 12) L(pLinea([[-46, y], [46, y]]), '#c9853f', .45);
  F(pPoli([[-58, -54], [0, -100], [58, -54], [50, -46], [0, -86], [-50, -46]]), ROJO, { sombra: 0 });
  F(pSuave([[-20, -2], [-20, -30], [0, -44], [20, -30], [20, -2]], true, .6), '#4a3a36');                                          // puerta
  F(pRR(-14, -70, 28, 12, 3), BLANCO); huella(0, -64, 4, CAFE);                                                                   // letrerito
  F(pEl(38, -4, 12, 5), '#f4ead6', { linea: false });
}, { ancho: 58 });

registrarObjeto('pelota', () => {
  F(pEl(0, -34, 32, 32), '#d7ea5a', { sombra: 12, brillo: [-22, -58, 10, 14] });
  L(pSuave([[-30, -48], [-10, -40], [-4, -20], [-14, -4]], false, .8), '#ffffff', 1.2);
  L(pSuave([[30, -22], [10, -30], [4, -50], [14, -64]], false, .8), '#ffffff', 1.2);
}, { ancho: 34 });

registrarObjeto('frasco-medicina', () => {
  F(pRR(-26, -86, 52, 16, 5), '#ffffff', { sombra: 10 });
  for (let x = -20; x <= 20; x += 6) L(pLinea([[x, -84], [x, -72]]), '#d9dde4', .35);
  F(pRR(-24, -72, 48, 70, 8), '#f0a24a', { sombra: 8, brillo: [-19, -66, 6, 54] });
  F(pRR(-24, -54, 48, 32, 0), BLANCO, { linea: false }); if (_modo === 'vector') L(pRR(-24, -72, 48, 70, 8), null, 1);
  huella(0, -38, 8, MENTA);
  F(pRR(30, -10, 16, 8, 4), BLANCO); F(pRR(34, -18, 8, 8, 4), '#9fd9ee');                                                       // pastillitas
}, { ancho: 36 });

registrarEscenario('veterinaria', p => {
  const g = _g;
  g.fillStyle = _reg(p.pared); g.fillRect(0, 0, W, PISO_Y);
  g.fillStyle = _reg(claro(p.acento2, .55)); g.fillRect(0, PISO_Y - 360, W, 360);                                            // media pared de azulejo
  g.fillStyle = _reg(claro(p.acento2, .4)); for (let x = 0; x < W; x += 90) g.fillRect(x, PISO_Y - 360, 3, 360);
  for (let y = PISO_Y - 270; y < PISO_Y; y += 90) g.fillRect(0, y, W, 3);
  g.fillStyle = _reg(p.acento2); g.fillRect(0, PISO_Y - 372, W, 14);
  // huellitas que suben por la pared (decoración)
  [[90, 760], [190, 680], [110, 590], [210, 510], [960, 690], [860, 610]].forEach(([x, y], i) => huella(x, y, 34, claro(p.acento, .5)));
  // repisa izquierda con frascos de premios
  F(pRR(30, 900, 250, 16, 6), '#c9a57a');
  [[70, 70, '#f4ead6'], [140, 90, claro(p.acento, .5)], [215, 60, claro(p.acento2, .3)]].forEach(([x, h, c]) => {
    F(pRR(x - 26, 900 - h, 52, h, 10), '#e8f4f8', { sombra: x + 12 }); F(pRR(x - 20, 900 - h + 20, 40, h - 26, 6), c, { linea: false });
    F(pRR(x - 22, 900 - h - 12, 44, 14, 4), p.acento); });
  // cartel con huella y corazón a la derecha
  F(pRR(780, 760, 250, 280, 12), BLANCO, { sombra: 1010 });
  F(pCorazon(905, 860, 60), claro(p.acento, .2), { linea: false });
  huella(905, 880, 34, '#ffffff');
  F(pRR(820, 980, 170, 14, 7), p.acento2, { linea: false }); F(pRR(850, 1006, 110, 12, 6), claro(p.acento2, .4), { linea: false });
  // piso de loseta
  for (let y = PISO_Y, i = 0; y < H; y += 100, i++) for (let x = 0, j = 0; x < W; x += 120, j++) { g.fillStyle = _reg((i + j) % 2 ? p.piso : claro(p.piso, .45)); g.fillRect(x, y, 120, 100); }
  g.fillStyle = _reg(oscuro(p.piso, .85)); g.fillRect(0, PISO_Y, W, 14);
});

registrarKit('veterinaria', {
  nombre: 'Veterinaria',
  paleta: { fondo: '#eaf5fa', pared: '#e2f0f7', piso: '#bfe3d4', acento: '#ff8a5b', acento2: '#5bb5a2', tinta: '#23303a' },
  escenario: 'veterinaria',
  objetos: ['perro', 'gato', 'transportadora', 'plato-croquetas', 'hueso', 'pelota', 'casita', 'bebedero', 'collar-placa', 'estetoscopio', 'jeringa', 'frasco-medicina'],
});
registrarKit('clinica-veterinaria', KITS.veterinaria);
})();
