# 国际化契约

design-guide 将 AIDE 使用的指令语言与命令行辅助工具的显示语言分开处理。

## 支持的语言

当前支持：

- `en`：英文（回退语言）
- `zh-CN`：简体中文

未知或不支持的值自动回退到 `en`。新增语言时，必须在 `locales/` 下增加完整资源，并在发布前通过翻译资源一致性测试。

## 语言解析顺序

CLI 工具按以下顺序决定语言：

1. 显式参数 `--locale en` 或 `--locale zh-CN`。
2. 环境变量 `F_DESIGN_LOCALE`。
3. 环境变量 `LC_ALL`。
4. 环境变量 `LANG`。
5. 回退到英文。

Shell 同步器支持相同的环境变量，也支持 `bash scripts/sync-aide.sh --locale zh-CN`。`detect-frontend-env.sh` 的结构化 Markdown key 有意保持英文，因为它的输出会作为 agent 的项目上下文被消费。

面向用户的回答默认跟随当前用户请求的语言，除非用户明确指定其他语言。本机偏好可以记录默认语言，但不能覆盖用户的显式要求。

## 输出稳定性

人类可读的帮助、状态和错误信息可以翻译。JSON 输出属于 API：字段名、枚举值和机器可读结构保持英文。JSON 内的人类可读错误文本可以保持英文以保证解析稳定，消费者应使用结构化字段做判断。

## 新增消息

先在英文资源中加入源字符串，再将同一 key 加入所有支持的语言资源。CLI 工具统一使用 `scripts/i18n.py`，不要再引入第二套翻译机制。缺失翻译会有意回退到英文源字符串。

## 验证

```bash
python3 -m unittest discover -s tests -q
python3 scripts/present-design.py --locale zh-CN --help
F_DESIGN_LOCALE=zh-CN python3 scripts/design-guide-doctor.py
```

不要把依赖语言的文本用作契约标识、fixture key、JSON 字段名、路由、选择器或文件路径。
