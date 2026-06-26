# Python Daily Poster

`Python Daily Poster` 是一个基于 JSON 规格生成中文信息海报的 Python 工具，适合做日报、榜单、资讯卡片这类固定版式输出。

当前内置两种海报类型：

- `daily`：生成 `摸鱼日报` 风格海报，可组合个人信息、摘要、倒计时、日程、语录等内容模块
- `baidu_hot`：生成 `百度热搜` 风格海报，按统一版式拉取并渲染热点榜单

默认输出 SVG，也支持按需导出 PNG/JPG/WEBP，方便接入自动化脚本、定时任务或内容发布流程。

## 安装

```bash
pip install -r requirements.txt
```

## 统一入口

```bash
# 摸鱼日报（daily）
python scripts/render_poster.py --type daily --spec references/daily-poster-spec.json --output out/daily_poster

# 百度热点 / 百度热搜（baidu_hot）
python scripts/render_poster.py --type baidu_hot --spec references/baidu-hot-spec.json --output out/baidu_hot_poster
```

也可以直接调用：

- `python scripts/render_daily_poster.py --spec ... --output ...`
- `python scripts/render_baidu_hot.py --spec ... --output ...`

## 示例展示

### 摸鱼日报 (`daily`)

![daily_poster 示例](assets/daily_poster.png)

### 百度热点 (`baidu_hot`)

![baidu_hot_poster 示例](assets/baidu_hot_poster.png)

## 摸鱼日报最小 JSON

```json
{
  "poster_type": "daily",
  "personal_info": {
    "name": "智普虾🦐",
    "bio_lines": [
      "OpenClaw 驱动的 AI 助手，搭载 GLM5 模型，机智温暖有点俏皮"
    ]
  }
}
```

## 百度热搜最小 JSON

```json
{
  "poster_type": "baidu_hot",
  "personal_info": {
    "name": "智普虾🦐",
    "bio_lines": [
      "OpenClaw 驱动的 AI 助手，搭载 GLM5 模型，机智温暖有点俏皮"
    ]
  },
  "output": {
    "formats": ["svg", "png"],
    "scale": 2
  }
}
```

## 约束

- `bio_lines` / `text_lines` 最多取前 `2` 行非空内容
- `baidu_hot` 固定使用代码内置 `title` / `subtitle` / `api_url` / `limit`
- `baidu_hot` 顶部日期区同一行显示公历、星期、农历
- 所有入口脚本都会输出统一 JSON 结果

## 项目目录架构

```text
daily-poster/
|-- .claude/                                        # 可选，本地开发工具配置目录（通常不提交）
|-- assets/                                         # README 中使用的示例海报图片
|   |-- baidu_hot_poster.png                        # 百度热搜海报示例图
|   `-- daily_poster.png                            # 摸鱼日报海报示例图
|-- out/                                            # 渲染输出目录
|   `-- .gitkeep                                    # 保持空目录被 Git 跟踪
|-- references/                                     # 示例规格、素材与参考文档
|   |-- cache/                                      # 本地缓存资源目录
|   |   `-- heisi-latest.jpg                        # 摸鱼日报示例中使用的黑丝日签缓存图
|   |-- baidu-hot-spec.json                         # 百度热搜海报示例输入
|   |-- daily-poster-spec.json                      # 摸鱼日报海报示例输入
|   |-- holiday-countdown-2026.json                 # 2026 节假日倒计时数据
|   `-- input-schema.md                             # 输入 JSON 字段说明
|-- scripts/                                        # 渲染器与运行时脚本
|   |-- generate_holiday_countdown.py               # 生成节假日倒计时数据文件
|   |-- holiday_countdown.py                        # 节假日倒计时解析与格式化逻辑
|   |-- lunar_calendar.py                           # 农历日期计算与格式化
|   |-- poster_runtime.py                           # 通用 CLI、输出与格式转换运行时
|   |-- render_baidu_hot.py                         # 百度热搜海报渲染器（内嵌百度 Logo base64）
|   |-- render_daily_poster.py                      # 摸鱼日报海报渲染器
|   |-- render_poster.py                            # 统一入口，按类型分发到不同渲染器
|   `-- svg_image_converter.py                      # SVG 导出为 PNG/JPG/WEBP 的转换工具
|-- .gitignore                                      # Git 忽略规则
|-- README.md                                       # 项目说明文档
|-- requirements.txt                                # Python 依赖列表
`-- SKILL.md                                        # 当前项目技能说明
```

## 致谢

- 项目中的部分动态内容接口由 [XXApi](https://xxapi.cn/about) 提供，包括百度热搜及部分 `daily` 模块所使用的数据能力。
