/**
 * 验证「每个分页点各开一页」（用户原则：每次分页都从新的一页开始）：
 *  场景：brake-system 树设两个分页点 —— 制动回路失效（DFS 靠前）、踏板行程传递失效
 *  期望：
 *    P1 = 顶事件页（两个分页点都虚线保留，分别标注 → 第 2 页 / → 第 3 页）
 *    P2 = 制动回路失效子树，承接第 1 页
 *    P3 = 踏板行程传递失效子树，承接第 1 页
 *  同时回归单分页点场景（制动回路失效 → P2）。
 */
import fs from 'node:fs';
import { parseDSL } from '../src/model.mjs';
import { paginateBanded, buildBandedView } from '../src/paginate.mjs';
import { renderA4HTML } from '../src/svg.mjs';

const base = parseDSL(fs.readFileSync('examples/brake-system.fta', 'utf8'));
const kidsOf = new Map();
for (const c of base.connections) {
  if (!kidsOf.has(c.from)) kidsOf.set(c.from, []);
  kidsOf.get(c.from).push(c.to);
}
const nm = (id) => base.nodes.find((n) => n.id === id)?.name || id;
const findByName = (tree, s) =>
  tree.nodes.find((n) => n.name.includes(s) && tree.connections.some((c) => c.from === n.id));

let fail = 0;
const check = (name, ok, extra = '') => {
  console.log(`${ok ? '✓' : '✗'} ${name}${extra ? '  ' + extra : ''}`);
  if (!ok) fail++;
};

// ---- 场景一：两个分页点 ----
{
  const tree = parseDSL(fs.readFileSync('examples/brake-system.fta', 'utf8'));
  findByName(tree, '制动回路失效').pageBreak = true;
  findByName(tree, '踏板行程传递失效').pageBreak = true;
  const pag = paginateBanded(tree, { budget: 14 });
  console.log('\n[两个分页点] 页数:', pag.pages.length);
  check('共 3 页', pag.pages.length === 3, pag.pages.map((p) => p.tops.map(nm).join('/')).join(' | '));

  const [p1, p2, p3] = pag.pages;
  check('P1 顶事件 = 顶事件', p1.tops.length === 1 && nm(p1.tops[0]).includes('制动系统无法建立'));
  check('P1 含 2 个分页点', p1.breakNodes.length === 2,
    p1.breakNodes.map(nm).join(','));
  check('P2 顶 = 制动回路失效', p2.tops.length === 1 && nm(p2.tops[0]) === '制动回路失效',
    p2.tops.map(nm).join(','));
  check('P3 顶 = 踏板行程传递失效', p3.tops.length === 1 && nm(p3.tops[0]) === '踏板行程传递失效',
    p3.tops.map(nm).join(','));
  check('P2 承接第 1 页', p2.continuedFrom === 1);
  check('P3 承接第 1 页', p3.continuedFrom === 1);

  // pageOf：分页点应归属它展开的那一页
  const pageOf = {};
  for (const pg of pag.pages) for (const id of pg.nodes) pageOf[id] = pg.index;
  const loopBreak = findByName(tree, '制动回路失效').id;
  const pedalBreak = findByName(tree, '踏板行程传递失效').id;
  check('制动回路失效归第 2 页', pageOf[loopBreak] === 2);
  check('踏板行程传递失效归第 3 页', pageOf[pedalBreak] === 3);

  // 子树完整：P2 应含轮缸内漏、制动管路破裂；P3 应含踏板自由行程过大、踏板连杆断裂
  const namesOf = (pg) => [...pg.nodes].map(nm).join(' ');
  check('P2 子事件齐全', namesOf(p2).includes('轮缸内漏') && namesOf(p2).includes('制动管路破裂'));
  check('P3 子事件齐全', namesOf(p3).includes('踏板自由行程过大') && namesOf(p3).includes('踏板连杆断裂'));

  // A4 导出标注
  const html = renderA4HTML(tree, { budget: 14, heatmap: {} });
  fs.writeFileSync('D:\\tmp\\a4-two-breaks.html', html);
  const sheets = html.match(/<section class="sheet">[\s\S]*?<\/section>/g) || [];
  check('A4 共 3 页', sheets.length === 3, String(sheets.length));
  if (sheets[0]) {
    check('P1 标注 → 第 2 页', sheets[0].includes('⤓ 分页 → 第 2 页'));
    check('P1 标注 → 第 3 页', sheets[0].includes('⤓ 分页 → 第 3 页'));
  }
  if (sheets[1]) check('P2 标注 ↑ 续自第 1 页', sheets[1].includes('↑ 续自第 1 页'));
  if (sheets[2]) check('P3 标注 ↑ 续自第 1 页', sheets[2].includes('↑ 续自第 1 页'));
}

// ---- 场景二（回归）：单分页点 ----
{
  const tree = parseDSL(fs.readFileSync('examples/brake-system.fta', 'utf8'));
  findByName(tree, '制动回路失效').pageBreak = true;
  const pag = paginateBanded(tree, { budget: 14 });
  console.log('\n[单分页点回归] 页数:', pag.pages.length);
  check('共 2 页', pag.pages.length === 2);
  check('P2 顶 = 制动回路失效', nm(pag.pages[1].tops[0]) === '制动回路失效');
  check('P1 分页点标注指向第 2 页（A4）', renderA4HTML(tree, { budget: 14, heatmap: {} }).includes('⤓ 分页 → 第 2 页'));
}

// ---- 场景三（回归）：无分页点，自动分页不炸 ----
{
  const tree = parseDSL(fs.readFileSync('examples/brake-system.fta', 'utf8'));
  const pag = paginateBanded(tree, { budget: 6 });
  let covered = 0;
  for (const pg of pag.pages) covered += pg.nodes.size;
  console.log('\n[无分页点自动] 页数:', pag.pages.length);
  check('所有节点都被覆盖（分页点节点可能跨页计数）', covered >= tree.nodes.length,
    `covered=${covered} total=${tree.nodes.length}`);
  // 每页的顶事件（除 P1）必须是前面某页出现过的节点 —— 页序连续
  let contiguous = true;
  for (let i = 1; i < pag.pages.length; i++) {
    for (const t of pag.pages[i].tops) {
      if (!pag.pages.some((p) => p.index < i + 1 && p.nodes.has(t))) contiguous = false;
    }
  }
  check('页序连续（下页顶事件在前面某页出现过）', contiguous);
}

console.log(fail ? `\n✗ 失败 ${fail} 项` : '\n✓ 全部通过');
process.exit(fail ? 1 : 0);
