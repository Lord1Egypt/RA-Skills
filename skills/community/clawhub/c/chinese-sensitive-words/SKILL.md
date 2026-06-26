---
name: chinese-sensitive-words
description: "Chinese sensitive word detection and content compliance checker (中文敏感词/违禁词检测). Scan text for banned, restricted, and risky words across Xiaohongshu (小红书), Douyin (抖音), Kuaishou (快手), and Bilibili (B站). Covers advertising law violations (广告法极限词), medical claims (医疗功效词), political, violent, gambling, and fraud-related terms. Returns risk levels (high/medium/low), word categories, and safe replacement suggestions. 100K+ daily-updated word dictionary with homophone detection (谐音变体), character-jumping detection (跳字检测), phone number & URL detection, and NER filtering. Free 10 requests/month, unlimited with token. Perfect for checking marketing copy, product descriptions, live-streaming scripts (直播话术), social media posts, and ad compliance (内容审核/文案合规)."
metadata:
  openclaw:
    emoji: "🔍"
    requires:
      bins:
        - curl
        - jq
    primaryEnv: SENSITIVE_WORDS_TOKEN
---

# 中文敏感词检测工具

检测中文文本中的敏感词/违禁词，支持小红书、抖音、快手、B站等主流平台。

## 快速开始

```bash
cd scripts/

# 检测文案中的敏感词
./check.sh "这是全网最好用的美白产品，效果立竿见影"

# 查询某个词的安全替换建议
./suggestions.sh "美白"

# 查询全部替换建议库
./suggestions.sh
```

## 功能特点

- **海量词库** — 10万+词条，每日更新，覆盖政治、色情、暴力、赌博、毒品、广告法极限词、医疗功效词等
- **多平台支持** — 小红书、抖音、快手、B站专属词库
- **风险分级** — 🔴 高危（封号）/ 🟡 中危（限流）/ 🔵 低危（建议修改）/ 💡 提示
- **替换建议** — 不只检测，还推荐安全替代词
- **智能识别** — 谐音变体（薇信→微信）、跳字（加 微 信）、手机号/URL 检测
- **NER 过滤** — 智能过滤地名、人名、机构名，减少误报

## 命令参考

### check.sh — 检测敏感词

检测文本中的敏感词/违禁词，返回风险等级和替换建议。

```bash
# 基本用法
./check.sh "要检测的文案内容"

# 关闭 NER 过滤（更严格的检测）
./check.sh "要检测的文案内容" --no-ner

# 从文件读取
./check.sh --file input.txt
```

**参数说明：**
- 第一个参数：要检测的文本（最大 3000 字符）
- `--no-ner`：关闭 NER 智能过滤，检测更严格
- `--file <路径>`：从文件读取待检测文本

**输出示例：**
```
⚠️ 检测到 4 个敏感词

风险概览: 🔴 高危=1 | 🟡 中危=2 | 🔵 低危=1

🔴 高危（可能导致封号/删帖）
  - "13812345678" — 分类: 手机号

🟡 中危（可能导致限流/降权）
  - "最好用" — 分类: 广告法极限词 → 建议替换: 很好用, 超好用
  - "美白" — 分类: 医疗功效 → 建议替换: 提亮, 焕亮

🔵 低危（建议修改）
  - "加微信" — 分类: 引流 → 建议替换: 私信咨询
```

### suggestions.sh — 获取替换建议

查询敏感词的安全替换词。

```bash
# 查询指定词的替换建议
./suggestions.sh "美白"
./suggestions.sh "最好"

# 查询全部替换建议库（按分类展示）
./suggestions.sh
```

**输出示例：**
```
"美白" (医疗功效词替换)
建议替换: 提亮, 焕亮, 匀净, 透亮
```

## 配置

### 免费使用（每月 10 次）

无需任何配置，开箱即用。

### 无限使用（获取 Token）

前往 [GitHub Issues](https://github.com/CCCpan/chinese-sensitive-words/issues) 获取正式 Token。

获取后在 skill 目录下创建 `.env` 文件：

```bash
SENSITIVE_WORDS_TOKEN=your_token_here
```

或设置环境变量：

```bash
export SENSITIVE_WORDS_TOKEN=your_token_here
```

### 默认 API 服务

本工具默认使用以下 API 服务进行敏感词检测：

```
https://www.xdhdancer.top/api8888
```

该服务由本项目维护，仅用于敏感词检测，不会存储或分享您的文本内容。

### 自定义服务地址

如果使用私有部署的检测服务：

```bash
SENSITIVE_WORDS_API_BASE=https://your-server.com/api
SENSITIVE_WORDS_TOKEN=your_token_here
```

## 使用额度

| 类型 | 额度 | 说明 |
|------|------|------|
| 免费（无 Token） | 10 次/月 | 开箱即用，无需注册 |
| 注册用户（有 Token） | 无限制 | [获取 Token](https://github.com/CCCpan/chinese-sensitive-words/issues) |

## 支持的平台词库

| 平台 | 词库内容 |
|------|----------|
| **通用** | 政治、色情、暴力、赌博、毒品、违法 |
| **小红书** | 广告法极限词、医疗功效、虚假宣传、焦虑营销、品牌词 |
| **抖音** | 直播违禁词、引流词、夸大宣传 |
| **快手** | 社区规范违禁词 |
| **B站** | 社区规范、内容审核词 |

## 风险等级说明

| 等级 | 影响 | 示例 |
|------|------|------|
| 🔴 高危 | 封号/删帖 | 政治敏感、色情、暴力、手机号 |
| 🟡 中危 | 限流/降权 | 广告法极限词、医疗功效、虚假宣传 |
| 🔵 低危 | 建议修改 | 引流词、促销词 |
| 💡 提示 | 注意措辞 | 焦虑营销、容貌身材相关 |

## 故障排除

**"Rate limit exceeded" 错误：**
- 免费额度已用完（每月 10 次），明天会重置
- 或前往 GitHub Issues 获取 Token，享受无限使用

**"Connection timeout" 错误：**
- 检查网络连接
- 如果使用自定义服务地址，确认地址可访问

**检测结果不准确：**
- 尝试关闭 NER 过滤（`--no-ner`），获得更严格的检测结果
- NER 过滤默认开启，会自动排除地名、人名等误报

## 许可证

MIT
