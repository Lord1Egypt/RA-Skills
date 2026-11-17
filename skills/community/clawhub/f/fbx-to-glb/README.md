# FBX-to-GLB Skill for WorkBuddy

FBX 转 GLB 无损转换 WorkBuddy 技能。提供 CLI 命令行转换和网页部署两种方式，基于 Assimp WASM 工业级引擎。

## 安装

**方式一：zip 导入**

1. 下载 [fbx-to-glb.zip](https://github.com/zzh448/fbx-to-glb-skill/releases/latest/download/fbx-to-glb.zip)
2. WorkBuddy → 左侧菜单 → 技能 → 导入 → 选择 zip 文件

**方式二：手动安装**

```bash
mkdir -p ~/.workbuddy/skills/fbx-to-glb
# 将仓库所有文件复制到 ~/.workbuddy/skills/fbx-to-glb/
```

## 使用

安装后，在 WorkBuddy 中直接说：

- "帮我转一下这个 FBX 文件"
- "把 C:/xxx.fbx 转成 GLB"
- "部署一个 FBX 转换网站"

WorkBuddy 会自动加载本技能完成转换。

## 功能

| 方式 | 说明 |
|------|------|
| CLI 转换 | `scripts/convert.js` — Node.js 命令行，贴图/材质/骨骼完整保留 |
| Web 部署 | `assets/web/` — 拖拽上传 + 3D 预览 + 一键下载，纯浏览器端运行 |

## 技术栈

- [assimpjs](https://github.com/kovacsv/assimpjs) — Assimp 编译为 WASM
- 工业级 FBX 解析，40+ 格式支持
