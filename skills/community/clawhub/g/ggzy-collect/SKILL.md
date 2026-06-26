---
name: ggzy_collect
description: 从公共资源交易网站（淄博）抓取项目信息并保存到Excel。用于收集特定日期范围内的招标公告、中标信息等信息。触发场景：(1) 用户要求查询或收集公共资源交易信息 (2) 需要从ggzyjy.zibo.gov.cn抓取项目数据 (3) 需要将项目列表导出为Excel文件
---

# ggzy_collect - 公共资源交易信息收集

## 快速开始

1. 使用浏览器访问目标网站
2. 设置日期筛选条件
3. 翻页收集项目信息
4. 导出到Excel文件

## 网站信息

- **网站**: http://ggzyjy.zibo.gov.cn:8082/
- **栏目**: 公共资源子站 -> 建设工程 -> 招标公告/中标公示
- **URL模式**: `http://ggzyjy.zibo.gov.cn:8082/jyxx/002001/gonggongziyuan.html?Paging={页码}`

## 工作流程

### 1. 打开浏览器并导航

使用浏览器工具打开目标页面：
- 使用 profile="clawdbot-cn" 或 profile="chrome"（如果用户已连接Chrome扩展）
- 初始URL: `http://ggzyjy.zibo.gov.cn:8082/jyxx/002001/gonggongziyuan.html?Paging=1`

### 2. 设置日期筛选

页面通常有筛选器，可以按日期过滤：
- 找到日期筛选控件（通常在页面顶部）
- 设置开始日期和结束日期
- 点击"查询"或"确定"按钮

### 3. 翻页收集数据

- 点击"下一页"按钮继续浏览
- 每天一个表格，包含：项目地点、项目名称、发布时间
- 当遇到日期早于目标范围时停止

### 4. 数据格式

每个项目包含以下字段：
- **项目地点**: 如"市本级"、"张店区"等
- **项目名称**: 招标/中标项目标题
- **发布时间**: 格式如 "2026-03-20"

### 5. 保存到Excel

使用Node.js脚本创建Excel文件：

```javascript
const XLSX = require('xlsx');

const data = [
  ['项目地点', '项目名称', '发布时间'],
  ['市本级', 'XXX项目', '2026-03-20'],
  // ... 更多数据
];

const worksheet = XLSX.utils.aoa_to_sheet(data);
const workbook = XLSX.utils.book_new();
XLSX.utils.book_append_sheet(workbook, worksheet, '项目列表');

XLSX.writeFile(workbook, 'D:\\ggzyjy.zb\\output.xlsx');
```

或者使用VBS脚本创建Excel。

## 注意事项

- 翻页时等待页面加载完成
- 检查项目日期，确保在目标日期范围内
- Excel文件路径可以使用用户指定的路径
- 如果页面有反爬机制，适当增加等待时间