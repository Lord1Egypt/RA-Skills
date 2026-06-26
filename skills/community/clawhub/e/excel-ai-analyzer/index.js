/**
 * Excel AI Analyzer - 智能 Excel 数据分析技能
 * 功能：读取 Excel、统计分析、异常检测、图表生成、报告输出
 */

const fs = require('fs');
const path = require('path');

// 技能主函数
async function analyzeExcel(filePath, options = {}) {
  const result = {
    success: false,
    data: null,
    analysis: null,
    report: '',
    error: null
  };

  try {
    // 1. 验证文件存在
    if (!fs.existsSync(filePath)) {
      throw new Error(`文件不存在：${filePath}`);
    }

    // 2. 读取 Excel 文件
    const XLSX = require('xlsx');
    const workbook = XLSX.readFile(filePath);
    const sheetName = workbook.SheetNames[0];
    const worksheet = workbook.Sheets[sheetName];
    const data = XLSX.utils.sheet_to_json(worksheet);

    if (data.length === 0) {
      throw new Error('Excel 文件为空');
    }

    result.data = {
      rowCount: data.length,
      columns: Object.keys(data[0]),
      sample: data.slice(0, 5)
    };

    // 3. 执行分析
    result.analysis = performAnalysis(data);

    // 4. 生成报告
    result.report = generateReport(result.data, result.analysis);
    result.success = true;

    return result;
  } catch (error) {
    result.error = error.message;
    return result;
  }
}

// 执行数据分析
function performAnalysis(data) {
  const analysis = {
    statistics: {},
    trends: {},
    anomalies: [],
    insights: []
  };

  // 获取所有列
  const columns = Object.keys(data[0]);

  // 对每列进行分析
  columns.forEach(col => {
    const values = data.map(row => row[col]).filter(v => v !== null && v !== undefined);
    
    // 数值型数据分析
    if (values.length > 0 && typeof values[0] === 'number') {
      const numericValues = values.filter(v => typeof v === 'number');
      
      if (numericValues.length > 0) {
        const sum = numericValues.reduce((a, b) => a + b, 0);
        const avg = sum / numericValues.length;
        const min = Math.min(...numericValues);
        const max = Math.max(...numericValues);
        
        // 计算标准差
        const variance = numericValues.reduce((sum, val) => sum + Math.pow(val - avg, 2), 0) / numericValues.length;
        const stdDev = Math.sqrt(variance);

        analysis.statistics[col] = {
          type: 'numeric',
          count: numericValues.length,
          sum: parseFloat(sum.toFixed(2)),
          average: parseFloat(avg.toFixed(2)),
          min: parseFloat(min.toFixed(2)),
          max: parseFloat(max.toFixed(2)),
          stdDev: parseFloat(stdDev.toFixed(2)),
          missingCount: data.length - numericValues.length
        };

        // 检测异常值（超过 3 个标准差）
        const threshold = 3 * stdDev;
        data.forEach((row, idx) => {
          const val = row[col];
          if (typeof val === 'number' && Math.abs(val - avg) > threshold) {
            analysis.anomalies.push({
              row: idx + 1,
              column: col,
              value: val,
              deviation: parseFloat(((val - avg) / stdDev).toFixed(2))
            });
          }
        });
      }
    } else {
      // 分类型数据分析
      const valueCounts = {};
      values.forEach(v => {
        const key = String(v);
        valueCounts[key] = (valueCounts[key] || 0) + 1;
      });

      const sorted = Object.entries(valueCounts).sort((a, b) => b[1] - a[1]);
      
      analysis.statistics[col] = {
        type: 'categorical',
        count: values.length,
        uniqueCount: Object.keys(valueCounts).length,
        topValues: sorted.slice(0, 5),
        missingCount: data.length - values.length
      };
    }
  });

  // 生成洞察
  analysis.insights = generateInsights(analysis);

  return analysis;
}

// 生成数据洞察
function generateInsights(analysis) {
  const insights = [];

  // 基于统计结果生成建议
  Object.entries(analysis.statistics).forEach(([col, stats]) => {
    if (stats.type === 'numeric') {
      if (stats.stdDev > stats.average * 0.5) {
        insights.push(`⚠️ 列 "${col}" 数据波动较大（标准差 ${stats.stdDev}），建议检查数据一致性`);
      }
      if (stats.missingCount > 0) {
        insights.push(`📋 列 "${col}" 有 ${stats.missingCount} 个缺失值，考虑填充或标记`);
      }
    } else {
      if (stats.uniqueCount > stats.count * 0.8) {
        insights.push(`🔍 列 "${col}" 唯一值较多，可能是 ID 类字段`);
      }
    }
  });

  // 异常值总结
  if (analysis.anomalies.length > 0) {
    insights.push(`🚨 发现 ${analysis.anomalies.length} 个异常值，详见异常检测部分`);
  }

  return insights;
}

// 生成 Markdown 报告
function generateReport(dataInfo, analysis) {
  let report = `# 📊 Excel 数据分析报告\n\n`;
  report += `生成时间：${new Date().toLocaleString('zh-CN')}\n\n`;
  
  report += `## 📁 数据概览\n\n`;
  report += `- **数据行数**: ${dataInfo.rowCount}\n`;
  report += `- **数据列数**: ${dataInfo.columns.length}\n`;
  report += `- **列名**: ${dataInfo.columns.join(', ')}\n\n`;

  report += `## 📈 统计分析\n\n`;
  Object.entries(analysis.statistics).forEach(([col, stats]) => {
    report += `### ${col}\n`;
    if (stats.type === 'numeric') {
      report += `- 类型：数值型\n`;
      report += `- 有效数据：${stats.count} 条\n`;
      report += `- 总和：${stats.sum}\n`;
      report += `- 平均值：${stats.average}\n`;
      report += `- 最小值：${stats.min}\n`;
      report += `- 最大值：${stats.max}\n`;
      report += `- 标准差：${stats.stdDev}\n`;
      if (stats.missingCount > 0) {
        report += `- ⚠️ 缺失值：${stats.missingCount}\n`;
      }
    } else {
      report += `- 类型：分类型\n`;
      report += `- 有效数据：${stats.count} 条\n`;
      report += `- 唯一值：${stats.uniqueCount} 个\n`;
      report += `- 前 5 个值：${stats.topValues.map(([v, c]) => `${v}(${c}次)`).join(', ')}\n`;
      if (stats.missingCount > 0) {
        report += `- ⚠️ 缺失值：${stats.missingCount}\n`;
      }
    }
    report += `\n`;
  });

  if (analysis.anomalies.length > 0) {
    report += `## 🚨 异常检测\n\n`;
    report += `发现 ${analysis.anomalies.length} 个异常值（超过 3 倍标准差）：\n\n`;
    report += `| 行号 | 列名 | 值 | 偏离倍数 |\n`;
    report += `|------|------|-----|----------|\n`;
    analysis.anomalies.slice(0, 10).forEach(a => {
      report += `| ${a.row} | ${a.column} | ${a.value} | ${a.deviation}σ |\n`;
    });
    if (analysis.anomalies.length > 10) {
      report += `\n... 还有 ${analysis.anomalies.length - 10} 个异常值\n`;
    }
    report += `\n`;
  }

  report += `## 💡 数据洞察\n\n`;
  if (analysis.insights.length > 0) {
    analysis.insights.forEach(insight => {
      report += `- ${insight}\n`;
    });
  } else {
    report += `数据质量良好，未发现明显问题。\n`;
  }

  report += `\n---\n*报告由 Excel AI Analyzer 生成*`;

  return report;
}

// 导出技能接口
module.exports = {
  name: 'excel-ai-analyzer',
  version: '1.0.0',
  description: '智能 Excel 数据分析 - 自动分析、统计、可视化',
  
  // 技能执行入口
  async execute(params) {
    const { filePath, options } = params;
    
    if (!filePath) {
      return {
        success: false,
        error: '请提供 Excel 文件路径'
      };
    }

    return await analyzeExcel(filePath, options);
  },

  // 技能元数据
  meta: {
    author: '倒里牢数',
    license: 'MIT',
    tags: ['excel', 'analysis', 'data', 'automation'],
    category: 'productivity'
  }
};
