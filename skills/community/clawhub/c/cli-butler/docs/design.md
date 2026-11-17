# 架构草案（实现会话按此展开，可修订但须回写本文档）

## 布局

```
SKILL.md            agent 入口：触发词、六功能用法、安全红线（英文）
bin/list.sh         F1  盘点全部 CLI
bin/manage.sh       F2  info / outdated / upgrade
bin/install.sh      F3  渠道路由安装 + journal 回写
bin/uninstall.sh    F4  渠道卸载 / manual 安全卸载（dry-run 默认）
bin/refchain.sh     F5  五层引用链 + last-used
bin/cap.sh          F6  功能枚举
lib/common.sh       渠道探测、journal 读写、归属判定、输出格式
tests/run.sh        fixtures 冒烟
```

## 公共约定

- 出口协议：人读表格到 stdout；`--kv` 出 `key=value` 行供 agent 解析；错误走 stderr + exit≠0。
- 渠道探测全部包 `timeout`（无 timeout 命令的平台降级），单渠道失败不阻塞整体。
- 归属判定顺序、journal 格式见 [provenance.md](provenance.md)。
- 危险操作（卸载、覆盖安装）一律先 dry-run 输出计划动作，`--yes` 或交互确认才执行。

## 实现顺序

F1 → F5 → F6 → F3 → F4 → F2（盘点与引用链是其余功能的地基）。
