# script-optimizer

纯自动化脚本质量优化器。验证 `script.json` 质量，自动修复模板默认值、角色匹配、运镜兼容等已知问题。

## 入口

```bash
# 方式 A：直接运行模块（推荐）
python3 scripts/optimize/__init__.py --project <项目目录> [选项]

# 方式 B：通过 project-generate 统一入口
python3 scripts/project-generate/project_generate.py --project <项目目录> optimize
```

## 调用方式

| 模式 | 命令 |
|------|------|
| 全自动 | `python3 scripts/optimize/__init__.py --project <项目目录>` |
| strict + force | `python3 scripts/optimize/__init__.py --project <项目目录> --strict --force` |
| JSON 输出 | `python3 scripts/optimize/__init__.py --project <项目目录> --strict --json` |
| 预览 | `python3 scripts/optimize/__init__.py --project <项目目录> --dry-run` |
| 仅报告 | `python3 scripts/optimize/__init__.py --project <项目目录> --report-only` |
| 修复 prompt | `python3 scripts/optimize/__init__.py --project <项目目录> --fix-prompts` |
| 同步类型配置 | `python3 scripts/optimize/__init__.py --project <项目目录> --sync-type` |

## 修复清单

| 修复项 | 说明 |
|--------|------|
| gender | 从 build/aura/personality 关键词推断 |
| aesthetic_style | 从类型配置注入 |
| distinctive_mark | 从 hair + face_details + color_scheme 自动构建 |
| face_details | 从 face 文本中按关键词提取 |
| camera_movement | 按 shot_type 填充默认运镜 |
| description | 从 prompt 截取 |
| duration_seconds | 字符串→int 类型修正 |
| reference_images | 从 shot_groups + character_cards 重建 |
| scene lighting/mood | 从 time_of_day 推断 |
| shot_groups | 删除孤儿引用，未分组 shot 创建新组 |
| characters 去重 | 独立检测并移除 characters 列表中的重复项 |
| 全局字段 | 从类型 .md 注入缺失字段 |
| 运镜兼容 | 清除互斥组合（仰+俯、拉+推等） |
| 泛称代词 | 检测「猫」「狗」「他」「她」等并替换为角色名 |

## 验证维度

P0 — 阻塞资产生成（模板占位符残留、description 过短、必填字段缺失等）
P1 — 建议修复（strict 模式下阻塞）
P2 — 消息（camera_movement 未设置、face_details 默认值等）

## 与 project-generate 集成

```python
from optimize import OptimizerV2
opt = OptimizerV2(project, strict=True, json_mode=True)
result = opt.run()
```
