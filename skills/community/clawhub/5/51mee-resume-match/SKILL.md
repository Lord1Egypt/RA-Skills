---
name: 51mee-resume-match
description: 人岗匹配。触发场景：用户要求匹配简历和职位；用户问这个候选人适合这个职位吗；用户要筛选最匹配的候选人。
---

# 人岗匹配技能

## 功能说明

评估候选人与职位的匹配程度，生成匹配度评分和分维度分析。

## API 调用

**接口地址**: `https://openapi.51mee.com/api/v1/parse/match`

**请求方式**: POST (multipart/form-data)

**参数**:
- `file`: 简历文件（必填）
- `jd_text`: 职位描述文本（必填）

**调用命令**:
```bash
curl -X POST "https://openapi.51mee.com/api/v1/parse/match" \
  -F "file=@候选人简历.pdf" \
  -F "jd_text=岗位职责:\n1. 负责系统架构设计\n\n任职要求:\n- 5年以上Java开发经验\n- 熟悉Spring Boot"
```

## 返回数据结构

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "overall_score": 85,
    "overall_level": "良好",
    "star_rating": 4,
    
    "dimensions": {
      "skill_match": {
        "score": 90,
        "level": "优秀",
        "matched_skills": ["Java", "Spring Boot", "MySQL"],
        "missing_skills": ["Docker", "K8s"],
        "details": "核心技能完全匹配"
      },
      "experience_match": {
        "score": 85,
        "level": "良好",
        "required_years": 5,
        "actual_years": 6,
        "industry_match": true,
        "details": "经验年限符合要求"
      },
      "education_match": {
        "score": 95,
        "level": "优秀",
        "required": "本科",
        "actual": "本科",
        "details": "学历符合要求"
      },
      "salary_match": {
        "score": 70,
        "level": "一般",
        "budget_range": "20K-25K",
        "expected_range": "25K-30K",
        "details": "期望薪资略高于预算"
      }
    },
    
    "advantages": [
      "技术栈高度匹配，Java/Spring/MySQL 都有实战经验",
      "有大型项目经验，处理过高并发场景",
      "职业发展路径清晰，稳定性好"
    ],
    
    "gaps": [
      "缺少容器化经验（Docker/K8s）",
      "期望薪资 25K，略高于预算 20K"
    ],
    
    "risks": [
      "最近一份工作时间较短（8个月）"
    ],
    
    "interview_suggestions": [
      "重点考察高并发项目细节",
      "了解跳槽原因",
      "评估容器化技术学习能力"
    ],
    
    "recommendation": {
      "should_interview": true,
      "confidence": 85,
      "reason": "综合素质优秀，技术匹配度高，值得深入沟通"
    }
  }
}
```

## 匹配维度说明

| 维度 | 字段 | 权重 | 说明 |
|------|------|------|------|
| 技能匹配 | `skill_match` | 高 | 技术栈是否对口 |
| 经验匹配 | `experience_match` | 高 | 工作年限、行业背景 |
| 学历匹配 | `education_match` | 中 | 教育背景 |
| 薪资匹配 | `salary_match` | 视情况 | 期望与预算对比 |

## 评分等级

| 分数 | 等级 | 星级 |
|------|------|------|
| 90-100 | 优秀 | ⭐⭐⭐⭐⭐ |
| 75-89 | 良好 | ⭐⭐⭐⭐ |
| 60-74 | 一般 | ⭐⭐⭐ |
| 0-59 | 较差 | ⭐⭐ |

## 输出模板

```markdown
## 候选人匹配报告

**候选人**: [姓名]
**综合匹配度**: [score]/100 ⭐⭐⭐⭐

### 分维度评估
| 维度 | 得分 | 评级 | 说明 |
|------|------|------|------|
| 技能匹配 | [score] | [level] | [details] |
| 经验匹配 | [score] | [level] | [details] |
| 学历匹配 | [score] | [level] | [details] |
| 薪资匹配 | [score] | [level] | [details] |

### 核心优势 ✅
- [advantage1]
- [advantage2]

### 需关注 ⚠️
- [gap1]
- [gap2]

### 面试建议
- [suggestion1]
- [suggestion2]

### 推荐
**[建议/不建议]面试** - [reason]
```

## 批量筛选流程

当用户要筛选多个候选人时：

1. **定义岗位要求** - 收集完整的职位描述
2. **逐个匹配** - 对每个候选人调用匹配接口
3. **对比排序** - 按 `overall_score` 排序
4. **输出报告** - 生成排名对比表

## 注意事项

- 必须同时提供简历文件和职位描述
- 职位描述越详细，匹配越准确
- 先检查返回的 `code` 字段
- 匹配结果是 AI 分析，最终决策需人工判断
