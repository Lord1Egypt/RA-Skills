# HTML 输出格式模板

## 设计规范

### 主题配色

| 用途 | 颜色值 | 说明 |
|------|--------|------|
| 主色 | #0EA5E9 | 天蓝色，旅行主题 |
| 辅色 | #10B981 | 翠绿色，自然主题 |
| 强调 | #F59E0B | 橙黄色，高亮提醒 |
| 背景 | #F8FAFC | 浅灰白，页面底色 |
| 卡片背景 | #FFFFFF | 白色 |
| 文字主色 | #1E293B | 深灰蓝 |
| 文字辅色 | #64748B | 中灰 |
| 边框 | #E2E8F0 | 浅灰 |
| 飞机图标色 | #0EA5E9 | 与主色一致 |
| 高铁图标色 | #10B981 | 与辅色一致 |
| 自驾图标色 | #F59E0B | 与强调色一致 |

### 字体

- 标题：`-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif`
- 正文：同上，line-height: 1.6
- 数字/价格：`font-variant-numeric: tabular-nums`

### 响应式

- 桌面：max-width 960px，居中布局
- 移动端：100% width，卡片间距缩小，字体适当缩小

## HTML 结构

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{出发地} → {目的地} | 全能旅行规划师</title>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <style>
    /* 全局样式 */
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      background: #F8FAFC;
      color: #1E293B;
      line-height: 1.6;
      padding: 20px;
    }
    .container { max-width: 960px; margin: 0 auto; }

    /* 头部概览 */
    .overview-card {
      background: linear-gradient(135deg, #0EA5E9 0%, #10B981 100%);
      color: white;
      border-radius: 16px;
      padding: 32px;
      margin-bottom: 24px;
      position: relative;
      overflow: hidden;
    }
    .overview-card h1 { font-size: 28px; margin-bottom: 8px; }
    .overview-meta {
      display: flex; gap: 16px; flex-wrap: wrap;
      font-size: 15px; opacity: 0.9;
    }
    .overview-meta span {
      background: rgba(255,255,255,0.2);
      padding: 4px 12px; border-radius: 8px;
    }
    .overview-budget {
      margin-top: 16px;
      display: flex; gap: 24px;
    }
    .budget-item {
      background: rgba(255,255,255,0.15);
      padding: 12px 20px; border-radius: 12px;
    }
    .budget-item .label { font-size: 13px; opacity: 0.8; }
    .budget-item .value { font-size: 22px; font-weight: 700; }

    /* 通用卡片 */
    .card {
      background: #FFFFFF;
      border: 1px solid #E2E8F0;
      border-radius: 12px;
      padding: 24px;
      margin-bottom: 20px;
    }
    .card-title {
      font-size: 18px; font-weight: 700;
      margin-bottom: 16px;
      display: flex; align-items: center; gap: 8px;
    }
    .card-title .icon { font-size: 22px; }

    /* 折叠面板 */
    .collapsible {
      border: 1px solid #E2E8F0;
      border-radius: 12px;
      margin-bottom: 12px;
      overflow: hidden;
    }
    .collapsible-header {
      background: #FFFFFF;
      padding: 16px 20px;
      cursor: pointer;
      display: flex; justify-content: space-between; align-items: center;
      font-weight: 600; font-size: 16px;
      user-select: none;
    }
    .collapsible-header:hover { background: #F1F5F9; }
    .collapsible-header .arrow {
      transition: transform 0.3s;
      font-size: 14px; color: #64748B;
    }
    .collapsible-header.active .arrow { transform: rotate(180deg); }
    .collapsible-body {
      padding: 20px;
      border-top: 1px solid #E2E8F0;
      display: none;
    }
    .collapsible-body.active { display: block; }

    /* 交通方案卡片 */
    .transport-card {
      border-left: 4px solid;
      border-radius: 12px;
      margin-bottom: 12px;
      overflow: hidden;
    }
    .transport-card.flight { border-left-color: #0EA5E9; }
    .transport-card.train { border-left-color: #10B981; }
    .transport-card.car { border-left-color: #F59E0B; }
    .transport-header {
      padding: 16px 20px;
      display: flex; align-items: center; gap: 12px;
      background: #FFFFFF;
    }
    .transport-header .emoji { font-size: 24px; }
    .transport-header .title { font-weight: 700; font-size: 17px; }
    .transport-header .tag {
      padding: 3px 10px; border-radius: 6px;
      font-size: 12px; font-weight: 600;
    }
    .transport-card.flight .tag { background: #E0F2FE; color: #0EA5E9; }
    .transport-card.train .tag { background: #D1FAE5; color: #10B981; }
    .transport-card.car .tag { background: #FEF3C7; color: #F59E0B; }
    .transport-body { padding: 20px; background: #F8FAFC; }

    /* 航班时间表 */
    .flight-table {
      width: 100%; border-collapse: collapse;
      font-size: 14px;
    }
    .flight-table th {
      background: #F1F5F9; padding: 10px 12px;
      text-align: left; font-weight: 600;
      border-bottom: 2px solid #E2E8F0;
    }
    .flight-table td {
      padding: 10px 12px; border-bottom: 1px solid #E2E8F0;
    }
    .flight-table .price { font-weight: 700; color: #0EA5E9; }
    .flight-table .recommended { background: #EFF6FF; }
    .flight-table .stars { color: #F59E0B; }

    /* 行程时间线 */
    .timeline {
      display: flex; gap: 16px;
      overflow-x: auto; padding-bottom: 8px;
      scrollbar-width: thin;
    }
    .timeline-day {
      min-width: 180px; flex-shrink: 0;
      background: #FFFFFF;
      border: 1px solid #E2E8F0;
      border-radius: 12px;
      padding: 16px;
      position: relative;
    }
    .timeline-day .day-label {
      font-weight: 700; font-size: 14px;
      color: #0EA5E9; margin-bottom: 8px;
    }
    .timeline-day .activity {
      font-size: 13px; color: #64748B;
      padding: 4px 0;
    }
    .timeline-day .activity .time {
      font-weight: 600; color: #1E293B;
    }

    /* 每日行程详情 */
    .day-detail { margin-bottom: 24px; }
    .day-header {
      background: linear-gradient(135deg, #0EA5E9, #38BDF8);
      color: white;
      padding: 12px 20px; border-radius: 10px;
      font-weight: 700; font-size: 16px;
      margin-bottom: 16px;
    }
    .time-block {
      display: flex; gap: 12px;
      margin-bottom: 16px;
      padding: 12px;
      background: #F8FAFC;
      border-radius: 8px;
    }
    .time-label {
      min-width: 60px; font-weight: 700;
      font-size: 13px; color: #0EA5E9;
      padding-top: 2px;
    }
    .time-content { font-size: 14px; }
    .time-content .name { font-weight: 600; }
    .time-content .meta { color: #64748B; font-size: 13px; }
    .spot-tag {
      display: inline-block;
      padding: 2px 8px; border-radius: 4px;
      font-size: 12px; margin: 2px;
    }
    .spot-tag.hot { background: #FEF3C7; color: #92400E; }
    .spot-tag.quiet { background: #D1FAE5; color: #065F46; }
    .spot-tag.project { background: #E0F2FE; color: #075985; }

    /* 美食卡片 */
    .food-card {
      background: #FFFFFF;
      border: 1px solid #E2E8F0;
      border-radius: 10px;
      padding: 16px;
      margin-bottom: 12px;
    }
    .food-card .restaurant-name { font-weight: 700; font-size: 16px; }
    .food-card .rating {
      display: inline-block;
      background: #FEF3C7; padding: 2px 8px;
      border-radius: 4px; font-weight: 600;
      font-size: 13px; color: #92400E;
    }
    .food-card .dish {
      display: inline-block;
      background: #D1FAE5; padding: 3px 10px;
      border-radius: 6px; font-size: 13px;
      margin: 4px 2px; color: #065F46;
    }
    .food-card .dish.must { background: #FEE2E2; color: #991B1B; }

    /* 住宿卡片 */
    .hotel-card {
      background: #FFFFFF;
      border: 1px solid #E2E8F0;
      border-radius: 10px;
      padding: 16px;
      margin-bottom: 12px;
    }
    .hotel-card .name { font-weight: 700; font-size: 16px; }
    .hotel-card .price-trend {
      display: flex; gap: 12px; margin-top: 8px;
    }
    .price-tag {
      padding: 4px 12px; border-radius: 6px;
      font-size: 13px; font-weight: 600;
    }
    .price-tag.low { background: #D1FAE5; color: #065F46; }
    .price-tag.high { background: #FEE2E2; color: #991B1B; }
    .price-tag.holiday { background: #FEF3C7; color: #92400E; }

    /* 天气卡片 */
    .weather-card {
      display: flex; gap: 20px; flex-wrap: wrap;
    }
    .weather-stat {
      text-align: center;
      padding: 16px;
      background: #F1F5F9;
      border-radius: 10px;
      min-width: 120px;
    }
    .weather-stat .icon { font-size: 24px; }
    .weather-stat .value { font-size: 20px; font-weight: 700; }
    .weather-stat .label { font-size: 13px; color: #64748B; }

    /* 行前清单 */
    .checklist {
      display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 16px;
    }
    .checklist-category {
      background: #F8FAFC;
      border: 1px solid #E2E8F0;
      border-radius: 10px;
      padding: 16px;
    }
    .checklist-category h4 {
      font-size: 15px; font-weight: 700;
      margin-bottom: 8px;
      display: flex; align-items: center; gap: 6px;
    }
    .checklist-category li {
      font-size: 14px; padding: 4px 0;
      list-style: none;
      display: flex; align-items: center; gap: 8px;
    }
    .checklist-category li::before {
      content: '☐'; color: #94A3B8; font-size: 16px;
    }

    /* Tips 卡片 */
    .tip-item {
      padding: 12px 0;
      border-bottom: 1px solid #F1F5F9;
    }
    .tip-item:last-child { border-bottom: none; }
    .tip-item .tip-title { font-weight: 600; font-size: 14px; }
    .tip-item .tip-desc { font-size: 13px; color: #64748B; }

    /* 预算饼图容器 */
    .chart-container {
      max-width: 360px;
      margin: 0 auto;
    }

    /* 底部 */
    .footer {
      text-align: center;
      padding: 24px;
      color: #94A3B8;
      font-size: 13px;
    }
  </style>
</head>
<body>
  <div class="container">

    <!-- 1. 方案概览 -->
    <div class="overview-card">
      <h1>{出发地} → {目的地}</h1>
      <div class="overview-meta">
        <span>📅 {天数}天</span>
        <span>👥 {人数}人 · {人群类型}</span>
        <span>🚗 {交通方式}</span>
        <span>🌤 {出行月份/日期}</span>
      </div>
      <div class="overview-budget">
        <div class="budget-item">
          <div class="label">总预算</div>
          <div class="value">¥{总预算}</div>
        </div>
        <div class="budget-item">
          <div class="label">人均预算</div>
          <div class="value">¥{人均预算}</div>
        </div>
      </div>
    </div>

    <!-- 2. 城际交通方案 -->
    <div class="card">
      <div class="card-title"><span class="icon">🚀</span> 城际交通方案</div>

      <!-- 飞机方案 -->
      <div class="transport-card flight">
        <div class="transport-header">
          <span class="emoji">✈️</span>
          <span class="title">{出发地} → {目的地}</span>
          <span class="tag">飞机</span>
        </div>
        <div class="transport-body">
          <table class="flight-table">
            <thead>
              <tr><th>时间段</th><th>航班示例</th><th>票价</th><th>推荐</th><th>说明</th></tr>
            </thead>
            <tbody>
              <tr><td>早班 06-09点</td><td>{航班号} {时间}</td><td class="price">¥{价格}</td><td class="stars">★★★★</td><td>价格最优</td></tr>
              <tr class="recommended"><td>午班 09-14点</td><td>{航班号} {时间}</td><td class="price">¥{价格}</td><td class="stars">★★★★★</td><td>性价比最佳</td></tr>
              <tr><td>晚班 18-22点</td><td>{航班号} {时间}</td><td class="price">¥{价格}</td><td class="stars">★★★</td><td>价格偏高</td></tr>
            </tbody>
          </table>
          <p style="margin-top:12px; font-size:14px;">
            <strong>✅ 推荐选择</strong>：{最优时间段}，理由：{理由}<br>
            <strong>💡 购票建议</strong>：提前{X}天，关注{航司/平台}特价<br>
            <strong>🔄 返程</strong>：{目的地} → {出发地}，{返程推荐}
          </p>
          <p style="margin-top:8px; font-size:13px; color:#64748B;">
            🚕 机场交通：出发 {方式}约{时间}¥{费用} | 到达 {方式}约{时间}¥{费用}
          </p>
        </div>
      </div>

      <!-- 高铁方案（如有） -->
      <div class="transport-card train">
        <!-- 同上结构，改 emoji 为 🚄，tag 改为 高铁 -->
      </div>

      <!-- 自驾方案（如有） -->
      <div class="transport-card car">
        <!-- 同上结构，改 emoji 为 🚗，tag 改为 自驾 -->
      </div>
    </div>

    <!-- 3. 历史天气 -->
    <div class="card">
      <div class="card-title"><span class="icon">🌤</span> 历史天气参考</div>
      <div class="weather-card">
        <div class="weather-stat">
          <div class="icon">🌡</div>
          <div class="value">{最低}~{最高}°C</div>
          <div class="label">日均气温</div>
        </div>
        <div class="weather-stat">
          <div class="icon">🌧</div>
          <div class="value">{X}%</div>
          <div class="label">降水概率</div>
        </div>
        <div class="weather-stat">
          <div class="icon">☀️</div>
          <div class="value">{X}%</div>
          <div class="label">晴天比例</div>
        </div>
        <div class="weather-stat">
          <div class="icon">👕</div>
          <div class="value">{穿衣方案}</div>
          <div class="label">穿衣建议</div>
        </div>
      </div>
      <p style="margin-top:12px; font-size:14px; color:#64748B;">
        ⚠️ {防晒/防雨/保暖提醒}
      </p>
    </div>

    <!-- 4. 预算分配 -->
    <div class="card">
      <div class="card-title"><span class="icon">💰</span> 预算分配</div>
      <div class="chart-container">
        <canvas id="budgetChart"></canvas>
      </div>
      <table style="width:100%; border-collapse:collapse; margin-top:16px; font-size:14px;">
        <thead><tr style="background:#F1F5F9;">
          <th style="padding:8px 12px; text-align:left;">板块</th>
          <th style="padding:8px 12px; text-align:left;">金额</th>
          <th style="padding:8px 12px; text-align:left;">比例</th>
        </tr></thead>
        <tbody>
          <!-- 每行一个板块：城际交通 / 住宿 / 餐饮 / 当地交通 / 游玩 / 弹性 -->
        </tbody>
      </table>
    </div>

    <!-- 5. 住宿价格趋势 -->
    <div class="card">
      <div class="card-title"><span class="icon">🏨</span> 住宿价格趋势</div>
      <div style="display:flex; gap:12px; flex-wrap:wrap;">
        <span class="price-tag low">淡季 ¥{价格范围}/晚 ({月份})</span>
        <span class="price-tag high">旺季 ¥{价格范围}/晚 (+{X}%)</span>
        <span class="price-tag holiday">节假日 ¥{价格范围}/晚 (+{X}%)</span>
      </div>
      <p style="margin-top:12px; font-size:14px;">
        💡 最佳预订时机：提前{X}周，建议{平台}比价
      </p>
    </div>

    <!-- 6. 行程时间线 -->
    <div class="card">
      <div class="card-title"><span class="icon">📍</span> 行程概览</div>
      <div class="timeline">
        <!-- 每天一个卡片 -->
        <div class="timeline-day">
          <div class="day-label">Day 1</div>
          <div class="activity"><span class="time">上午</span> {景点}</div>
          <div class="activity"><span class="time">下午</span> {景点}</div>
          <div class="activity"><span class="time">晚上</span> {活动}</div>
        </div>
        <!-- Day 2... Day N 重复 -->
      </div>
    </div>

    <!-- 7. 每日行程详情（折叠面板） -->
    <div class="card">
      <div class="card-title"><span class="icon">🗓</span> 每日行程详情</div>
      <!-- 每天一个折叠面板 -->
      <div class="collapsible">
        <div class="collapsible-header" onclick="togglePanel(this)">
          Day 1 — {标题概述}
          <span class="arrow">▼</span>
        </div>
        <div class="collapsible-body">
          <div class="time-block">
            <div class="time-label">上午</div>
            <div class="time-content">
              <div class="name">📍 {景点名称}</div>
              <div class="meta">开放 {时间} · 游览 {X}小时 · 门票 ¥{价格}</div>
              <div>
                <span class="spot-tag project">游玩: {项目}(¥{价格})</span>
                <span class="spot-tag hot">打卡: {网红点} ⏰{最佳时间}</span>
                <span class="spot-tag quiet">打卡: {安静点} 🌿</span>
              </div>
            </div>
          </div>
          <div class="time-block">
            <div class="time-label">午餐</div>
            <div class="time-content">
              <div class="name">🍽 {餐厅名称}</div>
              <div class="meta">大众点评 {评分}分 · 人均 ¥{价格}</div>
              <div><span class="dish must">🥇{推荐菜1}</span> <span class="dish">🥈{推荐菜2}</span></div>
            </div>
          </div>
          <div class="time-block">
            <div class="time-label">下午</div>
            <!-- 同上午结构 -->
          </div>
          <div class="time-block">
            <div class="time-label">晚餐</div>
            <!-- 同午餐结构 -->
          </div>
          <div class="time-block">
            <div class="time-label">住宿</div>
            <div class="time-content">
              <div class="name">🏨 {酒店/民宿名称}</div>
              <div class="meta">¥{价格}/晚 · {特色}</div>
            </div>
          </div>
        </div>
      </div>
      <!-- Day 2... Day N 重复同样的折叠面板 -->
    </div>

    <!-- 8. 美食专题 -->
    <div class="card">
      <div class="card-title"><span class="icon">🍜</span> 美食专题</div>
      <div style="margin-bottom:12px; font-size:15px; font-weight:600;">
        🔥 必吃清单：{特色菜1} / {特色菜2} / {特色菜3}
      </div>
      <!-- 每家餐厅一个美食卡片 -->
      <div class="food-card">
        <div class="restaurant-name">🍽 {餐厅名称}</div>
        <span class="rating">大众点评 {评分}分</span>
        <span style="margin-left:8px; font-size:14px; color:#64748B;">人均 ¥{价格}</span>
        <div style="margin-top:8px;">
          <span class="dish must">🥇{推荐菜1}</span>
          <span class="dish">🥈{推荐菜2}</span>
          <span class="dish">🥉{推荐菜3}</span>
        </div>
        <div style="font-size:13px; color:#64748B; margin-top:4px;">
          📍 {位置} · ⚠️ {排队/预约提示}
        </div>
      </div>
      <!-- 更多餐厅... -->
    </div>

    <!-- 9. 住宿专题 -->
    <div class="card">
      <div class="card-title"><span class="icon">🛏</span> 住宿专题</div>
      <div class="hotel-card">
        <div class="name">🏨 {酒店/民宿名称}</div>
        <div style="font-size:14px; color:#64748B;">{区域} · {特色} · {评分}</div>
        <div class="price-trend">
          <span class="price-tag low">淡季 ¥{价格}/晚</span>
          <span class="price-tag high">旺季 ¥{价格}/晚</span>
        </div>
      </div>
      <!-- 更多酒店... -->
    </div>

    <!-- 10. 景点打卡专题 -->
    <div class="card">
      <div class="card-title"><span class="icon">📸</span> 景点打卡专题</div>
      <table style="width:100%; border-collapse:collapse; font-size:14px;">
        <thead><tr style="background:#F1F5F9;">
          <th style="padding:8px 12px; text-align:left;">景点</th>
          <th style="padding:8px 12px; text-align:left;">打卡点</th>
          <th style="padding:8px 12px; text-align:left;">游玩项目</th>
          <th style="padding:8px 12px; text-align:left;">最佳时间</th>
        </tr></thead>
        <tbody>
          <tr>
            <td style="padding:8px 12px;">{景点名}</td>
            <td style="padding:8px 12px;">{打卡点1} / {打卡点2}</td>
            <td style="padding:8px 12px;">{项目1}(¥{价格}) / {项目2}</td>
            <td style="padding:8px 12px;">{时间}</td>
          </tr>
          <!-- 更多景点... -->
        </tbody>
      </table>
    </div>

    <!-- 11. 当地交通指南 -->
    <div class="card">
      <div class="card-title"><span class="icon">🚌</span> 当地交通指南</div>
      <div style="font-size:14px;">
        <!-- 交通方式列表 -->
      </div>
    </div>

    <!-- 12. 实用Tips -->
    <div class="card">
      <div class="card-title"><span class="icon">💡</span> 实用Tips</div>
      <div class="tip-item">
        <div class="tip-title">⚠️ {注意事项标题}</div>
        <div class="tip-desc">{详细说明}</div>
      </div>
      <!-- 更多 tips... -->
    </div>

    <!-- 13. 备选方案 -->
    <div class="collapsible">
      <div class="collapsible-header" onclick="togglePanel(this)">
        🔄 备选方案（雨天/航班取消/体力不足）
        <span class="arrow">▼</span>
      </div>
      <div class="collapsible-body">
        <!-- 备选方案内容 -->
      </div>
    </div>

    <!-- 14. 行前清单 -->
    <div class="card">
      <div class="card-title"><span class="icon">🎒</span> 行前清单</div>
      <div class="checklist">
        <div class="checklist-category">
          <h4>📦 行李</h4>
          <ul>
            <li>{物品1}</li>
            <li>{物品2}</li>
            <!-- 更多... -->
          </ul>
        </div>
        <div class="checklist-category">
          <h4>📋 证件</h4>
          <ul>
            <li>{证件1}</li>
            <li>{证件2}</li>
          </ul>
        </div>
        <div class="checklist-category">
          <h4>🔔 预约</h4>
          <ul>
            <li>{预约1}</li>
            <li>{预约2}</li>
          </ul>
        </div>
        <div class="checklist-category">
          <h4>🎫 航班/车次</h4>
          <ul>
            <li>出发: {航班号} {时间}</li>
            <li>返程: {航班号} {时间}</li>
          </ul>
        </div>
      </div>
    </div>

    <div class="footer">
      全能旅行规划师 · {生成日期}
    </div>

  </div>

  <script>
    // 折叠面板交互
    function togglePanel(header) {
      header.classList.toggle('active');
      const body = header.nextElementSibling;
      body.classList.toggle('active');
    }

    // 预算饼图
    const ctx = document.getElementById('budgetChart').getContext('2d');
    new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: ['城际交通', '住宿', '餐饮', '当地交通', '游玩', '弹性'],
        datasets: [{
          data: [/* 各板块金额 */],
          backgroundColor: ['#0EA5E9', '#10B981', '#F59E0B', '#8B5CF6', '#EC4899', '#94A3B8'],
          borderWidth: 2,
          borderColor: '#FFFFFF'
        }]
      },
      options: {
        responsive: true,
        plugins: {
          legend: { position: 'bottom', labels: { padding: 16, font: { size: 13 } } },
          tooltip: {
            callbacks: {
              label: function(context) {
                const value = context.parsed;
                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                const percent = Math.round(value / total * 100);
                return `¥${value} (${percent}%)`;
              }
            }
          }
        }
      }
    });

    // 默认展开第一个每日行程面板
    document.querySelector('.collapsible-header')?.classList.add('active');
    document.querySelector('.collapsible-body')?.classList.add('active');
  </script>
</body>
</html>
```

## 使用说明

1. **数据填充**：将模板中所有 `{变量}` 替换为实际搜集的数据
2. **条件渲染**：只保留用户选择的交通方式对应卡片（飞机/高铁/自驾），删除不需要的
3. **天数循环**：行程时间线和每日详情面板按实际天数重复生成 Day 1 ~ Day N
4. **餐厅/酒店**：按实际推荐数量生成对应卡片，建议 3-5 家餐厅、3-4 家住宿
5. **预算饼图数据**：将各板块实际金额填入 Chart.js 的 `data` 数组
6. **文件保存**：保存为 `{出发地}-{目的地}-旅行方案.html`，使用 present_files 展示
7. **折叠默认状态**：第一个每日行程面板默认展开，其余折叠

## 注意事项

- Chart.js 通过 CDN 加载，需联网查看饼图；离线时饼图不显示但其余内容正常
- 所有 CSS/JS 内联在单个 HTML 文件中，无外部文件依赖
- 不使用任何付费 API 或需要密钥的服务
- 价格标注遵循中国惯例（¥ 人民币，涨红跌绿）
- 移动端适配：卡片布局自动响应，时间线横向可滚动
