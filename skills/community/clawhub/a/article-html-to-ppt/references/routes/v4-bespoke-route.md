# PPT Smith V4 Bespoke 高定路线

## 定位

Bespoke 继承 V3 高定路线，是 V4 默认的质量上限。强模型不是“可选 IR 生成器”，而是
内容导演、叙事导演、设计导演和 PPT 作者。引擎提供来源锁、构建原语、真实渲染和
fail-closed QA。

```text
源材料 + 用户目标 + 页数合同 + 参考视觉（可选）
                         ↓
强模型完整阅读 → Content & Evidence Map → Narrative Contract
                         ↓
判断句标题、图表数据、关系拓扑、可见文案、speaker notes
                         ↓
模型编写原生 PPTX 作者代码与新组件
                         ↓
来源/数字/备注/可编辑性/结构/渲染/视觉复审
```

## 模型交付合同

模型必须提供：

- 受众、决策目标、叙事主线和页数理由；
- 全文证据映射，不得只读局部；
- 每页 assertion、证据、可见内容和完整 speaker notes；
- 原生图表数据、关系图和必要的新组件；
- 真实渲染后的逐页视觉复审与定向修订。

源文件截图不能替代页面创作。插图只有在无法原生重建且其本身具有视觉价值时才可作为
图片使用；图片周围的标题、结论、关键数字和解释仍由模型以原生对象创作。

## 页数合同

Production Request 支持 `auto`、`target`、`range` 和 `exact`。模型根据内容形成
`minimum_viable_pages`、`recommended_pages` 和 `maximum_useful_pages`。源文件页数不等于
输出页数；不得通过压字、截断或编造页面满足数字。

## 参考模板

在 Bespoke 中，参考模板是 `style_transfer` 或 `inspiration` 证据。模型可以学习字体、
色彩、留白、层级、图形语言和节奏，但从空白 Presentation 创作，不能声称严格复用母版。
需要原生组件复用时选择 Template 路线。

## 运行与验收

- `plan-bespoke`：锁定 Production Request、Narrative Contract 和内容评估；
- `author-bespoke`：执行模型作者脚本并完成非视觉门禁；
- `review-bespoke`：应用与 deck/render hash 绑定的视觉复审。

没有模型作者脚本、没有完整备注、只有 extractive IR 或没有视觉复审时，Bespoke 不得进入
最终状态。
