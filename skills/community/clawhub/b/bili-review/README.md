# bili-review 📺

> **高信息密度 B 站视频总结工具**：整合 **官方 AI 字幕**（UP 主主张） + **高能弹幕时序**（即时纠错与群体反应） + **深度楼中楼评论**（群众实测检验），生成三源交叉事实总结。

[![GitHub Stars](https://img.shields.io/github/stars/frozentearz/bili-review?style=flat-square)](https://github.com/frozentearz/bili-review)
[![License](https://img.shields.io/badge/license-MIT--0-blue?style=flat-square)](LICENSE)

---

## 📺 输出效果预览

`bili-review` 采用**渐进式双层呈现**：顶部置顶【速读卡】快速做决策，下方展开【详细总结】按视频类型提供落地干货。

```markdown
# 《XXX 深度实测》视频总结

> 👤 **UP主**：某科技测评 ｜ 📅 **发布时间**：2026-08-20 ｜ 🔗 **视频地址**：https://www.bilibili.com/video/BV1xxxxxx

---

### ⚡ 速读卡
- 🚦 **判定结论**：【⚠️ 避坑】（核心卖点存在发热暗病，暂不推荐冲首发）
- 📌 **一句话主张**：UP 主宣称性能提升 40%、续航翻倍，是今年最值得买的设备。
- 🔍 **弹幕/评论真相**：弹幕 `[08:24]` 密集吐槽高负载降频；评论区高赞（1200+赞）实测连续运行 20 分钟即触发严重发热卡顿。
- 🎯 **行动建议**：直接跳过首发，建议观望次代固件或选择民间平替。

---

## 📌 详细总（红黑榜版，另有步骤清单、前因后果与内幕、通俗打比方与机制拆解等《总结框架》）结

### 1. 🟢 UP 主吹的卖点（红榜）
- **性能飞跃**：宣称搭载全新架构，基准跑分提升 **40%**。
- **外观轻薄**：厚度缩减至 **8.2mm**，支持磁吸生态。

### 2. 🔴 弹幕与评论扒出的槽点（黑榜）
- **高负载发热降频**：弹幕 `[08:24]` 与 `[11:05]` 集中指出视频剪掉了烤机后半段；评论区多位首发用户反馈 4K 录像 15 分钟必死机。
- **拓展配件溢价高**：官方拓展坞售价高达 **¥599**，且协议私有。

### 3. ⚖️ 选型建议与民间平替
- **适合人群**：仅适合轻度办公、不玩大型游戏的外观党。
- **民间平替**：评论区高赞推荐 **品牌 B 去年同价位旗舰**，性能释放更稳定且便宜 30%。
```

---

## 🚀 选择使用方式

根据你的日常习惯，选择以下任意一种方式即可开箱即用：

### 方式 A：B 站网页端油猴脚本（最简单、适合日常刷视频）

直接在浏览器油猴插件（Tampermonkey / ScriptCat）中导入本仓库根目录下的 [`bili-review.user.js`](bili-review.user.js)：

1. 打开任意 B 站视频播放页面；
2. 页面右侧会出现悬浮工具栏，或直接按下快捷键 <kbd>Tab</kbd> 呼出抽屉面板；
3. 点击 **「一键总结」**，实时流式生成并渲染排版精美的视频总结。

---

### 方式 B：AI Agent 技能包（适合 Claude Code / OpenClaw / Antigravity）

如果你在使用各类 AI 终端或 Agent 工作流，可直接安装技能包：

```bash
# 方式一：OpenClaw / ClawHub
openclaw skills install @frozentearz/bili-review

# 方式二：npx skills（任意 Agent）
npx skills add frozentearz/bili-review -g
```

---

### 方式 C：Python CLI 命令行（适合开发者 / 脚本批量处理）

#### 1. 安装依赖

```bash
# macOS
brew install yt-dlp python3

# Windows / Linux / macOS (pip 方式)
pip install yt-dlp
```

#### 2. 克隆仓库与登录

```bash
git clone https://github.com/frozentearz/bili-review.git
cd bili-review

# 首次运行：从本机浏览器自动提取 Cookie（免输密码，一次授权有效约 150 天）
python3 scripts/bili_review.py login
```

#### 3. 常用抓取命令速查

```bash
# 一键抓取全部三源数据（AI 字幕 + 弹幕时序分析 + 评论区楼中楼）
python3 scripts/bili_review.py all "BV1YRhM64Eni"

# 仅抓取弹幕时序热点（30秒时间轴分桶 + 高能峰值 + 即时纠错预警）
python3 scripts/bili_review.py danmaku "BV1YRhM64Eni"

# 仅抓取字幕（支持 BV号 / AV号 / 网页完整链接 / b23.tv 短链）
python3 scripts/bili_review.py subtitle "https://www.bilibili.com/video/BV1YRhM64Eni"

# 仅抓取评论区（--replies 开启楼中楼深度深挖；--limit 设置楼层数）
python3 scripts/bili_review.py comments "BV1YRhM64Eni" --replies --limit 50
```

---

## 💡 四大场景总结框架

`bili-review` 会根据视频类型自动选用确定性的分析骨架，确保输出直击要害：

| 视频类型               | 适用总结方法             | 交付核心内容                                                                       |
| ---------------------- | ------------------------ | ---------------------------------------------------------------------------------- |
| **测评 / 避坑 / 选型** | **红黑榜对比法**         | 🟢 **红榜**（宣传亮点） ｜ 🔴 **黑榜**（实测槽点/暗病） ｜ ⚖️ **选型建议与民间平替** |
| **教程 / 实操 / 配置** | **步骤清单（做减法）**   | 🛠️ **准备工作** ｜ 📋 **核心步骤（直接抄作业）** ｜ ✂️ **做减法与避坑（跳过冗余）**  |
| **观点 / 商业 / 热点** | **前因后果与内幕**       | 📖 **背景与矛盾** ｜ 🧠 **UP 主主张** ｜ 🔍 **评论区内幕爆料** ｜ 💡 **底层真相**  |
| **科普 / 原理 /架构**  | **通俗打比方与机制拆解** | 💡 **通俗大白话比方** ｜ ⚙️ **底层运作机制** ｜ 📌 **弹幕纠错与细节补充**           |

---

## 🗺️ 全流程架构与数据管道

```mermaid
flowchart TD
    %% ==========================================
    %% 1. 输入解析与会话隔离
    %% ==========================================
    subgraph S1 ["1. 触发入口与会话隔离"]
        Input["双端触发入口：<br/>• 🌐 网页端：卡片【AI 总结】/ 播放页顶部【⚡ 总结本视频】/ Tab 抽屉 / 悬浮胶囊<br/>• 💻 CLI / Agent：python3 scripts/bili_review.py & 技能调用"]
        ParseId["标准化锁定唯一 BVID + 注入独立 Session ID (防跨视频历史串味)"]
        Input --> ParseId
    end

    %% ==========================================
    %% 2. 本地三源数据抓取（全新 WBI 验签引擎）
    %% ==========================================
    subgraph S2 ["2. 本地三源数据抓取管道（0 外部 API 费用）"]
        ParseId --> PipeSub["【源一：AI 字幕（最新 WBI 动态验签直连）】<br/>• 本地算法动态计算 w_rid & wts 防盗链签名<br/>• 直连 x/player/wbi/v2 毫秒级抓取 ai-zh 中文及全语言 AI 字幕<br/>• 滑动窗口去重与 [MM:SS] 时间戳对齐"]
        
        ParseId --> PipeDan["【源二：弹幕时序】<br/>• 免登录拉取全量 XML (zlib 纯原生极速解压)<br/>• 30秒分桶计算吐槽峰值与 [MM:SS] 即时纠错/翻车预警"]
        
        ParseId --> PipeCom["【源三：深度评论】<br/>• 阶梯抓取热门高赞主楼（过滤水评/刷屏）<br/>• 并发深挖楼中楼真实口碑（支持 Ctrl+C 中断保留）"]
        
        PipeSub --> MergeData["三源原始数据结构化拼装 (注入 BVID 强锚定)"]
        PipeDan --> MergeData
        PipeCom --> MergeData
    end

    %% ==========================================
    %% 3. 提示词规范与 4 大场景框架
    %% ==========================================
    subgraph S3 ["3. 提示词规范与 4 大场景框架匹配"]
        MergeData --> PromptInjection["注入 bili-review 独立 Prompt 规范:<br/>• 会话与数据强隔离 ｜ 速读卡与详细总结互不重复 ｜ 首句加粗结论先行"]
        
        PromptInjection --> Router{"AI 识别视频类型<br/>选用对应总结框架"}
        Router -- "测评 / 避坑" --> F1["【红黑榜对比法】<br/>🟢 红榜卖点 ｜ 🔴 黑榜暗病 ｜ ⚖️ 选型平替"]
        Router -- "教程 / 实操" --> F2["【步骤清单做减法】<br/>🛠️ 准备工作 ｜ 📋 核心步骤 ｜ ✂️ 跳过冗余"]
        Router -- "观点 / 商业" --> F3["【前因后果与内幕】<br/>📖 背景矛盾 ｜ 🧠 UP主主张 ｜ 💡 底层真相"]
        Router -- "科普 / 原理" --> F4["【通俗打比方与机制拆解】<br/>💡 通俗比方 ｜ ⚙️ 运作机制 ｜ 📌 弹幕纠错"]
    end

    %% ==========================================
    %% 4. AI 智力接入与双协议分发
    %% ==========================================
    subgraph S4 ["4. AI 智力接入与双协议分发 (Max Tokens 8192)"]
        F1 --> AIMode
        F2 --> AIMode
        F3 --> AIMode
        F4 --> AIMode

        AIMode{"AI 智力载体"}
        AIMode -- "形态 A: 网页油猴插件" --> M_Web["图形化设置面板 + 双协议分发器<br/>• Anthropic 协议 (/v1/messages，Claude / 本地 62999)<br/>• OpenAI 兼容协议 (/v1/chat/completions，DeepSeek / GPT / Ollama)<br/>• 支持 /v1/models 连通测试与模型拉取 ｜ 沙箱物理安全存储"]
        AIMode -- "形态 B: AI Agent 技能" --> M_Agent["由宿主 Agent 自身大脑消化生成<br/>(Claude Code / Antigravity / OpenClaw)"]
    end

    %% ==========================================
    %% 5. 渐进式双层总结交付与持久化
    %% ==========================================
    subgraph S5 ["5. 渐进式双层总结交付与持久化 (Progressive Output)"]
        M_Web --> LLMOut["LLM 流式 / 一次性生成双层结构"]
        M_Agent --> LLMOut

        subgraph Doc ["📄 完整视频总结 Markdown 研报"]
            Card["【置顶层】⚡ 速读卡 (秒级判断看不看)<br/>• 🚦 判定结论 (避坑/必看/跳过) ｜ 📌 一句话主张<br/>• 🔍 弹幕/评论真相 (附带时间戳/点赞数) ｜ 🎯 行动建议"]
            
            Detail["【展开层】📌 详细总结 (按框架落地)<br/>• 客观事实账本、加粗参数/指令、对比表格<br/>• 避免二次复述速读卡内容"]
            
            Card --> Detail
        end

        LLMOut --> Doc
        Doc --> DeliveryView["交付呈现与体验体系：<br/>• 🌐 网页端：侧边抽屉阅读器 (创建时间倒序锁定 ｜ 总结时间戳 ｜ 标题 Hover 直达原视频 ｜ 全屏 Tab)<br/>• 💻 终端/Agent：Markdown 研报直出 / 一键复制"]
    end

    %% 样式体系
    classDef step1 fill:#0284c7,stroke:#38bdf8,stroke-width:2px,color:#fff;
    classDef step2 fill:#0f766e,stroke:#2dd4bf,stroke-width:2px,color:#fff;
    classDef step3 fill:#7c3aed,stroke:#a78bfa,stroke-width:2px,color:#fff;
    classDef step4 fill:#d97706,stroke:#fcd34d,stroke-width:2px,color:#fff;
    classDef step5 fill:#15803d,stroke:#4ade80,stroke-width:2px,color:#fff;

    class Input,ParseId step1;
    class PipeSub,PipeDan,PipeCom,MergeData step2;
    class PromptInjection,Router,F1,F2,F3,F4 step3;
    class AIMode,M_Web,M_Agent step4;
    class LLMOut,Card,Detail,Doc,DeliveryView step5;
```

---

---

## 🔒 隐私与安全机制

- **安全沙箱隔离**：`cookies.txt` **仅筛选提取 B 站相关域名**，绝不读取或触碰其他网站数据。
- **本地权限保护**：本地 Cookie 保存为系统权限 `600`（仅当前系统用户可读写），已严格配置 `.gitignore`，绝不外泄。

---

## 🛣️ 路线图（Roadmap）

- [x] **v1.0**：基础 AI 字幕抓取与热门评论爬取。
- [x] **v1.2**：多浏览器 Cookie 自动提取、楼中楼并发深挖与 150 天免维护机制。
- [x] **v2.0**：视频与评论时间戳支持、结构化 Markdown 规范排版。
- [x] **v2.1**：
  - **弹幕时序分析引擎**：免登录 XML 抓取、30 秒时间轴分桶计算、即时纠错提炼。
  - **双层渐进总结体系**：置顶【速读卡】+ 展开【4 大场景详细总结】。
  - **B 站网页端油猴插件**（`bili-review.user.js`）：Tab 键呼出侧边栏抽屉与一键总结。

---

## 📄 License

MIT-0 License
