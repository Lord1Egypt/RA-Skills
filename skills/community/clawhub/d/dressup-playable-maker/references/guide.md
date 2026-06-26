# Dressup Playable 制作指南

## 图片规范

### 角色部件
- **格式**: PNG (透明背景)
- **尺寸**: 建议 400x800 像素
- **锚点**: 所有部件对齐到同一基准点（脚底中心）
- **命名**: 使用下划线分隔，如 `hair_01.png`

### 背景图
- **格式**: JPG 或 PNG
- **尺寸**: 建议 1080x1920 像素（9:16）
- **内容**: 留出底部 20% 空间给 UI 按钮

### 文件大小
- 单个文件不超过 500KB
- 总资源包不超过 5MB

## 目录结构示例

```
my-assets/
├── character/
│   ├── body.png
│   ├── hair/
│   │   ├── hair_1.png
│   │   ├── hair_2.png
│   │   └── hair_3.png
│   ├── dress/
│   │   ├── dress_1.png
│   │   ├── dress_2.png
│   │   └── dress_3.png
│   └── shoes/
│       ├── shoes_1.png
│       ├── shoes_2.png
│       └── shoes_3.png
└── background.jpg
```

## 制作流程

1. **准备素材** - 按规范制作角色部件和背景
2. **整理目录** - 按上述结构放置文件
3. **运行生成** - `python3 scripts/generate.py --input-dir ./my-assets --output-dir ./output`
4. **测试验证** - 在浏览器和手机端测试
5. **打包上传** - 将 output 文件夹打包为 zip 上传平台

## 常见问题

**Q: 部件错位怎么办？**
A: 确保所有部件使用相同的画布尺寸和锚点位置。

**Q: 图片加载慢？**
A: 使用 tinypng.com 等工具压缩图片。

**Q: 需要更多分类？**
A: 修改生成的 index.html 中的 `steps` 数组。
