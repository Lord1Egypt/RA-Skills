---
name: fbx-to-glb
description: "FBX 转 GLB 无损转换工具。提供 CLI 命令行转换（Node.js + assimpjs）和网页端部署（HTML + WASM，含 3D 预览）两种方式。基于 Assimp 工业级引擎，完整保留贴图、材质、骨骼动画和蒙皮。触发场景：用户请求将 FBX 文件转换为 GLB/glTF 格式、部署 FBX 转 GLB 转换网站、批量 3D 模型格式转换。"
version: 1.0.0
author: zzh448
trigger:
  - "帮我转个 FBX"
  - "把 FBX 转成 GLB"
  - "FBX 转 GLB"
  - "3D 模型格式转换"
  - "无损转换 FBX"
  - "转换这个 FBX 文件"
  - "部署 FBX 转换网站"
agent_created: true
---

# FBX → GLB Converter Skill

无损 FBX 转 GLB 格式转换，提供 CLI 和 Web 两种方案。

## 可用资源

| 资源 | 路径 | 用途 |
|------|------|------|
| CLI 转换脚本 | `scripts/convert.js` | Node.js 命令行转换工具 |
| Web 模板 | `assets/web/` | 网页版转换器完整文件 |

## 使用方式

### 方式 1：CLI 命令行转换（推荐日常使用）

适用于用户直接提供 FBX 文件路径，需要快速转换。

**前置条件：** 项目目录需安装 `assimpjs`：

```bash
cd <项目目录>
npm install assimpjs
```

**执行转换：**

```bash
node <skill-dir>/scripts/convert.js <输入.fbx> [-o <输出.glb>] [--force]
```

| 参数 | 说明 |
|------|------|
| 第一个参数 | 输入 FBX 文件路径（必须） |
| `-o` | 输出 GLB 路径（默认与输入同目录、同名） |
| `--force` | 覆盖已有输出文件 |

**示例：**

```bash
# 基本转换
node scripts/convert.js "C:/Users/xxx/model.fbx"

# 指定输出路径和覆盖
node scripts/convert.js "C:/Users/xxx/model.fbx" -o "C:/Users/xxx/model.glb" --force

# 从 skill 路径执行（用户未安装时）
node ~/.workbuddy/skills/fbx-to-glb/scripts/convert.js "文件路径.fbx"
```

### 方式 2：部署网页版转换器

适用于用户要分享给他人、或部署到托管平台。

网页版包含以下文件：

- `assets/web/index.html` — 主页面（拖拽上传 + 3D 预览 + 一键下载）
- `assets/web/assimpjs.js` — Assimp WASM JS 绑定
- `assets/web/assimpjs.wasm` — Assimp WASM 引擎（~4MB）
- `assets/web/robots.txt` — SEO 爬虫配置
- `assets/web/sitemap.xml` — 搜索引擎站点地图

**部署步骤：**

1. 将 `assets/web/` 下所有文件复制到目标目录
2. 推送到 GitHub Pages 或任意静态托管（Vercel、Netlify、CloudStudio 等）

**CloudStudio 部署（推荐最简单）：**

```bash
# 复制文件到 dist 目录
mkdir -p dist && cp assets/web/* dist/

# 调用 cloudstudio-deploy skill
```

**GitHub Pages 部署：**

1. 在 GitHub 创建仓库
2. 将 `assets/web/` 文件放入仓库的 `docs/` 目录
3. Settings → Pages → Source: `Deploy from a branch` → Branch: `master` → Folder: `/docs`
4. 等待 1-2 分钟后通过 `https://<用户名>.github.io/<仓库名>/` 访问

## 关键技术细节

- **引擎：** assimpjs（Assimp 编译为 WASM），工业级 FBX 解析
- **贴图：** `assimpjs` 使用 `FS.readFile(GetPath(), encoding: 'binary')` 获取文件内容（返回 Uint8Array），非 `GetName()`/`GetContent()` 方法
- **转换流程：** `assimp.FS.readFile` → 读取原始 FBX → `assimp.ConvertFileList` 转换 → 遍历结果文件找到 `.glb` → `FS.readFile` 读取 blob → 写入磁盘
- **Web 版特性：** 单向数据流（拖拽→解析→预览→导出），支持 OrbitControls 3D 旋转/缩放
- **文件限制：** CLI 无限制，Web 版建议 ≤500MB

## 故障排除

| 问题 | 原因 | 解决 |
|------|------|------|
| `GetName is not a function` | API 方法名错误 | 用 `GetPath()` 代替 `GetName()` |
| 导出白模（无贴图） | Three.js FBXLoader 贴图格式不兼容 | 改用 assimpjs（本 skill 默认方案） |
| WASM 加载失败 | 跨域限制 | 确保 `.wasm` 与 `.js` 同目录 |
| npm install 报错 | 缺少 node-gyp | 使用系统 npm: `"C:/Program Files/nodejs/npm.cmd" install assimpjs` |
| git push 报 `Connection reset` | GitHub 网络不稳定 | 在用户本地 Git Bash 中手动 push |
