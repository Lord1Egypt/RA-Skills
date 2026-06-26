# 08 渲染 HTML

## 脚本

```bash
python3 scripts/render_daily.py output/daily/{date}.json --output output/daily/{date}.html --force
```

## 作用

将日报 JSON 渲染为 HTML 页面。

## 输入

- `output/daily/{date}.json` — 经过 validate_payload.py 校验通过的日报 JSON

## 输出

- `output/daily/{date}.html` — 日报 HTML 页面
- `output/archive/{date-hour-min}.html` — 旧版本自动归档（如果已存在 HTML）

## 页面结构

- 顶部 header：日期、角色
- 左侧栏：速览（overview）、行动建议（actions）、趋势雷达（trends）
- 右侧：文章卡片流（articles），按 priority 排列
- 页脚：数据来源（data_sources）

## 参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| 第一个参数 | — | 输入 JSON 文件路径（必填） |
| `--output` | 同 input 路径改 .html | 输出 HTML 文件路径 |
| `--force` | false | 即使时间窗口校验有警告也继续渲染 |

## 时间窗口校验

渲染器会自动检查每条 article 的 `source_date` 和 `time_label` 是否在 3 天窗口内。超出窗口的会输出警告：

```
⚠️ 时间窗口校验警告：
  [article-3] source_date 2026-04-02 超出窗口（2026-04-03 ~ 2026-04-05）
```

- 不加 `--force`：有警告会阻止渲染
- 加 `--force`：输出警告但继续渲染

建议：如果是跨天发酵的事件（如 Gemma 4 从 4 月 3 日持续到 4 月 6 日），用 `--force` 跳过。

## 视觉基线

HTML 样式参考 `reference/daily_example.html`。修改页面风格需先改这个基线文件再同步渲染器。

## 完整命令示例

```bash
DATE=$(date +%Y-%m-%d)

# 标准渲染
python3 scripts/render_daily.py output/daily/$DATE.json --output output/daily/$DATE.html

# 强制渲染（跳过时间窗口警告）
python3 scripts/render_daily.py output/daily/$DATE.json --output output/daily/$DATE.html --force
```
