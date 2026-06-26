# SELF_CHECK

## 1. 规范检查

- [x] Skill 为独立文件夹
- [x] 包含 `SKILL.md`
- [x] `SKILL.md` 使用 YAML frontmatter
- [x] frontmatter 含 `name`
- [x] frontmatter 含 `description`
- [x] frontmatter 含 `version`
- [x] 运行要求写入 `metadata.openclaw`
- [x] 未声明不存在的安装器类型
- [x] 全部附属文件均为文本文件，符合发布要求
- [x] `description` 未使用易触发 YAML 解析歧义的冒号写法

## 2. 必要文件检查

- [x] `README.md`
- [x] `SELF_CHECK.md`
- [x] `scripts/music_skill.py`
- [x] `scripts/smoke_check.py`
- [x] `resources/music_apps.json`
- [x] `resources/recommendation_profiles.json`
- [x] `examples/usage-example.md`
- [x] `tests/smoke-test.md`

## 3. 脚本检查

- [x] 脚本可直接执行
- [x] 命令行参数明确
- [x] 无 TODO / 伪代码
- [x] 有错误处理
- [x] 默认只进行本地可审计操作
- [x] 不依赖未声明的第三方 Python 包
- [x] macOS 控制能力默认仅依赖系统自带 `osascript`；Spotify 精确点播为可选 token 增强

## 4. 资源引用检查

- [x] `scripts/music_skill.py` 真实读取 `resources/music_apps.json`
- [x] `scripts/music_skill.py` 真实读取 `resources/recommendation_profiles.json`

## 5. 安全审计

- [x] 未使用 `curl | bash`
- [x] 未下载远程执行脚本
- [x] 未使用 Base64 混淆执行
- [x] 未尝试读取浏览器 Cookie / token
- [x] 未逆向私有 API
- [x] 文件读写范围仅限 Skill 自身资源和用户明确提供的路径参数
- [x] 对外动作仅为：打开本地程序、打开 URI/URL、将文件或 URL 传给播放器、在 macOS 上调用 AppleScript 控制指定音乐 App

### 安全结论

该 Skill 属于**低到中风险的本地启动与桌面控制类 Skill**。  
风险主要来自“打开用户请求的 URI/URL / 文件路径”和“在 macOS 上驱动桌面自动化”这两类动作，而不是凭证、提权或隐蔽联网行为。  
控制版仍保持可审计：目标应用、动作类型、查询内容和执行结果都在 JSON 返回中可见。

## 6. 热门度与实用性评估

- 高频需求：高
- 理解门槛：低
- 传播性：高
- 二次定制空间：高
- 对特定平台/账号依赖：中
- 长期维护成本：中

## 7. 工程质量评分

| 项目 | 分数(10) | 说明 |
|---|---:|---|
| 规范对齐 | 9 | frontmatter 与目录完整 |
| 可执行性 | 9 | 脚本可直接跑 |
| 兼容性 | 8 | 多平台，多软件，macOS 控制能力更强 |
| 安全性 | 9 | 无高风险安装/执行模式 |
| 可维护性 | 9 | 数据驱动，资源与逻辑分离 |
| 实用性 | 9 | 相比原版新增主动控播 |

## 8. 已知边界

- [x] macOS 下 `control` 可直接控制 Spotify / Apple Music
- [x] macOS 下 `play <query>` 可走 UI 自动化模式
- [ ] Windows / Linux 仍以打开与搜索为主，后续可加可选控制插件层
- [x] Spotify 在提供 access token 时可先精确搜索首个匹配 track URI 再触发播放
- [ ] “按 query 精准命中某首歌并保证开播”仍受客户端版本、订阅、版权、地区与 UI 差异影响
