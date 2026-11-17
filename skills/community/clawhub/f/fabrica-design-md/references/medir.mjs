// Mide una página de prueba: desborde móvil, contenido invisible y capturas.
// Uso:  node medir.mjs <ruta/al/index.html> <carpeta-de-salida>
// Requiere Playwright:  npx playwright install chromium
import { chromium } from 'playwright';
import { resolve } from 'path';

const [archivo, salida = '.'] = process.argv.slice(2);
if (!archivo) { console.log('Uso: node medir.mjs <index.html> <carpeta-salida>'); process.exit(1); }
const url = 'file://' + resolve(archivo);

const b = await chromium.launch();
let fallos = 0;

for (const [tag, w, h] of [['escritorio', 1280, 900], ['movil', 390, 844]]) {
  const p = await b.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: 2 });
  await p.goto(url, { waitUntil: 'networkidle', timeout: 20000 });

  // dispara las animaciones de aparición antes de medir, o salen falsos vacíos
  await p.evaluate(async () => {
    await new Promise(r => { let y = 0; const t = setInterval(() => {
      window.scrollBy(0, 400); y += 400;
      if (y >= document.body.scrollHeight + 1000) { clearInterval(t); r(); } }, 30); });
    window.scrollTo(0, 0);
  });
  await p.waitForTimeout(1200);

  const m = await p.evaluate(() => {
    const culpables = [...document.querySelectorAll('*')]
      .filter(e => e.getBoundingClientRect().right > window.innerWidth + 1)
      .slice(0, 4).map(e => (e.tagName + '.' + (e.className || '')).slice(0, 50));
    const invisibles = [...document.querySelectorAll('section,div,p,h1,h2')]
      .filter(e => getComputedStyle(e).opacity === '0').length;
    return { desborde: document.documentElement.scrollWidth > window.innerWidth + 1,
             culpables, invisibles, alto: document.body.scrollHeight };
  });

  await p.screenshot({ path: `${salida}/prueba_${tag}.png`, fullPage: true });

  const marca = m.desborde || m.invisibles > 0 ? 'FALLA' : 'ok   ';
  if (m.desborde || m.invisibles > 0) fallos++;
  console.log(`${marca} ${tag.padEnd(11)} desborde=${m.desborde}  invisibles=${m.invisibles}  alto=${m.alto}px`);
  if (m.culpables.length) console.log(`      desbordan: ${m.culpables.join(' · ')}`);
  await p.close();
}
await b.close();

console.log(fallos === 0
  ? '\nSin fallos medidos. AHORA MIRA LAS CAPTURAS: pasar la medición no prueba que se vea bien.'
  : `\n${fallos} vista(s) con fallo. Arregla antes de entregar.`);
process.exit(fallos ? 1 : 0);
