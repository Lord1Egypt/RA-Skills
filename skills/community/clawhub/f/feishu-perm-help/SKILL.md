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

或者手动安装：
```bash
cp -r feishu-perm-helper ~/.openclaw/workspace/skills/
```

## 🚀 使用

### 安装后自动启用

安装完成后，Skill 会自动修改配置文件并重启 Gateway。

### 手动启用（可选）

如果自动启用失败，可以手动执行：

```bash
node ~/.openclaw/workspace/skills/feishu-perm-helper/scripts/enable-perm-tool.js
```

### 使用命令

安装后，在飞书里对机器人说：

**添加协作者：**
```
给这个表格添加编辑权限
https://xxx.feishu.cn/base/XXX
用户：ou_xxxxxxxxxxxx
```

**查看协作者列表：**
```
查看这个表格的协作者
https://xxx.feishu.cn/base/XXX
```

**移除协作者：**
```
移除 XX 的编辑权限
https://xxx.feishu.cn/base/XXX
用户：ou_xxxxxxxxxxxx
```

## 📝 配置说明

### 配置文件位置

`~/.openclaw/openclaw.json`

### 需要添加的配置

```json
{
  "channels": {
    "feishu": {
      "tools": {
        "perm": true
      },
      "accounts": {
        "default": {
          "tools": {
            "perm": true
          }
        }
      }
    }
  }
}
```

### 需要的飞书应用权限

确保飞书应用有以下权限：
- `docs:permission.member:create` - 添加协作者
- `docs:permission.member:read` - 查看协作者
- `docs:permission.member:delete` - 移除协作者

这些权限在飞书开放平台默认已授予。

## 🆘 故障排查

### 工具未启用

检查 Gateway 日志：
```bash
openclaw gateway status
```

应该看到：
```
[plugins] feishu_perm: Registered feishu_perm tool
```

### 权限不足错误

确保：
1. 飞书应用有相关 API 权限
2. 应用是表格的协作者（可管理权限）

### 配置不生效

重启 Gateway：
```bash
openclaw gateway restart
```

## 📞 反馈

遇到问题或有建议，欢迎反馈！

## 📄 许可证

MIT License
