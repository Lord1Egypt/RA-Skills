# AI Resume Screener

智能简历筛选，HR 效率提升 10 倍。

## 核心能力

✅ 简历解析 - 自动提取姓名/学历/经验/技能
✅ 智能匹配 - 根据职位要求自动评分排序
✅ 批量处理 - 一次处理 1000+ 份简历
✅ 多格式支持 - PDF/Word/图片/在线简历
✅ 偏见消除 - 匿名筛选，降低人为偏见
✅ 数据分析 - 简历来源、通过率、时间分析

## 快速开始

### 1. 安装
```bash
openclaw skills install ai-resume-screener
```

### 2. 配置职位要求
```yaml
name: ai-resume-screener
config:
  # 职位模板
  position:
    title: "Python开发工程师"
    requirements:
      - "3年以上Python经验"
      - "熟悉Django/Flask"
      - "有大型项目经验优先"
    skills:
      - Python: required
      - Django: preferred
      - Docker: plus
      
  # 评分权重
  scoring:
    skills: 40%
    experience: 30%
    education: 20%
    projects: 10%
```

### 3. 筛选简历
```bash
# 批量筛选
openclaw run --screen-resumes ./resumes_folder --position python_dev

# 查看排名
openclaw run --show-ranking --top 10
```

## ROI 计算

| 指标 | 人工筛选 | AI 筛选 | 提升 |
|------|----------|---------|------|
| 单份耗时 | 5 分钟 | 5 秒 | 60x |
| 日处理量 | 50 份 | 5000 份 | 100x |
| 匹配准确率 | 60% | 85% | +25% |
| HR 成本 | ¥8000/月 | ¥800/月 | 10x |

## 定价

| 套餐 | 价格 | 功能 |
|------|------|------|
| 基础版 | ¥199 | 简历解析 + 100份/月 |
| 专业版 | ¥499 | 智能匹配 + 1000份/月 |
| 企业版 | ¥1499 | 无限简历 + 多职位 + 定制 |

## 客户案例

### 某互联网公司
- 月均简历：3000 份
- HR 时间：从 100 小时降至 2 小时
- 招聘周期：缩短 40%

### 某猎头公司
- 简历库：10 万份
- 匹配速度：从 1 天降至 5 分钟
- 成单率：提升 30%

## 技术支持

- 📧 Email: contact@openclaw-cn.com
- 💬 Telegram: @openclaw_service
- 📱 微信: openclaw-cn

---

**安装配置服务**：¥199 起，30 分钟搞定！