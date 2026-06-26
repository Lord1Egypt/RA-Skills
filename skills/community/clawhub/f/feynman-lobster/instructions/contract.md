# 签约流程

当用户表达项目意愿时（"我在做 X 项目"、"签约"等），执行此流程。

若用户说"我想学 X"而非"我在做项目"，主动问："那你是在做什么项目来学 X？把项目路径和笔记路径给我，我读你的代码来教你。"

## 1. 收集基本要素

依次确认，一次只问一个。如果用户一句话说清了多个，不重复问。

- **做什么项目**（project）：用户正在做的事
- **为了什么**（motivation）：项目的目的、背景、想达成什么
- **给自己多久**（deadline）：截止日期
- **上下文路径**（resources）：项目代码、笔记、文档的路径——**必填**，龙虾需要读取这些内容才能按需教学

## 2. 上下文路径

签约时必须收集至少一个可读路径。用户可以说：

- "项目在 ~/projects/ml-project"
- "笔记在 ~/obsidian/翻译本.md"
- "代码在 ~/code/train.py"

写入 resources 时：

```json
{
  "type": "local",
  "title": "项目根目录",
  "path": "~/projects/ml-project"
},
{
  "type": "local",
  "title": "翻译本",
  "path": "~/obsidian/翻译本.md"
}
```

若用户签约时没给路径，主动问：

```
项目代码或笔记在哪个路径？我会读取这些内容（只读），基于你实际写的东西来教你。
```

## 3. 知识背景清单

将「做这个项目需要的知识背景」拆解为清单，分两类：

- **概念型**：gradient descent、loss function、过拟合...
- **工具型**：PyTorch DataLoader、wandb 日志、学会调学习率...

清单服务于项目，不是独立的学习课程。每个条目附一句话说明为什么做这个项目需要它。

展示给用户确认：

```
做「{project}」这个项目，你可能需要这些知识背景：

概念型：
1. {概念A} — {为什么需要}
2. {概念B} — {为什么需要}

工具型：
3. {工具/框架A} — {为什么需要}
...

这个清单是动态的，之后我读你的项目时发现新的需求会再加。有问题吗？
```

## 4. 可选信息

签约确认后，再问（都可跳过）：

```
还有几件事：

1. 完成后你想怎么奖励自己？（选填）
2. 要找监工吗？把对方龙虾地址发我就行。
```

## 5. 写入 contracts.json

```json
{
  "id": "contract_{timestamp}",
  "project": "{project}",
  "goal": "{project}",
  "motivation": "{motivation}",
  "reward": "{reward 或空}",
  "deadline": "{deadline}",
  "created_at": "{now}",
  "status": "active",
  "resources": [
    { "type": "local", "title": "...", "path": "..." }
  ],
  "clauses": [
    {
      "id": "clause_1",
      "concept": "...",
      "category": "concept",
      "status": "pending",
      "attempts": 0,
      "mastered_at": null,
      "added_reason": null
    }
  ],
  "supervisors": [],
  "last_active_at": "{now}"
}
```

注：保留 `goal` 字段以兼容现有面板，值与 `project` 相同。

## 6. 写入用户画像和项目摘要

签约后立即写入两个地方，不要写入统一的 `MEMORY.md`：

**A. `USER_PROFILE.md`**（若从对话中捕捉到新的跨项目信息）：
```markdown
## 用户画像
- {日期}: 项目「{project}」。动机：{motivation}。背景：{从对话中捕捉到的用户背景}
```

只写跨项目仍然有价值的信息，如背景、学习偏好、学习风格。不要把当前项目的具体概念进度写到这里。

**B. `contract-memory/{contract_id}.md`**（新建当前契约的项目摘要文件）：
```markdown
# 契约 {contract_id} — {project}

## 当前目标
- 项目：{project}
- 动机：{motivation}
- 截止：{deadline}

## 概念理解记录
（签约时为空，后续追问时填充）

## 知识盲区
（签约时为空，后续追问时填充）

## 阶段总结
（按需填充）
```

如果 `contract-memory/` 目录不存在，先创建。

## 7. 确认消息

```
🦞 契约生效！

"{project}"
我会读你的项目和笔记，在你需要时教你需要的知识。遇到不懂的随时问我，我也会主动发现你可能不懂的地方来问你。

面板：http://localhost:19380
```
