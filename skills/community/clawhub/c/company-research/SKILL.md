---
name: "company-research"
description: "企业背景调查工具（智访通） — 面向电信客户经理，输入企业名称即可生成企业概况、近期动态、互联网信息和商机雷达报告。通过公共搜索引擎（百度、360、搜狗微信、头条）搜集企业公开信息。"
metadata: {"openclaw":{"requires":{"bins":["agent-browser"]}}}
allowed-tools: Bash(agent-browser:*)
---

# 企业背景调查 v1.0

面向电信客户经理的企业信息搜集与商机分析工具。输入企业名称，自动搜索公开信息并输出结构化报告。

## 环境检测（首次运行必须执行）

在开始搜索前，先检测 `agent-browser` 是否可用：

```bash
which agent-browser
```

- **如果输出路径**（如 `/usr/local/bin/agent-browser`）：环境就绪，使用 `agent-browser` 模式。
- **如果输出为空或 not found**：告知用户需要安装：

> ⚠️ 本技能需要 agent-browser（headless 浏览器工具）才能获取完整的企业工商数据。
> 推荐通过 ClawHub 技能注册表安装（已审核）：
> ```
> clawhub install TheSethRose/agent-browser
> ```
> 或通过 npm 手动安装（Vercel Labs 开源项目 https://github.com/vercel-labs/agent-browser ）：
> ```
> npm install -g agent-browser && agent-browser install --with-deps
> ```
> 安装完成后重新发起查询即可。

## 浏览器工具

使用 `agent-browser` 的以下三个只读命令进行网页访问：

```bash
agent-browser open "<url>"       # 打开页面
agent-browser snapshot -c        # 获取页面文本内容（compact 模式）
agent-browser close              # 完成后关闭浏览器
```

> **重要**：每次 `open` 后必须 `snapshot -c` 读取内容，然后从 snapshot 输出中提取所需信息。

### 安全约束

本技能**仅使用**以下 agent-browser 命令：`open`、`snapshot`、`close`。

**禁止使用**以下功能：
- `state save` / `state load`（会话状态保存/加载）
- `cookies` / `storage`（Cookie 和本地存储访问）
- `network route`（网络请求拦截）
- `eval`（JavaScript 执行）
- `fill` / `click` / `type`（表单交互）

本技能不请求任何凭据、不访问已认证资源、不保存任何浏览器状态。所有访问目标均为公共搜索引擎。

## 搜索引擎

仅使用以下引擎：

| 引擎 | URL 模板 | 用途 |
|------|----------|------|
| 百度 | `https://www.baidu.com/s?wd={keyword}` | 企业工商信息、新闻、通用搜索（主力） |
| 360 | `https://www.so.com/s?q={keyword}` | 补充搜索、企业信息验证 |
| 微信 | `https://wx.sogou.com/weixin?type=2&query={keyword}` | 公众号文章、行业动态 |
| 头条 | `https://so.toutiao.com/search?keyword={keyword}` | 近期新闻、融资动向 |

## 数据提取策略

百度搜索结果页会内嵌爱企查/企查查的企业摘要卡片，从中可直接提取：
- 注册资本、参保人数、成立日期、统一社会信用代码
- 法定代表人、股东、实际控制人
- 对外投资、控股企业、分支机构数量及名称
- 企业标签（高新技术企业、专精特新等）
- 联系电话、注册地址

**关键技巧**：搜索关键词中加入"企查查"或"天眼查"可以让百度优先返回这些平台的摘要卡片。

## 搜索步骤

收到企业名称 `{company}` 后，按以下顺序执行：

### 第一轮：企业基础信息
```bash
# 1. 工商核心信息（参保人数、注册资本、股东等）
agent-browser open "https://www.baidu.com/s?wd={company}+参保人数+高新技术企业"
agent-browser snapshot -c
# 从 snapshot 提取：参保人数、注册资本、标签、简介

# 2. 股东、关联企业、分支机构
agent-browser open "https://www.baidu.com/s?wd={company}+股东+实际控制人+分支机构"
agent-browser snapshot -c
# 从 snapshot 提取：股东、控制企业、分支机构、对外投资

# 3. 官网和业务信息
agent-browser open "https://www.baidu.com/s?wd={company}+官网"
agent-browser snapshot -c
# 从 snapshot 提取：官网 URL、企业业务描述
```

### 第二轮：近期动态
```bash
# 4. 融资信息
agent-browser open "https://www.baidu.com/s?wd={company}+融资"
agent-browser snapshot -c

# 5. 招聘动向
agent-browser open "https://www.baidu.com/s?wd={company}+招聘+最新"
agent-browser snapshot -c

# 6. 中标记录
agent-browser open "https://www.baidu.com/s?wd={company}+中标+2024+2025"
agent-browser snapshot -c

# 7. 近期新闻（头条）
agent-browser open "https://so.toutiao.com/search?keyword={company}"
agent-browser snapshot -c

# 8. 微信文章
agent-browser open "https://wx.sogou.com/weixin?type=2&query={company}"
agent-browser snapshot -c
```

### 第三轮：深度信息
```bash
# 9. 高管背景
agent-browser open "https://www.baidu.com/s?wd={company}+创始人+董事长+经历"
agent-browser snapshot -c

# 10. 苏州本地活动
agent-browser open "https://www.baidu.com/s?wd={company}+苏州+工业园区"
agent-browser snapshot -c

# 11. 合作项目
agent-browser open "https://www.baidu.com/s?wd={company}+战略合作+签约"
agent-browser snapshot -c

# 12. 补充验证
agent-browser open "https://www.so.com/s?q={company}+核心业务+产品优势"
agent-browser snapshot -c
```

> **注意**：每轮搜索后评估已获取信息，如某维度已有充分数据则跳过后续同类查询。完成后执行 `agent-browser close`。

## 输出格式

严格按以下结构输出。**如果某个小节没有搜索到相关信息，直接省略该小节，不要输出空内容或"暂无"。**

---

### 一、企业概况

#### 1.1 基础信息

- **基础信息**：{联系电话}、{地址}、{注册资本}（并列显示，用"、"隔开，不换行）
- **官网网址**：{官网链接}
- **企业业务**：{主营业务描述}
- **名录标签**：{独角兽、高新技术企业、专精特新等}
- **榜单标签**：{各类 TOP 榜单}
- **参保人数**：{数字}人
- **股东及实际控制人**：{前3大股东}、实际控制人：{姓名}（并列显示，用"、"隔开，不换行）
- **核心人员**：{法人、董事、高管}（并列显示，用"、"隔开，不换行）
- **关联企业**：关联企业{数量}家，其中控制企业{数量}家（{列出最多10个名称}）、分支机构{数量}家（{列出最多10个名称}）、海外布局：{全球参控股企业名称}
- **其他信息**：{从企业年报、财务数据等用户输入中提取的有价值信息，整段输出，不换行}

> **电话格式要求**：原样显示电话号码，不要将连续数字识别为电话格式（如不要把 `4009282212` 格式化为 `400-928-2212`）

#### 1.2 近期动态

- **重要变更**：{最近一次地址/高管变动，说明变动前后对比}
- **融资动向**：{最新融资信息及趋势}（并列显示，用"、"隔开，不换行）
- **招聘动向**：{最新招聘发布时间、发布频次、主要岗位}（不换行）
- **招投标**：{仅显示「中标单位」角色的记录，注明涉及方、时间、金额}（并列显示，用"、"隔开，不换行）
- **主要客户**：{列出1-3家，优先关注政府、学校、医院、通信运营商}（并列显示，用"、"隔开，不换行）
- **近期新闻**：{2023年起的新闻最多5条，越近越靠前}（并列显示，用"、"隔开，不换行）

> **招投标警告**：严禁显示"提及单位"或"投标单位"角色的记录，仅显示该企业作为中标单位的记录。

#### 1.3 其他互联网信息

- 企业简介、核心业务、产品优势和市场地位
- 高管（创始人、董事长、总经理、副总经理）的以往工作经历、毕业院校、社会职务、籍贯、发表过的主要观点
- 企业及高管参加苏州的活动，或参加高校活动的情况
- 企业与苏州地方政府、领导的互动情况
- 企业项目、战略合作签约，特别关注在苏州的合作签约

---

### 二、商机雷达

根据上文搜集的企业信息，按以下规则自动判断并输出适用的商机建议。**不满足触发条件的项目直接省略。**

| 商机 | 触发条件 | 标记 |
|------|----------|------|
| **V网团购** | 参保人数 > 10 人（无数据时提醒用户自行关注） | ✅ |
| **FTTR-B 套餐** | 参保人数 < 10 人 或 未找到参保人数 | ✅ |
| **组网专线** | 分支机构 ≥ 3 家 | ✅ |
| **服贸通 / SD-WAN** | 存在海外市场或海外关联企业 | ✅ |
| **生态合作提醒** | 招投标或新闻涉及政府或运营商 | ✅ |
| **天翼云 + 算力 + 专线入云 + 算力补贴** | AI / 软件 / 研发型企业 | ✅ |
| **5G 工业互联网 / 智慧储能** | 拥有制造基地 | ✅ |
| **其他建议** | 以上维度之外，根据企业特征推荐一条电信相关商机并给出理由 | ✅ |

---

## 信息质量规则

1. **优先级**：优先选择与用户关注点直接相关且信息价值最高的内容。必须理解上下文和含义，不是关键词匹配。
2. **信息整合**：如果多个参考片段涉及同一主题，整合为一段。
3. **禁止编造**：只能根据搜索到的信息整理和总结，禁止引入外部知识或无依据推测。新闻没有明确时间时，禁止编造时间。
4. **防止混淆**：严禁混入名称相近但不是目标企业的信息，严禁混入非目标企业高管的信息。
5. **时效性**：2026年新闻优先展示，只关注2023年及之后的新闻（高管或运营商相关除外）。
6. **过滤噪音**：不要提供劳动纠纷等诉讼信息，不要提供专利、工商变更等高频重复性信息。
