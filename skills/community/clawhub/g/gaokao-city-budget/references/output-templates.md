# 输出模板说明 + 可复用 HTML 代码

---

## 设计原则

- **暖绿色调**：与就业热力图的蓝紫色系区分，用 `#059669 → #10B981 → #D1FAE5` 渐变，传递"生活/家庭"氛围
- **预算可视化**：三档预算（基础/中等/舒适）用横向拆分条，各费用占比一眼可见
- **费用卡片**：房租/餐饮/交通三大项独立卡片，每项有区间范围 + 数据条
- **学生视角**：突出学生实际花费，而非城市均价；醒目标注学生优惠政策
- **动画脚本**：进度条入场动画，卡片滚动淡入，hover 微交互

---

## 模板 A — 单城市预算画像（HTML）

**文件名格式**：`[城市名]-大学生活预算-[日期].html`

### 完整基础代码

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>[城市名] 大学生活成本预算</title>
<style>
  /* ── 全局变量 ── */
  :root {
    --brand:       #059669;
    --brand-light: #34D399;
    --brand-pale:  #ECFDF5;
    --brand-mid:   #A7F3D0;
    --accent:      #0891B2;    /* 蓝色用于交通模块 */
    --accent-pale: #E0F2FE;
    --amber:       #D97706;    /* 橙色用于餐饮模块 */
    --amber-pale:  #FEF3C7;
    --text-h:      #064E3B;
    --text-body:   #374151;
    --text-muted:  #9CA3AF;
    --card-bg:     #FFFFFF;
    --page-bg:     #F0FDF9;
    --border:      #D1FAE5;
    --radius:      14px;
    --shadow:      0 2px 12px rgba(5,150,105,.08);
    --shadow-lg:   0 8px 32px rgba(5,150,105,.14);
  }

  * { box-sizing: border-box; margin: 0; padding: 0; }

  body {
    font-family: -apple-system, "PingFang SC", "Microsoft YaHei", sans-serif;
    background: var(--page-bg);
    color: var(--text-body);
    line-height: 1.6;
    padding: 24px 16px 60px;
  }

  /* ── 页眉 ── */
  .page-header {
    max-width: 900px;
    margin: 0 auto 32px;
    padding: 32px 36px;
    background: linear-gradient(135deg, #065F46 0%, #059669 60%, #0891B2 100%);
    border-radius: 20px;
    color: #fff;
    box-shadow: var(--shadow-lg);
    position: relative;
    overflow: hidden;
  }
  .page-header::before {
    content: '';
    position: absolute;
    top: -50px; right: -50px;
    width: 200px; height: 200px;
    background: rgba(255,255,255,.07);
    border-radius: 50%;
  }
  .page-header::after {
    content: '';
    position: absolute;
    bottom: -30px; left: 40px;
    width: 120px; height: 120px;
    background: rgba(255,255,255,.05);
    border-radius: 50%;
  }
  .page-header .city-tag {
    display: inline-block;
    background: rgba(255,255,255,.2);
    border: 1px solid rgba(255,255,255,.35);
    border-radius: 20px;
    padding: 3px 12px;
    font-size: 12px;
    margin-bottom: 10px;
  }
  .page-header h1 { font-size: clamp(22px,4vw,30px); font-weight: 700; margin-bottom: 6px; }
  .page-header .meta {
    font-size: 13px; opacity: .75;
    display: flex; gap: 16px; flex-wrap: wrap;
  }

  /* ── 通用卡片 ── */
  .container { max-width: 900px; margin: 0 auto; }
  .card {
    background: var(--card-bg);
    border-radius: var(--radius);
    box-shadow: var(--shadow);
    padding: 24px 28px;
    margin-bottom: 20px;
    border: 1px solid var(--border);
  }
  .card-title {
    font-size: 15px; font-weight: 700; color: var(--text-h);
    margin-bottom: 18px;
    display: flex; align-items: center; gap: 8px;
  }
  .card-title .icon {
    width: 30px; height: 30px;
    border-radius: 9px;
    display: flex; align-items: center; justify-content: center;
    font-size: 15px;
  }
  .icon-green  { background: var(--brand-pale); }
  .icon-amber  { background: var(--amber-pale); }
  .icon-blue   { background: var(--accent-pale); }
  .icon-purple { background: #EDE9FE; }

  /* ── 月预算三档总览 ── */
  .budget-tiers {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 14px;
    margin-bottom: 20px;
  }
  .tier-box {
    border-radius: var(--radius);
    padding: 20px 16px;
    text-align: center;
    border: 2px solid transparent;
    transition: transform .15s, box-shadow .15s;
    cursor: default;
  }
  .tier-box:hover { transform: translateY(-3px); box-shadow: var(--shadow-lg); }
  .tier-basic    { background: var(--brand-pale);  border-color: var(--brand-mid); }
  .tier-mid      { background: #FFFBEB; border-color: #FDE68A; }
  .tier-comfort  { background: var(--accent-pale); border-color: #BAE6FD; }
  .tier-box .tier-label {
    font-size: 12px; font-weight: 700; letter-spacing: .06em;
    margin-bottom: 8px; opacity: .7;
  }
  .tier-box .tier-range {
    font-size: 20px; font-weight: 800; letter-spacing: -.03em;
    line-height: 1.2;
  }
  .tier-basic   .tier-range { color: var(--brand); }
  .tier-mid     .tier-range { color: #D97706; }
  .tier-comfort .tier-range { color: var(--accent); }
  .tier-box .tier-sub { font-size: 11px; color: var(--text-muted); margin-top: 5px; }

  /* ── 预算拆分条（三档叠加对比） ── */
  .split-bar-section { margin-top: 6px; }
  .split-row { margin-bottom: 14px; }
  .split-row-label {
    display: flex; justify-content: space-between;
    font-size: 13px; font-weight: 600; color: var(--text-h);
    margin-bottom: 5px;
  }
  .split-row-label .split-range { color: var(--text-muted); font-weight: 400; font-size: 12px; }
  .split-track {
    height: 10px; background: #F3F4F6;
    border-radius: 99px; overflow: hidden;
    position: relative;
  }
  .split-fill {
    height: 100%; border-radius: 99px;
    transition: width .7s cubic-bezier(.4,0,.2,1);
  }
  .fill-rent       { background: linear-gradient(90deg, #34D399, #059669); }
  .fill-food       { background: linear-gradient(90deg, #FCD34D, #D97706); }
  .fill-transport  { background: linear-gradient(90deg, #38BDF8, #0891B2); }
  .fill-util       { background: linear-gradient(90deg, #C084FC, #7C3AED); }
  .fill-misc       { background: linear-gradient(90deg, #FDA4AF, #E11D48); }

  /* ── 费用详情卡（房租/餐饮/交通各一张） ── */
  .cost-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 14px;
    margin-top: 14px;
  }
  .cost-item {
    border-radius: 10px;
    padding: 14px 16px;
    border: 1px solid transparent;
  }
  .cost-item-green  { background: var(--brand-pale);  border-color: var(--brand-mid); }
  .cost-item-amber  { background: var(--amber-pale);  border-color: #FDE68A; }
  .cost-item-blue   { background: var(--accent-pale); border-color: #BAE6FD; }
  .cost-item-purple { background: #F5F3FF; border-color: #DDD6FE; }
  .cost-item .ci-label { font-size: 11px; color: var(--text-muted); margin-bottom: 4px; font-weight: 600; }
  .cost-item .ci-value { font-size: 18px; font-weight: 800; line-height: 1.2; }
  .cost-item-green  .ci-value { color: var(--brand); }
  .cost-item-amber  .ci-value { color: var(--amber); }
  .cost-item-blue   .ci-value { color: var(--accent); }
  .cost-item-purple .ci-value { color: #7C3AED; }
  .cost-item .ci-sub { font-size: 11px; color: var(--text-muted); margin-top: 3px; }

  /* ── 学生优惠 badge ── */
  .discount-badges { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 14px; }
  .discount-badge {
    display: flex; align-items: center; gap: 5px;
    padding: 5px 12px;
    background: var(--brand-pale);
    border: 1px solid var(--brand-mid);
    border-radius: 20px;
    font-size: 12px; font-weight: 600; color: var(--brand);
  }
  .discount-badge.amber {
    background: var(--amber-pale); border-color: #FDE68A; color: var(--amber);
  }
  .discount-badge.blue {
    background: var(--accent-pale); border-color: #BAE6FD; color: var(--accent);
  }

  /* ── 真实花费参考（学生社区） ── */
  .quote-block {
    border-left: 3px solid var(--brand);
    background: var(--brand-pale);
    border-radius: 0 10px 10px 0;
    padding: 12px 16px;
    font-size: 13px;
    line-height: 1.7;
    margin: 10px 0;
    color: var(--text-body);
  }
  .quote-block .q-source {
    font-size: 11px; color: var(--text-muted);
    margin-top: 6px;
  }

  /* ── 注意提示 ── */
  .notice {
    background: #FFFBEB; border: 1px solid #FDE68A;
    border-radius: 10px; padding: 12px 16px;
    font-size: 12px; color: #92400E;
    display: flex; gap: 8px; align-items: flex-start;
    margin-top: 16px;
  }

  /* ── 页脚 ── */
  .footer {
    max-width: 900px; margin: 32px auto 0;
    padding: 20px 0 0; border-top: 1px solid var(--border);
    font-size: 12px; color: var(--text-muted); line-height: 1.9;
  }
  .footer a { color: var(--brand); text-decoration: none; }
  .disclaimer {
    margin-top: 12px; padding: 12px 16px;
    background: var(--brand-pale); border-radius: 10px;
    font-size: 11.5px; color: #065F46;
  }

  /* ── 响应式 ── */
  @media (max-width: 600px) {
    .budget-tiers { grid-template-columns: 1fr 1fr; }
    .cost-grid    { grid-template-columns: 1fr; }
    .page-header  { padding: 24px 20px; }
    .card         { padding: 18px 16px; }
  }
  @media (max-width: 400px) {
    .budget-tiers { grid-template-columns: 1fr; }
  }
</style>
</head>
<body>

<!-- ① 页眉 -->
<div class="page-header">
  <div class="city-tag">高考志愿参考 · 生活成本</div>
  <h1>[城市名] 大学生活费预算</h1>
  <div class="meta">
    <span>🎓 参考院校区域：[学校所在区/主要高校区]</span>
    <span>📅 数据生成：[日期]</span>
    <span>📦 来源：[贝壳/58同城/知乎/官网等]</span>
  </div>
</div>

<div class="container">

  <!-- ② 月预算三档 -->
  <div class="budget-tiers">
    <div class="tier-box tier-basic">
      <div class="tier-label">💡 基础档</div>
      <div class="tier-range">[X,XXX]–[X,XXX]<span style="font-size:13px;font-weight:500"> 元</span></div>
      <div class="tier-sub">住校内宿舍 · 主食食堂 · 公交出行</div>
    </div>
    <div class="tier-box tier-mid">
      <div class="tier-label">📊 中等档</div>
      <div class="tier-range">[X,XXX]–[X,XXX]<span style="font-size:13px;font-weight:500"> 元</span></div>
      <div class="tier-sub">校外合租 · 食堂+外卖 · 地铁出行</div>
    </div>
    <div class="tier-box tier-comfort">
      <div class="tier-label">✨ 舒适档</div>
      <div class="tier-range">[X,XXX]–[X,XXX]<span style="font-size:13px;font-weight:500"> 元</span></div>
      <div class="tier-sub">品牌公寓 · 外卖/餐厅为主 · 打车</div>
    </div>
  </div>

  <!-- ③ 费用占比拆分条 -->
  <div class="card">
    <div class="card-title"><span class="icon icon-green">📊</span>月均费用结构拆分（中等档参考）</div>
    <div class="split-bar-section">

      <div class="split-row">
        <div class="split-row-label">
          <span>🏠 住宿费</span>
          <span class="split-range">[X,XXX–X,XXX 元/月]</span>
        </div>
        <div class="split-track">
          <div class="split-fill fill-rent" style="width:[占总预算百分比，如42%]"></div>
        </div>
      </div>

      <div class="split-row">
        <div class="split-row-label">
          <span>🍜 餐饮费</span>
          <span class="split-range">[XXX–X,XXX 元/月]</span>
        </div>
        <div class="split-track">
          <div class="split-fill fill-food" style="width:[如35%]"></div>
        </div>
      </div>

      <div class="split-row">
        <div class="split-row-label">
          <span>🚇 交通费</span>
          <span class="split-range">[XX–XXX 元/月]</span>
        </div>
        <div class="split-track">
          <div class="split-fill fill-transport" style="width:[如10%]"></div>
        </div>
      </div>

      <div class="split-row">
        <div class="split-row-label">
          <span>💡 水电网费</span>
          <span class="split-range">[XX–XXX 元/月]</span>
        </div>
        <div class="split-track">
          <div class="split-fill fill-util" style="width:[如6%]"></div>
        </div>
      </div>

      <div class="split-row">
        <div class="split-row-label">
          <span>🛒 日用/弹性消费</span>
          <span class="split-range">[XXX–XXX 元/月]</span>
        </div>
        <div class="split-track">
          <div class="split-fill fill-misc" style="width:[如7%]"></div>
        </div>
      </div>

    </div>
    <div style="font-size:12px;color:var(--text-muted);margin-top:10px">
      ⚠️ 学费/住宿费（学校官方收取部分）未计入日常生活费，需另行计划。各项比例基于中等档估算，实际因人而异。
    </div>
  </div>

  <!-- ④ 房租详情 -->
  <div class="card">
    <div class="card-title"><span class="icon icon-green">🏠</span>住宿费用参考</div>
    <div class="cost-grid">
      <div class="cost-item cost-item-green">
        <div class="ci-label">校内宿舍（学年费）</div>
        <div class="ci-value">[X,XXX–X,XXX 元]</div>
        <div class="ci-sub">折合月均 [XXX] 元 · 来源：[学校官网]</div>
      </div>
      <div class="cost-item cost-item-green">
        <div class="ci-label">校外合租单间（月租）</div>
        <div class="ci-value">[X,XXX–X,XXX 元]</div>
        <div class="ci-sub">[区域说明] · 来源：[贝壳/58同城] · [日期]</div>
      </div>
      <div class="cost-item cost-item-purple">
        <div class="ci-label">品牌公寓合租（月租）</div>
        <div class="ci-value">[X,XXX–X,XXX 元]</div>
        <div class="ci-sub">含基础家具 · 来源：[自如/蛋壳] · [日期]</div>
      </div>
      <div class="cost-item cost-item-purple">
        <div class="ci-label">整租一居室（月租）</div>
        <div class="ci-value">[X,XXX–X,XXX 元]</div>
        <div class="ci-sub">[区域说明] · 来源：[贝壳] · [日期]</div>
      </div>
    </div>
    <!-- 学生租房真实引用 -->
    <div class="quote-block">
      "[引用学生原话，如：学校附近的单间大概在800到1200之间，离地铁近的贵一些，找室友合租的话人均可以到600-700……]"
      <div class="q-source">📌 [来源平台，如知乎/贴吧] · [年份] · [若知乎可注明获赞数]</div>
    </div>
    <div class="notice">
      ⚠️ 挂牌价为参考值，实际成交价可能低5–15%。大三/大四后选择校外的学生比例较高，建议入学初先住校内宿舍再做规划。
    </div>
  </div>

  <!-- ⑤ 餐饮详情 -->
  <div class="card">
    <div class="card-title"><span class="icon icon-amber">🍜</span>餐饮消费参考</div>
    <div class="cost-grid">
      <div class="cost-item cost-item-amber">
        <div class="ci-label">学校食堂 · 一餐均价</div>
        <div class="ci-value">[XX–XX 元]</div>
        <div class="ci-sub">含早/午/晚 · 来源：[学校贴吧/知乎] · [年份]</div>
      </div>
      <div class="cost-item cost-item-amber">
        <div class="ci-label">校外快餐/小吃 · 一餐均价</div>
        <div class="ci-value">[XX–XX 元]</div>
        <div class="ci-sub">[区域] · 来源：[大众点评] · [日期]</div>
      </div>
      <div class="cost-item cost-item-amber">
        <div class="ci-label">外卖 · 客单价参考</div>
        <div class="ci-value">[XX–XX 元/单]</div>
        <div class="ci-sub">含配送费 · 来源：[美团/调查数据] · [年份]</div>
      </div>
      <div class="cost-item cost-item-amber">
        <div class="ci-label">月均餐饮估算</div>
        <div class="ci-value">[XXX–X,XXX 元]</div>
        <div class="ci-sub">食堂为主约[XXX]元，外卖为主约[X,XXX]元</div>
      </div>
    </div>
    <div class="quote-block" style="border-color:#D97706;background:var(--amber-pale)">
      "[引用学生原话，如：我一般一天三顿都在食堂吃，一个月吃饭大概500左右，偶尔周末出去吃一次会多花点……]"
      <div class="q-source">📌 [来源平台] · [年份]</div>
    </div>
  </div>

  <!-- ⑥ 交通详情 -->
  <div class="card">
    <div class="card-title"><span class="icon icon-blue">🚇</span>交通费用参考</div>

    <!-- 学生优惠badges -->
    <div style="font-size:13px;color:var(--text-muted);margin-bottom:10px">学生专属优惠政策（以官网最新公告为准）：</div>
    <div class="discount-badges">
      <!-- 大模型根据实际政策填写，无政策则不显示此行 -->
      <div class="discount-badge blue">🚇 [优惠名称，如"地铁学生卡8折"]</div>
      <div class="discount-badge blue">🚌 [如"公交学生月卡50元/月"]</div>
      <!-- 如暂无学生优惠，显示: -->
      <!-- <div class="discount-badge amber">⚠️ 暂未查到学生专属优惠，建议查官网</div> -->
    </div>

    <div class="cost-grid" style="margin-top:14px">
      <div class="cost-item cost-item-blue">
        <div class="ci-label">地铁单程均价</div>
        <div class="ci-value">[X–X 元]</div>
        <div class="ci-sub">来源：[城市地铁官网] · [年份]</div>
      </div>
      <div class="cost-item cost-item-blue">
        <div class="ci-label">公交单程票价</div>
        <div class="ci-value">[X–X 元]</div>
        <div class="ci-sub">来源：[城市公交官网] · [年份]</div>
      </div>
      <div class="cost-item cost-item-blue">
        <div class="ci-label">月均交通估算（低频出行）</div>
        <div class="ci-value">[XX–XXX 元]</div>
        <div class="ci-sub">以校内活动为主，偶尔出行</div>
      </div>
      <div class="cost-item cost-item-blue">
        <div class="ci-label">月均交通估算（中频出行）</div>
        <div class="ci-value">[XXX–XXX 元]</div>
        <div class="ci-sub">每周出行2–3次，不含打车</div>
      </div>
    </div>
    <div class="quote-block" style="border-color:#0891B2;background:var(--accent-pale)">
      "[引用学生原话，如：平时基本不怎么出校，一个月交通费100以内，要是经常出去玩可能要200-300……]"
      <div class="q-source">📌 [来源平台] · [年份]</div>
    </div>
  </div>

</div><!-- /container -->

<!-- 页脚 -->
<div class="footer container">
  <strong>数据来源</strong><br>
  · <a href="[URL]">[来源1]</a> — [内容] · 采集时间：[日期]<br>
  · <a href="[URL]">[来源2]</a> — [内容] · 采集时间：[日期]<br>
  · [更多来源...]<br>
  <div class="disclaimer">
    📋 <strong>说明：</strong>以上数据来自公开平台及网络讨论，物价受时间、地段、个人消费习惯影响较大，仅作参考，不构成财务建议。建议结合
    <a href="#" target="_blank">贝壳找房实时挂牌价</a>、
    目标院校官网住宿费公告、
    城市交通官网学生优惠政策综合判断。
  </div>
</div>

<script>
  document.addEventListener('DOMContentLoaded', () => {
    // 1. 费用拆分进度条动画
    document.querySelectorAll('.split-fill').forEach(bar => {
      const target = bar.style.width;
      bar.style.width = '0';
      requestAnimationFrame(() => {
        setTimeout(() => { bar.style.width = target; }, 200);
      });
    });

    // 2. 卡片滚动淡入
    const cards = document.querySelectorAll('.card, .tier-box');
    const io = new IntersectionObserver(entries => {
      entries.forEach(e => {
        if (e.isIntersecting) {
          e.target.style.opacity = '1';
          e.target.style.transform = 'translateY(0)';
          io.unobserve(e.target);
        }
      });
    }, { threshold: 0.08 });
    cards.forEach((c, i) => {
      c.style.opacity = '0';
      c.style.transform = 'translateY(18px)';
      c.style.transition = `opacity .45s ease ${i * 60}ms, transform .45s ease ${i * 60}ms`;
      io.observe(c);
    });
  });
</script>

</body>
</html>
```

---

## 模板 B — 多城市生活成本对比热力表（HTML）

**文件名格式**：`城市生活成本对比-[城市1]vs[城市2]-[日期].html`

### 对比表专用样式（在模板 A CSS 基础上追加）

```html
<style>
  /* ── 对比表 ── */
  .compare-table { width:100%; border-collapse:separate; border-spacing:0; margin-top:16px; }
  .compare-table th {
    padding: 12px 14px;
    font-size: 12px; font-weight: 700; color: var(--text-muted);
    text-align: left; border-bottom: 2px solid var(--border);
    white-space: nowrap; background: #FAFAFA;
  }
  .compare-table th:first-child { border-radius: 10px 0 0 0; }
  .compare-table th:last-child  { border-radius: 0 10px 0 0; }
  .compare-table td {
    padding: 12px 10px; border-bottom: 1px solid var(--border); vertical-align: top;
  }
  .compare-table tr:last-child td { border-bottom: none; }

  /* 热力格 */
  .heat-cell {
    border-radius: 10px; padding: 9px 12px;
    position: relative; transition: transform .15s;
    cursor: default; min-width: 80px;
  }
  .heat-cell:hover { transform: scale(1.04); z-index: 1; }

  /* 绿色热力（费用低=好→深；费用高→浅，与就业技能逻辑相反） */
  /* 注意：费用类热力颜色深浅 = 费用相对低/高，页面需有说明 */
  .heat-low-1 { background:#D1FAE5; color:#065F46; border:1px solid #A7F3D0; }  /* 相对最低 */
  .heat-low-2 { background:#A7F3D0; color:#065F46; }
  .heat-low-3 { background:#6EE7B7; color:#064E3B; }
  .heat-low-4 { background:#34D399; color:#064E3B; }
  .heat-low-5 { background:#059669; color:#fff; }                                /* 相对最高（费用最贵） */
  .heat-na    { background:#F3F4F6; color:#9CA3AF; font-size:12px; }

  .heat-cell .hv { font-size:14px; font-weight:800; line-height:1.2; }
  .heat-cell .hs { font-size:11px; opacity:.75; margin-top:3px; }

  /* 城市名列 */
  .city-col { font-weight:700; font-size:14px; color:var(--text-h); min-width:80px; }
  .city-col .city-sub { font-size:11px; color:var(--text-muted); font-weight:400; margin-top:2px; }

  /* Tooltip */
  .heat-cell[data-tip]:hover::after {
    content: attr(data-tip);
    position: absolute; bottom: calc(100% + 6px); left:50%;
    transform: translateX(-50%);
    background: #064E3B; color: #fff; font-size:11px;
    padding: 5px 10px; border-radius:7px; white-space:nowrap;
    z-index:99; pointer-events:none; box-shadow:0 4px 12px rgba(0,0,0,.2);
  }
</style>

<!-- 色阶说明（费用类：颜色越深 = 相对越贵） -->
<div class="card">
  <div style="font-size:13px;color:var(--text-muted);margin-bottom:12px">
    以下热力色阶反映本次对比城市间的<strong>相对费用高低</strong>，颜色越深表示该项费用相对较高。
    <br>⚠️ 颜色深浅仅为本次对比组内相对值，不代表城市好坏，实际消费因个人习惯差异很大。
  </div>
  <div style="display:flex;align-items:center;gap:8px;font-size:12px;">
    <div style="width:20px;height:14px;border-radius:4px;background:#D1FAE5;border:1px solid #A7F3D0"></div> 相对较低 &nbsp;
    <div style="width:20px;height:14px;border-radius:4px;background:#6EE7B7"></div> 中等 &nbsp;
    <div style="width:20px;height:14px;border-radius:4px;background:#059669"></div> 相对较高 &nbsp;
    <div style="width:20px;height:14px;border-radius:4px;background:#F3F4F6;border:1px solid #E5E7EB"></div> 暂无数据
  </div>
</div>

<div class="card" style="overflow-x:auto">
  <div class="card-title"><span class="icon icon-green">📊</span>城市生活成本对比矩阵</div>
  <table class="compare-table">
    <thead>
      <tr>
        <th>城市</th>
        <th>合租单间（月）</th>
        <th>餐饮月均</th>
        <th>交通月均</th>
        <th>月均总预算（中等档）</th>
        <th>学生交通优惠</th>
        <th>综合物价印象</th>
      </tr>
    </thead>
    <tbody>
      <!-- 大模型按实际城市数据填，heat-low-1 到 heat-low-5 按同列相对高低赋值（费用最低=heat-low-1） -->
      <tr>
        <td class="city-col">
          [城市1]
          <div class="city-sub">[主要高校区域]</div>
        </td>
        <td>
          <div class="heat-cell heat-low-[1-5]" data-tip="来源：[平台] · [日期]">
            <div class="hv">[X,XXX–X,XXX 元]</div>
            <div class="hs">[区域说明]</div>
          </div>
        </td>
        <td>
          <div class="heat-cell heat-low-[1-5]" data-tip="[说明]">
            <div class="hv">[XXX–X,XXX 元]</div>
            <div class="hs">食堂+外卖估算</div>
          </div>
        </td>
        <td>
          <div class="heat-cell heat-low-[1-5]">
            <div class="hv">[XX–XXX 元]</div>
            <div class="hs">[是否含优惠]</div>
          </div>
        </td>
        <td>
          <div class="heat-cell heat-low-[1-5]">
            <div class="hv">[X,XXX–X,XXX 元]</div>
            <div class="hs">不含学费住宿费</div>
          </div>
        </td>
        <td>
          <div class="heat-cell heat-na">
            <div class="hv" style="font-size:12px">[有/无/政策名称]</div>
          </div>
        </td>
        <td>
          <div class="heat-cell heat-low-[1-5]">
            <div class="hv">[高/中/低]</div>
            <div class="hs">[一句话说明]</div>
          </div>
        </td>
      </tr>
      <!-- 更多城市行... -->
    </tbody>
  </table>
</div>
```

---

## 模板 C — 单项费用 Markdown 回复（对话内）

```markdown
## [城市名] · [费用项，如"合租单间月租"]

**数据概览**
[1–2句直接回答]

**详细数据**
| 类型 | 费用区间 | 适用范围 | 来源 | 采集时间 |
|------|---------|---------|------|---------|
| 校内宿舍 | X,XXX 元/学年 | 官方收取 | [学校官网] | [年份] |
| 校外合租单间 | X,XXX–X,XXX 元/月 | [学校附近区域] | [贝壳/58同城] | [年月] |

**学生真实反馈**
- [来源]（[年份]）："[引用原话，保留口语]"

**数据说明**
- 挂牌价为参考，实际成交可能低5–15%
- 不同楼层/朝向/装修差异较大，建议实地看房

**来源**：[平台](URL) — [日期]
```

---

## 通用输出禁止项

❌ 不得说"XX城市太贵，不建议去"或"XX城市生活成本低，适合选择"（消费因人而异）
❌ 不得只给单一数字不标来源和时间
❌ 不得用全市均价代替学生实际花费（学生消费比城市均价低很多）
❌ 热力颜色说明必须注明"颜色深=相对较贵，仅为本次对比组内相对值"

✅ 推荐三档预算结构（基础/中等/舒适），让家庭自选参考档位
✅ 推荐突出标注学生交通优惠政策（容易被忽略的省钱点）
✅ 推荐引用在校学生原话，保留真实感（但标注来源和年份）
