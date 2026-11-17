# HTML 模板使用与扩展指南

本文件说明 `assets/template.html` 的结构约定与二次扩展方法。该模板为**暖色极简、零外部 CDN、仅用系统字体**的单文件架构图骨架，已在 Skill 包内随附。

## 设计约束（必须遵守）

- **零外部依赖**：不引入任何 `<script src>`、Google Fonts、CDN 字体或图片外链。字体仅用系统字体栈（`system-ui` / `PingFang SC` / `Microsoft YaHei` / `sans-serif`）。
- **暖色基调**：背景 `#edebe1`、卡片 `#f5f3eb`、卡片悬浮 `#faf8f2`，顶部 3px 色条区分角色。
- **自包含**：所有 CSS 写在 `<style>` 内；不依赖 JS 即可渲染（动画与 hover 用纯 CSS）。
- **响应式**：768px 以下卡片纵向堆叠、容器收窄。

## 模板结构（自顶向下）

```
<header>          标题 + 一句话 tagline（本图聚焦脉络与范围）
<users-row>       可选：终端用户 / 运营后台等角色卡（avatar 用渐变色区分）
<section>×N      每层一个 section，带 section-tag 角标 + cards-row
  <section-tag>   层名角标，颜色见下方 theme 类
  <cards-row>     同层卡片横向排列
    <card>        单节点：card-title / card-route（路由或模块名）/ card-list（能力点）
<arrow-col>       层间竖向箭头（line + arrow-head）
<legend>          颜色图例
```

## 主题色类（直接复用，勿新增十六进制硬编码）

卡片与角标的颜色通过 `card-{role}` / `tag-{role}` 类切换，`{role}` ∈ {web, api, db, git, cli, feishu}：

| 角色类 | 色值变量 | 语义 |
| --- | --- | --- |
| `-web` | `--accent-blue` | 前端 / 网关 / 接入 |
| `-api` | `--accent-green` | 应用服务 / 接口 |
| `-db` | `--accent-amber` | 数据 / 存储 |
| `-git` | `--accent-purple` | 版本 / CI |
| `-cli` | `--accent-indigo` | 命令行 / 工具 |
| `-feishu` | `--accent-teal` | 协作 / 消息 |

> 新增角色时，先在 `:root` 增加 `--accent-xxx` 变量，再补 `card-xxx` 与 `tag-xxx` 两条规则，保持与现有 6 类同构。

## 扩展方法

1. **加层**：复制一个 `.section`（连同其 `section-N` 序号与层间 `arrow-col`）插入到目标位置，改 `section-tag` 文案与 `tag-*` 类。
2. **加节点**：在某层 `.cards-row` 内复制一个 `.card`，改 `card-*` 类、`card-title`、`card-route`、`card-list` 项。
3. **改标题 / 副标题**：编辑 `.header h1` 与 `.tagline`。
4. **加角色卡**：在 `.users-row` 内复制 `.user-card`，通过 `avatar-{role}` 换渐变。
5. **加图例**：在 `.legend` 内追加 `.legend-item`，`legend-dot` 用对应 `--accent-*` 内联样式。

## 自检清单

- [ ] 无 `<script src>` / 外链字体 / 外链图片
- [ ] 所有节点都有 `card-title`（非空）
- [ ] 每层层名 `section-tag` 不重复、与 `legend` 一一对应
- [ ] 层间箭头数量 = 层数 - 1
- [ ] 768px 下无横向溢出（卡片 `max-width` 生效）
