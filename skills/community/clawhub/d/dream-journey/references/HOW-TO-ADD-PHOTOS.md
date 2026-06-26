# 如何在报告中添加图片

## 📸 图片支持方式

报告生成器支持 **3 种图片添加方式**：

### 方式 1：使用网络图片 URL（推荐）

在 JSON 数据中使用 `src` 字段填写图片 URL：

```json
{
  "photos": [
    {
      "src": "https://example.com/photo1.jpg",
      "alt": "图片描述",
      "caption": "图片说明文字"
    }
  ]
}
```

**推荐图片源**：
- Unsplash: `https://images.unsplash.com/photo-xxx?w=800`
- 飞猪/携程景点图片
- 自己上传到图床的图片

### 方式 2：使用本地图片路径

将图片放在报告同级目录，使用相对路径：

```json
{
  "photos": [
    {
      "src": "./photo1.jpg",
      "alt": "五营晨雾",
      "caption": "梦中的晨雾，在这里真实可见"
    },
    {
      "src": "./photo2.jpg",
      "alt": "森林木屋",
      "caption": "森林深处的木屋"
    }
  ]
}
```

**文件结构**：
```
/Users/catschro/.qoderwork/skills/dream-journey/
├── 伊春五营森林寻梦报告-report.html
├── photo1.jpg          ← 图片放在同级目录
├── photo2.jpg
└── test-data.json
```

### 方式 3：不填图片（占位符）

如果暂时没有图片，可以不填 `src`，会显示占位符：

```json
{
  "photos": [
    {
      "alt": "五营晨雾",
      "caption": "梦中的晨雾"
    }
  ]
}
```

或者完全不填 photos 数组：

```json
{
  "photos": []
}
```

会显示 "📸 照片待添加" 的占位卡片。

---

## 🎯 完整示例

```json
{
  "title": "伊春五营森林寻梦报告",
  "photos": [
    {
      "src": "https://images.unsplash.com/photo-1448375240586-882707db888b?w=800",
      "alt": "五营晨雾",
      "caption": "梦中的晨雾，在这里真实可见"
    },
    {
      "src": "./my-photo-1.jpg",
      "alt": "我拍的木屋",
      "caption": "和梦里一模一样的木屋"
    },
    {
      "alt": "待添加",
      "caption": "下次补上照片"
    }
  ]
}
```

---

## 💡 获取目的地图片的方法

### 1. Unsplash 免费图库
访问 https://unsplash.com 搜索目的地关键词，复制图片链接：
```
https://images.unsplash.com/photo-xxx?w=800
```

### 2. 手机拍照上传
1. 行程中拍照保存到手机
2. 上传到图床（如 SM.MS、ImgBB）
3. 复制 URL 填入 JSON

### 3. 使用 FlyAI 查询结果中的图片
如果 FlyAI 返回景点图片 URL，直接使用。

---

## 🖼️ 照片墙效果

- ✅ 响应式网格布局（自动适配手机/桌面）
- ✅ 悬停缩放 + 旋转动画
- ✅ 说明文字滑入效果
- ✅ 圆角阴影卡片
- ✅ 支持 1-10 张图片

---

## 🔧 快速测试

**前置要求**：
- 已安装 Node.js（v14+）：https://nodejs.org/
- 验证安装：`node --version`

运行以下命令生成带图片的示例报告：

```bash
cd /Users/catschro/.qoderwork/skills/dream-journey
node scripts/generate-report.js --json test-forest-with-photos.json
```

然后在浏览器打开生成的 HTML 文件查看效果！
