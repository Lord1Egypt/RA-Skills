# 🎨 古典美学视觉提示词库 (Visual Aesthetic Prompt Library)
版本: v1.0
用途: 为 `apply-china-classics` 提供精准的视觉解码参数，将抽象的古典意境转化为高质量的 AI 绘画指令。

---

## 📂 美学风格定义 (Aesthetic Presets)

### 1. 【宋代极简主义】 (Song Dynasty Minimalism)
*核心意境：清冷、留白、克制、禅意*
- **视觉关键词**: 
  - `Ink wash painting` (水墨), `muted tones` (哑光色调), `negative space` (留白), `atmospheric perspective` (大气透视).
- **材质与光影**: 
  - `Silk texture` (丝绸质感), `soft diffused light` (柔和漫反射), `morning mist` (晨雾).
- **Prompt 模板**: 
  - `[Subject], minimalist Song Dynasty ink painting style, vast negative space, subtle brushstrokes, muted colors, serene atmosphere, high-end Zen aesthetic, 8k resolution, elegant and quiet.`

### 2. 【敦煌瑰丽之境】 (Dunhuang Magnificent)
*核心意境：繁复、神圣、色彩浓郁、跨文化融合*
- **视觉关键词**: 
  - `Mineral pigments` (矿物颜料), `flying apsaras` (飞天), `intricate patterns` (复杂图案), `terracotta gold` (赤金).
- **材质与光影**: 
  - `Weathered fresco` (风化壁画), `gold leaf accents` (金箔点缀), `deep lapis lazuli` (深青金石色).
- **Prompt 模板**: 
  - `[Subject], Dunhuang cave mural style, rich mineral colors, intricate floating ribbons, celestial beings, ancient fresco texture, gold outlines, divine and mystical lighting, symmetrical composition, hyper-detailed ornament.`

### 3. 【中式赛博/新古典】 (Cyber-Neo Classical)
*核心意境：碰撞、重构、未来感、文化觉醒*
- **视觉关键词**: 
  - `Neon calligraphy` (霓虹书法), `holographic ink` (全息水墨), `traditional architecture mixed with circuitry` (传统建筑与电路结合).
- **材质与光影**: 
  - `Iridescent glass` (虹彩玻璃), `cyberpunk lighting` (赛博光影), `high contrast` (高对比).
- **Prompt 模板**: 
  - `[Subject], Neo-Classical Chinese cyberpunk, fusion of ancient temple and futuristic city, iridescent ink droplets, neon glow in traditional patterns, cinematic lighting, surreal digital art, sharp focus, 8k.`

---

## 🛠️ 视觉解码流程 (Visual Decoding Path)

当触发 `Prompt Mode` 时，遵循以下转化链路：
`古典概念 (如: 逍遥)` $\rightarrow$ `选择美学风格 (如: 宋代极简)` $\rightarrow$ `填充 Subject (如: 一只在云海中独行的鹤)` $\rightarrow$ `组合模板参数` $\rightarrow$ `生成最终指令`。

---

*本库通过对具体艺术史特征的参数化，确保 AI 输出不再是简单的“中国风”，而是具备文化深度的“美学表达”。*
