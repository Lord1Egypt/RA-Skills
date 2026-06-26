# 动作/战斗场景提示词模板

## 必需元素清单

- [ ] 参与角色数量及描述
- [ ] 打击类型（拳击、武器、能量攻击等）
- [ ] 打击力度级别（轻触/重击/影视夸张）
- [ ] 被击反应（倒退/倒地/防御/格挡）
- [ ] 冲击特效（火花/碎片/冲击波/无）
- [ ] 角色受伤表现（划痕/破损/变形/无）
- [ ] 面部表情变化序列
- [ ] 运镜方式
- [ ] 镜头速度（正常/慢动作/变速）
- [ ] 画面比例和时长

## 缺失检测规则

如果用户未指定以下要素，必须主动询问：
1. **打击力度**: "这个打击场景需要什么级别的冲击力？轻柔的接触、沉重的打击、还是夸张的影视效果？"
2. **受击反应**: "被击中的角色应该如何反应？后退、倒地、格挡还是被击飞？"
3. **表情变化**: "攻击者和被击者在打击前后的面部表情分别是怎样的？"
4. **受伤效果**: "需要表现受伤效果吗？比如划痕、护甲破损、流血等。"

## 示例 Prompt

### 输入
"两个武士在雨中决斗"

### 分析输出
```
场景类型: 动作/战斗
角色: 两名武士（需补充外观细节）
环境: 雨中（需确认具体场景——竹林/城镇/河边？）
缺失要素:
  - 打击力度未指定
  - 受击反应未指定
  - 面部表情未指定
  - 受伤效果未指定
  - 运镜方式未指定
```

### 优化后 Prompt (LumaAI 适配)
```
Cinematic slow-motion shot of two samurai warriors locked in a
rain-drenched duel. Camera tracks in a low-angle orbit around them.
The first warrior swings his katana with devastating force, the blade
cutting through sheets of rain. The second warrior parries, sparks
flying from the clash of steel. Rain droplets freeze in mid-air
during the impact moment. The attacker's face shows fierce
determination with gritted teeth, while the defender's expression
shifts from shock to resolute defiance. Rembrandt lighting from
a single paper lantern, teal and orange color grading, water
splashing in volumetric light beams. Photorealistic, 4K quality.
```

### 优化后 Prompt (Runway 适配)
```
Subject: Two samurai warriors in combat stance, katanas clashing
Camera: Low-angle tracking orbit, slow motion at contact point
Lighting: Rembrandt side light from paper lantern, volumetric rain
Style: Photorealistic, cinematic, teal-orange grading
Action: Powerful sword clash, sparks and water spray at impact
Environment: Rain-soaked courtyard, reflective wet stone ground
Expression: Attacker - fierce determination; Defender - resolute defiance
```
