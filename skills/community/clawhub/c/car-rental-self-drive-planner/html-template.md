# HTML 模板参考

生成 HTML 时使用此模板骨架。所有 `{占位符}` 在 Step 5 中动态填充。

## 完整模板

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{location} · {days}天租车自驾行前计划</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
      background: #f7fafc; color: #2d3748; line-height: 1.7;
    }

    /* Header */
    .header {
      background: linear-gradient(135deg, #1a365d, #2b6cb0);
      color: #fff; padding: 2.5rem 2rem; text-align: center;
    }
    .header h1 { font-size: 1.8rem; margin-bottom: 0.5rem; }
    .header .subtitle { opacity: 0.85; font-size: 0.95rem; }

    /* 合规提示条 */
    .compliance-bar {
      background: #fefcbf; color: #744210;
      text-align: center; padding: 0.6rem 1rem; font-size: 0.85rem; font-weight: 500;
    }

    /* 容器 */
    .container { max-width: 1100px; margin: 2rem auto; padding: 0 1.5rem; }

    /* 卡片网格 */
    .card-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(480px, 1fr));
      gap: 1.5rem;
    }

    /* 卡片通用 */
    .card {
      background: #fff; border-radius: 12px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.08); overflow: hidden;
    }
    .card-header {
      padding: 1rem 1.2rem; color: #fff;
      font-weight: 600; font-size: 1.05rem;
      display: flex; align-items: center; gap: 0.5rem;
    }
    .card-body { padding: 1.2rem 1.5rem; }

    /* 各卡片标题色 */
    .card-a .card-header { background: #38a169; }
    .card-b .card-header { background: #3182ce; }
    .card-c .card-header { background: #e53e3e; }
    .card-d .card-header { background: #805ad5; }

    /* Card A: 清单样式 */
    .checklist-group { margin-bottom: 1rem; }
    .checklist-group:last-child { margin-bottom: 0; }
    .checklist-group-title {
      font-weight: 600; font-size: 0.9rem; color: #2d3748;
      margin-bottom: 0.4rem; padding-bottom: 0.3rem;
      border-bottom: 2px solid #e2e8f0;
    }
    .checklist-item {
      padding: 0.35rem 0; padding-left: 1.5rem;
      position: relative; font-size: 0.9rem;
    }
    .checklist-item::before {
      content: "✅"; position: absolute; left: 0; top: 0.35rem; font-size: 0.8rem;
    }

    /* Card B: 注意事项 */
    .note-item {
      padding: 0.5rem 0; border-bottom: 1px solid #edf2f7;
      font-size: 0.9rem;
    }
    .note-item:last-child { border-bottom: none; }
    .note-item strong { color: #2b6cb0; }

    /* Card C: Do & Don't */
    .do-dont { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
    .do-section {
      background: #f0fff4; border-radius: 8px; padding: 1rem;
      border-left: 4px solid #38a169;
    }
    .dont-section {
      background: #fff5f5; border-radius: 8px; padding: 1rem;
      border-left: 4px solid #e53e3e;
    }
    .do-section h4 { color: #276749; margin-bottom: 0.5rem; }
    .dont-section h4 { color: #9b2c2c; margin-bottom: 0.5rem; }
    .do-item, .dont-item {
      padding: 0.3rem 0; padding-left: 1.4rem;
      position: relative; font-size: 0.9rem;
    }
    .do-item::before { content: "✔"; position: absolute; left: 0; color: #38a169; font-weight: bold; }
    .dont-item::before { content: "✘"; position: absolute; left: 0; color: #e53e3e; font-weight: bold; }

    /* Card D: 路线 */
    .route-block {
      border-left: 4px solid; padding: 1rem 1.2rem;
      margin-bottom: 1rem; border-radius: 0 8px 8px 0;
    }
    .route-block:last-child { margin-bottom: 0; }
    .route-block.route-1 { border-color: #805ad5; background: #faf5ff; }
    .route-block.route-2 { border-color: #dd6b20; background: #fffaf0; }
    .route-title { font-weight: 700; font-size: 1rem; margin-bottom: 0.3rem; }
    .route-block.route-1 .route-title { color: #553c9a; }
    .route-block.route-2 .route-title { color: #9c4221; }
    .route-meta {
      display: flex; gap: 0.8rem; flex-wrap: wrap;
      font-size: 0.8rem; color: #718096; margin: 0.5rem 0;
    }
    .route-meta span {
      background: #edf2f7; padding: 0.15rem 0.5rem; border-radius: 4px;
    }
    .route-days { margin: 0.5rem 0; font-size: 0.9rem; }
    .route-day { padding: 0.25rem 0; }
    .route-day strong { color: #4a5568; }
    .highlights {
      display: flex; flex-wrap: wrap; gap: 0.4rem; margin-top: 0.6rem;
    }
    .highlight-tag {
      padding: 0.15rem 0.55rem; border-radius: 12px; font-size: 0.78rem;
    }
    .route-block.route-1 .highlight-tag { background: #e9d8fd; color: #553c9a; }
    .route-block.route-2 .highlight-tag { background: #feebc8; color: #7b341e; }
    .route-compliance {
      margin-top: 0.5rem; font-size: 0.8rem;
      color: #718096; font-style: italic;
    }

    /* Footer */
    .footer {
      background: #edf2f7; text-align: center;
      padding: 1.5rem; margin-top: 2rem;
      font-size: 0.8rem; color: #718096; line-height: 1.8;
    }

    /* 响应式 */
    @media (max-width: 600px) {
      .card-grid { grid-template-columns: 1fr; }
      .do-dont { grid-template-columns: 1fr; }
      .header h1 { font-size: 1.4rem; }
    }
  </style>
</head>
<body>

  <!-- ====== Header ====== -->
  <div class="header">
    <h1>🚗 {location} · {days}天租车自驾行前计划</h1>
    <div class="subtitle">
      {experience_level_label} · {trip_type_label} · {drivers_label} · {style_preference_label}
    </div>
  </div>
  <div class="compliance-bar">⚠ 以当地交通法规与租车合同为准，本指南仅供参考</div>

  <div class="container">
    <div class="card-grid">

      <!-- ====== Card A: 行前准备清单 ====== -->
      <div class="card card-a">
        <div class="card-header">✅ 行前准备清单</div>
        <div class="card-body">
          <div class="checklist-group">
            <div class="checklist-group-title">📄 证件类</div>
            <div class="checklist-item">{证件项目1}</div>
            <div class="checklist-item">{证件项目2}</div>
            <!-- 根据location动态增减：国际驾照/翻译件等 -->
          </div>
          <div class="checklist-group">
            <div class="checklist-group-title">🛡 保险类</div>
            <div class="checklist-item">{保险项目1}</div>
            <div class="checklist-item">{保险项目2}</div>
          </div>
          <div class="checklist-group">
            <div class="checklist-group-title">📱 导航与通讯</div>
            <div class="checklist-item">{导航项目1}</div>
            <div class="checklist-item">{导航项目2}</div>
          </div>
          <div class="checklist-group">
            <div class="checklist-group-title">🚙 车辆与出行</div>
            <div class="checklist-item">{车辆项目1}</div>
            <div class="checklist-item">{车辆项目2}</div>
            <!-- 根据drivers/季节动态增减：儿童座椅、雪链等 -->
          </div>
        </div>
      </div>

      <!-- ====== Card B: 租车关键注意事项 ====== -->
      <div class="card card-b">
        <div class="card-header">📋 {location} 租车关键注意事项</div>
        <div class="card-body">
          <div class="note-item"><strong>{要点标题1}：</strong>{要点内容1}</div>
          <div class="note-item"><strong>{要点标题2}：</strong>{要点内容2}</div>
          <!-- 6-10条，涵盖驾照、路费、停车、油量、押金、事故、夜间风险等 -->
        </div>
      </div>

      <!-- ====== Card C: 安全驾驶与合规 ====== -->
      <div class="card card-c">
        <div class="card-header">🛡 安全驾驶与合规</div>
        <div class="card-body">
          <div class="do-dont">
            <div class="do-section">
              <h4>✔ Do</h4>
              <div class="do-item">{Do项1}</div>
              <div class="do-item">{Do项2}</div>
              <div class="do-item">{Do项3}</div>
              <!-- 3-5条 -->
            </div>
            <div class="dont-section">
              <h4>✘ Don't</h4>
              <div class="dont-item">{Don't项1}</div>
              <div class="dont-item">{Don't项2}</div>
              <div class="dont-item">{Don't项3}</div>
              <!-- 3-5条 -->
            </div>
          </div>
        </div>
      </div>

      <!-- ====== Card D: 推荐自驾路线 ====== -->
      <div class="card card-d">
        <div class="card-header">🗺 推荐自驾路线</div>
        <div class="card-body">

          <!-- 路线 1 -->
          <div class="route-block route-1">
            <div class="route-title">📍 {路线1标题，如"经典环线：南岛环线"}</div>
            <div class="route-meta">
              <span>📏 难度：{低/中/高}</span>
              <span>👥 适合：{人群标签}</span>
              <span>📍 起终点：{城市}</span>
            </div>
            <div class="route-days">
              <div class="route-day"><strong>Day 1-{n}：</strong>{天数分配摘要}</div>
              <div class="route-day"><strong>Day {n}-{m}：</strong>{天数分配摘要}</div>
              <!-- 按天分段，每段1-3行 -->
            </div>
            <div class="highlights">
              <span class="highlight-tag">{亮点1}</span>
              <span class="highlight-tag">{亮点2}</span>
              <span class="highlight-tag">{亮点3}</span>
              <!-- 3-6个亮点标签 -->
            </div>
            <div class="route-compliance">⚠ 仅推荐成熟景区与主干道，请以最新路况为准</div>
          </div>

          <!-- 路线 2（仅 trip_type=both 或 cross_region 时输出） -->
          <div class="route-block route-2">
            <div class="route-title">📍 {路线2标题，如"跨区域：xx至xx"}</div>
            <div class="route-meta">
              <span>📏 难度：{低/中/高}</span>
              <span>👥 适合：{人群标签}</span>
              <span>📍 起终点：{城市}</span>
            </div>
            <div class="route-days">
              <div class="route-day"><strong>Day 1-{n}：</strong>{天数分配摘要}</div>
              <div class="route-day"><strong>Day {n}-{m}：</strong>{天数分配摘要}</div>
            </div>
            <div class="highlights">
              <span class="highlight-tag">{亮点1}</span>
              <span class="highlight-tag">{亮点2}</span>
              <span class="highlight-tag">{亮点3}</span>
            </div>
            <div class="route-compliance">⚠ 仅推荐成熟景区与主干道，请以最新路况为准</div>
          </div>

        </div>
      </div>

    </div>
  </div>

  <!-- ====== Footer ====== -->
  <div class="footer">
    <p>📌 出发前请查看当地官方交通规则与租车合同</p>
    <p>🆘 紧急电话：{当地紧急号码，或"当地紧急号码（如 112 / 当地区号），以当地为准"}</p>
    <p>⏱ 路线与规则可能随时间更新，请以最新官方信息为准</p>
  </div>

</body>
</html>
```

## 占位符说明

| 占位符 | 来源 |
|--------|------|
| `{location}` | 用户输入 |
| `{days}` | 用户输入 |
| `{experience_level_label}` | 由 experience_level 映射：beginner→新手、intermediate→有经验、advanced→老司机 |
| `{trip_type_label}` | classic_loop→经典环线、cross_region→跨区域、both→环线+跨区域 |
| `{drivers_label}` | solo→独自出行、couple→情侣/双人、family→家庭、with_kids→带娃、mixed→混合 |
| `{style_preference_label}` | scenic→风景优先、city→城市探索、culture→人文深度、balanced→均衡体验 |
| `{证件/保险/导航/车辆项目}` | Step 3 根据 location 和 drivers 动态生成 |
| `{要点标题/内容}` | Step 3 生成的 6-10 条国家/地区差异 |
| `{Do/Don't 项}` | 通用合规 + 根据 location 适当补充 |
| `{路线标题/天数/亮点}` | Step 4 从路线模板生成 |
| `{当地紧急号码}` | 已知则填写，否则用泛化写法 |

## 注意事项

- 所有 `{占位符}` 必须在生成时被实际内容替换，最终 HTML 中不应出现花括号占位符
- Card D 中路线 2 的 `route-block route-2` 仅在 `trip_type=both` 或 `trip_type=cross_region` 时渲染
- 移动端通过 `@media (max-width: 600px)` 自动切换为单列布局
- Do/Don't 在窄屏下也切换为单列
