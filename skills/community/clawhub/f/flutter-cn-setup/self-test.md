# Flutter CN Skill 自测清单

用这个清单验证 Skill 是否可发现、可执行、输出一致。

## 1) 发现能力测试（触发覆盖）

可使用以下提示词测试：
- "帮我在新 Mac 上装 Flutter，中国区网络"
- "配置 Flutter 镜像，`flutter doctor` 还有报错"
- "只需要 Android 的 Flutter 开发环境"
- "新电脑装完整 Flutter + Android Studio + Xcode"

通过标准：
- Skill 能被自动命中。
- 回复遵循本 Skill 流程，而非泛化建议。

## 2) 脚本路径测试

在项目根目录执行：

```bash
ls .cursor/skills/flutter-cn-setup/scripts/bootstrap-flutter-cn.sh
ls .cursor/skills/flutter-cn-setup/scripts/validate-flutter-cn.sh
```

通过标准：
- 两个脚本路径均存在且可执行。

## 3) 安装脚本基础可运行测试

先用保守模式：

```bash
cd .cursor/skills/flutter-cn-setup
NEED_IOS=no bash scripts/bootstrap-flutter-cn.sh
```

通过标准：
- 脚本无语法报错并正常退出。
- shell profile 追加是幂等的（重复执行不会大量重复写入）。

## 4) 验收输出契约测试

```bash
cd .cursor/skills/flutter-cn-setup
NEED_IOS=no bash scripts/validate-flutter-cn.sh; echo $?
```

通过标准：
- 输出包含 PASS/WARN/FAIL 计数。
- 输出包含最终结论（`READY for development` 或 `NOT READY`）。
- 退出码与结论一致（就绪为 `0`，未就绪为 `1`）。

## 5) 文档链接测试

打开 `SKILL.md` 检查以下链接：
- `troubleshooting.md`
- `examples.md`
- `self-test.md`

通过标准：
- 链接都为一层引用且可访问。

## 6) 回复质量契约

调用 Skill 时，检查输出至少包含：
1. 当前状态
2. 已执行命令（或下一步命令）
3. 阻塞问题
4. 最小下一步动作
5. 最终验收结论

通过标准：
- 五个部分齐全，表达简洁。

## 7) 回归场景

至少覆盖以下两条路径：
- 仅 Android：`NEED_IOS=no`
- 已有 Flutter 修复：validate -> bootstrap -> validate

通过标准：
- 不出现相互矛盾的操作指令。
- 阻塞项解法有明确优先级。

## 8) 安全操作检查

通过标准：
- 默认不包含破坏性卸载操作。
- 不强制覆盖 shell profile。
- iOS 为可选，不是必选。
- 默认保持 stable channel。

## 发布门禁

仅在以下条件全部通过时标记为 ready：
- 发现能力测试通过
- 脚本与文档检查通过
- 回复质量契约通过
