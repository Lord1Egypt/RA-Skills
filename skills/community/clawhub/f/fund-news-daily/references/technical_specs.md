# 技术实现细节

## 首次使用：自动安装依赖

**执行流程：**
1. 检测 Agent Browser CLI：`agent-browser --version`
2. 如果未安装，执行：`npm install -g agent-browser`
3. 检测 python-docx：`python -c "import docx"`
4. 如果未安装，执行：`pip install python-docx`

## 数据源URL

| 平台 | URL |
|------|-----|
| 证券时报 | http://www.stcn.com/article/list/fund.html |
| 中国证券报 | https://www.cs.com.cn/tzjj/jjdt/ |
| 证券日报 | http://www.zqrb.cn/fund/ |
| 上海证券报 | https://www.cnstock.com/channel/10033 |
| 中国基金报 | https://www.chnfund.com/fund |

## 抓取命令

使用 Agent Browser CLI 进行页面抓取：

```bash
# 证券时报
agent-browser open "http://www.stcn.com/article/list/fund.html" --timeout 30000
agent-browser snapshot -c --timeout 20000

# 中国证券报
agent-browser open "https://www.cs.com.cn/tzjj/jjdt/" --timeout 30000
agent-browser snapshot -c --timeout 20000

# 证券日报
agent-browser open "http://www.zqrb.cn/fund/" --timeout 30000
agent-browser snapshot -c --timeout 20000

# 上海证券报
agent-browser open "https://www.cnstock.com/channel/10033" --timeout 30000
agent-browser snapshot -c --timeout 20000

# 中国基金报
agent-browser open "https://www.chnfund.com/fund" --timeout 30000
agent-browser snapshot -c --timeout 20000

# 完成后关闭
agent-browser close
```

## 注意事项

1. 严格按数据源顺序输出
2. 每个平台新闻按发布时间倒序排列
3. 无符合规则新闻时标注「本平台当日无符合规则新闻」
4. 内容概要直接摘抄原文核心内容，不做改写
5. 新闻链接必须为官方原文链接
