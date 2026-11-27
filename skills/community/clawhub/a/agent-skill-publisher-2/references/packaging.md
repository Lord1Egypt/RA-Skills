# 打包和验证

## 环境和命令

工具需要 Python 3.10+ 与 PyYAML 6.x。可用 `python -m pip install 'PyYAML>=6,<7'` 在适当虚拟环境安装；已有 uv 时可用 `uv run --with 'PyYAML>=6,<7' python scripts/publish.py ...`。没有这些运行条件时可编辑文件，但不能声称已执行检查。依赖已安装后，所有打包与检查操作离线运行。

```text
python scripts/publish.py check /path/to/skill
python scripts/publish.py package /path/to/skill /path/to/standard.zip --profile standard
python scripts/publish.py package /path/to/skill /path/to/trae.zip --profile trae
python scripts/publish.py package /path/to/skill /path/to/folder.zip --profile folder
python scripts/publish.py package /path/to/skill /path/to/workbuddy.zip --profile workbuddy --metadata /path/to/market.json
python scripts/publish.py check /path/to/workbuddy.zip --profile workbuddy
python scripts/publish.py expert /path/to/config.json /path/to/agent-body.md /path/to/avatar.png /path/to/expert.zip --skill /path/to/skill
python scripts/publish.py check /path/to/expert.zip --profile expert
```

先复制 assets/expert-config.example.json 与 assets/expert-body.example.md 到项目工作目录，再替换作者、角色和技能入口。`--skill` 可重复提供多个目录；每个目录必须自包含。正文入口随实际内置技能修改，示例路径只适用于本技能。专家命令在输出内生成配置与 frontmatter，不要求先安装技能。

## 工具做什么

- 使用 YAML 安全解析并拒绝重复字段；检查命名、描述、版本和 WorkBuddy 元数据。
- 检查实际目录或 ZIP，防止绝对路径、上层跳转、符号链接、大小写冲突及 Windows 无法安全落盘的文件名。
- 保留二进制原字节和资源层级；WorkBuddy 技能 profile 对深层资源报错，不自动重命名。
- 校验常见 Markdown 内联本地链接；不覆盖所有 Markdown 引用形式、脚本动态路径或外部 URL 可用性。
- 生成可复现 ZIP，读取实际产物再次校验，输出 SHA256、文件数、入口及明确的未验证状态。不会执行被打包代码。
- WorkBuddy 专家交付须从实际 ZIP 核对 `avatar` 引用的图片；换图时还要与选定新图比对字节摘要。专家平台不能手动补传头像，不能把图片遗漏留给上传后处理，详见 [WorkBuddy 适配](workbuddy.md)。
- 拒绝输出位于源码目录内，避免把旧 ZIP 自己装进新 ZIP；默认拒绝覆盖现有产物，`--force` 仅适用于你确认需要替换的输出。
- 常见凭据文件和明显 Token 模式会阻止打包，只报告文件/规则，不打印值。它是有限检查，不能作为无敏感数据证明。

## 工具不做什么

不完整验证每个平台所有 schema；不转换任意工具 API；不自动安装、联网、运行代码或发布；不自动迁移有动态路径的深层资源；不证明头像内容适合审核。其图片检查读取 PNG/JPEG 尺寸和文件体积，不替代人工查看与解码检查。

## 应如何补充证据

在独立临时目录解压自己审查过的包；用实际运行时运行关键路径，确认模板、资源和相对引用仍有效。不要自动执行来历不明的技能自带测试。安装到正确客户端后检查发现、读取参考、脚本调用和输出；在线服务测试按当前授权进行。

公开验证报告至少包含源版本/commit、目标 profile、规则来源、实际 ZIP 哈希、通过/失败检查及未执行阶段。长文案与技能正文完整性都要检查，不只数文件。只有真实上传/调用完成后才更新对应状态。


## 指定头像和安装核对

`publish.py check expert.zip --profile expert --expected-avatar selected.png`核对包内引用的实际图片字节，尺寸合格但仍是旧图也会失败。报告含头像路径/尺寸/SHA256、专家版本、内置技能版本及清单存在时的build_id；隐藏plugin.json是专家版本来源，不强制专家与技能版本相同。

`verify_install.py release.zip installed-directory --profile expert`只读比较可信ZIP与选定目录。普通技能使用standard/workbuddy，外层技能文件夹包使用folder并指定安装后的技能根目录。缺失/变更文件返回1；额外文件单列，release_files_match=true不等于exact_file_set=true，也不代表运行客户端已加载该目录。工具不修复文件、不验证发行来源真实性。更新前先把已安装版本备份到发现目录以外。

报告与发行清单标记artifact_role及importable_workflow=false，不交给FastGPT/n8n当工作流导入。实际工作流、检查合同和报告应使用清楚的文件名。更换头像/专家上传版本时只做相应包检查；业务逻辑未变不要求重跑业务联调。
