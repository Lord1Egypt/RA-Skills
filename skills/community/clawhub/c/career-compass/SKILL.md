---
name: career-compass
description: 职场罗盘 by Barry — 一站式求职辅助 Skill。整合简历解析优化、公司调研（就业向）、同城职位搜索、模拟面试四大模块。输入个人信息/简历，自动生成简历优化方向、公司调研报告、招聘表单，并可进行模拟面试。
author: Barry
version: "1.0.0"
tags:
  - career
  - job-search
  - resume
  - interview
  - mock-interview
  - boss-cli
  - pdf
  - company-analysis
  - employment
  - 求职
  - 简历
  - 面试
install:
  kind: script
  script: |
    # career-compass 依赖安装脚本（Barry 版本）
    # 说明：
    # 1. ClawHub 发布时未携带 INSTALL.bat / INSTALL.sh
    # 2. 也未上传 uv.lock，本安装脚本不会依赖仓库内 lock 文件
    # 3. 运行时如果系统已安装 uv / pipx 会优先使用，否则自动回退到 pip

    echo "============================================"
    echo "  Career Compass 依赖安装 (by Barry)"
    echo "============================================"

    install_boss_cli() {
        echo "▶ 安装 boss-cli..."

        if command -v boss >/dev/null 2>&1; then
            echo "  [OK] boss-cli 已安装"
            return 0
        fi

        if command -v uv >/dev/null 2>&1; then
            echo "  [INFO] 检测到 uv，优先使用 uv tool install"
            uv tool install kabi-boss-cli >/dev/null 2>&1 && {
                echo "  [OK] boss-cli 已安装 (uv)"
                return 0
            }
            echo "  [WARN] uv 安装失败，准备继续尝试 pipx / pip"
        fi

        if command -v pipx >/dev/null 2>&1; then
            echo "  [INFO] 检测到 pipx，尝试使用 pipx 安装"
            pipx install kabi-boss-cli >/dev/null 2>&1 && {
                echo "  [OK] boss-cli 已安装 (pipx)"
                return 0
            }
            echo "  [WARN] pipx 安装失败，准备继续尝试 pip"
        fi

        if command -v pip >/dev/null 2>&1; then
            echo "  [INFO] 尝试使用 pip --user 安装"
            pip install kabi-boss-cli --user >/dev/null 2>&1 && {
                echo "  [OK] boss-cli 已安装 (pip)"
                return 0
            }
        elif command -v python >/dev/null 2>&1; then
            echo "  [INFO] 尝试使用 python -m pip --user 安装"
            python -m pip install kabi-boss-cli --user >/dev/null 2>&1 && {
                echo "  [OK] boss-cli 已安装 (python -m pip)"
                return 0
            }
        elif command -v python3 >/dev/null 2>&1; then
            echo "  [INFO] 尝试使用 python3 -m pip --user 安装"
            python3 -m pip install kabi-boss-cli --user >/dev/null 2>&1 && {
                echo "  [OK] boss-cli 已安装 (python3 -m pip)"
                return 0
            }
        fi

        echo "  [WARN] boss-cli 自动安装失败，请手动运行："
        echo "         pip install kabi-boss-cli --user"
        return 1
    }

    echo ""
    install_boss_cli

    # Step 2: 安装 PDF 工具链（用于简历解析）
    echo ""
    echo "▶ 检查 PDF 工具链..."
    MISSING=""
    for tool in pdftotext tesseract ghostscript; do
        if command -v $tool &>/dev/null; then
            echo "  [OK] $tool 已安装"
        else
            echo "  [MISSING] $tool 未安装"
            MISSING=1
        fi
    done

    if [ -n "$MISSING" ]; then
        echo ""
        echo "  PDF 工具链未完整安装（用于解析简历 PDF）。"
        echo "  macOS 安装:  brew install poppler tesseract ghostscript"
        echo "  Ubuntu:     sudo apt install poppler-utils tesseract-ocr ghostscript"
        echo "  Windows:    https://github.com/oschwartz10612/poppler-windows/releases"
        echo ""
        echo "  [INFO] 不安装 PDF 工具链也可以使用：直接复制简历内容粘贴给 AI 即可"
    fi

    echo ""
    echo "============================================"
    echo "  安装检查完成！"
    echo "============================================"
    echo ""
    echo "  在 AI 对话中说以下任意一句即可激活："
    echo ""
    echo "  '帮我全面准备面试'"
    echo "  '我要去XX公司面试，帮我模拟一下'"
    echo "  '帮我看看简历有哪些可以优化的地方'"
    echo "  '分析一下这家公司'"
    echo "  '帮我搜索同城类似职位'"
    echo ""
---

# 🎯 Career Compass — 职场罗盘
**by Barry** | 一站式求职辅助

---

## 🧭 整体架构

本 Skill 由 4 个子模块组成，完整覆盖求职全流程：

| 模块 | 类型 | 触发关键词 |
|------|------|-----------|
| **简历收集 & 优化** | Prompt 逻辑 | 简历、优化、改简历、简历诊断、项目经历、关键词对齐、自我介绍 |
| **公司调研** | Prompt + 搜索 | 调研、分析公司、公司怎么样、值不值得去、靠谱吗、避雷、加班、薪资、团队风格 |
| **职位搜索** | boss-cli | 搜索职位、找工作、看看机会、同城机会、岗位推荐、有没有在招、薪资范围 |
| **模拟面试** | Prompt + 搜索 | 面试、模拟、准备面试、过一遍、拷打我、压力面、反问、复盘 |

---

## 🚀 完整使用流程

```
用户首次激活
    ↓
Step 1：收集简历 + 目标公司 + JD
    ↓
Step 2：简历优化建议
    ↓
Step 3：目标公司调研（就业视角）
    ↓
Step 4：同城职位搜索
    ↓
Step 5：模拟面试（可选）
    ↓
Step 6：复盘评分卡
```

---

## Step 1 — 首次激活：收集基本信息

> 💡 **触发时机**：用户第一次表达求职意图时执行。信息可以分多次收集，不强制一次性完成。
>
> **宽松触发原则：** 只要用户表达出与求职、跳槽、面试、简历、公司判断、岗位机会、薪资比较、offer 选择、面试复盘等任一相关意图，即可激活本 Skill；不要求必须出现“简历”“面试”“调研”这类精确词。
>
> **可直接激活的模糊表达示例：**
> - 我最近想换工作
> - 帮我看看这份工作值不值得去
> - 我有个面试，不知道怎么准备
> - 你帮我看看我现在找什么岗位合适
> - 这家公司靠谱不靠谱
> - 我想冲一下面试
> - 这个 offer 要不要接
> - 帮我梳理一下求职方向

**必须收集（首次）：**
1. 简历（PDF 文件路径 或 粘贴文本）
2. 目标公司名称
3. 目标岗位或 JD

**可以后续收集（对话中逐步补充）：**
- 个人能力/证书
- 职场经验
- 就业标准（薪资/上班时间/公司规模等）
- 目标城市

---

### 1.1 收集简历

**优先方式 A（粘贴文本）：**
> 请把你的简历内容直接粘贴给我，你可以对姓名、公司名进行脱敏处理（如"张三"→"张先生"，公司名可模糊）。

**方式 B（PDF 路径）：**
用户给出 PDF 路径后，使用以下方式解析：

```bash
pdftotext /path/to/resume.pdf - 2>/dev/null || \
tesseract /path/to/resume.pdf stdout 2>/dev/null
```

如果 PDF 工具链不可用：
> 当前环境不支持 PDF 解析，请直接把简历中的关键信息粘贴给我：
> - 最近 1-2 段工作经历（公司名可脱敏）
> - 核心技术栈 / 技能
> - 教育背景

---

### 1.2 收集目标公司和 JD

**触发公司调研时：**
> 请告诉我你要去的公司名称，以及招聘要求（JD）内容（如果有的话）。
> 公司名我可以只填简称，如不确定公司全名也可以描述行业/产品。

**JD 格式说明：**
可以是截图、粘贴文字、或简单描述岗位要求。

---

### 1.3 收集就业标准（可后续补充）

| 维度 | 问题 |
|------|------|
| 薪资 | 你的期望薪资范围是多少？最低接受多少？ |
| 上班时间 | 对双休、弹性时间有要求吗？ |
| 公司规模 | 偏好大厂/中型/小公司？ |
| 融资阶段 | 在意公司融资阶段吗（如已上市/D轮）？ |
| 地点 | 目标城市/区域？ |
| 其他 | 有哪些硬性要求（外企、不加班等）？ |

---

## Step 2 — 简历优化建议

基于简历内容，给出：

### 2.1 结构诊断
检查：基本信息、技能清单、教育背景、工作经历、项目经历是否完整

### 2.2 关键词对齐
对标目标 JD，提取高频技能词，在简历中优先呈现

### 2.3 成就量化
将"负责/参与XXX"改为"主导XXX，效率提升X%/带来X万收益"

### 2.4 项目描述（STAR法则）
Situation（背景）→ Task（任务）→ Action（行动）→ Result（结果）

### 2.5 自检清单
- [ ] JD 关键词覆盖率 ≥ 60%
- [ ] 每段经历有量化数据
- [ ] 无错别字/格式混乱
- [ ] 联系方式最新

---

## Step 3 — 公司调研（就业视角）

> 📌 **依赖**：`web_search` / `web_fetch`（平台内置）进行公开信息搜索

### 3.1 触发场景（扩充）

以下任一表达均触发公司调研；允许模糊表达、情绪化表达、求建议式表达，不要求用户准确提供“调研”二字：

| 中文触发 | English 触发 |
|---------|-------------|
| 调研/分析/了解这家公司 | analyze this company |
| 这家公司怎么样 | how is this company |
| 去这家公司怎么样 | is this company worth joining |
| 这家公司靠谱吗 | is [Company] a good company |
| 帮我查一下XX公司 | research [Company] |
| XX公司压力大吗 | work life balance at [Company] |
| XX公司加班严重吗 | overtime culture at [Company] |
| XX公司裁员吗 | layoffs at [Company] |
| XX公司薪资待遇 | salary at [Company] |
| 对比XX和XX公司 | compare [A] vs [B] |
| 帮我看看这个公司靠不靠谱 | check this company |
| 这家公司值不值得去 | should I join [Company] |
| 这家公司能不能去 | can I join [Company] |
| 这家公司有没有坑 | red flags at [Company] |
| 这家公司适合长期发展吗 | growth at [Company] |
| 我拿到XX公司的面试了 | I have an interview with [Company] |
| 我收到了XX公司的 offer | I got an offer from [Company] |
| 这个公司值不值得投 | should I apply to [Company] |
| 这家公司团队风格怎么样 | team culture at [Company] |
| 这家公司会不会很卷 | is [Company] intense |
| 帮我避雷这家公司 | warn me about [Company] |

**关联触发补充：**
- 只要句子里同时出现“公司/企业/团队/老板/offer/入职”中的任一词，以及“怎么样/靠谱不/值不值/能不能去/坑不坑/卷不卷/稳定不稳定/适不适合”等判断性词语，也默认进入公司调研流程。
- 若用户没有给出完整公司名，但提供了简称、产品名、行业名、岗位邀请、面试邀约，也应先进入调研模式并继续追问补全信息。

### 3.2 调研结构（就业专用，改造自 public-company-analysis）

**一、公司概况**
- 名称、行业、总部、成立时间
- 业务描述：产品/服务、客户群体、盈利模式
- 公司规模：员工数、分支机构

**二、经营稳定性（就业核心）**
- 融资阶段 / 上市情况
- 近年营收趋势（判断是否健康经营）
- 现金流状态（判断能否按时发薪）
- 债务情况（是否资不抵债风险）
- ⚠️ 就业风险提示：财务数据反映的稳定性

**三、行业地位 & 前景**
- 市场份额 / 行业排名
- 主要竞争对手
- 政策环境影响
- 行业所处周期

**四、员工评价 & 舆论（最重要）**
- 近 3-6 个月舆论倾向：正面/中性/负面
- 关键事件：融资/大订单/裁员/欠薪/老板失信等
- 员工评价来源：脉脉、知乎、Indeed/Glassdoor、BOSS直聘评价
- ⚠️ 就业风险标注：任何裁员/欠薪/违法用工相关舆情重点标注

**五、目标岗位匹配度**
- 公司业务 vs 目标岗位
- 技术栈是否匹配
- 职级晋升通道

### 3.3 就业匹配打分（10分制）

| 维度 | 权重 | 数据来源 |
|------|------|---------|
| 经营稳定性 | 20% | 融资/营收/现金流 |
| 舆论评价 | 25% | 脉脉/知乎/新闻 |
| 岗位匹配 | 20% | JD vs 用户技能 |
| 地点/通勤 | 15% | 公司地址 vs 用户要求 |
| 行业前景 | 10% | 行业分析 |
| 加班/文化 | 10% | 舆论/评价 |

**评级：**
- 8-10 分：⭐⭐⭐ 强烈推荐
- 5-7 分：⭐⭐ 可以考虑
- 3-4 分：⭐ 谨慎评估
- 0-2 分：⚠️ 风险较高

### 3.4 数据来源优先级
1. 公司官网 / IR 页面
2. 脉脉 / 知乎（员工真实评价）
3. 东方财富 / Yahoo Finance（财务数据）
4. 天眼查 / 企查查（工商信息）
5. 36kr / 虎嗅（行业分析）

---

## Step 4 — 同城职位搜索（boss-cli）

### 4.1 触发场景

| 中文触发 | English 触发 |
|---------|-------------|
| 帮我搜索职位 | search jobs |
| 同城有什么职位 | jobs in [city] |
| XX城市有什么机会 | opportunities in [city] |
| 帮我看看XX城市的职位 | job search in [city] |
| 找类似职位 | find similar jobs |
| 这家公司还在招人吗 | is [Company] hiring |
| 工资多少 | salary range for [role] |
| XX职位好找吗 | is [role] in demand |
| 我现在能找什么工作 | what jobs fit me now |
| 我适合投什么岗位 | what roles should I apply for |
| 最近有没有合适机会 | any suitable openings lately |
| 帮我看看市场上有没有坑位 | find openings for me |
| 想看看杭州最近的前端机会 | frontend roles in Hangzhou |
| 有没有和我背景接近的岗位 | jobs matching my background |
| 我这个简历能投哪些岗位 | what jobs match this resume |
| 想看看薪资高一点的机会 | higher paying roles |

**关联触发补充：**
- 用户提到“找工作、看机会、投递方向、市场行情、岗位缺口、岗位选择、城市机会、薪资带宽、岗位匹配”等任意相关话题时，都可以进入职位搜索或岗位推荐流程。
- 如果用户还没明确城市/岗位名称，先根据已有简历或经历推断方向，再追问补全城市、薪资、经验年限。

### 4.2 boss-cli 使用流程

**⚠️ 首次使用前必须完成登录（一次性操作）：**

```bash
# Step 1: 检查是否已安装
which boss || echo "NEED_INSTALL"

# Step 2: 检查是否已登录
boss status --json 2>/dev/null
```

**未安装时（自动触发安装）：**
```bash
# 自动安装 boss-cli
uv tool install kabi-boss-cli 2>/dev/null || \
pip install kabi-boss-cli --user 2>/dev/null
```

**未登录时（分步引导）：**

**第一步：**
> 搜索 BOSS 直聘职位需要绑定你的 BOSS 账号。Cookie 存在你本地电脑，不会泄露。

**第二步：**
> 请先确认你的 Chrome/Edge/FireFox 已经登录了 zhipin.com

**第三步：**
> 在终端运行：
> ```
> boss login
> ```

**第四步：**
> 验证：
> ```
> boss status
> boss me --json
> ```
> 看到名字即成功 ✅

### 4.3 搜索命令参考

```bash
# 基础搜索
boss search "{岗位}" --city {城市} --salary {薪资} --json

# 精准搜索
boss search "{岗位}" --city {城市} --salary 20-30K --exp 3-5年 --industry 互联网 --json

# 查看推荐
boss recommend --json

# 导出 CSV
boss export "{岗位}" --city {城市} -n 50 -o {城市}_{岗位}.csv
```

### 4.4 职位表单格式

| 公司 | 岗位 | 薪资 | 上班时间 | 规模 | 融资 | 区域 | 发布时间 | 匹配度 |
|------|------|------|---------|------|------|------|---------|--------|
| xxx | xxx | xx-xxK | 双休 | 1000-9999人 | 已上市 | 杭州-西湖区 | 3天内 | ⭐⭐⭐ |

---

## Step 5 — 模拟面试

### 5.1 触发场景

| 中文触发 | English 触发 |
|---------|-------------|
| 模拟面试 | mock interview |
| 开始面试 | start interview |
| 面试练习 | interview practice |
| 帮我准备面试 | prepare for interview |
| XX分钟后有面试 | interview in N minutes |
| 帮我过一遍面试 | walk me through the interview |
| 行为面试 | behavioral interview |
| 技术面试 | technical interview |
| 复盘面试 | post-interview review |
| 面试评分 | interview score |
| 你来面我 | interview me |
| 拷打我一下 | grill me |
| 帮我压力面 | stress interview me |
| 帮我练自我介绍 | practice my self intro |
| 面试官可能会问什么 | likely interview questions |
| 我怕面试答不上来 | help me prepare answers |
| 帮我准备反问问题 | help me prepare reverse questions |
| 模拟一下面试官追问 | simulate follow-up questions |

**关联触发补充：**
- 只要用户提到“马上面试、准备面试、过一遍、练回答、自我介绍、反问、追问、压力面、复盘、被问懵了”等表达，就默认进入模拟面试或面试准备流程。
- 如果用户只说“我明天有个面试”或“我有点慌”，也应直接接管并开始收集公司、岗位、JD、简历亮点。

### 5.2 面试准备

综合以下信息出题：
- 目标公司背景（Step 3 调研）
- JD 要求
- 简历亮点（Step 2 优化后）

### 5.3 面试模块（参考 interview-simulator）

**开场（1题）：**
> "请自我介绍，重点说说为什么你适合这个岗位。"

**技术/专业（2-3题）：**
基于 JD 和公司技术栈提问

**STAR 行为（1-2题）：**
> "请描述一次你遇到重大技术挑战的经历。"

**公司动机（1题）：**
> "你为什么想加入我们公司？"

**反问（1题）：**
> "你有什么问题想问我吗？"

### 5.4 评分标准（1-10）

| 维度 | 权重 |
|------|------|
| 答案完整度 | 25% |
| 技术深度 | 30% |
| 表达清晰度 | 20% |
| 岗位匹配度 | 25% |

---

## Step 6 — 复盘评分卡

```
════════════════════════════════════════
        📋 面试复盘评分卡
════════════════════════════════════════
目标公司：{公司名称}
目标岗位：{岗位名称}
面试时间：{YYYY-MM-DD HH:MM}
────────────────────────────────────────
面试表现：
  自我介绍：        [X/10]
  技术/专业能力：    [X/10]
  项目/经历深度：    [X/10]
  行为问题（STAR）： [X/10]
  岗位理解/动机：    [X/10]
  沟通表达：        [X/10]
────────────────────────────────────────
综合得分：          [X/10]
综合评价：{Strong Hire / Hire / Lean Hire / Lean No Hire / No Hire}
────────────────────────────────────────
💪 优势：
  1. …
  2. …
  3. …

🔧 待提升：
  1. …
  2. …
  3. …

📚 针对该公司的复习建议：
  1. …
  2. …
════════════════════════════════════════
```

---

## 🗣️ 全场景触发词速查表

| 场景 | 推荐触发语 |
|------|-----------|
| 全面启动 | "帮我全面准备面试" / "我最近想换工作，帮我一起梳理一下" |
| 简历优化 | "帮我看看简历有哪些可以优化的地方" / "我这份简历能打几分" / "你帮我改改简历" |
| 上传简历 | "这是我的简历" / "我上传了简历" / "你先看看我的经历" |
| 公司调研 | "帮我调研一下XX公司" / "XX公司怎么样" / "这家公司值不值得去" / "这家公司靠谱吗" |
| 职位搜索 | "帮我搜索XX城市的XX岗位" / "我现在适合找什么工作" / "看看最近有没有合适机会" |
| 模拟面试 | "帮我模拟一下XX公司的面试" / "你来面我" / "帮我压力面一下" |
| JD分析 | "帮我看看这个JD" / "这个岗位要求是什么" / "我能不能胜任这个岗位" |
| Offer评估 | "帮我评估一下这个Offer" / "这个 offer 值不值得接" / "这份工作能去吗" |
| 面试复盘 | "面试完了，帮我复盘一下" / "我刚面完，有点乱，帮我总结一下" |
| 谈薪指导 | "马上要谈薪资了，帮我准备一下" / "薪资怎么谈更稳" |
| 自我介绍 | "帮我写一个自我介绍" / "帮我准备一版面试开场" |
| 离职原因 | "面试被问到离职原因怎么说" / "离职原因怎么表达更稳妥" |
| 反问环节 | "面试反问环节应该问什么" / "最后我该问面试官什么" |
| 求职方向 | "我接下来该往哪个方向找工作" / "你觉得我适合什么岗位" |
| 情绪接管 | "我有点慌，不知道怎么准备" / "我怕这场面试挂掉" |

---

## ⚠️ 安全与隐私

1. **简历 PII**：建议用户自行脱敏（姓名/公司名）
2. **boss-cli Cookie**：存储本地，不上传服务器
3. **PDF 处理**：在用户本地完成，不上传文件
4. **禁止编造**：所有结论基于公开信息

---

## 📂 文件结构

```
career-compass/
├── SKILL.md                    ← 主 Skill 入口
├── README.md                   ← 使用说明
├── ref/
│   ├── pdf-tool/              ← PDF 解析参考
│   ├── employment-company/     ← 公司调研参考
│   └── interview-simulator/    ← 面试模拟参考
└── boss-cli/                  ← BOSS 直聘 CLI 源码
```
