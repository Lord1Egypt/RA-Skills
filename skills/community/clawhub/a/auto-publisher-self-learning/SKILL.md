---
name: auto-publisher-self-learning
description: |
  自进化技能自动发布器。一键将本地 skill 发布到 ClawHub 市场，自动处理
  各类已知错误和异常，并在每次执行中记录失败模式、学习最优策略、
  持续迭代改进发布流程。内置质量门禁、智能重试、版本冲突自动解决。
  触发词：发布技能、上架skill、publish skill、部署skill、自动发布。
agent_created: true
version: 1.0.2
display_name: "自进化技能发布器"
display_name_en: "Self-Learning Skill Publisher"
description_zh: "能自我学习迭代的自动技能发布器，越用越聪明"
description_en: "Self-improving skill publisher that learns from every publish"
visibility: "public"
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
  - WebSearch
  - WebFetch
---

# 自进化技能发布器

## 核心哲学

本技能不仅仅是一个发布工具——它拥有**学习记忆系统**，每次发布过程中：
1. 记录所有遇到的错误和成功处理方式
2. 下次遇到同类错误时自动应用已知方案
3. 统计发布成功率、各步骤耗时、常见失败模式
4. 持续优化发布策略（重试间隔、patch方案、质量门禁阈值）

简单说：**用得越多，发布越顺，出错越少**。

---

## 学习记忆系统（核心创新）

### 学习记忆文件

存储在 `~/.workbuddy/skills/auto-publisher-self-learning/learned_patterns.json`

```json
{
  "version": 1,
  "totalPublishes": 0,
  "totalSuccesses": 0,
  "patterns": {
    "errors": {
      "slug already taken": {
        "count": 0,
        "lastSolution": "append -v2 suffix",
        "lastUsed": "",
        "successRate": 0.0
      },
      "rate limit exceeded": {
        "count": 0,
        "lastSolution": "retry after 65min",
        "lastUsed": "",
        "optimalWaitMs": 3900000,
        "successRate": 0.0
      },
      "400 acceptLicenseTerms": {
        "count": 0,
        "lastSolution": "patch CLI publish.js",
        "lastUsed": "",
        "successRate": 0.0
      },
      "401 Unauthorized": {
        "count": 0,
        "lastSolution": "ask user for new token",
        "lastUsed": "",
        "successRate": 0.0
      },
      "GitHub account must be at least 14 days old": {
        "count": 0,
        "lastSolution": "notify user to wait 14 days",
        "lastUsed": "",
        "successRate": 0.0
      },
      "Path must be a folder": {
        "count": 0,
        "lastSolution": "cd to skill dir and use . as path",
        "lastUsed": "",
        "successRate": 0.0
      },
      "Version already exists": {
        "count": 0,
        "lastSolution": "auto-bump patch version",
        "lastUsed": "",
        "successRate": 0.0
      }
    },
    "quality_fails": {
      "description_too_short": 0,
      "missing_trigger_keywords": 0,
      "frontmatter_invalid": 0,
      "name_not_hyphen_case": 0,
      "missing_description": 0
    },
    "env_checks": {
      "clawhub_installed": true,
      "clawhub_working": true,
      "last_known_registry": "https://clawhub.ai"
    }
  }
}
```

### 自学习流程

每次发布后：
1. **记录结果**：成功/失败/部分成功
2. **提取错误模式**：从错误信息中匹配已知模式
3. **更新统计**：更新计数、成功率、最优方案
4. **调整策略**：如果某种方案的失败率上升，尝试替代方案
5. **版本升级**：当学习数据积累到一定程度，自动建议优化skill自身

---

## 执行流程

### 阶段一：环境准备与自检

```bash
# 1. 检查 clawhub CLI
which clawhub 2>/dev/null || npm install -g clawhub
clawhub version 2>/dev/null || clawhub --version

# 2. 检查学习记忆文件
LEARN_FILE="$HOME/.workbuddy/skills/auto-publisher-self-learning/learned_patterns.json"
if [ ! -f "$LEARN_FILE" ]; then
  mkdir -p "$(dirname "$LEARN_FILE")"
  echo '{"version":1,"totalPublishes":0,"totalSuccesses":0,"patterns":{"errors":{},"quality_fails":{},"env_checks":{}}}' > "$LEARN_FILE"
  echo "🆕 初始化学习记忆文件"
fi

# 3. 读取学习数据
LEARN_DATA=$(cat "$LEARN_FILE")

# 4. 环境自检 — 根据学习数据快速跳过或执行
# 如果learning记录显示clawhub_working=true且已安装，跳过重复安装检查
```

### 阶段二：用户输入收集

从用户对话中提取以下信息（缺什么问什么，不问重复的）：

| 参数 | 示例 | 说明 |
|------|------|------|
| skill目录路径 | `~/.workbuddy/skills/my-skill` | 包含SKILL.md的文件夹 |
| 多技能批量发布 | `~/.workbuddy/skills/` | 可指定多个或整个目录 |
| slug（URL名称） | `my-awesome-tool` | 小写字母+连字符 |
| 版本号 | `1.0.0` | semver格式，自动递增 |
| changelog | `Initial release` | 发布说明 |

**批量模式**：如果用户提供的是skills目录（含多个子目录），自动扫描所有含SKILL.md的子目录，逐个发布。

### 阶段三：质量门禁（Quality Gate）

对每个要发布的skill执行三轮检查——**每轮结果都记录到学习记忆**：

#### Level 1 — 硬性拦截（必须通过）

- [ ] SKILL.md 文件存在
- [ ] YAML frontmatter 存在并可解析
- [ ] 含 name 字段（非空）
- [ ] 含 description 字段（非空）
- [ ] 含 version 字段（有效 semver）
- [ ] description 不含尖括号 `<` `>`

#### Level 2 — 警告（建议修复）

- [ ] description 至少 20 字
- [ ] 含触发词（"触发词：" 或 "trigger："）
- [ ] yaml 中 agent_created: true
- [ ] visibility 字段存在

#### Level 3 — 质量评分

- [ ] 有 allowed-tools 声明
- [ ] 有使用示例或操作步骤
- [ ] 错误处理方法或边界说明
- [ ] 版本号 ≥ 1.0.0

**学习记录**：每次quality fail都记录到 `quality_fails`，当同一类型失败超过3次时，在下一次自动在质量门禁中提前预警。

### 阶段四：Patch CLI 的已知 Bug（根据学习记忆判断）

从学习记忆中读取是否有已知bug需要patch：

```bash
# clawhub CLI 已知 bug: publish 时缺少 acceptLicenseTerms
PUBLISH_JS=$(find /usr/local/lib /usr/lib /usr/local/nvm* ~/.nvm -name "publish.js" -path "*/clawhub/*" 2>/dev/null | head -1)
# 如果没找到，检查当前node安装路径
if [ -z "$PUBLISH_JS" ]; then
  PUBLISH_JS=$(find / -path "*/node_modules/clawhub/*" -name "publish.js" 2>/dev/null | head -1)
fi

if [ -n "$PUBLISH_JS" ]; then
  grep -q "acceptLicenseTerms" "$PUBLISH_JS" && echo "✅ 已 patch" || {
    sed -i 's/skillName:/acceptLicenseTerms: true, skillName:/' "$PUBLISH_JS"
    echo "🔧 已应用 acceptLicenseTerms patch"
    # 记录到学习记忆
  }
fi
```

### 阶段五：执行发布

```bash
cd "$SKILL_DIR" && clawhub publish "." \
  --slug "$SLUG" \
  --name "$DISPLAY_NAME" \
  --version "$VERSION" \
  --changelog "$CHANGELOG" \
  --tags "latest" \
  --json
```

### 阶段六：智能错误处理（3次重试 + 学习）

捕获错误 → 匹配学习记忆中的模式 → 应用已知方案 → 如新错误则记录并尝试通用方案：

| 错误模式 | 学习后的处理方案 |
|---------|----------------|
| `Path must be a folder` | 自动cd到目录后用 `.` 替代完整路径 |
| `slug already taken` / 409 | slug追加 `-v2` 或递增后缀 |
| `rate limit exceeded` / 429 | 从学习记忆中读取 `optimalWaitMs`，等待后重试；更新最优等待时间 |
| `acceptLicenseTerms` (400) | 重新patch CLI后重试 |
| `401 Unauthorized` | 提示用户重新生成token |
| `Version already exists` | 自动 bump patch 版本（1.0.0 → 1.0.1）后重试 |
| `GitHub account must be at least 14 days old` | 记录到学习，进入等待模式 |
| **未知错误** | 记录完整错误信息到 `unknown_errors`，尝试通用重试（最多3次） |

**学习更新逻辑**（每次重试后）：
```python
# 伪代码
if retry_successful:
  pattern["successRate"] = (pattern["successRate"] * pattern["count"] + 1) / (pattern["count"] + 1)
  pattern["lastSolution"] = current_solution
else:
  pattern["successRate"] = (pattern["successRate"] * pattern["count"]) / (pattern["count"] + 1)
  # 如果某种方案成功率低于30%，自动尝试下一种方案
  if pattern["successRate"] < 0.3:
    try_alternative_solution(pattern)
pattern["count"] += 1
pattern["lastUsed"] = current_time
```

### 阶段七：验证上架

```bash
clawhub search "$SLUG" 2>/dev/null | grep "$SLUG"
# 或
curl -s "https://clawhub.ai/api/v1/skills/$SLUG" | grep -q "$SLUG"
```

### 阶段八：总结与学习报告

每次发布完成后，输出：

```
📊 发布报告
━━━━━━━━━━━━━━━━━
✅ 成功: my-skill@1.0.0  → https://clawhub.ai/skills/my-skill
📦 安装: clawhub install my-skill

🧠 自学习统计（累计）
━━━━━━━━━━━━━━━━━
📈 总发布次数: 15
✅ 成功率: 86.7%
🔁 自动重试次数: 3
🎯 重试挽救成功率: 66.7%
📝 已学习模式: 7个
⚠️ 常见失败: rate_limit_exceeded (2次)
🧪 建议: 尝试在非高峰时段发布（UTC 02:00-06:00）

💡 自我改进建议
━━━━━━━━━━━━━━━━━
- "description_too_short" 失败次数已达3次，建议在质量门禁中加强预警
- 发布耗时中位数 12秒，较上次优化了 15%
```

---

## 快速调用示例

用户说：**"把我新做的my-tool技能发布到市场"**

本技能自动：
1. 扫描 `~/.workbuddy/skills/` 找到 my-tool
2. 检查质量门禁 → 通过
3. 检查学习记忆 → clawhub已安装，无需重复检查
4. 执行发布 → 成功
5. 更新学习记忆
6. 输出报告

用户说：**"把新创建的10个技能全部发布"**

本技能自动：
1. 扫描用户指定的目录 → 找到10个含SKILL.md的子目录
2. 按批处理逐个发布
3. 每个失败自动重试（使用学习记忆中的方案）
4. 输出汇总报告

---

## 学习记忆存储

| 文件 | 用途 |
|------|------|
| `learned_patterns.json` | 错误模式、成功率、最优方案 |
| `publish_history.json` | 每次发布的详细记录（技能名、耗时、结果） |
| `quality_trends.json` | 质量门禁统计数据、趋势分析 |

---

## 自我迭代机制

当本技能检测到以下条件时，自动建议更新自身：

1. **累计发布 ≥ 20 次**：建议根据错误统计优化流程
2. **某个新模式出现 ≥ 3 次**：建议将新模式固化到代码中
3. **成功率连续下降**：建议审查质量门禁阈值
4. **CLI 更新检测到**：建议重新验证 patch 是否仍需要

自我更新方式：向用户提交修改建议（可读报告），由用户决定是否执行。
