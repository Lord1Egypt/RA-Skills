# 发现规则

`scripts/build_daily_json.py` 会在当前应用根目录里发现来源 Markdown。

## 文件匹配规则

- 递归扫描应用根目录内所有按 `YYYY-MM-DD.md` 日期格式命名的 Markdown 文件，例如 `2026-04-09.md`
- 以文件名中的日期作为“最新”的主排序键
- 不把文件修改时间当作“最新”的主定义

## 忽略目录

扫描时跳过以下目录：

- `.git`
- `.next`
- `.cache`
- `.venv`
- `venv`
- `node_modules`
- `dist`
- `build`
- `coverage`
- `tmp`

## 同日 tie-break 规则

如果最新日期下存在多个候选文件，按下面顺序选一个：

1. 更高的“日报路径相似度”分数
2. 更短的相对路径
3. 更新的修改时间
4. 字典序路径作为最后的稳定 tie-break

## 日报路径相似度

脚本会对包含下列片段的路径增加权重：

- `daily`
- `journal`
- `journals`
- `log` or `logs`
- `note` or `notes`

这些路径提示只用于同日 tie-break，不是硬性目录约定。
