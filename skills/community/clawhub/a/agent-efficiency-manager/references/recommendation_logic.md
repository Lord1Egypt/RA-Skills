# 技能推荐逻辑详解

本文档说明如何基于 Agent 角色和配置，智能推荐适配的技能。

---

## 推荐流程

```
输入：Agent 配置 + 可用技能列表
    ↓
步骤1：识别 Agent 角色（role_detection）
    ↓
步骤2：过滤可用技能（skill_filtering）
    ↓
步骤3：匹配评分（matching_score）
    ↓
步骤4：排序与截断（ranking）
    ↓
输出：Top-N 推荐列表
```

---

## 步骤1：角色识别（role_detection）

### 方法：关键词匹配

**角色关键词映射表：**

| 角色 | 关键词（agent.name / agent.id） |
|------|--------------------------------|
| stock | stock, finance, trading, market, analysis |
| writer | write, doc, report, content |
| realestate | realestate, property, house, home |
| enterprise | enterprise, service, customer |
| investment | investment, park, business |
| contract | contract, legal, review |
| finance | finance, forecast, budget |
| training | training, education, course |

**实现：**
```python
def detect_agent_role(agent_config):
    agent_name = agent_config.get("name", "").lower()
    agent_id = agent_config.get("id", "").lower()
    
    for role, keywords in ROLE_KEYWORDS.items():
        if any(kw in agent_name or kw in agent_id for kw in keywords):
            return role
    
    return "general"  # 未匹配，使用通用推荐
```

---

## 步骤2：技能过滤（skill_filtering）

### 过滤规则

1. **排除已安装**：`skill.name not in agent.skills`
2. **按角色匹配**：技能描述包含角色关键词
3. **质量门槛**：评分 ≥ 4.0，下载量 ≥ 100
4. **兼容性检查**：技能无已知冲突

**实现：**
```python
def filter_skills(available_skills, agent_config):
    current_skills = set(agent_config.get("skills", []))
    agent_role = detect_agent_role(agent_config)
    
    filtered = []
    for skill in available_skills:
        # 规则1：排除已安装
        if skill["name"] in current_skills:
            continue
        
        # 规则2：按角色匹配
        if not is_role_match(skill, agent_role):
            continue
        
        # 规则3：质量门槛
        if skill.get("rating", 0) < 4.0:
            continue
        if skill.get("downloads", 0) < 100:
            continue
        
        # 规则4：兼容性检查（TODO）
        
        filtered.append(skill)
    
    return filtered

def is_role_match(skill, role):
    """检查技能是否匹配角色"""
    if role == "general":
        return True  # 通用推荐，不过滤
    
    skill_desc = skill.get("description", "").lower()
    keywords = ROLE_KEYWORDS.get(role, [])
    
    return any(kw in skill_desc for kw in keywords)
```

---

## 步骤3：匹配评分（matching_score）

### 评分维度

| 维度 | 权重 | 说明 |
|------|------|------|
| **角色相关度** | 50% | 技能描述与角色关键词的匹配程度 |
| **评分** | 30% | skillhub 用户评分（1-5 分） |
| **下载量** | 20% | 技能受欢迎程度（对数缩放） |

**计算公式：**
```python
def calculate_matching_score(skill, agent_role):
    # 维度1：角色相关度（0-1）
    role_relevance = calculate_role_relevance(skill, agent_role)
    
    # 维度2：评分（0-1）
    rating_score = skill.get("rating", 0) / 5.0
    
    # 维度3：下载量（0-1，对数缩放）
    downloads = skill.get("downloads", 0)
    download_score = min(1.0, math.log10(downloads + 1) / 3.0)  # 1000 次下载 ≈ 1.0
    
    # 加权求和
    final_score = (
        role_relevance * 0.5 +
        rating_score * 0.3 +
        download_score * 0.2
    )
    
    return final_score

def calculate_role_relevance(skill, agent_role):
    """计算角色相关度"""
    skill_desc = skill.get("description", "").lower()
    keywords = ROLE_KEYWORDS.get(agent_role, [])
    
    if not keywords:
        return 0.5  # 通用技能，中等相关度
    
    # 计算关键词命中率
    hits = sum(1 for kw in keywords if kw in skill_desc)
    relevance = hits / len(keywords)
    
    return relevance
```

---

## 步骤4：排序与截断（ranking）

### 策略

1. **按评分降序排列**
2. **截断到 Top-5**（避免推荐过多）
3. **去重**（移除功能重复的技能）

**实现：**
```python
def rank_and_truncate(skills, top_n=5):
    # 按评分排序
    sorted_skills = sorted(skills, key=lambda x: x["matching_score"], reverse=True)
    
    # 去重（基于功能描述相似度，TODO）
    
    # 截断
    return sorted_skills[:top_n]
```

---

## 特殊规则

### 1. 新 Agent 推荐通用技能

对于新创建的 Agent（技能数 < 5），推荐通用基础技能：
- `online-search`（联网搜索）
- `docx`（文档处理）
- `pdf`（PDF 处理）
- `xlsx`（表格处理）

### 2. 跨领域技能警告

如果推荐了与 Agent 角色无关的技能，添加警告标签：
```python
{
    "skill_name": "stock-analysis",
    "reason": "匹配角色：stock",
    "warning": "⚠️ 此技能与 Agent 角色可能无关，请确认是否必要"
}
```

### 3. 技能冲突检测

检测功能重复的技能（如 `another_them` 和 `another-them`）：
```python
def detect_conflicts(recommended_skills):
    """检测推荐列表中的功能冲突"""
    conflicts = []
    
    # 规则：another_them 和 another-them 不能同时存在
    if "another_them" in recommended_skills and "another-them" in recommended_skills:
        conflicts.append({
            "skills": ["another_them", "another-them"],
            "reason": "功能重复，建议只保留一个"
        })
    
    return conflicts
```

---

## 输出格式

### 推荐列表项

```json
{
    "skill_name": "auto-translator",
    "description": "自动翻译技能，支持多语言文档翻译",
    "rating": 4.5,
    "downloads": 1200,
    "matching_score": 0.85,
    "reason": "匹配角色：writer（文档处理相关）",
    "warning": null
}
```

### 完整推荐报告

```json
{
    "agent_id": "writer",
    "agent_name": "莱特先生",
    "add_recommendations": [
        { ... },
        { ... }
    ],
    "remove_suggestions": [
        {
            "skill": "another_them / another-them",
            "reason": "重复技能，建议只保留一个"
        }
    ],
    "summary": "建议添加 2 个技能，移除 1 个"
}
```

---

## 调优建议

1. **定期更新角色关键词**：根据实际使用效果调整
2. **引入用户反馈**：记录推荐采纳率，优化评分权重
3. **A/B 测试**：对比不同评分策略的效果
4. **考虑技能依赖**：推荐时检查依赖关系（如 `docx` 依赖 `python-docx`）

---

**最后更新：** 2026-05-29
