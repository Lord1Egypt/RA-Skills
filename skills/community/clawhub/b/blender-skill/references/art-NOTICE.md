# NOTICE / 第三方来源

## arjun988/blender-skills

- URL: https://github.com/arjun988/blender-skills
- Version referenced: v1.3.0（2026-07-10，94 skills / 269 files / 292.2 KB，0 行可执行代码）
- License: MIT
- What we used: **美术生产规范数值与流程框架**（命名前缀体系、collection 分层、面数/贴图/TD 预算、LOD 比例、导出参数、参考图匹配闭环的步骤骨架、风格包的氛围要素）
- What we did NOT do: 未复制其 `SKILL.md` / `references` 原文；未采用其宣称但不属于官方 MCP v1.0.3 的工具（Poly Haven / Hyper3D / Hunyuan3D）；未引入其 60+ 风格包全文
- Transformation: 全部重写为带 Blender 版本守卫的规格表 + bpy 片段 + `asset_qa.py` 可执行审计器

MIT License 要求保留版权与许可声明：

```
MIT License

Copyright (c) 2026 arjun988

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Blender

- https://www.blender.org/ — GPL。本技能仅通过 Python API 调用，不包含 Blender 源码。

## 其他

- 官方 Blender MCP Server（`lab/blender_mcp`，add-on v1.0.3）— 工具名与用法以官方仓库为准
- 各引擎（Unreal / Unity / Godot）导入规范为其官方文档中的公开约定
