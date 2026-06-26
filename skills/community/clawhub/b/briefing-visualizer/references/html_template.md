# 简报 HTML 模板参考

## 快速开始

将以下结构复制到新的 HTML 文件，替换内容后使用 `process_briefing.py` 处理即可。

---

## 完整模板

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>简报标题</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    width: 390px;  /* 必须与截图宽度一致 */
    background: #FFF8F0;
    font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif;
    color: #4A3728;
    padding: 0;
  }

  /* 顶部标题区 */
  .header {
    background: linear-gradient(135deg, #D4845A 0%, #C46B3A 50%, #B85C2A 100%);
    padding: 32px 20px 26px;
    text-align: center;
    border-bottom: 2px solid #A04820;
  }
  .header-badge { font-size: 11px; color: #FFF5EB; letter-spacing: 2px; margin-bottom: 12px; }
  .header-title { font-size: 26px; font-weight: 800; color: #fff; line-height: 1.3; margin-bottom: 8px; }
  .header-subtitle { font-size: 11px; color: #FFE8D5; letter-spacing: 3px; margin-bottom: 12px; }
  .header-date { font-size: 11px; color: #FFF0E0; }

  /* 数据摘要 */
  .stats-row { display: flex; gap: 8px; margin: 18px 16px; }
  .stat-box { flex: 1; background: #fff; border: 1.5px solid #E8D5C4; border-radius: 10px; padding: 14px 6px; text-align: center; }
  .stat-num { font-size: 20px; font-weight: 800; color: #C46B3A; }
  .stat-label { font-size: 10px; color: #7A6050; margin-top: 4px; }

  /* 板块标题 */
  .section { padding: 22px 16px 14px; }
  .section-header { display: flex; align-items: center; gap: 10px; margin-bottom: 16px; padding-bottom: 10px; border-bottom: 1.5px solid #E8D5C4; }
  .section-icon { width: 34px; height: 34px; border-radius: 9px; display: flex; align-items: center; justify-content: center; font-size: 17px; }
  .icon-ocean { background: linear-gradient(135deg, #2D8BAE, #3AAFD4); }
  .icon-ball  { background: linear-gradient(135deg, #D45A2A, #E87848); }
  .icon-combo { background: linear-gradient(135deg, #3D7A4A, #5AAD6A); }
  .section-title { font-size: 17px; font-weight: 700; color: #3A2A1A; }
  .section-desc { font-size: 10px; color: #8A7060; margin-top: 2px; }

  /* 资讯卡片 */
  .news-card { background: #fff; border: 1.5px solid #E8D5C4; border-radius: 10px; padding: 14px 16px; margin-bottom: 10px; position: relative; overflow: hidden; }
  .news-card::before { content: ''; position: absolute; top: 0; left: 0; width: 4px; height: 100%; border-radius: 2px 0 0 2px; }
  .card-ocean::before { background: linear-gradient(180deg, #2D8BAE, #3AAFD4); }
  .card-ball::before  { background: linear-gradient(180deg, #D45A2A, #E87848); }
  .card-combo::before { background: linear-gradient(180deg, #3D7A4A, #5AAD6A); }

  .card-top { display: flex; align-items: flex-start; gap: 8px; margin-bottom: 9px; }
  .card-number { width: 22px; height: 22px; border-radius: 6px; display: flex; align-items: center; justify-content: center; font-size: 10px; font-weight: 700; }
  .num-ocean { background: rgba(45,139,174,0.15); color: #2D8BAE; }
  .num-ball  { background: rgba(212,90,42,0.15); color: #D45A2A; }
  .num-combo { background: rgba(61,122,74,0.15); color: #3D7A4A; }
  .card-headline { font-size: 14px; font-weight: 700; color: #2A1A0A; line-height: 1.5; flex: 1; }
  .card-body { font-size: 13px; color: #5A4A3A; line-height: 1.8; margin-bottom: 9px; padding-left: 30px; }
  .card-footer { display: flex; align-items: center; gap: 6px; padding-left: 30px; flex-wrap: wrap; }

  /* 标签 */
  .tag { display: inline-flex; padding: 2px 10px; border-radius: 14px; font-size: 10px; font-weight: 600; }
  .tag-trend  { background: rgba(200,140,40,0.12); color: #B87820; border: 1px solid rgba(184,120,32,0.3); }
  .tag-market { background: rgba(212,90,42,0.12); color: #C04020; border: 1px solid rgba(200,85,40,0.3); }
  .tag-brand  { background: rgba(130,80,180,0.12); color: #7A50B4; border: 1px solid rgba(122,80,180,0.3); }
  .tag-supply { background: rgba(45,139,174,0.12); color: #2D8BAE; border: 1px solid rgba(45,139,174,0.3); }
  .tag-join   { background: rgba(61,122,74,0.12); color: #3D7A4A; border: 1px solid rgba(61,122,74,0.3); }
  .tag-tech   { background: rgba(45,139,174,0.1); color: #2D8BAE; border: 1px solid rgba(45,139,174,0.25); }
  .hot-icon   { font-size: 10px; color: #C04020; background: rgba(192,64,32,0.08); border: 1px solid rgba(192,64,32,0.2); padding: 2px 9px; border-radius: 10px; font-weight: 700; }

  .divider { height: 1.5px; background: linear-gradient(90deg, transparent, #E8D5C4, transparent); margin: 4px 16px; }

  /* 亮点框 */
  .highlight-box { background: linear-gradient(135deg, rgba(212,90,42,0.08), rgba(200,140,40,0.06)); border: 1.5px solid rgba(212,90,42,0.25); border-radius: 10px; padding: 12px 14px; margin: 0 16px 16px; display: flex; gap: 10px; }
  .highlight-icon { font-size: 16px; flex-shrink: 0; }
  .highlight-text { font-size: 12px; color: #5A4030; line-height: 1.8; }

  /* 底部页脚 */
  .footer { background: #F5EDE0; padding: 16px 20px; border-top: 1.5px solid #E8D5C4; text-align: center; }
  .footer-text { font-size: 10px; color: #8A7060; line-height: 1.8; }
  .footer-brand { font-size: 12px; color: #C46B3A; font-weight: 700; margin-top: 6px; }

  /* 底部通栏广告图 */
  .bottom-image { width: 100%; display: block; }
</style>
</head>
<body>

<!-- 顶部 -->
<div class="header">
  <div class="header-badge">📊 行业情报</div>
  <div class="header-title">标题<br>副标题</div>
  <div class="header-subtitle">DATE LABEL</div>
  <div class="header-date">📅 2026年X月X周</div>
</div>

<!-- 数据摘要（可选） -->
<div class="stats-row">
  <div class="stat-box"><div class="stat-num">X<span style="font-size:12px">亿</span></div><div class="stat-label">指标一</div></div>
  <div class="stat-box"><div class="stat-num">X<span style="font-size:12px">%</span></div><div class="stat-label">指标二</div></div>
  <div class="stat-box"><div class="stat-num">X<span style="font-size:12px">倍</span></div><div class="stat-label">指标三</div></div>
</div>

<!-- 板块1 -->
<div class="section">
  <div class="section-header">
    <div class="section-icon icon-ocean">🦪</div>
    <div>
      <div class="section-title">板块一 · 标题</div>
      <div class="section-desc">关键词 / 关键词 / 关键词</div>
    </div>
  </div>

  <div class="news-card card-ocean">
    <div class="card-top">
      <div class="card-number num-ocean">01</div>
      <div class="card-headline">标题：核心信息一句话</div>
    </div>
    <div class="card-body">正文描述，2-4句，数据/来源/意义。</div>
    <div class="card-footer">
      <span class="tag tag-trend">标签一</span>
      <span class="tag tag-market">标签二</span>
      <span class="hot-icon">🔥 重要</span>
    </div>
  </div>
  <!-- 更多卡片... -->
</div>

<div class="divider"></div>

<!-- 亮点洞察 -->
<div class="highlight-box">
  <div class="highlight-icon">💡</div>
  <div class="highlight-text"><strong>核心洞察：</strong>总结性文字。</div>
</div>

<!-- 底部页脚 -->
<div class="footer">
  <div class="footer-text">数据来源：来源一 · 来源二</div>
  <div class="footer-text">仅供内部参考</div>
  <div class="footer-brand">🏢 品牌名 · 情报系统</div>
</div>

<!-- 底部通栏广告图 -->
<img class="bottom-image" src="file:///path/to/banner.png" alt="">

</body>
</html>
```

---

## 配色方案（可自定义）

| 用途 | 颜色 | 色值 |
|------|------|------|
| 主色（头部/标题） | 暖橙 | #C46B3A |
| 背景色 | 米白 | #FFF8F0 |
| 正文色 | 深棕 | #5A4A3A |
| 板块一色 | 海洋蓝 | #2D8BAE |
| 板块二色 | 丸子橙 | #D45A2A |
| 板块三色 | 组合绿 | #3D7A4A |
| 边框色 | 浅棕 | #E8D5C4 |
