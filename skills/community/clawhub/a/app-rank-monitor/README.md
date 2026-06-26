# 点点数据自动获取工具

## 📊 功能概述

自动获取点点数据平台上架榜单数据，支持 12 个平台，自动发送到钉钉群。

## ✨ 核心功能

### 1. 支持平台 (12 个)
- **App Store**: 中国区
- **安卓渠道**: 华为、小米、vivo、OPPO、魅族、应用宝、百度、360、荣耀、鸿蒙、豌豆荚

### 2. 智能特性
- ✅ **浏览器后台常开**: 避免重复登录
- ✅ **自动登录**: Cookie 过期自动重新登录
- ✅ **智能检查**: 当天文件已存在则跳过
- ✅ **强制获取**: 支持 `--force` 参数重新获取
- ✅ **文件验证**: 下载后验证文件内容是否匹配
- ✅ **自动重试**: 文件不匹配自动重新下载
- ✅ **钉钉通知**: Markdown 格式 + TOP20 + Excel 附件

### 3. 安全机制
- ✅ 页面标题验证（防止获取错误平台数据）
- ✅ 文件内容验证（确保数据匹配当前渠道）
- ✅ 二次验证机制（不匹配自动重新下载）

## 🚀 快速开始

### 环境准备
```bash
cd ~/.openclaw/workspace/skills/app-rank-monitor

# 安装依赖
./venv/bin/pip install -r requirements.txt
```

### 配置
1. **点点数据账号**: `config/credentials.yaml`
```yaml
diandian:
  username: your_username
  password: your_password
```

2. **钉钉配置**: `config/dingtalk.yaml`
```yaml
dingtalk:
  client_id: "your_client_id"
  client_secret: "your_client_secret"
  chat_id: "your_chat_id"
  webhook: "your_webhook"
```

### 使用方法

#### 1. 启动浏览器（首次运行）
```bash
./tools/keep_browser_alive.sh
```

#### 2. 获取上架榜单
```bash
# 正常获取（文件存在则跳过）
./venv/bin/python tools/diandian_connect.py --platform <平台名称>

# 强制重新获取
./venv/bin/python tools/diandian_connect.py --platform <平台名称> --force
```

#### 3. 获取下架榜单
```bash
# 获取下架榜单
./venv/bin/python tools/diandian_connect.py --platform <平台名称> --offline

# 强制重新获取下架榜单
./venv/bin/python tools/diandian_connect.py --platform <平台名称> --offline --force
```

#### 4. 支持的平台名称
```bash
# App Store
./venv/bin/python tools/diandian_connect.py --platform appstore_cn

# 安卓渠道（上架榜）
./venv/bin/python tools/diandian_connect.py --platform huawei      # 华为
./venv/bin/python tools/diandian_connect.py --platform xiaomi     # 小米
./venv/bin/python tools/diandian_connect.py --platform vivo       # vivo
./venv/bin/python tools/diandian_connect.py --platform oppo       # OPPO
./venv/bin/python tools/diandian_connect.py --platform meizu      # 魅族
./venv/bin/python tools/diandian_connect.py --platform tencent    # 应用宝
./venv/bin/python tools/diandian_connect.py --platform baidu      # 百度
./venv/bin/python tools/diandian_connect.py --platform qihoo360   # 360
./venv/bin/python tools/diandian_connect.py --platform honor      # 荣耀
./venv/bin/python tools/diandian_connect.py --platform harmony    # 鸿蒙
./venv/bin/python tools/diandian_connect.py --platform wandoujia  # 豌豆荚

# 安卓渠道（下架榜）
./venv/bin/python tools/diandian_connect.py --platform huawei --offline
./venv/bin/python tools/diandian_connect.py --platform xiaomi --offline
# ... 其他平台同理
```

## 📁 文件结构

```
app-rank-monitor/
├── tools/
│   ├── diandian_connect.py      # 主程序
│   ├── diandian_auto_login.py   # 自动登录
│   └── keep_browser_alive.sh    # 浏览器后台运行
├── config/
│   ├── credentials.yaml         # 点点数据账号
│   └── dingtalk.yaml           # 钉钉配置
├── reports/                     # 下载的文件
└── README.md                    # 本文档
```

## 📊 输出示例

### 钉钉消息格式
```markdown
## 📊 点点数据 - 上架监控

**📅 数据日期**: 2026-03-24
**📱 平台**: 华为
**📈 类型**: 上架监控

---

### 📊 数据统计
- **新上架**: 120 个
- **恢复上架**: 15 个
- **总计**: 135 个

---

### 🔥 TOP 20 新上架
1. **应用名称 1** (分类)
2. **应用名称 2** (分类)
...

---

📄 完整数据：`huawei_new_apps_20260324.xlsx`
```

### 文件命名
- 格式：`{platform}_new_apps_{YYYYMMDD}.xlsx`
- 示例：`huawei_new_apps_20260324.xlsx`

## 🔧 高级配置

### 修改等待时间
在 `tools/diandian_connect.py` 中：
```python
# 导出后等待时间（默认 5 秒）
await asyncio.sleep(5)

# 重新下载前等待时间（默认 2 秒）
await asyncio.sleep(2)
```

### 修改验证逻辑
```python
def validate_excel_file(file_path: Path, platform_name: str) -> bool:
    """验证 Excel 文件内容是否匹配当前渠道"""
    # 读取前 3 行
    df = pd.read_excel(file_path, sheet_name=0, nrows=3)
    
    # 检查是否包含平台名称
    file_content = df.to_string().lower()
    return platform_name.lower() in file_content
```

## 📝 更新日志

### v2.0 (2026-03-24)
- ✅ 支持 12 个平台
- ✅ 添加页面标题验证
- ✅ 添加文件内容验证
- ✅ 自动重试机制
- ✅ 鸿蒙平台名称改为 harmony

### v1.0 (2026-03-23)
- ✅ 初始版本
- ✅ 支持华为、小米渠道
- ✅ 基础钉钉通知

## 🐛 常见问题

### 1. 文件内容不匹配
**现象**: 下载的文件是上一次导出的数据

**原因**: 点点数据导出有缓存机制，快速连续下载可能会拿到旧数据

**解决**: 
- ✅ 已自动修复，程序会自动重新下载（最多重试一次）
- 如果仍然失败，可以清空下载目录重试：
  ```bash
  rm -rf /var/folders/hv/ky0s2_b96k1f69x2z0my_8nc0000gn/T/playwright-artifacts-*
  ```

### 2. 页面标题不匹配
**现象**: 页面标题不包含平台名称

**解决**:
- 检查 URL 是否正确
- 检查平台名称拼写

### 3. 浏览器无法连接
**现象**: 提示无法连接到浏览器

**解决**:
```bash
# 重启浏览器
pkill -f "Chrome.*diandian"
./tools/keep_browser_alive.sh
```

### 4. 导出超时
**现象**: 60 秒超时未触发下载

**原因**: 点点数据生成导出文件需要时间，数据量大会比较慢

**解决**:
- ✅ 当前已配置 90 秒超时，可满足大部分情况
- 如果仍然超时，可以修改 `tools/diandian_connect.py` 中的 `download_timeout` 参数

## 📞 技术支持

如有问题，请联系开发团队。

## 📄 许可证

MIT License
