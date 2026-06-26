# bie-zheng-luan-prototype (别整乱原型分析技能)

> **作者**: 杰哥 | **主页**: https://clawhub.ai/skills/bie-zheng-luan-prototype | **源码**: https://github.com/jermyn-zmj/bie-zheng-luan-prototype

将产品原型转换为详细技术规范的技能，支持4种输入类型：URL原型、本地HTML文件、图片原型、XMind文件。新增交互式业务分析功能，可从原型推断业务流程。

## 🎯 功能特性

### ✅ 支持的输入类型
1. **URL原型** - Figma、墨刀、Axure、蓝湖等设计工具的公开/内网链接
2. **本地HTML文件** - 导出的HTML原型文件、本地保存的网页原型
3. **图片原型** - 设计稿截图、高保真原型图（PNG/JPG/WebP等）
4. **XMind文件** - 产品功能脑图、信息架构图

### ✅ 核心能力
- **智能解析**：自动识别输入类型并选择相应解析方式
- **深度HTML解析**：提取菜单、筛选条件、表格列、操作按钮、状态Tab、抽屉面板等完整信息
- **多UI框架适配**：自动检测并适配企业后台、标准后台、移动端H5等UI框架
- **交互式业务分析**：从原型推断业务流程、状态流转，生成问题让用户确认
- **功能拆解**：将原型元素拆解为前端组件、后端接口、数据库设计
- **技术文档生成**：输出完整的技术规范文档
- **多格式支持**：HTML、图片、思维导图全面覆盖

## 📦 安装

### 通过OpenClaw安装
```bash
openclaw skills install https://clawhub.ai/skills/bie-zheng-luan-prototype
```

### 手动安装
```bash
# 克隆仓库
git clone https://github.com/[your-username]/bie-zheng-luan-prototype.git

# 复制到技能目录
cp -r bie-zheng-luan-prototype ~/.openclaw/workspace/skills/
```

## 🚀 使用方法

### 基本调用
当用户提供原型时，直接使用本技能：

```bash
# 分析URL原型
分析这个Figma原型：https://www.figma.com/file/xxx

# 分析本地HTML文件
分析这个HTML原型文件：/path/to/prototype.html

# 分析图片原型
分析这张设计稿截图：/path/to/design.png

# 分析XMind文件
分析这个产品脑图：/path/to/product.xmind
```

### HTML分析输出格式
```bash
# 标准分析报告（默认）
python scripts/html-extractor.py prototype.html markdown

# JSON格式数据
python scripts/html-extractor.py prototype.html json

# 交互式业务分析（包含流程推断和问题）
python scripts/html-extractor.py prototype.html interactive
```

### 输入类型自动识别
技能会根据输入内容自动判断解析方式：

| 输入内容 | 识别方式 | 解析方式 |
|---------|---------|---------|
| `https://...` 或 `http://...` | 以http/https开头 | URL原型解析 |
| `/path/to/file.html` | 文件路径，以.html结尾 | 本地HTML文件解析 |
| `<!DOCTYPE html>...` | 以HTML标签开头 | 直接解析粘贴的HTML内容 |
| `/path/to/file.png/.jpg/.jpeg/.gif/.webp/.bmp` | 图片格式文件路径 | 图片原型解析 |
| `/path/to/file.xmind` | .xmind后缀文件路径 | XMind文件解析 |

## 📋 输出文档

技能会生成包含以下内容的技术规范文档：

### 1. 系统概览
- 原型来源和类型
- 分析时间和版本
- 总体功能描述
- 技术栈建议

### 2. 页面结构分析
- 布局分解（头部、侧边栏、主内容区、底部）
- 功能模块清单
- 交互元素识别

### 3. 业务流程分析（交互式模式）
- 业务流程顺序（页面流转图）
- 每个页面的操作列表和执行条件
- 状态流转规则（状态机图）
- 关键字段和筛选维度
- 需要用户确认的问题清单

### 4. 前端实现方案
- 页面路由规划
- 组件清单（名称、props、状态、交互逻辑）
- 样式方案（CSS框架、设计系统）
- 交互细节

### 5. 后端实现方案
- API接口设计（路由、HTTP方法、参数、返回值）
- 业务逻辑伪代码
- 数据库表设计
- 第三方服务集成

### 6. 开发注意事项
- 技术栈建议
- 特殊依赖说明
- 性能和安全考虑
- 测试要点

## 🔧 内置工具

### 脚本文件及功能说明

| 脚本文件 | 功能 | 网络访问 | 文件操作 | 安全措施 |
|---------|------|---------|---------|---------|
| `url-prototype-analyzer.sh` | URL原型解析主脚本 | curl/wget下载公开URL | 读取HTML、写入输出文件 | URL验证、SSRF检测、命令注入防护 |
| `run_analysis.sh` | 本地HTML综合分析入口 | 无 | 读取本地HTML、写入输出文件 | 路径验证、敏感路径警告 |
| `html-extractor.py` | HTML内容深度提取 | 无 | 读取HTML文件 | 纯Python解析，无外部调用 |
| `html_extractor/analyzer.py` | 业务流程分析 | 无 | 无 | 纯Python分析 |
| `spec-generator.py` | 技术文档生成 | 无 | 写入输出文件 | 纯Python生成 |
| `image-prototype-analyzer.py` | 图片原型分析 | 仅在设置ANTHROPIC_API_KEY时调用Claude API | 读取图片文件 | 默认本地分析，外部API需手动启用 |
| `xmind-analyzer.py` | XMind文件分析 | 无 | 读取.xmind文件（zip解压） | 纯Python解析 |

**脚本详细行为说明：**

1. **url-prototype-analyzer.sh**
   - 仅下载用户提供的原型URL（http/https协议）
   - 内网URL默认阻止，需 `--allow-internal` 参数确认
   - 不执行任何 pip install 命令
   - 所有输入参数经过严格验证

2. **run_analysis.sh**
   - 仅处理本地文件，无网络访问
   - 路径验证防止命令注入
   - 敏感路径（.ssh/.env/.git等）会发出警告

3. **image-prototype-analyzer.py**
   - 默认使用本地分析（颜色提取、布局推断），无数据传输
   - 设置 `ANTHROPIC_API_KEY` 后可启用视觉增强分析（图片会发送到Anthropic服务器）

### 参考模板
- `references/template-spec.md` - 技术规范文档模板
- `references/component-catalog.md` - 前端组件目录
- `references/api-design.md` - API设计规范

### 示例输出
- `assets/sample-output/sample-user-management.md` - 用户管理系统示例

## 📊 技术架构

### 解析流程
```
输入识别 → 内容解析 → 业务分析 → 功能拆解 → 文档生成 → 输出保存
```

### 依赖要求
- **Python 3.8+**
- **Python包（核心）**：
  - `beautifulsoup4` (HTML解析)
  - `lxml` (HTML解析器)
  - `Pillow` (图片处理)
- **Python包（可选，用于增强功能）**：
  - `anthropic` (Claude Vision API，用于图片原型精确分析) — 需设置 `ANTHROPIC_API_KEY`
  - `opencv-python` (高级图像处理)

### 文件结构
```
bie-zheng-luan-prototype/
├── SKILL.md                    # 技能主文件
├── README.md                   # 说明文档
├── LICENSE                     # MIT许可证
├── skill.json                  # 技能元数据
├── scripts/                    # 分析脚本
│   ├── url-prototype-analyzer.sh
│   ├── html-extractor.py       # HTML提取入口
│   ├── html_extractor/         # HTML解析核心模块包
│   │   ├── config.py           # UI框架配置
│   │   ├── models.py           # 数据结构定义
│   │   ├── detector.py         # UI框架检测器
│   │   ├── extractor.py        # 核心解析器
│   │   ├── analyzer.py         # 业务流程分析器
│   │   ├── utils.py            # 辅助函数
│   │   └── main.py             # 入口函数
│   ├── spec-generator.py       # 技术文档生成工具
│   ├── image-prototype-analyzer.py
│   ├── xmind-analyzer.py
│   └── run_analysis.sh
├── references/                 # 参考模板
│   ├── template-spec.md
│   ├── component-catalog.md
│   └── api-design.md
├── assets/                     # 资源文件
│   └── sample-output/
│       └── sample-user-management.md
└── requirements.txt            # Python依赖
```

## 🎨 示例场景

### 示例1：用户管理系统原型
**输入**：Figma用户管理后台URL

**输出包含**：
- 前端：用户列表组件、用户表单组件、权限选择组件
- 后端：用户CRUD接口、权限验证接口、搜索接口
- 数据库：users表、roles表、user_roles关联表

### 示例2：电商商品页面原型  
**输入**：墨刀电商商品详情页URL

**输出包含**：
- 前端：商品展示组件、购物车组件、评价组件
- 后端：商品查询接口、购物车接口、下单接口
- 数据库：products表、categories表、orders表

### 示例3：业务流程分析（交互式模式）
**输入**：本地HTML原型文件

**输出包含**：
- 业务流程顺序（页面流转图）
- 每个页面的操作列表和执行条件
- 状态流转规则（状态机图）
- 关键字段和筛选维度
- 需要用户确认的问题清单

## 🛡️ 安全措施

本技能实施了严格的安全防护：

### 内网URL控制
- **默认阻止**：私有网络地址自动拒绝
- **用户确认**：需 `--allow-internal` 参数才能访问内网
- 检测范围：localhost、127.x、10.x、172.16-31.x、192.168.x

### 外部API控制
- **默认禁用**：未设置 `ANTHROPIC_API_KEY` 不调用外部API
- **主动触发**：仅在用户设置环境变量后启用
- 图片分析默认使用本地基础功能

### 无自动安装
- Shell脚本**不执行** `pip install`
- 仅检查依赖，提示用户手动安装
- 避免运行时写入操作

### 命令注入防护
- URL验证：只允许http/https协议
- 阻止Shell特殊字符
- 长度限制：URL最大2048字符

---

## ⚠️ 安全注意事项

> 🔴 **使用前必读**：本技能涉及网络访问和可选外部API调用，请理解以下风险：

### 内网URL访问控制
- 内网URL**默认被阻止**
- 需使用 `--allow-internal` 参数确认后才能访问
- 请勿分析不应访问的内部系统

### 外部API数据传输
- 视觉增强分析需设置 `ANTHROPIC_API_KEY`
- **默认禁用**：未设置环境变量时不调用外部API
- 启用后图片会发送到Anthropic服务器

### 本地文件访问
- 技能会读取您指定的本地文件路径
- 请确保路径指向预期文件

### 首次使用建议
- **手动安装依赖**：`pip install beautifulsoup4 pillow lxml`（脚本不会自动安装）
- 检查 `scripts/` 目录下的脚本内容
- 在隔离环境中首次测试

## 🔄 版本历史

### v3.1.0 (2026-05-18)
- ✅ 优化交互式分析：改进页面名称匹配（通过菜单page_id匹配view_id）
- ✅ 过滤无效按钮（去重和过滤纯图标按钮）
- ✅ 清理状态Tab名称（分离名称和数量）
- ✅ 增强UI框架适配（新增scm-view容器模式）

### v3.0.0 (2026-05-18)
- ✅ **新增交互式业务分析功能**
- ✅ 从原型推断业务流程和状态流转
- ✅ 生成问题让用户确认，循环迭代直到理解完整业务逻辑
- ✅ 新增BusinessFlowAnalyzer模块

### v2.9.2 (2026-04-29)
- ✅ 增强文档透明度：补充脚本功能详细说明表格（网络访问、文件操作、安全措施）
- ✅ 补充作者信息和项目链接在README顶部
- ✅ 响应平台安全审查建议，提高脚本行为透明度

### v2.9.1 (2026-04-29)
- ✅ 修复spec-generator.py的Python 3.7兼容性问题（`str | None`改为`Optional[str]`）

### v2.9.0 (2026-04-29)
- ✅ **完全通用化重构**：移除所有硬编码的业务专有名词
- ✅ 动态生成路由、API接口、数据库表，不依赖特定业务词汇映射
- ✅ 可适配任何业务领域原型（仓储、ERP、WMS、CMS、CRM等）

### v2.8.0 (2026-04-29)
- ✅ **增强技术实现推断**：智能路由解析（处理javascript:void(0)等特殊值）
- ✅ 增强按钮位置识别（多层级父元素检查）
- ✅ 业务API接口推断、完整数据库表设计、实体关系图、状态枚举定义

### v2.7.0 (2026-04-29)
- ✅ **模块化重构**：将 html-extractor.py (2000+行) 拆分为 html_extractor 包（7个模块）
- ✅ 提高代码可维护性和可读性

### v2.6.0 (2026-04-24)
- ✅ 补充弹窗/抽屉面板解析：弹窗内表单字段、锚点导航、统计信息
- ✅ 补充状态筛选Tab、进度条组件解析

### v2.5.0 (2026-04-24)
- ✅ 补充缺失解析模块：消息通知卡片、人员进度卡片、页面标签栏
- ✅ 优化表格层级识别和数据类型推断

### v2.4.0 (2026-04-24)
- ✅ 重写HTML解析器，深度提取菜单结构、筛选条件、表格列、操作按钮
- ✅ 支持多页面视图识别和独立分析

### v2.3.0 (2026-04-23)
- ✅ **内网URL默认阻止**，需 `--allow-internal` 参数确认
- ✅ **禁止自动pip安装**，改为提示用户手动安装
- ✅ **外部API默认禁用**，仅在设置 `ANTHROPIC_API_KEY` 后启用
- ✅ 在skill.json中完善安全措施声明

### v2.2.0 (2026-04-23)
- ✅ 实施命令注入防护（URL/路径输入验证）
- ✅ 添加SSRF检测警告（私有网络地址检测）
- ✅ 添加路径遍历防护（敏感路径检测）
- ✅ 在skill.json中声明安全缓解措施

### v2.1.0 (2026-04-23)
- ✅ 增加安全警告声明（SSRF、数据泄露风险）
- ✅ 在skill.json中声明可选环境变量 `ANTHROPIC_API_KEY`
- ✅ 增加外部服务数据传输警告
- ✅ 提供首次使用安全建议

### v2.0.0 (2026-04-22)
- ✅ 新增本地HTML文件解析支持
- ✅ 新增图片原型分析功能
- ✅ 新增XMind文件解析功能
- ✅ 修复spec-generator.py中的bug
- ✅ 完善技能文档和示例

### v1.0.0 (2026-04-21)
- ✅ 初始版本：URL原型分析功能
- ✅ 基础HTML解析和文档生成

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🤝 贡献

欢迎提交Issue和Pull Request！

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 开启 Pull Request

## 📞 支持

- 问题反馈：[GitHub Issues](https://github.com/jermyn-zmj/bie-zheng-luan-prototype/issues)
- 功能建议：[GitHub Discussions](https://github.com/jermyn-zmj/bie-zheng-luan-prototype/discussions)

---

*让产品原型不再"别整乱"，一键生成技术规范！*
