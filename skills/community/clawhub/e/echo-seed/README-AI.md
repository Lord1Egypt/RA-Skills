# Echo Seed AI 分析功能

> 🧠 让种子更智能 - AI 点子扩张、链接分析、智能关联

---

## 📋 功能特性

### 1. AI 点子扩张 💡
输入简单想法，AI 帮你扩展成完整方案：
- 技术方案（使用什么技术栈）
- 核心功能（主要功能列表）
- 工作量评估（预计开发时间）
- 风险评估（可能的风险和挑战）
- 行动建议（下一步可以做什么）

**示例：**
```
输入："做个 VR 版 B 站"

输出：
- 技术方案：Unity、Meta Quest SDK、WebXR...
- 核心功能：沉浸式视频播放大厅、3D 弹幕系统...
- 工作量：MVP 版本 4-6 个月
- 风险：VR 硬件保有量有限、开发成本高...
- 行动建议：先做 2D Demo 视频演示视觉概念...
```

### 2. AI 链接分析 🔗
输入 URL，AI 自动提取内容并总结：
- 网页内容摘要
- 关键词提取
- 标签建议

### 3. 智能关联 🔍
自动发现相关种子：
- 基于关键词匹配
- 相似度排序
- 帮助发现知识关联

---

## 🚀 快速开始

### 1. 数据库迁移

```bash
cd /root/.openclaw/workspace/echo-seed
python3 -c "
import sqlite3
conn = sqlite3.connect('data/capsules.db')
with open('migration.sql', 'r') as f:
    conn.executescript(f.read())
conn.commit()
conn.close()
"
```

### 2. 启动服务

```bash
cd /root/.openclaw/workspace/echo-seed
python3 scripts/echo-web.py
```

访问：http://localhost:5000

### 3. 访问 AI 分析面板

访问：http://localhost:5000/ai.html

---

## 📖 API 文档

### AI 点子扩张
```bash
POST /api/capsule/<capsule_id>/analyze/expand

# Response
{
    "code": 200,
    "data": {
        "expanded": {
            "技术方案": ["Unity", "Meta XR SDK"],
            "核心功能": ["虚拟屏幕", "弹幕渲染"],
            "工作量": "MVP 2-3 周",
            "风险": ["API 封禁", "法律风险"],
            "行动建议": ["研究 API", "学习 Unity"]
        },
        "related_capsules": [...],
        "suggested_tags": ["VR", "B 站"]
    }
}
```

### AI 链接分析
```bash
POST /api/capsule/<capsule_id>/analyze/link

# Response
{
    "code": 200,
    "data": {
        "url": "https://...",
        "analysis": {
            "summary": "网页内容摘要...",
            "keywords": ["关键词 1", "关键词 2"],
            "suggested_tags": ["标签 1", "标签 2"]
        }
    }
}
```

### 智能关联
```bash
GET /api/capsule/<capsule_id>/relations

# Response
{
    "code": 200,
    "data": {
        "relations": [
            {"id": "123", "title": "相关种子", "similarity": 0.85}
        ]
    }
}
```

---

## 🗄️ 数据库结构

### ai_analyses - AI 分析记录表
```sql
CREATE TABLE ai_analyses (
    id INTEGER PRIMARY KEY,
    capsule_id TEXT,
    analysis_type TEXT,  -- 'expansion', 'link', 'relation'
    input_content TEXT,
    output_content TEXT,
    tokens_used INTEGER,
    created_at DATETIME
);
```

### capsule_relations - 种子关联表
```sql
CREATE TABLE capsule_relations (
    id INTEGER PRIMARY KEY,
    source_capsule_id TEXT,
    target_capsule_id TEXT,
    relation_type TEXT,  -- 'semantic', 'keyword', 'time'
    similarity_score REAL
);
```

### capsule_tags - 自动标签表
```sql
CREATE TABLE capsule_tags (
    id INTEGER PRIMARY KEY,
    capsule_id TEXT,
    tag_name TEXT,
    tag_source TEXT,  -- 'auto' or 'manual'
    confidence_score REAL
);
```

---

## 🔧 配置说明

### 小小爪 API 配置

在 `scripts/ai_service.py` 中配置：
```python
XIAOXIAOZHAO_CONFIG = {
    "base_url": "https://api.minimaxi.com/anthropic/v1",
    "api_key": "sk-xxx",
    "model": "MiniMax-M2.5"
}
```

### 环境变量
```bash
export FLASK_DEBUG=True  # 调试模式
export PORT=5000         # 端口
```

---

## ✅ 测试报告

**测试时间：** 2026-03-06 22:30

| 功能 | 状态 | 说明 |
|------|------|------|
| AI 点子扩张 | ✅ 通过 | 小小爪输出详细方案 |
| AI 链接分析 | ⚠️ 部分通过 | SSL 证书问题（网络环境） |
| 智能关联 | ✅ 通过 | 关键词匹配正常 |
| 数据库迁移 | ✅ 通过 | 3 张表创建成功 |
| 前端 UI | ✅ 通过 | Vue3 组件正常渲染 |

---

## 📝 使用示例

### 1. 点子扩张
1. 打开 AI 分析面板 (http://localhost:5000/ai.html)
2. 选择一个种子
3. 点击"💡 点子扩张"
4. 查看 AI 生成的详细方案

### 2. 链接分析
1. 选择一个包含 URL 的种子
2. 点击"🔗 链接分析"
3. 查看 AI 总结的网页内容

### 3. 智能关联
1. 选择一个种子
2. 点击"🔗 智能关联"
3. 查看相关的其他种子

---

## 🐛 已知问题

1. **链接分析 SSL 问题** - 某些网站证书验证失败（网络环境问题）
2. **关联准确度** - 基于关键词匹配，语义理解有限

---

## 📚 开发者

- **架构师：** 小爪（同中书门下平章事）
- **开发工程师：** 小小爪（六部尚书）
- **开发范式：** 儒家式开发

---

## 📜 许可证

MIT License

---

**最后更新：** 2026-03-06 22:30
