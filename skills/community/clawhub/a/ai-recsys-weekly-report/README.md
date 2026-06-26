# AI 搜广推技术周报 Skill - 安装与使用指南

## 一、这个 Skill 是什么？

这是一个 **可迁移的自动化 Skill**，将"AI大模型技术在搜广推领域的应用"技术周报的完整生成流程打包。安装后可以在任意 WorkBuddy 账号上：

- 手动触发：生成单次深度技术研究报告
- 自动化定时任务：每周自动执行并同步到 IMA 知识库

## 二、安装步骤

### Step 1: 解压 Skill 文件

将 `ai-recsys-weekly-report.zip` 解压到你的 Skills 目录：

```bash
# 创建 skills 目录（如果不存在）
mkdir -p ~/.workbuddy/skills

# 解压到 skills 目录
unzip ai-recsys-weekly-report.zip -d ~/.workbuddy/skills/

# 确认结构
ls ~/.workbuddy/skills/ai-recsys-weekly-report/
# 应该看到: SKILL.md, scripts/, references/
```

### Step 2: 安装依赖 Skill

本 Skill **依赖** `ima-skills`（腾讯 IMA 知识库操作）。在 WorkBuddy 中安装：

1. 打开 WorkBuddy
2. 进入 Skill 市场 / 设置
3. 搜索并安装 **ima-skills**（或 **腾讯ima**）

### Step 3: 配置 IMA 凭证

```bash
# 打开 https://ima.qq.com/agent-interface
# 获取 Client ID 和 API Key

# 存储凭证
mkdir -p ~/.config/ima
echo "你的Client_ID" > ~/.config/ima/client_id
echo "你的API_Key" > ~/.config/ima/api_key
```

### Step 4: 配置 Node.js 路径（重要！）

上传脚本依赖 Node.js 来运行 COS 上传组件。编辑脚本中的路径：

```bash
# 用你喜欢的编辑器打开
nano ~/.workbuddy/skills/ai-recsys-weekly-report/scripts/upload-to-ima.py

# 找到 NODE_PATH 配置行（约第25行），修改为你的 Node 路径：
# 常见路径:
#   macOS Homebrew: /opt/homebrew/bin/node
#   nvm: ~/.nvm/versions/node/vXX.XX.X/bin/node
#   WorkBuddy 内置: ~/.workbuddy/binaries/node/versions/XX.XX.X/bin/node
#   系统: /usr/local/bin/node

# 验证 node 是否可用:
node --version
```

### Step 5: 获取目标知识库 ID

你需要一个已有的 IMA 知识库来存储报告。获取方式：

```bash
# 方法1: 通过 IMA 客户端查看
# 打开 IMA -> 知识库 -> 点击目标知识库 -> 复制 ID

# 方法2: 如果已配置凭证，可以用 API 搜索
curl -s -X POST "https://ima.qq.com/openapi/wiki/v1/search_knowledge_base" \
  -H "ima-openapi-clientid: $(cat ~/.config/ima/client_id)" \
  -H "ima-openapi-apikey: $(cat ~/.config/ima/api_key)" \
  -H "Content-Type: application/json" \
  -d '{"query": "", "cursor": "", "limit": 20}'
```

记下目标知识库的 ID（格式类似 `_ZE8alWezaRhoUzbmhKTUX7fFPMS4cofZjquLr-5cB4=`）。

## 三、使用方法

### 方式 A: 单次手动生成

在 WorkBuddy 对话中直接说：

> "帮我生成一份 AI 搜广推技术周报，同步到我的 IMA 知识库"

或更具体：

> "用 ai-recsys-weekly-report skill 出一份本周的大模型推荐系统技术报告，知识库ID是 xxx"

### 方式 B: 自动化定时任务

在 WorkBuddy 中创建自动化：

| 字段 | 值 |
|:---|:---|
| 名称 | AI搜广推技术周报 |
| 执行频率 | 每周一上午 9:00 |
| Prompt | 请加载 ai-recsys-weekly-report skill，完整执行一次周报生成并同步到IMA知识库。知识库ID: `<你的KB_ID>` |
| 工作空间 | 你的工作空间路径 |
| 状态 | ACTIVE |

RRULE 格式: `FREQ=WEEKLY;BYDAY=MO;BYHOUR=9;BYMINUTE=0`

## 四、报告输出说明

每次执行会产出：

1. **本地文件**: `AI搜广推技术周报_YYYY-MM-DD.md` (2000-4000字)
2. **IMA 知识库**: 同步到指定知识库
3. **报告内容**:
   - 本周热点综述 (3-5条)
   - 深度技术解读 (2-5篇论文)
   - 技术对比分析表格
   - 创新思考与建议
   - 趋势预测
   - 延伸阅读推荐 (6-12条)
   - 优化调整思考建议
   - 参考文献 (含链接)

## 五、自定义修改

### 修改研究范围

编辑 `references/research-scope.md`，可以：
- 添加/删除研究方向
- 更新代表性工作列表
- 调整搜索关键词

### 修改报告模板

编辑 `SKILL.md` 中的「Step 2: 生成报告」章节，可以：
- 增加/减少章节
- 调整字数要求
- 改变格式风格

### 修改信息源优先级

编辑 `SKILL.md` 中的搜索策略部分，可以：
- 增加 CSDN、掘金等中文来源
- 添加特定会议追踪（如只关注 KDD）
- 调整搜索关键词

## 六、常见问题

**Q: 上传失败提示"找不到 cos-upload.cjs"？**
A: 确保已安装 ima-skills skill，且脚本中 `COS_UPLOAD_SCRIPT` 路径正确。

**Q: Node.js 报错 command not found？**
A: 编辑 `scripts/upload-to-ima.py` 中的 `NODE_PATH` 变量，改为你系统的实际 Node 路径。

**Q: IMA 凭证错误？**
A: 检查 `~/.config/ima/client_id` 和 `~/.config/ima/api_key` 文件内容是否正确。

**Q: 想改报告的保存目录？**
A: 在自动化任务的 prompt 中指定输出路径，或在 SKILL.md 中修改默认路径。

**Q: 想同时发送多个知识库？**
A: 修改 `scripts/upload-to-ima.py`，支持多 kb-id 参数。

## 七、目录结构

```
ai-recsys-weekly-report/
├── SKILL.md                          # 主定义文件
├── README.md                         # 本安装指南
├── scripts/
│   └── upload-to-ima.py              # IMA 知识库上传封装脚本
└── references/
    └── research-scope.md             # 研究范围与技术方向参考
```

## 八、更新日志

- **v1.0** (2026-04-19): 初始版本
  - 完整的三步流程（搜集 → 生成 → 同步）
  - 标准 COS 上传（cos-upload.cjs）
  - 6大技术方向覆盖
  - 可配置的知识库 ID 和 Node 路径
