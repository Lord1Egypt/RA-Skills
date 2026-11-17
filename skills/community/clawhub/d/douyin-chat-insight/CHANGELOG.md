## 0.2.1 — 2026-08-05

### Changed
- 可选链接 ASR 文档改为 **SiliconFlow 主路径**（推荐注册页 `https://cloud.siliconflow.cn/i/1srulim9` → 控制台建 Key）；百炼降为非抖音公网可选。核心路径仍零 Key。

## 0.2.0 — 2026-08-05

### Changed
- **正式改名**：`chat-value-insight` → **`douyin-chat-insight`**（Douyin Chat Insight / 抖音聊天转知识库）
- GitHub / ClawHub slug、文档、安装路径同步

### Note
- 0.1.x 旧 slug 不再作为主发布名；安装请用新 slug


### Fixed
- ClawHub 安装验收：fixture 多路径 + docs/examples 双份 + doctor 嵌入兜底；单测在市场精简包下 soft-pass
- sample_simple 加厚至 6 条，保证无 jsonl 时仍可 smoke

## 0.1.5 — 2026-08-04

## 0.1.4 — 2026-08-04

### Fixed
- ClawHub 打包会丢弃裸 `.jsonl` fixture：新增 `sample_group.chatlab.txt` 双份；loader 识别 chatlab 伪装扩展名
- doctor / 测试 fixture 自动回退

### Changed
- 安装验收以 ClawHub 全新 install + doctor READY 为准

# Changelog

## 0.1.3 — 2026-08-04 (release-hardening)

- 可选 ASR 端口说清：`references/optional-douyin-link-asr.md`；报告 `optional_enhancements`；核心仍零 Key
- `scripts/doctor.py` 一键体检（测试+smoke+无路径泄漏+无百炼依赖）
- 更强路径脱敏（家目录与数据盘等绝对路径）；load 错误信息 basename
- CLI `--version`；写报告目录失败友好错误；HTML inventory 标题中文
- 多文件目录 fixture + 测试扩到 doctor/version/multi_dir
- 发布清单与 INSTALL 对齐 doctor

0.1.2 — 2026-08-04

- Reasonix R2：CLI/JSON `report_paths` 脱敏；gate 覆盖 `数据盘绝对路径`；load 错误 basename
- 费用说明：`docs/REASONIX_COST.md`；R2 报告：`docs/REASONIX_REVIEW_R2.md`
- 测试 15/15

0.1.1 — 2026-08-04

### Reasonix 复核后修复（P0/P1/P2）
- **P0 隐私**: 报告/inventory 中 `source_path` 仅保留 basename（禁止 `家目录` `家目录` `数据盘绝对路径` 泄漏）
- **P0 配置**: `owner_aliases` YAML 读写修复（inline list + 多行 list）；setup 静默失效已解
- **P1 空导出门禁**: 全会话 0 有效消息 → QUALITY_GATE_FAIL
- **P1 友好错误**: 缺文件/坏格式/坏 --formats 不抛 Traceback
- **P1 纯文本时间戳**: `[YYYY-mm-dd HH:MM]` 写入 `Message.ts`
- **P1 latest 指针**: 切换 formats 时清理陈旧 latest.*
- **P2 矛盾**: 跳过同发送者极性伪矛盾
- **P2 动作 refs**: 优先 `msg:<id>`
- **P2 脱敏样例**: `docs/examples/sanitized_fixture_report.*`
- 测试: 14/14 通过；真导出 smoke 路径脱敏通过

### Reasonix
- 报告: `docs/REASONIX_REVIEW.md`（原始复核 + 闭环状态）

## 0.1.0 — 2026-08-04

- 首个可公开安装版本：独立 skill，零 IM 登录，零百炼强制依赖
- CLI：`setup.py` / `run.py` inventory→深挖状态机
- 输入：ChatLab JSONL / JSON / 纯文本
- 输出：单页 HTML + Markdown + JSON 四块报告
- 文档：INSTALL、GTM、how-to-get-exports、routing-boundaries
- 测试：fixture unittest
