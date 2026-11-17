# Task: v0.1 实现与开源发布（无人值守）

- **负责人**: 本会话（pi, kelegele）
- **计划**: docs/superpowers/plans/2026-11-09-cli-butler-v0.1.md
- **目标**: 六功能实现（F1→F5→F6→F3→F4→F2）→ 验收 → 发布 GitHub `kelegele/cli-butler`
- **状态**: done — v0.1.0 已发布

## 预检结论（Task 0）

- 名字查重（2026-11-09）：npm E404 ✓ / GitHub 无同名 ✓ / skills.sh 零命中 ✓ → 定名 `cli-butler`，无需回退 toolbutler
- gh 已登录 kelegele（repo+workflow scope，https 协议）
- shellcheck 0.11.0 已装（/opt/homebrew/bin/shellcheck）

## 里程碑记录

- [x] T0 预检：查重 + shellcheck
- [ ] T1 测试夹具
- [ ] T2 common.sh 原语
- [ ] T3 channels.sh
- [ ] T4 F1 list
- [x] T5 F1 真机验证
  - 真机 `bin/list.sh --kv`：rc=0，2209 行，113s；human 输出分组 brew(706)/npm(9)/pipx(12)/uv(2)/gem(12)/system(1198)/untracked(233)，空组自动跳过
  - 性能改造三件：brew desc bulk 一次调用（原 151 包 × 1s）；whatis 预算（BUTLER_WHATIS_BUDGET，默认 20）+ AW_$name 缓存（key 需标识符消毒，@/-/点不可作变量名）；SEEN/JNAMES 用 case *"$LF$x$LF"* 零 fork 精确匹配（haystack 须 $LF 首尾垫护，$( ) 会剥尾 LF——曾致去重失效 3 连 fail）；realpath_safe 目录规范化 DIRC_ memo + basename/dirname 参数展开去 fork
  - 教训：channel_desc 保持 printf API（测试 $( ) 消费），whatis 回退挪到 add_row 主 shell 层（BASHPID 探测子 shell 在 bash 3.2 不可用——无 BASHPID）；kv 行断言 ${x##*desc=} 会残留尾 TAB，先 ${x//[[:space:]]/}
- [x] T6 F5 refchain
  - commit bb6c99c；tests 47/47
  - 真机：docker 三跳软链链（/usr/local/bin/docker → OrbStack xbin/docker → docker-tools）、owner=brew|managed、last-used=1790066193 ✓；真机 ~/Library/LaunchAgents/ai.deepseek.dsh.web.plist.off 存在且 layer4 grep 机制命中 ✓（node 无 launchd 引用则不误报）
  - 夹具：refchain/bin l3→l2→l1→real/real-tool 三级软链；com.fake.brewsvc.plist 内容改为引用 loose-tool（原 brewsvc 引用对 refchain 用例无意义）；zsh_history 4 行含 l3/loose-tool epoch
  - 教训：layer3 匹配目录要用原始 path 的 dir（${p%/*}），chain walk 后 cur 已漂移到 realpath 目录；测试文件自带 JDIR 后必须重 source common.sh（JOURNAL 在 source 时定死）；macOS awk 对多字节垃圾历史内容会 towc 崩——hist_last_used 已加 LC_ALL=C
- [x] T7 F6 cap
  - commit be84368；tests 47/47；真机 cap git：usage 行 + clone/init/add… 子命令表提取 ✓
- [x] T8 F3 install
  - commit 540964e；tests 47/47；真机验证留待 T11 统一做（dry-run 全矩阵）
- [x] T9 F4 uninstall（进行中）
- [x] T10 F2 manage
- [x] T11 验收加固
- [x] T12 发布

## 证据

- Commits: 181dee1(T0) 2e689c4(T1) 4be4be1(T2) 6b4706a(T3) 41ea367(T4) 96dbd5c(T5 perf) bb6c99c(T6) be84368(T7) 540964e(T8) d9bcaa9(T9) 5d5f7a0+948ea70(T10) 380e5cc(T11)
- tests: 79 passed / 0 failed；shellcheck bin/*.sh lib/*.sh tests/lib.sh rc=0
- F1 真机（--kv 2208 行 139s）：docker brew|managed 70.6M desc 完整（OrbStack 软链）；node npm|managed（nvm）；rg manual|untracked（~/.kimi-code/bin）；分组 human 输出 brew(706)/system(1198)/untracked(233)
- F5 真机：refchain docker 三跳软链链→docker-tools realpath ✓ last-used ✓；ai.deepseek.dsh.web.plist.off 存在（(disabled) 旗标由 fixture 测试覆盖）
- F4 真机：uninstall docker → plan brew uninstall docker + dry-run 不执行；manual 临时项 --yes → 删除+journal 清+plist 挪 .off（fixture 覆盖）
- F2/F3 真机：info git → system|system（SIP 拒绝路径）；upgrade docker → plan brew upgrade docker；install dry-run 由测试覆盖
- outdated 真机：--channel brew rc=0（本机无过期项）；cargo → "not supported, not guessing" rc=1
- CI：run 42533195840 success（Ubuntu shellcheck + 全测试）；期间修两个 Linux 兼容问题：tests/run.sh SC1091/SC2181、bin/list.sh local 变量未初始化（bash 5 set -u 报 unbound）
- 发布：https://github.com/kelegele/cli-butler （public，topics: cli/agent-skills/package-manager/homebrew/bash）
- Release: https://github.com/kelegele/cli-butler/releases/tag/v0.1.0 （tag v0.1.0）
- skills.sh 解析验证：`npx skills add kelegele/cli-butler` 识别仓库并定位根目录 SKILL.md ✓

## v0.1.1 — function-view inventory（2026-11-09 完成）
- 需求：用户裁定渠道分组是管理视角，回答「装了什么」需按功能分类；做成确定性能力 `list --by-function`。
- 实现：lib/function.sh（11 条关键词规则：AI/Agent、移动开发、容器、版本控制、库依赖、Web、多媒体、语言运行时 + 系统兜底 + 其他兜底）；bin/list.sh --by-function（组键=功能，渠道降为行属性；--kv 不变）。
- 修复：tests/test_list.sh 重复 source lib.sh 导致 TESTS_PASS/FAIL 计数器复位，掩盖累计结果（真实总数 177，此前误报 79）；bin/list.sh usage 行补 --by-function；gpg-agent 测试 desc 含 ssh 误中 Web 规则（改 "agent protocol helper"）。
- 证据：tests 177 passed / 0 failed；shellcheck clean；CI run 42538027848 绿；真机 --by-function：AI 62 / 移动 18 / 容器 10 / VCS 20 / 库 67 / Web 15 / 多媒体 29 / 运行时 67 / 系统 1198 / 其他 724（rc=0）。
- 发布：release https://github.com/kelegele/cli-butler/releases/tag/v0.1.1 ；tag v0.1.1 已 push；~/.agents/skills/cli-butler 已 rsync 至 v0.1.1（非 git 副本，repo 更新后需手动重同步）。

## 边界修复采纳（2aa0ea5，2026-11-09）
- 并行会话踩坑产出经审查后择优采纳（版本号 0.1.2 抬升已拒绝并回退）：pipx 空态 banner 过滤、~/.local/bin 共享目录仅在 pipx/uv 有实装时认领（修卸载路由误派）、realpath_safe 键补 @ 转义、du_size 不可读文件 stderr 消音、humanize_size "-" 入参。配套 7 条新断言，测试总数 184。
- 真机证据：pipx 空态 banner 真实存在（"nothing has been installed with pipx 😴"）；webget 归 manual|untracked 而非误归 pipx。
- 教训：多会话并行同一仓库时，未提交的越界改动先审查再定去留；对外语义（版本号/发布）必须经指令授权。
