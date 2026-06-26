---
name: douyin-sensitive-check
description: 抖音/短视频违禁词和敏感词检测（本地词库版，无需 API Key）。每天首次使用自动从 GitHub 开源词库更新本地缓存，离线检测文案合规性。支持多词库合并（广告极限词、平台限流词、暴恐、色情、涉枪涉爆等）。使用场景：(1) 生成短视频文案后自动检测违禁词，(2) 用户要求检查某段文字是否有问题，(3) 抖音/快手/B站内容合规审核，(4) 直播话术自查。触发词：违禁词、敏感词、检测、合规、抖音风控、限流词、能不能发。
metadata:
  openclaw:
    emoji: "🚨"
    requires:
      bins: ["python3"]
    platform: ["macos", "linux"]
    data: ["data/"]
    network:
      description: "每天首次使用时从 raw.githubusercontent.com 拉取开源词库更新（3 个公开仓库），无数据上传。网络失败时自动降级为本地缓存，不影响使用。"
      hosts: ["raw.githubusercontent.com"]
      trigger: "daily-first-use"
      optional: true
---

# 抖音违禁词检测 Skill（开源词库版）

本地词库 + 每日自动更新，无需 API Key，离线可用。

## 脚本路径

```
scripts/
  check.py         # 主检测脚本（入口）
  update_words.py  # 词库更新模块（每天首次自动触发）
data/              # 运行时生成，词库缓存目录（.gitignore 排除）
  sensitive_words.txt
  .update_state.json
```

## 常用命令

```bash
SKILL=~/.agents/skills/douyin-sensitive-check

# 检测一段文案
python3 $SKILL/scripts/check.py "今天给大家推荐史上最好用的护肤品，加我微信领优惠券"

# 检测文件
python3 $SKILL/scripts/check.py -f /path/to/script.txt

# 管道
echo "文案内容" | python3 $SKILL/scripts/check.py

# 强制更新词库
python3 $SKILL/scripts/check.py --update

# 查看词库状态
python3 $SKILL/scripts/check.py --status
```

## 工作流

1. **每天首次运行** → 自动调用 `update_words.py` 从 3 个 GitHub 开源词库拉取最新内容合并
2. 加载本地 `data/sensitive_words.txt`（去重合并，含数万词条）
3. 对输入文案做全文子串匹配（长词优先）
4. 输出：🔴 违禁词（必改）/ 🟡 广告极限词（建议改）+ 上下文标注
5. 根据结果帮用户改写文案，改完后再次检测直到通过

## 词库来源

- `konsheng/Sensitive-lexicon`：广告、政治、暴恐、色情、涉枪涉爆、补充词库
- `bigdata-labs/sensitive-stop-words`：广告、政治、色情、涉枪涉爆
- `jkiss/sensitive-words`：广告、政治、色情

## 更新机制

- `data/.update_state.json` 记录最后更新日期
- 每天第一次使用自动触发，当天内后续使用直接读缓存
- 网络失败时保留本地缓存，不影响使用
- 手动强制更新：`--update`

## 重要提示

- 开源词库以通用违禁词为主，抖音平台的部分特有限流词（如"私信"、"加微信"）已内置在 `check.py` 的 `CATEGORY_PATTERNS` 中补充
- 匹配策略是子串匹配，可能有误报；如需精确匹配可编辑 `data/sensitive_words.txt` 删除误报词
- 改写建议：被标注词优先用谐音、符号分割、同义替换等方式规避
