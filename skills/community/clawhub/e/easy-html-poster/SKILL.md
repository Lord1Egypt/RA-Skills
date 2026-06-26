# Skill: HTML海报制作

用HTML+浏览器截图的方式快速制作小红书/朋友圈海报。

## 使用场景
- 用户要求制作海报
- 需要快速生成可视化内容

## 核心步骤

### 1. 创建HTML文件
在 `~/Desktop/` 目录下创建HTML文件，包含完整样式的小红书海报模板。

关键要点：
- 宽度800px，高度1200px（竖版）
- 使用 `font-family: 'Noto Sans SC'` 支持中文
- 背景简约清新（白色或浅色）
- 配色：绿色(#27AE60)代表农业/养殖，红色(#E74C3C)代表法律/警示

### 2. 启动本地服务器
```bash
cd ~/Desktop
python3 -m http.server 9999
```

### 3. 浏览器打开并截图
- 使用OpenClaw browser工具打开 `http://localhost:9999/文件名.html`
- 截图保存到桌面

### 4. 清理
- 关闭本地服务器
- 删除临时HTML文件（可选保留）

## 模板示例

### 农业/养殖海报模板
```html
<style>
  .poster { width: 800px; height: 1200px; background: white; }
  .header { background: linear-gradient(135deg, #27AE60 0%, #1E8449 100%); padding: 30px; text-align: center; }
  .header-title { font-size: 36px; font-weight: 900; color: white; }
  .section { background: #F8F8F8; border-radius: 12px; padding: 15px; margin-bottom: 12px; }
  .section-title { font-size: 18px; font-weight: 700; color: #27AE60; }
  .highlight-box { background: #E8F8F0; border-radius: 12px; padding: 15px; border-left: 5px solid #27AE60; }
  .warning-box { background: #FDEBD0; border-radius: 12px; padding: 15px; border-left: 5px solid #E67E22; }
  .footer { background: linear-gradient(135deg, #27AE60 0%, #1E8449 100%); padding: 20px; text-align: center; }
  .tag { background: #E8F8F0; color: #27AE60; padding: 5px 10px; border-radius: 15px; font-size: 12px; }
</style>
```

### 法律/咨询海报模板
```html
<style>
  .poster { width: 800px; height: 1200px; display: flex; }
  .left { width: 220px; background: #FFF5F5; }
  .right { flex: 1; background: white; }
  .header { background: linear-gradient(135deg, #E74C3C 0%, #C0392B 100%); border-radius: 10px; padding: 16px; }
  .case-box { background: #F8F8F8; border-radius: 8px; padding: 12px; }
  .result-box { background: linear-gradient(135deg, #FFE5E5 0%, #FFF5F5 100%); border-radius: 8px; padding: 10px; }
  .cta-box { background: linear-gradient(135deg, #E74C3C 0%, #C0392B 100%); border-radius: 8px; padding: 10px; }
</style>
```

## 快速命令

```bash
# 启动服务器
cd ~/Desktop && python3 -m http.server 9999

# 关闭服务器
pkill -f "python3 -m http.server 9999"
```

## 注意事项
- 端口9999避免与8888冲突（Canva等可能占用）
- HTML中的图片用本地路径或网络URL
- 截图后及时关闭服务器释放资源
