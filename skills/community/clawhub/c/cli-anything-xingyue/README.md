# CLI-Anything OpenClaw Skill

让任意软件都能被 AI Agent 驱动。

## 安装

此 Skill 已预装在 OpenClaw 中。

## 使用方法

### 构建 CLI

为任意软件生成 CLI 工具：

```
/cli-build ./gimp
/cli-build https://github.com/blender/blender
```

### 优化 CLI

扩展和改进已生成的 CLI：

```
/cli-refine ./gimp
/cli-refine ./gimp "图像批处理"
```

### 验证 CLI

验证生成的 CLI 是否正确：

```
/cli-validate ./gimp
```

### 列出已生成的 CLI

```
/cli-list
```

## 前置要求

- Python 3.10+
- Git
- uv (包管理器)
- 目标软件已安装在系统中

## 注意事项

CLI-Anything 的完整构建功能需要：
1. **Claude Code** - 最佳支持，通过 Plugin 市场
2. **Codex** - 通过内置 Skill
3. **OpenClaw** - 当前版本提供引导和验证

对于完整的自动生成，建议在 Claude Code 或 Codex 环境中运行一次构建，然后将生成的 CLI 复制到 OpenClaw 中使用。

## 示例工作流

1. 在 Claude Code 中构建 CLI：
   ```
   /plugin marketplace add HKUDS/CLI-Anything
   /plugin install cli-anything
   /cli-anything:cli-anything ./gimp
   ```

2. 安装生成的 CLI：
   ```
   cd gimp/agent-harness && pip install -e .
   ```

3. 在 OpenClaw 中使用：
   ```
   cli-anything-gimp --json layer add -n "Background"
   ```

## 更多信息

- 官网: https://github.com/HKUDS/CLI-Anything
- 文档: https://github.com/HKUDS/CLI-Anything/blob/main/README_CN.md
