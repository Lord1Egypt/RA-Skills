# 历史作品与验证范围

以下保留原版本、对象统计与验证边界，不将历史样例重新标为 5.3.0 实测。当前入口与新增作品见[README](../../README.md)。

## 作品画廊

以下收录 `assets/samples/` 中的示例图，按**图片首次加入仓库的日期倒序**排列；日期不是 PPT 的制作日期。点击缩略图查看原图，较早的设计与架构示例可展开查看。可编辑对象数仅对应各自的交付 PPTX，历史案例的验证范围见下文。

<p>
  <a href="https://raw.githubusercontent.com/SkillMelody/PPT-Smith/3d66f434001c544ff0ac79b7230586b3d0c1690a/assets/samples/v5.2-xiaomi-q2-h1-22page-overview.png"><img src="https://raw.githubusercontent.com/SkillMelody/PPT-Smith/3d66f434001c544ff0ac79b7230586b3d0c1690a/assets/samples/v5.2-xiaomi-q2-h1-22page-overview.png" alt="小米集团2025年第二季度及上半年经营复盘，22页装饰商务PPT实际渲染总览" width="100%"></a><br>
  <strong>2026-10-18 · 小米经营复盘 · 22 页装饰商务实测</strong><br>
  <small>本次合入能力的开发分支实测 · 519 个原生对象，含 6 个图表、4 个表格 · 点击查看完整预览</small>
</p>

<details>
<summary>查看本次实测的版本与验证范围</summary>

以用户提供的《小米集团 2025 年第二季度及上半年经营复盘》资料与数据底表制作，完成真实渲染、多轮修订和独立 Agent 审核。图片直接来自最终 PPTX 的 22 页预览。实测使用开发提交 `af23320`，当时版本文件仍为 `5.1.1`；相关能力已纳入 `5.2.0`，未将历史运行改写为正式版测试。

PPT 含 370 个文本、139 个形状/路径、6 个原生图表、4 个原生表格，共 519 个原生对象，图片对象为 0。Linux + LibreOffice 中的文字、表格修改已验证保存后重开保留；图表数据在应用内的修改未完成有效验证，PowerPoint/WPS 未实测。使用阿里巴巴普惠体，字体未嵌入。本处公开总览图，原始资料、完整日志和证据包不随仓库分发。

</details>

<table>
  <tr>
    <td width="33%" valign="top"><a href="https://raw.githubusercontent.com/SkillMelody/PPT-Smith/3d66f434001c544ff0ac79b7230586b3d0c1690a/assets/samples/v5.1-template-image-guided-4page-2col-overview.png"><img src="https://raw.githubusercontent.com/SkillMelody/PPT-Smith/3d66f434001c544ff0ac79b7230586b3d0c1690a/assets/samples/v5.1-template-image-guided-4page-2col-overview.png" alt="生图设计后原生重建，四页两列总览" width="100%"></a><br><strong>2026-09-23 · 模板风格重建</strong><br><small>4 页 · 179 个可编辑对象 · <a href="https://github.com/SkillMelody/PPT-Smith/blob/3d66f434001c544ff0ac79b7230586b3d0c1690a/assets/samples/v5.1-template-image-guided-4page.pptx">下载 PPTX</a></small></td>
    <td width="33%" valign="top"><a href="https://raw.githubusercontent.com/SkillMelody/PPT-Smith/3d66f434001c544ff0ac79b7230586b3d0c1690a/assets/samples/v5.1-template-native-4page-2col-overview.png"><img src="https://raw.githubusercontent.com/SkillMelody/PPT-Smith/3d66f434001c544ff0ac79b7230586b3d0c1690a/assets/samples/v5.1-template-native-4page-2col-overview.png" alt="原生模板组件复用，四页两列总览" width="100%"></a><br><strong>2026-09-23 · 原生组件复用</strong><br><small>4 页 · 61 个可编辑对象 · <a href="https://github.com/SkillMelody/PPT-Smith/blob/3d66f434001c544ff0ac79b7230586b3d0c1690a/assets/samples/v5.1-template-native-4page.pptx">下载 PPTX</a></small></td>
    <td width="33%" valign="top"><a href="https://raw.githubusercontent.com/SkillMelody/PPT-Smith/3d66f434001c544ff0ac79b7230586b3d0c1690a/assets/samples/v5.1-no-image-policy-page-01.png"><img src="https://raw.githubusercontent.com/SkillMelody/PPT-Smith/3d66f434001c544ff0ac79b7230586b3d0c1690a/assets/samples/v5.1-no-image-policy-page-01.png" alt="v5.1 无生图政策解读封面" width="100%"></a><br><strong>2026-09-21 · v5.1 无生图封面</strong><br><small>6 页政策解读中的第 1 页 · <a href="https://github.com/SkillMelody/PPT-Smith/blob/3d66f434001c544ff0ac79b7230586b3d0c1690a/assets/samples/v5.1-no-image-policy-native.pptx">下载 PPTX</a></small></td>
  </tr>
  <tr>
    <td width="33%" valign="top"><a href="https://raw.githubusercontent.com/SkillMelody/PPT-Smith/3d66f434001c544ff0ac79b7230586b3d0c1690a/assets/samples/v5.1-no-image-policy-page-02.png"><img src="https://raw.githubusercontent.com/SkillMelody/PPT-Smith/3d66f434001c544ff0ac79b7230586b3d0c1690a/assets/samples/v5.1-no-image-policy-page-02.png" alt="v5.1 无生图政策解读三年目标页" width="100%"></a><br><strong>2026-09-21 · v5.1 目标页</strong><br><small>同一份 6 页可编辑政策 PPT</small></td>
    <td width="33%" valign="top"><a href="https://raw.githubusercontent.com/SkillMelody/PPT-Smith/3d66f434001c544ff0ac79b7230586b3d0c1690a/assets/samples/v5.1-no-image-policy-page-06.png"><img src="https://raw.githubusercontent.com/SkillMelody/PPT-Smith/3d66f434001c544ff0ac79b7230586b3d0c1690a/assets/samples/v5.1-no-image-policy-page-06.png" alt="v5.1 无生图政策解读行动页" width="100%"></a><br><strong>2026-09-21 · v5.1 行动页</strong><br><small>同一份 6 页可编辑政策 PPT</small></td>
    <td width="33%" valign="top"><a href="https://raw.githubusercontent.com/SkillMelody/PPT-Smith/3d66f434001c544ff0ac79b7230586b3d0c1690a/assets/samples/v5.0-latin-america-ai-zh-overview.png"><img src="https://raw.githubusercontent.com/SkillMelody/PPT-Smith/3d66f434001c544ff0ac79b7230586b3d0c1690a/assets/samples/v5.0-latin-america-ai-zh-overview.png" alt="v5.0 拉美 AI 与就业研究二十页总览" width="100%"></a><br><strong>2026-09-21 · v5.0 研究解读</strong><br><small>20 页 · 447 个原生可编辑对象 · <a href="https://github.com/SkillMelody/PPT-Smith/blob/3d66f434001c544ff0ac79b7230586b3d0c1690a/assets/samples/v5.0-latin-america-ai-zh-native.pptx">下载 PPTX</a></small></td>
  </tr>
  <tr>
    <td width="33%" valign="top"><a href="https://raw.githubusercontent.com/SkillMelody/PPT-Smith/3d66f434001c544ff0ac79b7230586b3d0c1690a/assets/samples/v5-declarative-design-native-preview.png"><img src="https://raw.githubusercontent.com/SkillMelody/PPT-Smith/3d66f434001c544ff0ac79b7230586b3d0c1690a/assets/samples/v5-declarative-design-native-preview.png" alt="v5 声明式设计原生预览" width="100%"></a><br><strong>2026-09-20 · v5 设计预览</strong><br><small>早期声明式设计示例</small></td>
    <td width="33%" valign="top"><a href="https://raw.githubusercontent.com/SkillMelody/PPT-Smith/3d66f434001c544ff0ac79b7230586b3d0c1690a/assets/samples/mgi-template-v4-31-page-contact-sheet.png"><img src="https://raw.githubusercontent.com/SkillMelody/PPT-Smith/3d66f434001c544ff0ac79b7230586b3d0c1690a/assets/samples/mgi-template-v4-31-page-contact-sheet.png" alt="V4 模板路线三十一页联系表" width="100%"></a><br><strong>2026-09-10 · V4 Template</strong><br><small>31 页研究报告演示</small></td>
    <td width="33%" valign="top"><a href="https://raw.githubusercontent.com/SkillMelody/PPT-Smith/3d66f434001c544ff0ac79b7230586b3d0c1690a/assets/samples/state-ai-2025-independent-bespoke-23-page-contact-sheet.png"><img src="https://raw.githubusercontent.com/SkillMelody/PPT-Smith/3d66f434001c544ff0ac79b7230586b3d0c1690a/assets/samples/state-ai-2025-independent-bespoke-23-page-contact-sheet.png" alt="V4 Bespoke 路线二十三页联系表" width="100%"></a><br><strong>2026-09-10 · V4 Bespoke</strong><br><small>23 页独立设计演示</small></td>
  </tr>
</table>

<details>
<summary>展开更早的 9 张示例图（2026-08 → 2026-07）</summary>

<table>
  <tr>
    <td width="33%" valign="top"><a href="https://raw.githubusercontent.com/SkillMelody/PPT-Smith/3d66f434001c544ff0ac79b7230586b3d0c1690a/assets/samples/v120-deepseek-v4-pro-state-of-ai-contact-sheet.png"><img src="https://raw.githubusercontent.com/SkillMelody/PPT-Smith/3d66f434001c544ff0ac79b7230586b3d0c1690a/assets/samples/v120-deepseek-v4-pro-state-of-ai-contact-sheet.png" alt="早期 State of AI 模型路径演示联系表" width="100%"></a><br><strong>2026-08-11 · State of AI 对照稿</strong></td>
    <td width="33%" valign="top"><a href="https://raw.githubusercontent.com/SkillMelody/PPT-Smith/3d66f434001c544ff0ac79b7230586b3d0c1690a/assets/samples/model-path-comparison-grid.png"><img src="https://raw.githubusercontent.com/SkillMelody/PPT-Smith/3d66f434001c544ff0ac79b7230586b3d0c1690a/assets/samples/model-path-comparison-grid.png" alt="模型路径对照网格" width="100%"></a><br><strong>2026-08-11 · 模型路径对照</strong></td>
    <td width="33%" valign="top"><a href="https://raw.githubusercontent.com/SkillMelody/PPT-Smith/3d66f434001c544ff0ac79b7230586b3d0c1690a/assets/samples/stateofai-2025-final-contact-sheet.png"><img src="https://raw.githubusercontent.com/SkillMelody/PPT-Smith/3d66f434001c544ff0ac79b7230586b3d0c1690a/assets/samples/stateofai-2025-final-contact-sheet.png" alt="早期 State of AI 演示联系表" width="100%"></a><br><strong>2026-07-21 · State of AI 演示</strong></td>
  </tr>
  <tr>
    <td width="33%" valign="top"><a href="https://raw.githubusercontent.com/SkillMelody/PPT-Smith/3d66f434001c544ff0ac79b7230586b3d0c1690a/assets/samples/ai-project-core-upgrade-contact-sheet.png"><img src="https://raw.githubusercontent.com/SkillMelody/PPT-Smith/3d66f434001c544ff0ac79b7230586b3d0c1690a/assets/samples/ai-project-core-upgrade-contact-sheet.png" alt="AI 项目核心升级示例联系表" width="100%"></a><br><strong>2026-07-21 · AI 项目升级</strong></td>
    <td width="33%" valign="top"><a href="https://raw.githubusercontent.com/SkillMelody/PPT-Smith/3d66f434001c544ff0ac79b7230586b3d0c1690a/assets/samples/ai-project-model-routing.png"><img src="https://raw.githubusercontent.com/SkillMelody/PPT-Smith/3d66f434001c544ff0ac79b7230586b3d0c1690a/assets/samples/ai-project-model-routing.png" alt="AI 项目模型路由示意" width="100%"></a><br><strong>2026-07-21 · 模型路由</strong></td>
    <td width="33%" valign="top"><a href="https://raw.githubusercontent.com/SkillMelody/PPT-Smith/3d66f434001c544ff0ac79b7230586b3d0c1690a/assets/samples/ai-project-agent-router.png"><img src="https://raw.githubusercontent.com/SkillMelody/PPT-Smith/3d66f434001c544ff0ac79b7230586b3d0c1690a/assets/samples/ai-project-agent-router.png" alt="AI 项目 Agent Router 示意" width="100%"></a><br><strong>2026-07-21 · Agent Router</strong></td>
  </tr>
  <tr>
    <td width="33%" valign="top"><a href="https://raw.githubusercontent.com/SkillMelody/PPT-Smith/3d66f434001c544ff0ac79b7230586b3d0c1690a/assets/samples/ai-project-execution-layer.png"><img src="https://raw.githubusercontent.com/SkillMelody/PPT-Smith/3d66f434001c544ff0ac79b7230586b3d0c1690a/assets/samples/ai-project-execution-layer.png" alt="AI 项目执行层示意" width="100%"></a><br><strong>2026-07-21 · 执行层</strong></td>
    <td width="33%" valign="top"><a href="https://raw.githubusercontent.com/SkillMelody/PPT-Smith/3d66f434001c544ff0ac79b7230586b3d0c1690a/assets/samples/palette-upgrade-overview.png"><img src="https://raw.githubusercontent.com/SkillMelody/PPT-Smith/3d66f434001c544ff0ac79b7230586b3d0c1690a/assets/samples/palette-upgrade-overview.png" alt="早期配色升级总览" width="100%"></a><br><strong>2026-07-21 · 配色升级</strong></td>
    <td width="33%" valign="top"><a href="https://raw.githubusercontent.com/SkillMelody/PPT-Smith/3d66f434001c544ff0ac79b7230586b3d0c1690a/assets/samples/native-architecture-diagram.png"><img src="https://raw.githubusercontent.com/SkillMelody/PPT-Smith/3d66f434001c544ff0ac79b7230586b3d0c1690a/assets/samples/native-architecture-diagram.png" alt="原生架构示意图" width="100%"></a><br><strong>2026-07-21 · 原生架构</strong></td>
  </tr>
</table>

</details>

## 模板路线对照：保留原生组件，或参考风格重新设计

同一份拉美 AI 与就业研究报告、同一份 37 页视觉模板，选取中文封面、57% 工时技术潜力、三类国家路径、66% 技能共享四页。两稿使用相同的 42 个内容项、四页讲稿和两组图表数据。下列总览均由最终 PPTX 的实际办公软件渲染页拼成，每张图按两列展示四页；未把设计图或截图放入 PPTX 充当整页内容。

| 使用约束 | 应选流程 | 本次四页样例 |
| --- | --- | --- |
| 母版、版式、图表工作簿和指定组件必须保留 | `template`：核验模板 → 选择与克隆原生对象 → 绑定新内容 → 真实预览与编辑验收 | A 展示原生组件复用及编排 |
| 只借鉴模板风格，可重新排版；无生图工具 | `create`：读模板视觉规则 → 锁定源内容 → 原生对象设计 → 渲染预览 → 视觉修订 | 可按此流程使用；本组未单独制作第三稿 |
| 只借鉴模板风格，可使用生图工具 | `create`：锁定内容 → 生成并核对整页设计目标 → 冻结目标 → 原生重建 → 逐页对照与编辑验收 | B 展示生图设计稿后原生重建 |
| 已有批准的完整页面设计图，要求尽量还原 | `recreate`：登记目标图 → 以源文档核对文字和数据 → 原生重建与差异审核 | 设计目标由用户提供时适用；本组 B 的目标由生图工具产生 |

**A · 原生模板组件复用。** [下载四页可编辑 PPTX](https://github.com/SkillMelody/PPT-Smith/blob/3d66f434001c544ff0ac79b7230586b3d0c1690a/assets/samples/v5.1-template-native-4page.pptx)。使用真实原生形状、图表和工作簿克隆与数据绑定能力，完成本次四页编排。**这是组件能力与视觉效果的对照样本，不是完整 strict-template 输入合同的端到端认证。**

![A：原生模板组件复用的四页 PPT 实际渲染，两列总览](https://raw.githubusercontent.com/SkillMelody/PPT-Smith/3d66f434001c544ff0ac79b7230586b3d0c1690a/assets/samples/v5.1-template-native-4page-2col-overview.png)

**B · 参考模板生图设计后原生重建。** [下载四页可编辑 PPTX](https://github.com/SkillMelody/PPT-Smith/blob/3d66f434001c544ff0ac79b7230586b3d0c1690a/assets/samples/v5.1-template-image-guided-4page.pptx)。本例先生成四张整页设计稿，其中一张因未锁定文案被修正；再把合格设计稿作为目标，用原生文字、形状和图表重建。B 通过完整声明式构建与独立逐页审核，交付门禁为 `final_delivery_ready`、0 个阻断项。设计稿与交付稿在纹理、渐变、图标和换行上仍有差异，不能视为逐像素 1:1。

![B：模板风格生图设计并重建的四页 PPT 实际渲染，两列总览](https://raw.githubusercontent.com/SkillMelody/PPT-Smith/3d66f434001c544ff0ac79b7230586b3d0c1690a/assets/samples/v5.1-template-image-guided-4page-2col-overview.png)

| 最终 PPTX 中的对象 | A 原生模板组件复用 | B 生图后原生重建 |
| --- | ---: | ---: |
| 可编辑文本对象 | 40 | 40 |
| 原生形状、线条和路径 | 19 | 137 |
| 原生图表（各含数据工作簿） | 2 | 2 |
| 图片对象 | 0 | 0 |
| **可编辑对象合计** | **61** | **179** |

以上按实际 PPTX 的顶层对象逐个计数；图表扇区、图表内置工作簿、字符与备注不重复计数。B 多出的对象主要是可编辑几何图标与构图元素，数量增加不直接证明设计更好。两份样例都在本机 LibreOffice 中验证了修改文字、形状和图表数据后保存、重开仍可编辑；未实测其他办公软件或操作系统。这是四页同源对照，不代表所有模板都能获得同样效果。

## v5.1 实测：无生图的 6 页中文政策解读

输入为用户提供的 7 页《人工智能中小企业创业支持计划（2026—2028年）》PDF。独立作者只使用新版 Skill 和源文档完成原创稿，未调用生图工具。输出包括 6 页中文内容、逐页来源和 6 页演讲者备注；90 天行动步骤明确标为作者建议。

**下载同一份 [可编辑 PPTX](https://github.com/SkillMelody/PPT-Smith/blob/3d66f434001c544ff0ac79b7230586b3d0c1690a/assets/samples/v5.1-no-image-policy-native.pptx)**，或查看 [对象统计与验收摘要 JSON](../../assets/samples/v5.1-no-image-policy-evidence.json)。以下图片均直接来自该 PPTX 的真实办公软件渲染，没有重绘或美化截图。

### 封面：13 个文本对象 + 6 个原生形状

![v5.1 无生图原创封面，主标题与三条政策主线均为原生对象](https://raw.githubusercontent.com/SkillMelody/PPT-Smith/3d66f434001c544ff0ac79b7230586b3d0c1690a/assets/samples/v5.1-no-image-policy-page-01.png)

### 目标页：16 个文本对象 + 3 个原生形状

![v5.1 三年目标页，保留“1万家以上”“突破2000家”及三个10个的原文限定](https://raw.githubusercontent.com/SkillMelody/PPT-Smith/3d66f434001c544ff0ac79b7230586b3d0c1690a/assets/samples/v5.1-no-image-policy-page-02.png)

### 行动页：18 个文本对象 + 5 个原生形状

![v5.1 原生时间轴，明确标记为作者建议而非官方申报流程](https://raw.githubusercontent.com/SkillMelody/PPT-Smith/3d66f434001c544ff0ac79b7230586b3d0c1690a/assets/samples/v5.1-no-image-policy-page-06.png)

统计直接读取交付 PPTX，每个文本框或形状计一次：

| 页码与内容 | 原生文本 | 原生形状 | 可编辑对象合计 |
| --- | ---: | ---: | ---: |
| 1 · 政策导航 | 13 | 6 | 19 |
| 2 · 三年目标 | 16 | 3 | 19 |
| 3 · 要素供给 | 15 | 4 | 19 |
| 4 · 主体培育 | 12 | 3 | 15 |
| 5 · 开源与保障 | 20 | 5 | 25 |
| 6 · 作者行动建议 | 18 | 5 | 23 |
| **全稿** | **94** | **26** | **120** |

本例图片、原生图表、原生表格和分组均为 **0**，6 页均有备注。数字是可编辑文本，不把它们称为原生图表；装饰线和圆点计入形状，备注、字符数不重复计入对象数。对象数量用于说明编辑结构，不作为设计质量分数。

该候选已通过独立逐页视觉与来源审核，门禁状态为 `final_delivery_ready`。在 **macOS + LibreOffice 26.2.4.2** 中通过 Basic/UNO 修改副本的文字、数字文字及形状颜色，保存、关闭、重开后验证修改保留、6 页备注完整，原候选文件未改变。此为实际应用对象编辑测试，并非 GUI 点击测试；不外推为 Windows/Linux 或 PowerPoint/WPS 实机验证。样例使用 Arial Unicode MS，字体未嵌入，换设备需检查字体与排版。

## v5.0 实测保留：20 页中文研究解读

输入为 67 页 *Agents, robots, and us: How AI reshapes work and skills in Latin America* 报告，输出 20 页《智能体、机器人与我们》中文研究解读，涵盖自动化潜力、经济价值、岗位与技能、国家对照和企业案例。每页均有来源与演讲者备注。这是 v5.0 阶段的真实历史成品，单独统计，不与上面的 v5.1 案例混算。

流程为“源文档 → 完整页面设计图 → 多模态识读与声明式重建 → 原生 PPTX → 实际渲染与验收”。以下保留原交付的 20 页总览图；[下载原始可编辑 PPTX](https://github.com/SkillMelody/PPT-Smith/blob/3d66f434001c544ff0ac79b7230586b3d0c1690a/assets/samples/v5.0-latin-america-ai-zh-native.pptx)，[查看逐页对象数据](../../assets/samples/v5.0-latin-america-ai-zh-evidence.json)。

![v5.0 智能体、机器人与我们：20 页中文可编辑 PPT 实际渲染总览](https://raw.githubusercontent.com/SkillMelody/PPT-Smith/3d66f434001c544ff0ac79b7230586b3d0c1690a/assets/samples/v5.0-latin-america-ai-zh-overview.png)

| 对象类别 | 数量 | 可编辑范围 |
| --- | ---: | --- |
| 原生文本框 | 274 | 修改文字、字体、字号与颜色 |
| 原生形状与路径 | 164 | 移动、缩放与改色 |
| 原生图表 | 7 | 修改数据系列；附 7 个内嵌工作簿 |
| 原生表格 | 2 | 修改单元格、行列和样式 |
| **原生可编辑对象合计** | **447** | **274 + 164 + 7 + 2** |
| 独立封面图片 | 1 | 可整体替换，内部插画元素不可逐个编辑 |
| **幻灯片对象总数** | **448** | **447 个原生对象 + 1 张图片** |

统计直接读取原交付 PPTX，每个对象只计一次；图表数据点、表格单元格、7 个数据工作簿和 20 页备注不重复计数。

<details>
<summary>展开 20 页可编辑对象明细</summary>

| 页码 | 文本 | 形状/路径 | 图表 | 表格 | 原生可编辑合计 | 可替换图片 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 7 | 2 | 0 | 0 | 9 | 1 |
| 2 | 15 | 18 | 0 | 0 | 33 | 0 |
| 3 | 19 | 6 | 0 | 0 | 25 | 0 |
| 4 | 13 | 5 | 1 | 0 | 19 | 0 |
| 5 | 14 | 7 | 1 | 0 | 22 | 0 |
| 6 | 9 | 3 | 1 | 0 | 13 | 0 |
| 7 | 9 | 3 | 1 | 0 | 13 | 0 |
| 8 | 16 | 10 | 0 | 0 | 26 | 0 |
| 9 | 11 | 5 | 0 | 1 | 17 | 0 |
| 10 | 13 | 8 | 1 | 0 | 22 | 0 |
| 11 | 9 | 3 | 1 | 0 | 13 | 0 |
| 12 | 12 | 5 | 1 | 0 | 18 | 0 |
| 13 | 15 | 9 | 0 | 0 | 24 | 0 |
| 14 | 7 | 3 | 0 | 1 | 11 | 0 |
| 15 | 20 | 9 | 0 | 0 | 29 | 0 |
| 16 | 15 | 6 | 0 | 0 | 21 | 0 |
| 17 | 16 | 13 | 0 | 0 | 29 | 0 |
| 18 | 20 | 9 | 0 | 0 | 29 | 0 |
| 19 | 17 | 28 | 0 | 0 | 45 | 0 |
| 20 | 17 | 12 | 0 | 0 | 29 | 0 |
| **全稿** | **274** | **164** | **7** | **2** | **447** | **1** |

</details>

历史验收在 macOS + LibreOffice 26.2.4.2 中通过 Basic/UNO 修改副本的文字、图表数据、表格数据及图片，保存、关闭、重开后改动均保留。设计图与原生重建在字体、图标、渐变及图表样式上仍有差异，不宣称逐像素 1:1；未进行 PowerPoint/WPS 实机验证。使用的 Hiragino Sans GB、Arial 未嵌入，换设备需核对字体与排版。

## 历史样例

以下为较早版本的真实渲染样例，不计入上面的 v5.1 对象统计。

<details>
<summary>展开 V4 Template 与 Bespoke 示例</summary>

**Template：31 页研究报告演示。** 基于源报告和原生模板组件完成编排，29 个正文页具备演讲者备注。

![V4 Template 31 页实际渲染联系表](https://raw.githubusercontent.com/SkillMelody/PPT-Smith/3d66f434001c544ff0ac79b7230586b3d0c1690a/assets/samples/mgi-template-v4-31-page-contact-sheet.png)

**Bespoke：23 页独立设计演示。** 从空白页面制作，含 12 个原生图表和 23 页备注。两份样例使用不同报告，不作为同源质量比较，也不表示与源报告出版方或模板品牌存在合作、授权或背书关系。

![V4 Bespoke 23 页实际渲染联系表](https://raw.githubusercontent.com/SkillMelody/PPT-Smith/3d66f434001c544ff0ac79b7230586b3d0c1690a/assets/samples/state-ai-2025-independent-bespoke-23-page-contact-sheet.png)

更多历史资源见 [样例目录](../../assets/samples/)。

</details>

