# 面部表情/情感场景提示词模板

## 必需元素清单

- [ ] 角色外观描述（年龄/性别/特征）
- [ ] 起始表情状态
- [ ] 结束表情状态
- [ ] 表情变化的触发事件
- [ ] 表情变化的速度（瞬间/渐变/缓慢）
- [ ] 眼睛细节（泪光/瞳孔变化/眼神方向）
- [ ] 嘴部细节（颤抖/咬唇/微笑弧度）
- [ ] 配合的肢体动作（如有）

## 缺失检测规则

如果用户未指定以下要素，必须主动询问：
1. **表情起止**: "角色的表情从什么状态开始，变化到什么状态？比如从微笑到落泪。"
2. **变化速度**: "这个表情变化是瞬间的还是缓慢渐变的？"
3. **眼睛状态**: "需要表现泪光、瞳孔放大等眼部细节吗？"
4. **触发原因**: "是什么导致了这个表情变化？看到某个事物、听到某句话、还是内心想法？"

## 示例 Prompt

### 输入
"一个女孩从难过变成开心"

### 优化后 Prompt (LumaAI 适配)
```
Intimate close-up of a young woman's face transitioning from
sadness to joy. Camera holds steady on a tight close-up with
shallow depth of field. She begins with downcast eyes, slightly
reddened from crying, a tear track visible on her left cheek.
Her lower lip trembles slightly. Then something catches her
attention off-screen — her eyes widen with recognition, pupils
dilating. The corners of her mouth begin to curl upward
involuntarily. The furrow between her brows softens and
disappears. A genuine smile blooms across her face, reaching
her eyes which now sparkle with happy tears. She lets out a
small laugh, covering her mouth with one hand. Soft, warm key
light from camera left, gentle fill light, subtle rim light
creating a halo effect on her hair. Shallow depth of field with
warm bokeh background. Natural skin tones, film grain texture.
```

## 微表情渐变序列库

### 从消极到积极
```
绝望 → 麻木 → 微光(眼神变化) → 犹疑 → 尝试微笑 → 真诚欢笑
悲伤 → 回忆(远视) → 温暖(眼角柔和) → 释然(嘴角上扬) → 平静微笑
愤怒 → 压抑(咬牙) → 放松(深呼吸) → 接受(眼神柔和) → 原谅(淡淡微笑)
```

### 从积极到消极
```
开心 → 困惑(眉皱) → 怀疑(眼神变化) → 震惊(瞪大) → 崩溃(泪水)
自信 → 动摇(微颤) → 恐惧(瞳孔收缩) → 绝望(眼神空洞)
平静 → 不安(眼神游移) → 紧张(咽口水) → 恐惧(瞳孔放大) → 尖叫
```

### 复杂情感
```
苦笑: 嘴角上扬 + 眉头微皱 + 眼神悲伤 — 表面微笑内心痛苦
强忍: 颤抖的嘴唇 + 努力睁大的眼睛 + 额头冒汗 — 压抑强烈情感
顿悟: 迷茫 → 眼神聚焦 → 瞳孔微缩 → 嘴唇微张 → 眼中闪光
```

## 镜头搭配建议

| 表情变化 | 推荐镜头 | 推荐运镜 | 推荐灯光 |
|---------|---------|---------|---------|
| 细腻渐变 | ECU/CU 特写 | 固定或缓慢推入 | 柔和自然光 |
| 瞬间爆发 | CU 特写 | 快速推入 | 高对比侧光 |
| 隐忍压抑 | MCU 中近景 | 缓慢环绕 | 低调暗光 |
| 多人表情对比 | 过肩/正反打 | 剪切切换 | 匹配光线 |
| 内心独白 | ECU 眼部特写 | 极缓推入 | 伦勃朗光 |
