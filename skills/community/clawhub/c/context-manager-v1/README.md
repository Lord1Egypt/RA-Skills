# 🔧 knowledge-workflow Skill

> 完整的知识管理工作流 - 可发布到 ClawHub
> 版本：v1.0

---

## 📋 目录结构

```
knowledge-workflow/
├── SKILL.md                 # Skill 文档（本文档）
├── main.py                  # 主程序
├── config.yaml              # 配置文件
├── clawhub.yaml             # ClawHub 发布配置
├── requirements.txt         # Python 依赖
└── subfunctions/            # 子功能模块
    ├── collect.py           # 收集功能
    ├── tag.py               # 打标功能
    ├── store.py             # 存储功能
    ├── evolve.py            # 知识发芽
    └── output.py            # 产出功能
```

---

## 🚀 安装

### 方式 1：从 ClawHub 安装（发布后）

```bash
clawhub install knowledge-workflow
```

### 方式 2：本地安装

```bash
cd ~/kb/skills/knowledge-workflow
pip install -r requirements.txt
```

---

## 💡 使用方式

### 方式 1：一键调用（完整工作流）

```bash
# 处理飞书文档
python main.py run feishu PFAvdKEILouK29xCgNuc5b1bnnK

# 处理微信读书导出
python main.py run wechat "[微信读书导出文本]"

# 处理 URL
python main.py run url https://example.com/article
```

### 方式 2：分步调用

```bash
# 步骤 1: 收集
python main.py collect feishu PFAvdKEILouK29xCgNuc5b1bnnK

# 步骤 2: 打标
python main.py tag note-20260414160000

# 步骤 3: 知识发芽
python main.py evolve note-20260414160000 spark

# 步骤 4: 产出文章
python main.py output spark-20260414160000 article
```

### 方式 3：作为 Python 库调用

```python
from main import KnowledgeWorkflow

kw = KnowledgeWorkflow()

# 一键调用
result = kw.run(
    source_type="feishu",
    content="PFAvdKEILouK29xCgNuc5b1bnnK",
    auto_execute=True
)

# 分步调用
note = kw.collect(source_type="feishu", content="PFAvdKEILouK29xCgNuc5b1bnnK")
tagged = kw.tag(note_id=note["note_id"], content=note["content"])
stored = kw.store(note_id=tagged["note_id"], content=tagged["content"], tags=tagged["tags"])
evolved = kw.evolve(note_id=stored["note_id"], evolve_type="spark")
article = kw.output(evolve_id=evolved["evolve_id"], output_type="article")
```

### 方式 4：OpenClaw Skill 调用

```
@ant knowledge-workflow:
来源：飞书文档 PFAvdKEILouK29xCgNuc5b1bnnK
自动执行：collect → tag → store → evolve → output
```

---

## 📊 子功能 API

### collect（收集）

```python
kw.collect(
    source_type="feishu|wechat|url|text",
    content="doc_token|URL|文本",
    metadata={"title": "可选标题"}
)
```

### tag（打标）

```python
kw.tag(
    note_id="note-001",
    content="笔记内容"
)
```

### store（存储）

```python
kw.store(
    note_id="note-001",
    content="带标签的笔记",
    tags={"themes": [...], "scenes": [...], "actions": [...]}
)
```

### evolve（知识发芽）

```python
kw.evolve(
    note_id="note-001",
    evolve_type="spark|model|cross|habit|subconscious"
)
```

### output（产出）

```python
kw.output(
    evolve_id="spark-001",
    output_type="article|weekly|monthly"
)
```

---

## 🔧 配置

编辑 `config.yaml`：

```yaml
storage:
  default_type: "local"  # local|feishu|obsidian
  base_path: "~/kb"

tagging:
  auto_tag: true
  confidence_threshold: 0.6

evolution:
  default_type: "spark"  # spark|model|cross|habit|subconscious

output:
  default_type: "article"  # article|weekly|monthly
```

---

## 📤 发布到 ClawHub

### 1. 检查配置

```bash
cat clawhub.yaml
```

### 2. 测试

```bash
python main.py run feishu PFAvdKEILouK29xCgNuc5b1bnnK
```

### 3. 发布

```bash
clawhub publish
```

### 4. 验证

```bash
clawhub search knowledge-workflow
```

---

## 🎯 使用场景

### 场景 1：个人知识管理

```
用户：我刚刚读了一篇好文章，想整理一下
→ 调用 knowledge-workflow
→ 输出：打标笔记 + 灵光闪现 + 存储路径
```

### 场景 2：团队知识沉淀

```
用户：把这个会议记录沉淀到团队知识库
→ 调用 knowledge-workflow
→ 输出：飞书文档 + 周报草稿
```

### 场景 3：自媒体内容生产

```
用户：基于这篇读书笔记，生成公众号文章
→ 调用 knowledge-workflow evolve + output
→ 输出：公众号文章草稿
```

---

## 📝 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.0 | 2026-04-14 | 初始版本，包含 5 个子功能 |

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

## 📄 许可证

MIT License

---

**维护者**：燃冰 & ant  
**版本**：v1.0  
**创建日期**：2026-04-14  
**发布状态**：待发布
