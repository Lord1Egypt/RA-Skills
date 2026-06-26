#!/usr/bin/env node
const { buildPoster } = require('../lib/builder');

const outputPath = process.argv[2] || '/tmp/canvas-poster-demo.png';

const { canvas, buffer } = buildPoster({
  width: 800,
  header: {
    bg: '#1e40af',
    title: '📊 示例看板',
    subtitle: 'canvas-poster · Section DSL Demo',
  },
  sections: [
    {
      type: 'kpi-cards',
      title: '📊 核心指标',
      cards: [
        { label: '总费用', value: '¥92.2万', color: 'red' },
        { label: '人数', value: '211人' },
        { label: '人均', value: '¥4,371' },
        { label: '达成率', value: '87.2%', color: 'green' },
      ],
    },
    {
      type: 'bar-chart',
      title: '💼 费用结构',
      bars: [
        { name: '住宿费', value: 380700, pct: 41.3 },
        { name: '交通费', value: 290000, pct: 31.5 },
        { name: '餐饮费', value: 150000, pct: 16.3 },
        { name: '其他', value: 101395, pct: 11.0 },
      ],
    },
    {
      type: 'pie-chart',
      title: '🗺️ 路线分布',
      slices: [
        { name: '北京→武汉', value: 180000, pct: 30.2 },
        { name: '北京→上海', value: 120000, pct: 20.1 },
        { name: '深圳→广州', value: 95000, pct: 15.9 },
        { name: '成都→重庆', value: 72000, pct: 12.1 },
        { name: '杭州→南京', value: 55000, pct: 9.2 },
      ],
    },
    {
      type: 'table',
      title: '⚠️ 异常分析',
      headers: ['部门', '异常金额', '占比'],
      rows: [
        ['AI应用中心', '¥64,121', '7.0%'],
        ['市场部', '¥42,300', '4.6%'],
      ],
    },
    {
      type: 'tips',
      title: '💡 管理建议',
      items: [
        '推行「驻留优先」策略：高频路线转为远程协作',
        '加强长期住宿管控：超7天需部门负责人审批',
        '综合降本潜力约 ¥7.5-13万/月',
      ],
    },
  ],
  footer: '🦞 canvas-poster · 示例海报',
  output: outputPath,
});

console.log(`Done: ${outputPath} (${canvas.width}x${canvas.height}, ${(buffer.length / 1024).toFixed(1)} KB)`);
