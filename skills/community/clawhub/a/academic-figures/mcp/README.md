# academic-figures-mcp

41 种投稿级学术图型的 MCP Server（FastMCP，数量随引擎注册表自动增长）：bar/line/km（含竞争风险）/forest/roc/slope/composite/prisma…，
本地确定性渲染（同输入同字节）、中文零配置、数据校验+渲染看门狗+退出码语义全继承自
[academic-figures](https://github.com/docsor1212/academic-figures) 引擎。

**边界**：纯本地渲染（零密钥/零遥测/零计费）；600dpi 成品落盘本地路径，MCP 回传仅 ≤150dpi 预览。

## 安装

```bash
# 本地安装（推荐，不访问 GitHub）：clone 或下载包后——
pip install -e <包目录>/mcp   # pip 可走清华/阿里镜像
uvx --from <包目录>/mcp academic-figures-mcp

# uvx git 直跑（国际网络备选）：
uvx --from "git+https://github.com/docsor1212/academic-figures#subdirectory=mcp" academic-figures-mcp

# 或本地路径
cd academic-figures/mcp && pip install . && academic-figures-mcp
```

## 客户端配置

Claude Code / Claude Desktop（`claude_desktop_config.json`）：

```json
{
  "mcpServers": {
    "academic-figures": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/docsor1212/academic-figures#subdirectory=mcp", "academic-figures-mcp"]
    }
  }
}
```

Cursor（`~/.cursor/mcp.json`）：同上结构。

Codex：`codex mcp add academic-figures -- uvx --from "git+https://github.com/docsor1212/academic-figures#subdirectory=mcp" academic-figures-mcp`

## Tools

| tool | 说明 |
|---|---|
| `render_chart` | 全图型渲染（随引擎注册表，当前 41 种）：`chart` + `data`（JSON/CSV 文本）+ `options`（title/subtitle/source/xlabel/ylabel/theme/journal/column/verify/peak_label/summary…）+ `dpi`（72–600）+ `fmt`；回预览 base64 + 成品落盘路径；重叠检出返回 `overlap_detected`（修复机制，不交付） |
| `suggest_chart` | 数据驱动图型推荐 |
| `doctor` | 渲染前参数/环境体检（只体检不渲染） |
| `query_capability` | 查图型能力面：chart 留空=全注册表+旗标域速览；指定图型=专属/域外旗标详情（动态真值=引擎，防清单漂移） |

Resources：`capability://matrix`（全图型注册表×期刊预设）、`capability://changelog`。
Prompt：`chart_picker`（选图引导）。

## 边界

- 单次调用单图；data ≤ 2MB；dpi 72–600；预览 ≤150dpi；渲染超时 900s
- 需要本地 Python 环境（uvx 自动装依赖；中文字体走系统字体自动探测）
- 不含 Pro 云渲染/计费功能

## 开发

```bash
bash mcp/sync_engine.sh                        # trunk scripts/ → af_engine/ 镜像（sha 门禁）
python3 -m unittest discover -s mcp/tests -p "test_bounds.py"
python3 mcp/tests/e2e.py                       # 需 fastmcp + 引擎依赖
```
