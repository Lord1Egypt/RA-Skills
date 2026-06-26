# 百度页面结构参考

## 百度首页结构

### URL
```
https://www.baidu.com
```

### 关键元素选择器

#### 搜索框
- **ID**: `#kw`
- **Name**: `wd`
- **Type**: `<input>`

#### 搜索按钮
- **ID**: `#su`
- **Value**: `"百度一下"`
- **Type**: `<input type="submit">`

## 搜索结果页结构

### URL 模式
```
https://www.baidu.com/s?wd={搜索词}
```

### 结果项选择器

#### 自然搜索结果
- **容器**: `.result` 或 `#content_left .result`
- **标题**: `h3 > a` 或 `.t > a`
- **摘要**: `.content-right_8Zs40` 或 `.c-abstract`
- **链接**: `h3 > a[href]`

#### 示例 HTML 结构
```html
<div class="result">
    <h3 class="t">
        <a href="https://example.com">搜索结果标题</a>
    </h3>
    <div class="c-abstract">
        搜索结果的摘要内容...
    </div>
    <div class="g">
        https://example.com
    </div>
</div>
```

## 页面操作说明

### 1. 输入搜索词
```javascript
// 定位搜索框并输入
document.querySelector('#kw').value = '搜索关键词';
```

### 2. 点击搜索
```javascript
// 点击搜索按钮
document.querySelector('#su').click();
// 或者
// 在搜索框按回车
document.querySelector('#kw').dispatchEvent(new KeyboardEvent('keydown', {key: 'Enter'}));
```

### 3. 等待结果
- 等待 URL 变为搜索结果页
- 等待 `#content_left` 元素加载完成
- 等待 `.result` 元素出现

## 反爬虫机制

### 常见验证码
- 图片验证码
- 滑动验证码
- 点击验证

### 应对建议
- 控制搜索频率
- 使用随机等待时间
- 必要时人工介入

## 移动端页面

### 移动版 URL
```
https://m.baidu.com
```

### 移动版选择器差异
- 搜索框: `#index-kw`
- 搜索按钮: `#index-bn`
- 结果项: `.result` (类名相似但结构可能不同)

## 更新记录

| 日期 | 变更内容 |
|------|----------|
| 2024-01 | 初始版本 |

> 注意：百度页面结构可能会更新，如遇到选择器失效请检查最新页面结构。
