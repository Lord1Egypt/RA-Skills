# 评估报告：HTML 生成规范

## 输出要求
评估信息足够后，必须生成一份**完整、自包含的 HTML 报告文件**（不依赖任何外部 CDN，雷达图用内联 SVG 绘制，可直接保存为 .html 在浏览器打开）。HTML 自上而下结构：

1. **顶部·雷达图**：5 维度（目标清晰度 / 身体与基础状态 / 饮食管理能力 / 运动与塑形能力 / 生活方式与执行力）的雷达图，**横向居中**。
2. **雷达图下方·一句话总结**：针对其瓶颈的总结判断。
3. **下方·五维进度条与分数**：每个维度一条进度条（宽度 = 得分÷20×100%）+ 分数（x/20），进度条下方一句说明。
4. **下方·待办事项**：2–3 条最重要下一步，关键内容用高亮（`<span class="hl">…</span>` 或 `<mark>`）标记。
5. **最下方·教练寄语**：一段温暖、有力量的收尾话。

> 知识库（来源 A/B）里的具体方法、数值与结论（蛋白质摄入量、训练频率、饮食配比、恢复要点等），应编织进「待办事项」与「教练寄语」中，并以高亮呈现关键数字——这是报告"具体怎么做"的部分。

### 雷达图绘制方法（内联 SVG，圆心 200,200，半径 150）
- 5 条轴线角度（从正上方顺时针）：维度1=−90°、维度2=−18°、维度3=54°、维度4=126°、维度5=198°。
- 网格五边形（100%）固定点：`200,50 342.66,153.65 288.17,321.35 111.83,321.35 57.34,153.65`（可叠加 75%/50%/25% 网格，见模板）。
- 数据点：对每个维度得分 `s`（0–20），该维顶点 = `x = 200 + 7.5·s·cosθ`、`y = 200 + 7.5·s·sinθ`，cos/sin 分别为：维度1(0,−1)、维度2(0.951,−0.309)、维度3(0.588,0.809)、维度4(−0.588,0.809)、维度5(−0.951,−0.309)。把 5 个顶点连成数据多边形 `<polygon>`，并在顶点画 `<circle>` 圆点，轴线末端放维度短标签。

### HTML 模板（将 {{占位}} 替换为真实内容；points 为上面算出的 5 顶点）
````html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>减脂塑形评估报告</title>
<style>
  body{font-family:-apple-system,"PingFang SC","Microsoft YaHei",sans-serif;background:#f5f7fa;color:#222;margin:0;padding:32px 16px;}
  .card{max-width:720px;margin:0 auto;background:#fff;border-radius:16px;box-shadow:0 8px 30px rgba(0,0,0,.08);padding:32px 28px;}
  h1{text-align:center;font-size:22px;margin:0 0 4px;}
  .sub{text-align:center;color:#8a94a6;font-size:13px;margin-bottom:24px;}
  .radar-wrap{display:flex;justify-content:center;margin:8px 0 20px;}
  .summary{text-align:center;font-size:16px;font-weight:600;line-height:1.6;background:#eef6ff;border-radius:12px;padding:16px;margin:0 0 24px;}
  .dim{margin-bottom:18px;}
  .dim-head{display:flex;justify-content:space-between;font-size:14px;margin-bottom:6px;}
  .dim-score{color:#2b7de9;font-weight:700;}
  .bar{height:12px;background:#eef0f3;border-radius:8px;overflow:hidden;}
  .bar-fill{height:100%;background:linear-gradient(90deg,#5eb3ff,#2b7de9);border-radius:8px;}
  .dim-exp{font-size:13px;color:#667;margin-top:6px;line-height:1.6;}
  .todos{margin-top:28px;}
  .todos h2{font-size:17px;margin:0 0 12px;}
  .todo{background:#fff7ed;border-left:4px solid #f59e0b;border-radius:8px;padding:12px 14px;margin-bottom:10px;font-size:14px;line-height:1.7;}
  .hl{background:#fff2c2;color:#7a4f01;font-weight:700;border-radius:3px;padding:0 3px;}
  .coach{margin-top:28px;padding:18px;border-radius:12px;background:linear-gradient(135deg,#1f2a44,#2b3a5e);color:#fff;font-size:14px;line-height:1.85;}
  .coach .t{font-weight:700;display:block;margin-bottom:6px;color:#ffd479;}
</style>
</head>
<body>
<div class="card">
  <h1>你的减脂塑形评估报告</h1>
  <div class="sub">基于你的专属评估 · 五维准备度评分 · 总分 {{total}}/100</div>
  <div class="radar-wrap">
    <svg width="400" height="400" viewBox="0 0 400 400">
      <polygon points="200,50 342.66,153.65 288.17,321.35 111.83,321.35 57.34,153.65" fill="none" stroke="#dfe5ee" stroke-width="1.5"/>
      <polygon points="200,87.5 306.99,165.24 266.15,291.01 133.85,291.01 93.01,165.24" fill="none" stroke="#eef0f3" stroke-width="1"/>
      <polygon points="200,125 271.33,176.82 244.1,260.68 155.9,260.68 128.67,176.82" fill="none" stroke="#eef0f3" stroke-width="1"/>
      <polygon points="200,162.5 235.66,188.41 222.05,230.34 177.95,230.34 164.34,188.41" fill="none" stroke="#eef0f3" stroke-width="1"/>
      <line x1="200" y1="200" x2="200" y2="50" stroke="#dfe5ee"/>
      <line x1="200" y1="200" x2="342.66" y2="153.65" stroke="#dfe5ee"/>
      <line x1="200" y1="200" x2="288.17" y2="321.35" stroke="#dfe5ee"/>
      <line x1="200" y1="200" x2="111.83" y2="321.35" stroke="#dfe5ee"/>
      <line x1="200" y1="200" x2="57.34" y2="153.65" stroke="#dfe5ee"/>
      <polygon points="{{points}}" fill="rgba(43,125,233,.25)" stroke="#2b7de9" stroke-width="2.5"/>
      <circle cx="{{c1x}}" cy="{{c1y}}" r="4" fill="#2b7de9"/>
      <circle cx="{{c2x}}" cy="{{c2y}}" r="4" fill="#2b7de9"/>
      <circle cx="{{c3x}}" cy="{{c3y}}" r="4" fill="#2b7de9"/>
      <circle cx="{{c4x}}" cy="{{c4y}}" r="4" fill="#2b7de9"/>
      <circle cx="{{c5x}}" cy="{{c5y}}" r="4" fill="#2b7de9"/>
      <text x="200" y="36" text-anchor="middle" font-size="13" fill="#445">目标</text>
      <text x="352" y="156" text-anchor="middle" font-size="13" fill="#445">身体</text>
      <text x="296" y="338" text-anchor="middle" font-size="13" fill="#445">饮食</text>
      <text x="104" y="338" text-anchor="middle" font-size="13" fill="#445">运动</text>
      <text x="48" y="156" text-anchor="middle" font-size="13" fill="#445">生活</text>
    </svg>
  </div>
  <div class="summary">{{summary}}</div>

  <div class="dim">
    <div class="dim-head"><span>① 目标清晰度</span><span class="dim-score">{{s1}}/20</span></div>
    <div class="bar"><div class="bar-fill" style="width:{{p1}}%"></div></div>
    <div class="dim-exp">{{e1}}</div>
  </div>
  <div class="dim">
    <div class="dim-head"><span>② 身体与基础状态</span><span class="dim-score">{{s2}}/20</span></div>
    <div class="bar"><div class="bar-fill" style="width:{{p2}}%"></div></div>
    <div class="dim-exp">{{e2}}</div>
  </div>
  <div class="dim">
    <div class="dim-head"><span>③ 饮食管理能力</span><span class="dim-score">{{s3}}/20</span></div>
    <div class="bar"><div class="bar-fill" style="width:{{p3}}%"></div></div>
    <div class="dim-exp">{{e3}}</div>
  </div>
  <div class="dim">
    <div class="dim-head"><span>④ 运动与塑形能力</span><span class="dim-score">{{s4}}/20</span></div>
    <div class="bar"><div class="bar-fill" style="width:{{p4}}%"></div></div>
    <div class="dim-exp">{{e4}}</div>
  </div>
  <div class="dim">
    <div class="dim-head"><span>⑤ 生活方式与执行力</span><span class="dim-score">{{s5}}/20</span></div>
    <div class="bar"><div class="bar-fill" style="width:{{p5}}%"></div></div>
    <div class="dim-exp">{{e5}}</div>
  </div>

  <div class="todos">
    <h2>接下来最重要的 3 件事</h2>
    <div class="todo">① {{t1}}</div>
    <div class="todo">② {{t2}}</div>
    <div class="todo">③ {{t3}}</div>
  </div>

  <div class="coach">
    <span class="t">教练寄语</span>
    {{coach}}
  </div>
</div>
</body>
</html>
````

### 占位说明
- `{{points}}`：5 个数据顶点 `x,y x,y x,y x,y x,y`（按维度1→5 顺序，用上方公式算出）；`{{c1x}}`~`{{c5y}}` 为对应顶点坐标（与 points 一致）。
- `{{p1}}`~`{{p5}}`：各维得分÷20×100（如 17/20→85）；`{{s1}}`~`{{s5}}`：原始分数；`{{total}}`：五维之和。
- `{{summary}}`：一句话总结；`{{e1}}`~`{{e5}}`：各维一句说明；`{{t1}}`~`{{t3}}`：待办（关键内容用 `<span class="hl">…</span>` 高亮）；`{{coach}}`：教练寄语。
- 输出时把整段 HTML 用 html 代码块呈现，并提示用户「复制保存为 .html 即可在浏览器查看」；若所在环境支持直接写文件，文件名建议为 `减脂塑形评估报告.html`。

**报告红线**：必须含一句话总结 + 五维评分 + 每项解释 + 总分 + 2–3 条待办 + 教练寄语；禁止长篇医学分析、堆术语、一次给十几个建议、无依据的"你代谢很差"、仅按体重判健康。

---

