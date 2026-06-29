# 示例输出：竞品周报

用模拟的两份周一数据（Socialinsider CSV + Agent-Reach YouTube JSON）跑的真实输出。

---

## 输入

### A. Socialinsider 导出的竞品 IG/TT/FB 数据（简化）
```
brand,platform,followers,followers_change,avg_engagement_rate,top_post_likes,top_post_topic
messick_farm_equipment,Instagram,48200,+820,4.1%,3100,"Kubota M7 现场演示"
messick_farm_equipment,TikTok,31000,+2400,7.8%,18000,"拖拉机翻新前后对比"
kramp_uk,Instagram,22500,+150,1.9%,640,"配件仓库实拍"
kramp_uk,Facebook,68000,+90,0.8%,210,"产品目录更新"
partsasap,Instagram,15300,+460,3.4%,1200,"John Deere 维修教程"
tvhgroup,Facebook,71200,+110,1.1%,340,"展会回顾"
yeswelder,Instagram,89000,+1900,5.2%,7800,"焊接技巧短视频"
brokentractorllc,TikTok,12400,+3100,11.2%,42000,"老拖拉机起死回生"
```

### B. Agent-Reach 抓的竞品 YouTube 数据（简化）
```
messick_farm_equipment: "Kubota SVL75 full walkaround" 24000 views, 980 likes
messick_farm_equipment: "How to grease your loader" 51000 views, 2300 likes
partsasap: "John Deere fuel filter change" 38000 views, 1600 likes
brokentractorllc: "Rescuing a seized engine PART 3" 112000 views, 8400 likes
```

---

## 输出（Skill 生成）

### ① 账号体量榜

按粉丝总量看，头部是 yeswelder（IG 89K）、tvhgroup（FB 71.2K）、kramp_uk（FB 68K）。但**增长**才是更值得看的信号：

- **brokentractorllc** TikTok 周增 +3,100（+25% 量级），增长最快
- **messick_farm_equipment** TikTok 周增 +2,400，IG +820，双平台齐涨
- **yeswelder** IG 周增 +1,900

增长几乎全集中在 TikTok 和短视频内容上，FB 普遍停滞（kramp_uk FB 仅 +90、tvhgroup FB +110）。

### ② 互动率排名

互动率（比粉丝数更能反映内容质量）：

1. **brokentractorllc** TikTok 11.2% —— 断层第一
2. **messick_farm_equipment** TikTok 7.8%
3. **yeswelder** IG 5.2%
4. **messick_farm_equipment** IG 4.1%
5. **partsasap** IG 3.4%

垫底的是传统 FB 内容：kramp_uk FB 0.8%、tvhgroup FB 1.1%。**FB 在竞品里普遍是低互动平台，TikTok 是高互动主战场。**

### ③ 本周 Top 内容（跨平台）

1. **brokentractorllc** TikTok"老拖拉机起死回生" 42K赞 / YouTube"Rescuing a seized engine PART 3" 112K播放 —— 修复改造类连载，叙事性强，是本周最大赢家
2. **messick_farm_equipment** TikTok"拖拉机翻新前后对比" 18K赞 —— before/after 形式
3. **yeswelder** IG"焊接技巧短视频" 7.8K赞 —— 实用技巧短视频
4. **messick** YouTube"How to grease your loader" 51K播放 —— 基础保养教程
5. **partsasap** YouTube"John Deere fuel filter change" 38K播放 —— 具体维修教程

共性：**修复/改造连载 + before/after + 实用教程**，都是"看得见过程"的内容。

### ④ 内容策略洞察

- **修复改造连载是本周最强形式**：brokentractorllc 的"起死回生 PART 3"在 TikTok 和 YouTube 双爆，说明连载式修复故事能持续吸量
- **before/after 对比百试不爽**：messick 的翻新对比、brokentractorllc 的起死回生，都用了视觉冲击强的前后对比
- **教程类稳定但不爆**：messick 和 partsasap 的保养/维修教程播放稳定（38-51K），适合做基本盘，不指望爆款
- **FB 是被放弃的平台**：所有竞品 FB 互动率都低于 1.2%，没人在 FB 上认真投入

### ⑤ 给 FridayParts 的 3 条行动建议

1. **做一个修复改造连载**：学 brokentractorllc，挑一台旧设备做"起死回生"系列，过程中自然植入 FridayParts 配件。这是本周验证过的最强形式，TikTok+YouTube 双发。
2. **多用 before/after 形式**：现有的维修教程内容，改成"换件前 vs 换件后"的对比呈现，视觉冲击更强。配件电商天然适合这个形式（旧件腐蚀 vs 新件）。
3. **FB 别再花大力气**：竞品 FB 全线低迷，FridayParts 的 FB 可以维持基本更新（用 fp_x_sync 同步即可），把内容产能集中到 TikTok 和短视频。

---

## 这版输出的亮点

| 特点 | 说明 |
|------|------|
| 不念数据 | 从数据里读出"增长全在TikTok、FB全员低迷"等结论 |
| 增长优先 | 没只看粉丝绝对值，突出谁在涨、涨在哪 |
| Top内容找共性 | 不只列5条，总结出"看得见过程"的规律 |
| 建议可落地 | "做修复连载""改before/after""FB别投入"——能直接执行 |
| 标来源 | 每条数据注明来自哪个平台 |
| 跨源合并 | brokentractorllc 的 TikTok+YouTube 数据合在一起看，不割裂 |
