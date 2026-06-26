# 百度搜索示例

## 示例 1：基础搜索

### 用户需求
搜索 "Python 教程"

### 执行步骤

1. **打开百度首页**
   - 使用 browser_agent 访问 https://www.baidu.com

2. **输入搜索词**
   - 定位搜索框元素（通常是 `<input id="kw">`）
   - 输入 "Python 教程"

3. **执行搜索**
   - 点击搜索按钮（通常是 `<input type="submit" value="百度一下">`）
   - 或按回车键

4. **获取结果**
   - 等待页面加载完成
   - 提取搜索结果标题和链接

### 预期输出

```
搜索结果：
1. Python 教程 - 廖雪峰的官方网站
   https://www.liaoxuefeng.com/wiki/1016959663602400

2. Python 基础教程 | 菜鸟教程
   https://www.runoob.com/python/python-tutorial.html

3. Python 教程 - 官方文档
   https://docs.python.org/zh-cn/3/tutorial/
```

## 示例 2：技术问题搜索

### 用户需求
搜索 "requests SSL 错误"

### 执行步骤

1. 打开百度
2. 输入 "requests SSL 错误"
3. 执行搜索
4. 获取结果

### 常见结果类型
- 技术博客文章
- Stack Overflow 问答
- GitHub Issues
- 官方文档

## 示例 3：批量搜索

### 场景
需要搜索多个关键词

### 执行方式
逐个执行搜索，每次搜索前返回百度首页

```
for keyword in keywords:
    1. 打开百度首页
    2. 搜索 keyword
    3. 记录结果
    4. 返回首页
```

## 注意事项

- 搜索间隔建议保持在 2-3 秒以上，避免触发反爬虫
- 如果页面加载慢，适当延长等待时间
- 某些搜索结果可能需要登录才能查看完整内容
