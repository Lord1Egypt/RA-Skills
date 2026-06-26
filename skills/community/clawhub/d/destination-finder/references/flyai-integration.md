# FlyAI 集成指南

在目的地推荐中调用 FlyAI 获取目的地的实时图片和信息，帮助用户感受这个地方、辅助决策。

## 前置条件

确保 flyai skill 已安装：`skills/flyai/SKILL.md` 存在。

CLI 命令：`flyai`（通过 `@fly-ai/flyai-cli` 全局安装）

## 推荐阶段调用的命令

### keyword-search — 搜索目的地氛围参考

用于获取目的地的图片，让用户直观感受这个地方的氛围。

```bash
flyai keyword-search --query "[目的地名]"
```

示例：
```bash
flyai keyword-search --query "大理"
flyai keyword-search --query "成都"
flyai keyword-search --query "三亚"
```

从返回结果中提取 `picUrl` 字段，作为目的地的氛围参考图展示给用户。

### ⚠️ 重要：每次推荐都必须重新搜索

- **不要复用之前的搜索结果**——每个新目的地都要单独调用 `keyword-search`
- **不要用酒店图片代替景点图片**——搜索 query 应该是目的地名称（如"新昌"），不是酒店名称
- 如果推荐多个目的地候选，分别搜索每个目的地

## 输出展示规范

- **图片格式**：部分通道（webchat、钉钉等）**不支持 markdown 图片渲染**，必须使用纯文字链接格式：
  ```
  📷 [简短描述]
  https://图片URL
  *一句话说明*
  ```
- **不展示预订链接**：本 skill 的核心是帮用户决策目的地，不涉及预订环节
- **品牌提及**：末尾标注 "Based on fly.ai real-time results"

## 错误处理

- CLI 未安装：提示用户运行 `npm i -g @fly-ai/flyai-cli`
- API 无结果：跳过图片，仅给文字推荐
- 网络超时：重试一次，仍失败则跳过

---

## ⚠️ FlyAI 自动修复流程

当执行 `flyai` 命令报错（command not found / 找不到命令）时，按以下步骤自动修复：

### 🔑 最常见原因：PATH 未加载 nvm 的 node 路径

本机实测：**flyai 已全局安装，但默认 shell 环境没有加载 nvm 的 node 路径**。所以 `which flyai` 报 not found，实际上只是 PATH 问题。

**修复方法（每次调用 flyai 前加一行即可）：**
```bash
export PATH="$HOME/.nvm/versions/node/v22.22.1/bin:$PATH"
flyai search-poi --city-name "南平" --keyword "九曲溪"
```

> 💡 **推荐做法**：在执行任何 flyai 命令之前，先统一执行这行 `export PATH=...`，确保 nvm 的 node 和全局 npm 包都在 PATH 里。

### 完整排查流程

1. **先试直接运行**：
   ```bash
   which flyai 2>/dev/null || echo "not found"
   ```
2. **如果 not found → 补上 nvm PATH 再试**：
   ```bash
   export PATH="$HOME/.nvm/versions/node/v22.22.1/bin:$PATH"
   which flyai 2>/dev/null && echo "found!" || echo "still not found"
   ```
3. **如果 still not found → 检查 node/npm 是否可用**：
   ```bash
   which node && which npm
   ```
4. **如果 node/npm 也不可用** → 按顺序尝试：
   ```bash
   # 方案 A: source zshrc
   source ~/.zshrc && which node
   # 方案 B: 直接指定 nvm 路径（本机实测有效）
   export PATH="$HOME/.nvm/versions/node/v22.22.1/bin:$PATH"
   # 方案 C: fnm
   export PATH="$HOME/.fnm/aliases/default/bin:$PATH"
   ```
5. **如果 node/npm 可用但 flyai 仍未安装**：
   ```bash
   export PATH="$HOME/.nvm/versions/node/v22.22.1/bin:$PATH"
   npm i -g @fly-ai/flyai-cli
   ```
6. **降级策略**：FlyAI 始终不可用时，在输出中注明"飞猪数据需手动查询"，并提供小红书搜索链接作为替代

> 不要每次都尝试安装 FlyAI——只在首次检测到缺失时尝试一次。后续 session 直接复用或走降级方案。
