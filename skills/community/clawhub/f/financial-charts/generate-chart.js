#!/usr/bin/env node

/**
 * Financial Charts Generator
 * 根据财务数据生成精美的ECharts HTML图表
 */

const fs = require('fs');
const path = require('path');

// 解析命令行参数
function parseArgs() {
  const args = process.argv.slice(2);
  const config = {
    data: null,
    chartType: 'line',
    title: '财务数据图表',
    outputPath: null,
    theme: 'dark',
    colors: null
  };

  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--data' && args[i + 1]) {
      config.data = JSON.parse(args[i + 1]);
      i++;
    } else if (args[i] === '--type' && args[i + 1]) {
      config.chartType = args[i + 1];
      i++;
    } else if (args[i] === '--title' && args[i + 1]) {
      config.title = args[i + 1];
      i++;
    } else if (args[i] === '--output' && args[i + 1]) {
      config.outputPath = args[i + 1];
      i++;
    } else if (args[i] === '--theme' && args[i + 1]) {
      config.theme = args[i + 1];
      i++;
    } else if (args[i] === '--colors' && args[i + 1]) {
      config.colors = args[i + 1].split(',');
      i++;
    }
  }

  return config;
}

// 生成配色方案
function generateColorScheme(theme, customColors) {
  if (customColors && customColors.length > 0) {
    return customColors;
  }

  const schemes = {
    dark: {
      background: 'linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%)',
      text: '#e8e8e8',
      colors: ['#1890ff', '#52c41a', '#faad14', '#ff7875', '#722ed1', '#13c2c2', '#fa8c16']
    },
    light: {
      background: 'linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)',
      text: '#2c3e50',
      colors: ['#1890ff', '#52c41a', '#faad14', '#ff4d4f', '#722ed1', '#13c2c2', '#fa8c16']
    },
    professional: {
      background: 'linear-gradient(135deg, #0c0c0c 0%, #1a1a2e 50%, #16213e 100%)',
      text: '#e8e8e8',
      colors: ['#00d4ff', '#00ff88', '#ffd700', '#ff4757', '#a55eea', '#1e90ff', '#ff6b81']
    }
  };

  return schemes[theme] || schemes.dark;
}

// 分析数据特征
function analyzeData(data, chartType) {
  const analysis = {
    isNegative: false,
    hasDate: false,
    hasMultiSeries: false,
    isFinancial: false,
    min: Infinity,
    max: -Infinity,
    trends: []
  };

  if (!Array.isArray(data)) return analysis;

  // 检查是否包含日期
  if (data.length > 0 && data[0] && (data[0].date || data[0].time || data[0].name)) {
    analysis.hasDate = true;
  }

  // 检查是否有多个系列
  if (data.length > 0 && data[0]) {
    const keys = Object.keys(data[0]);
    analysis.hasMultiSeries = keys.filter(k => !['name', 'date', 'time', 'value', 'x', 'y'].includes(k)).length > 0;
  }

  // 计算极值
  data.forEach(item => {
    if (item.value !== undefined) {
      analysis.min = Math.min(analysis.min, item.value);
      analysis.max = Math.max(analysis.max, item.value);
      if (item.value < 0) analysis.isNegative = true;
    }
  });

  // 检查金融数据特征
  const financeKeys = ['open', 'close', 'high', 'low', 'volume', 'change'];
  if (data.length > 0 && data[0]) {
    analysis.isFinancial = financeKeys.some(key => key in data[0]);
  }

  return analysis;
}

// 生成折线图配置
function generateLineOption(data, colors, analysis) {
  const xData = data.map((item, i) => item.name || item.date || item.time || i + 1);
  const yData = data.map(item => item.value);

  return {
    xAxis: {
      type: 'category',
      data: xData,
      boundaryGap: false,
      axisLine: { lineStyle: { color: '#ffffff30' } },
      axisLabel: { color: '#ffffff99' }
    },
    yAxis: {
      type: 'value',
      axisLine: { lineStyle: { color: '#ffffff30' } },
      axisLabel: { color: '#ffffff99' },
      splitLine: { lineStyle: { color: '#ffffff10' } }
    },
    series: [{
      data: yData,
      type: 'line',
      smooth: true,
      lineStyle: {
        width: 3,
        color: colors[0]
      },
      areaStyle: {
        color: {
          type: 'linear',
          x: 0, y: 0, x2: 0, y2: 1,
          colorStops: [
            { offset: 0, color: colors[0] + '80' },
            { offset: 1, color: colors[0] + '10' }
          ]
        }
      },
      itemStyle: {
        color: colors[0],
        shadowColor: colors[0],
        shadowBlur: 10
      }
    }],
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'rgba(0,0,0,0.8)',
      borderColor: colors[0],
      textStyle: { color: '#fff' }
    }
  };
}

// 生成柱状图配置
function generateBarOption(data, colors, analysis) {
  const xData = data.map((item, i) => item.name || i + 1);
  const yData = data.map(item => item.value);

  return {
    xAxis: {
      type: 'category',
      data: xData,
      axisLine: { lineStyle: { color: '#ffffff30' } },
      axisLabel: { color: '#ffffff99' }
    },
    yAxis: {
      type: 'value',
      axisLine: { lineStyle: { color: '#ffffff30' } },
      axisLabel: { color: '#ffffff99' },
      splitLine: { lineStyle: { color: '#ffffff10' } }
    },
    series: [{
      data: yData.map((val, i) => ({
        value: val,
        itemStyle: {
          color: val >= 0 ? colors[0] : colors[3],
          borderRadius: val >= 0 ? [4, 4, 0, 0] : [0, 0, 4, 4]
        }
      })),
      type: 'bar',
      barWidth: '60%'
    }],
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'rgba(0,0,0,0.8)',
      borderColor: colors[0],
      textStyle: { color: '#fff' }
    }
  };
}

// 生成饼图配置
function generatePieOption(data, colors, analysis) {
  const pieData = data.map((item, i) => ({
    name: item.name || item.label || `项目${i + 1}`,
    value: item.value
  }));

  return {
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c} ({d}%)',
      backgroundColor: 'rgba(0,0,0,0.8)',
      borderColor: colors[0],
      textStyle: { color: '#fff' }
    },
    legend: {
      orient: 'vertical',
      right: '5%',
      top: 'center',
      textStyle: { color: '#ffffff99' }
    },
    series: [{
      type: 'pie',
      radius: ['40%', '70%'],
      center: ['35%', '50%'],
      avoidLabelOverlap: true,
      itemStyle: {
        borderRadius: 8,
        borderColor: '#1a1a2e',
        borderWidth: 2
      },
      label: {
        color: '#ffffff99'
      },
      emphasis: {
        itemStyle: {
          shadowBlur: 20,
          shadowColor: colors[0] + '80'
        }
      },
      data: pieData.map((item, i) => ({
        ...item,
        itemStyle: { color: colors[i % colors.length] }
      }))
    }]
  };
}

// 生成K线图配置
function generateCandlestickOption(data, colors, analysis) {
  const dates = data.map(item => item.date || item.name);
  const ohlc = data.map(item => [item.open, item.close, item.low, item.high]);

  return {
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'cross' },
      backgroundColor: 'rgba(0,0,0,0.9)',
      textStyle: { color: '#fff' },
      formatter: (params) => {
        const d = params[0];
        return `${d.axisValue}<br/>开盘: ${d.data[1]}<br/>收盘: ${d.data[2]}<br/>最低: ${d.data[3]}<br/>最高: ${d.data[0]}`;
      }
    },
    xAxis: {
      type: 'category',
      data: dates,
      axisLine: { lineStyle: { color: '#ffffff30' } },
      axisLabel: { color: '#ffffff99' }
    },
    yAxis: {
      type: 'value',
      scale: true,
      axisLine: { lineStyle: { color: '#ffffff30' } },
      axisLabel: { color: '#ffffff99' },
      splitLine: { lineStyle: { color: '#ffffff10' } }
    },
    series: [{
      type: 'candlestick',
      data: ohlc,
      itemStyle: {
        color: '#52c41a',
        color0: '#ff4d4f',
        borderColor: '#52c41a',
        borderColor0: '#ff4d4f'
      }
    }]
  };
}

// 生成散点图配置
function generateScatterOption(data, colors, analysis) {
  const scatterData = data.map(item => [item.x || item.value, item.y || item.size || 0]);

  return {
    tooltip: {
      trigger: 'item',
      backgroundColor: 'rgba(0,0,0,0.8)',
      textStyle: { color: '#fff' }
    },
    xAxis: {
      type: 'value',
      axisLine: { lineStyle: { color: '#ffffff30' } },
      axisLabel: { color: '#ffffff99' },
      splitLine: { lineStyle: { color: '#ffffff10' } }
    },
    yAxis: {
      type: 'value',
      axisLine: { lineStyle: { color: '#ffffff30' } },
      axisLabel: { color: '#ffffff99' },
      splitLine: { lineStyle: { color: '#ffffff10' } }
    },
    series: [{
      type: 'scatter',
      symbolSize: 15,
      itemStyle: {
        color: colors[0],
        shadowBlur: 10,
        shadowColor: colors[0] + '80'
      },
      data: scatterData
    }]
  };
}

// 生成完整HTML
function generateHTML(config, option, colors) {
  const { title, theme } = config;
  const colorScheme = generateColorScheme(theme, config.colors);

  return `<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${title}</title>
    <script src="https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', 'PingFang SC', 'Microsoft YaHei', sans-serif;
            background: ${colorScheme.background};
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 20px;
        }

        .chart-header {
            text-align: center;
            margin-bottom: 30px;
            width: 100%;
            max-width: 1200px;
        }

        .chart-title {
            font-size: 2.5em;
            font-weight: 700;
            background: linear-gradient(135deg, ${colors[0]}, ${colors[3] || colors[1]}, ${colors[0]});
            background-size: 200% 200%;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            animation: gradientShift 3s ease infinite;
            text-shadow: 0 0 30px ${colors[0]}40;
            letter-spacing: 2px;
        }

        @keyframes gradientShift {
            0%, 100% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
        }

        .chart-subtitle {
            color: ${colorScheme.text}99;
            font-size: 1em;
            margin-top: 8px;
            letter-spacing: 1px;
        }

        .chart-container {
            width: 100%;
            max-width: 1200px;
            background: rgba(255, 255, 255, 0.03);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 30px;
            box-shadow:
                0 8px 32px rgba(0, 0, 0, 0.3),
                inset 0 1px 0 rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }

        #chart {
            width: 100%;
            height: 600px;
        }

        .chart-footer {
            margin-top: 20px;
            text-align: center;
            color: ${colorScheme.text}60;
            font-size: 0.85em;
        }

        .glow-line {
            width: 100px;
            height: 3px;
            background: linear-gradient(90deg, transparent, ${colors[0]}, transparent);
            margin: 15px auto;
            border-radius: 2px;
        }

        @media (max-width: 768px) {
            .chart-title { font-size: 1.8em; }
            #chart { height: 400px; }
            .chart-container { padding: 15px; }
        }
    </style>
</head>
<body>
    <div class="chart-header">
        <h1 class="chart-title">${title}</h1>
        <div class="glow-line"></div>
        <p class="chart-subtitle">数据可视化分析</p>
    </div>

    <div class="chart-container">
        <div id="chart"></div>
    </div>

    <div class="chart-footer">
        Generated by Financial Charts Skill
    </div>

    <script>
        const chart = echarts.init(document.getElementById('chart'));
        const option = ${JSON.stringify(option, null, 2)};

        // 响应式调整
        window.addEventListener('resize', () => {
            chart.resize();
        });

        chart.setOption(option);
    </script>
</body>
</html>`;
}

// 主函数
function main() {
  const config = parseArgs();

  if (!config.data) {
    console.error('错误: 请提供 --data 参数');
    console.log('用法: node generate-chart.js --data \'[{...}]\' --type line --title "图表标题" --output chart.html --theme dark');
    process.exit(1);
  }

  try {
    const data = typeof config.data === 'string' ? JSON.parse(config.data) : config.data;
    const analysis = analyzeData(data, config.chartType);
    const colors = generateColorScheme(config.theme, config.colors);

    let option;
    switch (config.chartType.toLowerCase()) {
      case 'line':
      case '折线图':
        option = generateLineOption(data, colors, analysis);
        break;
      case 'bar':
      case '柱状图':
        option = generateBarOption(data, colors, analysis);
        break;
      case 'pie':
      case '饼图':
        option = generatePieOption(data, colors, analysis);
        break;
      case 'candlestick':
      case 'kline':
      case 'k线图':
        option = generateCandlestickOption(data, colors, analysis);
        break;
      case 'scatter':
      case '散点图':
        option = generateScatterOption(data, colors, analysis);
        break;
      default:
        option = generateLineOption(data, colors, analysis);
    }

    const html = generateHTML(config, option, colors);
    const outputPath = config.outputPath || `chart-${Date.now()}.html`;

    fs.writeFileSync(outputPath, html, 'utf-8');
    const absPath = path.resolve(outputPath);
    console.log(`图表已生成: ${absPath}`);
    console.log(`打开命令: open "${absPath}"`);

  } catch (error) {
    console.error('生成失败:', error.message);
    process.exit(1);
  }
}

main();
