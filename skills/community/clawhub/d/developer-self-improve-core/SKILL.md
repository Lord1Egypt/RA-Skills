---
name: developer-self-improve-core
description: |
  开发者自改进核心技能 - 自动错误防重、自检、规则生成、记忆清洗、定时提醒
  
  核心功能：
  - 每轮回答前：自动错误防重
  - 每轮回答后：自动自检 + 生成规则草案
  - 累计 10 轮对话/每周：自动记忆清洗扫描
  - 自动提醒：每天 9:30 钉钉推送待确认规则
  
  核心原则：
  - AI 只提议，人类终审
  - 绝不自动写入/修改/删除长期记忆
  - 用户指令 > 长期规则 > AI 临时草案
metadata: 
  emoji: "🛡️"
  version: "1.1.9"
  author: "lijiujiu"
  license: "MIT"
  requires:
    bins: ["bash", "find", "grep", "awk", "md5sum", "stat", "sed"]
    optional: ["openclaw"]
    env: ["AUTO_MEMORY_WORKSPACE"]
    config: ["workspace/config/current_user.json"]
  tags: ["developer", "memory", "safe", "automation", "reminder", "dingtalk", "app-development", "开发人员", "APP 开发", "IT", "软件开发", "移动开发"]
---

# 🛡️ developer-self-improve-core

**开发者自改进核心技能**

---

## 🚀 快速开始

### 1. 安装技能

```bash
clawhub install developer-self-improve-core
```

### 2. 初始测试（推荐）

**首次安装后，建议先禁用自动化功能进行测试：**

```bash
vi config/config.yaml
```

确认以下配置（默认已禁用）：
```yaml
enable_reminder: false      # 默认：false（测试时禁用）
enable_auto_cleanup: false  # 默认：false（测试时禁用）
```

**测试命令：**
```bash
./scripts/developer-self-improve-core.sh init
./scripts/developer-self-improve-core.sh pre-check "测试场景"
./scripts/developer-self-improve-core.sh post-check "测试内容" "测试"
```

### 3. 启用定时提醒（可选）

**测试确认无误后，可以启用定时提醒：**

1. **配置钉钉账号：**
   ```bash
   vi config/config.yaml
   ```
   ```yaml
   dingtalk_target: "您的钉钉账号 ID"  # 替换为 18 位钉钉账号 ID
   enable_reminder: true               # 启用提醒
   ```

2. **配置 crontab：**
   ```bash
   crontab -e
   # 添加以下行（每天 9:30 执行）：
   30 9 * * * cd ~/.openclaw/workspace/skills/developer-self-improve-core && ./scripts/daily-check.sh
   ```

### 4. 使用技能

技能会自动在 AI 回答前后执行：
- ✅ 回答前：错误防重
- ✅ 回答后：自检 + 规则生成

---

## ⚡ 触发时机

| 时机 | 执行内容 | 频率 |
|------|----------|------|
| **每轮回答前** | 自动错误防重 | 每次响应前 |
| **每轮回答后** | 自动自检 + 生成规则草案 | 每次响应后 |
| **定期清洗** | 自动记忆清洗扫描 | 累计 10 轮对话或每周 |

---

## 🔄 一体化执行逻辑

### 1. 回答前（错误防重）

```
1. 加载当前场景对应的人工确认长期规则
   ↓
2. 命中已知错误类型则自动修正
   ↓
3. 仅使用人工确认规则，绝不使用未确认草案
   ↓
4. 内部标记：已规避同类错误
```

**示例：**
```
场景：代码推送
命中规则：【auto_push_001】永远使用 push_to_target.sh 脚本推送
行动：自动修正为使用脚本，标记"已规避同类错误"
```

---

### 2. 回答后（自检 + 反思 + 提案）

```
1. 静默自检：
   - 是否冲突长期规则
   - 是否重复犯错
   - 是否存在硬错误
   ↓
2. 仅在满足可信依据时生成规则草案：
   ✔ 用户明确规范/错误
   ✔ 可复现模式≥2 次
   ✔ 可验证逻辑/格式/事实错误
   ✔ 与历史规则冲突
   ↓
3. 禁止主观推断、特例泛化、幻觉规则
   ↓
4. 按固定格式生成草案，自动去重，不自动入库
   ↓
5. 主动询问用户：
   "我发现一个可沉淀的规则，是否加入长期记忆？【同意/修改/忽略】"
   ↓
6. 忽略的草案不再重复提示
```

**可信依据验证：**
| 依据类型 | 可信度 | 示例 |
|----------|--------|------|
| 用户明确要求≥2 次 | 高 | "记住，永远用脚本推送"（第 2 次提及） |
| 可复现模式≥2 次 | 中 | 域名切换问题出现 2 次 |
| 单次可验证硬错误 | 低 | 明显的逻辑/格式错误 |

---

### 3. 定期清洗（合并/去重/淘汰）

```
1. 自动扫描长期规则库：
   - 重复规则
   - 冲突规则
   - 低频规则（30 天未使用）
   - 被高阶规则覆盖的规则
   ↓
2. 生成清洗清单并询问：
   "以下规则建议合并/删除，是否执行？"
   ↓
3. 仅在用户批准后执行
   ↓
4. 保留操作日志，支持回滚
```

---

## 📝 强制格式约束

### 规则草案统一格式

```markdown
### 【规则 ID】auto_xxxx
（基于场景哈希/内容指纹生成，自动去重）

### 【场景】xxx
（明确描述适用场景，≤20 字）

### 【问题/模式】xxx
（明确描述发现的问题或可复现模式，≤20 字）

### 【建议规则】xxx
（极简一句话，不冗余、可直接执行）

### 【依据】xxx
（用户明确指出/重复模式/可验证错误）

### 【可信度】高/中/低
（严格绑定依据，不可随意标注）

### 【建议层级】长期/中期
```

---

### 可信度绑定规则

| 可信度 | 判定标准 |
|--------|----------|
| **高** | 用户明确要求≥2 次 |
| **中** | 可复现模式≥2 次 |
| **低** | 单次可验证硬错误 |

---

## ⚙️ 安全铁律（不可突破）

| 铁律 | 说明 |
|------|------|
| **AI 只提议，人类终审** | AI 可生成草案，但绝不自动入库 |
| **绝不自动写入/修改/删除长期记忆** | 所有记忆修改需用户批准 |
| **优先级排序** | 用户指令 > 长期规则 > AI 临时草案 |
| **记忆可追溯** | 所有记忆可追溯、可关闭、可回滚 |
| **规则冲突裁决** | 最新确认规则优先于旧规则 |
| **Token 优化** | 长期规则保持极简，仅一句话条目 |

---

## 📊 记忆结构

```
memory/
├── short_term/         短期记忆（对话结束自动销毁）
├── proposals/          临时提案区（按日期合并，保留 7 天）
│   ├── 2026-04-09.md   # 当天所有规则
│   └── 2026-04-08.md
├── rules/              长期规则库（仅人工确认）
│   └── confirmed_rules.md
├── cleanup/            待清洗区（需用户批准）
│   └── cleanup_20260409.md
└── logs/               操作日志（支持回滚）
    └── operations.log
```

---

## 🚀 使用示例

### 示例 1: 用户明确指出错误

**对话：**
```
用户：推送应该用 push_to_target.sh 脚本，不要手动 rsync
AI: 好的，已记录
```

**AI 生成草案：**
```markdown
### 【规则 ID】auto_push_script_001
### 【场景】代码推送
### 【问题/模式】手动 rsync 推送产生重复文件
### 【建议规则】永远使用 push_to_target.sh 脚本推送
### 【依据】用户明确指出
### 【可信度】高
### 【建议层级】长期
```

**AI 提案：**
```
我发现一个可沉淀的规则，是否加入长期记忆？

【规则 ID】auto_push_script_001
【场景】代码推送
【建议规则】永远使用 push_to_target.sh 脚本推送

【同意/修改/忽略】
```

---

### 示例 2: 重复模式检测

**对话：**
```
用户：（第 1 次）域名切换后请求还是旧域名
AI: 已修复，添加了内存缓存

用户：（第 2 次）域名切换后请求还是旧域名
AI: 已修复，verifiedDomain 没有同步更新
```

**AI 生成草案：**
```markdown
### 【规则 ID】auto_domain_cache_001
### 【场景】域名切换
### 【问题/模式】域名切换后 verifiedDomain 未同步更新
### 【建议规则】域名切换时必须同步更新 verifiedDomain 和 verifiedDomainCache
### 【依据】重复模式≥2 次
### 【可信度】中
### 【建议层级】长期
```

---

### 示例 3: 定期清洗

**AI 提案：**
```
累计 10 轮对话，触发记忆清洗扫描。

发现以下规则建议合并/删除，是否执行？

## 待合并规则

1. 【auto_push_001】永远使用 push_to_target.sh 脚本推送
2. 【auto_push_002】推送前检查配置文件
   ↓ 建议合并为
   【auto_push_001】推送相关规范（包含脚本使用和配置检查）

## 待删除规则

1. 【auto_old_rule_002】过时的规则（已 30 天未使用）
   ↓ 建议删除

【同意/修改/忽略】
```

---

## 🔧 脚本命令

### 初始化

```bash
./scripts/developer-self-improve-core.sh init
```

### 回答前检查（错误防重）

```bash
./scripts/developer-self-improve-core.sh pre-check "当前场景"
```

### 回答后检查（自检 + 提案）

```bash
./scripts/developer-self-improve-core.sh post-check "对话内容"
```

### 定期清洗

```bash
./scripts/developer-self-improve-core.sh cleanup
```

### 确认规则

```bash
./scripts/developer-self-improve-core.sh confirm [规则 ID] [同意/修改/忽略]
```

---

## 📖 更多文档

详见技能目录中的文档文件。

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

**作者：** lijiujiu  
**许可证：** MIT

---

## 📄 许可证

MIT License
