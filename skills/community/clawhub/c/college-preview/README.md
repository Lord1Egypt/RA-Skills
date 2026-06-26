# OpenClaw 助学——大学课程 20 天期末冲刺

这是重构后的 skill 文件夹版本。该版本保留了原有核心功能，但重新按“大学课程期末冲刺”的真实业务流程进行分层，不再沿用 school skill 的原始模块命名方式。

## 文件结构

- `SKILL.md`：总入口与模块调用说明
- `_meta.json`：skill 基础元数据
- `setup_profile.md`：首次建档与冲刺档案生成
- `study_scheduler.md`：20 天计划、每日任务、小测与局部调整
- `daily_coach.md`：每日讲解、例题、提示与输出风格
- `progress_tracker.md`：进度面板、日记录、节奏提醒与动态调整
- `policy_guard.md`：学术规范与使用边界

## 相比旧版本的变化

1. 删除 `.idea/` 工程文件；
2. 删除 `ADAPTATION_MAP.md`，避免保留改编痕迹；
3. 将 `by-age.md` 合并进 `daily_coach.md`；
4. 将 `motivation.md` 合并进 `daily_coach.md` 与 `progress_tracker.md`；
5. 将 `curriculum.md` 与 `exams.md` 的核心职责重组为 `setup_profile.md` 与 `study_scheduler.md`；
6. 将 `parents.md` 改造成更贴合业务含义的 `progress_tracker.md`；
7. 将 `safety.md` 改名为 `policy_guard.md`。
