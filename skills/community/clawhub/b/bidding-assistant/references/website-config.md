# 网站配置说明

## 目录
- [网站分类](#网站分类)
- [A类网站：政府采购](#a类网站政府采购)
- [B类网站：企业招标平台](#b类网站企业招标平台)
- [技术实现细节](#技术实现细节)

## 网站分类

### A类：政府采购网站（区域筛选）
此类网站需要采集后根据区域关键词（盐南高新区、经开区）进行筛选。

### B类：企业招标平台（全量采集）
此类网站全量采集所有公告，通过关键词过滤（公告、中标、结果、公示）。

## A类网站：政府采购

### 1. 盐城市政府采购网
- **网址**: `https://czj.yancheng.gov.cn/col/col2383/index.html`
- **状态**: ✅ 已实现
- **采集方式**: dataproxy接口（requests + 正则解析）
- **技术难度**: ⭐⭐ 中等
- **数据量**: 实时采集，根据日期范围动态获取
- **实现细节**:
  - 使用dataproxy接口获取JSON数据
  - URL参数: `?page=1&appid=1&webid=7&path=/&columnid={col_id}&unitid=135567&webname={encoded}&permissiontype=0`
  - 请求头: 需要特定的Referer和User-Agent
  - 数据解析: 使用正则表达式提取record元素中的字段
  - 13个子版块：采购意向、单一来源公示、资格预审和招标公告、竞争性谈判公告、竞争性磋商公告、询价公告、中标（成交）公告、终止公告、更正公告、其他公告、征集公告、入围公告、合同公告
  - 区域筛选: 匹配"盐南高新区"、"经开区"等关键词

### 2. 盐城市公共资源交易网
- **网址**: `https://yccggzy.jszwfw.gov.cn/tradeInfor?secondId=19&secondCode=transactionInfo`
- **状态**: ⏳ 待开发
- **采集方式**: playwright（动态加载）
- **技术难度**: ⭐⭐⭐ 中等

### 3. 开发区公共资源交易网
- **网址**: `http://218.92.181.186:8081/jyxx/about.html`
- **状态**: ✅ 已实现
- **采集方式**: requests + BeautifulSoup（静态HTML）
- **技术难度**: ⭐ 简单
- **区域特性**: 开发区网站，全量采集并标记为"经开区"
- **实现细节**:
  - 列表页URL: `http://218.92.181.186:8081/jyxx/about.html`
  - 链接格式: `/jyxx/{category}/{subcategory}/{date}/{uuid}.html`
  - 日期提取: 从URL路径中提取日期（格式YYYYMMDD）
  - 所有数据都标记为"经开区"，无需区域筛选
  - 支持招标公告、中标公告、采购公告等多种类型

### 3. 江苏世纪新城
- **网址**: `https://jscncg.com/tenderLease/tender/`
- **状态**: ✅ 已实现
- **采集方式**: requests + BeautifulSoup（静态HTML）
- **技术难度**: ⭐ 简单
- **数据量**: 共838条记录
- **区域特性**: 区域内公司，全量采集所有招投标信息
- **实现细节**:
  - 列表页URL: `https://jscncg.com/tenderLease/tender/`
  - 链接格式: `/tenderLease/tender/YYYY-MM-DD/{id}.html`
  - 数据结构: `<li myid="{id}"><a href="...">标题</a><span>日期</span></li>`
  - 日期提取: 从URL路径中提取日期（格式YYYY-MM-DD）
  - 区域标记: 标记为"区域内"，跳过关键词匹配

### 4. 城南新区公共资源交易网
- **网址**: `http://221.231.11.22:8099/jyxx/tradeInfo.html`
- **状态**: ✅ 已实现
- **采集方式**: requests + BeautifulSoup（静态HTML）
- **技术难度**: ⭐ 简单
- **实现细节**:
  - 列表页URL: `http://221.231.11.22:8099/jyxx/tradeInfo.html`
  - 链接格式: `/jyxx/{category}/{number}/{date}/{uuid}.html`
  - 日期提取: 从URL路径中提取日期（格式YYYYMMDD）
  - 已采集到"盐南高新区"相关项目4条（测试结果）

### 5. 中国政府采购网
- **网址**: `http://www.ccgp.gov.cn/`
- **状态**: ⏳ 待开发
- **采集方式**: playwright + 代理（动态+反爬）
- **技术难度**: ⭐⭐⭐⭐ 较难

### 6. 江苏政府采购网
- **网址**: `http://www.ccgp-jiangsu.gov.cn/`
- **状态**: ⏳ 待开发
- **采集方式**: playwright（动态加载）
- **技术难度**: ⭐⭐⭐ 中等

### 7. 江苏省公共资源交易网
- **网址**: `http://jsggzy.jszwfw.gov.cn/jyxx/tradeInfonew.html`
- **状态**: ⏳ 待开发
- **采集方式**: playwright（动态加载）
- **技术难度**: ⭐⭐⭐ 中等

### 8. 盐城市人民政府网
- **网址**: `https://www.yancheng.gov.cn/col/col16735/index.html`
- **状态**: ✅ 已实现
- **采集方式**: requests + BeautifulSoup（静态HTML + iframe）
- **技术难度**: ⭐ 简单
- **实现细节**:
  - 使用iframe加载内容: `/module/xxgk/search_custom.jsp?fieldConfigId=38195`
  - 分页采集，每页15条记录
  - 日期格式: `[2026-04-07]`
  - 数据量: 共2088条记录，140页
  - 区域筛选: 匹配"盐南高新区"、"经开区"等关键词

### 9. 江苏招标采购服务平台
- **网址**: `https://www.jszbcg.com/#/bulletin?page=1&category_id=88`
- **状态**: ⏳ 待开发
- **采集方式**: playwright（SPA单页应用）
- **技术难度**: ⭐⭐⭐ 中等

### 10. 全国招标采购公共服务平台
- **网址**: `https://www.hnzbcgxxw.com/list/4.html`
- **状态**: ✅ 已实现
- **采集方式**: requests + BeautifulSoup（静态HTML）
- **技术难度**: ⭐⭐ 简单
- **实现细节**:
  - 多分类采集: 招标/采购公告、中标/成交公告、变更/补充公告、其他公告/公示
  - 分页采集，每页10条记录
  - 日期格式: `2026-04-12`
  - 区域筛选: 匹配"盐南高新区"、"经开区"等关键词

### 11. 苏服采
- **网址**: `https://jsfwgov.cn/bidding?serviceType=1`
- **状态**: ✅ 已实现
- **采集方式**: Playwright浏览器自动化
- **技术难度**: ⭐⭐⭐ 中等
- **特殊处理**: 需要筛选地区（经开区、盐南高新区）
- **实现细节**:
  - 使用Playwright模拟浏览器操作
  - 自动识别区域选择器并选择区域
  - 支持JavaScript数据提取
  - 自动截图保存调试信息

## B类网站：企业招标平台

### 1. 盐城市大数据集团
- **网址**: `https://www.ycdatagroup.cn/news/19.html`
- **状态**: ✅ 已实现
- **采集方式**: requests + BeautifulSoup
- **URL格式**: `/news/show-{id}.html`
- **关键词过滤**: ["公告", "中标", "结果", "公示", "招标", "采购"]
- **日期提取**: 父级元素中的 `YYYY.MM.DD` 或 `YYYY-MM-DD`
- **区域特性**: 区域内公司，全量采集所有招投标信息
- **采集结果**: 测试采集到10条数据，全部标记为"区域内"

### 2. 盐城市东方集团
- **网址**: `https://www.orientalgroup.net.cn/zbzl/qzzgs/`
- **状态**: ✅ 已实现
- **采集方式**: requests + BeautifulSoup（静态HTML）
- **技术难度**: ⭐ 简单
- **数据量**: 共2229条记录
- **区域特性**: 区域内公司，全量采集所有招投标信息
- **实现细节**:
  - 列表页URL: `https://www.orientalgroup.net.cn/zbzl/qzzgs/`
  - 链接格式: `/zbzl/qzzgs/YYYY-MM-DD/{id}.html`
  - 数据结构: `<li><a class="col-xs-9" href="...">标题</a><span class="col-xs-3">日期</span></li>`
  - 日期提取: 从URL路径中提取日期（格式YYYY-MM-DD）
  - 区域标记: 标记为"区域内"，跳过关键词匹配

### 3. 江苏世纪新城
- **网址**: `https://jscncg.com/tenderLease/tender/`
- **状态**: ✅ 已实现
- **采集方式**: requests + BeautifulSoup（静态HTML）
- **技术难度**: ⭐ 简单
- **数据量**: 共838条记录
- **区域特性**: 区域内公司，全量采集所有招投标信息
- **实现细节**:
  - 列表页URL: `https://jscncg.com/tenderLease/tender/`
  - 链接格式: `/tenderLease/tender/YYYY-MM-DD/{id}.html`
  - 数据结构: `<li myid="{id}"><a href="...">标题</a><span>日期</span></li>`
  - 日期提取: 从URL路径中提取日期（格式YYYY-MM-DD）
  - 区域标记: 标记为"区域内"，跳过关键词匹配

### 4. 盐城市都市建设投资集团
- **网址**: `http://www.ycdsjt.cn/?zhaobiao/`
- **状态**: ✅ 已实现
- **采集方式**: requests + BeautifulSoup
- **URL格式**: `/?tongzhi/{id}.html` 或 `/?zhaobiao/{id}.html`
- **日期提取**: 默认使用当天日期
- **分类**: 多分类（通知、招标）
- **区域特性**: 区域内公司，全量采集所有招投标信息
- **采集结果**: 测试采集到45条数据，全部标记为"区域内"

### 5. 经开城发集团
- **网址**: `http://www.ycjkct.com/zbcg/zbxx/`（招标信息）、`http://www.ycjkct.com/zbcg/zbgs/`（中标信息）
- **状态**: ✅ 已实现
- **采集方式**: requests + BeautifulSoup
- **URL格式**: `/zbcg/{分类}/YYYY-MM-DD/{id}.html`
- **分类**: 2个（招标信息、中标信息）
- **区域特性**: 区域内公司，全量采集所有招投标信息
- **采集结果**: 测试采集到50条数据（招标25条+中标25条），全部标记为"区域内"

### 6. 悦达集团-阳光采购平台
- **网址**: `http://www.ydtender.com/`
- **状态**: ✅ 已实现
- **采集方式**: requests + BeautifulSoup
- **子分类**: 12个
- **URL格式**: `/{分类代码}/{id}.jhtml`
- **日期提取**: 从`<p class="Gray">`中提取"发布时间"
- **数据结构**: `<div class="List2"><ul><li><a>`嵌套结构
- **区域特性**: 区域内公司，全量采集所有招投标信息
- **采集结果**: 测试采集到120条数据（12个分类各10条），全部标记为"区域内"

#### 悦达集团子分类列表
```
https://www.ydtender.com/zbgg/index.jhtml      # 综合公告汇总页
https://www.ydtender.com/zgcgg/index.jhtml     # 工程公告
https://www.ydtender.com/zhwgg/index.jhtml     # 货物公告
https://www.ydtender.com/zfwgg/index.jhtml     # 服务公告
https://www.ydtender.com/jgcgg/index.jhtml     # 结果公告-工程
https://www.ydtender.com/jhwgg/index.jhtml     # 结果公告-货物
https://www.ydtender.com/jfwgg/index.jhtml     # 结果公告-服务
https://www.ydtender.com/pgcgg/index.jhtml     # 评审公示-工程
https://www.ydtender.com/phwgg/index.jhtml     # 评审公示-货物
https://www.ydtender.com/pfwgg/index.jhtml     # 评审公示-服务
https://www.ydtender.com/yyzbgg/index.jhtml    # 运营采购公告
https://www.ydtender.com/yyjggg/index.jhtml    # 运营结果公告
https://www.ydtender.com/yygyszj/index.jhtml   # 供应商征集
```

## 技术实现细节

### 通用关键词过滤
```python
KEYWORDS = ["公告", "中标", "结果", "公示"]
```

### 区域关键词配置
```python
REGION_KEYWORDS = {
    "盐南高新区": ["盐南高新区", "盐南", "城南新区", "城南"],
    "经开区": ["经开区", "经济技术开发区", "开发区"]
}
```

### 日期格式标准化
- 常见格式: `2026.04.12` → `2026-04-12`
- URL格式: `/2026-04-12/` → `2026-04-12`

### 去重策略
- 唯一标识: MD5(项目名称 + 发布日期 + 来源网站)
- 内容哈希: MD5(完整项目JSON)

## 注意事项

1. **实际可用网站**: 3个网站可正常采集并返回数据
   - ✅ 盐城市大数据集团（可用，测试采集10条）
   - ✅ 盐城市都市建设投资集团（可用，测试采集45条）
   - ✅ 悦达集团（可用，测试采集120条）

2. **被拦截网站**: 2个网站需要技术方案绕过反爬
   - ⚠️ 盐城市政府采购网（WAF拦截，需要Playwright）
   - ⚠️ 经开城投集团（反爬拦截，需要优化请求头）

3. **无法访问网站**: 2个网站域名可能已失效
   - ❌ 江苏世纪新城（DNS解析失败）
   - ❌ 盐城市东方集团（DNS解析失败）

4. **详细校验报告**: 请参见 [verification-report.md](verification-report.md)

5. **反爬策略**:
   - 设置合理的请求间隔（1-2秒）
   - 使用随机User-Agent
   - 必要时使用代理IP
   - 被拦截网站建议使用Playwright

6. **错误处理**:
   - 网络超时重试3次
   - 解析失败记录原始HTML
   - 异常情况记录日志

## 扩展开发

### 添加新网站适配器
1. 继承 `BaseCrawler` 类
2. 实现 `crawl(start_date, end_date)` 方法
3. 返回格式: `{"total": int, "new": int}`
4. 在 `main()` 函数中添加到爬虫列表

### 示例
```python
class NewSiteCrawler(BaseCrawler):
    SITE_NAME = "新网站名称"
    BASE_URL = "https://example.com"

    def crawl(self, start_date: str, end_date: str) -> Dict:
        # 实现采集逻辑
        pass
```
