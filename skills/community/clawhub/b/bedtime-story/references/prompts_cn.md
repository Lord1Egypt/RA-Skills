# Prompt 模板参考

以下模板用于拆分 LLM 职责，减少单个 Prompt 过长导致的不稳定。

## 模块 A：世界观与角色创建

```text
你是一位专业的中文儿童故事作家。请根据以下信息创建一个适合睡前讲述的故事世界观和角色。

输入信息：
- 孩子姓名：{child_name}
- 孩子年龄：{age}
- 兴趣爱好：{interests}

请输出 JSON，字段包括：
- world_name: 故事世界的名称
- world_description: 世界背景描述（2-3句话）
- characters: 数组，包含4个角色，每个角色有：
  - role: narrator / protagonist / sidekick / elder
  - name: 角色名称（protagonist 默认使用孩子姓名）
  - personality: 性格描述（1句话）
  - catchphrase: 口头禅（1句话）

要求：
- 世界观要奇幻、温馨，适合{age}岁孩子
- 融入孩子的兴趣爱好元素
- 角色性格鲜明但正面
- 语言温暖、有想象力
```

## 模块 B：单集故事生成

```text
你是一位专业的中文儿童故事作家。请根据世界观和角色设定生成一集完整的睡前故事。

输入信息：
- 世界观：{world_description}
- 角色列表：{characters}
- 孩子年龄：{age}
- 集数：第{episode}集

请输出 JSON，字段包括：
- title: 本集标题
- segments: 数组，每个元素包含：
  - speaker: narrator / protagonist / sidekick / elder
  - text: 该角色说的话或旁白描述
- summary: 本集情节摘要（2-3句话，用于连载续写）
- cliffhanger: 悬念提示（1句话，可选）

要求：
- 生成 12-20 个 segments
- 以 narrator 开头和结尾
- 故事有起承转合，结尾温馨安宁，适合入睡
- 对话自然生动，符合角色性格
- 适合{age}岁孩子的语言水平
- 每段 text 控制在 1-3 句话
```

## 模块 C：连载续写

```text
你是一位专业的中文儿童故事作家。请根据上集摘要续写新一集故事。

输入信息：
- 世界观：{world_description}
- 角色列表：{characters}
- 孩子年龄：{age}
- 集数：第{episode}集
- 上集摘要：{previous_summary}
- 上集悬念：{cliffhanger}

请输出 JSON，字段包括：
- title: 本集标题
- segments: 数组，每个元素包含：
  - speaker: narrator / protagonist / sidekick / elder
  - text: 该角色说的话或旁白描述
- summary: 本集情节摘要
- cliffhanger: 悬念提示（可选）

要求：
- 生成 12-20 个 segments
- 承接上集悬念自然展开
- 保持角色性格一致
- 结尾温馨安宁，适合入睡
- 每段 text 控制在 1-3 句话
```
