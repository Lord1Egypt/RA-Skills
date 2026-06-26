# Daily News Brief - 上传文件说明

## 文件夹位置
```
/Users/lezi/skills/daily-news-brief-upload/
```

## 文件列表

### 核心文件
- **skill.json** - OpenClaw skill 配置文件
- **index.ts** - 主程序入口
- **types.ts** - 类型定义
- **package.json** - 依赖配置
- **tsconfig.json** - TypeScript 配置

### 配置文件
- **config/default.json** - 默认配置
- **openclaw-config.json** - OpenClaw 特定配置

### 功能模块
- **source_fetchers/** - 新闻源抓取模块
  - base.ts - 基础类
  - cls.ts - 财联社
  - ithome.ts - IT之家
  - 36kr.ts - 36氪
  - index.ts - 模块入口

- **normalizer/** - 数据标准化模块
- **deduper/** - 去重模块
- **classifier/** - 分类模块
- **rewriter/** - 改写模块
- **ranker/** - 排序模块
- **scheduler/** - 定时任务模块
- **deliverer/** - 推送模块

### 文档
- **README.md** - 技能说明文档
- **Skill.md** - 技能详细文档
- **README-upload.md** - 上传说明文档
- **UPLOAD-INSTRUCTIONS.md** - 本文件

### 脚本
- **install.sh** - 安装脚本

### 其他
- **daily-news-brief.tar.gz** - 打包的技能文件（可选）

## 上传步骤

1. **选择上传方式**
   - 方式一：上传整个 `daily-news-brief-upload` 文件夹
   - 方式二：只上传 `daily-news-brief.tar.gz` 压缩包

2. **如果上传文件夹**
   ```bash
   # 在 OpenClaw 中解压
   cd /path/to/skills
   cp -r daily-news-brief-upload daily-news-brief
   cd daily-news-brief
   ```

3. **如果上传压缩包**
   ```bash
   # 在 OpenClaw 中解压
   tar -xzf daily-news-brief.tar.gz
   ```

4. **安装依赖**
   ```bash
   npm install
   ```

5. **注册技能**
   ```bash
   daily-news-brief register
   ```

6. **配置 Telegram**
   ```bash
   set config.telegram_chat_id "YOUR_CHAT_ID"
   set config.telegram_bot_token "YOUR_BOT_TOKEN"
   ```

7. **测试运行**
   ```bash
   daily-news-brief test
   ```

## 注意事项
- 确保 OpenClaw 支持 TypeScript 和 Node.js
- 需要互联网权限来抓取新闻
- 需要文件系统权限来读取配置
- 使用前已预配置 Telegram 发送功能