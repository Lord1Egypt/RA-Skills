---
name: "battle-report-briefing"
description: "为历史/军事战役制作移动端一屏简报（PNG 配图），含国旗 / 战术总结 / 多源核对"
version: "v1"
date: "2026-08-10T16:31:07.481Z"
---

# 战报简报 · Battle Report Briefing

把历史战役 / 军事冲突做成 **移动端单屏战术简报**（PNG 配图）。适用于：
- 用户要求"战报 / 战役简报 / 作战简报 / 战术可视化"
- 任何有公开档案的战役（解放战争、抗日、二战、近代冲突等）
- 双方对峙（PLA vs KMT / A vs B）或单方报告（装备损失、后勤数据等）

---

## 🎯 设计原则（核心）

1. **移动端一屏**：宽 390px（iPhone 标准），不放大能看全
2. **配色统一**：每个阵营一种主色，**绝不混用**
   - 解放战争：解放军 **中国红 `#C8102E`** + 国军 **青天白日蓝 `#003E7E`**
   - 抗日战争：可考虑 **`#8B0000` 抗战红** + **日章旗白红**
   - 自定义：双方各选一个主色，金色 `#FFD700` 做装饰
3. **必须含军旗**：内联 SVG 画双方旗帜（核心专业感）
   - 解放军：八一军旗（红底 + 金星 + "八一"）
   - 国军：青天白日满地红旗（红底 + 蓝角 + 白日 12 道光芒）
   - 缺数据时：单色 + 阵营徽章
4. **每日战损表 → 砍掉**：默认不画日报表格，重要数字进 KPI 卡片
5. **战术总结 → 必留**：5 条 bullet + 当时指挥官原话（如"不要伤亡数字，我只要塔山"）
6. **多源核对**：列 10+ 个独立来源（维基中英 + 百度百科×3 + 战史专著×3 + 档案×2）

---

## 📐 版面结构（自上而下 7 段）

```
┌──────────────────────────────────┐
│ ① HEADER                        │  红渐变 + ★ + 战役名 + 时间副标 + 简报编号
├──────────────────────────────────┤
│ ② MATCHUP（双方对决框）          │  双方旗帜 + 阵营名 + VS + 兵力/火力对比
├──────────────────────────────────┤
│ ③ 4 KPI 卡片（核心数据）         │  双方伤亡 / 交换比 / 关键装备等
├──────────────────────────────────┤
│ ④ 战术总结（白底卡片）           │  5 条 bullet + 指挥官原话引用
├──────────────────────────────────┤
│ ⑤ 双方指挥链（红/蓝对照表）      │  精简到 5~6 行核心将领
├──────────────────────────────────┤
│ ⑥ 信息源（暗色页脚）             │  13 个独立来源一行流
└──────────────────────────────────┘
```

**单方报告**时：砍掉 ② 段，全面用主色；其他结构不变。

---

## 🔧 工作流

### Step 1 · 多源研究
- ✅ 必查：维基百科（中文 + 英文）、百度百科（战役 + 英雄部队）
- ✅ 必查：官方战史专著（《解放军战史》《四野战史》《亲历记》《解放战争史》等）
- ✅ 必查：档案（国防大学档 / 国史馆 / 各军档案馆）
- ✅ 目标：≥ 10 个独立来源，关键数字（如总伤亡）≥ 3 源交叉印证
- ⚠️ 个体指挥官姓名/营连级牺牲：通常仅有"集体英模"记录，单个人名需查各团战史，必须标注置信度

### Step 2 · HTML 草稿
- 内联 SVG 画旗帜（60×40px 标准）
- 用语义化 class：`kpi.p` / `kpi.k` / `cmd-head.p` / `cmd-head.k`
- 单页用 `<div class="page" style="width:390px;background:#FDF6EC">`，子元素都包在 `.page` 内
- 字体：`font-family: -apple-system, "PingFang SC", "Microsoft YaHei", sans-serif`
- 数字字体：`"SF Mono", monospace` 等宽，金额 / 伤亡对齐全用 tabular-nums
- 配色卡片：背景用主题色 `#C8102E`/`#003E7E`，文字用白或深色对比

### Step 3 · Playwright 截图
- 用 `chromium.launch({ headless: true, executablePath: '/Users/tom.chang/.openclaw/browser/openclaw/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing' })`
- viewport 390×800、deviceScaleFactor 2
- 走 `file://` 路径 + `fullPage: true`
- 输出 PNG 路径示例：`/tmp/openclaw/sent/<战役名>.png`

### Step 4 · 推送给用户
- 用 `message` 工具 `action=send`，target=user_id
- 文案结构：`vN 简报名 + 改动说明 + 询问反馈`
- 附件 `attachments: [{ type:'image', media:'jpg/png 绝对路径', name:'...' }]`
- ⚠️ HTML 文件必须 cp 到 `/tmp/openclaw/sent/`（Kangyao profile 的 hostReadCapability 信任根目录），参考 TOOLS.md

---

## 🎨 配色速查（可直接复用）

| 阵营 | 主色 | 装饰色 | 暗色 |
|---|---|---|---|
| 解放军（PLA） | `#C8102E` 中国红 | `#FFD700` 金 | `#8B0000` |
| 国军（ROC） | `#003E7E` 青天白日蓝 | `#FFFFFF` 白日光 | `#002a55` |
| 日军（IJA） | `#FFFFFF` 白 | `#BC002D` 日之丸红 | `#7a0019` |
| 美军（USA） | `#3C3B6E` 蓝 | `#B31942` 红 | `#1a1a40` |
| 苏军（USSR） | `#8B0000` | `#FFD700` | `#4a0000` |

页脚固定：`background:#8B0000; color:#FFE4E1;`，"信息源"标签用 `#FFD700` 高亮。

---

## 📝 段头样板（直接复制可用）

```html
<div class="section bordered">
  <div class="section-title n">战术总结</div>
  <div class="tactic">
    <ul>
      <li><b>配置：</b>每师三梯队、1/3~2/3 兵力作预备队 —— 保证连续反冲锋能力</li>
      <li><b>战法：</b>海空轰炸时全转入地下坑道 —— 顶住 5,000+ 枚重磅炸弹</li>
      <li><b>转折：</b>10/12 休战日 4 纵做"战评" —— 总结出针对"波浪式"冲锋的克制战法</li>
      <li><b>意志：</b>34 团连级干部打光、反复补员 4 次，全团伤亡近半仍死守</li>
      <li><b>指挥：</b>团营干部靠前 —— 林彪下令"我不要伤亡数字，我只要塔山"</li>
    </ul>
    <div class="quote">
      "模范的英勇顽强的防御战" —— 林彪、罗荣桓战评<br>
      "对攻击锦州、取得调整部署与攻击准备时间，起了决定的作用"
    </div>
  </div>
</div>
```

---

## ✅ 验收 Checklist

发布前自检：

- [ ] 配色统一（无主色混用）
- [ ] 双方旗帜 SVG 正确渲染（青天白日 12 光芒清晰）
- [ ] 单卡 4 KPI 数字 ≥ 10 个来源交叉印证
- [ ] 战术总结 ≥ 5 条 bullet + 1 句指挥官原话
- [ ] 指挥链精简到 5~6 行核心将领
- [ ] 信息源 ≥ 10 个，列底成一行
- [ ] 截图分辨率 ≥ 780×N px（2x DPR）
- [ ] PNG 文件落到 `/tmp/openclaw/sent/` 才能发
- [ ] 置信度提示：核心数字 ✅ 高、个体指挥姓名 ⚠️ 需查战史

---

## 🚫 已知坑

- ❌ **不要用 `TMP` 根目录发图** — Kangyao profile 报 `OutboundDeliveryError: Local media path is not under an allowed directory`
- ❌ **不要写每日战损明细** — 压缩到 4 KPI 卡片即可（用户反馈：太稠密）
- ❌ **不要省略战术总结** — 用户明确说"必不可少的"
- ❌ **不要混用主色** — 例如红色 KPI 块里加蓝色 icon，会被判"不专业"
- ❌ **不要省略军旗** — 用户原话："连军队旗帜都没有非常不专业啊兄弟"

---

## 🔗 相关资源

- 工具根：TOOLS.md（Kangyao hostReadCapability 信任根目录 = `/tmp/openclaw/`）
- HTML→PNG 工具：Playwright + Chromium for Testing（已装在 `/opt/homebrew/lib/node_modules/gsd-pi/node_modules/playwright`）
- 解放战争数据来源：维基百科、百度百科、《中国人民解放军战史简编》、《四野战史》、《辽沈战役亲历记》、国史馆档案
