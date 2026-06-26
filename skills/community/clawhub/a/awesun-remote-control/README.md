# 向日葵(Awesun) Skill

基于[向日葵MCP服务](https://github.com/OrayDev/awesun-mcp)，为Claude Code、Open Code、🦞OpenClaw等支持Skills的AI Agent提供渐进式披露的工具调用。

***⚠️配置Skill前请安装符合版本向日葵客户端，并启用向日葵MCP服务，详见：[https://github.com/OrayDev/awesun-mcp](https://github.com/OrayDev/awesun-mcp)***

***⚠️本Skill依赖Python执行环境，建议版本 3.7以上***

## 使用帮助

1. 安装向日葵客户端(16.3.2以上)

2. 启用[向日葵MCP服务](https://github.com/OrayDev/awesun-mcp])，并切换到 stdio 方式（默认）

3. 安装本项目

```bash
# 克隆项目
git clone https://github.com/OrayDev/awesun-skill.git

cd awesun-skill

# 安装python mcp依赖
pip install mcp
```

开启向日葵客户端上的MCP服务，显示服务配置如下：

```json
{
  "mcpServers": {
    "awesun-mcp-server": {
      "command": "/Applications/AweSun.app/Contents/Helpers/awesun-mcp-server",
      "env": {
        "AWESUN_API_URL": "http://127.0.0.1:8908",
        "AWESUN_API_TOKEN": "xxxxxxxxxxx"
      }
    }
  }
}
```

编辑本项目下 `awesun-skill/awesun-remote-control/mcp-config.json` 

1. 把 `/Applications/AweSun.app/Contents/Helpers/awesun-mcp-server`(这是Mac的默认值) 替换成MCP服务配置的command，即上面的 `C:\Program Files\Oray\Awesun\awesun-mcp-server`
2. 替换 `your-mcp-server-token` 为配置中 AWESUN_API_TOKEN，即上面的 `xxxxxxxxxx`

即完成Skill配置，可安装到AI工具使用

### Skill安装

#### Claude code

1. 把 `awesun-remote-control` 复制到对应目录

```bash
# 全局安装
cp -r awesun-remote-control ~/.claude/skills/

# 安装到指定workspace（特定项目生效）,下面用 /your/path/of/workspace 为示例
mkdir -p /your/path/of/workspace/.claude/skills # 确保存在可跳过
cp -r awesun-remote-control /your/path/of/workspace/.claude/skills
```

2. 重启Claude code，输入 `/skills` 确认skill是否安装正确

#### Opencode

1. 把 `awesun-remote-control` 复制到对应目录

```bash
# 全局安装
cp -r awesun-remote-control ~/.opencode/skills/

# 安装到指定workspace（特定项目生效）,下面用 /your/path/of/workspace 为示例
mkdir -p /your/path/of/workspace/.opencode/skills # 确保存在可跳过
cp -r awesun-remote-control /your/path/of/workspace/.opencode/skills
```

2. 重启opencode，，输入 `/skills` 确认skill是否安装正确

#### 🦞OpenClaw

1. 把 `awesun-remote-control` 复制到OpenClaw配置目录

```bash
# Linux/Mac 默认路径
cp -r awesun-remote-control ~/.openclaw/skills/

# Windows
cp -r awesun-remote-control %USERPROFILE%\.openclaw\skills\
```

2. 发信息让OpenClaw自行加载Skill `awesun-remote-control` 确认安装成功，若无法成功尝试重启gateway。

## 功能特性

本 skill 基于向日葵MCP提供远程控制工具，功能与向日葵MCP一致，详见：[awesun-mcp](https://github.com/OrayDev/awesun-mcp) - 向日葵 MCP 服务

## 使用示例

安装完成后，你可以在对话框中这样使用：

```
帮我连接到办公室的电脑，然后截个图看看桌面状态

搜索一下名为"办公室电脑"的设备，然后建立远程桌面连接

在远程电脑上打开记事本并输入一些文字

关闭远程连接
```

## 注意事项

- 使用前请确保向日葵客户端已启动并登录
- 建议配合 [screenshot-ui-locator](http://github.com/OrayDev/screenshot-ui-locator) Skill 使用以提供更好的桌面操作体验

## 相关项目

- [awesun-mcp](https://github.com/OrayDev/awesun-mcp) - 向日葵 MCP 服务
- [awesun-ui-locator](https://github.com/OrayDev/awesun-ui-locator) - 截图辅助 GUI 理解 Skill
- [awesun-usecase-skill-example](https://github.com/OrayDev/awesun-usecase-skill-example) - 通过向日葵 MCP 实现的用例场景