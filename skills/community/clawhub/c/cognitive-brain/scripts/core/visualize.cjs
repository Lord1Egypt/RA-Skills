#!/usr/bin/env node
/**
 * Cognitive Brain - 可视化脚本（重构版）
 * 知识图谱可视化
 */

const { createLogger } = require('../../src/utils/logger.cjs');
const logger = createLogger('visualize');
const { generateDotGraph, generateMermaidGraph, generateTextGraph, generateHtmlGraph } = require('./graph_generators.cjs');
const { generateStats, printStats } = require('./stats_generator.cjs');

// 解析参数
function parseArgs() {
  const args = process.argv.slice(2);
  const params = { format: 'all' };

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    switch (arg) {
      case '--dot':
        params.format = 'dot';
        break;
      case '--mermaid':
        params.format = 'mermaid';
        break;
      case '--text':
        params.format = 'text';
        break;
      case '--html':
        params.format = 'html';
        break;
      case '--stats':
        params.format = 'stats';
        break;
      case '--help':
      case '-h':
        showHelp();
        process.exit(0);
        break;
    }
  }

  return params;
}

function showHelp() {
  console.log(`
Usage: node visualize.cjs [options]

Options:
  --dot       生成 DOT 格式（Graphviz）
  --mermaid   生成 Mermaid 格式
  --text      生成文本格式
  --html      生成 HTML 交互式图谱
  --stats     显示统计报告
  --help      显示帮助

默认生成所有格式。
  `);
}

// 主函数
async function main() {
  const args = parseArgs();

  try {
    switch (args.format) {
      case 'dot':
        const dot = await generateDotGraph();
        console.log(`✅ DOT 图谱: ${dot.path}`);
        console.log(`   节点: ${dot.concepts}, 边: ${dot.edges}`);
        break;

      case 'mermaid':
        const mermaid = await generateMermaidGraph();
        console.log(`✅ Mermaid 图谱: ${mermaid.path}`);
        console.log(`   节点: ${mermaid.concepts}, 边: ${mermaid.edges}`);
        break;

      case 'text':
        const text = await generateTextGraph();
        console.log(`✅ 文本图谱: ${text.path}`);
        break;

      case 'html':
        const html = await generateHtmlGraph();
        console.log(`✅ HTML 图谱: ${html.path}`);
        console.log(`   节点: ${html.concepts}, 边: ${html.edges}`);
        break;

      case 'stats':
        const stats = await generateStats();
        printStats(stats);
        break;

      default:
        // 生成所有格式
        console.log('📊 生成所有可视化格式...\n');

        const dotResult = await generateDotGraph();
        console.log(`✅ DOT: ${dotResult.path} (${dotResult.concepts}节点, ${dotResult.edges}边)`);

        const mermaidResult = await generateMermaidGraph();
        console.log(`✅ Mermaid: ${mermaidResult.path} (${mermaidResult.concepts}节点, ${mermaidResult.edges}边)`);

        const textResult = await generateTextGraph();
        console.log(`✅ Text: ${textResult.path}`);

        const htmlResult = await generateHtmlGraph();
        console.log(`✅ HTML: ${htmlResult.path} (${htmlResult.concepts}节点, ${htmlResult.edges}边)`);

        console.log('\n📈 统计报告:');
        const statsResult = await generateStats();
        printStats(statsResult);
    }

    process.exit(0);
  } catch (err) {
    console.error('❌ 可视化失败:', err.message);
    process.exit(1);
  }
}

// 导出函数
module.exports = {
  generateDotGraph,
  generateMermaidGraph,
  generateTextGraph,
  generateHtmlGraph,
  generateStats
};

// 主入口
if (require.main === module) {
  main();
}

