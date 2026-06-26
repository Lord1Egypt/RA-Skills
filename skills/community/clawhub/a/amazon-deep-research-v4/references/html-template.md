# HTML报告模板 V4

## 技术栈
- ECharts 5 CDN (SVG renderer)
- 内联CSS，无框架依赖
- 数据以JSON嵌入`<script>`
- 字体: -apple-system, "PingFang SC", sans-serif

## 报告结构

```
标题 + 数据来源标注(AMZScout/西柚/1688/WIPO)
常量栏(实时汇率+日期/运费/退货/广告/FBA来源)
数据来源图例(蓝=AMZScout, 橙=西柚, 红=1688)
7项毛利公式框(黑底白字, monospace)
KPI卡片行(合格数/平均毛利/费用来源/流量来源)
产品明细表(全部7项扣除拆解 + 西柚关键词 + IP风险)
数据来源说明
```

## 数据来源标注（必须在报告顶部）

```html
<div class="src-legend">
  <b>数据来源:</b>
  <span class="s-amz">AMZScout</span> FBA+佣金、月销、重量
  <span class="s-xy">西柚找词</span> 流量分、广告占比、关键词
  <span class="s-1688">1688以图搜</span> 采购价、下单链接
</div>
```

## 产品明细表列

```
#, 主图(Amazon真实), ASIN(链接), 产品名称,
AMZScout数据(月销/BSR/评分/FBA/佣金拆分),
西柚流量(流量分/自然%/广告%),
核心关键词(SV/CPC),
售价($),
1688采购(¥+链接),
供应商名,
①成本, ②运费, ③关税, ④总费(FBA+佣金), ⑤退货, ⑥广告,
净利($), 毛利率(%色标),
IP风险(🟢/🟡/🔴 + 详情 + 认证)
```

## 关键CSS规则

```css
body { background:#f0f2f5; font-family:-apple-system,"PingFang SC",sans-serif; font-size:12px }
.bar { background:#1a1a2e; color:#fff }
.formula { background:#2c3e50; color:#ecf0f1; font-family:monospace }
th { background:#1a1a2e; color:#fff; position:sticky; top:0 }
/* 数据来源色块 */
.s-amz { background:#e8f4fd; color:#0d47a1 }
.s-xy { background:#fff8e1; color:#e65100 }
.s-1688 { background:#fce4ec; color:#c62828 }
/* 毛利色标 */
.mg-g { background:#d4edda; color:#155724 } /* ≥35% */
.mg-y { background:#fff3cd; color:#856404 } /* ≥20% */
/* IP色标 */
.ip-l { background:#27ae60; color:#fff }
.ip-m { background:#f39c12; color:#fff }
/* 1688价格橙色 */
.src-p { color:#e67e22; font-weight:700 }
/* 主图 */
.img { width:56px; height:56px; object-fit:contain; border-radius:4px; border:1px solid #eee }
```

## 图表配置

1. **品类饼图**: donut型, 图例右侧
2. **价格vs毛利散点**: X=售价, Y=毛利率, 色标按毛利等级

## 生成方式

Python直接拼接HTML字符串 + JSON数据嵌入
输出: `output/amazon-research-v4.html`
