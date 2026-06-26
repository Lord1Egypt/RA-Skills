---
name: figma-desktop
description: "Figma 桌面 MCP Skill - 通过 Figma 桌面应用本地 MCP 服务访问完整功能，包括 Figma Make 设计生成、代码生成、设计系统管理等，无需 OAuth 认证"
---

# Figma 桌面 MCP Skill

通过 Figma 桌面应用内置的本地 MCP 服务器 (`http://127.0.0.1:3845/mcp`) 访问完整的 Figma 功能，包括 Figma Make、代码生成等高级特性。

## 核心优势

- ✅ **无需 OAuth** - 通过 Figma 桌面应用自动认证
- ✅ **完整功能** - 支持 Figma Make、代码生成、Code Connect
- ✅ **本地运行** - 低延迟，数据不经过第三方服务器
- ✅ **实时同步** - 与 Figma 桌面应用实时同步选择和状态

## 前置要求

### 1. 安装 mcporter

mcporter 是连接 MCP Server 的必需工具：

```bash
# 使用 npm 安装
npm install -g mcporter

# 验证安装
mcporter --version
```

### 2. 安装 Figma 桌面应用（最新版本）

- 下载地址：https://www.figma.com/downloads/
- 确保更新到最新版本

### 3. 启用 MCP 服务器

- 打开任意 Figma 设计文件
- 切换到 Dev Mode（开发模式）
- 在右侧面板启用 MCP server
- 复制服务器地址（默认 `http://127.0.0.1:3845/mcp`）

### 4. 保持 Figma 运行

- MCP 服务器随 Figma 桌面应用启动
- 关闭 Figma 后 MCP 服务不可用

## 配置步骤

### 步骤 1：安装 Figma 桌面应用

```bash
# macOS (使用 Homebrew)
brew install --cask figma

# 或从官网下载
# https://www.figma.com/downloads/
```

### 步骤 2：在 Figma 中启用 MCP

1. 打开 Figma 桌面应用
2. 打开或创建一个设计文件
3. 点击工具栏的切换开关，进入 **Dev Mode**（开发模式）
4. 在右侧面板找到 **MCP server** 选项
5. 点击启用 MCP server
6. 点击 **Copy URL** 复制服务器地址

### 步骤 3：配置 mcporter

```bash
# 添加 Figma 桌面 MCP（已预配置）
mcporter config add figma-desktop --url http://127.0.0.1:3845/mcp --transport http
```

### 步骤 4：验证连接

```bash
# 测试连接（需要在 Figma 中打开设计文件）
mcporter list figma-desktop
```

## 使用方法

### 基本命令

```bash
# 列出可用工具
mcporter list figma-desktop

# 调用工具
mcporter call figma-desktop.<tool-name> --param value
```

### Figma Make 功能（设计生成）

```bash
# 生成设计建议
mcporter call figma-desktop.make_suggest_layout '{"description": "登录页面", "width": 375}'

# 从描述生成组件
mcporter call figma-desktop.make_generate_component '{"description": "带图标的主按钮"}'

# 优化选中设计
mcporter call figma-desktop.make_optimize '{"goal": "提高可访问性对比度"}'
```

### 代码生成

```bash
# 生成 React 组件（基于 Figma 中的选择）
mcporter call figma-desktop.generate_code '{"framework": "react", "typescript": true}'

# 生成 Vue 组件
mcporter call figma-desktop.generate_code '{"framework": "vue"}'

# 生成 CSS/Tailwind
mcporter call figma-desktop.generate_code '{"framework": "css", "tailwind": true}'

# 生成 React Native
mcporter call figma-desktop.generate_code '{"framework": "react-native"}'
```

### 获取设计上下文

```bash
# 获取当前选中的设计节点
mcporter call figma-desktop.get_selection

# 获取选中节点的样式信息
mcporter call figma-desktop.get_styles '{"nodeId": "NODE_ID"}'

# 获取设计变量
mcporter call figma-desktop.get_variables

# 获取组件信息
mcporter call figma-desktop.get_component '{"componentKey": "KEY"}'
```

### Code Connect 集成

```bash
# 获取组件代码连接
mcporter call figma-desktop.code_connect_get '{"componentId": "ID"}'

# 同步代码到设计
mcporter call figma-desktop.code_connect_sync
```

### 文件操作

```bash
# 获取当前文件信息
mcporter call figma-desktop.get_current_file

# 获取文件结构
mcporter call figma-desktop.get_file_structure

# 获取页面列表
mcporter call figma-desktop.get_pages
```

## 使用场景示例

### 场景 1：从设计生成代码

1. 在 Figma 桌面应用中打开设计文件
2. 选中要生成代码的框架/组件
3. 在 OpenClaw 中执行：

```bash
mcporter call figma-desktop.generate_code '{"framework": "react", "typescript": true, "includeStyles": true}'
```

### 场景 2：AI 辅助设计（Figma Make）

1. 在 Figma 中创建新页面
2. 在 OpenClaw 中描述需求：

```bash
mcporter call figma-desktop.make_suggest_layout '{"description": "电商商品详情页，包含图片轮播、价格、购买按钮", "width": 1440}'
```

### 场景 3：设计系统同步

```bash
# 获取组件库
mcporter call figma-desktop.get_component_library

# 获取样式定义
mcporter call figma-desktop.get_style_definitions

# 同步到代码
mcporter call figma-desktop.sync_design_system
```

## 故障排除

### "MCP server is only available if your active tab is a design or FigJam file"

**原因**：Figma 中没有打开设计文件

**解决**：
1. 在 Figma 桌面应用中打开任意设计文件
2. 确保处于 Dev Mode
3. 确保 MCP server 已启用

### "Connection refused" 或 "Cannot connect"

**原因**：MCP 服务器未运行

**解决**：
1. 检查 Figma 桌面应用是否正在运行
2. 在 Figma 中重新启用 MCP server
3. 检查端口是否正确（默认 3845）

### 工具调用返回空结果

**原因**：Figma 中没有选中任何元素

**解决**：
1. 在 Figma 中选中要操作的框架或组件
2. 再次调用工具

### 代码生成功能不可用

**原因**：需要 Dev Mode 权限或特定文件访问权限

**解决**：
1. 确保文件有编辑权限
2. 检查是否处于 Dev Mode
3. 确保文件不是只读模式

## 注意事项

1. **Figma 必须保持运行**
   - MCP 服务器是 Figma 桌面应用的一部分
   - 关闭 Figma 后所有 MCP 调用都会失败

2. **需要打开设计文件**
   - 大多数工具需要在 Figma 中打开文件才能工作
   - 部分工具需要选中特定元素

3. **Dev Mode 要求**
   - 某些高级功能需要处于 Dev Mode
   - 确保有文件的编辑权限

4. **网络要求**
   - 虽然是本地服务器，但仍需要网络连接 Figma 服务
   - 防火墙不能阻止 localhost:3845

5. **版本兼容性**
   - 确保 Figma 桌面应用是最新版本
   - MCP 功能在旧版本中可能不可用

## 与第三方 MCP 对比

| 特性 | figma-desktop (推荐) | figma-mcp (第三方) |
|------|---------------------|-------------------|
| Figma Make | ✅ 完整支持 | ❌ 不支持 |
| 代码生成 | ✅ 完整支持 | ⚠️ 基础支持 |
| 认证方式 | 自动（通过桌面应用） | API Token |
| 需要 Figma 桌面 | ✅ 必须 | ❌ 不需要 |
| Code Connect | ✅ 支持 | ❌ 不支持 |
| 实时选择同步 | ✅ 支持 | ❌ 不支持 |

## 相关链接

- Figma 桌面应用下载：https://www.figma.com/downloads/
- Figma MCP 文档：https://developers.figma.com/docs/figma-mcp-server/
- Figma Make 介绍：https://www.figma.com/blog/introducing-figma-mcp-server/
- Code Connect 文档：https://developers.figma.com/code-connect/
