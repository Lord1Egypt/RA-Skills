# free-llm-installer

把「免费 / 免 key 大模型」一键装进 WorkBuddy 自定义模型，并附带一个 Claude Code 桌面模型切换器。

> 目标：让普通人打开即用，优先用免费模型，不花冤枉钱。

## 目录结构

```
free-llm-installer/                # 本目录本身就是一个 WorkBuddy 技能根目录
├── SKILL.md                       # 技能清单（WorkBuddy 加载用）
├── scripts/
│   └── install_free_llms.py       # 安装 / 体检 / 探测免费模型的脚本
├── tools/                         # 可选的桌面工具
│   ├── claude_model_switcher.pyw  # tkinter 切换器 GUI（点哪个切哪个）
│   ├── Claude模型切换器.cmd        # 双击启动切换器
│   ├── ccproxy.py                 # Anthropic→OpenAI 本地网关（切换器依赖）
│   └── ccproxy-vision.cmd         # 拉起读图代理实例（3458 端口）
└── examples/                      # 配置模板（key 已脱敏为占位符）
    ├── models.json.example        # WorkBuddy 自定义模型模板
    └── glm-profile.example.json   # Claude Code profile 模板
```

把本仓库根目录整体复制到 `~/.workbuddy/skills/free-llm-installer/` 即完成技能安装。

## 支持的免费模型

| 来源 | 模型 | 能力 | 备注 |
|---|---|---|---|
| 智谱 BigModel | `glm-4-flash` | 文本+工具 | **永久免费，最稳** |
| 智谱 BigModel | `glm-4.7-flash` | 文本+工具+推理 | 高峰偶发 429 |
| 智谱 BigModel | `glm-z1-flash` | 推理(数学/代码) | 不支持工具调用 |
| 智谱 BigModel | `glm-4v-flash` | 读图 | 不支持工具调用 |
| Kilo 网关（免 key） | `kilo-auto/free` | 文本+工具 | 零注册 |
| Kilo 网关（免 key） | `nemotron-3-nano-omni-30b` | 读图+工具+推理 | 免 key 读图兜底 |

智谱需在其开放平台拿 API key（https://open.bigmodel.cn），Kilo 用字面量 `anonymous` 即可。

## 使用

```bash
# 安装智谱 GLM 免费系列（需传 key）
python scripts/install_free_llms.py --zhipu-key <YOUR_ZHIPU_API_KEY>

# 安装 Kilo 免 key 系列
python scripts/install_free_llms.py --kilo

# 仅列出当前已装模型
python scripts/install_free_llms.py --list

# 一轮免费模型体检 + 国外平台探测
python scripts/install_free_llms.py --report

# 单独探测国外平台（OpenRouter 等）免费模型可达性
python scripts/install_free_llms.py --probe-foreign
```

## 桌面切换器（tools/）

双击 `Claude模型切换器.cmd` → 弹出窗口，点哪个模型就切到哪个（写入
`~/.claude/settings.json` 并自动拉起需要的本地代理）→ **重启 Claude Code** 生效。

切换器支持：Kilo 文本 / 读图 Vision / DeepSeek-V4(付费，慎开自动模式) /
GLM-4.7 / GLM-4-Flash。要新增模型，在 `claude_model_switcher.pyw` 的
`MODELS` 里加一行即可（配合 `~/.claude/profiles/<name>.json`）。

## 安全提示

- `examples/` 里的 key 均为占位符 `<YOUR_ZHIPU_API_KEY>` / `<YOUR_DEEPSEEK_API_KEY>`，
  **真实 key 永不入库**。
- 不要把 `~/.workbuddy/models.json`、`~/.claude/profiles/*.json` 直接提交。
- DeepSeek-V4 是**付费**模型，Claude Code 开自动模式极易烧钱，默认别选它。

## 已知坑

- 智谱免费档（glm-4.6v / 高峰 glm-4.7）偶发 `429 / 1305 访问量过大` → 服务器过载，
  非配置问题，重试或错峰即可。
- Kilo 免费 worker 并发槽有限（`16/16`）→ 瞬态拥挤，几秒后重试。
- 推理模型（glm-z1 / omni）吃 token 多，`max_tokens` 要给足（≥1024），否则工具调用会被截断。
