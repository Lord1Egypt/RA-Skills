# Boss直聘职位爬取 Skill

> 🕷️ 从 Boss 直聘批量提取职位详情（含 security_id、职位描述），支持 PUA 薪资解码和增量去重。

一个 [OpenClaw](https://github.com/openclaw/openclaw) Skill，帮助 AI Agent 或用户自动化爬取 Boss 直聘的职位数据。

---

## 功能特性

- 🔄 **智能滚动加载** — 使用 CDP 模拟真实鼠标滚轮，绕过 Boss 直聘反爬检测
- 🔐 **PUA 薪资解码** — 自动将 Boss 直聘的特殊 Unicode 字符还原为真实薪资数字
- 📋 **详情页深度提取** — 逐条打开详情页，提取 security_id 和完整职位描述
- 💾 **即时写入存储** — 每提取 1 条立即写入 CSV，中断不丢数据
- ✅ **质量报告** — 每次爬取后输出字段完整率和错误统计
- 🛡️ **两层容错** — 失败自动重试（指数退避），仍失败则跳过并记录错误日志
- 🕶️ **反爬优化** — 独立连接、随机等待、tab 即关，降低被检测风险

## 前置依赖

| 依赖 | 必需 | 说明 |
|------|------|------|
| Python 3.6+ | ✅ | 运行脚本 |
| websocket-client | ✅ | Python CDP 通信库 |
| CloakBrowser | ✅ | 反检测 Chromium 浏览器 |

## 安装

### 1. 克隆仓库

```bash
git clone https://github.com/iichaner/boss-resume-crawler.git
cd boss-resume-crawler
```

### 2. 安装 Python 依赖

```bash
pip3 install websocket-client
```

### 3. 安装 CloakBrowser

```bash
npm install cloakbrowser playwright-core

# 下载 Chromium（需要代理访问 GitHub）
export https_proxy=http://127.0.0.1:7890
curl -L --max-time 600 -o /tmp/cloakbrowser-darwin-x64.tar.gz <下载链接>
tar -xzf /tmp/cloakbrowser-darwin-x64.tar.gz -C ~/.cache/cloakbrowser/
```

> 📖 [CloakBrowser 文档](https://github.com/nickspaargaren/cloakbrowser)

## 快速开始

```bash
# 1. 启动 CloakBrowser（有头模式，必须）
open ~/.cache/cloakbrowser/Chromium.app --args \
  --remote-debugging-port=9222 \
  "--remote-allow-origins=*" \
  --user-data-dir=/tmp/chrome-cdp-profile \
  "https://www.zhipin.com/web/geek/jobs?query=总经理助理&city=101010100"

# 2. 在浏览器中扫码登录 Boss 直聘

# 3. 快速验证（爬取 5 条）
python3 scripts/boss_extract_cdp.py --max-scroll 3 --max-jobs 5 --output /tmp/boss_test

# 4. 正式爬取
python3 scripts/boss_extract_cdp.py --output ~/Desktop/jobs --max-scroll 50
```

## 脚本说明

| 脚本 | 用途 | 推荐度 |
|------|------|--------|
| `scripts/boss_extract_cdp.py` | **默认脚本**：纯 CDP 模式，反爬优化 | ⭐⭐⭐ 推荐 |
| `scripts/boss_extract_pure.py` | 旧版：纯 CDP 模式（无反爬优化） | ⭐ 备用 |
| `scripts/boss_extract_final.py` | agent-browser 模式 | ⭐⭐ 可选 |

### 默认脚本参数

```bash
python3 scripts/boss_extract_cdp.py [OPTIONS]

--output DIR       输出目录（默认当前目录）
--max-scroll N     最大滚动次数（默认 100）
--max-jobs N       最大爬取条数（默认全部）
--base-wait N      详情页基础等待秒数（默认 20）
```

### 示例

```bash
# 爬取全部职位，输出到桌面
python3 scripts/boss_extract_cdp.py --output ~/Desktop/jobs

# 只爬 20 条，滚动 30 次
python3 scripts/boss_extract_cdp.py --max-jobs 20 --max-scroll 30

# 网络较慢时增加等待
python3 scripts/boss_extract_cdp.py --base-wait 25
```

## 反爬设计

| 措施 | 实现 | 说明 |
|------|------|------|
| 有头模式 | CloakBrowser | headless 会被拦截 |
| 反检测浏览器 | CloakBrowser | 绕过自动化检测 |
| 真实滚轮模拟 | CDP `Input.dispatchMouseEvent` | 普通 scroll 不触发加载 |
| 随机滚动间隔 | 1.5-3.5 秒随机 | 模拟人类阅读节奏 |
| 随机详情页等待 | 20 秒 + 0-3 秒波动 | 降低请求规律性 |
| 独立 WebSocket 连接 | 每次操作新建，用完即关 | 防长连接被检测 |
| Tab 即关 | 提取后立即关闭 | 防 tab 堆积 |
| 指数退避重试 | +5 秒/次，最多 3 次 | 避免频繁重试触发风控 |

## 输出格式

### CSV 字段

| 字段名 | 说明 | 示例 |
|--------|------|------|
| 职位名称 | 职位标题 | 总经理助理 |
| 薪资 | PUA 解码后的真实薪资 | 15-20K·13薪 |
| 经验要求 | 工作经验 | 5-10年 |
| 学历要求 | 最低学历 | 本科 |
| 公司名称 | 招聘公司 | 某某科技有限公司 |
| 城市 | 工作城市 | 上海 |
| 区域 | 具体区域 | 浦东新区·张江 |
| job_id | Boss 直聘职位 ID | abc123def456 |
| security_id | 安全标识 | a1b2c3d4... |
| 职位描述 | 完整岗位职责和任职要求 | 负责协助总经理... |
| 创建日期 | 爬取时间 | 2026-06-01 20:50 |

### 质量报告示例

```
==================================================
爬取完成
==================================================
本次新增:     45 条
本次失败:     2 条
去重跳过:     3 条
累计总量:     128 条
输出文件:     /Users/ii/Desktop/jobs/jobs_data_20260601_2050.csv
错误日志:     /Users/ii/Desktop/jobs/temp/error_log.csv
```

## 常见问题

### Q: CDP 连接失败？

```bash
curl -s http://localhost:9222/json
```
返回页面列表即正常。如果为空，检查 CloakBrowser 是否启动。

### Q: 职位描述全部为空？

等待时间不足。使用 `--base-wait 25` 增加等待。

### Q: 滚动后职位数量不变？

脚本已使用 CDP `Input.dispatchMouseEvent mouseWheel`，如果仍无效，可能是网络问题或页面未登录。

### Q: 被风控拦截（ACCOUNT_RISK）？

- 使用新的 `--user-data-dir` 启动 CloakBrowser
- 减少 `--max-scroll` 次数
- 不要同时开多个爬取进程

### Q: CSV 打开乱码？

CSV 使用 `utf-8-sig` 编码。Excel 打开时选择 UTF-8，或用 WPS/文本编辑器打开。

## 项目结构

```
boss-resume-crawler/
├── SKILL.md                          # OpenClaw Skill 入口
├── README.md                         # 本文档
├── LICENSE                           # MIT 开源协议
├── references/
│   ├── sop.md                        # 详细操作流程（SOP）
│   ├── data-spec.md                  # 数据字段规格和选择器
│   └── error-handling.md             # 错误处理方案
└── scripts/
    ├── boss_extract_cdp.py           # 默认脚本（反爬优化）
    ├── boss_extract_pure.py          # 旧版备用脚本
    └── boss_extract_final.py         # agent-browser 模式脚本
```

## 更新日志

### v2.0.0 (2026-06-01)

**反爬优化重写：**
- ✨ 新增默认脚本 `boss_extract_cdp.py`（反爬优化版）
- 🔧 每次 CDP 操作新建独立 WebSocket 连接（修复超时问题）
- 🔧 每提取 1 条立即写入 CSV（修复中断丢数据问题）
- 🔧 详情页提取后立即关闭 tab（修复 tab 堆积问题）
- 🔧 所有等待时间加随机波动（增强反爬能力）
- 🔧 失败重试改为指数退避（+5 秒/次）
- 📝 更新 SKILL.md、SOP、错误处理文档

### v1.0.0 (2026-05-28)

- 🎉 初始版本
- 支持列表页滚动加载、详情页提取、PUA 薪资解码
- 支持 CSV 增量存储和跨文件去重

## License

[MIT](LICENSE)
