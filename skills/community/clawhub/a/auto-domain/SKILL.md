---
name: auto-domain
description: >
  当用户说"启动项目"、"给项目一个公网域名"、"start tunnel"、"expose my project"、
  "让项目可以公网访问"、"start my project with a public URL" 时自动触发。
  无需用户做任何操作：自动检测项目目录和端口，修复环境，启动 tunnel，
  直接返回公网域名 URL。
---

# Auto Domain

**一句话触发，全自动执行，直接给出公网 URL。用户无需手动配置。**

## Agent 执行步骤（全自动）

```
用户说：启动我的项目，给我一个公网域名
         ↓
1. 确认项目目录（pwd 或用户指定目录）
2. 运行 scripts/auto_start.sh [project_dir] [port]
         ↓
   auto_start.sh 自动完成：
   ├─ 检测端口（从 package.json / 框架类型自动判断）
   ├─ 安装/更新 project-tunnel.sh 到项目目录
   ├─ 检测环境（python3/python, curl, node, npm, lsof）
   ├─ 自动安装缺失工具（brew / apt / yum）
   └─ 启动 tunnel
         ↓
3. 从输出提取 public_url
4. 直接返回用户公网地址
```

## 调用方式

```bash
# 当前目录，自动检测端口
scripts/auto_start.sh

# 指定目录和端口
scripts/auto_start.sh /Users/huchangfeng/todo-katong 4545
```

输出中重点字段：`public_url`

## 触发关键词示例

- "启动我的项目"
- "给我的项目一个公网域名"
- "让外网能访问我的项目"
- "start tunnel for my project"
- "expose port 3000 to the internet"
- "给我一个公网 URL"
- "start my project with a public URL"

## 环境问题处理

```bash
scripts/check_env.sh          # 查看缺少哪些工具
scripts/fix_env.sh python3    # 修复指定工具
scripts/auto_start.sh         # 重试
```
