# 常见问题排查

| 问题 | 原因 | 处理 |
|---|---|---|
| 找不到上传器 | 依赖 Skill 未安装到同一 skills 根目录 | 安装 `upload-markdown-to-lexiang`，或设置 `LEXIANG_UPLOADER_HOME` |
| `cli_api` 不兼容 | 公共上传器版本不匹配 | 安装 `>=1.1.0,<2.0.0` |
| `AUTH_ERROR` | 尚未配置、已撤销或已失效的个人凭证 | 访问 https://lexiangla.com/ai/claw，运行 `auth login` |
| `PREFLIGHT_ERROR: 缺少图片文件` | Markdown 路径和实际下载文件不一致 | 修正引用或重新抓图，禁止删除图片引用规避 |
| `VERIFY_ERROR` | 线上标题、正文锚点、图片或公式与本地不一致 | 保留本地产物，修复公共上传器并重试 |
| 非中文文章未加工 | 未调用公共内容加工 Skill | 将工作包交给 `trans-doc-to-md` Prepared Markdown Package 模式 |
| 图后标题变普通段落 | 图片后的文本段以 `---` 开头 | 删除分隔线并重新上传 |
| CDP 打开 Testing Chrome | 9222 CDP Chrome 未正确连接 | 启动持久化 CDP Profile，禁止空登录态降级 |
| Whisper/native 库签名失败 | Agent 沙箱限制 | 申请沙箱外执行；不得静默用 Show Notes 冒充转录 |

## 上传器问题归属

以下问题必须在 `upload-markdown-to-lexiang` 中修复并补测试：

- Markdown 或图片路径解析
- 图文顺序
- 表格和公式转换
- page 创建或覆盖
- 个人凭证校验、过期提示和续期
- 线上标题、锚点、图片数和公式对账
- `trans-doc-to-md` 富元素标注的直接渲染

禁止把 `lexiang_upload.py` 复制回本 Skill 临时修补。
