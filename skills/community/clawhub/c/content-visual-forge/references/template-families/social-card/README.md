# Template Family · social-card

## 定位

面向小红书 / Rednote、社交平台组图、平台缩略图和跨平台传播卡片。

它不同于 `knowledge-carousel`：`knowledge-carousel` 优先讲清知识结构；`social-card` 优先形成一组可滑动、可传播、可截图复用的视觉论证。

## 适合场景

- 小红书 / Rednote 3:4 组图
- 产品更新解释图
- 截图驱动的工具介绍
- 文章或视频转写稿的社交平台拆页
- 教程、清单、避坑、对比、购买建议、路线 / 地点 / 装备类内容

## 不适合承诺的场景

遇到下面需求要先说明边界，不要硬套模板：

- 纯摄影大片或菜品摆盘展示，且图片质量本身就是全部交付
- OOTD 全身穿搭照片生成或模拟
- 梦核、Y2K、哥特萝莉、kawaii 等强装饰审美，若它们与当前编辑 / 瑞士视觉系统冲突
- 用户没有素材、但核心需求依赖真实照片或截图的帖子

可替代路径：

- 请求用户提供照片 / 截图
- 转为 `prompt_package`
- 转为信息图 / 清单型 `social-card`
- 转为 `wechat-inline-image` 或 `knowledge-carousel`

## 输出结构

正式规划默认先输出 `visual_direction`：

- 内容类型判断
- 传播目标判断
- 读者情绪判断
- 信息密度判断
- 三套风格方向：`click_first`、`save_first`、`brand_first`
- 推荐方案与不推荐方案
- 页面角色节奏与逐页视觉关系

默认：

```text
01 封面：强 hook + 一个核心视觉
02-06 内容页：每页一个观点
07-08 可选：总结 / 清单 / 对比 / 行动建议
```

常用页面角色：

- Hook cover
- Problem scene
- Insight frame
- Method / system
- Misconception vs reality
- Checklist
- Comparison
- Screenshot evidence
- One big quote
- Step-by-step flow
- Gear / tool / resource list
- Summary page

## 内容规则

- 图片承载 hook、对比、清单和关键证据，不承载完整文章。
- 正文细节留给平台正文或公众号正文。
- 页面标题要具体，有对象、有动作、有结果。
- 不使用“背景介绍”“核心观点”等抽象占位标题，除非页面真的在做背景铺垫。
- 每页文案必须回到 Source Lock，不补未经来源支持的事实。

## 视觉规则

- 默认尺寸：`1080 x 1440`
- 每页稳定安全区，避免标题和页脚贴边。
- 组内只使用一个视觉系统。
- 页面结构要有变化，不要每页都套同一张卡片。
- 截图页优先保证截图可读，文字随之减少。
- 不用随机装饰圆点、贴纸、渐变团块或嵌套卡片填空。
- 封面可以更冲击，内页必须更清晰；封面、证据页、流程页、总结页至少有两种不同 frame role。
- 提示词必须写清画幅、页面角色、标题区、主视觉区、文字安全区、配色、字体、留白和负面提示。
- 小字号中文、精确中文、截图标注和商业批量交付优先进入工程化渲染，不默认交给图像模型。

## 反模式检查

交付前必须检查：

- PPT 感：中心 bullet 列表、缺少滑动节奏。
- 廉价 AI 科技风：蓝紫渐变、随机霓虹线、复杂无意义背景。
- 信息过载：每页想讲完所有内容，靠缩小字号解决。
- 伪高级：只写“高级 / 极简 / 科技”，没有具体层级、留白和主视觉。
- 文字不可读：标题被纹理 / 光效 / 图片主体干扰。
- 风格断裂：每页像不同模板拼接。

## 工程化渲染

当要求批量、商用、中文准确、截图可读时，优先 `engineering_rendering`。

推荐使用单 HTML 多 frame：

```text
index.html
assets/
output/social-01-cover.png
output/social-02-<topic>.png
```

详见：

- `references/config/platform-specs.md`
- `references/render-engine.md`
- `references/config/quality-checklist.md`
