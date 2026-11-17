> **V7 兼容性说明**：本文件从 V6 完整继承。V7 保留所有 V6 能力，本文件内容完全有效。
> V7 新增 references 见 `references/edge-cloud-architecture.md` / `references/zero-upload-privacy.md` / `references/npu-scheduling-guide.md` / `references/edge-cloud-protocol.md` / `references/audit-report-v7.md`。
> 原始文件版本：V6 · 继承版本：V7 · 继承日期：2026-08-15

# 教学数据分析仪表盘

> V6 新增 · 能力八：教学数据分析与可视化

## 1. 概述

基于 Pandas + Plotly 的本地教学数据分析服务，支持成绩统计、学情诊断、可视化报表生成。

### 1.1 核心功能
- **成绩分析**：班级/个人成绩统计、排名、趋势、分布
- **学情诊断**：知识点掌握度、薄弱环节识别
- **可视化报表**：交互式图表、PDF 报告导出
- **预测预警**：基于历史数据的学习风险预警

## 2. 微服务设计

### 2.1 FastAPI 服务

```python
from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import io, base64, json

app = FastAPI(title="教学数据分析服务", version="1.0.0")

class AnalysisRequest(BaseModel):
    data: dict  # CSV/JSON 格式的成绩数据
    analysis_type: str  # "score_stats" | "knowledge_map" | "trend" | "warning"
    options: dict = {}

@app.post("/api/v1/analysis/analyze")
async def analyze(req: AnalysisRequest):
    df = pd.DataFrame(req.data)
    
    if req.analysis_type == "score_stats":
        return _score_statistics(df)
    elif req.analysis_type == "knowledge_map":
        return _knowledge_map(df)
    elif req.analysis_type == "trend":
        return _trend_analysis(df)
    elif req.analysis_type == "warning":
        return _warning_analysis(df)
    else:
        return {"error": f"Unknown analysis type: {req.analysis_type}"}

@app.post("/api/v1/analysis/chart")
async def generate_chart(req: AnalysisRequest):
    """生成交互式图表（Plotly HTML）"""
    df = pd.DataFrame(req.data)
    chart_type = req.options.get("chart_type", "bar")
    
    fig = _create_chart(df, chart_type, req.analysis_type)
    html = fig.to_html(include_plotlyjs='cdn', full_html=False)
    return {"chart_html": html}

@app.post("/api/v1/analysis/report")
async def generate_report(req: AnalysisRequest):
    """生成完整分析报告"""
    df = pd.DataFrame(req.data)
    report = {
        "summary": _generate_summary(df),
        "statistics": _score_statistics(df),
        "charts": [],
        "recommendations": _generate_recommendations(df)
    }
    return report

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "analysis"}
```

### 2.2 分析引擎

```python
def _score_statistics(df: pd.DataFrame) -> dict:
    """成绩统计分析"""
    stats = {}
    
    # 基础统计
    for col in df.select_dtypes(include='number').columns:
        stats[col] = {
            "mean": round(df[col].mean(), 2),
            "median": round(df[col].median(), 2),
            "std": round(df[col].std(), 2),
            "max": round(df[col].max(), 2),
            "min": round(df[col].min(), 2),
            "pass_rate": round((df[col] >= 60).mean() * 100, 1),
            "excellent_rate": round((df[col] >= 90).mean() * 100, 1),
        }
    
    # 分布统计
    if "score" in df.columns:
        stats["distribution"] = {
            "0-59": int((df["score"] < 60).sum()),
            "60-69": int(((df["score"] >= 60) & (df["score"] < 70)).sum()),
            "70-79": int(((df["score"] >= 70) & (df["score"] < 80)).sum()),
            "80-89": int(((df["score"] >= 80) & (df["score"] < 90)).sum()),
            "90-100": int((df["score"] >= 90).sum()),
        }
    
    return stats

def _knowledge_map(df: pd.DataFrame) -> dict:
    """知识点掌握度分析"""
    knowledge_cols = [c for c in df.columns if c.startswith("kp_")]
    
    if not knowledge_cols:
        return {"error": "未找到知识点列（需以 kp_ 开头）"}
    
    mastery = {}
    for col in knowledge_cols:
        kp_name = col.replace("kp_", "")
        mastery[kp_name] = {
            "avg_score": round(df[col].mean(), 2),
            "mastery_rate": round((df[col] >= 0.8).mean() * 100, 1),
            "weak_students": int((df[col] < 0.6).sum()),
        }
    
    # 识别薄弱知识点
    weak_points = sorted(mastery.items(), key=lambda x: x[1]["avg_score"])[:5]
    
    return {"mastery": mastery, "weak_points": weak_points}

def _warning_analysis(df: pd.DataFrame) -> dict:
    """学习风险预警"""
    warnings = []
    
    if "score" in df.columns:
        # 连续下滑
        if "exam_id" in df.columns:
            for student in df["student_id"].unique():
                student_scores = df[df["student_id"] == student].sort_values("exam_id")["score"]
                if len(student_scores) >= 3:
                    diffs = student_scores.diff().dropna()
                    if all(d < 0 for d in diffs[-3:]):
                        warnings.append({
                            "student_id": student,
                            "type": "连续下滑",
                            "severity": "high",
                            "detail": f"连续3次考试下滑，最新分数 {student_scores.iloc[-1]}"
                        })
        
        # 低分预警
        low_scores = df[df["score"] < 60]
        for _, row in low_scores.iterrows():
            warnings.append({
                "student_id": row.get("student_id", "unknown"),
                "type": "不及格",
                "severity": "medium",
                "detail": f"分数 {row['score']}，低于及格线"
            })
    
    return {"warnings": warnings, "total_at_risk": len(set(w["student_id"] for w in warnings))}
```

## 3. 可视化图表

### 3.1 图表类型

```python
def _create_chart(df, chart_type, analysis_type):
    """创建 Plotly 交互式图表"""
    
    if chart_type == "bar" and analysis_type == "score_stats":
        # 成绩分布柱状图
        fig = go.Figure(data=[
            go.Bar(
                x=['0-59', '60-69', '70-79', '80-89', '90-100'],
                y=[
                    (df["score"] < 60).sum(),
                    ((df["score"] >= 60) & (df["score"] < 70)).sum(),
                    ((df["score"] >= 70) & (df["score"] < 80)).sum(),
                    ((df["score"] >= 80) & (df["score"] < 90)).sum(),
                    (df["score"] >= 90).sum()
                ],
                marker_color=['#e74c3c', '#f39c12', '#f1c40f', '#2ecc71', '#27ae60']
            )
        ])
        fig.update_layout(title="成绩分布", xaxis_title="分数段", yaxis_title="人数")
        return fig
    
    elif chart_type == "radar" and analysis_type == "knowledge_map":
        # 知识点掌握雷达图
        knowledge_cols = [c for c in df.columns if c.startswith("kp_")]
        labels = [c.replace("kp_", "") for c in knowledge_cols]
        values = [df[c].mean() for c in knowledge_cols]
        
        fig = go.Figure(data=go.Scatterpolar(
            r=values + [values[0]],
            theta=labels + [labels[0]],
            fill='toself'
        ))
        fig.update_layout(title="知识点掌握度雷达图")
        return fig
    
    elif chart_type == "line" and analysis_type == "trend":
        # 成绩趋势折线图
        fig = go.Figure()
        for student in df["student_id"].unique()[:10]:  # 最多显示10人
            student_data = df[df["student_id"] == student].sort_values("exam_id")
            fig.add_trace(go.Scatter(
                x=student_data["exam_id"],
                y=student_data["score"],
                name=f"学生{student}",
                mode='lines+markers'
            ))
        fig.update_layout(title="成绩趋势", xaxis_title="考试", yaxis_title="分数")
        return fig
    
    elif chart_type == "heatmap":
        # 知识点关联热力图
        knowledge_cols = [c for c in df.columns if c.startswith("kp_")]
        corr = df[knowledge_cols].corr()
        labels = [c.replace("kp_", "") for c in knowledge_cols]
        
        fig = go.Figure(data=go.Heatmap(
            z=corr.values, x=labels, y=labels,
            colorscale='RdYlGn', zmid=0
        ))
        fig.update_layout(title="知识点关联矩阵")
        return fig
```

### 3.2 p5.js 集成

```javascript
// 在 p5.js 课件中嵌入数据分析图表
class DataAnalysisPanel {
  constructor(p5, containerId) {
    this.p5 = p5;
    this.container = document.getElementById(containerId);
    this.analysisUrl = 'http://localhost:8905/api/v1/analysis';
  }
  
  async loadAndAnalyze(csvData) {
    // 解析 CSV
    const data = this._parseCSV(csvData);
    
    // 调用分析服务
    const resp = await fetch(`${this.analysisUrl}/analyze`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ data, analysis_type: 'score_stats' })
    });
    const stats = await resp.json();
    
    // 渲染统计卡片
    this._renderStatsCards(stats);
    
    // 生成交互式图表
    const chartResp = await fetch(`${this.analysisUrl}/chart`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ data, analysis_type: 'score_stats', options: { chart_type: 'bar' } })
    });
    const chartData = await chartResp.json();
    
    // 嵌入图表
    const chartDiv = document.createElement('div');
    chartDiv.innerHTML = chartData.chart_html;
    this.container.appendChild(chartDiv);
    
    return stats;
  }
  
  _renderStatsCards(stats) {
    // 渲染统计摘要卡片
    Object.entries(stats).forEach(([key, val]) => {
      if (typeof val === 'object' && val.mean !== undefined) {
        const card = document.createElement('div');
        card.className = 'stat-card';
        card.innerHTML = `
          <h3>${key}</h3>
          <div class="stat-grid">
            <span>平均分: ${val.mean}</span>
            <span>及格率: ${val.pass_rate}%</span>
            <span>优秀率: ${val.excellent_rate}%</span>
          </div>
        `;
        this.container.appendChild(card);
      }
    });
  }
}
```

## 4. 教学场景

### 4.1 场景映射

| 场景 | 输入 | 分析类型 | 输出 |
|------|------|----------|------|
| 期中考试成绩分析 | Excel 成绩表 | score_stats + trend | 统计报告 + 趋势图 |
| 知识点薄弱诊断 | 答题数据 | knowledge_map | 雷达图 + 薄弱点列表 |
| 学习风险预警 | 多次考试成绩 | warning + trend | 预警名单 + 干预建议 |
| 班级对比分析 | 多班成绩 | score_stats | 对比柱状图 + 排名 |
| 学期总结报告 | 全学期数据 | 综合分析 | PDF 报告 + 图表集 |

### 4.2 报告模板

```python
REPORT_TEMPLATES = {
    "期中分析": {
        "sections": ["概览", "成绩分布", "排名", "进退步分析", "建议"],
        "charts": ["bar", "line", "box"],
    },
    "学情诊断": {
        "sections": ["知识点掌握度", "薄弱环节", "关联分析", "个性化建议"],
        "charts": ["radar", "heatmap", "bar"],
    },
    "学期总结": {
        "sections": ["整体概览", "趋势分析", "优秀表彰", "预警名单", "下学期建议"],
        "charts": ["line", "bar", "pie", "radar"],
    }
}
```

## 5. 质量门控

| 检查项 | 标准 | 验证方法 |
|--------|------|----------|
| 数据解析 | 支持 CSV/Excel/JSON | 格式测试 |
| 统计准确 | 与 Excel 计算结果一致 | 对比验证 |
| 图表渲染 | <2s 生成（1000 条数据） | 性能测试 |
| 大数据集 | 支持 10000+ 行 | 压力测试 |
| 报告完整 | 所有模板章节齐全 | 模板检查 |
| 隐私保护 | 学生数据不上传云端 | 安全审计 |
