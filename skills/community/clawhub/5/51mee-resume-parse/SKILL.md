---
name: 51mee-resume-parse
description: 简历解析。触发场景：用户上传简历文件要求解析、提取结构化信息。
---

# 简历解析技能

## 功能说明

读取简历文件（PDF/DOC/DOCX/JPG/PNG），使用大模型提取结构化信息。

## 处理流程

1. **读取文件** - 用户上传简历时，读取文件内容
2. **提取文本** - 从文件中提取纯文本内容
3. **调用大模型** - 使用以下 prompt 解析
4. **返回 JSON** - 解析结果为结构化数据

## Prompt 模板

```
```html
{简历文本内容}
```
扮演一个简历分析专家，详细地分析上面的简历
1. 按照下方的typescript结构定义，返回json格式的ResumeInfo结构
2. 有数据就填上数据，简历上没有提到，相应的值即为null，绝对不要虚构新的或者删除定义中的字段
3. 不要做任何解释，直接返回json
4. 日期格式："Y-m-d"，如 "2025-01-01"; 年格式："Y"，如 "2025"
5. 手机号无区号，如"19821450628"

```typescript
export interface WorkExperience {
    startDate: string | null;
    endDate: string | null;
    company: string;
    industry: string | null;
    department: string | null;
    positionName: string;
    blueCollarPosition: boolean | null;
    responsibility: string | null;
    workPerformance: string | null;
    current: boolean | null;
    workDesc: string | null;
};

export interface ProjectExperience {
    name: string;
    startDate: string | null;
    endDate: string | null;
    roleName: string | null;
    projectDesc: string | null;
};

export interface EducationExperience {
    startDate: string | null;
    endDate: string | null;
    school: string;
    major: string | null;
    degreeName: string | null; // 高中、本科、专科、硕士、博士、其它
};

export interface ResumeInfo {
    name: string | null;
    gender: number | null; // 0=男, 1=女
    age: string | null;
    birthday: string | null;
    description: string | null;
    
    workExpList: WorkExperience[];
    projExpList: ProjectExperience[];
    eduExpList: EducationExperience[];
    
    expectPosition: {
        positionName: string | null;
        lowSalary: number | null;
        highSalary: number | null;
        locationName: string | null;
    };
    
    contact: {
        phone: string | null;
        weixin: string | null;
        email: string | null;
    };
    
    keywords: string[];
    awards: string[];
    englishCertificates: string[];
    professionalSkills: string;
}
```
```

## 返回数据结构

```json
{
  "name": "张三",
  "gender": 0,
  "age": "30",
  "birthday": "1995-01-15",
  "description": "5年Java开发经验...",
  
  "workExpList": [...],
  "projExpList": [...],
  "eduExpList": [...],
  
  "expectPosition": {...},
  "contact": {...},
  
  "keywords": ["Java", "Spring"],
  "awards": ["优秀员工"],
  "englishCertificates": ["CET-6"],
  "professionalSkills": "精通Java..."
}
```

## 输出格式

```markdown
## 简历解析结果

### 基本信息
- **姓名**: [name]
- **性别**: [男/女]
- **年龄**: [age]
- **生日**: [birthday]

### 联系方式
- **手机**: [phone]
- **微信**: [weixin]
- **邮箱**: [email]

### 工作经历
[遍历 workExpList]

### 项目经历
[遍历 projExpList]

### 教育经历
[遍历 eduExpList]

### 期望职位
- **职位**: [positionName]
- **薪资**: [lowSalary]K-[highSalary]K
- **地点**: [locationName]

### 关键词
[keywords]

### 奖项
[awards]

### 英语证书
[englishCertificates]

### 专业技能
[professionalSkills]
```

## 注意事项

- 支持格式：PDF、DOC、DOCX、JPG、PNG
- 日期格式统一为 `Y-m-d`
- 没有 的字段填 `null`
- 直接返回 JSON，不要额外解释
