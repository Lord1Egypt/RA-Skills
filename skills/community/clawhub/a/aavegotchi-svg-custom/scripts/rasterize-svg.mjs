import fs from 'node:fs';
import { Resvg } from '@resvg/resvg-js';

const [svgPath, pngPath, sizeRaw] = process.argv.slice(2);

if (!svgPath || !pngPath) {
  console.error('Usage: node scripts/rasterize-svg.mjs <svg-path> <png-path> [size]');
  process.exit(1);
}

const size = Number(sizeRaw || 512);
const svg = fs.readFileSync(svgPath, 'utf8');
const resvg = new Resvg(svg, {
  fitTo: { mode: 'width', value: size },
  background: 'rgba(0,0,0,0)',
});
const png = resvg.render().asPng();
fs.writeFileSync(pngPath, png);
