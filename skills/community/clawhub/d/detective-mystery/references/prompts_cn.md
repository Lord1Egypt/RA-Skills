# Prompt 模板参考

以下模板用于拆分 LLM 职责。

## 模块 A：案件生成

```text
你是一位推理小说作家，需要生成一个完整的中文侦探推理案件。

输入信息：
- 难度：{difficulty}（easy=线索明显/medium=需要推理/hard=有误导线索）

请输出 JSON，字段包括：
- case_name: 案件名称
- background: 案件背景描述（3-5句话）
- crime: 犯罪事实描述（2-3句话）
- suspects: 数组，包含3个嫌疑人，每个有：
  - id: suspect_a / suspect_b / suspect_c
  - name: 中文姓名
  - occupation: 职业
  - motive: 作案动机
  - alibi: 不在场证明（真凶的应该有破绽）
  - personality: 性格特点（影响审讯表现）
  - is_culprit: true/false（恰好1个为true）
  - secret: 隐藏信息（审讯深入才会暴露）
- evidence: 数组，包含4-6条证据线索，每条有：
  - id: 编号
  - description: 线索描述
  - location: 发现位置
  - related_suspect: 关联嫌疑人ID
  - importance: high/medium/low
- locations: 数组，可勘察的地点（3-4个），每个有：
  - name: 地点名称
  - description: 地点描述
  - clues: 该地点可发现的证据ID列表
- solution: 完整的破案推理过程（3-5句话）

要求：
- 恰好1个真凶
- 每条线索至少关联1个嫌疑人
- 真凶的不在场证明必须有可验证的破绽
- 非真凶也应有可疑之处（增加推理难度）
- 案件逻辑自洽，根据证据可以唯一确定真凶
```

## 模块 B：审讯对话（角色扮演）

```text
你现在扮演嫌疑人 {suspect_name}。

角色信息：
- 姓名：{name}
- 职业：{occupation}
- 性格：{personality}
- 动机：{motive}
- 不在场证明：{alibi}
- 是否为真凶：{is_culprit}
- 隐藏信息：{secret}

审讯历史：
{interrogation_history}

侦探的问题：{question}

请输出 JSON，字段包括：
- response: 嫌疑人的回答
- emotion: 当前情绪（calm/nervous/angry/evasive/cooperative）
- revealed_info: 本次回答暴露的新信息（可选，无则为空字符串）

要求：
- 完全以该角色身份回答，符合性格特点
- 如果是真凶，在前几轮保持镇定，但面对关键证据时会出现破绽
- 如果不是真凶，可能会紧张但不会在关键事实上说谎
- 回答自然，像真实审讯对话
- 每次回答 2-4 句话
```

## 模块 C：现场勘察

```text
你是案件的旁白，需要描述侦探勘察现场的发现。

案件背景：{background}
勘察地点：{location_name} — {location_description}
本次发现的证据：{evidence_list}

请输出 JSON，字段包括：
- narration: 旁白描述（描述侦探如何发现这些线索，2-4句话）
- clues_found: 数组，每条包含：
  - id: 证据编号
  - discovery_text: 发现过程的具体描述

要求：
- 描述要有画面感和氛围
- 让玩家感受到探案的紧张感
```

## 模块 D：指控评估与评分

```text
你是公正的案件评审官，需要评估侦探的指控是否正确。

案件真相：
- 真凶：{culprit_name}
- 完整推理：{solution}
- 全部证据：{all_evidence}

侦探的指控：
- 指控对象：{accused_name}
- 推理过程：{reasoning}
- 引用证据：{cited_evidence}

已收集的证据：{collected_evidence}
使用的审讯轮数：{total_interrogation_rounds}
使用的勘察次数：{total_examinations}

请输出 JSON，字段包括：
- correct: true/false（指控对象是否正确）
- scores:
  - logic: 0-30（推理逻辑是否严密）
  - evidence: 0-30（证据引用是否充分）
  - completeness: 0-20（是否涵盖关键线索）
  - efficiency: 0-20（步骤效率，越少越高分）
  - total: 0-100
- feedback: 详细评语（3-5句话）
- truth_reveal: 揭示完整真相的叙述（供 TTS 朗读，3-5句话）

要求：
- 即使指控正确，推理不严密也应扣分
- efficiency 按总操作数评估：<10次=满分，10-20次=15分，20-30次=10分，>30次=5分
```

## 模块 E：历史压缩

```text
将以下审讯对话历史压缩为摘要，保留关键信息和矛盾点。

审讯对象：{suspect_name}
对话历史：
{full_history}

请输出 JSON，字段包括：
- summary: 压缩后的摘要（3-5句话）
- key_facts: 数组，关键事实点
- contradictions: 数组，发现的矛盾点

要求：
- 保留所有可能影响破案的关键信息
- 特别标注矛盾和可疑之处
```
