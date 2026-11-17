# Hermes adapter（可选）

本目录是 **Hermes 专用适配**，不是通用核心。通用能力在仓库根目录 `scripts/` + `SKILL.md`。

把表情检索/入库挂进 Hermes 工具列表，避免模型用 `terminal` + `ls|shuf` 绕开。

## 文件

| 文件 | 工具名 |
|------|--------|
| `search_meme_tool.py` | `search_meme` |
| `add_meme_tool.py` | `add_meme` |

通过 skill 的 `scripts/` 加载 `meme_db.py` / `meme_embed.py`。路径环境变量与通用层相同（`MEME_*`，兼容 `HERMES_*`）。

## 安装

1. Skill 本体放到任意位置，或：

```bash
~/.hermes/skills/media/agent-expression/
```

2. 拷贝工具：

```bash
cp hermes-tools/search_meme_tool.py /path/to/hermes-agent/tools/
cp hermes-tools/add_meme_tool.py    /path/to/hermes-agent/tools/
```

3. 在 `toolsets.py` 加入 `"search_meme", "add_meme"`，重启 gateway。

也可设 `HERMES_MEME_SKILL_DIR` / `MEME_HOME` 指向 skill 根目录。

## 参数摘要

**search_meme**：`query`，可选 `tag`，`pick` 默认 true → `media_tag`  
**add_meme**：`image_path`，可选 `tag` / `dry_run` / `caption`

密钥放在 `$MEME_HOME/.env` 或 `~/.hermes/.env`，不要写进工具代码。

其他宿主请看 [../references/hosts.md](../references/hosts.md)，不要依赖本目录。
