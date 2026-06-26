---
name: excalidraw-handdraw
description: 根据提示词生成手绘风格图表的 skill。用于：(1) 创建架构图、流程图、ER 图等 Excalidraw 手绘风格图表 (2) 通过 Docker 本地运行 canvas 服务器 (3) 生成 PNG/SVG 图片 (4) 保存图片到指定目录 (5) 将图表插入或替换到文件指定位置 (6) 支持中文手写字体。触发词：画图、创建图表、生成图表、手绘风格、架构图、流程图、Excalidraw、保存图表到文件、插入图表。
---

# Excalidraw Handdraw Skill

## Step 0: 检查 Canvas 服务器状态

首先检查 Docker canvas 是否已运行：

```bash
docker ps | grep mcp_excalidraw-canvas
```

如果未运行，使用脚本启动：
```bash
./scripts/start-canvas.sh
```

确认服务可用：
```bash
curl -s http://localhost:3000/health
```

## Step 1: 理解用户需求

用户描述想要创建的图表类型，例如：
- "画一个微服务架构图"
- "创建一个用户登录流程图"
- "生成一个数据库 ER 图"
- "画一个网络拓扑图"

分析需求：
- 确定图表类型（架构图、流程图、ER 图等）
- 确定需要的元素（矩形、箭头、文字等）
- 确定是否需要中文标签

## Step 2: 创建图表元素

使用 `batch_create_elements` 批量创建元素。参考坐标系统：
- 原点 (0,0) 在左上角
- x 向右增加，y 向下增加
- 元素宽度：`max(160, labelCharCount * 9)`
- 元素高度：单行 60px，双行 80px
- 垂直间距：80-120px
- 水平间距：40-60px

**JSON 元素示例：**
```json
{
  "elements": [
    {"id": "lb", "type": "rectangle", "x": 300, "y": 50, "width": 180, "height": 60, "text": "负载均衡器"},
    {"id": "svc-a", "type": "rectangle", "x": 100, "y": 200, "width": 160, "height": 60, "text": "服务 A"},
    {"id": "svc-b", "type": "rectangle", "x": 450, "y": 200, "width": 160, "height": 60, "text": "服务 B"},
    {"type": "arrow", "x": 0, "y": 0, "startElementId": "lb", "endElementId": "svc-a"},
    {"type": "arrow", "x": 0, "y": 0, "startElementId": "lb", "endElementId": "svc-b"}
  ]
}
```

## Step 3: 验证图表质量

创建后获取截图验证：
- 使用 `get_canvas_screenshot` 获取图片
- 检查文字是否截断
- 检查元素是否重叠
- 检查箭头是否穿过无关元素

发现问题时修复：
- 文字截断 → 增加元素宽度/高度
- 元素重叠 → 调整坐标位置
- 箭头穿过元素 → 使用曲线箭头或调整布局

## Step 4: 导出图片

当图表完成后，使用 Playwright 导出只包含画布区域的图片（无 UI 按钮）：

```bash
./scripts/export-canvas.sh [--output path]
```

默认输出到 `/tmp/excalidraw-diagram.png`

## Step 5: 保存到指定目录

使用脚本保存到用户指定位置：

```bash
./scripts/save-to-file.sh --source <图片路径> --dest <目标路径>
```

示例：
```bash
./scripts/save-to-file.sh --source /tmp/diagram.png --dest docs/diagrams/architecture.png
```

## Step 6: 插入/替换到文件

将图片插入到 Markdown 文件：

**插入到文件末尾：**
```markdown
![图表描述](图片路径)
```

**插入到特定位置：**
使用 sed 或脚本在指定标记位置插入：
```bash
# 在 <!-- diagram:start --> 和 <!-- diagram:end --> 之间插入
./scripts/insert-image.sh --file README.md --marker "diagram:start" --image path/to/image.png
```

**替换已存在的图片：**
```bash
./scripts/replace-image.sh --file README.md --old-image old.png --new-image new.png
```

## 常用命令参考

| 操作 | 命令 |
|------|------|
| 启动 Canvas | `./scripts/start-canvas.sh` |
| 停止 Canvas | `./scripts/stop-canvas.sh` |
| 导出图片（仅画布） | `./scripts/export-canvas.sh /tmp/diagram.png` |
| 保存到目录 | `./scripts/save-to-file.sh --source /tmp/d.png --dest docs/d.png` |
| 插入到文件 | `./scripts/insert-image.sh --file README.md --marker "diagram:start" --image d.png` |
| 替换图片 | `./scripts/replace-image.sh --file README.md --old d1.png --new d2.png` |

## 注意事项

1. **Docker 必须运行**：Canvas 服务器通过 Docker 运行
2. **中文支持**：使用 `fontFamily: "1"` 或默认字体，Excalidraw 原生支持中文
3. **中文手写字体**：如需更自然的手写效果，可使用 excalidraw-cn 的中文手写字体配置
4. **图片导出**：需要浏览器窗口打开才能截图，确保 canvas UI 可访问
5. **图片导出**：使用 Playwright 无头浏览器导出，只截取画布区域，无 UI 按钮

## 故障排除

- **Canvas 无法连接**：检查 Docker 容器是否运行 `docker ps | grep mcp_excalidraw-canvas`
- **导出失败**：确保浏览器可访问 http://localhost:3000
- **权限错误**：确保用户对目标目录有写权限
