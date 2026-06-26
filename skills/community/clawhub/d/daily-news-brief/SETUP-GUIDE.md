# 每日新闻简报Skill设置指南

## ✅ 已完成步骤

### 1. 依赖安装 ✅
- 已安装所有npm依赖包（112个）
- 创建了必要的目录结构（logs/, history/, templates/）

### 2. 测试运行 ✅
- 成功运行新闻简报系统
- 生成了今日新闻简报（2026年3月4日）
- 简报已保存到：
  - `latest-brief.md` - 最新简报
  - `history/2026-03-04.md` - 历史存档

## 🚀 下一步：设置定时任务

### 方法1：使用批处理文件（推荐）
1. **右键点击** `setup-task.bat`
2. 选择 **"以管理员身份运行"**
3. 按照提示完成设置

### 方法2：手动设置Windows计划任务
1. 打开 **"任务计划程序"** (`taskschd.msc`)
2. 点击 **"创建基本任务"**
3. 输入名称：`DailyNewsBrief`
4. 触发器：**每天**，时间：**08:00**
5. 操作：**启动程序**
6. 程序：`node`
7. 参数：`"C:\Users\User\.openclaw\workspace\skills\daily-news-brief\news-brief-simple.js"`
8. 起始于：`"C:\Users\User\.openclaw\workspace\skills\daily-news-brief"`

### 方法3：使用PowerShell脚本
```powershell
# 以管理员身份运行PowerShell
cd "C:\Users\User\.openclaw\workspace\skills\daily-news-brief"
.\setup-windows-task.ps1
```

## 📊 测试结果示例

### 生成的新闻简报内容：
```
# 📰 每日新闻简报 | 2026年3月4日 | 星期三

## 🌍 国际时事
1. 伊朗称完全控制霍尔木兹海峡... [央视]
2. 特朗普当年就伊朗挖苦奥巴马的言论... [新浪]
3. 美军在斯里兰卡海域袭击伊朗军舰... [新浪]

## 💰 经济形势
1. 避险不敌美联储，黄金高位闪崩 [新浪]
2. ATFX:黄金大跌逾4%后反弹... [新浪]

## 🔬 科技发展
1. 美考虑对中企买H200芯片"限购"... [新浪]
2. 苹果全线上调MacBook售价... [新浪]
```

## ⚙️ 配置说明

### 新闻源配置（可修改 `config.json`）
```json
{
  "newsSources": {
    "international": [
      "https://news.cctv.com/world",
      "https://news.sina.com.cn/world"
    ],
    "economic": [
      "https://finance.sina.com.cn"
    ],
    "technology": [
      "https://tech.sina.com.cn"
    ]
  }
}
```

### 优先级关键词（自动筛选）
- **国际**：特朗普、访华、中美、伊朗、中东
- **经济**：GDP、通胀、美联储、贸易、股市
- **科技**：AI、人工智能、芯片、电动、光伏

## 🔧 日常使用

### 手动运行
```bash
cd "C:\Users\User\.openclaw\workspace\skills\daily-news-brief"
node news-brief-simple.js
```

### 查看日志
```bash
# 查看运行日志
type logs\*.log

# 查看历史简报
dir history\
```

### 管理定时任务
```bash
# 查看任务状态
schtasks /query /tn DailyNewsBrief

# 立即运行任务
schtasks /run /tn DailyNewsBrief

# 删除任务
schtasks /delete /tn DailyNewsBrief /f
```

## 📈 扩展功能

### 1. 添加更多新闻源
编辑 `news-brief-simple.js`，在 `config.newsSources` 中添加URL

### 2. 调整发布时间
修改定时任务的触发器时间

### 3. 添加发布渠道
- 飞书集成：需要配置OpenClaw Feishu权限
- 微信机器人：需要配置微信API
- 邮件通知：添加SMTP配置

### 4. 自定义模板
编辑 `templates\brief-template.md` 文件

## 🆘 故障排除

### 常见问题

#### Q: 任务不执行
**A**: 
1. 检查任务计划程序中的任务状态
2. 确认node.js路径正确
3. 检查系统权限

#### Q: 新闻获取失败
**A**:
1. 检查网络连接
2. 确认新闻源URL可用
3. 查看错误日志

#### Q: 简报格式问题
**A**:
1. 检查HTML解析逻辑
2. 调整关键词过滤
3. 优化去重算法

### 日志位置
- 运行日志：`logs\` 目录
- 错误信息：控制台输出
- 历史简报：`history\` 目录

## 📞 支持信息

### 快速测试
```bash
# 测试新闻获取
cd "C:\Users\User\.openclaw\workspace\skills\daily-news-brief"
node news-brief-simple.js
```

### 验证安装
1. 检查 `node_modules` 目录是否存在
2. 检查 `latest-brief.md` 文件内容
3. 测试手动运行是否正常

### 获取帮助
- 查看 `README.md` 文件
- 检查控制台错误信息
- 查看系统事件日志

---

## 🎯 总结

### 已完成：
✅ 创建完整的新闻简报skill  
✅ 安装所有依赖包  
✅ 测试运行成功  
✅ 生成今日新闻简报  
✅ 创建定时任务设置脚本  

### 待完成：
🔲 以管理员身份运行 `setup-task.bat` 设置定时任务  
🔲 验证明天早上8点自动运行  
🔲 根据需要调整配置  

### 预期效果：
- 每天早上8点自动生成新闻简报
- 简报包含国际、经济、科技三个领域
- 特别关注特朗普访华等历史模式
- 自动保存历史记录
- 可通过飞书等渠道接收

---

**最后更新**: 2026年3月4日 21:25  
**状态**: 安装完成，待设置定时任务