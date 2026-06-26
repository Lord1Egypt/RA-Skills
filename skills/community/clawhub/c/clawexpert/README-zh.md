# ClawExpert 🧠

**让你的 Claw 成为自我进化的领域专家**

[English](README.md)

ClawExpert 是一个 OpenClaw 学习插件。安装后，你可以让 OpenClaw 围绕任意主题自主研究数小时，将成果沉淀为结构化、可引用的本地知识库——回答问题时基于真实资料，而非模型参数记忆。

---

## 快速开始

```bash
# 安装
clawhub install clawexpert

# 开始学习
/clawexpert learn 布雷顿森林体系的建立与瓦解

# 指定学习时长
/clawexpert learn --hours 3 A股市场分析框架
  
# 查看状态
/clawexpert status

# 深化已有主题
/clawexpert learn --deepen bretton-woods-system
```

学习完成后，直接提问即可。ClawExpert 自动识别相关主题，基于知识库给出带来源引用的回答。

---

## 工作原理

### 学习流程（`/clawexpert learn`）

| 步骤 | 内容 |
|------|------|
| **1. 初始化** `[0%]` | 生成 slug，检查同名/近似主题冲突，创建目录结构 |
| **2. 拆题** `[5%]` | 根据主题复杂度拆解为子课题（最少 4 个，无硬性上限） |
| **3. 并发学习** `[10%]` | 并行启动 subagent（上限为 `maxChildrenPerAgent`），超出则分批流水线执行 |
| **4. 监控** `[10–60%]` | 每 30 秒检查完成情况，实时显示进度 |
| **5. 合并** `[60–97%]` | 去重、构建知识树、写入正式节点与主题索引 |
| **6. 写索引** `[97%]` | 更新图书馆式 `_index/` 层（L1 → L2 → 主题摘要 + 资料摘要） |
| **7. 报告** `[100%]` | 输出学习完成摘要 |

### 检索流程（直接提问）

三层检索，从粗到细：

```
第一层：_index/_root_index.md
        全知识库主题地图——路由判断在此完成

第二层：_index/{l1}/{l2}/_index.md
        各主题的关键结论 + 资料摘要——大多数问题在此层即可回答

第三层：{slug}/raw/web/*.md
        原始下载资料——仅在需要精确核实数据时触发
```

### 来源优先级（T1–T4）

| 等级 | 示例 |
|------|------|
| **T1** | 同行评审论文、官方标准、政府统计报告 |
| **T1.5** | 知名机构的预印本（arXiv、SSRN 等） |
| **T2** | 央行报告、智库研究、国际组织文件、官方社交媒体 |
| **T3** | 专业媒体、领域专刊、专家评论 |
| **T4** | 大众媒体、博客、聚合站点 |

学习时优先采用高等级来源，仅在 T1–T3 覆盖不足时才使用 T4。

---

## 知识库结构

```
~/.openclaw/workspace/knowledge/
│
├── _categories.json                    # 你定义的 L1 一级分类（首次使用时设置）
│
├── _index/                             # 图书馆式索引层
│   ├── _root_index.md                  # 全知识库地图——每次会话自动加载
│   └── {l1-id}/
│       └── {l2-label}/
│           └── _index.md              # 分类索引：主题摘要、关键结论、资料摘要
│
└── {topic-slug}/                       # 存储层——每个主题一个目录
    ├── meta.json                       # 元数据：状态、子课题、会话记录
    ├── index.md                        # 知识树总览 + 待深入方向
    ├── raw/
    │   ├── web/{hash}.md               # 下载的网页资料（Markdown 格式）
    │   └── pdf/{hash}/                 # PDF 资料（超长时拆分为 part-*.md）
    └── nodes/
        ├── node-001.md                 # 正式知识节点
        └── ...
```

---

## 命令列表

| 命令 | 功能 |
|------|------|
| `/clawexpert learn <topic>` | 开始学习 |
| `/clawexpert learn --hours <n> <topic>` | 指定最长学习时长（小时，默认 2） |
| `/clawexpert learn --deepen <slug>` | 深化已有主题（追加，不覆盖） |
| `/clawexpert learn --auto` | 自动模式：深化所有未完成主题（适合 Cron） |
| `/clawexpert status` | 查看所有主题状态 |
| `/clawexpert show <slug>` | 展示某主题知识树 |
| `/clawexpert ask <slug> <question>` | 强制基于指定主题知识库回答 |
| `/clawexpert forget <slug>` | 删除某主题全部知识（需确认） |
| `/clawexpert export <slug>` | 将知识树导出为单文件 Markdown |

---

## 配置

推荐的 `openclaw.json` 配置：

```json
{
  "agents": {
    "defaults": {
      "subagents": { "maxChildrenPerAgent": 8 },
      "pdfModel": { "primary": "google/gemini-2.0-flash" }
    }
  },
  "plugins": {
    "entries": {
      "google": {
        "config": {
          "webSearch": {
            "apiKey": "{你的 Google AI Studio Key}",
            "model": "gemini-2.0-flash"
          }
        }
      }
    }
  },
  "env": {
    "CLAWEXPERT_KNOWLEDGE_DIR": "/自定义路径"
  }
}
```

| 配置项 | 说明 |
|--------|------|
| `maxChildrenPerAgent` | 并发 subagent 上限（未配置时默认为 5） |
| `pdfModel` | 必须使用 `provider: "google"` 才能走原生 PDF 路径 |
| 网络搜索 | 需要 Google AI Studio API Key；推荐 `gemini-2.0-flash`（免费层 15 RPM），`gemini-2.5-flash` 仅 5 RPM |
| `CLAWEXPERT_KNOWLEDGE_DIR` | 自定义知识库路径（默认 `~/.openclaw/workspace/knowledge`） |

---

## 与其他 Skill 的关系

| | self-improving-agent | ClawExpert |
|--|---------------------|------------|
| 学什么 | 怎么做事（程序性知识） | 知道什么（陈述性知识） |
| 知识来源 | 对话纠错 | 自主 Web 学习 |
| 适用场景 | 长期项目协作 | 专业领域问答与引用 |

两者可同时安装，互补不竞争。

---

## 许可证

MIT License
