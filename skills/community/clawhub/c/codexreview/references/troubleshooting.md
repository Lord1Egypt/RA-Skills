# 常见问题

## 没有找到 Codex 数据目录

先确认 Codex 已安装并至少完成过一次任务。使用自定义目录时，通过 `--codexHome` 指定：

```bash
node scripts/scan_usage.mjs --codexHome "/path/to/.codex"
```

## 工作区路径不存在

检查 `--workspace` 是否指向真实存在的目录。正常使用 skill 时，优先让 Codex 在当前工作区自动判断，不需要手工输入命令。

## 报告里的项目太少或归并不准

先确认扫描范围是否覆盖目标时间，再在工作区添加 `.codex-review.json`。配置方式见 [project-grouping.md](project-grouping.md)。

## Token 显示为 0 或明显偏低

部分旧会话或异常中断的会话可能没有 `token_count` 事件。报告仍可用于项目和 Prompt 复盘，但 Token 总量会偏低。

## 报告已生成但没有自动打开

先在命令输出中找到 HTML 路径并手动打开。macOS 的后台自动任务可能受到系统隐私权限限制；报告生成成功和浏览器打开失败是两件事。

## JSON 损坏或格式不完整

重新运行扫描，不要手工修补中间 JSON：

```bash
node scripts/scan_usage.mjs --workspace "/path/to/workspace" --output /tmp/codex_review_scan.json
```

## 页面内容为空

扩大时间范围，例如 `--days 14`。如果仍为空，检查 Codex 会话目录和工作区权限。

## 查看调试命令

```bash
node scripts/scan_usage.mjs --help
node scripts/build_report.mjs --help
node tests/run.mjs
```
