# Feishu Doc Publisher (飞书文档发布工具)

这是一个基于 Python 3 的 OpenClaw Skill 脚本工具，用于将本地的 Markdown 文件自动转换并发布为飞书在线文档（DocX）。

## 特性

- 🚀 **自动化发布**: 一键将 Markdown 转换为飞书在线文档。
- 📊 **复杂结构支持**: 完整支持 Markdown 表格、列表、代码块等复杂富文本结构。
- 🔐 **灵活的凭证管理**: 支持通过全局配置、项目本地配置或系统环境变量加载飞书应用凭证。
- 🛡️ **安全合规**: 代码结构经过优化，符合严格的静态安全分析标准。

本工具使用 Python 3 标准库编写，无需额外安装第三方依赖。

## 配置

本工具核心依赖飞书自建应用的 `FEISHU_APP_ID` 和 `FEISHU_APP_SECRET`，并支持可选的智能过户变量 `FEISHU_ADMIN`。你可以通过以下任一方式配置环境变量（优先级自下而上，当前工作区最高）：

1. **系统环境变量**: 
   直接在终端中导出相应的环境变量，或者通过上层环境传递。
2. **OpenClaw 全局配置**: 
   在 `~/.openclaw/.env` 文件中配置。
3. **工具专属全局配置**: 
   在 `~/.config/feishu-doc-publisher/.env` 文件中配置。
4. **Skill 目录配置**: 
   在当前工具代码根目录的 `.env` 文件中配置。
5. **当前工作区配置**: 
   在执行该工具的当前目录或上级工作区目录中的 `.env` 文件配置。

`.env` 文件格式如下：
```env
FEISHU_APP_ID=cli_xxxxxxxxx
FEISHU_APP_SECRET=xxxxxxxxxxxxxxxx
FEISHU_ADMIN=your_email@company.com  # 可选：用于发文后全自动过户文档所有权，默认为 APP 所有
```

## 用法

基本用法：
```bash
python3 scripts/publish.py <markdown_file_path>
```

指定自定义文档标题：
```bash
python3 scripts/publish.py <markdown_file_path> --title "你的自定义标题"
```

发布到指定的飞书知识库目录（需要提供 Folder Token）：
```bash
python3 scripts/publish.py <markdown_file_path> --folder <folder_token>
```

设置公开分享或组织内权限：
```bash
# 设置为组织内任何人可编辑（团队内部共享协作）
python3 scripts/publish.py <markdown_file_path> --share tenant-edit

# 设置为互联网任何人可读（外部公开分享）
python3 scripts/publish.py <markdown_file_path> --share public-read
```

彻底移交文档所有权（Transfer Owner）：
```bash
# 发布完成后立刻将文档 Owner 转移给指定的企业邮箱用户
python3 scripts/publish.py <markdown_file_path> --owner "email:your_name@company.com"
```
> **Tip**: 如果您不想每次都在命令行输入 `--owner`，您可以在任意生效的 `.env` 文件中配置统一的环境变量 **`FEISHU_ADMIN`**。
>
> 脚本会自动通过内容推断您的身份类型：
> - 包含 `@` 符号，自动按 `email` 邮箱移交。
> - 以 `ou_` 开头，自动按 `openid` 移交。
> - 其他情况，默认按内部 `userid` 工号移交。
> 
> ```env
> # 在 .env 中增加如下配置，即可实现发文后全自动过户！
> FEISHU_ADMIN=your_name@company.com
> ```

## 注意事项

- 本工具依赖飞书的 Open API，确保你的飞书应用已经开启了以下权限：
  - `docx:document`：用于读写新版文档的正文内容。
  - `drive:drive`：用于配置文档的分享权限（互联网可见）以及移交所有权。
- 在大量包含超大表格的 Markdown 文件转换中，脚本具备完善的自动重试和降级策略（回退为纯文本表格），以保证最终文档创建成功。
