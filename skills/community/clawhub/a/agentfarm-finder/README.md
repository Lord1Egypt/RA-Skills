# agentfarm-finder

自动追踪 Twitter 上的 AI Agent 挖矿/farming 机会。

## 快速开始

```bash
# 手动运行
bash agentfarm.sh

# 查看结果
cat output/results_$(date +%Y-%m-%d).md
```

## 定时任务

已自动配置每天 16:00 运行，无需手动操作。

查看日志：
```bash
tail -f output/cron.log
```

## 修改配置

编辑 `agentfarm.sh` 顶部的配置变量。

详细文档见 [SKILL.md](SKILL.md)。
