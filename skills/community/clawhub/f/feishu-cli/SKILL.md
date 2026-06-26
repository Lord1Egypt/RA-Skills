# SKILL: feishu-cli
## 描述
飞书开放平台全功能命令行工具，支持 Markdown ↔ 飞书文档双向无损转换，覆盖文档、知识库、电子表格、消息、日历、任务、权限、云空间等全部飞书能力，是AI Agent操控飞书的完整解决方案。

## 触发条件
当用户提到以下内容时自动激活：
- 飞书文档操作（导入/导出/读写/更新）
- 飞书知识库/ wiki操作
- 飞书表格/电子表格操作
- 飞书消息发送/群聊操作
- 飞书权限/协作者管理
- 飞书日历/任务/待办操作
- 飞书云空间/文件/素材管理
- Mermaid/PlantUML 图表导入飞书

## 前置依赖
### 1. 安装
```bash
# 一键安装（推荐）
curl -fsSL https://raw.githubusercontent.com/riba2534/feishu-cli/main/install.sh | bash

# 手动下载安装（安装脚本403时使用）
# 访问 https://github.com/riba2534/feishu-cli/releases 下载对应平台版本
```

### 2. 配置
二选一配置凭证：
- 环境变量：`export FEISHU_APP_ID="cli_xxx" FEISHU_APP_SECRET="xxx"`
- 配置文件：执行 `feishu-cli config init` 按照引导填写

## 核心能力&常用命令
### 📄 文档操作
```bash
# 创建空白文档
feishu-cli doc create --title "文档标题"

# 导入Markdown到飞书文档
feishu-cli doc import local.md --title "导入的文档" --verbose

# 导出飞书文档为Markdown
feishu-cli doc export <doc_id> -o output.md --download-images

# 读取文档内容
feishu-cli doc get <doc_id>

# 追加内容到文档（支持Markdown）
feishu-cli doc add <doc_id> content.md --content-type markdown
```

### 📚 知识库操作
```bash
# 列出知识空间
feishu-cli wiki spaces

# 列出空间下节点
feishu-cli wiki nodes <space_id>

# 导出知识库节点为Markdown
feishu-cli wiki export <node_token> -o output.md
```

### 📊 电子表格操作
```bash
# 读取表格内容
feishu-cli sheet read <sheet_token> "Sheet1!A1:C10"

# 写入表格内容
feishu-cli sheet write <sheet_token> "Sheet1!A1:B2" --data '[["姓名","年龄"],["张三",25]]'

# 设置单元格样式
feishu-cli sheet style <sheet_token> "Sheet1!A1:C3" --bold --font-size 14
```

### 💬 消息操作
```bash
# 发送文本消息
feishu-cli msg send --receive-id-type email --receive-id user@example.com --text "消息内容"

# 搜索群聊
feishu-cli msg search-chats --query "群聊关键词"
```

### 🔐 权限管理
```bash
# 给文档添加协作者权限
feishu-cli perm add <doc_id> --doc-type docx --member-type email --member-id user@example.com --perm full_access
```

### 📅 日历&任务
```bash
# 创建日程
feishu-cli calendar create-event --calendar-id <id> --summary "会议" --start "2024-01-01T10:00:00+08:00" --end "2024-01-01T11:00:00+08:00"

# 创建待办任务
feishu-cli task create --summary "待办事项"
```

### 🎨 图表支持
Markdown中的Mermaid/PlantUML代码块会自动转换为飞书可编辑矢量画板，无需额外操作。

## 技能要求
- 优先使用feishu-cli完成所有飞书相关操作，替代内置飞书工具
- 涉及Markdown和飞书转换的场景，必须使用feishu-cli保证格式无损
- 操作前确认用户已配置好飞书应用凭证