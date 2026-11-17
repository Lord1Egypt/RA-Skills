<p align="center">
<a href="README.md">English</a> | <b>简体中文</b> | <a href="https://docsor1212.github.io/aesthete-agent/">在线演示</a>
</p>

# aesthete-agent

**给 AI 用的、机械验证过的前端美学引擎。** 一个 Agent Skill（同时也是 MCP 服务器）：为 AI 规划、验证、导出配色系统——让代理不再交出紫渐变的 AI 味配色，而是交付能过 WCAG、扛得住色盲模拟、经得起评审的颜色方案。

```bash
npx skills add docsor1212/aesthete-agent   # 30 秒接入；另有 skillhub / clawhub / MCP uvx，见「安装」
```

别的工具给你的智能体"品味建议"。这个给它**闸门**：四道机械检查（对比度、三色盲模拟、AI 味检测、评分卡）全过才算交付——背后是 119 块实证色板库、五套整页布局配方、渲染实证的评审闭环。

[![install](https://img.shields.io/badge/install-npx%20skills%20add%20docsor1212%2Faesthete--agent-blue)](https://github.com/docsor1212/aesthete-agent)
[![license](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![palette library](https://img.shields.io/badge/palette%20library-119%20curated-orange)](#实证色板库)
[![tests](https://img.shields.io/badge/tests-125%20passing-brightgreen)](tests/)

## 为什么需要它

大模型配色差，是有可测量原因的：它把 hex 当文本操作；它向训练数据的中位数回退（前端教程的中位数是紫/靛蓝）；它看不见自己输出的颜色。`aesthete-agent` 用工程方式解决——**把品味外包给流程**：

- **实证色板库**：119 块精选色板，全部经过客观质量门过滤（明度平坦 → 拒收；无可读文字对 → 拒收；色盲碰撞 / AI 味签名 → 打旗）；
- **机械闸门**：每个决定都过闸——五维评分卡、精确 WCAG 2.2 边界（可选 APCA）、三色盲模拟、AI 味签名检测、渐变禁令（任何渐变 = P0 一票否决）、HTML 交付体检；
- **六步法**：宣言 → 语域核对 → 选库 → 角色化 → 验证 → 五镜自审，把"做好看"变成可复现管线；
- **偏好档案**：`profile.json` 从你每一次接受/否决中学习，被否的方向机械降权。

## 它渲染什么

下面每张图都是引擎的真实产出——OKLCH 角色派生、对比度过闸、色盲模拟、AI 味检查，然后渲染成完整场景。没有一张是手工挑色的。在线版：[视觉 showcase](https://docsor1212.github.io/aesthete-agent/demo/showcase.html)（30 个场景 × 精选色板）。

<table>
<tr>
<td width="50%"><img src="docs/img/showcase-mobile.png" alt="手机钱包场景"><br><sub><b>移动应用</b> — Bees &amp; Honey · 文字/底 5.6:1 AA</sub></td>
<td width="50%"><img src="docs/img/showcase-landing.png" alt="SaaS 落地页场景"><br><sub><b>SaaS 落地页</b> — 同一色板，浏览器外壳，3:1 强调口</sub></td>
</tr>
<tr>
<td width="50%"><img src="docs/img/showcase-dashboard.png" alt="数据仪表盘场景"><br><sub><b>仪表盘</b> — KPI 卡、图表柱、状态胶囊</sub></td>
<td width="50%"><img src="docs/img/showcase-ecom.png" alt="电商商品卡场景"><br><sub><b>电商</b> — Deep Space Blue · 60-30-10 强制执行</sub></td>
</tr>
<tr>
<td width="50%"><img src="docs/img/showcase-editorial.png" alt="杂志编辑页场景"><br><sub><b>杂志编辑页</b> — Lavender · 印刷级克制</sub></td>
<td width="50%"><img src="docs/img/showcase-hero.png" alt="视觉 showcase 页面"><br><sub><b>showcase 本身</b> — 30 个场景，一个引擎</sub></td>
</tr>
</table>

## 安装

**Agent Skill** — 任何兼容 skills 的代理（Claude Code、ZCode、Codex、Cursor、Gemini CLI）一行安装：

```bash
npx skills add docsor1212/aesthete-agent
```

**SkillHub**（国内最快，主力更新通道）：

```bash
skillhub install aesthete-agent --dir <你的 skills 目录>   # 如 ~/.claude/skills
```

或打开 [skillhub.cn/skills/aesthete-agent](https://skillhub.cn/skills/aesthete-agent)，点「安装到本地 Agent」。

**DeepSeek Harness 原生插件**（DSH 桌面版 / Web / TUI）——11 个原生工具直连捆绑引擎：

```bash
dsh plugin --profile web add github:docsor1212/dsh-aesthete-agent
```

**ClawHub**（国际注册表）：

**ClawHub**（国际注册表）：

```bash
npx clawhub install aesthete-agent
```

**MCP 服务器**（Claude Desktop、Cursor、任何 MCP 客户端）——引擎变 21 个可调用工具：

```bash
uvx aesthete-agent-mcp            # 来自 PyPI，零密钥
# 或：npx -y @smithery/cli install docsor1212/aesthete-agent-mcp --client claude
```

核心引擎纯 Python 标准库（离线可用、零密钥、零遥测）；图像取色可选装 Pillow；MCP 服务器的 FastMCP 为可选依赖。

## 30 秒上手

```bash
S="scripts/palette_forge.py"   # 在已安装的 skill 目录内
python "$S" match --brief "儿科临床教学页" --limit 6        # 按语域为实证库排序
python "$S" score --palette 264653,2A9D8F,E9C46A,F4A261,E76F51   # 五维评分卡 /20
python "$S" matrix --palette ... --method apca --recommend      # 全对对比度矩阵（APCA = WCAG 3 草案）
python "$S" semantic --count 8 --base 2A9D8F                    # 色盲安全的分类色
python "$S" visualize --palette ... --variants 3                # 10 个真实 UI 场景 + 变体对比
python "$S" report --palette ...                                # 全部闸门 → 一个 PASS/FAIL 裁决
python "$S" theme "素雅金窗" --format css                        # 命名主题包 → CSS token
python "$S" export --palette ... --format w3c                   # W3C Design Tokens JSON
python "$S" export --palette ... --format prompt                # 图像生成提示词块
python "$S" doctor                                              # 环境体检
```

完整方法（宣言 → 语域 → 选库 → 角色 → 验证 → 五镜自审）见 [SKILL.md](SKILL.md)；references 里每个任务都有 30 秒路由表。

## 里面有什么

| 领域 | 亮点 |
|---|---|
| 引擎（38 个子命令） | match/search/harmony/ramp/mutate/roles/score/contrast/blind/matrix/semantic/slop/themes/theme/export(w3c·context·css·tailwind·prompt)/card/showcase/visualize/report/critique/doctor/selftest/house/extract/directions/scene/scaffold/check-image/evidence/tokens/audit/chartpal/typescale/qc/narrate/exemplar/patch/loop |
| 实证色板库 | 119 块精选色板，带点赞分层、风格标签、闸门旗标 |
| 场景可视化 | 10 种真实前端场景 × 任意色板，明亮/暗色，`--variants` A/B 对比，`--svg` 槽位清单重着色 |
| 命名主题包 | 8 个主题（配色 + 字体 + 语气 + 适用域），全部有出处 |
| 质量闸门 | 退出码强制：评分卡、对比度、色盲碰撞、AI 味、HTML 体检（**渐变禁令：任何渐变 = P0**）、`report` 一键裁决聚合 |
| 偏好学习 | `profile.json` 被 match/score/lint 消费；裁决回写是铁律 |
| 测试 | 39 个自动化测试，含 WCAG 边界值（#767676=4.54 过 / #777777=4.48 拒）、APCA、W3C 导出 |

## 实证色板库

没有人能先验地知道"好看"——所以库的建设分三层过滤，各做各的：**人群信号**（社区公认榜单、点赞分层、跨页重复出现）、**客观质量门**（只拦客观坏掉的架构：明度平坦、无可读对；色盲碰撞与 AI 味打旗）、**上下文自审**（最终裁决在真实版式里、由你来做）。每一次拒收都记录实测原因。

## MCP 服务器

`mcp/` 把引擎包成 MCP 工具（JSON-RPC over stdio）。零密钥、零遥测；以自包含 wheel 发布——`server_data/` 内置引擎，`uvx aesthete-agent-mcp` 独立可用；另有纯标准库 stdio 兜底（`--stdio`），没有 FastMCP 也能跑。

| 工具 | 包装 |
|---|---|
| `palette_match` | 按 brief 排序实证库 |
| `palette_harmony` | OKLCH 谐和生成 |
| `palette_score` / `palette_report` | 五维评分卡 / 全闸 PASS-FAIL 裁决 |
| `palette_contrast` / `palette_matrix` | 对检查 / 全对矩阵（WCAG + APCA） |
| `palette_blind` / `palette_semantic` | 色盲模拟 / 色盲安全分类色 |
| `palette_slop` | AI 味签名检测 |
| `palette_visualize` | 10 场景渲染 + 变体 |
| `palette_themes` / `palette_theme` | 命名主题包 |
| `palette_export` | css / tailwind / w3c / context / prompt |

## 全平台可得

| 平台 | 句柄 | 链接 |
|---|---|---|
| GitHub（源） | [docsor1212/aesthete-agent](https://github.com/docsor1212/aesthete-agent) | 安装命令见上 |
| SkillHub（中文站） | [aesthete-agent](https://skillhub.cn/skills/aesthete-agent) | `skillhub install aesthete-agent` |
| ClawHub | [aesthete-agent](https://clawhub.ai/skills/aesthete-agent) | `npx clawhub install aesthete-agent` |
| PyPI（MCP） | [aesthete-agent-mcp](https://pypi.org/project/aesthete-agent-mcp/) | `uvx aesthete-agent-mcp` |
| Smithery（MCP） | [docsor1212/aesthete-agent-mcp](https://smithery.ai/server/docsor1212/aesthete-agent-mcp) | `npx -y @smithery/cli install ...` |
| 在线演示 | [GitHub Pages](https://docsor1212.github.io/aesthete-agent/) | showcase + 在线 visualizer |

## 许可

MIT
