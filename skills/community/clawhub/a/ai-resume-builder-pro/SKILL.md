---
name: ai-resume-pro
description: Professional AI resume builder that creates ATS-optimized resumes with tailored content, achievement highlighting, and industry-specific templates. Includes cover letter generation and LinkedIn optimization.
---

# AI Resume Pro

Professional resume creation tool powered by AI. Creates ATS-optimized resumes that pass applicant tracking systems and impress hiring managers.

---

## Features

### 📄 ATS-Optimized Resumes

- **Keyword Optimization**: Match job descriptions
- **Format Compliance**: ATS-friendly layouts
- **Section Structure**: Proper headings and organization
- **File Formats**: PDF, DOCX, TXT exports

### ✨ Content Enhancement

- **Achievement Highlighting**: Quantify accomplishments
- **Action Verbs**: Strong, impactful language
- **Skills Matching**: Align with job requirements
- **Industry Terminology**: Sector-specific keywords

### 📝 Cover Letters

- **Customized Content**: Tailored to each job
- **Company Research**: Incorporate company values
- **Hiring Manager Focus**: Address decision-makers
- **Call to Action**: Strong closing statements

### 💼 LinkedIn Optimization

- **Profile Summary**: Compelling headline and about section
- **Experience Descriptions**: Detailed role descriptions
- **Skills Section**: Relevant skill endorsements
- **Recommendation Requests**: Template for asking

---

## Usage

### Basic Resume Creation

```javascript
const builder = new ResumeBuilder();

const resume = await builder.createResume({
  personalInfo: {
    name: '张三',
    email: 'zhangsan@email.com',
    phone: '138-0000-0000',
    location: '北京'
  },
  experience: [
    {
      company: '某某科技公司',
      position: '高级软件工程师',
      startDate: '2020-01',
      endDate: 'present',
      responsibilities: [
        '负责后端系统开发',
        '带领 5 人团队',
        '优化系统性能提升 50%'
      ]
    }
  ],
  education: [
    {
      school: '北京大学',
      degree: '计算机科学与技术',
      year: '2016-2020'
    }
  ],
  targetJob: '高级后端开发工程师'
});

console.log(resume.content);
```

### Job-Tailored Resume

```javascript
const tailoredResume = await builder.tailorResume({
  resume: existingResume,
  jobDescription: jobPosting,
  emphasize: ['leadership', 'performance-optimization']
});
```

### Cover Letter Generation

```javascript
const coverLetter = await builder.generateCoverLetter({
  resume: resume,
  company: '某某公司',
  position: '高级后端开发工程师',
  hiringManager: '技术总监',
  keyPoints: ['5 年后端经验', '高并发系统经验', '团队管理经验']
});
```

---

## Architecture

```
User Input (Experience, Education, Skills)
    ↓
Content Analysis Agent
    ├─ Extract key achievements
    ├─ Identify transferable skills
    └─ Match with target job
    ↓
ATS Optimization Agent
    ├─ Keyword optimization
    ├─ Format compliance check
    └─ Section structure
    ↓
Content Enhancement Agent
    ├─ Achievement quantification
    ├─ Action verb enhancement
    └─ Industry terminology
    ↓
Template Selection
    ├─ Industry-appropriate design
    ├─ Experience level matching
    └─ ATS compatibility
    ↓
Final Resume (PDF/DOCX)
```

---

## Templates

### By Industry

- **Technology**: Clean, modern design
- **Finance**: Conservative, professional
- **Creative**: Visual, portfolio-focused
- **Healthcare**: Detailed, certification-focused
- **Education**: Achievement-oriented

### By Experience Level

- **Entry-Level**: Education-focused, internships highlighted
- **Mid-Level**: Experience and achievements balanced
- **Senior**: Leadership and impact emphasized
- **Executive**: Strategic vision and results

---

## Best Practices

### Content

1. **Quantify Achievements**: Use numbers and metrics
2. **Use Action Verbs**: Led, Managed, Developed, Optimized
3. **Tailor for Each Job**: Match keywords from job description
4. **Keep It Concise**: 1-2 pages maximum
5. **Proofread**: Zero typos or grammatical errors

### Format

1. **Simple Layout**: Avoid complex designs
2. **Standard Fonts**: Arial, Calibri, Times New Roman
3. **Clear Headings**: Easy to scan
4. **Consistent Formatting**: Dates, bullets, spacing
5. **ATS-Friendly**: No images, tables, or graphics

---

## Example Output

```markdown
# 张三
**高级软件工程师**

📧 zhangsan@email.com | 📱 138-0000-0000 | 📍 北京

## 个人总结
5 年后端开发经验，专注于高并发系统设计。曾带领 5 人团队优化系统性能，提升 50% 响应速度。熟悉 Java、Python、Go 等技术栈。

## 工作经历

### 某某科技公司 | 高级软件工程师
*2020-01 - 至今*

- **系统优化**: 重构核心模块，响应时间从 500ms 降至 250ms，提升 50%
- **团队领导**: 带领 5 人团队，完成 3 个大型项目，客户满意度 95%
- **技术创新**: 引入微服务架构，系统可扩展性提升 3 倍

### 某某创业公司 | 软件工程师
*2018-06 - 2019-12*

- **产品开发**: 从 0 到 1 开发核心产品，用户增长至 10 万+
- **性能优化**: 数据库优化，查询速度提升 80%

## 教育背景

**北京大学** | 计算机科学与技术 | 本科
*2016-2020*

## 技能

- **编程语言**: Java, Python, Go, JavaScript
- **框架**: Spring Boot, Django, Gin
- **数据库**: MySQL, PostgreSQL, Redis, MongoDB
- **工具**: Git, Docker, Kubernetes, Jenkins

## 证书

- AWS 认证解决方案架构师
- Oracle Java 认证专家
```

---

## Installation

```bash
clawhub install ai-resume-pro
```

---

## API Reference

### `createResume(options)`

Create a new resume from scratch.

**Parameters**:
- `personalInfo`: Personal information
- `experience`: Work experience array
- `education`: Education array
- `skills`: Skills list
- `targetJob`: Target job title

**Returns**: Resume object with formatted content

### `tailorResume(options)`

Tailor existing resume for specific job.

**Parameters**:
- `resume`: Existing resume
- `jobDescription`: Job posting text
- `emphasize`: Skills/experience to emphasize

**Returns**: Tailored resume

### `generateCoverLetter(options)`

Generate customized cover letter.

**Parameters**:
- `resume`: Candidate resume
- `company`: Company name
- `position`: Job position
- `hiringManager`: Hiring manager name (optional)

**Returns**: Cover letter text

---

## License

MIT

---

## Author

AI-Agent

---

## Version

1.1.0

---

## Created

2026-04-02

---

## Updated

2026-04-02 (Enhanced with examples and best practices)
