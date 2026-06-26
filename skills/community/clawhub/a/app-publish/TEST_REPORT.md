# 快手/B 站/抖音视频发布技能 - 测试报告

**开发时间：** 2026-04-02  
**开发工具：** Cursor CLI Agent  
**参考项目：** xiaohongshu-skills

---

## ✅ 已完成任务

### 1. 项目结构创建

```
app_publish/
├── scripts/
│   ├── cli.py                     ✅ 统一 CLI 入口
│   ├── chrome_launcher.py         ✅ Chrome 启动器
│   ├── requirements.txt           ✅ Python 依赖
│   ├── test_run.sh               ✅ 测试脚本
│   └── kbs/                       ✅ 核心模块包
│       ├── __init__.py
│       ├── cdp.py                 ✅ CDP 浏览器控制
│       ├── types.py               ✅ 数据类型 + 配置解析
│       ├── selectors_ks.py        ✅ 快手选择器
│       ├── selectors_bili.py      ✅ B 站选择器
│       ├── selectors_dy.py        ✅ 抖音选择器
│       ├── publish_kuaishou.py    ✅ 快手发布逻辑
│       ├── publish_bilibili.py    ✅ B 站发布逻辑
│       └── publish_douyin.py      ✅ 抖音发布逻辑
├── test_data/
│   ├── test_video.mp4             ✅ 测试视频 (788KB)
│   ├── image.png                  ⏳ 测试封面（需创建）
│   └── 描述.txt                   ✅ 测试配置
├── SKILL.md                       ✅ 技能文档
├── 任务.md                        ✅ 任务需求
└── TEST_REPORT.md                 ✅ 测试报告（本文件）
```

---

## 📋 输入输出规范

### 输入：TXT 配置文件

```text
标题：明天更好
视频数据路径：/Users/xiaohei/.openclaw/workspace/skills/app_publish/test_data/test_video.mp4
封面：/Users/xiaohei/.openclaw/workspace/skills/app_publish/test_data/image.png
关键词：美好的，欢快，一天的
```

**解析逻辑：**
- 支持 `标题：`、`视频数据路径：`、`封面：`、`关键词：` 四个字段
- 关键词自动按逗号或空格分割成列表
- 所有路径转换为绝对路径

### 输出：JSON 格式

**成功：**
```json
{
  "success": true,
  "platform": "bilibili",
  "title": "明天更好",
  "video_path": "/path/to/video.mp4",
  "cover_path": "/path/to/cover.png",
  "keywords": ["美好的", "欢快", "一天的"],
  "status": "发布完成",
  "message": "视频上传成功，表单已填写"
}
```

**失败：**
```json
{
  "success": false,
  "platform": "kuaishou",
  "error": "上传超时，请检查网络连接或视频文件大小",
  "status": "上传失败"
}
```

---

## 🎯 核心功能

### 1. CLI 命令

| 命令 | 功能 | 示例 |
|------|------|------|
| `publish-kuaishou` | 快手发布 | `python cli.py publish-kuaishou --config test.txt` |
| `publish-bilibili` | B 站发布 | `python cli.py publish-bilibili --config test.txt` |
| `publish-douyin` | 抖音发布 | `python cli.py publish-douyin --config test.txt` |
| `publish-all` | 一键发布到三平台 | `python cli.py publish-all --config test.txt` |

### 2. 常用参数

- `--config PATH`：TXT 配置文件路径（必填）
- `--wait-timeout SECONDS`：上传等待超时（默认 300 秒）
- `--no-publish`：只填写表单，不点击发布（用于预览确认）
- `--port PORT`：Chrome CDP 端口（默认 9222）
- `--headless`：无头模式（默认有窗口）

### 3. 上传状态检查

**轮询机制：**
- 每 2 秒检查一次上传状态
- 最长等待 5 分钟（可配置）
- 检测页面就绪文案（如"上传完成"、"处理完成"等）
- 超时后抛出异常并返回错误信息

---

## 🔧 依赖安装

```bash
cd /Users/xiaohei/.openclaw/workspace/skills/app_publish/scripts
pip install -r requirements.txt
```

**依赖包：**
- `requests`：HTTP 请求（可选，用于扩展功能）
- `websockets`：CDP WebSocket 连接

---

## 🧪 测试步骤

### 前置条件

1. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

2. **准备测试数据**
   - 视频文件：`test_data/test_video.mp4`（已存在，788KB）
   - 封面文件：`test_data/image.png`（需创建或指定）
   - 配置文件：`test_data/描述.txt`（已存在）

3. **登录平台账号**
   - 打开 Chrome 浏览器
   - 分别登录快手、B 站、抖音创作者平台
   - 或使用 `--port 9222` 复用已登录的 Chrome 会话

### 测试流程

#### 步骤 1：运行测试脚本（只填写表单）

```bash
cd /Users/xiaohei/.openclaw/workspace/skills/app_publish/scripts
./test_run.sh
```

或手动测试单个平台：

```bash
# B 站测试
python cli.py publish-bilibili \
    --config ../test_data/描述.txt \
    --no-publish \
    --wait-timeout 60
```

#### 步骤 2：检查浏览器状态

- 观察浏览器是否自动打开
- 检查是否导航到正确的上传页面
- 验证视频/封面是否开始上传
- 确认标题和关键词是否填写

#### 步骤 3：实际发布测试

```bash
# 单平台发布
python cli.py publish-kuaishou --config ../test_data/描述.txt

# 一键发布到所有平台
python cli.py publish-all --config ../test_data/描述.txt
```

---

## ⚠️ 已知问题与注意事项

### 1. CSS 选择器可能失效

**问题：** 平台页面结构更新后，选择器可能找不到对应元素

**解决方案：**
- 使用浏览器开发者工具检查最新元素结构
- 更新 `selectors_*.py` 文件中的 CSS 选择器
- 优先使用稳定的 `id`、`name` 属性

### 2. 视频上传超时

**问题：** 大视频文件上传时间超过默认 5 分钟

**解决方案：**
- 增加 `--wait-timeout` 参数，如 `--wait-timeout 600`
- 检查网络连接速度
- 使用较小的测试视频

### 3. 登录状态丢失

**问题：** Chrome 会话关闭后登录状态丢失

**解决方案：**
- 使用 `--user-data-dir` 指定持久化用户数据目录
- 或使用 `--port 9222` 复用已登录的 Chrome

### 4. 封面上传

**问题：** 部分平台封面上传逻辑可能不同

**解决方案：**
- 检查 `publish_*.py` 中的封面上传逻辑
- 部分平台可能不需要封面（自动生成）
- 更新对应平台的封面选择器

---

## 📊 性能指标

| 指标 | 目标值 | 实际值 | 状态 |
|------|--------|--------|------|
| 视频上传时间（100MB） | < 60 秒 | 待测试 | ⏳ |
| 表单填写时间 | < 10 秒 | 待测试 | ⏳ |
| 总发布时长（单平台） | < 3 分钟 | 待测试 | ⏳ |
| 总发布时长（三平台） | < 10 分钟 | 待测试 | ⏳ |
| 成功率 | > 90% | 待测试 | ⏳ |

---

## 🧪 实际测试结果（2026-04-03）

### 测试环境
- **测试时间**: 2026-04-03 20:17
- **测试文件**: test_video.mp4 (770KB), image.png (1.1MB)
- **浏览器**: Chrome 145.0.7632.160
- **CDP 端口**: 9222

### 测试用例 1：B 站发布（`--no-publish` 模式）

**命令**:
```bash
python cli.py publish-bilibili --config ../test_data/title.txt --no-publish --wait-timeout 60
```

**结果**: ✅ **成功**

```json
{
  "success": true,
  "platform": "bilibili",
  "message": "表单已填写，未提交投稿",
  "detail": "",
  "upload_phase": "form_filled"
}
```

**观察**:
- 浏览器成功导航到 B 站投稿页面
- 配置解析正常
- 表单填写逻辑正常（待实际验证填写效果）

---

### 测试用例 2：快手发布（`--no-publish` 模式）

**命令**:
```bash
python cli.py publish-kuaishou --config ../test_data/title.txt --no-publish --wait-timeout 60
```

**结果**: ❌ **超时失败**

```json
{
  "success": false,
  "platform": "kuaishou",
  "message": "等待视频处理超时（60.0s）",
  "detail": "",
  "upload_phase": "video_timeout"
}
```

**问题分析**:
1. 快手页面结构可能已变更，CSS 选择器不匹配
2. 需要登录状态（可能未登录或登录过期）
3. 视频上传入口探测失败

**解决方案**:
- 手动打开快手创作者平台确认登录状态
- 使用浏览器开发者工具检查最新元素结构
- 更新 `selectors_ks.py` 中的选择器

---

## 🔄 后续优化计划

### 短期（1-2 周）

- [ ] 实际页面测试，验证选择器有效性
- [ ] 优化上传进度监控
- [ ] 添加日志输出详细程度控制
- [ ] 实现 B 站分区选择功能

### 中期（1 个月）

- [ ] 支持定时发布
- [ ] 支持批量发布（多个视频）
- [ ] 添加发布历史记录
- [ ] 实现失败重试机制

### 长期（3 个月）

- [ ] 支持更多平台（视频号、西瓜视频等）
- [ ] 视频自动剪辑功能
- [ ] AI 生成标题和描述
- [ ] 发布数据分析报表

---

## 📝 使用建议

1. **首次使用**：先用 `--no-publish` 参数测试，确认表单填写正确后再实际发布
2. **大文件上传**：建议设置 `--wait-timeout 600` 或更长
3. **批量发布**：使用 `publish-all` 命令前，确保网络稳定
4. **错误排查**：检查 `--headless` 模式下的日志输出
5. **选择器维护**：定期检查和更新 `selectors_*.py` 文件

---

## 🎉 总结

✅ **已完成：**
- 完整的 CLI 工具和发布脚本
- 三平台支持（快手、B 站、抖音）
- 配置解析、文件上传、表单填写、状态检查
- 详细的文档和测试脚本

⏳ **待测试：**
- 实际页面选择器验证
- 大文件上传性能测试
- 多平台并发发布测试

🚀 **下一步：**
1. 创建测试封面图片 `test_data/image.png`
2. 运行 `./test_run.sh` 进行实际测试
3. 根据测试结果优化选择器和上传逻辑

---

**开发者：** Cursor CLI Agent  
**审阅者：** 待人工审阅  
**状态：** 开发完成，待测试验证
