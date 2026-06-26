# douyin-sensitive-check

> 抖音/短视频违禁词检测 OpenClaw Skill — 开源词库版，无需 API Key

## 功能

- 🔴 **违禁词检测**：涵盖政治、暴恐、色情、涉枪涉爆等（3,000+ 词）
- 🟠 **平台限流词**：抖音已知限流词，如"推广"、"加微信"、"优惠券"等
- 🟡 **广告极限词**：广告法违禁极限词，如"最好"、"第一"、"史上最"等
- 🟡 **医疗违禁词**：如"包治"、"根治"、"无副作用"等
- 📍 **上下文标注**：精确定位词在文案中的位置
- 🔄 **每日自动更新**：每天首次使用自动从 GitHub 拉取最新词库

## 词库来源（开源）

- [konsheng/Sensitive-lexicon](https://github.com/konsheng/Sensitive-lexicon) — MIT License
- [bigdata-labs/sensitive-stop-words](https://github.com/bigdata-labs/sensitive-stop-words)
- [jkiss/sensitive-words](https://github.com/jkiss/sensitive-words)

## 安装

```bash
# 克隆到 OpenClaw skills 目录
git clone https://github.com/YOUR_USERNAME/douyin-sensitive-check ~/.agents/skills/douyin-sensitive-check
```

## 使用

安装后直接在 OpenClaw 对话中说：

> "帮我检测这段文案有没有违禁词：今天给大家推广一款产品..."

### 命令行直接使用

```bash
SKILL=~/.agents/skills/douyin-sensitive-check

# 检测文案
python3 $SKILL/scripts/check.py "你的文案内容"

# 检测文件
python3 $SKILL/scripts/check.py -f script.txt

# 强制更新词库
python3 $SKILL/scripts/check.py --update

# 查看词库状态
python3 $SKILL/scripts/check.py --status
```

## 示例输出

```
🚨 发现 3 个风险词，建议修改后再发布

🟠 平台限流词（建议替换，影响流量）:
   ▸ 推广
     上下文: 今天给大家【推广】一款产品…

🟡 广告极限词（广告法风险）:
   ▸ 史上最
     上下文: …【史上最】好用！

── 标注后文案 ──
今天给大家【推广】一款产品，【史上最】好用！

📊 检测字数: 20 字 | 风险词: 3 个
```

## 隐私与网络说明

本 skill 仅在以下情况发起网络请求：

- 每天**首次使用时**自动从 `raw.githubusercontent.com` 拉取词库更新（3 个公开仓库）
- 请求目标均为公开 GitHub 仓库的原始文本文件，**无任何数据上传**
- 网络失败时自动降级为本地缓存，不影响正常使用
- 如需**完全离线使用**，可手动维护 `data/sensitive_words.txt`，将 `data/.update_state.json` 中 `last_update` 设为未来日期即可禁用自动更新

```json
// data/.update_state.json — 设置此值可禁用自动更新
{ "last_update": "2099-12-31", "word_count": 12345 }
```

## License

MIT
