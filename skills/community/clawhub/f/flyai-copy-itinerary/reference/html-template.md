# HTML 可视化攻略模板

本文档定义了攻略 HTML 文件的标准模板。

## 目录

1. [完整 HTML 模板](#完整-html-模板)
2. [样式说明](#样式说明)
3. [组件说明](#组件说明)
4. [使用方法](#使用方法)

---

## 完整 HTML 模板

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{目的地}}攻略 | {{出发城市}}出发 {{日期区间}}</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      min-height: 100vh;
      padding: 20px;
    }
    
    .container {
      max-width: 800px;
      margin: 0 auto;
      background: #fff;
      border-radius: 20px;
      box-shadow: 0 20px 60px rgba(0,0,0,0.3);
      overflow: hidden;
    }
    
    /* 头部区域 */
    .header {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
      padding: 40px 30px;
      text-align: center;
    }
    
    .header h1 {
      font-size: 2.5em;
      margin-bottom: 10px;
      text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    .header .meta {
      font-size: 1.1em;
      opacity: 0.9;
    }
    
    .header .source {
      margin-top: 15px;
      font-size: 0.9em;
      opacity: 0.7;
    }
    
    /* 快速信息卡片 */
    .quick-info {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 0;
      background: #f8f9fa;
      border-bottom: 1px solid #eee;
    }
    
    .quick-info .item {
      padding: 20px;
      text-align: center;
      border-right: 1px solid #eee;
    }
    
    .quick-info .item:last-child { border-right: none; }
    
    .quick-info .icon { font-size: 1.5em; margin-bottom: 5px; }
    .quick-info .label { font-size: 0.8em; color: #666; }
    .quick-info .value { font-size: 1.1em; font-weight: 600; color: #333; }
    
    /* 主体内容 */
    .content { padding: 30px; }
    
    /* 交通卡片 */
    .transport-card {
      background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
      border-radius: 15px;
      padding: 25px;
      color: white;
      margin-bottom: 30px;
    }
    
    .transport-card h2 {
      font-size: 1.3em;
      margin-bottom: 20px;
      display: flex;
      align-items: center;
      gap: 10px;
    }
    
    .flight-item {
      background: rgba(255,255,255,0.2);
      border-radius: 10px;
      padding: 15px;
      margin-bottom: 10px;
    }
    
    .flight-item:last-child { margin-bottom: 0; }
    
    .flight-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    
    .flight-info { flex: 1; }
    .flight-no { font-weight: 600; font-size: 1.1em; }
    .flight-time { font-size: 0.9em; opacity: 0.9; }
    .flight-price { font-size: 1.3em; font-weight: 700; }
    
    .transport-total {
      margin-top: 15px;
      padding-top: 15px;
      border-top: 1px solid rgba(255,255,255,0.3);
      text-align: right;
      font-size: 1.2em;
    }
    
    /* 每日行程 */
    .day-card {
      background: #fff;
      border: 1px solid #eee;
      border-radius: 15px;
      margin-bottom: 25px;
      overflow: hidden;
      box-shadow: 0 5px 15px rgba(0,0,0,0.05);
    }
    
    .day-header {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
      padding: 15px 20px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    
    .day-header h3 { font-size: 1.2em; }
    .day-theme { opacity: 0.9; font-size: 0.95em; }
    
    .day-content { padding: 20px; }
    
    .timeline-item {
      display: flex;
      gap: 15px;
      margin-bottom: 20px;
      position: relative;
    }
    
    .timeline-item:last-child { margin-bottom: 0; }
    
    .timeline-item::before {
      content: '';
      position: absolute;
      left: 35px;
      top: 30px;
      bottom: -20px;
      width: 2px;
      background: #eee;
    }
    
    .timeline-item:last-child::before { display: none; }
    
    .time-badge {
      width: 70px;
      flex-shrink: 0;
      text-align: center;
    }
    
    .time-badge .time {
      background: #667eea;
      color: white;
      padding: 5px 10px;
      border-radius: 20px;
      font-size: 0.85em;
      font-weight: 600;
    }
    
    .timeline-content {
      flex: 1;
      background: #f8f9fa;
      border-radius: 10px;
      padding: 15px;
    }
    
    .timeline-content h4 {
      font-size: 1em;
      margin-bottom: 8px;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    
    .timeline-content p {
      font-size: 0.9em;
      color: #666;
      line-height: 1.6;
    }
    
    /* 酒店卡片 */
    .hotel-card {
      background: #fff;
      border: 2px solid #667eea;
      border-radius: 12px;
      padding: 15px;
      margin-top: 10px;
    }
    
    .hotel-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 10px;
    }
    
    .hotel-name { font-weight: 600; color: #333; }
    .hotel-price { color: #e74c3c; font-weight: 700; font-size: 1.1em; }
    
    .hotel-meta {
      display: flex;
      gap: 15px;
      font-size: 0.85em;
      color: #666;
    }
    
    .hotel-link {
      display: inline-block;
      margin-top: 10px;
      background: #667eea;
      color: white;
      padding: 8px 15px;
      border-radius: 20px;
      text-decoration: none;
      font-size: 0.85em;
      transition: transform 0.2s;
    }
    
    .hotel-link:hover { transform: scale(1.05); }
    
    /* 状态标签 */
    .status {
      display: inline-block;
      padding: 3px 10px;
      border-radius: 10px;
      font-size: 0.8em;
      font-weight: 600;
    }
    
    .status-ok { background: #d4edda; color: #155724; }
    .status-warn { background: #fff3cd; color: #856404; }
    .status-error { background: #f8d7da; color: #721c24; }
    .status-info { background: #d1ecf1; color: #0c5460; }
    
    /* 费用总览 */
    .budget-card {
      background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
      border-radius: 15px;
      padding: 25px;
      color: white;
      margin: 30px 0;
    }
    
    .budget-card h2 {
      font-size: 1.3em;
      margin-bottom: 20px;
      display: flex;
      align-items: center;
      gap: 10px;
    }
    
    .budget-table {
      width: 100%;
      border-collapse: collapse;
    }
    
    .budget-table td {
      padding: 12px 0;
      border-bottom: 1px solid rgba(255,255,255,0.2);
    }
    
    .budget-table tr:last-child td { border-bottom: none; }
    
    .budget-table .item { opacity: 0.9; }
    .budget-table .amount { text-align: right; font-weight: 600; }
    .budget-table .note { text-align: right; font-size: 0.85em; opacity: 0.8; }
    
    .budget-total {
      margin-top: 15px;
      padding-top: 15px;
      border-top: 2px solid rgba(255,255,255,0.3);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    
    .budget-total .label { font-size: 1.2em; }
    .budget-total .value { font-size: 1.8em; font-weight: 700; }
    .budget-total .per-person { font-size: 0.9em; opacity: 0.9; }
    
    /* 差异对比 */
    .diff-card {
      background: #f8f9fa;
      border-radius: 15px;
      padding: 25px;
      margin: 30px 0;
    }
    
    .diff-card h2 {
      font-size: 1.2em;
      margin-bottom: 20px;
      color: #333;
    }
    
    .diff-table {
      width: 100%;
      border-collapse: collapse;
    }
    
    .diff-table th {
      background: #667eea;
      color: white;
      padding: 12px;
      text-align: left;
    }
    
    .diff-table td {
      padding: 12px;
      border-bottom: 1px solid #eee;
      vertical-align: top;
    }
    
    .diff-table tr:nth-child(even) { background: #fff; }
    
    .original { color: #666; }
    .adapted { color: #333; font-weight: 500; }
    
    /* 小贴士 */
    .tips-card {
      background: #fff3cd;
      border-radius: 15px;
      padding: 25px;
      margin: 30px 0;
    }
    
    .tips-card h2 {
      font-size: 1.2em;
      margin-bottom: 15px;
      color: #856404;
    }
    
    .tips-list {
      list-style: none;
    }
    
    .tips-list li {
      padding: 8px 0;
      padding-left: 25px;
      position: relative;
      color: #856404;
    }
    
    .tips-list li::before {
      content: '💡';
      position: absolute;
      left: 0;
    }
    
    /* 操作按钮 */
    .actions {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      margin-top: 30px;
      padding-top: 30px;
      border-top: 1px solid #eee;
    }
    
    .action-btn {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 12px 20px;
      border-radius: 25px;
      text-decoration: none;
      font-weight: 600;
      transition: transform 0.2s, box-shadow 0.2s;
    }
    
    .action-btn:hover {
      transform: translateY(-2px);
      box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    .action-btn.primary {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
    }
    
    .action-btn.secondary {
      background: #f8f9fa;
      color: #333;
      border: 1px solid #ddd;
    }
    
    /* 页脚 */
    .footer {
      text-align: center;
      padding: 30px;
      background: #f8f9fa;
      color: #666;
      font-size: 0.85em;
    }
    
    /* 响应式 */
    @media (max-width: 600px) {
      body { padding: 10px; }
      .header { padding: 30px 20px; }
      .header h1 { font-size: 1.8em; }
      .quick-info { grid-template-columns: repeat(2, 1fr); }
      .quick-info .item { border-bottom: 1px solid #eee; }
      .content { padding: 20px; }
      .timeline-item { flex-direction: column; gap: 10px; }
      .timeline-item::before { display: none; }
      .time-badge { width: auto; text-align: left; }
    }
    
    /* 打印样式 */
    @media print {
      body { background: white; padding: 0; }
      .container { box-shadow: none; }
      .action-btn { display: none; }
      .hotel-link { display: none; }
    }
  </style>
</head>
<body>
  <div class="container">
    <!-- 头部 -->
    <div class="header">
      <h1>🌴 {{目的地}}攻略</h1>
      <div class="meta">{{出发城市}}出发 · {{日期区间}} · {{天数}}天{{晚数}}晚 · {{人数}}人</div>
      <div class="source">基于 @{{原作者}} 攻略改编</div>
    </div>
    
    <!-- 快速信息 -->
    <div class="quick-info">
      <div class="item">
        <div class="icon">✈️</div>
        <div class="label">机票</div>
        <div class="value">¥{{机票总价}}</div>
      </div>
      <div class="item">
        <div class="icon">🏨</div>
        <div class="label">住宿</div>
        <div class="value">¥{{住宿总价}}</div>
      </div>
      <div class="item">
        <div class="icon">🎫</div>
        <div class="label">门票</div>
        <div class="value">¥{{门票总价}}</div>
      </div>
      <div class="item">
        <div class="icon">💰</div>
        <div class="label">人均</div>
        <div class="value">¥{{人均费用}}</div>
      </div>
    </div>
    
    <div class="content">
      <!-- 大交通 -->
      <div class="transport-card">
        <h2>✈️ 大交通方案</h2>
        
        <div class="flight-item">
          <div class="flight-row">
            <div class="flight-info">
              <div class="flight-no">去程 · {{去程航班号}}</div>
              <div class="flight-time">{{去程日期}} {{去程时间}} {{出发城市}}→{{目的地}}</div>
            </div>
            <div class="flight-price">¥{{去程价格}}/人</div>
          </div>
        </div>
        
        <div class="flight-item">
          <div class="flight-row">
            <div class="flight-info">
              <div class="flight-no">回程 · {{回程航班号}}</div>
              <div class="flight-time">{{回程日期}} {{回程时间}} {{目的地}}→{{出发城市}}</div>
            </div>
            <div class="flight-price">¥{{回程价格}}/人</div>
          </div>
        </div>
        
        <div class="transport-total">
          ✅ 往返合计 ¥{{机票往返价格}}/人 
          <a href="{{机票预订链接}}" class="hotel-link" target="_blank">立即预订</a>
        </div>
      </div>
      
      <!-- Day 1 示例 -->
      <div class="day-card">
        <div class="day-header">
          <h3>📅 Day 1 · {{Day1日期}}（{{Day1周几}}）</h3>
          <span class="day-theme">{{Day1主题}}</span>
        </div>
        <div class="day-content">
          <!-- 时间线项目 -->
          <div class="timeline-item">
            <div class="time-badge">
              <span class="time">{{时间1}}</span>
            </div>
            <div class="timeline-content">
              <h4>✈️ {{活动标题1}}</h4>
              <p>{{活动描述1}}</p>
            </div>
          </div>
          
          <div class="timeline-item">
            <div class="time-badge">
              <span class="time">{{时间2}}</span>
            </div>
            <div class="timeline-content">
              <h4>🏨 入住酒店</h4>
              <p>{{酒店描述}}</p>
              
              <div class="hotel-card">
                <div class="hotel-header">
                  <span class="hotel-name">{{酒店名称}}</span>
                  <span class="hotel-price">¥{{酒店价格}}/晚</span>
                </div>
                <div class="hotel-meta">
                  <span>⭐ {{酒店评分}}</span>
                  <span>📍 {{酒店位置}}</span>
                  <span class="status status-ok">✅ 有房</span>
                </div>
                <a href="{{酒店预订链接}}" class="hotel-link" target="_blank">查看详情并预订</a>
              </div>
            </div>
          </div>
          
          <div class="timeline-item">
            <div class="time-badge">
              <span class="time">{{时间3}}</span>
            </div>
            <div class="timeline-content">
              <h4>📍 {{景点名称}}</h4>
              <p>{{景点描述}}</p>
              <p><span class="status status-ok">✅ {{门票价格}}</span> · {{开放时间}}</p>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 更多 Day 卡片... -->
      <!-- 按相同格式重复 day-card -->
      
      <!-- 费用总览 -->
      <div class="budget-card">
        <h2>💰 费用总览（{{人数}}人合计）</h2>
        
        <table class="budget-table">
          <tr>
            <td class="item">✈️ 机票往返×{{人数}}</td>
            <td class="amount">¥{{机票总价}}</td>
            <td class="note">{{航班说明}}</td>
          </tr>
          <tr>
            <td class="item">🏨 住宿{{晚数}}晚</td>
            <td class="amount">¥{{住宿总价}}</td>
            <td class="note">{{酒店说明}}</td>
          </tr>
          <tr>
            <td class="item">🎫 景点门票×{{人数}}</td>
            <td class="amount">¥{{门票总价}}</td>
            <td class="note">{{景点说明}}</td>
          </tr>
          <tr>
            <td class="item">🚗 当地交通</td>
            <td class="amount">¥{{交通费用}}</td>
            <td class="note">打车+租车</td>
          </tr>
          <tr>
            <td class="item">🍜 餐饮预估</td>
            <td class="amount">¥{{餐饮费用}}</td>
            <td class="note">{{天数}}天</td>
          </tr>
        </table>
        
        <div class="budget-total">
          <div>
            <div class="label">📊 合计</div>
          </div>
          <div style="text-align: right;">
            <div class="value">¥{{总费用}}</div>
            <div class="per-person">人均 ¥{{人均费用}}</div>
          </div>
        </div>
      </div>
      
      <!-- 差异对比 -->
      <div class="diff-card">
        <h2>📋 与原攻略的差异说明</h2>
        
        <table class="diff-table">
          <thead>
            <tr>
              <th style="width: 30px;">#</th>
              <th>原攻略</th>
              <th>你的版本</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>1</td>
              <td class="original">{{差异1原内容}}</td>
              <td class="adapted">{{差异1调整}}</td>
            </tr>
            <tr>
              <td>2</td>
              <td class="original">{{差异2原内容}}</td>
              <td class="adapted">{{差异2调整}}</td>
            </tr>
            <!-- 更多差异行... -->
          </tbody>
        </table>
      </div>
      
      <!-- 小贴士 -->
      <div class="tips-card">
        <h2>‼️ 小贴士</h2>
        <ul class="tips-list">
          <li>{{提示1}}</li>
          <li>{{提示2}}</li>
          <li>{{提示3}}</li>
          <!-- 更多提示... -->
        </ul>
      </div>
      
      <!-- 操作按钮 -->
      <div class="actions">
        <a href="{{机票预订链接}}" class="action-btn primary" target="_blank">
          ✈️ 预订机票
        </a>
        <a href="{{酒店预订链接}}" class="action-btn primary" target="_blank">
          🏨 预订酒店
        </a>
        <a href="javascript:window.print()" class="action-btn secondary">
          🖨️ 打印攻略
        </a>
        <a href="javascript:exportImage()" class="action-btn secondary" id="exportBtn">
          📷 导出图片
        </a>
      </div>
      
      <!-- 导出提示 -->
      <div id="exportTip" style="display: none; text-align: center; padding: 15px; background: #d4edda; border-radius: 10px; margin-top: 15px; color: #155724;">
        🎉 图片生成中，请稍候...
      </div>
    </div>
    
    <!-- 页脚 -->
    <div class="footer">
      <p>由 FlyAI 一键抄作业助手生成 · {{生成时间}}</p>
      <p>数据来源：飞猪旅行</p>
    </div>
  </div>
  
  <!-- 引入 html2canvas -->
  <script src="https://cdn.jsdelivr.net/npm/html2canvas@1.4.1/dist/html2canvas.min.js"></script>
  
  <script>
    async function exportImage() {
      const exportBtn = document.getElementById('exportBtn');
      const exportTip = document.getElementById('exportTip');
      const container = document.querySelector('.container');
      
      // 显示提示
      exportBtn.style.pointerEvents = 'none';
      exportBtn.innerHTML = '⏳ 生成中...';
      exportTip.style.display = 'block';
      
      try {
        // 临时隐藏操作按钮区域
        const actions = document.querySelector('.actions');
        const originalDisplay = actions.style.display;
        actions.style.display = 'none';
        exportTip.style.display = 'none';
        
        // 生成图片
        const canvas = await html2canvas(container, {
          scale: 2, // 2倍清晰度
          useCORS: true,
          allowTaint: true,
          backgroundColor: '#667eea',
          logging: false
        });
        
        // 恢复操作按钮
        actions.style.display = originalDisplay;
        
        // 下载图片
        const link = document.createElement('a');
        link.download = '{{目的地}}攻略-{{出发日期}}.png';
        link.href = canvas.toDataURL('image/png');
        link.click();
        
        // 显示成功提示
        exportTip.innerHTML = '✅ 图片已保存到下载文件夹！可直接分享到朋友圈/微信群';
        exportTip.style.display = 'block';
        
        setTimeout(() => {
          exportTip.style.display = 'none';
        }, 3000);
        
      } catch (error) {
        console.error('导出失败:', error);
        exportTip.innerHTML = '❌ 导出失败，请重试';
        exportTip.style.background = '#f8d7da';
        exportTip.style.color = '#721c24';
        exportTip.style.display = 'block';
      }
      
      // 恢复按钮
      exportBtn.style.pointerEvents = 'auto';
      exportBtn.innerHTML = '📷 导出图片';
    }
  </script>
</body>
</html>
```

---

## 样式说明

### 配色方案

| 元素 | 颜色 | 用途 |
|------|------|------|
| 主色调 | `#667eea → #764ba2` | 头部、按钮、Day卡片头 |
| 交通卡片 | `#11998e → #38ef7d` | 机票信息，绿色表示出行 |
| 费用卡片 | `#f093fb → #f5576c` | 费用总览，粉红吸引注意 |
| 警告提示 | `#fff3cd` | 小贴士背景 |
| 成功状态 | `#d4edda` | 可用、有房 |
| 警告状态 | `#fff3cd` | 需确认 |
| 错误状态 | `#f8d7da` | 不可用 |

### 响应式断点

- **桌面端**：> 600px，完整布局
- **移动端**：≤ 600px，单列布局，时间线简化

### 打印优化

- 隐藏预订按钮
- 移除阴影和渐变背景
- 优化纸张布局

---

## 组件说明

### 1. 头部区域 (header)
展示目的地、出行信息、原攻略来源

### 2. 快速信息 (quick-info)
4格快速预览：机票、住宿、门票、人均费用

### 3. 交通卡片 (transport-card)
去程和回程航班信息，含预订链接

### 4. 每日行程 (day-card)
- day-header：日期和主题
- timeline-item：时间线项目
- hotel-card：嵌入式酒店卡片

### 5. 状态标签 (status)
- `status-ok`：✅ 可用
- `status-warn`：⚠️ 需确认
- `status-error`：❌ 不可用
- `status-info`：ℹ️ 信息

### 6. 费用总览 (budget-card)
表格形式展示各项费用和总计

### 7. 差异对比 (diff-card)
原攻略 vs 定制版本的差异表格

### 8. 小贴士 (tips-card)
重要提醒和建议

### 9. 操作按钮 (actions)
预订链接和打印按钮

---

## 使用方法

### 生成 HTML 文件

1. 准备攻略数据（目的地、日期、费用等）
2. 替换模板中的 `{{变量}}` 占位符
3. 使用 `create_file` 工具生成文件

### 变量占位符列表

| 变量 | 说明 | 示例 |
|------|------|------|
| `{{目的地}}` | 旅行目的地 | 普吉岛 |
| `{{出发城市}}` | 用户出发城市 | 杭州 |
| `{{日期区间}}` | 出行日期范围 | 4月4日-4月8日 |
| `{{天数}}` | 总天数 | 5 |
| `{{晚数}}` | 住宿晚数 | 4 |
| `{{人数}}` | 出行人数 | 4 |
| `{{原作者}}` | 原攻略作者 | Elaine |
| `{{机票总价}}` | 机票费用 | 12,468 |
| `{{住宿总价}}` | 住宿费用 | 2,001 |
| `{{门票总价}}` | 门票费用 | 1,600 |
| `{{人均费用}}` | 人均总费用 | 5,132 |
| `{{去程航班号}}` | 去程航班 | VZ3537+VZ314 |
| `{{回程航班号}}` | 回程航班 | OD543+D7306 |
| `{{机票预订链接}}` | 飞猪机票链接 | https://a.feizhu.com/... |
| `{{酒店预订链接}}` | 飞猪酒店链接 | https://a.feizhu.com/... |
| `{{生成时间}}` | 攻略生成时间 | 2026-03-31 |

### 动态生成 Day 卡片

对于每一天的行程，复制 `day-card` 组件并替换：
- `{{DayN日期}}`：当天日期
- `{{DayN周几}}`：星期几
- `{{DayN主题}}`：当天主题
- 时间线项目根据实际活动增减

### 示例代码

```python
# 生成 HTML 文件
html_content = """
<!DOCTYPE html>
<html lang="zh-CN">
...（将所有变量替换为实际值）
</html>
"""

create_file(
  file_path="/Users/xxx/Desktop/普吉岛-攻略-2026-04-04.html",
  file_content=html_content
)
```

---

## 最佳实践

1. **变量替换**：使用字符串替换或模板引擎替换所有 `{{变量}}`
2. **动态内容**：根据实际天数和活动数量动态生成 day-card 和 timeline-item
3. **链接处理**：确保所有预订链接 `jumpUrl` 正确提取
4. **状态标注**：根据验证结果使用正确的 status 类名
5. **响应式测试**：生成后在移动端和桌面端都测试一下
