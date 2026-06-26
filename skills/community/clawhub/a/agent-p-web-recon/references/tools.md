# Web Recon 工具清单

## 被动收集（无痕迹）

### 搜索引擎
| 工具 | 用途 | 链接 |
|------|------|------|
| Google | 通用搜索 + 缓存 | `site:domain.com` |
| Bing | 备用搜索引擎 | `site:domain.com` |
| DuckDuckGo | 隐私搜索 | - |
| Shodan | IoT/服务器搜索 | shodan.io |
| Censys | 证书/主机搜索 | censys.io |

### 历史快照
| 工具 | 用途 | 链接 |
|------|------|------|
| Wayback Machine | 网页历史存档 | web.archive.org |
| Archive.today | 网页快照 | archive.today |
| Google Cache | 搜索引擎缓存 | `cache:url` |

### URL 发现
| 工具 | 安装 | 用途 |
|------|------|------|
| gau | `go install github.com/lc/gau` | 获取已知 URL |
| waybackurls | `go install github.com/tomnomnom/waybackurls` | 历史 URL |
| hakrawler | `go install github.com/hakluke/hakrawler` | 爬虫发现 |

---

## 半主动探测（低风险）

### 爬虫模拟
```bash
# 修改 User-Agent
curl -A "Googlebot/2.1" https://target.com

# 常见爬虫 UA
Googlebot/2.1 (+http://www.google.com/bot.html)
Bingbot/2.0 (+http://www.bing.com/bingbot.htm)
Mozilla/5.0 (compatible; YandexBot/3.0)
```

### RSS/Feed 发现
```bash
# 常见位置
/rss /rss.xml /feed /atom.xml /blog/rss

# 使用 hurl 测试
hurl --head https://target.com/rss
```

### 公共 API 探测
```bash
# 使用 gau + grep
gau target.com | grep -E "api|json|xml"

# 使用 httpx 探测
echo target.com | httpx -path /api/v1 -status-code
```

---

## 主动扫描（需授权）

### 目录扫描
| 工具 | 安装 | 特点 |
|------|------|------|
| dirsearch | `pip install dirsearch` | 经典，速度快 |
| gobuster | `go install github.com/OJ/gobuster` | Go 编写，稳定 |
| ffuf | `go install github.com/ffuf/ffuf` | 高度可配置 |
| feroxbuster | `cargo install feroxbuster` | Rust 编写，极速 |

### 常用字典
- `common.txt` - 通用路径
- `directory-list-2.3-medium.txt` - 中等规模
- `raft-medium-words.txt` - 综合字典
- 自定义字典 - 针对特定技术栈

### 前端分析
```bash
# 使用 browser 工具
# DevTools → Network → 分析 API 请求
# DevTools → Application → 查看 LocalStorage/SessionStorage
# DevTools → Sources → 查看 JS 源码
```

---

## 自动化脚本

### 内置脚本
| 脚本 | 用途 |
|------|------|
| `scripts/recon.sh` | 综合侦察（被动 + 主动） |
| `scripts/cache_viewer.py` | 缓存/快照查看器 |
| `scripts/scaffold.py` | 项目脚手架生成 |

### 快速命令
```bash
# 被动侦察
./recon.sh https://target.com --passive

# 主动侦察（需授权）
./recon.sh https://target.com --active

# 查看历史快照
python cache_viewer.py https://target.com --wayback
```

---

## 输出示例

### 报告结构
```markdown
## 侦察报告：target.com

### 发现内容
| 路径 | 内容 | 访问方式 | 风险 |
|------|------|----------|------|
| /api/posts | JSON | 公开 | 中 |
| /admin | HTML | 未授权 | 高 |

### 敏感暴露
- [ ] 用户数据
- [ ] 内部路径
- [ ] 配置文件
- [ ] 备份文件

### 修复建议
1. 添加鉴权中间件
2. 配置 robots.txt
3. 移除敏感路径
```

---

*P 注：工具是手段，不是目的。理解原理比记住命令更重要。*
