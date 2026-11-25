/**
 * FTA Studio - HTTP 服务
 * 同时提供：静态图形编辑器 + REST API（供 WorkBuddy / 外部程序调用）
 * 零依赖，仅使用 Node.js 内置 http 模块
 */

import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { fta } from './api.mjs';
import { parseDSL, stringifyDSL, validateTree } from './model.mjs';
import { quantify } from './quantify.mjs';
import { renderSVG, renderA4HTML } from './svg.mjs';
import { generateMarkdownReport, generateHTMLReport } from './report.mjs';
import { buildNodeHeatmapForCLI } from './helpers.mjs';
import { paginate, autoPaginate, buildPageView, paginateSummary, paginateBanded } from './paginate.mjs';
import {
  toFaultTreePlusXML, fromFaultTreePlusXML, toCAFTA, fromCAFTA,
  toMediniJSON, importAny, detectFormat,
} from './interchange.mjs';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..');
const PUBLIC = path.join(ROOT, 'public');

const MIME = {
  '.html': 'text/html; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.mjs': 'text/javascript; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.svg': 'image/svg+xml',
  '.png': 'image/png',
  '.ico': 'image/x-icon',
};

function sendJSON(res, code, obj) {
  const body = JSON.stringify(obj, null, 2);
  res.writeHead(code, {
    'Content-Type': 'application/json; charset=utf-8',
    'Content-Length': Buffer.byteLength(body),
    'Access-Control-Allow-Origin': '*',
  });
  res.end(body);
}

function sendText(res, code, text, type = 'text/plain; charset=utf-8') {
  res.writeHead(code, {
    'Content-Type': type,
    'Content-Length': Buffer.byteLength(text),
    'Access-Control-Allow-Origin': '*',
  });
  res.end(text);
}

async function readBody(req) {
  const chunks = [];
  for await (const c of req) chunks.push(c);
  if (!chunks.length) return null;
  const raw = Buffer.concat(chunks).toString('utf8');
  try {
    return JSON.parse(raw);
  } catch {
    return raw; // 纯文本（DSL）
  }
}

function treeFromBody(body) {
  if (typeof body === 'string') return parseDSL(body);
  if (body?.dsl) return parseDSL(body.dsl);
  if (body?.tree) return body.tree;
  if (Array.isArray(body?.nodes)) return body;
  throw new Error('请求体需为 DSL 文本、{dsl}、{tree} 或含 nodes 数组的对象');
}

function handleAPI(req, res, url) {
  const p = url.pathname;

  // POST /api/analyze — 完整分析
  if (p === '/api/analyze' && req.method === 'POST') {
    readBody(req).then((body) => {
      const tree = treeFromBody(body);
      const opts = body && typeof body === 'object' ? (body.options || body.opts || {}) : {};
      const result = fta.analyze(tree, {
        report: opts.report || 'json',
        maxOrder: opts.maxOrder,
        truncation: opts.truncation,
        quantification: opts.quantification,
        includeDiagram: opts.includeDiagram !== false,
        includeSVG: opts.includeSVG,
      });
      if (result.ok === false && result.report) {
        return sendText(res, 200, result.report, 'text/markdown; charset=utf-8');
      }
      if (result.report === 'html') return sendText(res, 200, result.report, 'text/html; charset=utf-8');
      if (result.report === 'markdown') return sendText(res, 200, result.report, 'text/markdown; charset=utf-8');
      sendJSON(res, 200, result);
    }).catch((e) => sendJSON(res, 400, { ok: false, error: e.message }));
    return;
  }

  // POST /api/dsl — DSL 文本 → 完整分析（最常用）
  if (p === '/api/dsl' && req.method === 'POST') {
    readBody(req).then((body) => {
      const tree = treeFromBody(body);
      const opts = body && typeof body === 'object' ? (body.options || {}) : {};
      const result = fta.analyze(tree, { report: opts.report || 'json' });
      sendJSON(res, 200, result);
    }).catch((e) => sendJSON(res, 400, { ok: false, error: e.message }));
    return;
  }

  // POST /api/report — 生成 Markdown/HTML 报告
  if (p === '/api/report' && req.method === 'POST') {
    readBody(req).then((body) => {
      const tree = treeFromBody(body);
      const opts = body && typeof body === 'object' ? (body.options || {}) : {};
      const q = quantify(tree, opts);
      const heatmap = buildNodeHeatmapForCLI(tree, q);
      const fmt = opts.format || 'markdown';
      if (fmt === 'html') {
        sendText(res, 200, generateHTMLReport(tree, q, { heatmap }), 'text/html; charset=utf-8');
      } else {
        sendText(res, 200, generateMarkdownReport(tree, q, { heatmap, embedImage: opts.embedImage !== false }), 'text/markdown; charset=utf-8');
      }
    }).catch((e) => sendJSON(res, 400, { ok: false, error: e.message }));
    return;
  }

  // POST /api/svg — 返回 SVG
  if (p === '/api/svg' && req.method === 'POST') {
    readBody(req).then((body) => {
      const tree = treeFromBody(body);
      const opts = body && typeof body === 'object' ? (body.options || {}) : {};
      const q = quantify(tree, opts);
      const heatmap = opts.heatmap ? buildNodeHeatmapForCLI(tree, q) : {};
      sendText(res, 200, renderSVG(tree, { heatmap, showProb: true, mode: opts.mode || 'light' }), 'image/svg+xml');
    }).catch((e) => sendJSON(res, 400, { ok: false, error: e.message }));
    return;
  }

  // POST /api/validate — 校验
  if (p === '/api/validate' && req.method === 'POST') {
    readBody(req).then((body) => {
      const tree = treeFromBody(body);
      sendJSON(res, 200, validateTree(tree));
    }).catch((e) => sendJSON(res, 400, { ok: false, error: e.message }));
    return;
  }

  // POST /api/simulate — what-if
  if (p === '/api/simulate' && req.method === 'POST') {
    readBody(req).then((body) => {
      const tree = treeFromBody(body);
      const overrides = body.overrides || {};
      const result = fta.simulate(tree, overrides, body.options || {});
      sendJSON(res, 200, result);
    }).catch((e) => sendJSON(res, 400, { ok: false, error: e.message }));
    return;
  }

  // POST /api/normalize — 规范化输出 DSL
  if (p === '/api/normalize' && req.method === 'POST') {
    readBody(req).then((body) => {
      const tree = treeFromBody(body);
      sendJSON(res, 200, { ok: true, dsl: stringifyDSL(tree) });
    }).catch((e) => sendJSON(res, 400, { ok: false, error: e.message }));
    return;
  }

  // GET /api/capabilities
  if (p === '/api/capabilities') {
    sendJSON(res, 200, fta.capabilities());
    return;
  }

  // ============ 跨页 / 多图 ============

  // POST /api/paginate — 计算分页方案
  if (p === '/api/paginate' && req.method === 'POST') {
    readBody(req).then((body) => {
      const tree = treeFromBody(body);
      const o = (body && body.options) || {};

      // mode:'band' —— 按画图人设定的分页点（pageBreak）切页，
      // 与 A4 导出所用引擎完全一致；没有分页点时退回自动预算。
      if (o.mode === 'band') {
        const bp = paginateBanded(tree, { budget: o.maxNodes ?? 14 });
        const pageOf = {};
        for (const pg of bp.pages) {
          for (const id of pg.nodes) pageOf[id] = pg.index;
        }
        // 分页点同时属于「上一页的页底」和「下一页的页顶」，而 pageOf 是单值映射
        // （后写者胜，即归属到展开它的那一页）。节点数必须按 pageOf 统计，
        // 否则会出现"显示 8 个节点、画布只画出 7 个"的不一致。
        const perPage = {};
        for (const pg of Object.values(pageOf)) perPage[pg] = (perPage[pg] || 0) + 1;

        // 分页点同时出现在两页：上一页画虚线框（不展开），下一页作为顶事件展开。
        // pageOf 只能记一页，所以另外给出"本页额外显示的分页点"。
        // 页底那条"接续边"上的事件，其实归属下一页，但本页仍要画出来（虚线）
        const extraOf = {};
        for (const pg of bp.pages) {
          const extras = [...pg.nodes].filter((id) => pageOf[id] !== pg.index);
          if (extras.length) extraOf[pg.index] = extras;
        }
        // 本页顶事件中承接上一页的：同样画虚线，表示"上页已分页"
        const contOf = {};
        for (const pg of bp.pages) {
          if (pg.index > 1) contOf[pg.index] = pg.tops.slice();
        }
        // 上一页的节点数要把这些虚线框加回来，才能和画布上看到的一致
        for (const k of Object.keys(extraOf)) {
          perPage[k] = (perPage[k] || 0) + extraOf[k].length;
        }

        return sendJSON(res, 200, {
          ok: true,
          single: bp.pages.length <= 1,
          total: bp.pages.length,
          pages: bp.pages.map((pg) => ({
            index: pg.index,
            title: pg.title,
            nodeCount: perPage[pg.index] || 0,
            roots: pg.tops,
            continuedFrom: pg.continuedFrom ? { fromPage: pg.continuedFrom } : null,
            continuesTo: [],
            manual: !!pg.manual,
          })),
          references: [],
          pageOf,
          extraOf,
          contOf,
          breakCount: bp.breakCount,
        });
      }

      const pag = autoPaginate(tree, {
        maxNodes: o.maxNodes ?? 24,
        maxDepth: o.maxDepth ?? 5,
        threshold: o.threshold ?? 40,
        force: o.force,
      });
      sendJSON(res, 200, {
        ok: true,
        single: pag.single,
        total: pag.pages.length,
        pages: paginateSummary(pag),
        references: pag.references,
        pageOf: Object.fromEntries(pag.pageOf),
      });
    }).catch((e) => sendJSON(res, 400, { ok: false, error: e.message }));
    return;
  }

  // POST /api/page-svg — 渲染指定页
  if (p === '/api/page-svg' && req.method === 'POST') {
    readBody(req).then((body) => {
      const tree = treeFromBody(body);
      const o = (body && body.options) || {};
      const pag = autoPaginate(tree, {
        maxNodes: o.maxNodes ?? 24, maxDepth: o.maxDepth ?? 5,
        threshold: o.threshold ?? 40, force: o.force,
      });
      const view = buildPageView(tree, pag, Number(o.pageIndex || 1));
      if (!view) return sendJSON(res, 404, { ok: false, error: '页不存在' });
      const q = quantify(tree, o);
      const heatmap = buildNodeHeatmapForCLI(tree, q);
      sendText(res, 200,
        renderSVG(view, {
          heatmap,
          showProb: o.showProb !== false,
          mode: o.mode || 'light',
          page: { nodes: new Set(view.nodes.map((n) => n.id)), title: view.meta.pageTitle },
        }), 'image/svg+xml');
    }).catch((e) => sendJSON(res, 400, { ok: false, error: e.message }));
    return;
  }

  // POST /api/svg-a4 — 导出 A4 分页 HTML（打印 / 另存 PDF 即按 A4 分页）
  if (p === '/api/svg-a4' && req.method === 'POST') {
    readBody(req).then((body) => {
      const tree = treeFromBody(body);
      const o = (body && body.options) || {};
      const q = quantify(tree, o);
      const heatmap = buildNodeHeatmapForCLI(tree, q);
      sendText(res, 200,
        renderA4HTML(tree, {
          heatmap,
          budget: Number(o.budget) || 14,
          showProb: o.showProb !== false,
          mode: o.mode || 'light',
        }), 'text/html; charset=utf-8');
    }).catch((e) => sendJSON(res, 400, { ok: false, error: e.message }));
    return;
  }

  // ============ 格式互操作 ============

  // POST /api/export — 导出指定格式
  if (p === '/api/export' && req.method === 'POST') {
    readBody(req).then((body) => {
      const tree = treeFromBody(body);
      const o = (body && body.options) || {};
      const fmt = (o.format || 'faulttreeplus').toLowerCase();
      const q = quantify(tree, o);

      if (fmt === 'faulttreeplus' || fmt === 'ft+' || fmt === 'xml') {
        const pag = (o.paginate && o.maxNodes)
          ? paginate(tree, { maxNodes: o.maxNodes })
          : null;
        return sendText(res, 200, toFaultTreePlusXML(tree, { pag }), 'application/xml; charset=utf-8');
      }
      if (fmt === 'cafta') {
        return sendText(res, 200, toCAFTA(tree), 'application/xml; charset=utf-8');
      }
      if (fmt === 'medini' || fmt === 'medini-json') {
        const analysis = fta.analyze(tree, { report: 'none' });
        return sendJSON(res, 200, toMediniJSON(tree, analysis));
      }
      if (fmt === 'json') {
        return sendJSON(res, 200, tree);
      }
      if (fmt === 'dsl' || fmt === 'txt') {
        return sendText(res, 200, stringifyDSL(tree), 'text/plain; charset=utf-8');
      }
      if (fmt === 'svg') {
        const heatmap = buildNodeHeatmapForCLI(tree, q);
        return sendText(res, 200, renderSVG(tree, { heatmap, showProb: true }),
          'image/svg+xml');
      }
      sendJSON(res, 400, { ok: false, error: `不支持的格式: ${fmt}` });
    }).catch((e) => sendJSON(res, 400, { ok: false, error: e.message }));
    return;
  }

  // POST /api/import — 导入任意支持格式（自动识别）
  if (p === '/api/import' && req.method === 'POST') {
    readBody(req).then((body) => {
      const content = typeof body === 'string' ? body
        : (body.content ?? body.dsl ?? body.text ?? '');
      const filename = (body && body.filename) || '';
      const r = importAny(content, filename);
      const q = r.validation.ok ? quantify(r.tree, body.options || {}) : null;
      sendJSON(res, 200, {
        ok: r.validation.ok,
        format: r.format,
        tree: r.tree,
        validation: r.validation,
        metrics: q ? q.metrics : null,
      });
    }).catch((e) => sendJSON(res, 400, { ok: false, error: e.message }));
    return;
  }

  // GET /api/examples
  if (p === '/api/examples') {
    const names = ['brake', 'power-supply', 'sensor-2oo3'];
    sendJSON(res, 200, { examples: names.map((n) => {
      const ex = fta.loadExample(n);
      return { name: n, title: ex.meta.title, ok: ex.ok };
    }) });
    return;
  }

  // GET /api/example/:name
  if (p.startsWith('/api/example/') && req.method === 'GET') {
    const name = decodeURIComponent(p.split('/').pop());
    const ex = fta.loadExample(name);
    if (!ex.ok) return sendJSON(res, 404, ex);
    sendJSON(res, 200, { ok: true, name, tree: ex.tree, analysis: ex.analysis, dsl: ex.dsl });
    return;
  }

  sendJSON(res, 404, { ok: false, error: '未知 API 路径' });
}

function serveStatic(req, res, url) {
  let fp = url.pathname;
  if (fp === '/') fp = '/index.html';
  const full = path.join(PUBLIC, path.normalize(fp).replace(/^(\.\.[\/\\])+/, ''));
  if (!full.startsWith(PUBLIC)) {
    res.writeHead(403); return res.end('Forbidden');
  }
  fs.readFile(full, (err, data) => {
    if (err) {
      res.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8' });
      return res.end('404 Not Found');
    }
    res.writeHead(200, {
      'Content-Type': MIME[path.extname(full)] || 'application/octet-stream',
      // 本地工具：禁止浏览器缓存，避免改了代码却仍加载旧 app.js/style.css
      'Cache-Control': 'no-store, must-revalidate',
      'Pragma': 'no-cache',
      'Expires': '0',
    });
    res.end(data);
  });
}

export function createServer() {
  return http.createServer((req, res) => {
    const url = new URL(req.url, `http://${req.headers.host || 'localhost'}`);
    if (req.method === 'OPTIONS') {
      res.writeHead(204, {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET,POST,OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
      });
      return res.end();
    }
    if (url.pathname.startsWith('/api/')) return handleAPI(req, res, url);
    return serveStatic(req, res, url);
  });
}

export function startServer(port = 8777) {
  const server = createServer();
  return new Promise((resolve) => {
    server.listen(port, '127.0.0.1', () => {
      const addr = server.address();
      console.log('');
      console.log('  ╔══════════════════════════════════════════════════════════╗');
      console.log('  ║   FTA Studio 已启动                                       ║');
      console.log('  ╚══════════════════════════════════════════════════════════╝');
      console.log('');
      console.log(`  图形编辑器:  http://127.0.0.1:${addr.port}/`);
      console.log('');
      console.log('  REST API:');
      console.log(`    POST /api/analyze      完整分析（返回 JSON 或报告）`);
      console.log(`    POST /api/dsl          DSL 文本 → 分析结果`);
      console.log(`    POST /api/report       生成 Markdown/HTML 报告`);
      console.log(`    POST /api/svg          渲染故障树 SVG`);
      console.log(`    POST /api/validate     模型校验`);
      console.log(`    POST /api/simulate     What-if 敏感度模拟`);
      console.log(`    GET  /api/capabilities 能力清单`);
      console.log(`    GET  /api/examples     示例列表`);
      console.log('');
      resolve(server);
    });
  });
}

// 直接运行时启动
if (process.argv[1] && import.meta.url.endsWith(path.basename(process.argv[1]))) {
  const port = Number(process.env.FTA_PORT || process.argv[2] || 8777);
  startServer(port);
}