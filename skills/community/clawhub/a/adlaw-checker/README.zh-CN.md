# 广告法违禁词检测器 (AdLaw Checker)

> 检查文案中的广告法违规词汇，避免法律风险

---

## 📦 安装

```bash
# 安装依赖
pip install jieba pandas

# 复制技能文件夹到 workspace/skills/adlaw-checker/
```

---

## 🚀 使用方法

### 方法 1: 命令行

```bash
# 检查单条文案
python scripts/checker.py check --text "这是最好的产品"

# 检查文件
python scripts/checker.py check --file "copywriting.txt"

# 指定平台 (小红书/微信/抖音)
python scripts/checker.py check --text "xxx" --platform xiaohongshu

# 生成报告
python scripts/checker.py check --text "xxx" --report "report.json"
```

### 方法 2: Python 代码

```python
from scripts.checker import AdLawChecker

checker = AdLawChecker()

# 检查文案
result = checker.check("这是最好的产品，销量第一")
print(f"违禁词：{result['violations']}")
print(f"风险等级：{result['risk_level']}")
print(f"合规分数：{result['compliance_score']}")

# 批量检查
texts = ["文案 1", "文案 2", "文案 3"]
results = checker.batch_check(texts)
```

### 方法 3: Agent 调用

```
@legal 检查这篇文案的广告法合规性

文案内容:
"这是市面上最好的 AI 工具，效率提升 300%，
第一品牌，用户都说顶级体验！"

输出：违禁词列表 + 修改建议
```

---

## 📊 违禁词分类

### 高风险 (绝对化用语)

| 违禁词 | 替换建议 |
|--------|----------|
| 最好 | 优秀/出色 |
| 第一 | 领先/前列 |
| 顶级 | 高端/优质 |
| 唯一 | 独特/特别 |
| 100% | 几乎/大部分 |
| 永久 | 长期/持久 |

### 中风险 (夸大用语)

| 违禁词 | 替换建议 |
|--------|----------|
| 领先 | 较为先进 |
| 极致 | 出色 |
| 完美 | 很好 |
| 颠覆性 | 创新 |

### 低风险 (推荐用语)

| 违禁词 | 替换建议 |
|--------|----------|
| 推荐 | 分享 |
| 必买 | 值得入手 |
| 种草 | 推荐 |
| 爆款 | 热门 |

---

## 📝 输出示例

```json
{
  "text": "这是最好的产品",
  "violations": [
    {
      "word": "最好",
      "position": 2,
      "risk_level": "high",
      "category": "绝对化用语",
      "suggestion": "建议替换为'优秀'"
    }
  ],
  "risk_level": "high",
  "compliance_score": 85,
  "suggestions": [
    "将'最好'替换为'优秀'"
  ],
  "compliant_version": "这是优秀的产品"
}
```

---

## ⚙️ 高级功能

### 平台特定检查

```python
# 小红书
checker.check("文案", platform="xiaohongshu")

# 微信公众号
checker.check("文案", platform="wechat")

# 抖音
checker.check("文案", platform="douyin")
```

### 行业特定检查

```python
# 美妆行业
checker.set_industry("cosmetics")

# 食品行业
checker.set_industry("food")

# 教育行业
checker.set_industry("education")
```

### 自定义词库

```python
# 添加违禁词
checker.add_violation_words(["自定义词"], "high")

# 添加替换建议
checker.add_suggestion("最好", "很不错")
```

---

## ⚠️ 注意事项

1. **仅供参考** - 不能替代法律意见
2. **定期更新** - 词库需定期维护
3. **人工复核** - 重要文案建议人工审核

---

## 📚 相关资源

- [SKILL.md](./SKILL.md) - 技能文档
- [广告法全文](http://www.gov.cn/gongbao/content/2015/content_2893774.htm)

---

*合规创作，远离风险。* ⚖️✅
