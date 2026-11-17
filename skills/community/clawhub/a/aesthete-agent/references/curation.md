> 何时读我:理解选板方法论、要扩充调色板库时。
> 最短路径:三层过滤→扩库流水线→已知边界。
> 回 INDEX:SKILL.md「参考文档(30 秒路由)」。

# 选板方法论与扩库流水线

## 核心问题:你怎么知道哪些配色好看?

**诚实回答:没有任何先验方法能判定"好看"。** 库的可靠性来自三层过滤,每层只对自己能负责的部分负责:

### 第 1 层:人群信号(谁选的?)

- 数据只收 **源站官方榜单页**:trending / popular / latest(各 48,站方排序即大众投票结果)。
- **点赞分层(tier)**:★★★ ≥50K、★★ ≥20K、★ >0、new=0。likes 是"被收藏欲"——万人收藏不代表适配你的医学图表,但它筛掉了大多数新手垃圾。
- **跨页重复(occurrences)**:同一调色板同时上 trending 和 popular = 更稳定的背书;只出现一次的新板标 new 降权。

### 第 2 层:客观质量门(机器只拦"坏",不判"好")

流水线(`scripts/build_library.py`,随包发布)执行的确定性检查:

| 门 | 规则 | 处置 | 理由 |
|---|---|---|---|
| FLAT-LIGHTNESS | 明度极差 <0.15 | **拒绝** | 无明度架构=文字/背景角色必然失败 |
| NO-READABLE-PAIR | 任意两色对比度最高 <4.5:1 | **拒绝** | 连一组可读文字对都凑不出 |
| CB-COLLISION-RISK | 色盲模拟后最小两两分离 <0.02(oklab) | 打旗 | 图表场景需换明度策略,普通 UI 未必致命 |
| SLOP-SIGNATURE | Tailwind 默认族成员 / 双中饱和紫(oklch 色相 275-330°) | 打旗 | 中位数陷阱,默认绕行 |
| NARROW-LIGHTNESS | 极差 <0.25 | 打旗 | 能用但架构受限 |

首批战果:116 去重 → **87 入库 / 29 拒绝**(被拒的都是真坏:如 Golden Summer Fields 全板最高对比 2.15:1)。打旗不删——红旗留给使用时判断,库保持诚实。

### 第 3 层:使用时上下文自审(最终裁决)

色板离开上下文没有对错。六步法第 6 步(card mockup + emitImage 目检)+ 用户确认才是"好看"的最终判定点。库的作用是把**起跑线**从"模型裸想"提高到"被人群筛选+机器验过架构"。

## 扩库流水线

```bash
# 1. 收割(浏览器配方见 harvest-playbook.md):保存到 palette-research/
#    命名:trending_raw.json / popular2_raw.json / latest_raw.json
# 2. 重建库(去重+质量门+分层,写入 skill 的 palettes/palettes.json):
python scripts/build_library.py --raw <收割目录> --out <库文件>
# 3. 检查输出:kept/rejected 比例、flag 数、覆盖率——拒绝率骤降或 flag 全零都说明门坏了
```

库 schema v2 字段:name / hexes / text_hint(源站自带的明暗文字标记)/ likes / tier / computed_styles / occurrences / metrics(lightness_span, max_contrast, cb_min_separation)/ flags / sources。

## 已知边界

- 风格标签是 HSL 统计**计算值**,非站方口径(源站的风格过滤 URL 是 SEO 克隆页,拿不到官方标签——见 harvest 坑⑤)。
- 匿名状态下每排序页固定 48 张,分页参数被忽略;总池≈144,去重后 ~116。要更多需登录态或换数据源(未验证)。
- latest 页多为无名新板(tier=new),作新鲜度补充,不作主力。
