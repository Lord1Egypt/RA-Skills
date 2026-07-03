# ETF 查询功能安装工作流：etf-fund-query

本工作流用于单独安装并初始化 ETF 查询功能（etf-fund-query）。安装时请按阶段执行；如果遇到异常，按对应阶段的处理方式给出原因和修复建议，不要跳过。

## 输入参数

- `apiKey`：必填。基金查询服务 API Key。安装脚本也支持不传入参数时交互式输入。
- `skillsDir`：可选。安装目录，默认 `~/.openclaw/workspace/skills`。也可以通过环境变量 `OPENCLAW_SKILLS_DIR` 覆盖。
- `--skip-api-verify`：可选。离线安装或网络受限时跳过接口连通性校验。

一键安装命令：

```bash
./install.sh --api-key "YOUR_KEY"
```

离线或仅做本地配置校验：

```bash
./install.sh --api-key "YOUR_KEY" --skip-api-verify
```

只更新本机私有 key，不重新复制功能文件：

```bash
./install.sh --api-key "YOUR_KEY" --no-install --skip-api-verify
```

## 阶段 1：环境检测

检查项：

- 当前系统是否可运行 shell 脚本。
- 是否存在 `python3`。
- Python 版本是否不低于 3.8。
- 是否能创建或写入安装目录，默认 `~/.openclaw/workspace/skills`。

异常处理：

- 未找到 `python3`：安装 Python 3.8 或更高版本后重试。
- Python 版本过低：升级 Python 后重试。
- 安装目录不可写：修复目录所有权/权限，或使用 `--skills-dir` 指定可写目录。

## 阶段 2：安装包完整性检查

检查项：

- `etf-fund-query/` 目录是否完整存在。
- `SKILL.md`、`config.py` 和 `references/catalog-etf.md` 是否齐全。

异常处理：

- 目录或文件缺失：不要继续安装；重新解压安装包，或重新下载完整安装包。

## 阶段 3：初始化 API Key

执行内容：

- 从 `--api-key` 参数读取 key；如果未传入，则交互式隐藏输入。
- 安装日志只显示脱敏 key。

异常处理：

- key 为空：使用 `./install.sh --api-key YOUR_KEY` 重新运行。

## 阶段 4：安装并写入 API Key

执行内容：

- 将 `etf-fund-query` 复制到目标安装目录。
- 将对应版本的 `config.py` 写入已安装功能目录。
- 写入 API Key（两处同时写入）：
  1. 写入 shell profile（zsh -> `~/.zshrc`，bash -> `~/.bash_profile`）。
  2. 写入本地配置文件（`_FALLBACK_KEY`）。

异常处理：

- 复制失败：检查目标目录权限，或使用 `--skills-dir DIR`。
- 两种写入方式均失败：检查 HOME 目录和安装目录权限。

## 阶段 5：能力校验

本地校验：

- `etf-fund-query` 能正确加载本地配置，读取到 API Key。

接口连通性校验：

- 调用 ETF 详情接口，使用测试代码 `510300`。

异常处理：

- 接口校验失败：检查网络、API Key 是否有效；离线环境可加 `--skip-api-verify` 先完成安装。
- 如果接口明确返回 API Key 无效或已过期，必须停止安装并要求更换有效 key。

## 阶段 6：完成确认

完成后输出：

- 安装目录。
- 可用功能：`etf-fund-query`。
