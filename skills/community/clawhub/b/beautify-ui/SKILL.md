# beautify-ui - 智能 UI 美化技能 v3.3.0

🎨 一键应用 30 种知名设计风格（Notion/Figma/Linear/Apple/Alibaba/Shopify 等），自动检测项目类型并生成实时预览页

## 功能特性

- **30 种设计风格**：Notion、Figma、Linear、Vercel、Stripe、Apple、Tesla、Spotify、GitHub、Discord、Slack、Telegram、Alibaba、ByteDance、Tencent、Ant Design、Huawei、Xiaomi、JD、Meituan、Shopify、Amazon、Taobao 等
- **智能项目检测**：自动识别 Vite/Next.js/Nuxt.js/Remix/SvelteKit/Tailwind/CRA 等项目类型
- **自动风格推荐**：根据内容类型（教育/文档/电商）推荐最佳风格
- **实时预览**：生成增强版预览页，支持暗色模式、响应式测试、交互式色彩调整
- **智能 CSS 注入**：支持多种框架，自动处理构建项目
- **Tailwind 配置生成**：自动生成 tailwind.config.js 配置（含颜色、字体、圆角、阴影）
- **Design Tokens 导出**：支持 JSON/JS 格式的设计令牌
- **组件代码片段**：自动生成按钮、卡片、表单等组件代码
- **A/B 风格对比**：并排对比两种风格效果
- **中国厂商风格**：支持 Alibaba、ByteDance、Tencent、Ant Design、Huawei、Xiaomi、JD、Meituan 风格
- **电商风格**：支持 Shopify、Amazon、Taobao 风格

## 使用方法

### 基础用法
```bash
# 指定风格
py skills/beautify-ui/scripts/beautify.py <项目路径> linear

# 智能推荐（自动检测并推荐最佳风格）
py skills/beautify-ui/scripts/beautify.py <项目路径> --auto

# 生成实时预览页（不修改原项目）
py skills/beautify-ui/scripts/beautify.py <项目路径> apple --preview

# 查看帮助
py skills/beautify-ui/scripts/beautify.py --help
```

### 使用示例
```bash
# 示例 1：教育网站美化（自动推荐 Notion 风格）
py skills/beautify-ui/scripts/beautify.py C:\projects\edu-site --auto

# 示例 2：技术文档美化（指定 Vercel 风格）
py skills/beautify-ui/scripts/beautify.py C:\projects\docs vercel

# 示例 3：生成 Apple 风格预览页
py skills/beautify-ui/scripts/beautify.py C:\projects\my-site apple --preview

# 示例 4：批量处理多个项目
for project in project1 project2 project3; do
  py skills/beautify-ui/scripts/beautify.py C:\projects\$project linear
done
```

## 支持的 30 种风格

### 教育文档类（4 种）
- `notion` - 温暖简约，适合教育/文学/阅读
- `vercel` - 黑白科技感，适合技术文档/API
- `claude` - 温暖陶土色，适合阅读写作
- `cursor` - 暗黑编辑器风，适合开发工具

### 创意设计类（5 种）
- `figma` - 活泼多彩，适合互动/创意/年轻
- `elevenlabs` - 暗黑电影感，适合音频/媒体
- `spotify` - 绿黑音乐风，适合娱乐媒体
- `airbnb` - 珊瑚旅行风，适合生活摄影
- `bytedance` - 字节跳动渐变活力，适合社交/短视频

### 工具效率类（4 种）
- `linear` - 极简精准，适合工具/逻辑/效率
- `raycast` - 暗铬渐变，适合效率工具
- `superhuman` - 高级键盘流，适合邮件效率
- `ollama` - 终端单色，适合极客开发者

### 商务金融类（5 种）
- `stripe` - 专业紫色，适合商务/金融/企业
- `tesla` - 未来科技感，适合汽车/科技
- `apple` - 高级留白电影感，适合高端零售
- `github` - 开发者友好，适合代码/开源
- `antdesign` - 蚂蚁金服企业级，适合企业/后台/中台

### 社交娱乐类（4 种）
- `discord` - 社交娱乐，活力社区
- `slack` - 协作办公，色彩丰富
- `telegram` - 简洁快速，蓝色为主
- `tencent` - 腾讯蓝色社交，适合即时通讯

### 中国厂商类（8 种）
- `alibaba` - 阿里云橙色科技，适合云服务/企业
- `bytedance` - 字节跳动渐变活力，适合社交/短视频
- `tencent` - 腾讯蓝色社交，适合即时通讯
- `antdesign` - 蚂蚁金服企业级，适合企业/后台/中台
- `huawei` - 华为红色科技，适合企业/云服务
- `xiaomi` - 小米橙色活力，适合科技/硬件
- `jd` - 京东红白信任，适合电商/数码
- `meituan` - 美团黄色生活，适合外卖/旅游

### 电商生活类（3 种）
- `shopify` - 简洁专业电商风，适合在线商店
- `amazon` - 橙黑电商风，适合零售/市场
- `taobao` - 淘宝活力橙色，适合购物/拍卖

## 输出内容

执行后生成：

1. **DESIGN.md** - 完整设计规范文档
   - 色彩系统
   - 字体规范
   - 组件样式
   - 布局原则

2. **styles/theme-override.css** - CSS 变量覆盖文件
   - 全局样式覆盖
   - 组件样式优化
   - 使用 `!important` 确保优先级

3. **assets/theme-override.css** - 构建项目专用（如适用）
   - 自动复制到 assets 目录
   - 支持 Vite/Next.js/Nuxt.js/Remix/SvelteKit/CRA 项目

4. **preview-{style}.html** - 实时预览页（使用 --preview 时）
   - 完整 HTML 页面
   - 交互式色彩系统（实时调整主色调）
   - 暗色/亮色模式切换
   - 响应式断点测试工具
   - 按钮/卡片/表格/表单等组件展示

5. **tokens.json / tokens.js** - Design Tokens（使用 --tokens 时）
   - JSON/JS 格式的设计令牌
   - 包含颜色、字体、圆角、阴影等

6. **snippets/** - 组件代码片段（使用 --snippets 时）
   - button.html - 按钮组件代码
   - card.html - 卡片组件代码
   - form.html - 表单组件代码

7. **compare-{styleA}-vs-{styleB}.html** - A/B 风格对比页（使用 --compare 时）
   - 并排对比两种风格
   - 支持单独查看 A 或 B

## 智能检测能力

自动识别：
- **项目类型**：Static HTML / Vite / Next.js / Nuxt.js / Remix / SvelteKit / Create React App
- **样式系统**：Tailwind CSS / CSS Modules / Styled Components / Emotion
- **预处理器**：SCSS / Less
- **内容类型**：教育/文档/电商/通用

根据检测结果：
- 推荐最适合的风格
- 选择正确的 CSS 注入策略
- 处理构建项目的特殊需求

## 适用场景

- ✅ 快速美化教育网站/学习平台
- ✅ 为技术文档应用专业风格
- ✅ 电商网站风格统一
- ✅ 企业官网视觉升级
- ✅ 个人博客美化
- ✅ 原型设计快速出效果
- ✅ A/B 测试不同风格效果

## 注意事项

⚠️ **重要提示**：
1. 本技能会修改项目文件，建议先备份或使用 Git
2. 构建项目（Vite/Next.js）需要手动添加 CSS 引用
3. 预览页会生成在项目目录中，可手动删除
4. 使用 `--preview` 参数不会修改原项目

💡 **最佳实践**：
- 首次使用建议先用 `--auto` 让技能推荐风格
- 使用 `--preview` 查看效果后再应用
- 生产环境使用前先在开发环境测试
- 保留 DESIGN.md 作为项目文档

## 技术细节

### 架构设计
- **单文件结构**：为保持脚本可移植性，采用单文件设计
- **零外部依赖**：仅使用 Python 3.8+ 标准库
- **模块化函数**：虽然在同一文件，但函数职责清晰分离

### 项目类型检测
- 读取 `package.json` 判断框架（Vite/Next.js/CRA）
- 扫描依赖检测 Tailwind CSS
- 分析文件结构识别 CSS Modules

### CSS 注入策略
1. 生成 CSS 变量（`:root`）
2. 全局覆盖（使用 `!important`）
3. 针对组件选择器优化
4. 构建项目自动复制到 `assets/`

### 预览页生成
- 完整 HTML 页面（含样式）
- 交互式色彩系统展示
- 按钮/卡片效果演示
- 对比区域（修改前后）

## 更新日志

### v3.3.0 (2026-04-22)
- ✨ 新增 3 种电商风格：Shopify、Amazon、Taobao
- ✨ 新增 4 种中国厂商风格：Huawei、Xiaomi、JD、Meituan
- ✨ 增强预览页：交互式色彩系统、暗色/亮色模式切换、响应式断点测试
- ✨ 新增组件展示：表格、标签页、进度条、日期选择器
- ✨ 扩展框架支持：Nuxt.js、Remix、SvelteKit
- ✨ 新增 CSS-in-JS 检测：Styled Components、Emotion
- ✨ 新增 SCSS/Less 配置文件生成支持
- ✨ 新增 Design Tokens 导出功能（JSON/JS 格式）
- ✨ 新增组件代码片段生成（按钮、卡片、表单）
- ✨ 新增 A/B 风格对比功能
- ✨ 新增 --dry-run 预览模式
- ✨ 更新文档，风格数量更新为 30 种

### v3.2.0 (2026-04-22)
- ✨ 新增 4 种中国厂商风格：Alibaba Cloud、ByteDance、Tencent、Ant Design
- ✨ 实现 Tailwind 配置自动生成功能（tailwind.config.js）
- 📝 更新文档，风格数量更新为 23 种

### v3.1.0 (2026-04-21)
- ✨ 新增 4 种流行风格：GitHub、Discord、Slack、Telegram
- ✨ 实现 `--help` 参数功能
- 🐛 修复 Tesla 风格颜色不完整问题
- 🐛 修复宽泛异常捕获问题（改为捕获具体异常）
- ♻️ 重构变量命名，将 `template` 改为 `style_data` 避免歧义
- 📝 更新 SKILL.md 文档，修正风格数量（16→19）

### v3.0.1 (2026-04-14)
- 📝 完善 SKILL.md 文档
- 📝 添加详细使用示例
- 📝 补充风格列表说明
- 📝 添加注意事项和最佳实践

### v3.0.0 (2026-04-14)
- ✨ 新增实时预览功能（--preview）
- ✨ 风格库扩展至 16 种
- ✨ 智能项目检测（Vite/Next.js/Tailwind）
- ✨ 自动风格推荐
- 🐛 修复构建项目 CSS 注入问题
- 🐛 优化 Windows 编码兼容性

### v2.0.0
- ✨ 智能项目检测
- ✨ 自动风格推荐
- ✨ Tailwind 配置支持

### v1.0.0
- 🎉 初始版本发布
- 5 种基础风格

## 文件结构

```
beautify-ui/
├── SKILL.md              # 技能说明（本文件）
├── README.md             # 使用文档
├── scripts/
│   └── beautify.py       # 核心脚本（v3.1）
```

## 致谢

灵感来自 [awesome-design-md](https://github.com/VoltAgent/awesome-design-md) 项目，感谢 VoltAgent 团队的出色工作！

## 许可证

MIT License

## 支持与贡献

- **问题反馈**：欢迎提交 Issue
- **风格建议**：欢迎 PR 新风格
- **功能建议**：欢迎讨论改进方案

---

**作者**：OpenClaw Community
**版本**：3.3.0
**最后更新**：2026-04-22
