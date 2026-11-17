#!/usr/bin/env node
// armar.mjs — copia un estilo a tu carpeta de trabajo como UN solo archivo (con el núcleo adentro),
// para que funcione con doble clic desde cualquier lugar.
// Uso: node armar.mjs <estilo> <destino.html>      ej. node armar.mjs libreta-a-mano ~/Desktop/animaciones/gancho.html
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const raiz = join(dirname(fileURLToPath(import.meta.url)), '..');
const [estilo, destino] = process.argv.slice(2);
if (!estilo || !destino) { console.error('uso: node armar.mjs <estilo> <destino.html>'); process.exit(1); }
const html = readFileSync(join(raiz, 'estilos', estilo.replace(/\.html$/, '') + '.html'), 'utf8');
// Mete adentro TODO lo que la pieza carga de la skill: ../nucleo/*.js (núcleo, personaje, títere, objetos, kits…)
// y ../vendor/*.js (librerías como three.min.js). Así la pieza funciona sola desde cualquier carpeta.
const marca = /<script src="\.\.\/(nucleo|vendor)\/([\w./-]+\.js)"><\/script>/g;
if (!/<script src="\.\.\/nucleo\/nucleo\.js"><\/script>/.test(html) && !/<script src="\.\.\/nucleo\//.test(html)) { console.error('El estilo no carga ../nucleo/nucleo.js; ¿ya está armado?'); process.exit(1); }
const metidos = [];
const armado = html.replace(marca, (_, dir, arch) => { metidos.push(`${dir}/${arch}`); return '<script>\n' + readFileSync(join(raiz, dir, arch), 'utf8') + '\n</script>'; });
mkdirSync(dirname(resolve(destino)), { recursive: true });
writeFileSync(destino, armado);
console.log('armado -> ' + resolve(destino) + '  (' + metidos.join(', ') + ')');
