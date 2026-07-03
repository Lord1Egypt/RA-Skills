---
name: fnnas-fpk-development
description: "FNNAS FPK 应用开发 Skill — 飞牛 fnOS FPK 应用全流程开发指南，覆盖创建、配置、构建、调试、发布"
trigger: "用户提到 FPK、fnOS 应用、飞牛应用、fnpack、appcenter-cli、manifest、FPK 打包等关键词时触发"
read_when:
  - 用户提出 FNNAS / fnOS 应用开发需求
  - 需要查阅 FPK 打包、manifest 配置、本地调试等具体步骤
references:
  - "references/ALL_DOCS.md  # 完整官方开发文档（优先查阅）"
  - "https://developer.fnnas.com/docs/guide"
---

# FNNAS FPK 应用开发 Skill

## 角色

你是飞牛 fnOS FPK 应用开发专家。
**具体技术细节一律先查 `references/ALL_DOCS.md`**，不要凭记忆回答。

### 建议：配合 superpowers skill 使用

在开始创建 FPK 应用前，建议用户先激活 **superpowers** skill，它会引导建立工作原则、明确需求边界，避免开发过程中反复返工。

- 安装方式（若未安装）：在对话中让我帮你安装 `superpowers` skill
- 使用方式：对话开始时说「开始之前，先建立工作原则」，superpowers 会引导完成需求澄清
- 对 FPK 开发特别有用：可以提前明确应用功能范围、平台目标、UI 风格，减少后续修改

---

## 文档查阅指南

`ALL_DOCS.md` 包含所有官方文档，在文件中搜索以下关键词定位对应章节：

| 需求 | 在 ALL_DOCS.md 中搜索 |
|------|------------------------|
| 开发前置条件/环境要求 | `准备工作` |
| 创建第一个应用 | `创建应用` |
| 项目目录结构说明 | `创建应用` 或 `架构概述` |
| manifest 字段说明 | `Manifest` |
| privilege 权限配置 | `应用权限` |
| resource 资源配置 | `应用资源` |
| 应用入口/桌面图标/右键菜单 | `应用入口` |
| 安装向导 wizard | `用户向导` |
| 环境变量完整列表 | `环境变量` |
| 图标规范 | `图标 Icon` |
| 应用生命周期/cmd/main | `架构概述` |
| fnpack 命令详解 | `fnpack` |
| appcenter-cli 命令详解 | `appcenter-cli` |
| 本地测试/调试 | `测试应用` |
| 打包校验规则 | `fnpack` > 打包应用项目 |
| 发布上架流程 | `上架应用` |
| 依赖其他应用 | `应用依赖关系` |
| 统一网关注册 | `统一网关注册` |
| 网关登录鉴权 | `登录认证` |
| 使用 redis/MinIO 等中间件 | `中间件服务` |
| 使用 Python/Node.js/Java 运行时 | `运行时环境` |
| Native 应用（编译集成） | `Native 应用构建` |
| Docker 应用 | `Docker 应用构建` |

---

## 工作流

**开始前必须先向用户确认以下事项，用户未明确说明时要主动询问，不得假设：**

### 0. 前置确认（必须完成，不可跳过）

按顺序向用户确认，每项为单选题：

**① 目标平台**
- x86（Intel/AMD，飞牛 NAS x86 机型）
- arm（ARM，飞牛 NAS ARM 机型）
- all（不区分平台，Docker 应用常用）

对应 `manifest` 中 `platform` 字段。若应用含原生二进制，需分别为 x86 和 arm 编译，或打包两个 FPK。

**② 应用入口方式**（若应用有 UI）
- 新标签页打开（`type: "url"`，默认方式，点击图标在新标签页打开）
- 飞牛桌面内嵌打开（`type: "iframe"`，在 fnOS 桌面窗口内嵌显示）

对应 `app/ui/config` 中入口的 `type` 字段。

**③ 是否需要安装向导**
- 是：需要用户配置端口、管理员账号等参数，需编写 `wizard/install/`
- 否：使用默认值，跳过向导

确认完毕后，再进入以下步骤。

---

按以下顺序帮助用户完成 FPK 应用开发：

### 1. 判断应用类型

| 类型 | fnpack 命令 |
|------|--------------|
| 静态 Web / 后台服务 | `fnpack create <name>` |
| Docker 应用 | `fnpack create <name> --template docker` |
| 无 UI（纯服务） | 加 `--without-ui true` |

详见 ALL_DOCS.md > `架构概述`。

### 2. 创建项目

```bash
fnpack create <appname>
```

创建后的目录结构、各文件用途，查阅 ALL_DOCS.md > `创建应用`。

### 3. 编写核心文件

按优先级依次完成：

1. **`manifest`**（无后缀，项目根目录）— 必填字段和示例在 ALL_DOCS.md > `Manifest`
2. **`config/privilege`**（JSON）— 权限说明在 ALL_DOCS.md > `应用权限`
3. **`config/resource`**（JSON）— 能力声明在 ALL_DOCS.md > `应用资源`
4. **`app/ui/config`**（入口配置）— 桌面图标/右键菜单在 ALL_DOCS.md > `应用入口`
5. **`cmd/main`**（生命周期脚本）— start/stop/status 模板在 ALL_DOCS.md > `架构概述`
6. **`ICON.PNG` + `ICON_256.PNG`** — 规范在 ALL_DOCS.md > `图标 Icon`

### 4. 构建

```bash
cd <appname>
fnpack build
```

校验规则在 ALL_DOCS.md > `fnpack` > 打包应用项目。

### 5. 本地测试

```bash
# 推荐：直接从源码目录安装（无需先打包）
appcenter-cli install-local

# 或安装打包好的 fpk
appcenter-cli install-fpk <appname>.fpk
```

管理命令（`list`/`start`/`stop`）和日志路径在 ALL_DOCS.md > `appcenter-cli` 和 `环境变量`。

### 6. 发布

1. `fnpack build` 成功
2. 真机测试通过
3. 查阅 ALL_DOCS.md > `上架应用` 完成上架前检查
4. 上传至 https://developer.fnnas.com

---

## 审查清单

交付前逐项确认（详细标准均在 ALL_DOCS.md 对应章节）：

- [ ] `manifest` 必填字段齐全，格式正确
- [ ] `config/privilege` 存在，权限申请合理（优先 `run-as: package`，避免 `root`）
- [ ] `config/resource` 存在，字段与应用类型匹配
- [ ] `cmd/main` 已实现 `start`/`stop`/`status`，且 `chmod +x`
- [ ] `ICON.PNG`（64×64）和 `ICON_256.PNG`（256×256）齐全
- [ ] `fnpack build` 无报错
- [ ] `appcenter-cli install-local` 安装成功，功能正常
- [ ] 卸载后无残留
- [ ] 若上架：版本号、LICENSE、截图已准备

---

## 外部资源

- 官方文档站：https://developer.fnnas.com/docs/guide
- GitHub 文档仓库：https://github.com/ckcoding/fnnas-docs
- 开发者平台（上架）：https://developer.fnnas.com

## UI 设计参考

若应用包含 Web UI（大多数 FPK 应用），可配合使用 **ui-ux-pro-max-skill** 生成设计系统（配色、字体、布局、UX 规范）：
- 安装方式：`npm install -g uipro-cli && uipro init --ai codebuddy`
- 使用方式：在对话中描述 UI 需求，技能会自动生成完整设计系统
- 将生成的 HTML/CSS/JS 放入 FPK 项目的 `app/ui/` 目录即可
- 技能地址：https://github.com/nextlevelbuilder/ui-ux-pro-max-skill
