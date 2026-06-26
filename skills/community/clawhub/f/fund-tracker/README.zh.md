# 基金申购状态跟踪器

[English](./README.md)

使用 AKShare 跟踪基金申购状态、日限额、手续费，以及相对上次运行的变化。

## 快速安装

先安装 skill：

```bash
npx skills add alondotsh/alon-skills --skill fund-tracker
```

然后在安装后的 skill 目录中安装 Python 运行依赖：

```bash
pip install -r tools/requirements.txt
```

## 适用场景

适用于你想检查基金是否开放申购、是否限额、是否暂停申购，以及这些状态是否相对上次检查发生变化的场景。

这个 skill 面向基金申购状态跟踪，不用于股票或 ETF 市价分析。

## 功能说明

- 从 `tools/presets.json` 读取基金代码 preset。
- 通过 AKShare 的东方财富基金申购接口拉取状态。
- 与 `runtime/history_<preset>.json` 中的上次结果对比。
- 输出包含基金代码、简称、申购状态、日限额、手续费、净值和变化说明的 JSON。

## 使用方式

```bash
# 默认 preset
python3 tools/check.py

# 指定 preset
python3 tools/check.py dingtou

# 查看全部 preset
python3 tools/check.py list
```

## Preset 管理

基金列表通过 preset 组织，保存在 `tools/presets.json`：

```json
{
  "default": {
    "label": "汇丰QDII",
    "funds": ["006075", "050025", "016057", "016055", "016533", "016532"]
  }
}
```

每个 preset 都有独立的历史文件，保存在 `runtime/` 下。

## 安全边界

- 脚本依赖 AKShare 和上游东方财富数据源。
- 网络错误或上游字段变化会以 JSON error 返回。
- `runtime/` 是本地运行状态，不应提交。
- 输出仅供信息参考，不构成投资建议。

## 输出结果

命令输出 JSON，包含：

- `preset`
- `label`
- `missing_funds`
- `data`

每条 `data` 记录包含基金代码、简称、申购状态、日限额、手续费、最新净值和变化说明。

## 项目结构

| 路径 | 用途 |
|------|------|
| `SKILL.md` | Agent skill 指令 |
| `tools/check.py` | 基金状态检查脚本 |
| `tools/presets.json` | Preset 定义 |
| `tools/requirements.txt` | Python 依赖 |
| `runtime/history_<preset>.json` | 自动生成的本地历史 |
| `tests/test_check.py` | 单元测试 |

## 关于 Alon

这些公开 skills 来自 Alon 日常高频使用的真实工作流。

我长期看好 agent skills，也愿意和对 skill 制作感兴趣的人交流。

- GitHub：https://github.com/alondotsh
- ClawHub：https://clawhub.ai/u/alondotsh
- X：https://x.com/alondotsh
- 公众号：alondotsh
