/**
 * Income Tracker - 收入追踪器
 * 多平台收入记录、统计分析、趋势图表
 */

const fs = require('fs');
const path = require('path');
const dayjs = require('dayjs');

// 默认数据路径
const DEFAULT_DATA_PATH = path.join(process.env.HOME, 'clawd', 'data', 'income-tracker.json');

// 汇率缓存（简化版，实际应使用 API）
const EXCHANGE_RATES = {
  USD: { CNY: 7.24, USDT: 1 },
  CNY: { USD: 0.138, USDT: 0.138 },
  USDT: { USD: 1, CNY: 7.24 }
};

/**
 * 收入追踪器主处理函数
 */
async function handler(input = {}) {
  const { action = 'stats', ...params } = input;
  
  // 初始化数据
  const dataPath = process.env.DATA_PATH || DEFAULT_DATA_PATH;
  const data = loadData(dataPath);
  
  switch (action) {
    case 'add':
    case 'record':
      return addIncome(data, params, dataPath);
    
    case 'stats':
    case 'statistics':
      return getStatistics(data, params);
    
    case 'chart':
    case 'trend':
      return getChart(data, params);
    
    case 'analyze':
    case 'analysis':
      return analyzeIncome(data, params);
    
    case 'list':
      return listRecords(data, params);
    
    case 'export':
      return exportData(data, params);
    
    case 'sources':
      return getSources(data);
    
    case 'predict':
      return predictIncome(data, params);
    
    default:
      return { 
        error: `Unknown action: ${action}`,
        availableActions: ['add', 'stats', 'chart', 'analyze', 'list', 'export', 'sources', 'predict']
      };
  }
}

/**
 * 加载数据
 */
function loadData(dataPath) {
  try {
    if (fs.existsSync(dataPath)) {
      return JSON.parse(fs.readFileSync(dataPath, 'utf-8'));
    }
  } catch (e) {
    console.error('Load data error:', e.message);
  }
  
  // 返回默认数据结构
  return {
    records: [],
    sources: {
      'a2a-market': { name: 'A2A市场', type: 'platform' },
      'clawhub': { name: 'ClawHub', type: 'platform' },
      'upwork': { name: 'Upwork', type: 'platform' },
      'fiverr': { name: 'Fiverr', type: 'platform' },
      'freelancer': { name: 'Freelancer', type: 'platform' },
      'outsourcing': { name: '外包项目', type: 'project' },
      'consulting': { name: '咨询服务', type: 'service' },
      'course': { name: '付费课程', type: 'content' },
      'video': { name: '视频收益', type: 'content' },
      'other': { name: '其他', type: 'other' }
    },
    settings: {
      baseCurrency: 'CNY',
      timezone: 'Asia/Shanghai'
    }
  };
}

/**
 * 保存数据
 */
function saveData(data, dataPath) {
  const dir = path.dirname(dataPath);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
  fs.writeFileSync(dataPath, JSON.stringify(data, null, 2));
}

/**
 * 添加收入记录
 */
function addIncome(data, params, dataPath) {
  const { amount, currency = 'CNY', source = 'other', date, note = '', tags = [] } = params;
  
  if (!amount || amount <= 0) {
    return { error: 'Invalid amount' };
  }
  
  const record = {
    id: `inc_${Date.now()}_${Math.random().toString(36).substr(2, 5)}`,
    amount: parseFloat(amount),
    currency: currency.toUpperCase(),
    source,
    date: date || dayjs().format('YYYY-MM-DD'),
    time: dayjs().format('HH:mm:ss'),
    note,
    tags,
    createdAt: new Date().toISOString()
  };
  
  // 转换为基准货币
  record.amountInBase = convertCurrency(record.amount, record.currency, data.settings.baseCurrency);
  
  data.records.push(record);
  saveData(data, dataPath);
  
  return {
    success: true,
    record,
    message: `✅ 已记录收入: ${record.amount} ${record.currency} 来自 ${data.sources[source]?.name || source}`
  };
}

/**
 * 获取统计数据
 */
function getStatistics(data, params) {
  const { period = 'month', year, month, startDate, endDate } = params;
  const now = dayjs();
  
  // 确定时间范围
  let start, end;
  
  if (startDate && endDate) {
    start = dayjs(startDate);
    end = dayjs(endDate);
  } else if (period === 'day') {
    start = now.startOf('day');
    end = now.endOf('day');
  } else if (period === 'week') {
    start = now.startOf('week');
    end = now.endOf('week');
  } else if (period === 'month') {
    const targetMonth = month || now.month() + 1;
    const targetYear = year || now.year();
    start = dayjs(`${targetYear}-${targetMonth}-01`);
    end = start.endOf('month');
  } else if (period === 'year') {
    const targetYear = year || now.year();
    start = dayjs(`${targetYear}-01-01`);
    end = dayjs(`${targetYear}-12-31`);
  } else {
    start = now.startOf('month');
    end = now.endOf('month');
  }
  
  // 筛选记录
  const records = data.records.filter(r => {
    const d = dayjs(r.date);
    return d.isAfter(start) && d.isBefore(end);
  });
  
  // 计算统计
  const baseCurrency = data.settings.baseCurrency;
  const total = records.reduce((sum, r) => sum + (r.amountInBase || r.amount), 0);
  const count = records.length;
  const avg = count > 0 ? total / count : 0;
  
  // 按来源分组
  const bySource = {};
  records.forEach(r => {
    const src = r.source;
    if (!bySource[src]) bySource[src] = { count: 0, total: 0 };
    bySource[src].count++;
    bySource[src].total += r.amountInBase || r.amount;
  });
  
  // 按日期分组
  const byDate = {};
  records.forEach(r => {
    const date = r.date;
    if (!byDate[date]) byDate[date] = { count: 0, total: 0 };
    byDate[date].count++;
    byDate[date].total += r.amountInBase || r.amount;
  });
  
  return {
    period,
    startDate: start.format('YYYY-MM-DD'),
    endDate: end.format('YYYY-MM-DD'),
    total: total.toFixed(2),
    totalCurrency: baseCurrency,
    count,
    average: avg.toFixed(2),
    bySource,
    byDate,
    records: records.slice(-10) // 最近10条
  };
}

/**
 * 生成图表数据
 */
function getChart(data, params) {
  const { type = 'trend', days = 30 } = params;
  const now = dayjs();
  const start = now.subtract(days, 'day');
  
  const records = data.records.filter(r => {
    const d = dayjs(r.date);
    return d.isAfter(start) && d.isBefore(now);
  });
  
  // 按日期聚合
  const dailyTotals = {};
  for (let i = 0; i <= days; i++) {
    const date = start.add(i, 'day').format('YYYY-MM-DD');
    dailyTotals[date] = 0;
  }
  
  records.forEach(r => {
    if (dailyTotals[r.date] !== undefined) {
      dailyTotals[r.date] += r.amountInBase || r.amount;
    }
  });
  
  // 生成 ASCII 图表
  const values = Object.values(dailyTotals);
  const labels = Object.keys(dailyTotals).map(d => d.slice(5)); // MM-DD
  
  if (type === 'trend') {
    return {
      type: 'trend',
      title: `📈 收入趋势（最近 ${days} 天）`,
      data: dailyTotals,
      chart: generateAsciiChart(values, labels),
      summary: {
        total: values.reduce((a, b) => a + b, 0).toFixed(2),
        average: (values.reduce((a, b) => a + b, 0) / values.length).toFixed(2),
        max: Math.max(...values).toFixed(2),
        min: Math.min(...values).toFixed(2)
      }
    };
  }
  
  if (type === 'pie' || type === 'source') {
    const bySource = {};
    records.forEach(r => {
      const src = data.sources[r.source]?.name || r.source;
      if (!bySource[src]) bySource[src] = 0;
      bySource[src] += r.amountInBase || r.amount;
    });
    
    const total = Object.values(bySource).reduce((a, b) => a + b, 0);
    const pieData = Object.entries(bySource)
      .sort((a, b) => b[1] - a[1])
      .map(([source, amount]) => ({
        source,
        amount: amount.toFixed(2),
        percentage: ((amount / total) * 100).toFixed(1)
      }));
    
    return {
      type: 'pie',
      title: '🥧 收入来源分布',
      data: pieData,
      total: total.toFixed(2)
    };
  }
  
  return { error: 'Unknown chart type' };
}

/**
 * 分析收入
 */
function analyzeIncome(data, params) {
  const { by = 'source' } = params;
  const stats = getStatistics(data, { period: 'month' });
  
  // 计算环比增长
  const prevMonthStats = getStatistics(data, { 
    period: 'month',
    month: dayjs().month(), // 上个月
    year: dayjs().subtract(1, 'month').year()
  });
  
  const growth = prevMonthStats.total > 0 
    ? ((stats.total - prevMonthStats.total) / prevMonthStats.total * 100).toFixed(1)
    : 0;
  
  // 来源分析
  const sourceAnalysis = Object.entries(stats.bySource)
    .map(([source, info]) => ({
      source: data.sources[source]?.name || source,
      count: info.count,
      total: info.total.toFixed(2),
      percentage: ((info.total / stats.total) * 100).toFixed(1)
    }))
    .sort((a, b) => parseFloat(b.total) - parseFloat(a.total));
  
  return {
    title: '📊 收入分析报告',
    currentMonth: {
      total: stats.total,
      count: stats.count,
      average: stats.average
    },
    growth: {
      value: growth,
      direction: growth >= 0 ? '📈 上涨' : '📉 下降'
    },
    topSources: sourceAnalysis.slice(0, 5),
    insights: generateInsights(stats, sourceAnalysis, growth)
  };
}

/**
 * 列出记录
 */
function listRecords(data, params) {
  const { limit = 20, source, startDate, endDate } = params;
  
  let records = [...data.records].reverse();
  
  if (source) {
    records = records.filter(r => r.source === source);
  }
  
  if (startDate) {
    records = records.filter(r => r.date >= startDate);
  }
  
  if (endDate) {
    records = records.filter(r => r.date <= endDate);
  }
  
  return {
    total: records.length,
    records: records.slice(0, limit).map(r => ({
      id: r.id,
      date: r.date,
      amount: `${r.amount} ${r.currency}`,
      source: data.sources[r.source]?.name || r.source,
      note: r.note
    }))
  };
}

/**
 * 导出数据
 */
function exportData(data, params) {
  const { format = 'json', startDate, endDate } = params;
  
  let records = data.records;
  
  if (startDate) {
    records = records.filter(r => r.date >= startDate);
  }
  
  if (endDate) {
    records = records.filter(r => r.date <= endDate);
  }
  
  if (format === 'csv') {
    const header = '日期,金额,币种,来源,备注\n';
    const rows = records.map(r => 
      `${r.date},${r.amount},${r.currency},${r.source},"${r.note}"`
    ).join('\n');
    return {
      format: 'csv',
      data: header + rows,
      count: records.length
    };
  }
  
  return {
    format: 'json',
    data: JSON.stringify(records, null, 2),
    count: records.length
  };
}

/**
 * 获取来源列表
 */
function getSources(data) {
  return {
    sources: Object.entries(data.sources).map(([id, info]) => ({
      id,
      name: info.name,
      type: info.type
    }))
  };
}

/**
 * 预测收入
 */
function predictIncome(data, params) {
  // 获取最近3个月数据
  const records = data.records.filter(r => {
    const d = dayjs(r.date);
    return d.isAfter(dayjs().subtract(3, 'month'));
  });
  
  const baseCurrency = data.settings.baseCurrency;
  
  // 按月分组
  const monthlyTotals = {};
  records.forEach(r => {
    const month = r.date.slice(0, 7); // YYYY-MM
    if (!monthlyTotals[month]) monthlyTotals[month] = 0;
    monthlyTotals[month] += r.amountInBase || r.amount;
  });
  
  const months = Object.keys(monthlyTotals).sort();
  const values = months.map(m => monthlyTotals[m]);
  
  // 简单线性预测
  const avg = values.reduce((a, b) => a + b, 0) / values.length;
  const trend = values.length > 1 
    ? (values[values.length - 1] - values[0]) / (values.length - 1)
    : 0;
  
  const prediction = avg + trend;
  
  return {
    title: '🔮 收入预测',
    basedOn: {
      months: months.length,
      data: monthlyTotals
    },
    prediction: {
      nextMonth: prediction.toFixed(2),
      currency: baseCurrency,
      confidence: Math.max(0.3, Math.min(0.9, values.length * 0.15)).toFixed(0)
    },
    trend: trend >= 0 ? '📈 上升' : '📉 下降',
    suggestion: prediction > avg 
      ? '继续保持当前策略，收入有望增长'
      : '建议拓展收入来源或提高定价'
  };
}

/**
 * 货币转换
 */
function convertCurrency(amount, from, to) {
  if (from === to) return amount;
  const rate = EXCHANGE_RATES[from]?.[to] || 1;
  return amount * rate;
}

/**
 * 生成 ASCII 图表
 */
function generateAsciiChart(values, labels) {
  const max = Math.max(...values, 1);
  const height = 10;
  const lines = [];
  
  for (let i = height; i >= 0; i--) {
    const threshold = (max / height) * i;
    let line = `${threshold.toFixed(0).padStart(5)} │ `;
    
    values.forEach((v, idx) => {
      if (idx % 3 === 0) { // 每3天显示一个点
        if (v >= threshold && v < threshold + max / height) {
          line += '●';
        } else if (v >= threshold) {
          line += '│';
        } else {
          line += ' ';
        }
      }
    });
    lines.push(line);
  }
  
  lines.push('─────┴' + '─'.repeat(values.length / 3));
  lines.push('       ' + labels.filter((_, i) => i % 3 === 0).join(' '));
  
  return lines.join('\n');
}

/**
 * 生成洞察
 */
function generateInsights(stats, sourceAnalysis, growth) {
  const insights = [];
  
  if (growth >= 20) {
    insights.push('🎉 本月收入增长显著，继续保持！');
  } else if (growth < 0) {
    insights.push('⚠️ 本月收入有所下降，需要关注');
  }
  
  if (sourceAnalysis.length > 0) {
    const topSource = sourceAnalysis[0];
    if (parseFloat(topSource.percentage) > 50) {
      insights.push(`💡 收入高度依赖 ${topSource.source}，建议拓展其他来源`);
    }
  }
  
  if (stats.count < 5) {
    insights.push('📝 本月收入记录较少，可能遗漏了一些收入');
  }
  
  return insights;
}

// CLI 入口
if (require.main === module) {
  const args = process.argv.slice(2);
  const action = args[0] || 'stats';
  
  let params = {};
  if (action === 'add') {
    params = {
      action: 'add',
      amount: parseFloat(args[1]),
      currency: args[2] || 'CNY',
      source: args[3] || 'other',
      note: args[4] || ''
    };
  } else {
    params = { action, period: args[1] || 'month' };
  }
  
  handler(params).then(result => {
    console.log(JSON.stringify(result, null, 2));
  });
}

module.exports = { handler };
