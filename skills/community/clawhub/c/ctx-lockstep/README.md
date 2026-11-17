# ctx-lockstep

基于**文件**的长期项目上下文管理 OpenClaw skill。「lockstep（同步步进）」：项目的进入/退出/恢复/固化需要步调一致地同步上下文，避免会话中断后状态丢失。

- **GitHub**: https://github.com/holdyounger/ctx-lockstep
- **ClawHub**: https://clawhub.ai/skills/ctx-lockstep

## 特性

- **单目录收敛**：项目状态全部收进 `<项目>/.ctx-lockstep/`，不再在项目根目录平铺多个 md 文件（尊重仓库整洁与个人隐私习惯；可选 commit 或 gitignore）
- **事件驱动的漂移检测**（不依赖心跳、不依赖模型自觉、无常驻进程）：
  - git 项目 → post-commit hook 机械地把每次 commit 追加到 `commits.log`，固化时清空；积压行数 = 未固化提交数
  - 非 git 项目 → mtime 扫描（排除 node_modules/build 等噪声，阈值 = 上次固化时间戳），近似值
  - 检测发生在"进入/恢复项目"时，按需执行一次，token 成本≈0
- **固化轻量化**：小步进度只更新 `PROJECT.md` 单文件；仅阶段大节点才写 checkpoint 快照

## 项目结构

```
<项目>/.ctx-lockstep/
├── PROJECT.md          # 唯一恢复入口：主线/断点/决策/索引/固化记录
├── checkpoints/        # 阶段快照（YYYY-MM-DD-主题.md）
└── commits.log         # git 项目 hook 自动维护
```

## 快速使用

对 assistant 说：

- 「帮我接管这个项目目录」/「把这个目录纳入项目管理」→ 接管已有项目
- 「帮我建一个长期项目」→ 初始化新项目
- 「恢复项目」/「继续 ClipSense」→ 进入项目（自动跑漂移检测）
- 「固化当前项目」→ 保存断点

## 脚本

```bash
# 初始化 / 接管（自动装 git hook；非 git 项目自动走 mtime 模式）
python3 scripts/init_project.py '{"existing_path": "/path/to/project"}'
python3 scripts/init_project.py '{"projects_root": "/path/to", "project_name": "proj"}'

# 漂移检测（进入项目时执行）
python3 scripts/check_drift.py /path/to/project
```

## 目录说明

- `SKILL.md` — skill 主说明（工作流/规则/迁移指南）
- `scripts/init_project.py` — 初始化 + hook 安装
- `scripts/check_drift.py` — 漂移检测（git/mtime 双模式）
- `templates/` — PROJECT.md、PROJECT_SYSTEM.md、hook 文档等模板
- `docs/` — 补充说明（初始化测试、注册表维护、发布规范等）

## 发布建议

- 示例均为通用占位数据，不含真实路径
- 发布前过 `docs/发布规范.md` 检查清单
