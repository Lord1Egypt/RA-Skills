const { buildPoster } = require('../lib/builder');

/**
 * @param {Object} data
 * @param {string} data.title
 * @param {string} data.subtitle
 * @param {Array} data.overview - [{label, value, color?, sub?}]
 * @param {Array} data.expense  - [{name, value, pct}]
 * @param {Array} data.routes   - [{name, value, pct}]
 * @param {Array} data.abnormal - [string[]]
 * @param {Array} data.tips     - [string]
 * @param {string} data.footer
 * @param {string} output
 */
function buildDashboard(data, output) {
  const sections = [];

  if (data.overview) {
    sections.push({ type: 'kpi-cards', title: '📊 差旅总览', cards: data.overview });
  }

  if (data.expense) {
    sections.push({ type: 'bar-chart', title: '💼 费用结构', bars: data.expense });
  }

  if (data.routes) {
    sections.push({ type: 'pie-chart', title: '🗺️ 差旅路线 TOP 5', slices: data.routes });
  }

  if (data.abnormal) {
    sections.push({
      type: 'table',
      title: '⚠️ 异常费用分析',
      color: '#ef4444',
      rowBg: 'rgba(239,68,68,0.06)',
      headers: data.abnormalHeaders || ['部门', '异常金额', '涉及人数'],
      rows: data.abnormal,
    });
  }

  if (data.tips) {
    sections.push({ type: 'tips', title: '💡 降本建议', items: data.tips });
  }

  return buildPoster({
    width: 800,
    header: {
      bg: '#1e40af',
      bgEnd: '#3b82f6',
      title: data.title || '📊 数据看板',
      subtitle: data.subtitle || '',
    },
    sections,
    footer: data.footer || '🦞 AI 自动生成',
    output,
  });
}

module.exports = { buildDashboard };
