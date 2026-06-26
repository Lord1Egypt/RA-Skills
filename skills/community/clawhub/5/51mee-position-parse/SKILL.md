---
name: 51mee-position-parse
description: 职位解析。触发场景：用户提供职位描述要求解析；用户想分析JD的核心要求。
---

# 职位解析技能

## 功能说明

解析职位描述（JD）文本，使用大模型提取结构化信息。

## 处理流程

1. **接收文本** - 用户提供职位描述
2. **调用大模型** - 使用以下 prompt 解析
3. **返回 JSON** - 结构化职位信息

## Prompt 模板

```
```text
{职位描述文本}
```
扮演一个职位分析专家，详细分析上面的职位描述
1. 按照下方的typescript结构定义，返回json格式的PositionInfo结构
2. 有数据就填上数据，JD上没有提到，相应的值即为null，绝对不要虚构新的或删除定义中的字段
3. 不要做任何解释，直接返回json

```typescript
export interface PositionInfo {
    positionName: string;          // 职位名称
    positionType: string | null;   // 职位类型：技术类/市场类/运营类等
    experienceRequired: string | null; // 经验要求，如"3-5年"
    educationRequired: string | null;  // 学历要求
    salaryRange: {
        min: number | null;
        max: number | null;
    };
    
    company: {
        name: string | null;
        industry: string | null;
        scale: string | null;  // 公司规模
    };
    
    requirements: {
        skills: string[];          // 技能要求
        responsibilities: string[]; // 岗位职责
        softSkills: string[];       // 软技能要求
    };
    
    keywords: string[];
}
```
```

## 返回数据结构

```json
{
  "positionName": "高级Java开发工程师",
  "positionType": "技术类",
  "experienceRequired": "5年以上",
  "educationRequired": "本科及以上",
  "salaryRange": {
    "min": 20000,
    "max": 35000
  },
  "company": {
    "name": null,
    "industry": "互联网/IT",
    "scale": null
  },
  "requirements": {
    "skills": ["Java", "Spring Boot", "MySQL"],
    "responsibilities": ["系统架构设计", "核心代码开发"],
    "softSkills": ["团队协作", "沟通能力"]
  },
  "keywords": ["Java", "Spring Boot", "架构"]
}
```

## 输出格式

```markdown
## 职位分析报告

### 基本信息
- **职位**: [positionName]
- **类型**: [positionType]
- **经验要求**: [experienceRequired]
- **学历要求**: [educationRequired]

### 薪资范围
[salaryRange.min]K - [salaryRange.max]K

### 技能要求
| 必备 | 加分 |
|------|------|
| [skill1] | [skillA] |

### 岗位职责
1. [responsibility1]
2. [responsibility2]

### 软技能要求
- [softSkill1]
- [softSkill2]

### 关键词
[keywords]
```

## 注意事项

- 职位描述越详细，解析越准确
- 没有 的字段填 `null`
- 直接返回 JSON，不要额外解释
