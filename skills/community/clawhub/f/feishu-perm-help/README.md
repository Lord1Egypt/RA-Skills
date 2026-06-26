# feishu-perm-helper

一键启用飞书权限管理工具，让 OpenClaw 可以管理飞书文档/表格的协作者权限。

## 🎯 功能

- ✅ 自动启用 `feishu_perm` 工具
- ✅ 支持添加/查看/移除协作者
- ✅ 提供常用命令示例

## 📦 安装

```bash
clawhub install feishu-perm-helper
```

安装完成后自动启用，无需额外配置。

## 🚀 使用

### 添加协作者

在飞书里对机器人说：

```
给这个表格添加编辑权限
https://xxx.feishu.cn/base/XXX
用户：ou_xxxxxxxxxxxx
```

### 查看协作者列表

```
查看这个表格的协作者
https://xxx.feishu.cn/base/XXX
```

### 移除协作者

```
移除 XX 的编辑权限
https://xxx.feishu.cn/base/XXX
用户：ou_xxxxxxxxxxxx
```

## 📝 权限说明

**权限级别：**
- `view` - 只读
- `edit` - 可编辑
- `full_access` - 可管理

**支持的文档类型：**
- `bitable` - 多维表格
- `docx` - 云文档
- `sheet` - 在线表格
- `folder` - 文件夹

## 🆘 故障排查

### 工具未启用

```bash
openclaw gateway status
```

应该看到：`feishu_perm: Registered feishu_perm tool`

### 权限不足

确保飞书应用是表格的协作者（可管理权限）。

## 📄 许可证

MIT License
