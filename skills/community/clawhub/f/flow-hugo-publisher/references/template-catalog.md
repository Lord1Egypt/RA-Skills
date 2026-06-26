# Hugo 模板目录与选型建议

用于初始化阶段快速选型。默认优先推荐内置模板；若用户有明确品牌风格或历史主题仓库，再走自定义模板。

## 内置模板清单

| 模板 | 仓库 | 适用场景 | 特点 |
|------|------|----------|------|
| `ananke` | `https://github.com/theNewDynamic/gohugo-theme-ananke.git` | 通用博客、个人站起步 | Hugo 官方示例，配置简单 |
| `PaperMod` | `https://github.com/adityatelange/hugo-PaperMod.git` | 技术博客、内容写作为主 | 轻量、加载快、SEO 友好 |
| `Stack` | `https://github.com/CaiJimmy/hugo-theme-stack.git` | 内容型博客、分类较多站点 | 信息架构清晰，侧边栏友好 |
| `Docsy` | `https://github.com/google/docsy.git` | 文档站、产品手册、知识库 | 文档导航强，适合多层级内容 |
| `blowfish` | `https://github.com/nunocoracao/blowfish.git` | 现代风格博客、品牌展示 | 样式现代，可定制度高 |

## 选择策略（托管默认）

1. 用户未指定模板：默认推荐 `PaperMod`。
2. 用户是文档站诉求：优先 `Docsy`。
3. 用户强调“先快速跑起来”：优先 `ananke`。
4. 用户有明确 UI 风格或历史模板：走自定义模板 URL。

## 自定义模板输入规范

- 必须是可访问的 Git 仓库地址（HTTPS）
- 建议包含 `README` 和示例配置说明
- 若为私有仓库，需要用户先完成访问权限配置

示例：

```text
https://github.com/<owner>/<hugo-theme-repo>.git
```

## 初始化命令参考

以 `<workspacePath>` 为工作目录，`<themeName>` 为主题名，`<themeRepo>` 为模板地址：

```bash
hugo new site "<workspacePath>"
git -C "<workspacePath>" init
git -C "<workspacePath>" submodule add "<themeRepo>" "themes/<themeName>"
```

在 `hugo.toml` 写入：

```toml
theme = "<themeName>"
```

## 常见失败与回退

1. 模板仓库下载失败：提示检查网络或更换镜像后重试。
2. 主题名与目录不一致：以 `themes/` 实际目录名为准更新 `theme` 字段。
3. 自定义模板不兼容当前 Hugo 版本：提示切换模板或升级 Hugo Extended。
