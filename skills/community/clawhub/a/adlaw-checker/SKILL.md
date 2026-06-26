# AdLaw Checker Skill

**Slug:** `adlaw-checker`  
**Version:** 1.0.0  
**Author:** 咪咪  
**Description:** 广告法违禁词检测 - 检查文案中的广告法违规词汇，避免法律风险

---

## 🎯 功能概述

本技能提供广告法合规检查能力，支持：
- 违禁词检测 (最、第一、顶级等)
- 虚假宣传识别
- 平台规则检查 (小红书、抖音、微信公众号)
- 修改建议生成

---

## 📦 安装

### 前置条件

```bash
# Python 3.8+
python --version

# 安装依赖
pip install jieba pandas
```

### 安装技能

```bash
# 手动安装
# 复制此技能文件夹到 workspace/skills/adlaw-checker/
```

---

## 🛠️ 使用方法

### 方法 1: 直接调用

```
@legal 检查这篇文案的广告法合规性

文案内容:
"这是市面上最好的 AI 工具，效率提升 300%，
第一品牌，用户都说顶级体验！"

输出：违禁词列表 + 修改建议
```

### 方法 2: Python 脚本

```python
from adlaw_checker import AdLawChecker

checker = AdLawChecker()

# 检查文案
result = checker.check("这是最好的产品，销量第一")
print(f"违禁词：{result['violations']}")
print(f"风险等级：{result['risk_level']}")
print(f"修改建议：{result['suggestions']}")

# 批量检查
texts = ["文案 1", "文案 2", "文案 3"]
results = checker.batch_check(texts)
```

### 方法 3: 命令行

```bash
# 检查单条文案
python -m adlaw_checker check --text "这是最好的产品"

# 检查文件
python -m adlaw_checker check --file "copywriting.txt"

# 生成报告
python -m adlaw_checker check --text "xxx" --report "report.json"
```

---

## 📊 违禁词分类

### 绝对化用语 (高风险)

| 违禁词 | 替换建议 |
|--------|----------|
| 最好 | 优秀、出色、良好 |
| 第一 | 领先、前列、知名 |
| 顶级 | 高端、优质、专业 |
| 唯一 | 独特、特别 |
| 绝对 | 非常、相当、很 |
| 100% | 几乎、大部分 |
| 永久 | 长期、持久 |
| 万能 | 多功能、多种用途 |

### 虚假宣传 (高风险)

| 违禁词 | 替换建议 |
|--------|----------|
| 根治 | 改善、缓解 |
| 无效退款 | 售后保障 |
| 一天见效 | 持续使用可见效果 |
| 零风险 | 低风险 |
| 稳赚不赔 | 投资有风险 |

### 平台特定规则

#### 小红书

| 违禁词 | 替换建议 |
|--------|----------|
| 种草 | 推荐、分享 |
| 必买 | 值得入手 |
| 断货王 | 热门、受欢迎 |
| 全网最低 | 优惠、划算 |

#### 微信公众号

| 违禁词 | 替换建议 |
|--------|----------|
| 点击领取 | 了解详情 |
| 立即抢购 | 了解产品 |
| 限时秒杀 | 优惠活动 |

---

## ⚙️ 配置选项

### 配置文件：`config.json`

```json
{
  "risk_levels": {
    "high": ["最", "第一", "顶级", "唯一"],
    "medium": ["领先", "优秀", "专业"],
    "low": ["推荐", "值得"]
  },
  "platform_rules": {
    "xiaohongshu": true,
    "wechat": true,
    "douyin": true
  },
  "auto_suggest": true,
  "output_format": "json"
}
```

---

## 📝 示例工作流

### 检查小红书笔记

```
@legal 检查这篇小红书笔记的广告法合规性

笔记标题："这款 AI 工具是最好的效率神器！"
笔记正文："使用一天就见效，效率提升 300%，
全网第一，用户都说顶级体验！"

检查项目:
- 广告法违禁词
- 小红书平台规则
- 虚假宣传风险

输出：
1. 违禁词列表
2. 风险等级评估
3. 修改建议
4. 合规版本
```

### 批量检查文案

```
@legal 批量检查以下文案的合规性

文案列表:
1. "最好用的 AI 工具"
2. "销量第一的效率神器"
3. "顶级团队打造"
4. "100% 好评"

输出：批量检查报告
```

---

## 📊 输出数据格式

### 单次检查结果

```json
{
  "text": "这是最好的产品",
  "violations": [
    {
      "word": "最好",
      "position": 2,
      "risk_level": "high",
      "category": "绝对化用语",
      "suggestion": "建议替换为'优秀'或'出色'"
    }
  ],
  "risk_level": "high",
  "compliance_score": 60,
  "suggestions": [
    "将'最好'替换为'优秀'",
    "避免使用绝对化用语"
  ],
  "compliant_version": "这是优秀的产品"
}
```

### 批量检查报告

```json
{
  "total_texts": 10,
  "violations_found": 15,
  "high_risk": 5,
  "medium_risk": 7,
  "low_risk": 3,
  "average_compliance_score": 72,
  "details": [...]
}
```

---

## 🔧 高级功能

### 1. 自定义词库

```python
checker = AdLawChecker()

# 添加自定义违禁词
checker.add_violation_words(["自家产品", "内部推荐"])

# 添加自定义替换建议
checker.add_suggestion("最好", "很不错")

# 保存自定义词库
checker.save_custom_dict("custom_dict.json")
```

### 2. 行业特定检查

```python
# 美妆行业
checker.set_industry("cosmetics")
result = checker.check("本产品美白效果最好")

# 食品行业
checker.set_industry("food")
result = checker.check("100% 纯天然")

# 教育行业
checker.set_industry("education")
result = checker.check("保过班，无效退款")
```

### 3. 实时监测

```python
# 监测文案变更
checker.monitor("copywriting.txt", callback=lambda r: print(r))
```

---

## 📚 违禁词库

### 完整列表 (部分)

```
绝对化用语:
最、第一、顶级、唯一、绝对、100%、永久、万能、
根治、彻底、完全、100% 有效、零风险、史无前例

虚假宣传:
一天见效、三天瘦十斤、永不反弹、稳赚不赔、
无效退款、包治百病、延年益寿

平台特定:
种草、必买、断货王、全网最低、点击领取、
立即抢购、限时秒杀
```

---

## 🐛 故障排查

### 问题 1: 检测不准确

```
可能原因:
- 词库未更新
- 上下文理解不足

解决方案:
1. 更新违禁词库
2. 人工复核结果
3. 添加自定义规则
```

### 问题 2: 误报率高

```
可能原因:
- 词库过于严格
- 缺少上下文

解决方案:
1. 调整风险等级
2. 添加白名单词汇
3. 结合人工审核
```

---

## ⚠️ 注意事项

1. **仅供参考** - 本工具不能替代法律意见
2. **定期更新** - 广告法规会更新，词库需定期维护
3. **人工复核** - 重要文案建议人工 + 工具双重检查
4. **平台差异** - 不同平台规则可能不同

---

## 📚 相关资源

- [中华人民共和国广告法](http://www.gov.cn/gongbao/content/2015/content_2893774.htm)
- [小红书社区规范](https://www.xiaohongshu.com/community_guidelines)
- [微信公众号运营规范](https://mp.weixin.qq.com/cgi-bin/announce?action=getannouncement)

---

## ⚠️ 免责声明

> 本工具提供的检查结果仅供参考，不构成法律意见。重要商业文案建议咨询专业律师。因使用本工具导致的法律风险，由使用者自行承担。

---

*合规创作，远离风险。* ⚖️✅
