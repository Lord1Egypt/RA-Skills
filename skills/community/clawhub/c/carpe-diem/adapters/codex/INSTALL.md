# Codex 适配

## 一键安装

```bash
bash install.sh --platform codex
```

或指定安装目标：

```bash
bash install.sh --platform codex --target ~/.codex/skills/carpe-diem
```

预览安装计划：

```bash
bash install.sh --platform codex --dry-run
```

脚本会自动检测是否在 Carpe Diem 项目根目录中运行；如果不是，则从 GitHub 下载后执行。

## 用户级安装

默认目标是 `~/.codex/skills/carpe-diem`。先在 Carpe Diem 源码目录生成计划：

```bash
python3 scripts/carpe_diem.py install plan --platform codex --json > /tmp/carpe-diem-install.json
```

检查输出中的 `source`、`target`、`version`、`files` 和 `fingerprint`。确认后执行：

```bash
python3 scripts/carpe_diem.py install apply --plan /tmp/carpe-diem-install.json --yes
python3 scripts/carpe_diem.py install verify --target ~/.codex/skills/carpe-diem
```

重启或新开 Codex 会话后，用“我想做一个项目，但没有头绪”触发。若当前 Codex 版本未自动发现用户 Skill，可直接要求它读取 `~/.codex/skills/carpe-diem/SKILL.md`。

目录和重启说明依据 OpenAI 的 [Agent Skills 仓库](https://github.com/openai/skills)。本机首次验证版本会记录在 `docs/internal-testing.md`。

## 卸载

卸载只会删除带有效安装回执、且安装后未被修改的副本：

```bash
python3 scripts/carpe_diem.py install uninstall --target ~/.codex/skills/carpe-diem --yes
```
