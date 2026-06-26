# 卡帕西六步抄作业法 · Get笔记落地手册

> 核心思想："现在 AI 已经把做事情的门槛变得极低，而'做什么'反而比'怎么做'要有价值得多。"
> 一旦 Skill 跑通，以后你只需要一句话，整套知识管理流程自动跑完。

**🎯 默认主阵地："得到"知识库（topic_id: `eYzMmvnm`）**
> 张公子的主要知识管理环境在此知识库。六步法所有操作优先使用 `@getnote/cli`，API作为降级方案。

---

## 工具优先级的变化（v0.1.5+）

| 操作 | 优先方案 | 降级方案 |
|------|---------|---------|
| 语义搜索（Step 4） | `getnote search --kb <id>` ✅ | 本地AI分析（不可靠） |
| 存入内容（Step 2） | `getnote save <url\|text>` ✅ | `POST /resource/note/save` |
| 列出笔记 | `getnote kb <id> --all -o json` ✅ | `GET /resource/knowledge/notes` |
| 管理知识库 | `getnote kb create/add` ✅ | `POST /resource/knowledge/create` |
| 给笔记打标签 | `getnote tag add <id> <tag>` ✅ | Tag API（路径未知） |

> **为什么优先CLI？**
> 1. `getnote search` 解决了 recall API 返回 404 的问题
> 2. `getnote save --url` 自动异步抓取链接内容，无需手动轮询
> 3. 所有输出 `-o json`，AI直接解析，无需文本处理
> 4. QPS限制由CLI内部处理

---

## 第1步：30秒搭建目标知识库

**一句话指令：**
```
帮我建"内容素材库"知识库，用途是"收集做内容用的案例、数据、观点和灵感"
```

**执行（CLI）：**
```bash
getnote kb create "内容素材库" --desc "收集做内容用的案例、数据、观点和灵感"
```

---

## 第2步：零门槛随手存

### 2A. 链接存档（CLI自动异步抓取）
**指令：**
```
把这个链接存到内容素材库：https://...
```

**执行（CLI）：**
```bash
getnote save https://example.com/article --tag AI -o json
```
→ CLI自动轮询抓取页面全文，完成后返回结构化JSON

### 2B. 语音/录音存档
> ⚠️ CLI `save` 不支持直接上传音频。录音笔记存为文字笔记，在content中写入AI生成的摘要。

**执行（CLI）：**
```bash
getnote save "录音摘要内容..." --title "录音笔记标题" --tag 录音,AI -o json
```

### 2C. 零散想法
**执行（CLI）：**
```bash
getnote save "刚看到一个数据：XXX" --tag 经济观察 -o json
```

---

## 第3步：全自动整理

**手动触发：**
```
整理一下内容素材库里最近的新笔记
```

**执行（CLI）：**
```bash
# 获取全部笔记
getnote kb eYzMmvnm --all -o json

# 语义分析后打标签
getnote tag add <note_id> <标签>
```

**整理逻辑：**
1. 遍历知识库全部笔记（`--all` 自动翻页）
2. 语义判断归属细分类目
3. 自动补充缺失标签
4. 生成整理报告

---

## 第4步：向知识库提问（CLI语义搜索 ✅）

**基础语义搜索（CLI）：**
```
在内容素材库里搜一下：关于 AI Agent 的最新进展
```
```bash
getnote search "AI Agent最新进展" --kb eYzMmvnm --limit 5 -o json
```

**进阶对比分析（CLI）：**
```
对比分析内容素材库里关于"大模型开源 vs 闭源"的所有观点
```
```bash
# 分别召回正方和反方
getnote search "开源大模型优势" --kb eYzMmvnm --limit 8 -o json
getnote search "开源大模型问题" --kb eYzMmvnm --limit 8 -o json
# 本地整合输出对比框架
```

**全局脉络梳理（CLI）：**
```
梳理一下 AI 行业观察库关于 RAG 领域的全局脉络
```
```bash
getnote search "RAG" --kb eYzMmvnm --limit 10 -o json
# 按时间线组织RAG相关笔记，输出脉络图谱
```

---

## 第5步：反哺知识库（沉淀复利）

**沉淀分析结果（CLI）：**
```
把刚才关于 AI Agent 的分析结果存成新笔记，标题叫"AI Agent 发展脉络"
```
```bash
getnote save "<完整分析内容>" --title "AI Agent 发展脉络" --tag AI,沉淀 -o json
```

**沉淀创作产出（CLI）：**
```
把我刚写的文章存到内容素材库
```
```bash
getnote save "<文章正文>" --title "<标题>" --tag 产出 -o json
```

---

## 第6步：每周知识库体检

**触发指令：**
```
给内容素材库做个体检
```

**执行（CLI）：**
```bash
# 统计所有知识库
getnote kbs -o json

# 获取某知识库详情
getnote kb eYzMmvnm --all -o json
```

**体检内容：**
1. **总量统计**：笔记总数、知识库数
2. **分类索引**：各主题下的笔记清单
3. **内容空白识别**：哪些重要主题还没有笔记？
4. **活跃度分析**：哪些知识库很久没更新了？
5. **优化建议**：标签体系是否需要精简？

**保存索引笔记：**
```
把体检报告存成索引笔记
```
```bash
getnote save "<体检报告全文>" --title "🏥 知识库体检报告 · X | YYYY-MM-DD" --tag 体检报告 -o json
```

---

## 六步闭环流程

```
第1步：建库 → 第2步：存入 → 第3步：整理 → 第4步：搜索
                                                      ↓
第6步：体检 ← 第5步：反哺 ← (分析结果沉淀回知识库) ← (搜索结果)
```

六步法不是线性流程，而是**循环增强系统**：
- 存得越多 → 搜索越准 → 分析越深 → 反哺越有价值 → 形成复利
