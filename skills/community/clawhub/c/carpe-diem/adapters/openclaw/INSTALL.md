# OpenClaw 适配

## 一键安装

```bash
bash install.sh --platform openclaw
```

或指定安装目标：

```bash
bash install.sh --platform openclaw --target ~/.openclaw/skills/carpe-diem
```

预览安装计划：

```bash
bash install.sh --platform openclaw --dry-run
```

脚本会自动检测是否在 Carpe Diem 项目根目录中运行；如果不是，则从 GitHub 下载后执行。

## 用户级安装

默认目标是 `~/.openclaw/skills/carpe-diem`：

```bash
python3 scripts/carpe_diem.py install plan --platform openclaw --json > /tmp/carpe-diem-install.json
python3 scripts/carpe_diem.py install apply --plan /tmp/carpe-diem-install.json --yes
python3 scripts/carpe_diem.py install verify --target ~/.openclaw/skills/carpe-diem
```

新开 OpenClaw 会话后，用“我想开始一个项目，但还没有方向”触发。项目或工作区级使用时，可通过 `install plan --target` 把同一 Skill 快照放入对应工作区的 `skills/carpe-diem`。

Carpe Diem 不读取 OpenClaw 的其他工作区内容，除非用户在对话中明确批准目标和只读范围。

目录优先级依据 OpenClaw 官方的 [Skills 文档](https://docs.openclaw.ai/skills)。OpenClaw 也提供 `openclaw skills install ./path/to/skill`；Carpe Diem 自带安装器的价值是先生成可审阅快照计划，并以回执限制卸载范围。

## 卸载

```bash
python3 scripts/carpe_diem.py install uninstall --target ~/.openclaw/skills/carpe-diem --yes
```
