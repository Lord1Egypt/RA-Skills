# 客户端标识对照表（`skillId` 取值）

> 本表只用于**创建游客时上报的 `skillId`**（客户端/平台标识，历史命名，见 `references/guest-access.md`），回答的是"用户从哪个客户端/平台来"，属于**请求字段**。
> **不要把这个标识写进任何 URL**：输出的 `detail_url` 一律原样引用接口返回值，不得追加、修改或删除任何查询参数（见 SKILL.md §五）。
> **本表不含技能包**：创建游客时另有 `skillCode` = **本 SKILL 的包名**（`debtop-debt-screening`，取自该包 SKILL.md 的 `name`），表示"调用由哪个 SKILL 产生"——与客户端标识是两个维度：不要用表内取值填 `skillCode`。
> 表内为**已约定**取值，直接采用；表里没有的客户端**按下面「生成规则」由脚本生成**（勿手写），并登记回本表，避免统计口径分裂。**同一产品多端共用一个标识**。

## 生成规则（`skillId`）

创建游客时上报的 `skillId` 按下面三级优先规则生成 —— 这是唯一权威规则，**不要凭感觉手写**：

**① 表内命中（最优先）**：客户端产品名在本表「客户端 / 平台」列 → 用表内「标识」。

> ⚠️ **中文产品名必须走这条**：算法只产出 ASCII，中文名会被归一化成空 → 兜底 `mcp`。例如 `千问办公` → `qwen-office`。

**② 表外按算法生成**（用脚本，勿手写）：

```bash
python3 scripts/client_id.py --name "<客户端产品名>"    # 表命中或算法生成, 输出标识（实现见 @scripts/client_id.py）
python3 scripts/client_id.py --name "<产品名>" --json   # 附带来源: table / derived / fallback
python3 scripts/client_id.py --check                    # 规则自检向量
```

1. Unicode NFKC 归一化（全角 → 半角）→ 去首尾空白 → 转小写；
2. 任何**非** `[a-z0-9]` 的连续字符段 → 单个 `-`（空格、中文、`/`、`+`、emoji 都算）；
3. 合并连续 `-`，去掉首尾 `-`；
4. 截断到 **32** 字符并去掉结尾 `-`（服务端上限 64，留余量）；
5. 结果为空 → `mcp`。

**③ 拿不到客户端产品名** → `mcp`。

**产品名从哪来（按优先级）**：① 宿主平台显式提供的客户端名 → ② 宿主应用名 → ③ 用户说明 → ④ 兜底 `mcp`。

**禁止编进标识的信息**：版本号 / 端类型（`-ios`、`-web`、`-app`）/ 部署位置类信息（内部部署名、集群名）/ 随机串、UUID、时间戳 / 用户信息（昵称、手机号、设备型号、本机用户名）/ `guest_id`、令牌片段。

**一致性要求**：同一产品在**任何端、任何版本、任何会话、任何 SKILL** 里都必须得到同一个标识；标识一旦上线**不要随意变更**（服务端创建去重按「技能包 + 客户端 + 来源 + 设备/用户」分组，值变了会各自建游客）。

**自检向量**（`python3 scripts/client_id.py --check` 必须全部通过；自定义实现可用下表对拍）：

| 输入（产品名） | 输出 | 走哪条 |
|---|---|---|
| `千问办公` | `qwen-office` | 表 |
| `Kimi（月之暗面）` | `kimi` | 表 |
| `GitHub Copilot` | `github-copilot` | 表 |
| `WorkBuddy` | `workbuddy` | 表（与算法结果一致） |
| `  Cursor  ` | `cursor` | 算法 |
| `Foo Bar` | `foo-bar` | 算法 |
| `qwen_office` | `qwen-office` | 算法 |
| `Qoder.app` | `qoder-app` | 算法 |
| `123Client` | `123client` | 算法 |
| `Very Long Name With Many Words And More` | `very-long-name-with-many-words-a` | 算法（截断 32） |
| `未知中文客户端` / `---` / 空 | `mcp` | 兜底 |

**办公 / 通用 AI 助手**

| 客户端 / 平台 | 标识 |
|---|---|
| 千问办公 | `qwen-office` |
| 通义千问（阿里） | `qwen` |
| 豆包（字节） | `doubao` |
| 文心一言 / 文小言（百度） | `ernie` |
| 腾讯元宝 | `yuanbao` |
| Kimi（月之暗面） | `kimi` |
| 智谱清言（GLM） | `chatglm` |
| 讯飞星火 | `spark` |
| 秘塔 AI 搜索 | `metaso` |
| 天工（昆仑万维） | `tiangong` |
| 海螺 AI（MiniMax） | `hailuo` |
| 跃问（阶跃星辰） | `yuewen` |
| 商量 SenseChat（商汤） | `sensechat` |
| 纳米 AI（360） | `nami` |
| 盘古 / 小艺（华为） | `pangu` |
| ChatGPT | `chatgpt` |
| Claude | `claude` |
| Gemini | `gemini` |
| Grok（xAI） | `grok` |
| Perplexity | `perplexity` |
| Microsoft Copilot | `copilot` |
| Meta AI | `meta-ai` |
| Le Chat（Mistral） | `le-chat` |
| Poe | `poe` |
| Monica | `monica` |

**编程 / IDE Agent**

| 客户端 / 平台 | 标识 |
|---|---|
| WorkBuddy | `workbuddy` |
| CodeBuddy（腾讯云） | `codebuddy` |
| 通义灵码（阿里） | `lingma` |
| 文心快码 Comate（百度） | `comate` |
| Trae（字节） | `trae` |
| Qoder | `qoder` |
| Cursor | `cursor` |
| GitHub Copilot | `github-copilot` |
| Windsurf | `windsurf` |
| JetBrains AI | `jetbrains-ai` |
| Amazon Q | `amazon-q` |
| Cline | `cline` |
| Roo Code | `roo-code` |
| Continue | `continue` |
| Aider | `aider` |
| Zed | `zed` |
| Replit | `replit` |
| Devin | `devin` |

**Agent 平台 / 编排**

| 客户端 / 平台 | 标识 |
|---|---|
| 扣子 Coze（字节） | `coze` |
| Dify | `dify` |
| 阿里云百炼 | `bailian` |
| 腾讯元器 | `yuanqi` |
| 百度千帆 | `qianfan` |
| n8n | `n8n` |
| Manus | `manus` |
| Genspark | `genspark` |
| Zapier | `zapier` |

**企业协作 / 办公套件**

| 客户端 / 平台 | 标识 |
|---|---|
| 钉钉 AI 助理 | `dingtalk` |
| 飞书智能伙伴（Lark） | `feishu` |
| 企业微信 | `wecom` |
| Notion AI | `notion-ai` |
| Slack AI | `slack` |

**开源客户端 / 自建**

| 客户端 / 平台 | 标识 |
|---|---|
| Open WebUI | `open-webui` |
| LobeChat | `lobechat` |
| NextChat | `nextchat` |
| Cherry Studio | `cherry-studio` |
| Chatbox | `chatbox` |
| LibreChat | `librechat` |
| AnythingLLM | `anythingllm` |
| 兜底：自建 / 内部平台 / 判断不出客户端 | `mcp` |
