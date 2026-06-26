# Scrapling 解析 API 速查

在使用 Python 脚本提取网页内容时，参考以下常用的解析方法。

## 1. CSS 选择器
```python
# 获取所有匹配的文本
page.css('.quote .text::text').getall()

# 获取第一个匹配的文本
page.css('.quote')[0].css('.text::text').get()

# 获取属性
page.css('a::attr(href)').get()
```

## 2. XPath
```python
page.xpath('//div[@class="quote"]/span/text()').getall()
```

## 3. BeautifulSoup 风格
```python
# 查找所有匹配的元素
page.find_all('div', class_='quote')
page.find_all('div', {'class': 'quote'})

# 按文本查找
page.find_by_text('quote', tag='div')
```

## 4. 元素导航
```python
element.parent           # 父元素
element.next_sibling     # 下一个兄弟元素
element.below_elements() # 下方的元素
element.find_similar()   # 查找相似结构的元素
```