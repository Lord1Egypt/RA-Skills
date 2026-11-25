import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const EXAMPLE = path.join(__dirname, '..', 'examples', 'brake-system.fta');

const post = (p, obj) => new Promise((resolve, reject) => {
  const body = typeof obj === 'string' ? obj : JSON.stringify(obj);
  const req = http.request({
    host: '127.0.0.1', port: 8777, path: p, method: 'POST',
    headers: { 'Content-Type': 'application/json', 'Content-Length': Buffer.byteLength(body) },
  }, (res) => {
    let d = '';
    res.on('data', (c) => { d += c; });
    res.on('end', () => {
      try { resolve(JSON.parse(d)); } catch { resolve(d); }
    });
  });
  req.on('error', reject);
  req.end(body);
});

const dsl = fs.readFileSync(EXAMPLE, 'utf8');

// 1) 原始分析
const orig = await post('/api/analyze', { dsl });
// 2) 导出 FaultTree+
const xml = await post('/api/export', { dsl, options: { format: 'faulttreeplus', maxNodes: 14 } });
fs.writeFileSync(path.join(__dirname, '..', 'out', 'brake-faulttreeplus.xml'), String(xml));
// 3) 导入回来
const back = await post('/api/import', { content: String(xml), filename: 'rt.xml' });
// 4) 再导出 CAFTA 并回读
const cafta = await post('/api/export', { dsl, options: { format: 'cafta' } });
const caftaBack = await post('/api/import', { content: String(cafta), filename: 'c.xml' });

console.log('=== 原始 ===');
console.log('  节点', orig.tree ? orig.tree.nodes.length : orig.validation, 'Q=', orig.metrics.topProb.toExponential(4), '割集', orig.cutSets.total);
console.log('=== FaultTree+ 往返 ===');
console.log('  识别格式:', back.format, '校验:', back.ok);
console.log('  节点', back.tree.nodes.length, '连接', back.tree.connections.length);
console.log('  Q=', back.metrics.topProb.toExponential(4), '割集', back.metrics.cutSets.total);
console.log('=== CAFTA 往返 ===');
console.log('  识别格式:', caftaBack.format, '校验:', caftaBack.ok);
console.log('  节点', caftaBack.tree.nodes.length);
console.log('  Q=', caftaBack.metrics?.topProb?.toExponential(4));
console.log('');
const same = Math.abs(orig.metrics.topProb - back.metrics.topProb) < 1e-18;
console.log(same ? '✓ FaultTree+ 往返概率完全一致' : '✗ 概率不一致');
console.log(orig.cutSets.total === back.metrics.cutSets.total ? '✓ 割集完全一致' : '✗ 割集不一致');