# Content Visual Forge 核心硬规则

本文件包含所有非协商的核心原则和硬规则。

---

## 内容与忠实度

### 1. No Source Lock, No Generation
没有完成 Source Lock，不允许直接生成图片。

### 2. Current Source First
当前输入源优先于历史示例。

### 3. Content Fidelity First
内容忠实度优先于视觉效果。

---

## 输出模式与执行路径

### 4. Output Mode Must Be Declared
必须先确定输出模式（cover-card / social-card / knowledge-carousel 等）。

### 5. Execution Mode Must Be Declared
必须先确定执行路径（preview / production / engineering_rendering 等）。

---

## 文字与可读性

### 6. Chinese Legibility First
中文标题或关键文字可读性优先。

### 7. Small Chinese Text Should Not Be Delegated to Image Models by Default
小字号中文默认不交给图像模型。

### 8. Production Cover Defaults to Background + Typography Overlay
正式封面默认优先采用"无文字背景图 + 后期标题排版"。

---

## 设计与版权

### 9. Anti-Plagiarism By Design
参考图只能参考风格，不复制版式与装饰组合。

### 10. Editorial Systems Over Template Copying
借鉴外部设计方法时只吸收网格、主题色、字号阶梯和质量门禁等方法，不复制模板、类名体系或素材。

### 11. Painter Style Atlas Uses Local Snapshot
画家风格图鉴默认读取本地 snapshot，只能转译为风格因子，不默认仿写具体艺术家。

### 12. External Assets Need Source Records
HTML / CSS 背景图、纹理、照片、logo 或产品图必须按 `asset-source-policy.md` 记录来源与授权；授权不明时改用 CSS 纹理、抽象视觉或请求用户补充素材。

---

## 平台与规格

### 13. Platform Specs Before Social Cards
社交平台组图和公众号封面对必须先声明平台尺寸、输出数量、安全区和命名规则。

### 14. WeChat Cover Pair Is Not Cropping
公众号 `21:9` 主封面和 `1:1` 方封面必须分别构图；方封面使用短标题，不把主封面硬裁或硬塞长标题。

---

## 质量与门禁

### 15. Engineering Rendering For Production
批量、商用、文字必须准确时，优先切换工程化渲染。

### 16. Risk Action Blacklist Must Be Checked
交付前必须检查 `risk-action-blacklist.md`；命中时回到对应路由、切换工程化渲染或停止交付。

### 17. No Unrequested Exam Labels
除非用户明确要求，具体卡片内容不自动加入考试名或等级标签。

---

## 增强与实验

### 18. Design Enhancement Has Fallback
设计增强必须先使用默认设计基线；额外设计能力只能补充视觉方向、token、模板和评审，不得成为阻断条件。

### 19. Visual Direction Is A Layer, Not A Shortcut
小红书 / Rednote / 社交组图的视觉导演层必须建立在 Source Lock、平台规格、内容压缩和页面角色之上，不得用"高级感"替代事实与结构。

### 20. Illustration Grammar Must Be Explicit
启用插画感成图时，必须先声明 scene_role、subject_focus、composition_axis、camera_distance、palette_temperature、texture_level、text_load 与 blocked_mimicry。

### 21. Creative Micro Assets Are Method-Only Enhancements
ASCII、手绘图解、Excalidraw、p5.js、PixiJS 等只能作为局部创意媒介或浏览器视觉层，必须建立在 Source Lock、输出模式、平台规格、内容压缩和文字精确性边界之后。

### 22. PixiJS Generated Visual Layer Is Static-Export First
当工程化渲染画质不足时，PixiJS 可作为 AI 生图后的 canvas 视觉叠层或静态帧渲染路线；不得把 PixiJS canvas 输出承诺成可编辑设计源、可编辑 PPT 对象或图片交付中的原生动画。

### 23. Style Exploration Is An Experiment Layer
稀有风格探索必须先锁主体身份和平台边界，再组合材质、年代、媒介、光线、空间、影像缺陷等视觉轴。

### 24. External References Are Method Only
参考外部视觉规划方法、创意技能或教程时，只吸收方法论，不复制模板、风格库原文、示例图、素材、CSS、配色、prompt 或视觉签名。

---

**版本：** 1.0.0  
**最后更新：** 2026-06-15
