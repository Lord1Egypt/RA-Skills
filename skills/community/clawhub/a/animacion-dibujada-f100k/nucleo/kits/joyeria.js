// KIT JOYERÍA — se carga después de nucleo/objetos.js
(() => {
const ORO = '#e0b44c', ORO_F = '#b8862a', PLATA = '#d3d8e0', PLATA_F = '#9aa2ae', GEMA = '#8fd8f0', RUBI = '#e34d6a', ESMERALDA = '#3fbf8f',
      TERCIOPELO = '#5b2a4a', TERCIOPELO_C = '#7a3a63', CREMA = '#fbf5ea';

function piedra(cx, cy, r, col = GEMA) {                    // piedra facetada vista de frente
  F(pPoli([[cx - r, cy - r * .2], [cx - r * .55, cy - r * .75], [cx + r * .55, cy - r * .75], [cx + r, cy - r * .2], [cx, cy + r]]), col, { sombra: cx + r * .1, k: .78 });
  F(pPoli([[cx - r * .55, cy - r * .75], [cx + r * .55, cy - r * .75], [cx + r * .3, cy - r * .2], [cx - r * .3, cy - r * .2]]), claro(col, .45), { linea: false });
  L(pLinea([[cx - r, cy - r * .2], [cx + r, cy - r * .2]]), oscuro(col, .7), .35);
  L(pLinea([[cx - r * .3, cy - r * .2], [cx, cy + r]]), oscuro(col, .7), .3); L(pLinea([[cx + r * .3, cy - r * .2], [cx, cy + r]]), oscuro(col, .7), .3);
}
function destello(cx, cy, s, t = 0) {                        // la estrellita del brillo
  const k = .7 + .3 * Math.sin(t * 6 + cx);
  F(pEstrella(cx, cy, s * k, s * .22 * k, 4, 0), '#ffffff', { linea: false });
}

registrarObjeto('anillo-piedra', t => {                    // anillo con piedra en garras
  const aro = pEl(0, -34, 32, 32);
  _g.save(); _g.lineWidth = 11; _g.strokeStyle = _tinta; if (_modo === 'vector') { _g.lineWidth = 11 + _lw * 2; _g.stroke(aro); }
  _g.strokeStyle = _reg(ORO); _g.lineWidth = _modo === 'pixel' ? 9 : 11; _g.stroke(aro); _g.restore();
  L(pEl(0, -34, 32, 32, 0, Math.PI * 1.05, Math.PI * 1.45, false), '#fff0b8', .6);
  [-12, -4, 4, 12].forEach(x => F(pRR(x - 2, -76, 4, 14, 2), ORO_F, { linea: false }));      // garras
  piedra(0, -82, 20);
  destello(14, -96, 9, t);
}, { ancho: 34, anima: true });

registrarObjeto('argolla', () => {                          // argolla lisa, parada y ladeada
  F(pEl(0, -40, 36, 38), ORO, { sombra: 10, k: .82 });
  F(pEl(4, -40, 24, 28), CREMA, { linea: true });
  L(pEl(-2, -40, 32, 34, 0, Math.PI * 1.1, Math.PI * 1.5, false), '#fff0b8', .8);
}, { ancho: 36 });

registrarObjeto('collar', t => {                            // collar en su exhibidor
  F(pRR(-34, -6, 68, 6, 3), TERCIOPELO, { sombra: 20 });
  F(pSuave([[-6, -6], [-10, -40], [-34, -70], [-30, -96], [0, -104], [30, -96], [34, -70], [10, -40], [6, -6]], true, .6), TERCIOPELO_C, { sombra: 10, brillo: [-26, -96, 6, 24] });
  L(pSuave([[-28, -92], [-22, -64], [0, -50], [22, -64], [28, -92]], false, .9), ORO, 1);
  for (let i = 0; i < 9; i++) { const u = i / 8, x = -26 + u * 52, y = -88 + Math.sin(u * Math.PI) * 36; F(pEl(x, y, 2.5, 2.5), ORO_F, { linea: false }); }
  L(pLinea([[0, -52], [0, -44]]), ORO, .6);
  piedra(0, -36, 9, RUBI);
  destello(8, -44, 6, t);
}, { ancho: 36, anima: true });

registrarObjeto('aretes', () => {                           // par de aretes colgantes en su tarjeta
  F(pRR(-38, -100, 76, 98, 8), CREMA, { sombra: 22 });
  F(pEl(0, -92, 5, 5), '#e8dccb', { linea: false });
  [-16, 16].forEach(x => {
    F(pEl(x, -74, 4, 4), ORO);
    L(pLinea([[x, -70], [x, -58]]), ORO_F, .6);
    F(pSuave([[x, -58], [x + 9, -44], [x, -24], [x - 9, -44]], true, .8), ESMERALDA, { sombra: x + 2, k: .8, brillo: [x - 5, -52, 3, 10] });
  });
}, { ancho: 40 });

registrarObjeto('estuche-anillo', t => {                    // cajita abierta de terciopelo con anillo
  F(pRR(-40, -40, 80, 38, 8), TERCIOPELO, { sombra: 22 });
  F(pSuave([[-40, -40], [-38, -86], [-30, -94], [30, -94], [38, -86], [40, -40]], true, .4), TERCIOPELO_C, { sombra: 22 });   // tapa abierta
  F(pRR(-32, -88, 64, 40, 6), '#f3e6ee', { linea: false });
  F(pRR(-32, -44, 64, 20, 6), '#8e4f78', { linea: false });
  L(pLinea([[0, -44], [0, -26]]), '#5b2a4a', .5);
  L(pEl(0, -46, 12, 12, 0, Math.PI, Math.PI * 2, false), ORO, 1.3);
  piedra(0, -62, 9);
  destello(10, -72, 7, t);
}, { ancho: 42, anima: true });

registrarObjeto('lupa-joyero', () => {                      // lupita de joyero: cilindro negro con lente
  _g.save(); _g.translate(0, -34); _g.rotate(-.35);
  F(pRR(-26, -24, 40, 48, 8), '#2d2a3a', { sombra: 4 });
  F(pRR(-30, -26, 10, 52, 5), '#4a4658');
  F(pEl(18, 0, 12, 26), '#bfe6f2', { sombra: 20 });
  F(pEl(16, -8, 3, 8), '#ffffff', { linea: false });
  _g.restore();
  L(pSuave([[-28, -14], [-44, -8], [-50, -2]], false), '#8a909c', .6);                      // cordón
}, { ancho: 38 });

registrarObjeto('balanza-joyero', () => {                   // báscula de precisión con tapa de vidrio, sin cifras
  F(pRR(-50, -24, 100, 22, 6), '#3a3f4b', { sombra: 30 });
  F(pRR(-38, -20, 40, 12, 3), '#a8e6c4', { linea: false });
  [-24, -14, -4].forEach(x => F(pRR(x, -17, 6, 6, 1), '#2f6b4f', { linea: false }));         // segmentos, no números
  F(pEl(30, -14, 5, 5), ORO); F(pEl(42, -14, 5, 5), PLATA);
  F(pRR(-40, -84, 80, 60, 6), '#e8f6fb', { sombra: 26, k: .95 });                           // tapa de vidrio
  F(pPoli([[-32, -78], [-22, -78], [-34, -40], [-38, -48]]), '#ffffff', { linea: false });
  F(pEl(0, -30, 22, 4), PLATA_F, { linea: false });
  L(pEl(0, -38, 8, 8), ORO, 1);
}, { ancho: 52 });

registrarObjeto('caja-regalo-joya', () => {                // cajita chica con moño
  F(pRR(-34, -52, 68, 50, 5), '#1f5c6b', { sombra: 12 });
  F(pRR(-38, -62, 76, 14, 5), '#2a7486', { sombra: 12 });
  F(pRR(-5, -62, 10, 60, 1), ORO, { linea: false }); L(pRR(-5, -62, 10, 60, 1), null, .45);
  F(pRR(-38, -34, 76, 8, 1), ORO, { linea: false }); L(pRR(-38, -34, 76, 8, 1), null, .45);
  F(pEl(-12, -70, 13, 8, -.4), ORO); F(pEl(12, -70, 13, 8, .4), ORO); F(pEl(0, -66, 6, 6), ORO_F);
}, { ancho: 40 });

registrarObjeto('cadena', t => {                        // cadena de eslabones en S sobre el mostrador, con dije de corazón
  const pts = []; for (let i = 0; i <= 18; i++) { const u = i / 18; pts.push([-50 + u * 92, -12 - Math.sin(u * Math.PI * 1.6) * 26 - u * 30]); }
  pts.forEach(([x, y], i) => { if (i === pts.length - 1) return;
    const [x2, y2] = pts[i + 1], a = Math.atan2(y2 - y, x2 - x), cx = (x + x2) / 2, cy = (y + y2) / 2;
    const eslabon = pEl(cx, cy, 5.6, i % 2 ? 2.2 : 3.6, a);
    if (i % 2) F(eslabon, ORO_F, { linea: _modo === 'vector', grosor: .4 });
    else { _g.save(); _g.lineWidth = _modo === 'pixel' ? 1.6 : 2.6; if (_modo === 'vector') { _g.strokeStyle = _tinta; _g.lineWidth = 2.6 + _lw * .7; _g.stroke(eslabon); _g.lineWidth = 2.6; } _g.strokeStyle = _reg(ORO); _g.stroke(eslabon); _g.restore(); }
  });
  const [ex, ey] = pts[pts.length - 1];
  L(pLinea([[ex, ey], [ex + 2, ey - 8]]), ORO_F, .5);
  F(pCorazon(ex + 4, ey - 22, 13), ORO, { brillo: [ex - 4, ey - 30, 4, 7] });
  destello(ex + 14, ey - 36, 7, t);
}, { ancho: 50, anima: true });

registrarObjeto('diamante', t => {                          // piedra grande suelta
  const R = 48, cy = -50;
  F(pPoli([[-R, cy - 10], [-R * .55, cy - 38], [R * .55, cy - 38], [R, cy - 10], [0, cy + 48]]), GEMA, { sombra: 4, k: .78 });
  F(pPoli([[-R * .55, cy - 38], [R * .55, cy - 38], [R * .3, cy - 10], [-R * .3, cy - 10]]), claro(GEMA, .55), { linea: false });
  F(pPoli([[-R, cy - 10], [-R * .3, cy - 10], [0, cy + 48]]), claro(GEMA, .25), { linea: false });
  L(pLinea([[-R, cy - 10], [R, cy - 10]]), oscuro(GEMA, .7), .45);
  [[-R * .55, -R * .3], [R * .55, R * .3]].forEach(([a, b]) => L(pLinea([[a, cy - 38], [b, cy - 10]]), oscuro(GEMA, .7), .35));
  L(pLinea([[-R * .3, cy - 10], [0, cy + 48]]), oscuro(GEMA, .7), .35); L(pLinea([[R * .3, cy - 10], [0, cy + 48]]), oscuro(GEMA, .7), .35);
  if (_modo === 'vector') L(pPoli([[-R, cy - 10], [-R * .55, cy - 38], [R * .55, cy - 38], [R, cy - 10], [0, cy + 48]]), null, 1);
  destello(-22, -86, 11, t); destello(30, -40, 7, t + 1);
}, { ancho: 46, anima: true });

registrarObjeto('medidor-tallas', () => {                   // mandril de tallas: cono con anillo puesto
  F(pPoli([[-7, -100], [7, -100], [18, -14], [-18, -14]]), PLATA, { sombra: 4, brillo: [-5, -92, 3, 70] });
  for (let y = -90; y < -20; y += 8) L(pLinea([[-8 - (y + 100) * .1, y], [-2 - (y + 100) * .1, y]]), PLATA_F, .35);
  F(pRR(-28, -16, 56, 14, 5), '#3a3f4b', { sombra: 12 });
  F(pEl(0, -56, 16, 5), ORO, { sombra: 6 }); L(pEl(0, -56, 16, 5, 0, Math.PI, Math.PI * 2, false), '#fff0b8', .5);
}, { ancho: 30 });

registrarObjeto('pulsera', () => {                          // pulsera de eslabones, acostada
  const aro = pEl(0, -28, 44, 24);
  _g.save(); _g.lineWidth = 12; if (_modo === 'vector') { _g.strokeStyle = _tinta; _g.lineWidth = 12 + _lw * 2; _g.stroke(aro); }
  _g.strokeStyle = _reg(PLATA); _g.lineWidth = _modo === 'pixel' ? 9 : 12; _g.stroke(aro); _g.restore();
  for (let i = 0; i < 14; i++) { const a = i / 14 * Math.PI * 2; L(pLinea([[Math.cos(a) * 38, -28 + Math.sin(a) * 19], [Math.cos(a) * 50, -28 + Math.sin(a) * 29]]), PLATA_F, .45); }
  piedra(0, -8, 8, RUBI);
}, { ancho: 48 });

registrarEscenario('joyeria', p => {
  const g = _g;
  g.fillStyle = _reg(p.pared); g.fillRect(0, 0, W, PISO_Y);
  g.fillStyle = _reg(claro(p.pared, .22)); for (let x = 0; x < W; x += 270) g.fillRect(x + 22, 0, 226, PISO_Y - 260);   // paneles
  g.fillStyle = _reg(p.acento); g.fillRect(0, PISO_Y - 262, W, 8);                                                     // moldura dorada
  // luces de techo: conos cálidos sobre las vitrinas
  [[160], [920]].forEach(([x]) => {
    F(pRR(x - 34, 0, 68, 26, 6), p.acento);
    if (_modo === 'vector') { const gr = g.createLinearGradient(0, 26, 0, 1080); gr.addColorStop(0, 'rgba(255,236,180,.55)'); gr.addColorStop(1, 'rgba(255,236,180,0)');
      g.fillStyle = gr; g.beginPath(); g.moveTo(x - 28, 26); g.lineTo(x + 28, 26); g.lineTo(x + 170, 1080); g.lineTo(x - 170, 1080); g.closePath(); g.fill(); }
  });
  // vitrinas altas a los lados: marco dorado, fondo de terciopelo y piezas que brillan
  [[20], [800]].forEach(([x]) => {
    const y0 = 660, y1 = 1150, w = 260;
    F(pRR(x, y0, w, y1 - y0, 12), p.acento, { sombra: x + w - 20 });
    F(pRR(x + 14, y0 + 14, w - 28, y1 - y0 - 28, 6), oscuro(p.acento2, .7), { linea: false });
    [y0 + 170, y0 + 330].forEach(yy => F(pRR(x + 14, yy, w - 28, 12, 2), claro(p.acento2, .2), { linea: false }));
    [[x + 70, y0 + 170], [x + 190, y0 + 170], [x + 130, y0 + 330]].forEach(([cx, cy], i) => {
      F(pRR(cx - 26, cy - 50, 52, 50, 8), claro(p.acento2, .15), { linea: false });                                     // cojincito
      L(pEl(cx, cy - 34, 14, 14), i === 1 ? '#d3d8e0' : p.acento, 1.3);
      F(pEstrella(cx + 18, cy - 54, 12, 3, 4, 0), '#ffffff', { linea: false });
    });
    F(pRR(x + 130, y0 + 420, 60, 40, 6), claro(p.acento2, .15), { linea: false }); F(pCorazon(x + 160, y0 + 440, 10), p.acento, { linea: false });
    F(pPoli([[x + 30, y0 + 24], [x + 70, y0 + 24], [x + 30, y0 + 150]]), 'rgba(255,255,255,.35)', { linea: false });
  });
  // mostrador de vidrio al frente: aquí se paran los objetos
  F(pRR(-20, PISO_Y - 6, W + 40, 34, 6), '#e8f6fb', { sombra: 'abajo:' + (PISO_Y + 12), k: .92 });
  g.fillStyle = _reg(p.piso); g.fillRect(0, PISO_Y + 28, W, H - PISO_Y);
  g.fillStyle = _reg(oscuro(p.piso, .85)); g.fillRect(0, PISO_Y + 28, W, 12);
  g.fillStyle = _reg(claro(p.piso, .12)); for (let x = 60; x < W; x += 240) g.fillRect(x, PISO_Y + 40, 8, H);
  g.fillStyle = _reg(p.acento); g.fillRect(0, PISO_Y + 120, W, 8);
});

registrarKit('joyeria', {
  nombre: 'Joyería',
  paleta: { fondo: '#f5ecdf', pared: '#ecdfcc', piso: '#4a3446', acento: '#e0b44c', acento2: '#8e4f78', tinta: '#2b2433' },
  escenario: 'joyeria',
  objetos: ['estuche-anillo', 'anillo-piedra', 'collar', 'aretes', 'diamante', 'argolla', 'medidor-tallas', 'lupa-joyero', 'balanza-joyero', 'cadena', 'pulsera', 'caja-regalo-joya'],
});
})();
