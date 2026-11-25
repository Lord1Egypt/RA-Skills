#!/usr/bin/env node
/**
 * FTA Studio CLI
 *
 * 用法:
 *   fta analyze <file.fta|file.json> [options]   运行完整分析
 *   fta report  <file> --out <report.md>        生成 Markdown 报告
 *   fta svg     <file> --out <tree.svg>          导出 SVG 图形
 *   fta json    <file> --out <result.json>      导出 JSON 结果
 *   fta validate <file>                          校验模型
 *   fta example <name>                           加载内置示例并分析
 *   fta serve   [--port 8777]                    启动图形编辑器 + API 服务
 *   fta caps                                    查看能力清单
 *
 * 常用选项:
 *   --order N        割集阶数上限
 *   --truncation X   概率截断阈值
 *   --method M       auto | rare | bdd
 *   --no-diagram     报告中不嵌入图形
 *   --heatmap        输出热力图数据
 *   --quiet          仅输出结果，不输出日志
 */

import fs from 'node:fs';
import path from 'node:path';
import process from 'node:process';
import { fta } from './api.mjs';
import { parseDSL, stringifyDSL, validateTree, fmtNum } from './model.mjs';
import { quantify } from './quantify.mjs';
import { renderSVG } from './svg.mjs';
import { generateMarkdownReport, generateHTMLReport } from './report.mjs';
import { buildNodeHeatmapForCLI } from './helpers.mjs';

const argv = process.argv.slice(2);

function parseArgs(args) {
  const out = { _: [] };
  for (let i = 0; i < args.length; i++) {
    const a = args[i];
    if (a.startsWith('--')) {
      const key = a.slice(2).replace(/^no-/, '');
      const val = args[i + 1] && !args[i + 1].startsWith('--') ? args[(i += 1)] : true;
      out[key === '' ? a.slice(2) : key] = val;
    } else {
      out._.push(a);
    }
  }
  return out;
}

const args = parseArgs(argv);
const cmd = args._[0];
const file = args._[1];

function loadTree(fp) {
  const raw = fs.readFileSync(fp, 'utf8');
  const ext = path.extname(fp).toLowerCase();
  if (ext === '.json') {
    const obj = JSON.parse(raw);
    if (obj.dsl) return parseDSL(obj.dsl);
    if (obj.tree) return obj.tree;
    return obj;
  }
  // 默认当作 DSL 文本；若解析失败尝试 JSON
  try {
    const t = parseDSL(raw);
    if (t.nodes.length) return t;
  } catch { /* fall through */ }
  try {
    return JSON.parse(raw);
  } catch {
    throw new Error(`无法解析输入文件: ${fp}`);
  }
}

function saveOut(text, outPath) {
  if (!outPath || outPath === true) {
    process.stdout.write(typeof text === 'string' ? text : JSON.stringify(text, null, 2));
    process.stdout.write('\n');
    return;
  }
  fs.mkdirSync(path.dirname(path.resolve(outPath)), { recursive: true });
  fs.writeFileSync(outPath, text, 'utf8');
  if (!args.quiet) console.error(`✓ 已写入 ${outPath}`);
}

async function main() {
  switch (cmd) {
    case undefined:
    case 'help':
    case '--help':
      printHelp();
      break;

    case 'caps':
      console.log(JSON.stringify(fta.capabilities(), null, 2));
      break;

    case 'serve': {
      const { startServer } = await import('./server.mjs');
      await startServer(Number(args.port || 8777));
      break;
    }

    case 'validate': {
      if (!file) throw new Error('缺少输入文件');
      const tree = loadTree(file);
      const v = validateTree(tree);
      console.log(JSON.stringify(v, null, 2));
      if (!v.ok) process.exitCode = 1;
      break;
    }

    case 'example': {
      const name = file || 'brake';
      const res = fta.loadExample(name);
      if (!res.ok) throw new Error(res.error);
      console.log(`\n📋 示例：${res.name} — ${res.meta.title}\n`);
      const an = res.analysis;
      console.log(`顶事件概率 Q(TOP) = ${fmtNum(an.metrics.topProb)} (${an.metrics.topProbMethod})`);
      console.log(`最小割集：${an.cutSets.total} 个，单一失效点 ${an.cutSets.singlePoints} 个`);
      console.log(`\n前 5 重要度：`);
      for (const r of an.importance.slice(0, 5)) {
        console.log(`  #${r.rank} ${r.name}  q=${fmtNum(r.probability)}  Criticality=${fmtNum(r.criticality)}  FV=${fmtNum(r.fussellVesely)}`);
      }
      if (args.out) {
        saveOut(generateMarkdownReport(res.tree, quantify(res.tree), { heatmap: buildNodeHeatmapForCLI(res.tree) }), args.out);
      }
      break;
    }

    case 'analyze':
    case 'report':
    case 'svg':
    case 'json':
    case 'dsl': {
      if (!file) throw new Error('缺少输入文件');
      const tree = loadTree(file);
      const q = quantify(tree, {
        maxOrder: args.order ? Number(args.order) : undefined,
        truncation: args.truncation ? Number(args.truncation) : undefined,
        quantification: args.method || undefined,
      });

      if (cmd === 'dsl') {
        saveOut(stringifyDSL(tree), args.out);
        break;
      }

      const heatmap = buildNodeHeatmapForCLI(tree, q);

      if (cmd === 'svg') {
        saveOut(renderSVG(tree, { heatmap, showProb: true, mode: args.dark ? 'dark' : 'light' }), args.out || true);
        break;
      }

      if (cmd === 'json') {
        const payload = fta.analyze(tree, { report: 'none', heatmap });
        saveOut(JSON.stringify(payload, null, 2), args.out || true);
        break;
      }

      // analyze / report
      const svg = renderSVG(tree, { heatmap, showProb: true, mode: 'light' });
      if (args.svg && args.svg !== true) {
        fs.mkdirSync(path.dirname(path.resolve(args.svg)), { recursive: true });
        fs.writeFileSync(args.svg, svg, 'utf8');
        if (!args.quiet) console.error(`✓ 图形已导出 ${args.svg}`);
      }

      const ropts = {
        heatmap,
        includeDiagram: !args['no-diagram'],
        embedImage: !args['no-diagram'] && !args.noembed,
        svgFile: args.svg && args.svg !== true ? args.svg : null,
      };
      const md = generateMarkdownReport(tree, q, ropts);

      if (cmd === 'report' && args.html) {
        saveOut(generateHTMLReport(tree, q, ropts), args.out || true);
      } else {
        saveOut(md, args.out || true);
      }

      if (!args.out && !args.quiet) {
        console.error(`\n📊 分析完成：`);
        console.error(`   顶事件概率 Q(TOP) = ${fmtNum(q.metrics.topProb)}  [${q.metrics.topProbMethod}]`);
        console.error(`   最小割集 ${q.metrics.cutSets.total} 个，1 阶（单点失效）${q.metrics.cutSets.singlePoints} 个`);
        console.error(`   树规模 ${tree.nodes.length} 节点 / ${tree.connections.length} 连接\n`);
      }
      break;
    }

    default:
      console.error(`未知命令: ${cmd}`);
      printHelp();
      process.exitCode = 1;
  }
}

function printHelp() {
  console.log(`
╔══════════════════════════════════════════════════════════════╗
║   FTA Studio — 故障树分析工具 (对标 Ansys medini analyze)   ║
╚══════════════════════════════════════════════════════════════╝

命令:
  analyze <file>          完整分析并输出 Markdown 报告（默认打印到屏幕）
  report  <file>          同 analyze，可加 --html 输出 HTML
  svg     <file>          导出故障树 SVG 图形
  json    <file>          导出结构化分析结果 JSON
  dsl     <file>          规范化输出为紧凑 DSL 文本
  validate <file>         校验模型合法性
  example <name>          分析内置示例 (brake/power-supply/sensor-2oo3)
  serve  [--port 8777]    启动图形编辑器 + HTTP API
  caps                    查看能力清单

选项:
  --out <path>     输出文件路径（省略则打印到标准输出）
  --order N        割集阶数上限（0 = 不限）
  --truncation X   概率截断阈值（如 1e-12）
  --method M       求解方法 auto | rare | bdd
  --svg <path>     同时导出 SVG 到指定文件
  --html           report 命令输出 HTML
  --no-diagram     报告不嵌入图形
  --noembed        报告中用文件引用代替内嵌图
  --quiet          静默模式

输入格式:
  *.fta / *.txt  紧凑 DSL 文本（推荐，便于 AI 生成）
  *.json         结构化模型 JSON

示例:
  fta example brake --out brake-report.md
  fta analyze my-tree.fta --order 3 --out report.md
  fta svg my-tree.json --out tree.svg
`);
}

main().catch((e) => {
  console.error(`❌ 错误: ${e.message}`);
  if (process.env.FTA_DEBUG) console.error(e.stack);
  process.exitCode = 1;
});