import fs from 'node:fs';
import { parseDSL } from '../src/model.mjs';
import { paginateBanded, buildBandedView } from '../src/paginate.mjs';
import { renderSVG, renderA4HTML } from '../src/svg.mjs';

const tree = parseDSL(fs.readFileSync('examples/brake-system.fta', 'utf8'));
const kidsOf = new Map();
for (const c of tree.connections) {
  if (!kidsOf.has(c.from)) kidsOf.set(c.from, []);
  kidsOf.get(c.from).push(c.to);
}
const nm = (id) => tree.nodes.find((n) => n.id === id)?.name || id;

const target = tree.nodes.find((n) => n.name.includes('制动回路失效') && (kidsOf.get(n.id) || []).length);
target.pageBreak = true;
const pag = paginateBanded(tree, { budget: 14 });
console.log('页数:', pag.pages.length, '| 分页点:', nm(target.id));

for (const p of pag.pages) {
  const v = buildBandedView(tree, pag, p.index);
  const svg = renderSVG(v, {
    heatmap: {}, showProb: true,
    markers: [...(v.meta.breakMarkerIds || []), ...(v.meta.contMarkerIds || [])],
  });
  const dashed = (svg.match(/stroke-dasharray="4 3"/g) || []).length;
  console.log(`  P${p.index}: ${v.nodes.length} 节点 | breakMarker=${(v.meta.breakMarkerIds || []).map(nm).join(',') || '-'} | contMarker=${(v.meta.contMarkerIds || []).map(nm).join(',') || '-'} | 虚线框=${dashed}`);
}

const html = renderA4HTML(tree, { budget: 14, heatmap: {} });
fs.writeFileSync('D:\\tmp\\a4-cont-marker.html', html);
const sheets = html.match(/<section class="sheet">[\s\S]*?<\/section>/g) || [];
sheets.forEach((s, i) => {
  const d = (s.match(/stroke-dasharray="4 3"/g) || []).length;
  const hasTarget = s.includes('制动回路失效');
  console.log(`  A4 P${i + 1}: 含分页点文字=${hasTarget} 虚线框=${d}`);
});
