---
name: chinese-office-automation
description: 中文办公自动化 - 专为中文用户设计的办公自动化技能套件。集成中文文档处理、拼音转换、节假日判断、农历支持等功能。
metadata:
  openclaw:
    requires:
      bins: ["python3"]
    install:
      - id: python3
        kind: binary
        binary: python3
        label: Install Python 3
      - id: zhdate
        kind: python-package
        package: zhdate
        label: Install zhdate for Chinese calendar
---

# 中文办公自动化 (Chinese Office Automation)

专为中文用户设计的办公自动化技能套件，解决中文特有的办公场景需求。

## 功能特性

### 1. 中文文档处理
- 简繁转换
- 中文分词和关键词提取
- 中文文本摘要
- 敏感词过滤

### 2. 日期时间处理
- 中国节假日判断
- 农历日期转换
- 工作日计算（考虑调休）
- 节气查询

### 3. 拼音处理
- 汉字转拼音
- 拼音首字母提取
- 姓名拼音规范化

### 4. 中文格式化
- 数字转中文大写
- 金额格式化（财务场景）
- 中文日期格式化

### 5. 常用模板
- 请假条
- 工作汇报
- 会议纪要
- 通知公告

## 使用场景

### 日常办公
- 判断今天是否工作日
- 生成中文格式日期
- 转换金额为大写

### 文档处理
- 批量简繁转换
- 提取文档关键词
- 生成文本摘要

### 报表生成
- 格式化中文日期
- 金额大写转换
- 生成标准公文格式

## 示例用法

```bash
# 判断是否工作日
python3 scripts/workday_check.py "2026-03-16"

# 农历转换
python3 scripts/lunar_convert.py "2026-03-16"

# 金额大写
python3 scripts/number_to_chinese.py "12345.67"
```

## 依赖

- Python 3.6+
- zhdate (农历库)
- pypinyin (拼音库)
- opencc (简繁转换)

安装依赖:
```bash
pip install zhdate pypinyin opencc
```

## 配置

在 `TOOLS.md` 中添加:

```markdown
### Chinese Office
- Timezone: Asia/Shanghai
- Default Output: simplified_chinese
- Holiday Region: mainland
```

## 中国节假日数据

包含2010-2030年中国法定节假日及调休安排，自动更新。

---

**版本**: 1.0.0
**作者**: @lijie
**分类**: 办公自动化 / 中文特化
