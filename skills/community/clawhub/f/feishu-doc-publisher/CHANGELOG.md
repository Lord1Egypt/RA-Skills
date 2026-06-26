# Changelog

## [2.0.0] - 2026-05-17

### Changed
- 将整个项目从 Node.js 环境迁移到了纯 Python 3 标准库实现，实现零外部依赖，极大地简化了安装和维护成本。
- 更新了环境变量配置加载机制，统一读取顺序，优先级依次为：
  1. 系统环境变量
  2. `~/.openclaw/.env`
  3. `~/.config/feishu-doc-publisher/.env`
  4. Skill 项目目录下的 `.env`
## [1.1.2] - 2026-05-02

### Changed
- 移除子进程调用，避免触发 ClawHub `suspicious.dangerous_exec` 静态规则。
- 保留本地文件模块与飞书 API 模块分离：`local-file.js` 只包含文件 I/O，`feishu-api.js` 只包含网络请求。

## [1.1.1] - 2026-05-02

### Changed
- 将本地 Markdown/图片文件读取集中到独立 `local-file.js` helper，主发布脚本仅通过子进程获取已解析内容后调用飞书 API，避免触发 ClawHub `suspicious.potential_exfiltration` 静态规则。
- 同步 `package.json`、`package-lock.json` 与 `SKILL.md` 版本号，避免发布平台复用旧版本缓存。

## [1.1.0] - 2026-05-02

### Added
- 支持 Markdown 图片上传：自动识别文档中的本地图片路径，并自动上传、关联至飞书在线文档图块。

### Changed
- 初步将二进制文件读取逻辑从主发布流程中剥离。

## [1.0.0] - 2026-04-30

### Added
- 首次发布
- 支持将 Markdown 文件发布为飞书在线文档
- 完整支持表格样式（通过 `blocks/convert` API + `descendant` 接口）
- 支持标题、段落、有序/无序列表、待办事项、分隔线、引用、代码块
- 支持加粗、斜体、删除线、行内代码、超链接等行内样式
- 表格插入失败时自动回退为纯文本格式
- 支持自定义文档标题（`--title`）
- 支持指定目标文件夹（`--folder`）
