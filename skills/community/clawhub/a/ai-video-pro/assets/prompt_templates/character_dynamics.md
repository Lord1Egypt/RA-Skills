# 角色交互场景提示词模板

## 必需元素清单

- [ ] 角色数量及外观描述
- [ ] 角色之间的关系（对抗/合作/情感）
- [ ] 空间关系（距离、面向、高低差）
- [ ] 肢体互动方式（握手/拥抱/对峙/追逐）
- [ ] 眼神交流（有/无/回避）
- [ ] 情绪基调（紧张/温馨/悲伤/欢快）
- [ ] 面部表情渐变
- [ ] 环境氛围

## 缺失检测规则

如果用户未指定以下要素，必须主动询问：
1. **角色关系**: "这两个角色之间是什么关系？朋友、对手、还是陌生人？"
2. **情绪基调**: "这个场景的情绪基调是什么？紧张、温暖、悲伤还是其他？"
3. **眼神交流**: "角色之间是否有眼神交流？直视、回避还是对峙？"
4. **空间变化**: "在镜头中，角色之间的距离会发生变化吗？走近/远离/保持？"

## 示例 Prompt

### 输入
"父亲送女儿上大学的离别场景"

### 优化后 Prompt (LumaAI 适配)
```
Emotional medium shot of a middle-aged father and his college-age
daughter standing outside a university dormitory building. Camera
slowly dollies in from a medium wide shot to a close-up. The father
gently adjusts his daughter's backpack strap, his hands slightly
trembling. His expression shifts from a forced smile to eyes
glistening with unshed tears. The daughter looks up at him with
gratitude and determination, her eyes also wet. Golden hour
sunlight streams through autumn maple trees, creating warm
bokeh in the background. Soft, warm color grading with subtle
lens flare. The father pulls her into a tight embrace, his chin
resting on her head. Photorealistic, cinematic depth of field.
```

## 角色动态要素矩阵

| 交互类型 | 关键动作 | 面部重点 | 推荐运镜 |
|---------|---------|---------|---------|
| 对抗 | 对峙姿态、拳头握紧 | 怒视、紧绷 | 正反打、荷兰角 |
| 合作 | 并肩、击掌、点头 | 默契微笑、坚定 | 跟拍、环绕 |
| 离别 | 拥抱、挥手、回望 | 不舍、强忍泪水 | 缓慢推轨、慢动作 |
| 重逢 | 奔跑、拥抱、惊喜 | 喜极而泣、灿烂笑容 | 跟拍、变焦拉伸 |
| 冲突 | 指责、转身、摔门 | 愤怒、受伤、失望 | 手持、快速剪切 |
| 浪漫 | 牵手、对视、接近 | 温柔、含羞、深情 | 环绕、柔焦 |
