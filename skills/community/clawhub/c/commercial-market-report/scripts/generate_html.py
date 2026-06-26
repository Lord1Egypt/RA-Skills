#!/usr/bin/env python3
"""
生成商业市调报告 HTML 演示稿（含 Chart.js 图表）
用法: python generate_html.py "项目名称" [site_area] [far] --output "输出路径"
"""
import sys, os, datetime, json

def generate_html(project_name, site_area=28000, far=3.5, competitors=None, output_dir=None):
    date_str = datetime.datetime.now().strftime('%Y年%m月')
    site_area = float(site_area)
    far = float(far)
    total_area = site_area * far
    commercial_area = total_area * 0.75
    dining = commercial_area * 0.35
    retail = commercial_area * 0.30
    experience = commercial_area * 0.20
    support = commercial_area * 0.10

    competitors = competitors or [
        {"name": "龙湖天街", "area": 80000},
        {"name": "和谐广场", "area": 60000},
        {"name": "万象城", "area": 100000},
        {"name": "高新万达", "area": 80000},
        {"name": "印象城", "area": 50000},
    ]

    # 图表数据 JSON，供前端 Chart.js 渲染
    chart_data = {
        "mix": {
            "labels": ["餐饮", "零售", "亲子体验", "体验娱乐", "配套服务"],
            "values": [round(dining), round(retail), round(experience), round(support), round(support)],
            "colors": ["#0052cc","#0066ee","#3377ff","#6699ff","#99bbff"]
        },
        "competitors": {
            "labels": [c["name"] for c in competitors],
            "values": [c["area"] for c in competitors],
            "colors": ["#dc2626","#f59e0b","#10b981","#3b82f6","#8b5cf6"]
        },
        "investment": {
            "labels": ["土地成本", "建安成本", "装修成本", "预备金"],
            "values": [12000, 18000, 8000, 4000],
            "colors": ["#0052cc","#0066ee","#3377ff","#6699ff"]
        },
        "sensitivity": {
            "labels": ["+20%", "+10%", "基准", "-10%", "-20%"],
            "values": [14.5, 12.0, 10.5, 8.2, 5.5],
            "colors": ["#10b981","#84cc16","#0052cc","#f59e0b","#dc2626"]
        }
    }

    charts_json = json.dumps(chart_data, ensure_ascii=False)

    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{project_name} — 市场调研汇报</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
:root {{
  --bg:#ffffff; --text:#1a1a2e; --accent:#0052cc; --accent-light:#e8f0fe; --gray:#6b7280; --border:#e5e7eb;
  --slide-padding: clamp(2rem,5vw,4rem); --body-size: clamp(0.85rem,1.8vw,1.1rem);
}}
* {{ box-sizing:border-box; margin:0; padding:0; }}
html,body {{ height:100%; overflow-x:hidden; font-family:'Inter','PingFang SC','Microsoft YaHei',sans-serif; background:var(--bg); color:var(--text); scroll-snap-type:y mandatory; scroll-behavior:smooth; }}
.slide {{ width:100vw; height:100vh; height:100dvh; overflow:hidden; scroll-snap-align:start; display:flex; flex-direction:column; padding:var(--slide-padding); }}
.slide-content {{ flex:1; display:flex; flex-direction:column; justify-content:center; max-height:100%; overflow:hidden; }}
.cover {{ background:var(--text); color:white; justify-content:center; }}
.cover h1 {{ font-size:clamp(2.5rem,6vw,5rem); font-weight:700; line-height:1.1; color:white; margin-bottom:1.5rem; }}
.cover .subtitle {{ font-size:clamp(1rem,2.5vw,1.5rem); font-weight:300; color:#93c5fd; margin-bottom:2rem; }}
.cover .meta {{ font-size:clamp(0.7rem,1.2vw,0.85rem); color:#9ca3af; display:flex; gap:2rem; flex-wrap:wrap; }}
.chapter-tag {{ font-size:clamp(0.6rem,1.2vw,0.8rem); letter-spacing:0.15em; text-transform:uppercase; color:var(--accent); margin-bottom:0.4rem; }}
h2 {{ font-size:clamp(1.4rem,3vw,2.2rem); font-weight:600; margin-bottom:0.4rem; }}
.divider {{ width:2.5rem; height:3px; background:var(--accent); margin:1rem 0 1.5rem; }}
.bullets {{ list-style:none; display:flex; flex-direction:column; gap:0.8rem; }}
.bullets li {{ display:flex; align-items:flex-start; gap:0.8rem; font-size:var(--body-size); line-height:1.5; }}
.bullets li::before {{ content:''; width:7px; height:7px; min-width:7px; background:var(--accent); border-radius:50%; margin-top:0.45em; }}
.grid-2 {{ display:grid; grid-template-columns:1fr 1fr; gap:1.5rem; margin-top:1rem; align-items:start; }}
.grid-2 .chart-wrap {{ background:var(--accent-light); border-radius:12px; padding:1rem; }}
.chart-title {{ font-size:0.8rem; font-weight:600; color:var(--accent); margin-bottom:0.5rem; text-align:center; }}
canvas {{ max-height:220px !important; }}
table {{ width:100%; border-collapse:collapse; font-size:var(--body-size); margin-top:1rem; }}
th {{ background:var(--accent); color:white; padding:0.6rem 1rem; text-align:left; font-weight:600; }}
td {{ padding:0.5rem 1rem; border-bottom:1px solid var(--border); }}
tr:nth-child(even) td {{ background:var(--accent-light); }}
.stats {{ display:flex; gap:2rem; flex-wrap:wrap; margin:1rem 0; }}
.stat {{ text-align:center; }}
.stat-num {{ font-size:clamp(1.8rem,4vw,3rem); font-weight:700; color:var(--accent); line-height:1; }}
.stat-label {{ font-size:clamp(0.6rem,1vw,0.75rem); color:var(--gray); text-transform:uppercase; letter-spacing:0.08em; margin-top:0.3rem; }}
.closing {{ background:var(--text); color:white; justify-content:center; align-items:center; text-align:center; }}
.closing h2 {{ color:white; font-size:clamp(2rem,5vw,4rem); }}
.closing .divider {{ background:#60a5fa; margin:1.5rem auto; }}
.closing p {{ color:#d1d5db; font-size:var(--body-size); }}
.nav-dots {{ position:fixed; right:1.5rem; top:50%; transform:translateY(-50%); display:flex; flex-direction:column; gap:0.5rem; z-index:100; }}
.nav-dots button {{ width:7px; height:7px; border-radius:50%; border:none; background:var(--border); cursor:pointer; transition:all 0.2s; }}
.nav-dots button.active {{ background:var(--accent); transform:scale(1.3); }}
.progress-bar {{ position:fixed; top:0; left:0; height:3px; background:var(--accent); z-index:200; width:0%; transition:width 0.3s; }}
@media(max-width:768px) {{ .grid-2 {{ grid-template-columns:1fr; }} .nav-dots {{ display:none; }} }}
</style>
</head>
<body>
<div class="progress-bar" id="progress"></div>
'''

    # === SLIDE 1: COVER ===
    html += f'''
<section class="slide cover">
  <div class="slide-content">
    <h1>{project_name}</h1>
    <div class="subtitle">市场调研汇报</div>
    <div class="meta">
      <span>📍 济南槐荫区</span>
      <span>📐 用地面积：{site_area:,.0f} m²</span>
      <span>📐 可建面积：{total_area:,.0f} m²</span>
      <span>📅 {date_str}</span>
    </div>
  </div>
</section>'''

    # === SLIDE 2: TOC ===
    html += '''
<section class="slide">
  <div class="slide-content">
    <div class="chapter-tag">CONTENTS</div>
    <h2>汇报目录</h2>
    <div class="divider"></div>
    <div style="display:flex;flex-direction:column;gap:0.8rem;margin-top:1rem">
      <div style="display:flex;align-items:center;gap:1rem">
        <span style="font-size:clamp(1.2rem,3vw,1.8rem);font-weight:700;color:var(--accent);min-width:2rem">01</span>
        <span style="font-size:var(--body-size)">项目概况与区域分析</span>
      </div>
      <div style="display:flex;align-items:center;gap:1rem">
        <span style="font-size:clamp(1.2rem,3vw,1.8rem);font-weight:700;color:var(--accent);min-width:2rem">02</span>
        <span style="font-size:var(--body-size)">竞争市场分析（含SWOT）</span>
      </div>
      <div style="display:flex;align-items:center;gap:1rem">
        <span style="font-size:clamp(1.2rem,3vw,1.8rem);font-weight:700;color:var(--accent);min-width:2rem">03</span>
        <span style="font-size:var(--body-size)">消费者调研分析</span>
      </div>
      <div style="display:flex;align-items:center;gap:1rem">
        <span style="font-size:clamp(1.2rem,3vw,1.8rem);font-weight:700;color:var(--accent);min-width:2rem">04</span>
        <span style="font-size:var(--body-size)">商业定位与业态组合</span>
      </div>
      <div style="display:flex;align-items:center;gap:1rem">
        <span style="font-size:clamp(1.2rem,3vw,1.8rem);font-weight:700;color:var(--accent);min-width:2rem">05</span>
        <span style="font-size:var(--body-size)">财务测算</span>
      </div>
      <div style="display:flex;align-items:center;gap:1rem">
        <span style="font-size:clamp(1.2rem,3vw,1.8rem);font-weight:700;color:var(--accent);min-width:2rem">06</span>
        <span style="font-size:var(--body-size)">结论与设计建议</span>
      </div>
    </div>
  </div>
</section>'''

    # === SLIDE 3: 项目概况 ===
    html += f'''
<section class="slide">
  <div class="slide-content">
    <div class="chapter-tag">CHAPTER 01</div>
    <h2>项目概况与区域分析</h2>
    <div class="divider"></div>
    <div class="stats">
      <div class="stat"><div class="stat-num">{site_area:,.0f}</div><div class="stat-label">用地面积 m²</div></div>
      <div class="stat"><div class="stat-num">{far}</div><div class="stat-label">容积率</div></div>
      <div class="stat"><div class="stat-num">{total_area:,.0f}</div><div class="stat-label">可建面积 m²</div></div>
      <div class="stat"><div class="stat-num">{commercial_area:,.0f}</div><div class="stat-label">商业面积 m²</div></div>
    </div>
    <ul class="bullets" style="margin-top:1.5rem">
      <li>区位优势：济南西部门户，槐荫区核心，地铁上盖，客流导入便捷</li>
      <li>交通可达：经十路、齐鲁大道，BRT+地铁多维交通，停车充足</li>
      <li>配套成熟：省立医院西院、多所学校、政务中心环伺</li>
      <li>发展趋势：济南西进战略核心承载区，城市功能加速完善</li>
    </ul>
  </div>
</section>'''

    # === SLIDE 4: 竞品分析 ===
    html += '''
<section class="slide">
  <div class="slide-content">
    <div class="chapter-tag">CHAPTER 02</div>
    <h2>竞争市场分析 — 竞品体量对比</h2>
    <div class="divider"></div>
    <div class="grid-2">
      <div class="chart-wrap"><div class="chart-title">周边竞品体量（m²）</div><canvas id="competitor-bar"></canvas></div>
      <div>
        <ul class="bullets">
          <li>龙湖济南西城天街：8万㎡，距本项目1.5km，餐饮+亲子+零售</li>
          <li>和谐广场：6万㎡，距本项目2.0km，全业态综合</li>
          <li>济南万象城：10万㎡，距本项目3.5km，城市高端型</li>
          <li>高新万达广场：8万㎡，距本项目4.0km，区域综合型</li>
          <li>印象城：5万㎡，距本项目3.0km，年轻时尚定位</li>
        </ul>
      </div>
    </div>
  </div>
</section>'''

    # === SWOT Slide ===
    html += '''
<section class="slide">
  <div class="slide-content">
    <div class="chapter-tag">CHAPTER 02</div>
    <h2>竞争市场分析 — SWOT 分析</h2>
    <div class="divider"></div>
    <div class="grid-2">
      <div style="background:#f0fdf4;border-radius:12px;padding:1rem;border-left:4px solid #16a34a">
        <div style="font-weight:700;color:#16a34a;font-size:0.9rem;margin-bottom:0.5rem">✅ S 优势</div>
        <ul class="bullets" style="gap:0.5rem">
          <li>区位优势：西部门户，地铁上盖</li>
          <li>政策支持：西进战略核心承载区</li>
          <li>配套成熟：医疗/教育/政务齐全</li>
        </ul>
      </div>
      <div style="background:#fef2f2;border-radius:12px;padding:1rem;border-left:4px solid #dc2626">
        <div style="font-weight:700;color:#dc2626;font-size:0.9rem;margin-bottom:0.5rem">⚠️ W 劣势</div>
        <ul class="bullets" style="gap:0.5rem">
          <li>区域认知度：新区分需培育期</li>
          <li>竞品分流：龙湖/万达先发优势</li>
          <li>招商难度：品牌商家入驻门槛</li>
        </ul>
      </div>
      <div style="background:#eff6ff;border-radius:12px;padding:1rem;border-left:4px solid #2563eb">
        <div style="font-weight:700;color:#2563eb;font-size:0.9rem;margin-bottom:0.5rem">🔮 O 机会</div>
        <ul class="bullets" style="gap:0.5rem">
          <li>市场缺口：精品商业供给不足</li>
          <li>人口导入：新建住宅持续交付</li>
          <li>消费升级：品质需求持续增长</li>
        </ul>
      </div>
      <div style="background:#fff7ed;border-radius:12px;padding:1rem;border-left:4px solid #ea580c">
        <div style="font-weight:700;color:#ea580c;font-size:0.9rem;margin-bottom:0.5rem">⚡ T 威胁</div>
        <ul class="bullets" style="gap:0.5rem">
          <li>竞品分流：体量竞争压力</li>
          <li>电商冲击：实体商业受挤压</li>
          <li>成本上涨：地价/建安成本上升</li>
        </ul>
      </div>
    </div>
  </div>
</section>'''

    # === SLIDE 5: 消费者画像 ===
    html += '''
<section class="slide">
  <div class="slide-content">
    <div class="chapter-tag">CHAPTER 03</div>
    <h2>消费者调研 — 客群画像</h2>
    <div class="divider"></div>
    <div class="grid-2">
      <div class="chart-wrap"><div class="chart-title">客群年龄分布</div><canvas id="consumer-pie"></canvas></div>
      <div>
        <ul class="bullets">
          <li><strong>核心客群</strong>：25-45岁，白领/公务员，家庭年收入15-30万</li>
          <li><strong>次级客群</strong>：银发群体（区域老龄化程度高）、亲子家庭（儿童消费刚需）</li>
          <li><strong>消费偏好</strong>：餐饮高频（网红餐厅/聚餐）、亲子刚需、体验升级</li>
          <li><strong>业态优先级</strong>：🔥精品超市+餐饮  ⚡影院健身  ○美容文创</li>
        </ul>
      </div>
    </div>
  </div>
</section>'''

    # === SLIDE 6: 业态配比 ===
    html += f'''
<section class="slide">
  <div class="slide-content">
    <div class="chapter-tag">CHAPTER 04</div>
    <h2>商业定位 — 业态面积配比</h2>
    <div class="divider"></div>
    <div class="grid-2">
      <div class="chart-wrap"><div class="chart-title">业态面积配比（商业{commercial_area:,.0f} m²）</div><canvas id="mix-pie"></canvas></div>
      <div>
        <table>
          <tr><th>业态</th><th>占比</th><th>面积 m²</th></tr>
          <tr><td>餐饮</td><td>35%</td><td>{dining:,.0f}</td></tr>
          <tr><td>零售</td><td>30%</td><td>{retail:,.0f}</td></tr>
          <tr><td>亲子体验</td><td>20%</td><td>{experience:,.0f}</td></tr>
          <tr><td>体验娱乐</td><td>10%</td><td>{support:,.0f}</td></tr>
          <tr><td>配套服务</td><td>5%</td><td>{support:,.0f}</td></tr>
        </table>
      </div>
    </div>
  </div>
</section>'''

    # === SLIDE 7: 投资估算 ===
    html += '''
<section class="slide">
  <div class="slide-content">
    <div class="chapter-tag">CHAPTER 05</div>
    <h2>财务测算 — 投资构成</h2>
    <div class="divider"></div>
    <div class="grid-2">
      <div class="chart-wrap"><div class="chart-title">总投资构成（万元）</div><canvas id="invest-pie"></canvas></div>
      <div>
        <table>
          <tr><th>成本项目</th><th>金额（万元）</th></tr>
          <tr><td>土地成本</td><td>12,000</td></tr>
          <tr><td>建安成本</td><td>18,000</td></tr>
          <tr><td>装修成本</td><td>8,000</td></tr>
          <tr><td>预备金</td><td>4,000</td></tr>
          <tr><td><strong>合计</strong></td><td><strong>42,000</strong></td></tr>
        </table>
      </div>
    </div>
  </div>
</section>'''

    # === SLIDE 8: 敏感性分析 ===
    html += '''
<section class="slide">
  <div class="slide-content">
    <div class="chapter-tag">CHAPTER 05</div>
    <h2>财务测算 — 敏感性分析</h2>
    <div class="divider"></div>
    <div class="grid-2">
      <div class="chart-wrap"><div class="chart-title">不同租金下的IRR对比</div><canvas id="sensitivity-bar"></canvas></div>
      <div>
        <ul class="bullets">
          <li><strong>基准情景</strong>：IRR 10-12%，回收期8-10年</li>
          <li><strong>乐观情景（+10%租金）</strong>：IRR 13-15%，回收期7-8年</li>
          <li><strong>悲观情景（-10%租金）</strong>：IRR 7-9%，回收期10-12年</li>
          <li><strong>风险情景（-20%租金）</strong>：IRR 4-6%，回收期超过15年</li>
          <li><strong>盈亏平衡点</strong>：出租率约75%</li>
        </ul>
      </div>
    </div>
  </div>
</section>'''

    # === SLIDE 9: 结论 ===
    html += '''
<section class="slide">
  <div class="slide-content">
    <div class="chapter-tag">CHAPTER 06</div>
    <h2>结论与设计建议</h2>
    <div class="divider"></div>
    <div class="grid-2">
      <div>
        <div style="font-weight:600;color:var(--accent);margin-bottom:0.8rem">✅ 核心结论</div>
        <ul class="bullets">
          <li>市场可行性良好，4万㎡体量适中</li>
          <li>差异化定位存在竞争空间</li>
          <li>强餐饮+强亲子是核心竞争力</li>
          <li>需与龙湖/万达形成错位</li>
        </ul>
      </div>
      <div>
        <div style="font-weight:600;color:var(--accent);margin-bottom:0.8rem">🏗️ 设计建议</div>
        <ul class="bullets">
          <li>街区+盒子组合，兼顾休闲与品质</li>
          <li>双中庭+环形动线，避免商业死角</li>
          <li>亲子主题空间作为聚客引擎</li>
          <li>800-1000个停车位满足家庭需求</li>
          <li>分期开发，一期F1-F3优先开业</li>
        </ul>
      </div>
    </div>
  </div>
</section>'''

    # === SLIDE 10: CLOSING ===
    html += f'''
<section class="slide closing">
  <div class="slide-content">
    <h2>谢谢观看</h2>
    <div class="divider"></div>
    <p>{project_name} · 市场调研汇报</p>
    <p style="margin-top:1.5rem;font-size:0.7rem;color:#6b7280">{date_str} · 仅供参考，以最终调研为准</p>
  </div>
</section>'''

    # === CHARTS JS ===
    html += f'''
<script>
const DATA = {charts_json};

function makePie(id, data) {{
  new Chart(document.getElementById(id), {{
    type: 'pie',
    data: {{
      labels: data.labels,
      datasets: [{{
        data: data.values,
        backgroundColor: data.colors,
        borderWidth:0,
      }}]
    }},
    options: {{
      responsive: true,
      maintainAspectRatio: true,
      plugins: {{
        legend: {{ position:'bottom', labels: {{ font:{{size:11}}, padding:12 }} }}
      }}
    }}
  }});
}}

function makeBar(id, data, yLabel='') {{
  new Chart(document.getElementById(id), {{
    type: 'bar',
    data: {{
      labels: data.labels,
      datasets: [{{
        label: yLabel || '数值',
        data: data.values,
        backgroundColor: data.colors,
        borderRadius: 4,
      }}]
    }},
    options: {{
      responsive: true,
      maintainAspectRatio: true,
      plugins: {{ legend: {{ display: false }} }},
      scales: {{ y: {{ beginAtZero: true }} }}
    }}
  }});
}}

// Render all charts
makeBar('competitor-bar', DATA.competitors, '体量 m²');
makePie('consumer-pie', {{labels:['25-35岁','35-45岁','45-55岁','55岁以上'],values:[30,35,25,10],colors:['#0052cc','#3377ff','#6699ff','#99bbff']}});
makePie('mix-pie', DATA.mix);
makePie('invest-pie', DATA.investment);
makeBar('sensitivity-bar', DATA.sensitivity, 'IRR %');

// Nav dots + progress
const slides = document.querySelectorAll('.slide');
const progress = document.getElementById('progress');
const nav = document.createElement('div'); nav.className='nav-dots'; document.body.appendChild(nav);
slides.forEach((_,i) => {{ const btn = document.createElement('button'); btn.title=`Slide ${{i+1}}`; btn.onclick = () => slides[i].scrollIntoView({{behavior:'smooth'}}); nav.appendChild(btn); }});
window.addEventListener('scroll', () => {{
  progress.style.width = (window.scrollY / (document.documentElement.scrollHeight - window.innerHeight) * 100) + '%';
  let cur = 0; slides.forEach((s,i) => {{ if(s.getBoundingClientRect().top < window.innerHeight/2) cur = i; }});
  nav.querySelectorAll('button').forEach((b,i) => b.classList.toggle('active', i===cur));
}});
document.addEventListener('keydown', e => {{
  let cur = [...slides].findIndex(s => {{ const r=s.getBoundingClientRect(); return r.top>=0 && r.top<window.innerHeight/2; }});
  if(e.key==='ArrowDown'||e.key==='ArrowRight'||e.key===' ') {{ e.preventDefault(); slides[Math.min(cur+1,slides.length-1)].scrollIntoView({{behavior:'smooth'}}); }}
  if(e.key==='ArrowUp'||e.key==='ArrowLeft') {{ e.preventDefault(); slides[Math.max(cur-1,0)].scrollIntoView({{behavior:'smooth'}}); }}
}});
</script>
</body></html>'''

    filename = f'{project_name}_汇报PPT_{datetime.datetime.now().strftime("%Y%m%d")}.html'
    out_path = os.path.join(output_dir, filename) if output_dir else filename
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"HTML_SAVED:{out_path}")
    return out_path

if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('project_name', nargs='?', default='商业项目')
    p.add_argument('site_area', nargs='?', default='28000')
    p.add_argument('far', nargs='?', default='3.5')
    p.add_argument('--output', dest='output_dir', default=None)
    a = p.parse_args()
    generate_html(project_name=a.project_name, site_area=a.site_area, far=a.far, output_dir=a.output_dir)
