// KIT PASTELERÍA — se carga después de nucleo/objetos.js
(() => {
const CREMA = '#fff4e2', ROSA = '#ff9fb8', ROSA_F = '#f06a8f', CAFE = '#a8683c', FRESA = '#ff4d5e', HOJA = '#56b870', METAL = '#c3c8d2';

function goteo(y, x0, x1, col, n = 6, largo = 9) {    // glaseado que escurre: banda arriba y gotas redondas de largo desigual
  const p = new Path2D(), r = Math.min(4.2, (x1 - x0) / n / 3.2);
  p.moveTo(x0 - 1, y - 4); p.lineTo(x1 + 1, y - 4); p.lineTo(x1 + 1, y + 3);
  for (let i = n - 1; i >= 0; i--) {
    const cx = x0 + (x1 - x0) * (i + .5) / n, l = 3 + largo * (.35 + .65 * hash2(i, n + x0));
    p.lineTo(cx + r, y + 3); p.lineTo(cx + r, y + l); p.arc(cx, y + l, r, 0, Math.PI); p.lineTo(cx - r, y + 3);
  }
  p.lineTo(x0 - 1, y + 3); p.closePath();
  F(p, col, { sombra: x1 - (x1 - x0) * .22 });
}

registrarObjeto('pastel-pisos', t => {
  F(pEl(0, -3, 50, 6), '#ffffff');                                                   // base
  F(pRR(-44, -40, 88, 36, 6), CREMA, { sombra: 22 }); goteo(-40, -44, 44, ROSA, 8, 10);
  F(pRR(-32, -68, 64, 30, 6), CREMA, { sombra: 16 }); goteo(-68, -32, 32, ROSA, 6, 9);
  F(pRR(-20, -90, 40, 24, 6), CREMA, { sombra: 10 }); goteo(-90, -20, 20, ROSA, 4, 8);
  [-30, -10, 10, 30].forEach(x => F(pEl(x, -20, 4, 4), ROSA_F, { linea: false }));
  F(pEl(0, -95, 8, 8), FRESA, { brillo: [-5, -101, 4, 5] });
  L(pSuave([[0, -103], [3, -108], [8, -110]], false), HOJA, .6);
}, { ancho: 50 });

registrarObjeto('cupcake', () => {
  F(pPoli([[-30, -40], [30, -40], [22, -2], [-22, -2]]), '#8fd3c8', { sombra: 12 });
  [-18, -6, 6, 18].forEach(x => L(pLinea([[x, -38], [x * .75, -4]]), '#5fae9f', .5));
  F(pSuave([[-36, -40], [-30, -56], [-14, -60], [0, -66], [14, -60], [30, -56], [36, -40]]), ROSA, { sombra: 14 });
  F(pSuave([[-24, -58], [-16, -72], [0, -76], [16, -72], [24, -58]]), '#ffb5c8', { sombra: 10 });
  F(pSuave([[-12, -74], [-6, -86], [6, -86], [12, -74]]), '#ffc9d6', { sombra: 4 });
  F(pEl(2, -92, 8, 8), FRESA, { brillo: [-2, -98, 4, 5] });
  [[-20, -52, '#ffd23f'], [16, -50, '#7bc6ff'], [-4, -64, '#ffffff'], [12, -68, '#ffd23f']].forEach(([x, y, c]) => F(pRR(x, y, 6, 3, 1.5), c, { linea: false }));
}, { ancho: 36 });

registrarObjeto('rebanada', () => {
  const lado = pPoli([[-46, -44], [30, -58], [30, -6], [-46, 6]]);                    // cara de enfrente con capas
  F(lado, '#f5d6a8');
  _g.save(); _g.clip(lado);
  [[-26, '#ffffff'], [-40, '#ff9fb8']].forEach(([y, c]) => F(pPoli([[-50, y + 16], [34, y + 4], [34, y + 12], [-50, y + 24]]), c, { linea: false }));
  _g.restore(); if (_modo === 'vector') L(lado, null, 1);
  F(pPoli([[30, -58], [52, -48], [52, -2], [30, -6]]), '#e8bf85');                    // costado
  F(pSuave([[-48, -44], [-10, -52], [30, -60], [52, -50], [30, -46], [-10, -40]], true, .6), CREMA, { sombra: 34 });
  F(pSuave([[8, -62], [16, -74], [24, -64], [16, -56]]), FRESA, { brillo: [11, -70, 4, 5] });
  F(pEstrella(16, -74, 6, 3, 5), HOJA, { linea: false });
}, { ancho: 50 });

registrarObjeto('batidor', () => {
  _g.save(); _g.rotate(.18);
  for (const [rx, c] of [[24, '#9aa2ae'], [16, '#b7bdc7'], [8, '#d0d5dd']]) L(pSuave([[0, -40], [-rx, -62], [-rx * .8, -90], [0, -100], [rx * .8, -90], [rx, -62], [0, -40]], true, .8), c, 1);
  F(pRR(-7, -44, 14, 10, 3), METAL);
  F(pRR(-8, -36, 16, 36, 7), '#f08a4b', { sombra: 2, brillo: [-5, -32, 4, 24] });
  F(pEl(0, -4, 5, 3), '#c96a33', { linea: false });
  _g.restore();
}, { ancho: 28 });

registrarObjeto('duya', () => {                        // bolsa para decorar con su boquilla
  _g.save(); _g.translate(0, -50); _g.rotate(-.5);
  F(pSuave([[-30, -46], [30, -46], [34, -40], [8, 30], [-8, 30], [-34, -40]], true, .5), '#e9f4ff', { sombra: 8 });
  F(pRR(-32, -52, 64, 12, 6), '#bcd9f2');
  L(pLinea([[-14, -30], [-4, 16]]), '#bcd9f2', .6);
  F(pPoli([[-9, 28], [9, 28], [5, 44], [-5, 44]]), METAL, { sombra: 2 });
  [-5, 0, 5].forEach(x => L(pLinea([[x * .8, 30], [x * .6, 43]]), '#8a909c', .35));
  _g.restore();
  F(pSuave([[14, -2], [16, -12], [26, -14], [30, -6], [36, -2]], true, .8), ROSA, { sombra: 28 });
}, { ancho: 36 });

registrarObjeto('horno', t => {
  F(pRR(-50, -100, 100, 98, 8), '#f1f3f6', { sombra: 30 });
  F(pRR(-50, -100, 100, 22, 8), '#d9dde4');
  [-34, -18, 18, 34].forEach(x => F(pEl(x, -89, 6, 6), '#555a66'));
  F(pEl(0, -89, 10, 5), '#2d2a3a', { linea: false });
  F(pRR(-40, -70, 80, 58, 6), '#2d2a3a');
  const brillo = .75 + .25 * Math.sin(t * 6);
  F(pRR(-34, -64, 68, 46, 4), _modo === 'pixel' ? '#ff9d3c' : `rgba(255,${Math.round(150 + 30 * brillo)},60,1)`, { linea: false });
  F(pRR(-18, -38, 36, 16, 4), '#c98a4a', { linea: false }); goteo(-38, -18, 18, CREMA, 4, 5);
  F(pRR(-30, -80, 60, 6, 3), '#9aa2ae');
  F(pRR(-44, -8, 12, 8, 2), '#555a66'); F(pRR(32, -8, 12, 8, 2), '#555a66');
}, { ancho: 52, anima: true });

registrarObjeto('caja-pastel', () => {
  F(pRR(-44, -66, 88, 64, 5), '#ffe3ec', { sombra: 16 });
  F(pPoli([[-48, -66], [48, -66], [44, -80], [-44, -80]]), '#ffd0de', { sombra: 16 });
  F(pRR(-6, -80, 12, 78, 1), ROSA_F, { linea: false }); L(pRR(-6, -80, 12, 78, 1), null, .5);
  F(pRR(-44, -40, 88, 10, 1), ROSA_F, { linea: false }); L(pRR(-44, -40, 88, 10, 1), null, .5);
  F(pRR(-38, -32, 26, 24, 4), '#dff3fb'); F(pRR(-33, -20, 16, 10, 2), ROSA, { linea: false }); F(pEl(-25, -22, 3, 3), FRESA, { linea: false });   // ventanita: se ve el pastel
  F(pEl(-15, -88, 16, 10, -.4), ROSA_F); F(pEl(15, -88, 16, 10, .4), ROSA_F); F(pEl(0, -86, 7, 7), '#d44f74');
}, { ancho: 48 });

registrarObjeto('vela', t => {
  const cuerpo = pRR(-9, -64, 18, 62, 4);
  F(cuerpo, '#8fd3ff'); _g.save(); _g.clip(cuerpo);
  for (let y = -80; y < 10; y += 16) F(pPoli([[-12, y], [12, y - 10], [12, y - 4], [-12, y + 6]]), '#ffffff', { linea: false });
  _g.restore(); if (_modo === 'vector') L(cuerpo, null, 1);
  L(pLinea([[0, -64], [0, -72]]), TINTA_OBJ, .6);
  const f = 1 + .12 * Math.sin(t * 17) + .06 * Math.sin(t * 29), inc = Math.sin(t * 11) * 2;
  F(pSuave([[0, -72], [7 * f, -80], [inc, -100 * (.93 + .07 * f)], [-7 * f, -80]], true, .9), '#ffb020', { linea: false });
  F(pSuave([[0, -73], [3.5, -79], [inc * .5, -89], [-3.5, -79]], true, .9), '#fff1a8', { linea: false });
}, { ancho: 16, anima: true });

registrarObjeto('cuchara-madera', () => {
  _g.save(); _g.rotate(-.3);
  F(pRR(-5, -66, 10, 66, 5), '#d49a5f', { sombra: 1 });
  F(pEl(0, -80, 15, 21), '#d49a5f', { sombra: 4 });
  F(pEl(0, -82, 9, 14), '#b97e45', { linea: false });
  L(pLinea([[-1, -56], [-1, -10]]), '#b97e45', .4);
  _g.restore();
}, { ancho: 22 });

registrarObjeto('harina', () => {
  F(pSuave([[-38, -2], [-42, -50], [-30, -78], [-16, -84], [16, -84], [30, -78], [42, -50], [38, -2]], true, .8), '#f3ead8', { sombra: 16 });
  F(pSuave([[-16, -84], [-22, -96], [0, -90], [22, -96], [16, -84]], true, .8), '#e8dcc3');
  L(pLinea([[-18, -84], [18, -84]]), '#a8683c', 1);
  F(pRR(-26, -62, 52, 36, 6), '#ffffff'); T('HARINA', 0, -52, 10, CAFE);
  L(pLinea([[0, -32], [0, -46]]), '#e0a93c', .7);
  [-1, 1].forEach(s => [0, 1, 2].forEach(i => F(pEl(s * 4, -44 + i * 4, 3, 2, s * .6), '#e0a93c', { linea: false })));
  F(pEl(40, -8, 10, 5), '#ffffff', { linea: false }); F(pEl(-44, -4, 7, 4), '#ffffff', { linea: false });
}, { ancho: 44 });

registrarObjeto('huevo', () => {
  const cas = pSuave([[0, -84], [22, -66], [30, -34], [20, -6], [0, 0], [-20, -6], [-30, -34], [-22, -66]], true, 1);
  F(cas, '#f7e3c6', { sombra: 6, k: .88, brillo: [-20, -68, 10, 26], brilloCol: '#ffffff' });   // cáscara color crema, brillo marcado
  _g.save(); _g.clip(cas); [[10, -40], [16, -22], [-8, -18], [4, -60]].forEach(([x, y]) => { _g.fillStyle = _reg('#e2c49c'); _g.beginPath(); _g.arc(x, y, 1.8, 0, 7); _g.fill(); }); _g.restore();
}, { ancho: 30 });

registrarObjeto('fresa', () => {
  const cuerpo = pSuave([[0, -2], [-24, -30], [-30, -56], [-16, -70], [0, -66], [16, -70], [30, -56], [24, -30]], true, .9);
  F(cuerpo, FRESA, { sombra: 8, brillo: [-20, -58, 7, 14] });
  for (let i = 0; i < 12; i++) { const x = (hash2(i, 3) - .5) * 36, y = -14 - hash2(i, 7) * 46; if (Math.abs(x) < 26 - (y + 70) * .02 * 6) F(pEl(x, y, 1.8, 2.8), '#ffe27a', { linea: false }); }
  F(pEstrella(0, -70, 18, 8, 5, -Math.PI / 2), HOJA, { sombra: 4 });
  F(pRR(-2, -84, 4, 10, 2), '#3f8f55');
}, { ancho: 30 });

registrarObjeto('bascula', () => {
  F(pSuave([[-38, -58], [38, -58], [30, -72], [-30, -72]], true, .4), METAL, { sombra: 14 });
  F(pRR(-4, -58, 8, 8, 2), '#9aa2ae');
  F(pPoli([[-40, -50], [40, -50], [46, -2], [-46, -2]]), '#ff9fb8', { sombra: 22 });
  F(pEl(0, -28, 18, 18), '#ffffff');
  L(pEl(0, -28, 13, 13, 0, Math.PI, Math.PI * 2, false), '#c3c8d2', .5);
  L(pLinea([[0, -28], [9, -38]]), FRESA, .8);
}, { ancho: 46 });

registrarObjeto('vitrina', () => {
  F(pRR(-54, -26, 108, 24, 4), CAFE, { sombra: 30 });
  F(pRR(-50, -100, 100, 76, 6), '#dff3fb', { sombra: 30, k: .95 });
  L(pLinea([[-50, -62], [50, -62]]), '#9aa2ae', .8);
  [[-30, -62], [0, -62], [30, -62]].forEach(([x, y], i) => { F(pRR(x - 11, y - 14, 22, 14, 4), [ROSA, CREMA, '#8fd3c8'][i]); F(pEl(x, y - 16, 4, 4), FRESA, { linea: false }); });
  [[-26, -28], [6, -28], [34, -28]].forEach(([x, y], i) => { F(pPoli([[x - 10, y - 16], [x + 10, y - 16], [x + 7, y], [x - 7, y]]), '#8fd3c8'); F(pEl(x, y - 20, 11, 7), [ROSA, '#ffc9d6', CREMA][i]); });
  F(pPoli([[-40, -96], [-28, -96], [-44, -66], [-50, -66]]), '#ffffff', { linea: false });
}, { ancho: 56 });

registrarEscenario('pasteleria', p => {
  const g = _g;
  g.fillStyle = _reg(p.pared); g.fillRect(0, 0, W, H);
  g.fillStyle = _reg(claro(p.pared, .3)); for (let x = 0; x < W; x += 120) g.fillRect(x, 0, 60, PISO_Y);          // rayas del papel tapiz
  // banderines arriba (zona que tapa Instagram: solo decoración)
  // (los banderines van en el «vivo»: se mecen)
  // repisa con frascos a los lados (sin tocar el centro, donde va el texto)
  F(pRR(40, 930, 250, 18, 6), oscuro(p.piso, .75));
  [[80, '#ffffff', 70], [150, claro(p.acento2, .2), 90], [225, claro(p.acento, .3), 60]].forEach(([x, c, h]) => {
    F(pRR(x - 26, 930 - h, 52, h, 10), c, { sombra: x + 10 }); F(pRR(x - 20, 930 - h - 14, 40, 16, 5), oscuro(p.piso, .65)); });
  F(pRR(790, 930, 250, 18, 6), oscuro(p.piso, .75));
  [[840, 1.1], [930, .9], [1000, 1]].forEach(([x, s], i) => { F(pEl(x, 930 - 20 * s, 34 * s, 20 * s, 0, Math.PI, Math.PI * 2), [p.acento, p.acento2, '#ffd23f'][i]); });
  // mostrador
  F(pRR(-20, PISO_Y - 6, W + 40, 146, 10), p.piso, { sombra: 'abajo:' + (PISO_Y + 118) });   // cubierta con fondo: caben 2 filas
  L(pLinea([[0, PISO_Y + 60], [W, PISO_Y + 60]]), oscuro(p.piso, .93), .5);
  g.fillStyle = _reg(claro(p.acento2, .15)); g.fillRect(0, PISO_Y + 140, W, H - PISO_Y);
  g.fillStyle = _reg(p.acento2); for (let x = 0; x < W; x += 90) g.fillRect(x, PISO_Y + 140, 45, H);
  g.fillStyle = _reg(oscuro(p.acento2, .85)); g.fillRect(0, PISO_Y + 140, W, 14);
}, (t, p) => {   // vivo: banderines que se mecen con aire suave
  const cols = [p.acento, p.acento2, '#ffd23f'], cuerda = x => 110 + Math.sin(x / 1080 * Math.PI) * 26 + Math.sin(t * 1.3) * 3;
  L(pSuave([[0, cuerda(0)], [270, cuerda(270)], [540, cuerda(540)], [810, cuerda(810)], [1080, cuerda(1080)]], false), p.tinta, .6);
  for (let i = 0; i < 9; i++) { const x = 20 + i * 125, y = cuerda(x + 45), a = Math.sin(t * 1.7 + i * .8) * .07;
    _g.save(); _g.translate(x + 45, y); _g.rotate(a); F(pPoli([[-45, 0], [45, 0], [0, 88]]), cols[i % 3], { brillo: [-30, 4, 26, 8] }); _g.restore(); }
});

registrarKit('pasteleria', {
  nombre: 'Pastelería',
  paleta: { fondo: '#fde2e4', pared: '#fcd5de', piso: '#fff4e8', acento: '#ff7aa2', acento2: '#9fdcd2', tinta: '#3b2530' },
  escenario: 'pasteleria',
  objetos: ['pastel-pisos', 'cupcake', 'rebanada', 'batidor', 'duya', 'horno', 'caja-pastel', 'vela', 'cuchara-madera', 'harina', 'huevo', 'fresa', 'bascula', 'vitrina'],
});
})();
