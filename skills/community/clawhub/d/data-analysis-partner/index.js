/**
 * OpenClaw data-analysis Skill
 * 调用 Python 分析脚本，生成带 ECharts 交互图表的自包含 HTML 报告
 */

// CommonJS 格式，兼容 OpenClaw skill runner
const { spawnSync } = require("child_process");
const { writeFileSync, mkdirSync, existsSync } = require("fs");
const { join } = require("path");
const { homedir } = require("os");

// 优先使用 Skill 内置 .venv，回退到系统 python3
function resolvePythonBin() {
  const venvPy = join(__dirname, ".venv", "bin", "python3");
  if (existsSync(venvPy)) return venvPy;

  // 回退到系统 python3，检查是否有 pandas
  const sysPy = spawnSync("python3", ["-c", "import pandas, numpy"], { encoding: "utf8" });
  if (sysPy.status === 0) return "python3";

  throw new Error(
    "未找到可用的 Python 环境，请手动安装依赖：\n" +
    `  python3 -m venv "${join(__dirname, ".venv")}"\n` +
    `  "${venvPy}" -m pip install pandas numpy openpyxl xlrd`
  );
}

const PYTHON_BIN = resolvePythonBin();

// ─────────────────────────────────────────────────────────────
// ECharts 调色板
// ─────────────────────────────────────────────────────────────
const PALETTE = [
  "#4e9bff", "#36cfc9", "#73d13d", "#ffa940", "#ff4d4f",
  "#9254de", "#36cfc9", "#ff85c0", "#bae637", "#40a9ff",
];

// ─────────────────────────────────────────────────────────────
// ECharts option 构建器
// ─────────────────────────────────────────────────────────────

function buildEChartsOption(chart) {
  const base = {
    backgroundColor: "transparent",
    animation: true,
    animationDuration: 600,
  };

  const titleStyle = {
    title: {
      text: chart.title,
      subtext: chart.subtitle || "",
      left: "center",
      top: 8,
      textStyle: { fontSize: 14, fontWeight: "bold", color: "#1a1a2e" },
      subtextStyle: { fontSize: 11, color: "#888" },
    },
  };

  const tooltip = { trigger: "axis", confine: true };
  const gridPadding = { grid: { left: "10%", right: "5%", bottom: "15%", top: "18%" } };

  // ── 柱状图 ──────────────────────────────────────────────
  if (chart.type === "bar" || chart.type === "grouped_bar") {
    return {
      ...base,
      ...titleStyle,
      tooltip,
      ...gridPadding,
      xAxis: {
        type: "category",
        data: chart.x,
        axisLabel: {
          rotate: chart.x.length > 6 ? 35 : 0,
          fontSize: 11,
          interval: 0,
          overflow: "truncate",
          width: 80,
        },
        name: chart.xAxisName || "",
      },
      yAxis: {
        type: "value",
        name: chart.yAxisName || "",
        nameTextStyle: { fontSize: 11 },
      },
      series: [
        {
          type: "bar",
          data: chart.y.map((v, i) => ({
            value: v,
            itemStyle: { color: chart.color || PALETTE[i % PALETTE.length] },
          })),
          label: {
            show: chart.x.length <= 12,
            position: "top",
            fontSize: 10,
            formatter: (p) =>
              typeof p.value === "number" && p.value >= 1000
                ? p.value.toLocaleString()
                : p.value,
          },
          barMaxWidth: 48,
        },
      ],
    };
  }

  // ── 直方图 ──────────────────────────────────────────────
  if (chart.type === "histogram") {
    return {
      ...base,
      ...titleStyle,
      tooltip: { trigger: "axis" },
      ...gridPadding,
      xAxis: {
        type: "category",
        data: chart.x,
        axisLabel: { rotate: 30, fontSize: 10, interval: Math.floor(chart.x.length / 6) },
        name: "区间",
      },
      yAxis: { type: "value", name: "频次" },
      series: [
        {
          type: "bar",
          data: chart.y,
          barCategoryGap: "5%",
          itemStyle: { color: "#4e9bff", borderRadius: [2, 2, 0, 0] },
          markLine: {
            silent: true,
            lineStyle: { color: "#ff4d4f", type: "dashed" },
            data: [
              { xAxis: chart.mean, name: `均值 ${chart.mean}` },
            ],
          },
        },
      ],
    };
  }

  // ── 折线图 ──────────────────────────────────────────────
  if (chart.type === "line") {
    return {
      ...base,
      ...titleStyle,
      tooltip,
      ...gridPadding,
      xAxis: {
        type: "category",
        data: chart.x,
        axisLabel: {
          rotate: 35,
          fontSize: 10,
          interval: Math.max(0, Math.floor(chart.x.length / 8) - 1),
        },
      },
      yAxis: { type: "value", name: chart.yAxisName || "" },
      series: [
        {
          type: "line",
          data: chart.y,
          smooth: chart.smooth || false,
          symbol: chart.x.length > 50 ? "none" : "circle",
          symbolSize: 4,
          lineStyle: { width: 2, color: "#4e9bff" },
          areaStyle: { color: { type: "linear", x: 0, y: 0, x2: 0, y2: 1,
            colorStops: [
              { offset: 0, color: "rgba(78,155,255,0.25)" },
              { offset: 1, color: "rgba(78,155,255,0.02)" },
            ]}},
        },
      ],
    };
  }

  // ── 多系列柱状图 ──────────────────────────────────────────
  if (chart.type === "multi_bar") {
    return {
      ...base,
      ...titleStyle,
      tooltip: { trigger: "axis", axisPointer: { type: "shadow" } },
      legend: { bottom: 4, textStyle: { fontSize: 11 } },
      grid: { left: "10%", right: "5%", bottom: "20%", top: "20%" },
      xAxis: {
        type: "category",
        data: chart.x,
        axisLabel: { rotate: chart.x.length > 6 ? 30 : 0, fontSize: 11, interval: 0 },
        name: chart.xAxisName || "",
      },
      yAxis: { type: "value" },
      series: chart.series.map((s, i) => ({
        name: s.name,
        type: "bar",
        data: s.data,
        itemStyle: { color: PALETTE[i % PALETTE.length] },
        barMaxWidth: 32,
      })),
    };
  }

  // ── 饼图 ─────────────────────────────────────────────────
  if (chart.type === "pie") {
    return {
      ...base,
      ...titleStyle,
      tooltip: { trigger: "item", formatter: "{b}: {c} ({d}%)" },
      legend: { orient: "vertical", right: "5%", top: "center", textStyle: { fontSize: 11 } },
      series: [
        {
          type: "pie",
          radius: ["35%", "65%"],
          center: ["40%", "55%"],
          data: chart.data.map((d, i) => ({
            ...d,
            itemStyle: { color: PALETTE[i % PALETTE.length] },
          })),
          label: { formatter: "{b}\n{d}%", fontSize: 11 },
          emphasis: {
            itemStyle: { shadowBlur: 10, shadowOffsetX: 0, shadowColor: "rgba(0,0,0,0.3)" },
          },
        },
      ],
    };
  }

  // ── 热力图 ────────────────────────────────────────────────
  if (chart.type === "heatmap") {
    const n = chart.x.length;
    const cellSize = Math.max(30, Math.min(60, Math.floor(320 / n)));
    return {
      ...base,
      ...titleStyle,
      tooltip: {
        position: "top",
        formatter: (p) => `${chart.y[p.data[1]]} vs ${chart.x[p.data[0]]}<br/>r = ${p.data[2]}`,
      },
      grid: { left: "18%", right: "8%", bottom: "18%", top: "22%" },
      xAxis: {
        type: "category",
        data: chart.x,
        axisLabel: { rotate: 35, fontSize: 10 },
        splitArea: { show: true },
      },
      yAxis: {
        type: "category",
        data: chart.y,
        axisLabel: { fontSize: 10 },
        splitArea: { show: true },
      },
      visualMap: {
        min: -1,
        max: 1,
        calculable: true,
        orient: "horizontal",
        left: "center",
        bottom: 4,
        inRange: { color: ["#d73027", "#f7f7f7", "#1a9641"] },
        textStyle: { fontSize: 10 },
      },
      series: [
        {
          type: "heatmap",
          data: chart.data,
          label: { show: n <= 8, fontSize: 10,
            formatter: (p) => p.data[2].toFixed(2) },
          emphasis: { itemStyle: { shadowBlur: 10, shadowColor: "rgba(0,0,0,0.5)" } },
        },
      ],
    };
  }

  return null;
}

// ─────────────────────────────────────────────────────────────
// HTML 报告生成器
// ─────────────────────────────────────────────────────────────

function generateHTMLReport(data) {
  const {
    basic_info,
    stats,
    charts,
    insights,
    requirements,
    summary,
    file_name,
  } = data;

  const now = new Date().toLocaleString("zh-CN", {
    year: "numeric", month: "2-digit", day: "2-digit",
    hour: "2-digit", minute: "2-digit",
  });

  // 构建列信息表格行
  const colRows = basic_info.columns
    .map((c) => {
      const typeLabel = {
        numeric: '<span class="badge badge-blue">数值</span>',
        categorical: '<span class="badge badge-green">分类</span>',
        datetime: '<span class="badge badge-purple">时间</span>',
        text: '<span class="badge badge-gray">文本</span>',
        boolean: '<span class="badge badge-orange">布尔</span>',
        empty: '<span class="badge badge-red">空列</span>',
      }[c.type] || `<span class="badge badge-gray">${c.type}</span>`;

      const missingCell =
        c.missing_pct > 20
          ? `<span style="color:#ff4d4f;font-weight:600">${c.missing_pct}%</span>`
          : c.missing_pct > 0
          ? `<span style="color:#ffa940">${c.missing_pct}%</span>`
          : `<span style="color:#52c41a">0%</span>`;

      return `
        <tr>
          <td><code>${c.name}</code></td>
          <td>${typeLabel}</td>
          <td>${missingCell}</td>
          <td>${c.unique.toLocaleString()}</td>
          <td class="sample-vals">${c.sample.join(" / ")}</td>
        </tr>`;
    })
    .join("");

  // 构建描述统计表格
  const statsRows = Object.entries(stats)
    .map(([col, s]) => `
      <tr>
        <td><code>${col}</code></td>
        <td>${s.count.toLocaleString()}</td>
        <td>${s.mean}</td>
        <td>${s.std}</td>
        <td>${s.min}</td>
        <td>${s.q25}</td>
        <td>${s.median}</td>
        <td>${s.q75}</td>
        <td>${s.max}</td>
        <td>${s.skew}</td>
      </tr>`)
    .join("");

  // 构建洞察列表
  const insightItems = insights
    .map((ins) => {
      const color = ins.level === "warning" ? "#fff3e0" : "#e8f4fd";
      const border = ins.level === "warning" ? "#ffa940" : "#4e9bff";
      return `
        <div class="insight-item" style="background:${color};border-left:4px solid ${border}">
          ${ins.icon} ${ins.text}
        </div>`;
    })
    .join("");

  // 构建图表区域
  const chartDivs = charts
    .map((chart, i) => {
      const option = buildEChartsOption(chart);
      if (!option) return "";
      const optionJson = JSON.stringify(option);
      return `
        <div class="chart-card">
          <div id="chart-${i}" class="chart-container"></div>
          <script>
            (function() {
              var dom = document.getElementById('chart-${i}');
              var myChart = echarts.init(dom, null, { renderer: 'canvas' });
              myChart.setOption(${optionJson});
              window.addEventListener('resize', function() { myChart.resize(); });
            })();
          </script>
        </div>`;
    })
    .join("");

  // 拼装完整 HTML
  return `<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>📊 数据分析报告 - ${file_name}</title>
  <script src="https://cdn.jsdelivr.net/npm/echarts@5/dist/echarts.min.js"></script>
  <style>
    :root {
      --bg: #f0f2f5;
      --card: #ffffff;
      --primary: #1a1a2e;
      --accent: #4e9bff;
      --accent2: #36cfc9;
      --text: #222;
      --muted: #888;
      --border: #e8e8e8;
      --radius: 12px;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC",
                   "Helvetica Neue", sans-serif;
      background: var(--bg);
      color: var(--text);
      line-height: 1.6;
    }

    /* ── 顶部 Header ── */
    .header {
      background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
      color: #fff;
      padding: 36px 48px 28px;
    }
    .header-row { display: flex; justify-content: space-between; align-items: flex-start; }
    .header h1 { font-size: 26px; font-weight: 700; letter-spacing: 0.5px; }
    .header .subtitle { font-size: 13px; color: rgba(255,255,255,0.65); margin-top: 6px; }
    .header .meta { font-size: 12px; color: rgba(255,255,255,0.5); margin-top: 4px; }
    .requirements-box {
      margin-top: 18px;
      background: rgba(255,255,255,0.08);
      border: 1px solid rgba(255,255,255,0.15);
      border-radius: 8px;
      padding: 12px 16px;
      font-size: 13px;
      color: rgba(255,255,255,0.9);
    }
    .requirements-box .label {
      font-size: 11px;
      color: var(--accent2);
      text-transform: uppercase;
      letter-spacing: 0.8px;
      margin-bottom: 4px;
    }

    /* ── 主内容容器 ── */
    .main { max-width: 1280px; margin: 0 auto; padding: 32px 24px 60px; }

    /* ── 统计卡片 ── */
    .stats-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
      gap: 16px;
      margin-bottom: 32px;
    }
    .stat-card {
      background: var(--card);
      border-radius: var(--radius);
      padding: 20px 16px;
      text-align: center;
      box-shadow: 0 2px 8px rgba(0,0,0,0.06);
      transition: transform 0.2s, box-shadow 0.2s;
    }
    .stat-card:hover { transform: translateY(-2px); box-shadow: 0 4px 16px rgba(0,0,0,0.1); }
    .stat-card .num { font-size: 32px; font-weight: 700; color: var(--accent); line-height: 1.1; }
    .stat-card .label { font-size: 12px; color: var(--muted); margin-top: 4px; }

    /* ── 区块 ── */
    .section { margin-bottom: 32px; }
    .section-title {
      font-size: 17px;
      font-weight: 700;
      color: var(--primary);
      margin-bottom: 16px;
      padding-left: 12px;
      border-left: 4px solid var(--accent);
    }

    /* ── 卡片 ── */
    .card {
      background: var(--card);
      border-radius: var(--radius);
      padding: 24px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }

    /* ── 表格 ── */
    .table-wrap { overflow-x: auto; }
    table { width: 100%; border-collapse: collapse; font-size: 13px; }
    thead th {
      background: #f7f8fa;
      color: #555;
      font-weight: 600;
      padding: 10px 14px;
      text-align: left;
      border-bottom: 2px solid var(--border);
      white-space: nowrap;
    }
    tbody tr:hover { background: #fafafa; }
    tbody td {
      padding: 9px 14px;
      border-bottom: 1px solid var(--border);
      vertical-align: middle;
    }
    code {
      background: #f5f5f5;
      padding: 2px 6px;
      border-radius: 4px;
      font-size: 12px;
      color: #e83e8c;
    }
    .sample-vals { color: var(--muted); font-size: 12px; max-width: 200px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }

    /* ── Badge ── */
    .badge {
      display: inline-block;
      padding: 2px 8px;
      border-radius: 10px;
      font-size: 11px;
      font-weight: 600;
    }
    .badge-blue { background: #e6f4ff; color: #1677ff; }
    .badge-green { background: #f6ffed; color: #52c41a; }
    .badge-purple { background: #f9f0ff; color: #722ed1; }
    .badge-gray { background: #f5f5f5; color: #666; }
    .badge-orange { background: #fff7e6; color: #d46b08; }
    .badge-red { background: #fff2f0; color: #cf1322; }

    /* ── 洞察 ── */
    .insights-list { display: flex; flex-direction: column; gap: 10px; }
    .insight-item {
      padding: 12px 16px;
      border-radius: 8px;
      font-size: 13px;
      line-height: 1.6;
    }
    .no-insights { color: var(--muted); font-size: 13px; padding: 12px 0; }

    /* ── 图表网格 ── */
    .charts-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(480px, 1fr));
      gap: 20px;
    }
    .chart-card {
      background: var(--card);
      border-radius: var(--radius);
      padding: 8px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.06);
      transition: box-shadow 0.2s;
    }
    .chart-card:hover { box-shadow: 0 4px 20px rgba(0,0,0,0.1); }
    .chart-container { width: 100%; height: 320px; }

    /* ── 页脚 ── */
    .footer {
      text-align: center;
      color: var(--muted);
      font-size: 12px;
      padding: 24px;
      border-top: 1px solid var(--border);
      margin-top: 16px;
    }
  </style>
</head>
<body>

<!-- ── Header ── -->
<div class="header">
  <div class="header-row">
    <div>
      <h1>📊 数据分析报告</h1>
      <div class="subtitle">文件：${file_name}${basic_info.sampled ? `（已抽样，原始 ${basic_info.original_rows.toLocaleString()} 行）` : ""}</div>
      <div class="meta">生成时间：${now}</div>
    </div>
  </div>
  <div class="requirements-box">
    <div class="label">分析需求</div>
    ${requirements}
  </div>
</div>

<!-- ── 主内容 ── -->
<div class="main">

  <!-- 统计卡片 -->
  <div class="stats-grid">
    <div class="stat-card">
      <div class="num">${basic_info.rows.toLocaleString()}</div>
      <div class="label">数据行数</div>
    </div>
    <div class="stat-card">
      <div class="num">${basic_info.cols}</div>
      <div class="label">数据列数</div>
    </div>
    <div class="stat-card">
      <div class="num">${summary.numeric_cols.length}</div>
      <div class="label">数值字段</div>
    </div>
    <div class="stat-card">
      <div class="num">${summary.categorical_cols.length}</div>
      <div class="label">分类字段</div>
    </div>
    <div class="stat-card">
      <div class="num" style="color:${basic_info.duplicates > 0 ? "#ffa940" : "#52c41a"}">${basic_info.duplicates.toLocaleString()}</div>
      <div class="label">重复行数</div>
    </div>
    <div class="stat-card">
      <div class="num">${charts.length}</div>
      <div class="label">生成图表</div>
    </div>
    <div class="stat-card">
      <div class="num">${insights.length}</div>
      <div class="label">自动洞察</div>
    </div>
  </div>

  <!-- 数据洞察 -->
  ${insights.length > 0 ? `
  <div class="section">
    <div class="section-title">🔍 数据洞察</div>
    <div class="card">
      <div class="insights-list">
        ${insightItems}
      </div>
    </div>
  </div>` : ""}

  <!-- 可视化图表 -->
  ${charts.length > 0 ? `
  <div class="section">
    <div class="section-title">📈 可视化分析</div>
    <div class="charts-grid">
      ${chartDivs}
    </div>
  </div>` : ""}

  <!-- 数据概览 -->
  <div class="section">
    <div class="section-title">📋 数据概览 — 字段信息</div>
    <div class="card">
      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>字段名</th>
              <th>类型</th>
              <th>缺失率</th>
              <th>唯一值</th>
              <th>样本值</th>
            </tr>
          </thead>
          <tbody>${colRows}</tbody>
        </table>
      </div>
    </div>
  </div>

  <!-- 描述统计 -->
  ${statsRows ? `
  <div class="section">
    <div class="section-title">📊 描述统计 — 数值字段</div>
    <div class="card">
      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>字段</th><th>计数</th><th>均值</th><th>标准差</th>
              <th>最小值</th><th>Q25</th><th>中位数</th><th>Q75</th>
              <th>最大值</th><th>偏度</th>
            </tr>
          </thead>
          <tbody>${statsRows}</tbody>
        </table>
      </div>
    </div>
  </div>` : ""}

</div>

<div class="footer">
  本报告由 OpenClaw data-analysis Skill 自动生成 · ${now}
</div>

</body>
</html>`;
}

// ─────────────────────────────────────────────────────────────
// 核心工具函数
// ─────────────────────────────────────────────────────────────

module.exports = {
  async analyze_data({ file_path, requirements, output_dir }, { config }) {
    // 1. 确定输出目录
    const outDir = output_dir
      || config?.outputDir?.replace("~", homedir())
      || join(homedir(), "Downloads");
    mkdirSync(outDir, { recursive: true });

    // 2. 调用 Python 分析脚本
    const scriptPath = join(__dirname, "scripts", "analyze.py");
    const maxCharts = String(config?.maxCharts || 8);

    const result = spawnSync(
      PYTHON_BIN,
      [scriptPath, "--file", file_path, "--requirements", requirements, "--max-charts", maxCharts],
      { encoding: "utf8", maxBuffer: 20 * 1024 * 1024 }
    );

    if (result.status !== 0 || result.error) {
      const errMsg = result.stderr || result.error?.message || "未知错误";
      throw new Error(`数据分析脚本执行失败：\n${errMsg}`);
    }

    let analysisData;
    try {
      analysisData = JSON.parse(result.stdout);
    } catch {
      throw new Error(`分析脚本输出解析失败：${result.stdout.slice(0, 500)}`);
    }

    if (analysisData.error) {
      throw new Error(`数据分析出错：${analysisData.error}\n${analysisData.traceback || ""}`);
    }

    // 3. 生成 HTML 报告
    const timestamp = new Date().toISOString().replace(/[:.]/g, "-").slice(0, 19);
    const baseName = (analysisData.file_name || "report").replace(/\.[^.]+$/, "");
    const reportFileName = `report_${baseName}_${timestamp}.html`;
    const reportPath = join(outDir, reportFileName);

    const html = generateHTMLReport(analysisData);
    writeFileSync(reportPath, html, "utf8");

    // 4. 返回结构化结果（供 AI Agent 生成自然语言总结）
    return {
      report_path: reportPath,
      open_command: `open "${reportPath}"`,
      summary: analysisData.summary,
      charts_count: analysisData.charts.length,
      insights: analysisData.insights.map((i) => i.text),
      file_name: analysisData.file_name,
      basic_info: {
        rows: analysisData.basic_info.rows,
        cols: analysisData.basic_info.cols,
        numeric_cols: analysisData.summary.numeric_cols,
        categorical_cols: analysisData.summary.categorical_cols,
        datetime_cols: analysisData.summary.datetime_cols,
        missing_fields: analysisData.summary.missing_fields,
        duplicates: analysisData.basic_info.duplicates,
      },
    };
  },
};
